from __future__ import annotations

import pytest

from uncertainty_permission_simulation.formal_model import render_p0_report
from uncertainty_permission_simulation.process_model import TraceSpec, run_trace
from uncertainty_permission_simulation.schemas import PAYLOAD_MODELS, RecordMeta, StoredRecord, content_hash, validate_model_manifest_inventory


def test_manifest_model_inventory_is_bidirectional() -> None:
    validate_model_manifest_inventory()
    assert "CompiledConfiguration" in PAYLOAD_MODELS
    assert "SimulationCase" in PAYLOAD_MODELS


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


def test_p0_report_matches_noncomposite_expected_profile() -> None:
    preserve = run_trace(TraceSpec("P0-E-PRESERVE", "U1", "preserve", True, review_delay=30))
    fallback = run_trace(TraceSpec("P0-E-FALLBACK", "U1", "fallback", True))
    report = render_p0_report(preserve, fallback)
    assert report["assessment_profile"]["preserve"]["F0"]["status"] == "pass"
    assert report["assessment_profile"]["fallback"]["F0"]["status"] == "fail"
    assert report["assessment_profile"]["fallback"]["F4"]["status"] == "fail"
    assert report["conclusion"]["overall_score"] == "prohibited"
    assert preserve.held_bundle_hash == fallback.held_bundle_hash
