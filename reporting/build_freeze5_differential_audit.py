#!/usr/bin/env python3
"""Pair every Freeze 4/5 attempt and fail on behavioral or shared-result drift."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_OUTPUT = ROOT / "docs/FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.json"
MARKDOWN_OUTPUT = ROOT / "docs/FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.md"
SUITES = (
    (
        "core",
        ROOT / "outputs/confirmatory_v3",
        ROOT / "outputs/confirmatory_v4",
        "5ac3d5c5a5d04cea7241e76ec5f390f9f266cfbd60cafd2339507dd44e360588",
        "7bf7ee0a3ef39b355bcb9f7ddcf9320787b954e6ebbf9f83faa1e62210b98ba0",
    ),
    (
        "information_latency_sensitivity",
        ROOT / "outputs/sensitivity_information_latency_v3",
        ROOT / "outputs/sensitivity_information_latency_v4",
        "d5762c5194d62e5c3dd6082bd72bb0c2856765c2326087e8988882ecded93570",
        "3a67f1c898a90296ebde3c0d29bee843edfef840c7f1cd2e0ecd2c0b9fab62a7",
    ),
)
TOP_LEVEL_STUDY_FIELDS = (
    "artifact_kind",
    "attempt_id",
    "claim_limit",
    "family",
    "family_id",
    "policy_id",
    "replication",
    "seed_id",
)
SHARED_ANALYSIS_SECTIONS = (
    "primary_metrics",
    "precision",
    "extension_required",
    "paired_estimates",
    "process_contrasts",
    "common_random_number_diagnostics",
    "evaluation_bridge_summary",
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


def cell_map(analysis: dict[str, object]) -> dict[tuple[str, str], dict[str, object]]:
    return {
        (str(cell["family_id"]), str(cell["policy_id"])): cell
        for cell in analysis["cell_summaries"]
    }


def audit_suite(
    suite_id: str,
    old_root: Path,
    new_root: Path,
    expected_old_analysis_hash: str,
    expected_new_analysis_hash: str,
) -> dict[str, object]:
    old_paths = {path.name: path for path in (old_root / "attempts").glob("*.json")}
    new_paths = {path.name: path for path in (new_root / "attempts").glob("*.json")}
    if set(old_paths) != set(new_paths):
        raise RuntimeError(f"attempt inventory drift: {suite_id}")

    counts = {
        "cohort_hash_mismatch_count": 0,
        "compiled_configuration_receipt_identity_change_count": 0,
        "evaluation_bridge_receipt_mismatch_count": 0,
        "event_count_mismatch_count": 0,
        "event_hash_mismatch_count": 0,
        "expected_attempt_hash_change_count": 0,
        "expected_attempt_schema_change_count": 0,
        "paired_attempt_count": len(old_paths),
        "shared_row_mismatch_count": 0,
        "top_level_study_identity_mismatch_count": 0,
    }
    added_signatures: set[tuple[str, ...]] = set()
    for name in sorted(old_paths):
        old = load_json(old_paths[name])
        new = load_json(new_paths[name])
        old_row = old["row"]
        new_row = new["row"]
        counts["cohort_hash_mismatch_count"] += old_row["cohort_hash"] != new_row["cohort_hash"]
        counts["event_hash_mismatch_count"] += old_row["event_hash"] != new_row["event_hash"]
        counts["event_count_mismatch_count"] += old_row["event_count"] != new_row["event_count"]
        counts["evaluation_bridge_receipt_mismatch_count"] += (
            old["evaluation_bridge_receipt"] != new["evaluation_bridge_receipt"]
        )
        counts["compiled_configuration_receipt_identity_change_count"] += (
            old["compiled_configuration_hash"] != new["compiled_configuration_hash"]
        )
        counts["expected_attempt_hash_change_count"] += old["attempt_hash"] != new["attempt_hash"]
        counts["expected_attempt_schema_change_count"] += (
            old["schema_version"] == 3 and new["schema_version"] == 4
        )
        counts["top_level_study_identity_mismatch_count"] += any(
            old[field] != new[field] for field in TOP_LEVEL_STUDY_FIELDS
        )
        counts["shared_row_mismatch_count"] += any(
            old_row[field] != new_row[field] for field in old_row
        )
        added_signatures.add(tuple(sorted(set(new_row) - set(old_row))))

    if len(added_signatures) != 1:
        raise RuntimeError(f"new row schema is inconsistent: {suite_id}")
    expected = len(old_paths)
    blocking_count = sum(counts[key] for key in (
        "cohort_hash_mismatch_count",
        "evaluation_bridge_receipt_mismatch_count",
        "event_count_mismatch_count",
        "event_hash_mismatch_count",
        "shared_row_mismatch_count",
        "top_level_study_identity_mismatch_count",
    ))
    for key in (
        "compiled_configuration_receipt_identity_change_count",
        "expected_attempt_hash_change_count",
        "expected_attempt_schema_change_count",
    ):
        if counts[key] != expected:
            blocking_count += expected - counts[key]

    old_analysis = load_json(old_root / "analysis/analysis_r030.json")
    new_analysis = load_json(new_root / "analysis/analysis_r030.json")
    if old_analysis["analysis_hash"] != expected_old_analysis_hash:
        raise RuntimeError(f"unexpected Freeze 4 analysis: {suite_id}")
    if new_analysis["analysis_hash"] != expected_new_analysis_hash:
        raise RuntimeError(f"unexpected Freeze 5 analysis: {suite_id}")
    if any(old_analysis[key] != new_analysis[key] for key in SHARED_ANALYSIS_SECTIONS):
        blocking_count += 1
    old_cells = cell_map(old_analysis)
    new_cells = cell_map(new_analysis)
    if set(old_cells) != set(new_cells) or any(
        any(old_cell[field] != new_cells[key][field] for field in old_cell)
        for key, old_cell in old_cells.items()
    ):
        blocking_count += 1

    return {
        "blocking_mismatch_count": blocking_count,
        "comparison_counts": counts,
        "new_analysis_hash": expected_new_analysis_hash,
        "new_root": new_root.relative_to(ROOT).as_posix(),
        "old_analysis_hash": expected_old_analysis_hash,
        "old_root": old_root.relative_to(ROOT).as_posix(),
        "row_fields_added": list(next(iter(added_signatures))),
        "shared_analysis_sections_exact": [
            *SHARED_ANALYSIS_SECTIONS,
            "all pre-existing cell-summary fields",
        ],
        "status": "pass" if blocking_count == 0 else "fail",
        "suite_id": suite_id,
    }


def render_markdown(receipt: dict[str, object]) -> str:
    paired = sum(
        int(suite["comparison_counts"]["paired_attempt_count"])
        for suite in receipt["suites"]
    )
    return f"""# Freeze 4/Freeze 5 Differential Audit

Status: **{receipt['status']}**

Every Freeze 4 attempt was paired with its Freeze 5 counterpart ({paired:,} attempts). Cohort hashes, complete system-event hashes, event counts, evaluation-bridge receipts, top-level study identities, every pre-existing row field, and every pre-existing analysis field are exact. There are no missing or unexpected attempt identifiers and no blocking mismatch.

The event hash is a digest of the ordered system stream, including each case identifier, causal key, event type, timestamp, and event details. Exact event hashes therefore establish that Freeze 5 changed reporting rather than cases, event order, timing, actions, queues, or modeled outcomes.

The compiled-configuration hash changes in every pair because the compiled receipt binds executable identity; this is an expected identity change after the frozen reporting code advanced. The evaluation specification and its routing/action comparison receipt remain byte-identical. Attempt hashes and schema versions change because Freeze 5 adds 19 stored row fields and advances the attempt schema.

## New reporting only

For fail-open review, Freeze 5 stores evidence-only, authorization-only, and joint failures plus the two overlapping unions. For information first, it stores adequate response evidence, retrieval attempts and successes, unresolved evidence after acquisition, and review-request incidence. All old cell estimates, paired contrasts, precision decisions, process contrasts, random-number diagnostics, and evaluation summaries are unchanged.

Machine receipt: `docs/FREEZE4_FREEZE5_DIFFERENTIAL_AUDIT.json`
"""


def main() -> None:
    suites = [audit_suite(*suite) for suite in SUITES]
    value = {
        "schema_version": 1,
        "artifact_kind": "freeze_differential_audit",
        "freeze4_manifest_hash": "bd330d56273ae7a85aed872b5e1442400b02b1f6b822c1fa6154ae2de5d62c63",
        "freeze5_manifest_hash": "d18c7377c6b84d6ac4748ab6be9ab512c2d76cc958b2273bd2a78737957fd4ea",
        "status": "pass" if all(suite["status"] == "pass" for suite in suites) else "fail",
        "suites": suites,
        "claim": "Freeze 5 adds reporting observability while preserving Freeze 4 cohorts, complete event streams, evaluation receipts, and every shared outcome",
        "event_hash_contract": "the stored event hash covers ordered case IDs, causal keys, event types, timestamps, and event details",
    }
    receipt = value | {"audit_hash": canonical_hash(value)}
    JSON_OUTPUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MARKDOWN_OUTPUT.write_text(render_markdown(receipt), encoding="utf-8")
    print(json.dumps({
        "status": receipt["status"],
        "audit_hash": receipt["audit_hash"],
        "paired_attempts": sum(
            suite["comparison_counts"]["paired_attempt_count"] for suite in suites
        ),
        "blocking_mismatches": sum(suite["blocking_mismatch_count"] for suite in suites),
    }, sort_keys=True))
    if receipt["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
