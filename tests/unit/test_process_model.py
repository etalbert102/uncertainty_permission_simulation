from pathlib import Path

import pytest

from uncertainty_permission_simulation.applications.robodebt import load_early_adapter
from uncertainty_permission_simulation.configuration import CompilationError, ParameterValue, ScenarioOverlaySpec, compile_configuration
from uncertainty_permission_simulation.process_model import TraceSpec, execute_topology, run_trace
from uncertainty_permission_simulation.profiles import canonical_process, nonisomorphic_process, policy, smoke_overlay


ROOT = Path(__file__).resolve().parents[2]


def test_all_seven_golden_behaviors() -> None:
    preserve = run_trace(TraceSpec("P", "U1", "preserve", True, review_delay=30))
    fallback = run_trace(TraceSpec("F", "U1", "fallback", True))
    assert preserve.final_action == "hold" and fallback.final_action == "progress"
    null_a = run_trace(TraceSpec("N1", "U1", "preserve", False, force_scrutiny=True, review_delay=30))
    null_b = run_trace(TraceSpec("N2", "U1", "fallback", False, force_scrutiny=True, review_delay=30))
    assert null_a.semantic_projection[1:] == null_b.semantic_projection[1:]
    assert run_trace(TraceSpec("I", "U1")).final_action == "progress"
    assert run_trace(TraceSpec("C", "U2C", review_delay=30)).final_action == "hold"
    assert run_trace(TraceSpec("O", "U2O", review_delay=30)).final_action == "progress"
    assert run_trace(TraceSpec("S", "U2C", response=True, action_evidence=True)).functional_permission
    restored = run_trace(TraceSpec("R", "U1", external_exposure=True, correction=True))
    assert restored.restoration_complete is False


def test_compiler_emits_one_receipt_per_slot() -> None:
    compiled = compile_configuration(configuration_id="C", process=canonical_process(), policy=policy("U2C"), overlay=smoke_overlay(), evaluation_spec_id="E")
    assert {receipt.slot_id for receipt in compiled.receipts} == canonical_process().parameter_slot_ids
    assert not compiled.unresolved_parameter_slot_ids


def test_compiler_rejects_documented_override() -> None:
    process = canonical_process().model_copy(update={"documented_parameters": (ParameterValue(slot_id="notice_delay", value="1", provenance="documented", owner_id="SOURCE"),)})
    with pytest.raises(CompilationError, match="PROFILE_PARAMETER_CONFLICT"):
        compile_configuration(configuration_id="C", process=process, policy=policy("U1"), overlay=smoke_overlay(), evaluation_spec_id="E")


def test_nonisomorphic_topology_runs_without_kernel_change() -> None:
    compiled = compile_configuration(configuration_id="N", process=nonisomorphic_process(), policy=policy("U2C"), overlay=smoke_overlay(), evaluation_spec_id="E")
    events = execute_topology(("CASE_ARRIVAL", "ROUTING_COMPLETED", "EVIDENCE_REQUESTED", "CASE_CLOSED"))
    assert compiled.process_profile.stage_ids[1] == "triage"
    assert events[-1] == "CASE_CLOSED"


def test_robodebt_adapter_preserves_unsupported_slots() -> None:
    process, historical = load_early_adapter(ROOT / "data/sources/robodebt/r_oci_early.yaml")
    overlay = ScenarioOverlaySpec(overlay_id="A", parameters=(
        ParameterValue(slot_id="notice_delay", value="1", provenance="stylized", owner_id="A"),
        ParameterValue(slot_id="review_capacity", value="1", provenance="stylized", owner_id="A"),
        ParameterValue(slot_id="review_service_time", value="30", provenance="stylized", owner_id="A"),
    ))
    compiled = compile_configuration(configuration_id="R", process=process, policy=historical, overlay=overlay, evaluation_spec_id="E", application_mapping_id="R-MAP")
    assert compiled.application_mapping_id == "R-MAP"
    assert next(receipt for receipt in compiled.receipts if receipt.slot_id == "response_deadline").provenance == "documented"
