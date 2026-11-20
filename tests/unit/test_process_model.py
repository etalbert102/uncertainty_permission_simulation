from pathlib import Path

import pytest

from uncertainty_permission_simulation.applications.robodebt import load_early_adapter
from uncertainty_permission_simulation.artifacts import BundleBuilder, build_bundle, ref
from uncertainty_permission_simulation.cli import _slice1_validation_observations, _specs
from uncertainty_permission_simulation.configuration import (
    CompilationError,
    ParameterValue,
    SUPPORTED_EVIDENCE_STATE_ID,
    ScenarioOverlaySpec,
    UNRESOLVED_EVIDENCE_STATE_ID,
    compile_configuration,
    evaluate_robust_action_support,
    load_evaluation_specification,
    period_evidence_evaluation_specification,
    progression_action_instance,
)
from uncertainty_permission_simulation.process_model import TraceSpec, execute_topology, run_trace
from uncertainty_permission_simulation.profiles import canonical_process, nonisomorphic_process, policy, smoke_overlay
from uncertainty_permission_simulation.schemas import ContractError


ROOT = Path(__file__).resolve().parents[2]


def test_period_evidence_specification_executes_exact_refinement_certificate() -> None:
    specification = period_evidence_evaluation_specification("TEST-EVALUATION@1")
    supported = evaluate_robust_action_support(
        specification,
        action=progression_action_instance(specification, case_id="CASE-1"),
        evidence_state_id=SUPPORTED_EVIDENCE_STATE_ID,
    )
    unresolved = evaluate_robust_action_support(
        specification,
        action=progression_action_instance(specification, case_id="CASE-1"),
        evidence_state_id=UNRESOLVED_EVIDENCE_STATE_ID,
    )
    assert supported.robust_action_support is True
    assert unresolved.robust_action_support is False
    assert supported.refinement_certificate_id == "CERT-PERIOD-EVIDENCE-PRESENT@1"
    assert unresolved.refinement_certificate_id == "CERT-PERIOD-EVIDENCE-UNRESOLVED@1"
    assert supported.action_instance_id == "CASE-1:PROGRESS"


def test_support_evaluation_rejects_action_identity_drift() -> None:
    specification = period_evidence_evaluation_specification("TEST-EVALUATION@1")
    action = progression_action_instance(specification, case_id="CASE-1")
    drifted = action.model_copy(update={"authority_direction": "narrows_progression"})
    with pytest.raises(CompilationError, match="EVALUATION_ACTION_INSTANCE_INVALID"):
        evaluate_robust_action_support(
            specification,
            action=drifted,
            evidence_state_id=SUPPORTED_EVIDENCE_STATE_ID,
        )


def test_frozen_evaluation_specification_is_loaded_as_external_artifact() -> None:
    specification = load_evaluation_specification(
        ROOT / "experiments/evaluation_specs/period_evidence_v2.json"
    )
    compiled = compile_configuration(
        configuration_id="EXTERNAL-SPEC",
        process=canonical_process(),
        policy=policy("U2C"),
        overlay=smoke_overlay(),
        evaluation_spec_id=specification.evaluation_spec_id,
        evaluation_specification=specification,
    )
    assert compiled.evaluation_specification_origin == "external"


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


def test_stored_bundle_is_reference_closed_and_matches_prespecified_results() -> None:
    specs = _specs()
    results = {spec.trace_id: run_trace(spec) for spec in specs}
    reference_u2c = compile_configuration(
        configuration_id="SYNTH-U2C", process=canonical_process(), policy=policy("U2C"),
        overlay=smoke_overlay(), evaluation_spec_id="P0-SIGMA-1",
    )
    observations = _slice1_validation_observations(reference_u2c)
    bundle = build_bundle(specs, results, validation_observations=observations)
    assert bundle["closure_status"] == "valid"
    assert bundle["record_count"] == 726
    assert all(comparison["match"] for comparison in bundle["comparisons"])
    assert bundle["validation_receipt_status"] == {
        "isomorphic_vocabulary": "match",
        "nonisomorphic_topology": "match",
        "application_adapter": "match",
    }
    assert all(record["payload"] for record in bundle["records"])
    records = {(record["meta"]["object_id"], record["meta"]["object_version"]): record for record in bundle["records"]}
    representations = [record for record in bundle["records"] if record["payload"].get("payload_kind") == "representation"]
    target_kinds = {
        records[(ref_value["object_id"], ref_value["object_version"])]["payload"]["field_kind"]
        for record in representations
        for ref_value in record["payload"]["field_refs"]
    }
    assert len(representations) == 9
    assert sum(len(record["payload"]["field_refs"]) for record in representations) == 9
    assert target_kinds == {"claim", "untyped"}
    assert len(bundle["rule_implementation_receipts"]) == 3
    assert bundle["reference_target_receipt"]["declared_reference_fields"] >= 236
    assert bundle["reference_target_receipt"]["typed_target_refs_validated"] > 0


def test_stored_validation_receipt_exposes_observation_mutation() -> None:
    specs = _specs()
    results = {spec.trace_id: run_trace(spec) for spec in specs}
    reference_u2c = compile_configuration(
        configuration_id="SYNTH-U2C", process=canonical_process(), policy=policy("U2C"),
        overlay=smoke_overlay(), evaluation_spec_id="P0-SIGMA-1",
    )
    observations = _slice1_validation_observations(reference_u2c)
    observations["isomorphic_vocabulary"]["event_order_equal"] = False
    bundle = build_bundle(specs, results, validation_observations=observations)
    assert bundle["validation_receipt_status"]["isomorphic_vocabulary"] == "mismatch"
    receipt_ref = bundle["validation_receipt_refs"]["isomorphic_vocabulary"]
    receipt = next(
        record for record in bundle["records"]
        if record["meta"]["object_id"] == receipt_ref["object_id"]
    )
    assert receipt["payload"]["expected_value"]["event_order_equal"] is True
    assert receipt["payload"]["observed_value"]["event_order_equal"] is False
    assert receipt["payload"]["comparison_status"] == "mismatch"


def test_record_graph_rejects_unresolved_reference_and_cycle() -> None:
    missing = BundleBuilder()
    missing.add("ProcessState", "A", {
        "process_state_id": "A", "case_ref": ref("MISSING"), "stage": "x", "current_route": "x",
        "prior_escalation": False, "active_review_gate": False, "emergency_authorization": False,
    })
    with pytest.raises(ContractError, match="SCHEMA_REFERENCE_UNRESOLVED"):
        missing.store.validate_closure()

    cycle = BundleBuilder()
    cycle.add("Metric", "A", {
        "metric_id": "A", "numerator": "1", "denominator": "1", "unit_id": "case",
        "scope_refs": (ref("B"),), "estimate": "1",
    }, provenance="simulated", basis="versioned_sources", sources=(ref("B"),))
    cycle.add("Metric", "B", {
        "metric_id": "B", "numerator": "1", "denominator": "1", "unit_id": "case",
        "scope_refs": (ref("A"),), "estimate": "1",
    }, provenance="simulated", basis="versioned_sources", sources=(ref("A"),))
    with pytest.raises(ContractError, match="SCHEMA_REFERENCE_CYCLE"):
        cycle.store.validate_closure()


def test_record_graph_enforces_manifest_reference_target_kinds() -> None:
    valid = BundleBuilder()
    source = valid.add("ModelOutput", "SOURCE", {
        "model_output_id": "SOURCE", "primary_estimate_id": "x",
        "primary_confidence_decimal": "0.4", "broad_class_id": "vehicle",
        "fallback_threshold_decimal": "0.6", "alternative_ids": (),
        "alternative_probabilities": "not_provided", "source_type": "synthetic_model_output",
    })
    field = valid.add("UntypedField", "FIELD", {
        "field_id": "FIELD", "field_name": "object_class", "value": "vehicle",
        "visibility": ("router",),
    }, basis="versioned_sources", sources=(source,))
    valid.add("Representation", "REP", {
        "representation_id": "REP", "field_refs": (field,), "provenance_visible": False,
    }, basis="versioned_sources", sources=(field,), schema_id="P0-SCHEMA-FALLBACK")
    valid.store.validate_closure()

    invalid = BundleBuilder()
    wrong_target = invalid.add("ModelOutput", "WRONG", {
        "model_output_id": "WRONG", "primary_estimate_id": "x",
        "primary_confidence_decimal": "0.4", "broad_class_id": "vehicle",
        "fallback_threshold_decimal": "0.6", "alternative_ids": (),
        "alternative_probabilities": "not_provided", "source_type": "synthetic_model_output",
    })
    invalid.add("Representation", "BAD-REP", {
        "representation_id": "BAD-REP", "field_refs": (wrong_target,), "provenance_visible": False,
    }, basis="versioned_sources", sources=(wrong_target,), schema_id="P0-SCHEMA-FALLBACK")
    with pytest.raises(ContractError, match="SCHEMA_REFERENCE_TARGET_INVALID.*not ModelOutput"):
        invalid.store.validate_closure()

    wrong_global_role = BundleBuilder()
    wrong_case = wrong_global_role.add("ModelOutput", "NOT-A-CASE", {
        "model_output_id": "NOT-A-CASE", "primary_estimate_id": "x",
        "primary_confidence_decimal": "0.4", "broad_class_id": "vehicle",
        "fallback_threshold_decimal": "0.6", "alternative_ids": (),
        "alternative_probabilities": "not_provided", "source_type": "synthetic_model_output",
    })
    wrong_global_role.add("ProcessState", "BAD-PROCESS", {
        "process_state_id": "BAD-PROCESS", "case_ref": wrong_case, "stage": "x", "current_route": "x",
        "prior_escalation": False, "active_review_gate": False, "emergency_authorization": False,
    })
    with pytest.raises(ContractError, match="ProcessState.case_ref.*not ModelOutput"):
        wrong_global_role.store.validate_closure()
