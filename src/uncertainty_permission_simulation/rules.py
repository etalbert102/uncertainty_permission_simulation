"""Closed executable-rule registry for the formal-model kernel.

The registry is deliberately static.  Rule records select one of these callables by
identifier and version; they never import user-supplied code or evaluate prose.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any, Callable


RuleInputs = dict[str, Any]
RuleParameters = dict[str, Any]
RuleCallable = Callable[[RuleInputs, RuleParameters], Any]


def _one(inputs: RuleInputs, role_id: str) -> Any:
    value = inputs[role_id]
    if isinstance(value, (list, tuple)):
        if len(value) != 1:
            raise ValueError(f"role {role_id} requires exactly one input")
        return value[0]
    return value


def _field(inputs: RuleInputs, binding: dict[str, str]) -> Any:
    value = _one(inputs, binding["input_role_id"])
    for token in binding["field_path"].lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, (list, tuple)) else value[token]
    return value


def p0_preserve_projection(inputs: RuleInputs, parameters: RuleParameters) -> dict[str, Any]:
    return {
        "projected_values": [_field(inputs, binding) for binding in parameters["source_field_paths"]],
        "projection_fact_set_by_evidence_id": parameters["projection_fact_set_by_evidence_id"],
        "alternative_semantic_type": parameters["alternative_semantic_type"],
        "polarity": parameters["polarity"],
        "uncertainty_status": parameters["uncertainty_status"],
    }


def p0_threshold_broad_fallback(inputs: RuleInputs, parameters: RuleParameters) -> dict[str, Any]:
    confidence = float(_field(inputs, parameters["confidence_path"]))
    threshold = float(_field(inputs, parameters["threshold_path"]))
    return {"output_path": parameters["output_path"], "fallback_applies": confidence < threshold}


def p0_visible_material_route(inputs: RuleInputs, parameters: RuleParameters) -> dict[str, Any]:
    representation = _one(inputs, "representation")
    visible = bool(representation.get("provenance_visible", False))
    constructor = "enhanced" if visible else "routine"
    return {
        "constructor": constructor,
        "broad_class_id": parameters["broad_class_id"],
        "action_refs": parameters["action_refs_by_case_id"],
    }


def p0_low_resolution_control_route(inputs: RuleInputs, parameters: RuleParameters) -> dict[str, Any]:
    low_resolution = bool(_field(inputs, parameters["case_field_path"]))
    return {
        "constructor": "enhanced" if low_resolution else "routine",
        "action_refs": parameters["action_refs_by_case_id"],
    }


def constant_true(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    return True


def any_action_direction_in_disposition_set(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    disposition = _one(inputs, "disposition")
    action_ids = set(_field(inputs, parameters["set_path"]))
    actions = inputs.get("actions", ())
    return any(
        action.get("action_instance_id") in action_ids
        and action.get("authority_direction") == parameters["required_direction"]
        for action in actions
    )


def declared_status_aggregation(inputs: RuleInputs, parameters: RuleParameters) -> dict[str, Any]:
    statuses = [component.get("status") for component in inputs.get("components", ())]
    mode = parameters["aggregation_mode"]
    if mode == "any_fail_conjunctive":
        status = "fail" if "fail" in statuses else "pass"
    elif mode == "any_pass_disjunctive":
        status = "pass" if "pass" in statuses else "fail"
    else:
        threshold = float(parameters["threshold"])
        status = "pass" if statuses and statuses.count("pass") / len(statuses) >= threshold else "fail"
    return {"status": status, "completeness": "complete"}


def material_item_applies_to_output_action(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    return (
        _field(inputs, parameters["output_path"]) == parameters["required_id"]
        and _one(inputs, "affected_action").get("action_instance_id")
        == parameters["affected_action_ref"]["object_id"]
    )


def boolean_input_is_true(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    return _field(inputs, parameters["input_field"]) is True


def any_boolean_input_is_true(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    return any(_field(inputs, binding) is True for binding in parameters["input_fields"])


def exact_semantic_fields(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    claim = _one(inputs, "surfaced_claim")
    material_item = _one(inputs, "material_item")
    required = _one(inputs, "required_meaning")
    return all(claim.get(field) == material_item.get(field) == required.get(field) for field in parameters["compared_fields"])


def event_strictly_before_boundary(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    events = inputs.get("events", ())
    surfaced = [event for event in events if event.get("event_type_id") == parameters["surfaced_event_type"]]
    boundary = [event for event in events if event.get("event_type_id") == parameters["boundary_event_type"]]
    return bool(surfaced and boundary and min(event["simulation_time"] for event in surfaced) < min(event["simulation_time"] for event in boundary))


def source_anchored_materiality_membership(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    evaluation = _one(inputs, "evaluation_specification")
    declared = {ref["object_id"] for ref in parameters["material_item_refs"]}
    return bool(declared.intersection(evaluation.get("material_item_ids", ())))


def action_support_membership(inputs: RuleInputs, parameters: RuleParameters) -> bool:
    evidence = _one(inputs, "evidence_state")
    satisfied = set(evidence.get("satisfied_support_condition_ids", ()))
    required = {ref["object_id"] for ref in parameters["support_condition_refs"]}
    return required.issubset(satisfied)


def execute_action_intervention(inputs: RuleInputs, parameters: RuleParameters) -> dict[str, Any]:
    return {
        "intervention_unit": parameters["intervention_unit"],
        "focal_action": _one(inputs, "focal_action"),
        "action_executed": True,
        "initial_system_state": _one(inputs, "initial_system_state"),
    }


def hold_action_intervention(inputs: RuleInputs, parameters: RuleParameters) -> dict[str, Any]:
    return {
        "intervention_unit": parameters["intervention_unit"],
        "focal_action": _one(inputs, "focal_action"),
        "action_executed": False,
        "initial_system_state": _one(inputs, "initial_system_state"),
    }


RULE_IMPLEMENTATIONS: dict[str, RuleCallable] = {
    "p0_preserve_projection": p0_preserve_projection,
    "p0_threshold_broad_fallback": p0_threshold_broad_fallback,
    "p0_visible_material_route": p0_visible_material_route,
    "p0_low_resolution_control_route": p0_low_resolution_control_route,
    "constant_true": constant_true,
    "any_action_direction_in_disposition_set": any_action_direction_in_disposition_set,
    "declared_status_aggregation": declared_status_aggregation,
    "material_item_applies_to_output_action": material_item_applies_to_output_action,
    "boolean_input_is_true": boolean_input_is_true,
    "any_boolean_input_is_true": any_boolean_input_is_true,
    "exact_semantic_fields": exact_semantic_fields,
    "event_strictly_before_boundary": event_strictly_before_boundary,
    "source_anchored_materiality_membership": source_anchored_materiality_membership,
    "action_support_membership": action_support_membership,
    "execute_action_intervention": execute_action_intervention,
    "hold_action_intervention": hold_action_intervention,
}


def implementation_code_hash(implementation_id: str) -> str:
    """Hash the complete static code artifact and bind it to one registry ID."""

    if implementation_id not in RULE_IMPLEMENTATIONS:
        raise KeyError(implementation_id)
    artifact = Path(__file__).read_bytes()
    return sha256(artifact + b"\0" + implementation_id.encode("utf-8")).hexdigest()
