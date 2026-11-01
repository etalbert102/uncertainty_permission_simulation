"""Blocking Slice 3 engineering and artifact validator.

Independent cold-reader returns are deliberately outside this validator and remain a
separate external pre-freeze gate.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uncertainty_permission_simulation.experiments import canonical_hash, validate_experiment_config  # noqa: E402


def _json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _self_hash(value: dict[str, object], field: str) -> bool:
    observed = value[field]
    candidate = dict(value)
    candidate.pop(field)
    return observed == canonical_hash(candidate)


def main() -> int:
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
    if len(receipt["paired_estimates"]) != 225:
        diagnostics.append("pilot paired-estimate inventory mismatch")
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
        "queue_dynamics_change_review_effectiveness",
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
    baseline_types = {item["event_type"] for item in trace["arms"]["baseline"]["events"]}
    repair_types = {item["event_type"] for item in trace["arms"]["repair"]["events"]}
    if not {"REPRESENTATION_APPLIED", "PROGRESSION_EXECUTED", "EXTERNAL_CONSEQUENCE_STARTED", "CORRECTION_EXECUTED", "RESTORATION_EVALUATED"} <= baseline_types:
        diagnostics.append("worked-trace baseline path is incomplete")
    if not {"PROGRESSION_HELD", "EVIDENCE_REQUESTED", "EXTERNAL_EVIDENCE_RETURNED", "SUPPORTED_DISPOSITION_RECORDED"} <= repair_types:
        diagnostics.append("worked-trace repair path is incomplete")

    packet = (ROOT / "docs/ROBODEBT_WORKED_TRACE_PACKET.md").read_text(encoding="utf-8")
    oracle = (ROOT / "docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md").read_text(encoding="utf-8")
    if "ROBUST_PERMISSION_VIOLATION" in packet or "withheld expected profile" not in oracle.lower():
        diagnostics.append("worked-trace packet/oracle separation failed")
    bundle_script = (ROOT / "scripts/build_slice3_reader_bundle.py").read_text(encoding="utf-8")
    if "ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md" not in bundle_script or "FORBIDDEN" not in bundle_script:
        diagnostics.append("Slice 3 bundle builder does not explicitly forbid the oracle")
    for path in (
        ROOT / "docs/CASE_APPLICATION_SUFFICIENCY.md",
        ROOT / "docs/PROTOCOL_REVISION_LOG.md",
        ROOT / "docs/SLICE3_COLD_READER_QA_RECEIPT.md",
        ROOT / "docs/SLICE3_READER_HANDOFF.md",
        ROOT / "docs/PILOT_AUDIT.md",
    ):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            diagnostics.append(f"required Slice 3 artifact missing or empty: {path.relative_to(ROOT)}")

    confirmatory_artifacts = list((ROOT / "outputs").glob("confirmatory*/**/*"))
    if confirmatory_artifacts:
        diagnostics.append("confirmatory output exists before freeze")
    if diagnostics:
        for item in diagnostics:
            print(f"FAIL: {item}")
        return 1
    print(
        "Slice 3 engineering gate passed: "
        f"{validation['family_count']} development families, "
        f"{len(receipt['cell_summaries'])} family-policy cells, "
        f"pilot receipt {receipt['receipt_hash']}; independent reader QA remains externally pending"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
