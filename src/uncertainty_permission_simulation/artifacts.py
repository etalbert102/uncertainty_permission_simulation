"""Materialize deterministic Slice 1 outputs as a closed stored-record graph."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .events import DEFAULT_PRIORITIES
from .formal_model import p0_profile
from .metrics import trace_metrics
from .process_model import TraceResult, TraceSpec
from .schemas import MANIFEST, PAYLOAD_MODELS, RecordMeta, RecordRef, RecordStore, StoredRecord


EXPECTED_DISPOSITIONS = {
    "P0-E-PRESERVE": ("enhanced_scrutiny", "hold"),
    "P0-E-FALLBACK": ("timeout_progression", "progress"),
    "P0-NO-CHANGE-PRESERVE": ("enhanced_scrutiny", "hold"),
    "P0-NO-CHANGE-FALLBACK": ("enhanced_scrutiny", "hold"),
    "GOLDEN-IMPUTE-NONRESPONSE": ("timeout_progression", "progress"),
    "GOLDEN-U2C-QUEUE-HOLD": ("review_timeout", "hold"),
    "GOLDEN-U2O-TIMEOUT": ("timeout_progression", "progress"),
    "GOLDEN-SUPPORTED-PROGRESSION": ("supported_progression", "progress"),
    "GOLDEN-PARTIAL-RESTORATION": ("timeout_progression", "progress"),
}


def ref(object_id: str) -> RecordRef:
    return RecordRef(object_id=object_id, object_version=1)


class BundleBuilder:
    def __init__(self) -> None:
        self.store = RecordStore()

    def add(
        self,
        kind: str,
        object_id: str,
        values: dict[str, Any],
        *,
        provenance: str = "hypothetical",
        basis: str = "synthetic_no_external_source",
        sources: tuple[RecordRef, ...] = (),
        schema_id: str | None = None,
    ) -> RecordRef:
        spec = MANIFEST["payload_kinds"][kind]
        schema = spec.get("schema") or spec["schema_variants"][0]
        payload = PAYLOAD_MODELS[kind](**values)
        meta = RecordMeta(
            object_id=object_id,
            object_version=1,
            schema_id=schema_id or schema["schema_id"],
            schema_version=schema["schema_version"],
            owner_id=f"SLICE1-{kind.upper()}-OWNER",
            provenance_status=provenance,
            source_basis=basis,
            source_refs=sources,
        )
        self.store.add(StoredRecord.create(meta=meta, payload=payload))
        return ref(object_id)


def build_bundle(specs: tuple[TraceSpec, ...], results: dict[str, TraceResult]) -> dict[str, Any]:
    b = BundleBuilder()
    case = b.add("FixtureCase", "SLICE1-CASE", {
        "case_id": "SLICE1-CASE", "case_kind": "synthetic_vertical_slice", "latent_object_type": "oracle_only",
        "sensor_resolution_px": (12, 18), "atmospheric_distortion": True, "road_track": True,
        "low_resolution_track": True, "historical_or_operational_source": "none",
    })
    model_output = b.add("ModelOutput", "SLICE1-MODEL-OUTPUT", {
        "model_output_id": "SLICE1-MODEL-OUTPUT", "primary_estimate_id": "pickup_like_silhouette",
        "primary_confidence_decimal": "0.42", "broad_class_id": "vehicle", "fallback_threshold_decimal": "0.6",
        "alternative_ids": ("armed_technical", "civilian_pickup", "modified_truck"),
        "alternative_probabilities": "not_provided", "source_type": "synthetic_model_output",
    })
    clock = b.add("ClockConfig", "SLICE1-CLOCK", {"clock_config_id": "SLICE1-CLOCK", "decision_time": "21", "observation_window": "0..21", "review_deadline": "21"})
    temporal = b.add("TemporalScope", "SLICE1-TIME", {
        "temporal_scope_id": "SLICE1-TIME", "mode": "simulation_only", "start_value": None,
        "start_precision": "not_applicable", "end_value": None, "end_precision": "not_applicable",
        "reference_as_of": None, "simultaneous_activation_claimed": False, "limitation": None,
    })
    rule = b.add("ExecutableRule", "SLICE1-RULE", {
        "rule_id": "SLICE1-RULE", "rule_kind": "routing", "implementation_id": "p0_visible_material_route",
        "implementation_version": 1, "parameters": (), "input_role_specs": (),
        "output_schema_ref": {"schema_id": "formal_model.disposition", "schema_version": 1},
    })
    hold = b.add("Action", "SLICE1-ACTION-HOLD", {
        "action_instance_id": "SLICE1-ACTION-HOLD", "action_type_id": "hold", "actor_role_id": "SYSTEM",
        "target_id": "SLICE1-CASE", "parameter_vector": {}, "resource_commitment": {},
        "operational_or_external_consequence": {}, "reversibility_window": {}, "authorization_requirement": {},
        "source_rule_refs": (rule,), "authority_direction": "constraint",
    })
    progress = b.add("Action", "SLICE1-ACTION-PROGRESS", {
        "action_instance_id": "SLICE1-ACTION-PROGRESS", "action_type_id": "progress", "actor_role_id": "SYSTEM",
        "target_id": "SLICE1-CASE", "parameter_vector": {}, "resource_commitment": {},
        "operational_or_external_consequence": {}, "reversibility_window": {}, "authorization_requirement": {},
        "source_rule_refs": (rule,), "authority_direction": "progression",
    })
    process = b.add("ProcessProfile", "SLICE1-PROCESS", {
        "process_profile_id": "SLICE1-PROCESS", "profile_kind": "canonical_synthetic", "temporal_scope_ref": temporal,
        "role_refs": (), "stage_refs": (), "queue_refs": (), "resource_refs": (), "deadline_refs": (), "gate_refs": (),
        "transition_rule_refs": (rule,), "action_type_ids": ("hold", "progress"),
        "parameter_slot_ids": ("notice_delay", "response_deadline", "review_capacity", "review_service_time"),
    })
    policy_map = b.add("PolicyMap", "SLICE1-POLICY-MAP", {
        "policy_map_id": "SLICE1-POLICY-MAP", "material_alternative_ids": ("armed_technical",),
        "materiality_reason_id": "material_alternative", "required_information_action_refs": (),
        "required_review_action_refs": (hold,), "blocked_until_review_action_refs": (progress,),
        "authorized_action_refs": (hold, progress), "confidence_alone_is_material": False,
    }, basis="versioned_sources", sources=(model_output,))
    policy_refs: dict[str, RecordRef] = {}
    for policy_id in ("U1", "U2C", "U2O"):
        policy_refs[policy_id] = b.add("PolicyProfile", f"SLICE1-POLICY-{policy_id}", {
            "policy_profile_id": f"SLICE1-POLICY-{policy_id}", "policy_kind": "counterfactual",
            "operational_policy_map_ref": policy_map, "transformation_rule_refs": (rule,), "routing_rule_refs": (rule,),
            "permission_rule_refs": (rule,), "gate_policy_rule_refs": (rule,) if policy_id != "U1" else (),
            "timeout_rule_refs": (rule,), "information_action_rule_refs": (), "correction_rule_refs": (),
            "restoration_rule_refs": (), "parameter_slot_ids": ("notice_delay", "response_deadline", "review_capacity", "review_service_time"),
            "source_fixture_refs": (),
        }, basis="versioned_sources", sources=(policy_map, rule))
    comparison = b.add("ActionComparisonSchema", "SLICE1-ACTION-COMPARISON", {"action_comparison_schema_id": "SLICE1-ACTION-COMPARISON", "material_field_names": ("action_type_id", "authority_direction")}, basis="versioned_sources", sources=(model_output,))
    applicability = b.add("ApplicabilitySpecification", "SLICE1-APPLICABILITY", {"applicability_specification_id": "SLICE1-APPLICABILITY", "scope_declaration_refs": ()}, basis="versioned_sources", sources=(model_output,))
    baseline = b.add("Baseline", "SLICE1-BASELINE", {
        "baseline_id": "SLICE1-BASELINE", "trigger_rule_ref": rule, "required_action_refs_when_triggered": (hold,),
        "blocked_action_refs_until_review": (progress,), "final_action_refs": (progress,),
    }, basis="versioned_sources", sources=(rule, hold, progress))
    evaluation = b.add("EvaluationSpecification", "SLICE1-EVALUATION", {
        "evaluation_spec_id": "SLICE1-EVALUATION", "evaluation_basis": "synthetic_vertical_slice",
        "material_alternative_ids": ("armed_technical",), "materiality_reason_id": "material_alternative",
        "baseline_selection_ref": baseline, "action_comparison_schema_ref": comparison,
        "action_set_representation_mode": "finite", "applicability_spec_ref": applicability,
        "scope_declaration_refs": (), "semantic_correspondence_mode": "exact_semantic_id",
        "required_meaning_refs": (), "semantic_correspondence_rule_ref": rule,
        "required_intervention_capabilities": ("hold",), "required_intervention_action_ref": hold,
        "surfacing_deadline_rule_ref": rule, "f5_undetermined_field_ids": ("contestability_horizon",),
    }, basis="versioned_sources", sources=(baseline, comparison, applicability, rule, hold))
    registry = b.add("EventPriorityRegistry", "SLICE1-PRIORITIES", {
        "event_priority_registry_id": "SLICE1-PRIORITIES", "event_type_priorities": DEFAULT_PRIORITIES,
        "collision_policy": "reject_duplicate_causal_key", "simultaneous_boundary_policy": "priority_then_microstep_then_transition_then_key",
    }, basis="versioned_sources", sources=(rule,))

    parameter_refs: list[RecordRef] = []
    receipt_refs: list[RecordRef] = []
    for index, (slot, value) in enumerate((("notice_delay", "1"), ("response_deadline", "21"), ("review_capacity", "1"), ("review_service_time", "30"))):
        parameter = b.add("ScenarioParameter", f"SLICE1-PARAM-{index}", {
            "scenario_parameter_id": f"SLICE1-PARAM-{index}", "parameter_name": slot, "target_slot_id": slot,
            "value": {"kind": "decimal", "value": value}, "unit_id": None, "provenance_level": "stylized",
            "value_owner": "stylized_overlay", "source_value_ref": None, "validity_rule_refs": (),
        })
        parameter_refs.append(parameter)
        receipt_refs.append(b.add("ParameterBindingReceipt", f"SLICE1-RECEIPT-{index}", {
            "parameter_binding_receipt_id": f"SLICE1-RECEIPT-{index}", "target_slot_id": slot,
            "target_owner_ref": process, "resolved_parameter_ref": parameter,
            "resolution_source": "stylized_overlay", "conflict_status": "no_conflict",
        }, basis="versioned_sources", sources=(process, parameter)))
    overlay = b.add("ScenarioOverlay", "SLICE1-OVERLAY", {
        "scenario_overlay_id": "SLICE1-OVERLAY", "process_profile_ref": process,
        "policy_profile_refs": tuple(policy_refs.values()), "parameter_refs": tuple(parameter_refs),
        "overwrite_policy": "fill_declared_unbound_slots_only",
    }, basis="versioned_sources", sources=(process, *policy_refs.values(), *parameter_refs))
    compiled_refs: dict[str, RecordRef] = {}
    for policy_id, policy_ref in policy_refs.items():
        compiled_refs[policy_id] = b.add("CompiledConfiguration", f"SLICE1-COMPILED-{policy_id}", {
            "compiled_configuration_id": f"SLICE1-COMPILED-{policy_id}", "process_profile_ref": process,
            "policy_profile_ref": policy_ref, "evaluation_spec_ref": evaluation, "application_mapping_ref": None,
            "scenario_overlay_ref": overlay, "parameter_binding_receipt_refs": tuple(receipt_refs),
            "compiler_contract_version": 1, "compiler_code_hash": "0" * 64,
            "unresolved_parameter_slot_ids": (), "semantic_projection_rule_ref": rule,
        }, basis="versioned_sources", sources=(process, policy_ref, evaluation, overlay, *receipt_refs, rule))

    comparisons: list[dict[str, Any]] = []
    trace_refs: dict[str, RecordRef] = {}
    for spec in specs:
        result = results[spec.trace_id]
        representation = b.add("Representation", f"{spec.trace_id}-REPRESENTATION", {
            "representation_id": f"{spec.trace_id}-REPRESENTATION", "field_refs": (),
            "provenance_visible": spec.representation == "preserve",
        }, provenance="derived", basis="versioned_sources", sources=(model_output,), schema_id="P0-SCHEMA-PRESERVE" if spec.representation == "preserve" else "P0-SCHEMA-FALLBACK")
        process_state = b.add("ProcessState", f"{spec.trace_id}-PROCESS", {
            "process_state_id": f"{spec.trace_id}-PROCESS", "case_ref": case, "stage": "deterministic_trace",
            "current_route": result.route, "prior_escalation": False, "active_review_gate": result.gate_state == "closed",
            "emergency_authorization": False,
        })
        trace_spec = b.add("TraceSpecification", f"{spec.trace_id}-SPEC", {
            "trace_specification_id": f"{spec.trace_id}-SPEC", "case_ref": case, "model_output_ref": model_output,
            "transformation_ref": rule, "routing_rule_ref": rule, "held_input_bindings": (), "random_draw_count": 0,
        }, basis="versioned_sources", sources=(case, model_output, rule))
        event_refs: list[RecordRef] = []
        state_refs: list[tuple[RecordRef, RecordRef]] = []
        routed = False
        for index, event in enumerate(result.events):
            selected = (progress,) if event.event_type_id == "PROGRESSION_EXECUTED" else ((hold,) if event.event_type_id == "ACTION_COMPUTED" and result.final_action == "hold" else ())
            pre_route = result.route if routed else "unassigned"
            if event.event_type_id == "ROUTING_COMPLETED":
                routed = True
            post_route = result.route if routed else "unassigned"
            pre_process = b.add("ProcessState", f"{event.event_id}-PROCESS-PRE", {
                "process_state_id": f"{event.event_id}-PROCESS-PRE", "case_ref": case,
                "stage": f"before:{event.event_type_id}", "current_route": pre_route,
                "prior_escalation": False, "active_review_gate": result.gate_state == "closed",
                "emergency_authorization": False,
            })
            post_process = b.add("ProcessState", f"{event.event_id}-PROCESS-POST", {
                "process_state_id": f"{event.event_id}-PROCESS-POST", "case_ref": case,
                "stage": f"after:{event.event_type_id}", "current_route": post_route,
                "prior_escalation": event.event_type_id in {"REVIEW_QUEUED", "REVIEW_STARTED", "REVIEW_COMPLETED"},
                "active_review_gate": result.gate_state == "closed", "emergency_authorization": False,
            })
            shared_state_values = {
                "case_ref": case, "evidence_refs": (model_output,), "representation_ref": representation,
                "clock_ref": clock, "policy_ref": policy_refs[spec.policy_id],
                "transformation_ref": rule, "decision_rule_ref": rule, "evaluation_spec_ref": evaluation,
                "enabled_action_refs": (hold, progress),
            }
            pre = b.add("PreState", f"{event.event_id}-PRE", {"state_snapshot_id": f"{event.event_id}-PRE", **shared_state_values, "process_state_ref": pre_process, "selected_action_refs": ()}, provenance="simulated", basis="versioned_sources", sources=(case, model_output, representation, pre_process, clock, policy_refs[spec.policy_id], rule, evaluation))
            post = b.add("PostState", f"{event.event_id}-POST", {"state_snapshot_id": f"{event.event_id}-POST", **shared_state_values, "process_state_ref": post_process, "selected_action_refs": selected}, provenance="simulated", basis="versioned_sources", sources=(case, model_output, representation, post_process, clock, policy_refs[spec.policy_id], rule, evaluation))
            state_refs.append((pre, post))
            event_ref = b.add("Event", event.event_id, {
                "event_id": event.event_id, "trace_id": spec.trace_id, "trace_kind": "case_trace",
                "trace_specification_ref": trace_spec, "event_type_id": event.event_type_id, "case_ref": case,
                "timestamp": str(event.timestamp), "priority": DEFAULT_PRIORITIES[event.event_type_id],
                "priority_registry_ref": registry, "microstep_rank": event.microstep_rank,
                "transition_rank": event.transition_rank, "causal_event_key": event.causal_event_key,
                "root_event_key": event.root_event_key, "descendant_path": event.descendant_path,
                "actor_ref": "SYSTEM", "action_refs": selected, "representation_ref": representation,
                "process_state_ref": post_process, "rule_executions": (), "evidence_refs": (model_output,),
                "policy_ref": policy_refs[spec.policy_id], "intervention_pair_ref": None, "intervention_arm": "none",
                "keyed_draw_refs": (), "pre_state_ref": pre, "post_state_ref": post,
            }, provenance="simulated", basis="versioned_sources", sources=(trace_spec, pre, post, registry, policy_refs[spec.policy_id]))
            event_refs.append(event_ref)
        selected_action = progress if result.final_action == "progress" else hold
        disposition = b.add("Disposition", f"{spec.trace_id}-DISPOSITION", {
            "disposition_id": f"{spec.trace_id}-DISPOSITION", "route": result.route,
            "routing_reasons": (result.gate_state,), "automatic_action_refs": (progress,) if result.functional_permission else (),
            "post_review_action_refs": (), "selected_action_refs": (selected_action,),
            "constraint_action_refs": (hold,) if result.final_action == "hold" else (), "information_action_refs": (),
            "restoration_action_refs": (), "gate_requirements": (), "review_evidence_complete": False,
        }, provenance="simulated", basis="versioned_sources", sources=(trace_spec, selected_action))
        trace_ref = b.add("Trace", spec.trace_id, {
            "trace_id": spec.trace_id, "trace_specification_ref": trace_spec, "event_refs": tuple(event_refs),
            "initial_state_ref": state_refs[0][0], "final_state_ref": state_refs[-1][1],
            "final_disposition_ref": disposition, "random_draw_count": 0, "held_bundle_hash": result.held_bundle_hash,
            "gate_state_refs": (), "review_state_refs": (),
        }, provenance="simulated", basis="versioned_sources", sources=(trace_spec, *event_refs, state_refs[0][0], state_refs[-1][1], disposition))
        trace_refs[spec.trace_id] = trace_ref
        expected_route, expected_action = EXPECTED_DISPOSITIONS[spec.trace_id]
        expected = b.add("ExpectedResult", f"{spec.trace_id}-EXPECTED", {
            "expected_result_id": f"{spec.trace_id}-EXPECTED", "trace_specification_ref": trace_spec,
            "expected_disposition": {"route": expected_route, "selected_action": expected_action},
            "expected_assessment_specs": (),
        }, basis="versioned_sources", sources=(trace_spec,))
        comparisons.append({
            "trace_id": spec.trace_id,
            "expected_result_ref": expected.model_dump(),
            "actual_trace_ref": trace_ref.model_dump(),
            "match": (result.route, result.final_action) == (expected_route, expected_action),
        })
        metrics = trace_metrics(result)
        b.add("Metric", f"{spec.trace_id}-METRIC-PROGRESSION", {
            "metric_id": f"{spec.trace_id}-METRIC-PROGRESSION", "numerator": str(metrics["progression_count"]),
            "denominator": "1", "unit_id": "case", "scope_refs": (trace_ref,),
            "estimate": str(metrics["progression_count"]),
        }, provenance="simulated", basis="versioned_sources", sources=(trace_ref,))

    for trace_id, arm in (("P0-E-PRESERVE", "preserve"), ("P0-E-FALLBACK", "fallback")):
        trace_ref = trace_refs[trace_id]
        for property_id, assessment in p0_profile(results[trace_id], arm=arm).items():
            diagnostic_refs: list[RecordRef] = []
            for index, code in enumerate(assessment.diagnostic_codes):
                diagnostic_refs.append(b.add("Diagnostic", f"{trace_id}-{property_id}-D{index}", {
                    "diagnostic_id": f"{trace_id}-{property_id}-D{index}", "code": code,
                    "category": "fixture_integrity", "owning_layer": "formal_evaluator", "severity": "blocking",
                    "property_or_helper_id": property_id, "message_template_id": code, "case_ref": case,
                    "trace_ref": trace_ref, "action_refs": (), "context_refs": (trace_ref,),
                    "expected_value": None, "observed_value": None,
                    "artifact_path": "data/golden_traces/slice1_records_v1.json", "suggested_next_action": "follow fixture intervention",
                }, provenance="simulated", basis="versioned_sources", sources=(trace_ref, case)))
            b.add("Assessment", f"{trace_id}-{property_id}-ASSESSMENT", {
                "assessment_id": f"{trace_id}-{property_id}-ASSESSMENT", "property_or_helper_id": property_id,
                "evaluation_unit_ref": trace_ref, "status": assessment.status, "completeness": assessment.completeness,
                "value": assessment.value, "scope_declaration_ref": None, "applicability_rule_ref": None,
                "diagnostic_refs": tuple(diagnostic_refs), "component_bindings": (), "aggregation_rule_ref": None,
                "false_antecedent_ref": None, "missing_or_invalid_fields": (), "evaluation_input_bindings": (),
            }, provenance="simulated", basis="versioned_sources", sources=(trace_ref, *diagnostic_refs))

    b.store.validate_closure()
    records = [record.model_dump(mode="json") for record in b.store.records()]
    return {
        "bundle_schema_version": 1,
        "record_count": len(records),
        "records": records,
        "comparisons": comparisons,
        "closure_status": "valid",
        "compiled_configuration_refs": {key: value.model_dump() for key, value in compiled_refs.items()},
    }
