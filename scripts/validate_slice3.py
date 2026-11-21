"""Blocking Slice 3 engineering and reporting-rehearsal validator."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uncertainty_permission_simulation.experiments import canonical_hash, validate_experiment_config  # noqa: E402
from uncertainty_permission_simulation.schemas import MANIFEST  # noqa: E402


def _json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _self_hash(value: dict[str, object], field: str) -> bool:
    observed = value[field]
    candidate = dict(value)
    candidate.pop(field)
    return observed == canonical_hash(candidate)


def main(*, allow_confirmatory_output: bool = False) -> int:
    diagnostics: list[str] = []
    config_path = ROOT / "experiments/configs/pilot_v1.yaml"
    validation = validate_experiment_config(config_path)
    receipt = _json(ROOT / "data/pilot/pilot_v1_receipt.json")
    if receipt["artifact_kind"] != "development_pilot_receipt":
        diagnostics.append("pilot receipt kind mismatch")
    if receipt["validation"] != validation:
        diagnostics.append("pilot receipt no longer matches validated config/scenario hashes")
    if not _self_hash(receipt, "receipt_hash"):
        diagnostics.append("pilot receipt hash mismatch")
    if len(receipt["families"]) != 15 or len(receipt["cell_summaries"]) != 75:
        diagnostics.append("pilot must store 15 family and 75 family-policy summaries")
    if len(receipt["paired_estimates"]) != 15:
        diagnostics.append("pilot paired-estimate inventory mismatch")
    if len(receipt["process_contrasts"]) != 30:
        diagnostics.append("pilot process-contrast inventory mismatch")
    runtime = receipt["runtime"]
    if not runtime["within_ceiling"] or runtime["predicted_confirmatory_seconds"] > 86400:
        diagnostics.append("predicted confirmatory runtime exceeds the frozen 24-hour ceiling")
    precision = receipt["precision"]
    if not precision["projected_rate_target_met_at_minimum_replications"]:
        diagnostics.append("projected rate MCSE target not met at minimum replications")
    if not precision["projected_paired_target_met_at_minimum_replications"]:
        diagnostics.append("projected paired MCSE target not met at minimum replications")
    audit = receipt["audit"]
    for key in (
        "queue_dynamics_change_timeout_activation",
        "timeout_semantics_change_progression",
        "paired_case_membership_preserved",
    ):
        if not audit[key]:
            diagnostics.append(f"pilot dynamic audit failed: {key}")
    if not audit["stage_aware_censoring_reason_counts"]:
        diagnostics.append("pilot omitted stage-aware censoring reasons")
    swap = receipt["adapter_swap_rehearsal"]
    if swap["status"] != "pass" or swap["engine_change_required"]:
        diagnostics.append("adapter-swap rehearsal failed")

    dummy = _json(ROOT / "data/pilot/dummy_analysis_receipt_v1.json")
    if not _self_hash(dummy, "receipt_hash"):
        diagnostics.append("dummy-analysis receipt hash mismatch")
    if dummy != receipt["dummy_analysis_receipt"]:
        diagnostics.append("stored dummy-analysis receipt differs from pilot receipt")
    for name in (
        "figure_capacity_timeout_prototype_v1.svg",
        "figure_information_tradeoff_prototype_v1.svg",
    ):
        text = (ROOT / "data/pilot" / name).read_text(encoding="utf-8")
        if "Prototype" not in text or "confirmatory" not in text:
            diagnostics.append(f"figure prototype lacks development-only boundary: {name}")

    figure3 = (ROOT / "data/pilot/figure3_reporting_rehearsal.svg").read_text(
        encoding="utf-8"
    )
    if (
        "Development-only reporting rehearsal" not in figure3
        or "Decision state at cutoff" not in figure3
        or "Where U3 unresolved cases accumulate" not in figure3
    ):
        diagnostics.append("Figure 3 reporting rehearsal lacks the repaired three-panel contract")
    table3 = _json(ROOT / "data/pilot/table3_reporting_rehearsal.json")
    if not _self_hash(table3, "table_hash"):
        diagnostics.append("Table 3 reporting rehearsal hash mismatch")
    expected_quantities = {
        "U2C_TIMEOUT_ACTIVATION",
        "U3_MINUS_U0_UNRESOLVED_NONPROGRESSION",
        "U2C_CONDITIONAL_TIMELY_REVIEW",
        "U3_MINUS_U0_INTERACTION_EVENTS",
        "U3_MINUS_U0_WORKLOAD_EVENTS",
    }
    observed_quantities = {
        str(row["quantity_id"]) for row in table3.get("rows", [])
    }
    if (
        table3.get("status") != "development_only_rehearsal"
        or observed_quantities != expected_quantities
        or table3.get("row_count") != len(expected_quantities)
    ):
        diagnostics.append("Table 3 reporting rehearsal does not match the repaired quantity contract")

    trace_path = ROOT / "data/golden_traces/robodebt_worked_trace_v1.json"
    trace = _json(trace_path)
    if not _self_hash(trace, "artifact_hash"):
        diagnostics.append("worked-trace artifact hash mismatch")
    spec_path = ROOT / "data/scenarios/worked_trace_spec_v1.yaml"
    if trace["specification_hash"] != sha256(spec_path.read_bytes()).hexdigest():
        diagnostics.append("worked trace no longer matches its prespecified input")
    if trace["randomness"] != {"mode": "deterministic", "keyed_draws": []}:
        diagnostics.append("worked trace must remain deterministic")
    for arm in ("baseline", "repair"):
        compiled = trace["compilation"][arm]
        if compiled["unresolved_parameter_slot_ids"]:
            diagnostics.append(f"worked-trace {arm} arm has unresolved parameter slots")
        if len(trace["assessments"][arm]) != 6:
            diagnostics.append(f"worked-trace {arm} arm lacks six separate F0-F5 rows")
        for assessment in trace["assessments"][arm]:
            if assessment["status"] not in {"pass", "fail", "unassessable", "not_applicable"}:
                diagnostics.append(f"worked-trace {arm} has invalid status {assessment['status']}")
            if assessment["completeness"] not in {"complete", "incomplete", "invalid"}:
                diagnostics.append(
                    f"worked-trace {arm} has invalid completeness {assessment['completeness']}"
                )
            unknown_diagnostics = set(assessment["diagnostics"]) - set(
                MANIFEST["closed_diagnostic_codes"]
            )
            if unknown_diagnostics:
                diagnostics.append(
                    f"worked-trace {arm} has non-registry diagnostics {sorted(unknown_diagnostics)}"
                )
    baseline_types = {item["event_type"] for item in trace["arms"]["baseline"]["events"]}
    repair_types = {item["event_type"] for item in trace["arms"]["repair"]["events"]}
    if not {"REPRESENTATION_APPLIED", "PROGRESSION_EXECUTED", "EXTERNAL_CONSEQUENCE_STARTED", "CORRECTION_EXECUTED", "RESTORATION_EVALUATED"} <= baseline_types:
        diagnostics.append("worked-trace baseline path is incomplete")
    if not {"PROGRESSION_HELD", "EVIDENCE_REQUESTED", "EXTERNAL_EVIDENCE_RETURNED", "SUPPORTED_DISPOSITION_RECORDED"} <= repair_types:
        diagnostics.append("worked-trace repair path is incomplete")

    packet = (ROOT / "docs/ROBODEBT_WORKED_TRACE_REVIEW_PACKET.md").read_text(encoding="utf-8")
    reference = (ROOT / "docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md").read_text(encoding="utf-8")
    if "ROBUST_PERMISSION_VIOLATION" in packet or "reference profile" not in reference.lower():
        diagnostics.append("worked-trace review-input/reference separation failed")
    for path in (
        ROOT / "docs/CASE_APPLICATION_SUFFICIENCY.md",
        ROOT / "docs/PROTOCOL_REVISION_LOG.md",
        ROOT / "docs/PROCEDURE_COMPREHENSIBILITY_REVIEW.md",
        ROOT / "docs/PILOT_AUDIT.md",
    ):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            diagnostics.append(f"required Slice 3 artifact missing or empty: {path.relative_to(ROOT)}")

    confirmatory_artifacts = [
        path
        for base in (
            ROOT / "outputs/confirmatory_v3",
            ROOT / "outputs/sensitivity_information_latency_v3",
        )
        if base.exists()
        for path in base.rglob("*")
        if path.is_file()
    ]
    if confirmatory_artifacts and not allow_confirmatory_output:
        diagnostics.append("confirmatory output exists before freeze")
    if diagnostics:
        for item in diagnostics:
            print(f"FAIL: {item}")
        return 1
    print(
        "Slice 3 engineering gate passed: "
        f"{validation['family_count']} development families, "
        f"{len(receipt['cell_summaries'])} family-policy cells, "
        f"pilot receipt {receipt['receipt_hash']}; Figure 3 and Table 3 reporting rehearsal verified"
    )
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-confirmatory-output", action="store_true")
    arguments = parser.parse_args()
    raise SystemExit(main(allow_confirmatory_output=arguments.allow_confirmatory_output))
