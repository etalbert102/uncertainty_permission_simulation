from __future__ import annotations

import pytest

from uncertainty_permission_simulation.formal_model import render_p0_report
from uncertainty_permission_simulation.process_model import TraceSpec, run_trace
from uncertainty_permission_simulation.schemas import (
    MANIFEST,
    PAYLOAD_MODELS,
    ContractError,
    RecordMeta,
    StoredRecord,
    content_hash,
    validate_executable_rule,
    validate_model_manifest_inventory,
    validate_rule_registry_manifest,
)


def _valid_routing_rule():
    return PAYLOAD_MODELS["ExecutableRule"](
        rule_id="RULE-1",
        rule_kind="routing",
        implementation_id="p0_visible_material_route",
        implementation_version=1,
        parameters=(
            {"parameter_id": "policy_ref", "value_kind": "record_ref", "value": {"object_id": "POLICY", "object_version": 1}},
            {"parameter_id": "broad_class_id", "value_kind": "literal", "value": "vehicle"},
            {"parameter_id": "action_refs_by_case_id", "value_kind": "record_ref_set", "value": {"CASE": ({"object_id": "ACTION", "object_version": 1},)}},
            {"parameter_id": "constructors", "value_kind": "literal", "value": ("enhanced", "routine", "unassessable")},
        ),
        input_role_specs=(
            {"role_id": "representation", "accepted_schema_refs": ({"schema_id": "P0-SCHEMA-PRESERVE", "schema_version": 1}, {"schema_id": "P0-SCHEMA-FALLBACK", "schema_version": 1}), "cardinality": "one"},
            {"role_id": "policy", "accepted_schema_refs": ({"schema_id": "P0-SCHEMA-POLICY", "schema_version": 1},), "cardinality": "one"},
            {"role_id": "process_state", "accepted_schema_refs": ({"schema_id": "P0-SCHEMA-PROCESS", "schema_version": 1},), "cardinality": "one"},
            {"role_id": "clock", "accepted_schema_refs": ({"schema_id": "P0-SCHEMA-CLOCK", "schema_version": 1},), "cardinality": "one"},
        ),
        output_schema_ref={"schema_id": "formal_model.disposition", "schema_version": 1},
    )


def test_manifest_model_inventory_is_bidirectional() -> None:
    validate_model_manifest_inventory()
    validate_rule_registry_manifest()
    assert "CompiledConfiguration" in PAYLOAD_MODELS
    assert "SimulationCase" in PAYLOAD_MODELS


def test_manifest_rejects_unknown_reference_target_kind() -> None:
    targets = MANIFEST["payload_kinds"]["Representation"]["reference_targets"]
    original = targets["field_refs"]
    targets["field_refs"] = ["MissingPayloadKind"]
    try:
        with pytest.raises(ContractError, match="names unknown target kinds"):
            validate_model_manifest_inventory()
    finally:
        targets["field_refs"] = original


def test_manifest_rejects_missing_target_role_and_nested_path() -> None:
    roles = MANIFEST["reference_target_roles"]
    case_targets = roles.pop("case_ref")
    try:
        with pytest.raises(ContractError, match="reference fields lack target declarations"):
            validate_model_manifest_inventory()
    finally:
        roles["case_ref"] = case_targets

    targets = MANIFEST["payload_kinds"]["Representation"]["reference_targets"]
    original = targets.pop("field_refs")
    targets["field_refs/*/does_not_exist"] = original
    try:
        with pytest.raises(ContractError, match="undeclared or not reference-bearing"):
            validate_model_manifest_inventory()
    finally:
        targets.pop("field_refs/*/does_not_exist")
        targets["field_refs"] = original


def test_record_envelope_and_hash_are_replayable() -> None:
    model = PAYLOAD_MODELS["TemporalScope"]
    payload = model(
        temporal_scope_id="TIME-1",
        mode="simulation_only",
        start_value=None,
        start_precision="not_applicable",
        end_value=None,
        end_precision="not_applicable",
        reference_as_of=None,
        simultaneous_activation_claimed=False,
        limitation=None,
    )
    meta = RecordMeta(
        object_id="TIME-1",
        object_version=1,
        schema_id="process_model.temporal_scope",
        schema_version=1,
        owner_id="TEST",
        provenance_status="hypothetical",
        source_basis="synthetic_no_external_source",
    )
    record = StoredRecord.create(meta=meta, payload=payload)
    assert record.content_hash == content_hash(meta, payload)


def test_binary_float_is_rejected_from_canonical_record() -> None:
    model = PAYLOAD_MODELS["CaseAttribute"]
    payload = model(case_attribute_id="A-1", semantic_id="x", value=0.1, visibility="latent")
    meta = RecordMeta(object_id="A-1", object_version=1, schema_id="case.attribute", schema_version=1, owner_id="TEST", provenance_status="simulated", source_basis="versioned_sources", source_refs=({"object_id": "S", "object_version": 1},))
    with pytest.raises(ValueError, match="binary floats"):
        StoredRecord.create(meta=meta, payload=payload)


def test_declared_set_order_does_not_change_hash() -> None:
    model = PAYLOAD_MODELS["ProcessProfile"]
    common = dict(
        process_profile_id="P",
        profile_kind="canonical_synthetic",
        temporal_scope_ref={"object_id": "T", "object_version": 1},
        role_refs=(), stage_refs=(), queue_refs=(), resource_refs=(), deadline_refs=(), gate_refs=(), transition_rule_refs=(),
        action_type_ids=("b", "a"), parameter_slot_ids=("y", "x"),
    )
    first = model(**common)
    second = model(**(common | {"action_type_ids": ("a", "b"), "parameter_slot_ids": ("x", "y")}))
    meta = RecordMeta(object_id="P", object_version=1, schema_id="process_model", schema_version=1, owner_id="TEST", provenance_status="hypothetical", source_basis="synthetic_no_external_source")
    assert content_hash(meta, first) == content_hash(meta, second)


def test_executable_rule_accepts_exact_closed_signature() -> None:
    validate_executable_rule(_valid_routing_rule())


def test_executable_rule_hash_normalizes_nested_signature_sets() -> None:
    first = _valid_routing_rule()
    values = first.model_dump(mode="python")
    values["input_role_specs"] = list(reversed(values["input_role_specs"]))
    representation = next(item for item in values["input_role_specs"] if item["role_id"] == "representation")
    representation["accepted_schema_refs"] = list(reversed(representation["accepted_schema_refs"]))
    second = PAYLOAD_MODELS["ExecutableRule"](**values)
    validate_executable_rule(second)
    meta = RecordMeta(
        object_id="RULE-1",
        object_version=1,
        schema_id="P0-SCHEMA-EXECUTABLE-RULE",
        schema_version=1,
        owner_id="TEST",
        provenance_status="hypothetical",
        source_basis="synthetic_no_external_source",
    )
    assert content_hash(meta, first) == content_hash(meta, second)


def test_executable_rule_rejects_unknown_implementation_and_missing_parameter() -> None:
    valid = _valid_routing_rule()
    with pytest.raises(ContractError, match="unknown implementation_id"):
        validate_executable_rule(valid.model_copy(update={"implementation_id": "not_registered"}))
    with pytest.raises(ContractError, match="missing required parameters"):
        validate_executable_rule(valid.model_copy(update={"parameters": valid.parameters[:-1]}))


@pytest.mark.parametrize(
    ("update", "message"),
    (
        ({"rule_kind": "support"}, "kind must be routing"),
        ({"implementation_version": 2}, "version must be 1"),
        ({"input_role_specs": ()}, "input role IDs differ"),
        ({"output_schema_ref": {"schema_id": "wrong", "schema_version": 1}}, "output schema drift"),
    ),
)
def test_executable_rule_rejects_signature_drift(update: dict[str, object], message: str) -> None:
    mutated = _valid_routing_rule().model_copy(update=update)
    with pytest.raises(ContractError, match=message):
        validate_executable_rule(mutated)


def test_rule_registry_rejects_code_artifact_hash_drift() -> None:
    declaration = MANIFEST["closed_rule_implementations"]["constant_true"]
    original = declaration["code_artifact_hash"]
    declaration["code_artifact_hash"] = "0" * 64
    try:
        with pytest.raises(ContractError, match="code-artifact hash drift"):
            validate_rule_registry_manifest()
    finally:
        declaration["code_artifact_hash"] = original


def test_p0_report_matches_noncomposite_expected_profile() -> None:
    preserve = run_trace(TraceSpec("P0-E-PRESERVE", "U1", "preserve", True, review_delay=30))
    fallback = run_trace(TraceSpec("P0-E-FALLBACK", "U1", "fallback", True))
    report = render_p0_report(preserve, fallback)
    assert report["assessment_profile"]["preserve"]["F0"]["status"] == "pass"
    assert report["assessment_profile"]["fallback"]["F0"]["status"] == "fail"
    assert report["assessment_profile"]["fallback"]["F4"]["status"] == "fail"
    assert report["conclusion"]["overall_score"] == "prohibited"
    assert preserve.held_bundle_hash == fallback.held_bundle_hash
