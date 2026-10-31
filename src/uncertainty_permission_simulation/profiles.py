"""Closed synthetic profiles used by the deterministic vertical slice."""

from __future__ import annotations

from .configuration import ParameterValue, PolicyProfileSpec, ProcessProfileSpec, ScenarioOverlaySpec


CORE_CAPABILITIES = frozenset({"notice", "response", "representation", "routing", "review", "progression", "correction", "restoration"})
CORE_ACTIONS = frozenset({"hold", "request_evidence", "review", "progress", "correct", "restore"})
CORE_SLOTS = frozenset({"notice_delay", "response_deadline", "review_capacity", "review_service_time"})


def canonical_process(profile_id: str = "SYNTHETIC-CORE@1") -> ProcessProfileSpec:
    return ProcessProfileSpec(
        profile_id=profile_id,
        stage_ids=("arrival", "notice", "response", "routing", "review", "action", "correction", "closed"),
        capabilities=CORE_CAPABILITIES,
        action_type_ids=CORE_ACTIONS,
        parameter_slot_ids=CORE_SLOTS,
    )


def nonisomorphic_process() -> ProcessProfileSpec:
    return ProcessProfileSpec(
        profile_id="SYNTHETIC-NONISOMORPHIC@1",
        stage_ids=("intake", "triage", "optional_review", "evidence", "decision", "closed"),
        capabilities=CORE_CAPABILITIES | {"triage"},
        action_type_ids=CORE_ACTIONS,
        parameter_slot_ids=CORE_SLOTS,
    )


def policy(profile_id: str) -> PolicyProfileSpec:
    semantics = {"U1": "none", "U2C": "fail_closed", "U2O": "fail_open"}[profile_id]
    required = frozenset({"notice", "response", "representation", "routing", "progression"})
    if profile_id != "U1":
        required |= {"review"}
    return PolicyProfileSpec(
        profile_id=profile_id,
        required_capabilities=required,
        required_action_type_ids=frozenset({"progress", "hold"}),
        parameter_slot_ids=CORE_SLOTS,
        gate_semantics=semantics,
    )


def smoke_overlay(overlay_id: str = "SMOKE-OVERLAY@1") -> ScenarioOverlaySpec:
    values = {"notice_delay": "1", "response_deadline": "21", "review_capacity": "1", "review_service_time": "30"}
    return ScenarioOverlaySpec(
        overlay_id=overlay_id,
        parameters=tuple(ParameterValue(slot_id=slot, value=value, provenance="stylized", owner_id=overlay_id) for slot, value in values.items()),
    )
