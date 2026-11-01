"""Closed synthetic profiles used by the deterministic vertical slice."""

from __future__ import annotations

from .configuration import ParameterValue, PolicyProfileSpec, ProcessProfileSpec, ScenarioOverlaySpec


CORE_CAPABILITIES = frozenset({"notice", "response", "representation", "routing", "review", "progression", "correction", "restoration", "assistance", "extension", "evidence_acquisition"})
CORE_ACTIONS = frozenset({"hold", "request_evidence", "review", "progress", "correct", "restore"})
CORE_SLOTS = frozenset({"notice_delay", "response_deadline", "review_capacity", "review_service_time"})
STOCHASTIC_SLOTS = frozenset({
    "initiation_window", "extension_duration", "review_service_window", "notice_delivery_probability",
    "administrative_access_probability", "comprehension_probability",
    "record_availability_probability", "response_effort_limit", "assistance_effort_bonus",
    "extension_effort_bonus", "extension_need_probability",
    "evidence_retrieval_success_probability", "evidence_retrieval_latency_scale",
    "external_consequence_delay", "recovery_start_delay",
    "recovery_capacity", "recovery_service_time", "recovery_window",
    "correction_request_delay", "correction_uptake_probability",
    "reassessment_capacity", "reassessment_service_time", "correction_window",
    "administrative_cutoff",
})


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


def stochastic_process(profile_id: str = "SYNTHETIC-STOCHASTIC@1") -> ProcessProfileSpec:
    return canonical_process(profile_id).model_copy(update={
        "stage_ids": (
            "arrival", "notice", "response", "routing", "review", "action",
            "recovery", "correction", "reassessment", "closed",
        ),
        "capabilities": CORE_CAPABILITIES | {"recovery", "reassessment"},
        "action_type_ids": CORE_ACTIONS | {"recover", "reassess"},
        "parameter_slot_ids": CORE_SLOTS | STOCHASTIC_SLOTS,
    })


def policy(profile_id: str) -> PolicyProfileSpec:
    semantics = {"U0": "none", "U1": "none", "U2C": "fail_closed", "U2O": "fail_open", "U3": "fail_closed"}[profile_id]
    required = frozenset({"notice", "response", "representation", "routing", "progression"})
    if profile_id in {"U2C", "U2O", "U3"}:
        required |= {"review"}
    if profile_id == "U0":
        required |= {"extension"}
    if profile_id == "U3":
        required |= {"assistance", "extension", "evidence_acquisition"}
    required_actions = {"progress", "hold"}
    if profile_id == "U3":
        required_actions.add("request_evidence")
    return PolicyProfileSpec(
        profile_id=profile_id,
        required_capabilities=required,
        required_action_type_ids=frozenset(required_actions),
        parameter_slot_ids=CORE_SLOTS,
        gate_semantics=semantics,
    )


def smoke_overlay(overlay_id: str = "SMOKE-OVERLAY@1") -> ScenarioOverlaySpec:
    values = {"notice_delay": "1", "response_deadline": "21", "review_capacity": "1", "review_service_time": "30"}
    return ScenarioOverlaySpec(
        overlay_id=overlay_id,
        parameters=tuple(ParameterValue(slot_id=slot, value=value, provenance="stylized", owner_id=overlay_id) for slot, value in values.items()),
    )
