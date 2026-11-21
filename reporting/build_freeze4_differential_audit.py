#!/usr/bin/env python3
"""Pair Freeze 3 and Freeze 4 attempts and classify every permitted difference."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / "docs/FREEZE3_FREEZE4_DIFFERENTIAL_AUDIT.json"
MARKDOWN_OUTPUT = ROOT / "docs/FREEZE3_FREEZE4_DIFFERENTIAL_AUDIT.md"
SUITES = (
    ("core", "outputs/confirmatory_v2", "outputs/confirmatory_v3", "CONFIRMATORY-V2", "CONFIRMATORY-V3"),
    (
        "information_latency_sensitivity",
        "outputs/sensitivity_information_latency_v2",
        "outputs/sensitivity_information_latency_v3",
        "SENSITIVITY-INFORMATION-LATENCY-V2",
        "SENSITIVITY-INFORMATION-LATENCY-V3",
    ),
)
SHARED_ROW_FIELDS = (
    "family_id",
    "load",
    "missing_evidence",
    "access_barrier",
    "retrievability",
    "staff_access",
    "replication",
    "policy_id",
    "case_count",
    "event_count",
    "cohort_hash",
    "event_hash",
    "unsupported_progression_rate",
    "recipient_burden_rate",
    "agency_workload_rate",
    "censoring_reason_counts",
    "review_mean_wait_time",
    "correction_mean_exposure_time",
)
SHARED_CELL_METRICS = (
    "unsupported_progression_rate",
    "recipient_burden_rate",
    "agency_workload_rate",
)


def canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"artifact is not a mapping: {path}")
    return value


def self_hash_valid(value: Mapping[str, object], field: str) -> bool:
    candidate = dict(value)
    observed = candidate.pop(field, None)
    return observed == canonical_hash(candidate)


def _cell_map(analysis: Mapping[str, object]) -> dict[tuple[str, str], Mapping[str, object]]:
    return {
        (str(cell["family_id"]), str(cell["policy_id"])): cell
        for cell in analysis["cell_summaries"]
    }


def audit_suite(
    suite_id: str,
    old_root: Path,
    new_root: Path,
    old_config_id: str,
    new_config_id: str,
) -> dict[str, object]:
    old_attempts = old_root / "attempts"
    new_attempts = new_root / "attempts"
    old_names = {path.name for path in old_attempts.glob("*.json")}
    new_names = {path.name for path in new_attempts.glob("*.json")}
    missing = sorted(old_names - new_names)
    unexpected = sorted(new_names - old_names)
    counters: Counter[str] = Counter()
    added_signatures: Counter[tuple[str, ...]] = Counter()
    removed_signatures: Counter[tuple[str, ...]] = Counter()
    first_failures: list[dict[str, object]] = []

    for name in sorted(old_names & new_names):
        old = load_json(old_attempts / name)
        new = load_json(new_attempts / name)
        old_row = old["row"]
        new_row = new["row"]
        counters["paired_attempt_count"] += 1
        for field in ("attempt_id", "family_id", "family", "replication", "policy_id", "seed_id", "compiled_configuration_hash"):
            if old.get(field) != new.get(field):
                counters[f"top_level_{field}_mismatch_count"] += 1
        if old.get("config_id") == old_config_id and new.get("config_id") == new_config_id:
            counters["expected_config_identity_change_count"] += 1
        else:
            counters["unexpected_config_identity_count"] += 1
        if old.get("manifest_hash") != new.get("manifest_hash"):
            counters["expected_manifest_identity_change_count"] += 1
        else:
            counters["unexpected_manifest_identity_equality_count"] += 1
        if old.get("schema_version") == 2 and new.get("schema_version") == 3:
            counters["expected_attempt_schema_change_count"] += 1
        else:
            counters["unexpected_attempt_schema_count"] += 1
        if old.get("attempt_hash") != new.get("attempt_hash"):
            counters["expected_attempt_hash_change_count"] += 1
        else:
            counters["unexpected_attempt_hash_equality_count"] += 1
        if old.get("evaluation_bridge_receipt") != new.get("evaluation_bridge_receipt"):
            counters["support_receipt_mismatch_count"] += 1
        if old_row.get("cohort_hash") != new_row.get("cohort_hash"):
            counters["cohort_hash_mismatch_count"] += 1
        if old_row.get("event_hash") != new_row.get("event_hash"):
            counters["event_hash_mismatch_count"] += 1
        for field in SHARED_ROW_FIELDS:
            if old_row.get(field) != new_row.get(field):
                counters[f"shared_row_{field}_mismatch_count"] += 1
        if old_row.get("unresolved_hold_rate") != new_row.get("held_rate"):
            counters["held_rate_bridge_mismatch_count"] += 1
        recovery_entry_rate = (
            int(new_row["supported_recovery_entry_count"])
            + int(new_row["unsupported_recovery_entry_count"])
        ) / int(new_row["case_count"])
        if float(old_row["recovery_exposure_rate"]) != recovery_entry_rate:
            counters["recovery_entry_bridge_mismatch_count"] += 1
        right_censored_rate = sum(int(value) for value in new_row["censoring_reason_counts"].values()) / int(new_row["case_count"])
        if float(old_row["right_censored_rate"]) != right_censored_rate:
            counters["censoring_reason_bridge_mismatch_count"] += 1
        if int(new_row["timely_review_count"]) + int(new_row["timeout_activation_count"]) != int(new_row["review_request_count"]):
            counters["timeout_partition_mismatch_count"] += 1
        if sum(int(new_row[field]) for field in (
            "supported_progression_count", "unsupported_progression_count",
            "evidence_requested_count", "held_count", "pre_action_open_count",
        )) != int(new_row["case_count"]):
            counters["decision_partition_mismatch_count"] += 1
        if sum(int(new_row[field]) for field in (
            "supported_recovery_entry_count", "unsupported_recovery_entry_count",
            "no_recovery_entry_count",
        )) != int(new_row["case_count"]):
            counters["recovery_partition_mismatch_count"] += 1
        old_keys = set(old_row)
        new_keys = set(new_row)
        added_signatures[tuple(sorted(new_keys - old_keys))] += 1
        removed_signatures[tuple(sorted(old_keys - new_keys))] += 1
        blocking_now = sum(
            counters[key] for key in (
                "cohort_hash_mismatch_count",
                "event_hash_mismatch_count",
                "support_receipt_mismatch_count",
                "decision_partition_mismatch_count",
                "recovery_partition_mismatch_count",
                "timeout_partition_mismatch_count",
            )
        )
        if blocking_now and len(first_failures) < 5:
            first_failures.append({"attempt": name, "blocking_mismatch_total": blocking_now})

    old_analysis = load_json(old_root / "analysis/analysis_r030.json")
    new_analysis = load_json(new_root / "analysis/analysis_r030.json")
    old_cells = _cell_map(old_analysis)
    new_cells = _cell_map(new_analysis)
    cell_mismatches: Counter[str] = Counter()
    if set(old_cells) != set(new_cells):
        cell_mismatches["cell_inventory_mismatch_count"] += 1
    for key in sorted(set(old_cells) & set(new_cells)):
        for metric in SHARED_CELL_METRICS:
            for field in (metric, f"{metric}_mcse"):
                if old_cells[key].get(field) != new_cells[key].get(field):
                    cell_mismatches[f"{field}_mismatch_count"] += 1
        if old_cells[key].get("unresolved_hold_rate") != new_cells[key].get("held_rate"):
            cell_mismatches["held_rate_bridge_mismatch_count"] += 1
    bridge_equal = old_analysis.get("evaluation_bridge_summary") == new_analysis.get("evaluation_bridge_summary")
    blocking_keys = (
        "cohort_hash_mismatch_count",
        "event_hash_mismatch_count",
        "support_receipt_mismatch_count",
        "decision_partition_mismatch_count",
        "recovery_partition_mismatch_count",
        "timeout_partition_mismatch_count",
        "held_rate_bridge_mismatch_count",
        "recovery_entry_bridge_mismatch_count",
        "censoring_reason_bridge_mismatch_count",
        "unexpected_config_identity_count",
        "unexpected_manifest_identity_equality_count",
        "unexpected_attempt_schema_count",
    )
    blocking_count = sum(counters[key] for key in blocking_keys) + sum(cell_mismatches.values())
    if not bridge_equal:
        blocking_count += 1
    return {
        "suite_id": suite_id,
        "status": "pass" if not missing and not unexpected and blocking_count == 0 else "fail",
        "old_root": old_root.relative_to(ROOT).as_posix(),
        "new_root": new_root.relative_to(ROOT).as_posix(),
        "old_attempt_count": len(old_names),
        "new_attempt_count": len(new_names),
        "missing_attempt_ids": missing,
        "unexpected_attempt_ids": unexpected,
        "comparison_counts": dict(sorted(counters.items())),
        "shared_cell_comparison_counts": dict(sorted(cell_mismatches.items())),
        "evaluation_bridge_summary_exact": bridge_equal,
        "row_fields_added_signatures": [
            {"fields": list(fields), "attempt_count": count}
            for fields, count in sorted(added_signatures.items())
        ],
        "row_fields_removed_signatures": [
            {"fields": list(fields), "attempt_count": count}
            for fields, count in sorted(removed_signatures.items())
        ],
        "classified_event_difference_counts": {
            "identity_only_serialization": counters["expected_attempt_hash_change_count"],
            "compiled_configuration_receipt_identity": counters[
                "top_level_compiled_configuration_hash_mismatch_count"
            ],
            "event_detail": 0,
            "event_order": 0,
            "timestamp": 0,
            "action": 0,
            "queue": 0,
            "outcome": 0,
            "unresolved_event_hash_mismatch": counters["event_hash_mismatch_count"],
        },
        "first_failures": first_failures,
        "blocking_mismatch_count": blocking_count,
        "old_analysis_hash": old_analysis["analysis_hash"],
        "new_analysis_hash": new_analysis["analysis_hash"],
    }


def render_markdown(receipt: Mapping[str, object]) -> str:
    lines = [
        "# Freeze 3/Freeze 4 Differential Audit",
        "",
        f"Status: **{receipt['status']}**",
        "",
        "This audit pairs every stored Freeze 3 and Freeze 4 attempt. It tests behavioral continuity separately from the expected metric-schema, configuration, manifest, and attempt-hash changes.",
        "",
        "| Suite | Paired attempts | Cohort mismatches | Event mismatches | Support-receipt mismatches | Blocking mismatches |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for suite in receipt["suites"]:
        counts = suite["comparison_counts"]
        lines.append(
            f"| {suite['suite_id']} | {counts.get('paired_attempt_count', 0):,} | "
            f"{counts.get('cohort_hash_mismatch_count', 0):,} | "
            f"{counts.get('event_hash_mismatch_count', 0):,} | "
            f"{counts.get('support_receipt_mismatch_count', 0):,} | "
            f"{suite['blocking_mismatch_count']:,} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "Exact cohort hashes, event hashes, evaluation-bridge receipts, shared valid metrics, held-state bridges, recovery-entry bridges, and stage-coded censoring bridges establish that Freeze 4 changed measurement and reporting rather than generated behavior. Attempt hashes change because the configuration identity, manifest identity, schema version, and stored row fields changed.",
        "",
        "`DecisionServiceEffective` and the aggregate censoring rate were removed from primary reporting. Conditional review and gate measures now store raw counts, use null for non-applicability, and are aggregated by ratio of sums. The five decision states and three recovery-entry states are new measurements of unchanged traces.",
        "",
        f"Machine receipt: `{JSON_OUTPUT.relative_to(ROOT).as_posix()}`",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    suites = [
        audit_suite(suite_id, ROOT / old, ROOT / new, old_id, new_id)
        for suite_id, old, new, old_id, new_id in SUITES
    ]
    value = {
        "schema_version": 1,
        "artifact_kind": "freeze_differential_audit",
        "freeze3_manifest_hash": "47170f8cb450709b19f0bf47b48b887208ee75cde07dbf1ee34169891f6b9c6b",
        "freeze4_manifest_hash": "bd330d56273ae7a85aed872b5e1442400b02b1f6b822c1fa6154ae2de5d62c63",
        "status": "pass" if all(suite["status"] == "pass" for suite in suites) else "fail",
        "suites": suites,
        "claim": "measurement-only Freeze 4 changes preserve generated cohort, event, action-support, queue, and shared valid outcome identities",
    }
    receipt = value | {"audit_hash": canonical_hash(value)}
    JSON_OUTPUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MARKDOWN_OUTPUT.write_text(render_markdown(receipt), encoding="utf-8")
    print(json.dumps({
        "status": receipt["status"],
        "audit_hash": receipt["audit_hash"],
        "paired_attempts": sum(suite["comparison_counts"]["paired_attempt_count"] for suite in suites),
        "blocking_mismatches": sum(suite["blocking_mismatch_count"] for suite in suites),
    }, sort_keys=True))
    if receipt["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
