"""Finite-cohort stochastic substrate built from policy-neutral keyed latents."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from typing import Literal

from .configuration import CompiledConfigurationSpec, ParameterValue, ScenarioOverlaySpec
from .events import DEFAULT_PRIORITIES, Event, EventQueue
from .policies import EngagementDecision, EngagementInputs, map_engagement, policy_behavior
from .random_streams import DRAW_FAMILY_IDS, KeyedDraw, KeyedRandomStream, normalized_decimal
from .schemas import ContractError


@dataclass(frozen=True)
class StochasticInputOverlay:
    overlay_id: str
    provenance: Literal["stylized", "sensitivity"]
    initiation_window: Decimal
    notice_delay: Decimal
    response_deadline: Decimal
    review_capacity: Decimal
    review_service_time: Decimal
    extension_duration: Decimal
    notice_delivery_probability: Decimal
    administrative_access_probability: Decimal
    comprehension_probability: Decimal
    record_availability_probability: Decimal
    response_effort_limit: Decimal
    assistance_effort_bonus: Decimal
    extension_effort_bonus: Decimal
    extension_need_probability: Decimal
    evidence_retrieval_success_probability: Decimal
    evidence_retrieval_latency_scale: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.overlay_id, str) or not self.overlay_id:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "overlay_id must be nonempty")
        if self.provenance not in {"stylized", "sensitivity"}:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "stochastic inputs require stylized or sensitivity provenance")
        nonnegative = {
            "initiation_window": self.initiation_window,
            "notice_delay": self.notice_delay,
            "response_deadline": self.response_deadline,
            "review_service_time": self.review_service_time,
            "extension_duration": self.extension_duration,
            "evidence_retrieval_latency_scale": self.evidence_retrieval_latency_scale,
        }
        for field_name, value in nonnegative.items():
            if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
                raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must be finite and nonnegative")
        if self.response_deadline == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "response_deadline must be positive")
        if not isinstance(self.review_capacity, Decimal) or self.review_capacity <= 0 or self.review_capacity != self.review_capacity.to_integral_value():
            raise ContractError("SCENARIO_PARAMETER_INVALID", "review_capacity must be a positive integer value")
        probabilities = {
            "notice_delivery_probability": self.notice_delivery_probability,
            "administrative_access_probability": self.administrative_access_probability,
            "comprehension_probability": self.comprehension_probability,
            "record_availability_probability": self.record_availability_probability,
            "response_effort_limit": self.response_effort_limit,
            "assistance_effort_bonus": self.assistance_effort_bonus,
            "extension_effort_bonus": self.extension_effort_bonus,
            "extension_need_probability": self.extension_need_probability,
            "evidence_retrieval_success_probability": self.evidence_retrieval_success_probability,
        }
        for field_name, value in probabilities.items():
            if not isinstance(value, Decimal) or not value.is_finite() or not (Decimal(0) <= value <= Decimal(1)):
                raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must lie in [0, 1]")

    def canonical_value(self) -> dict[str, str]:
        return {
            "overlay_id": self.overlay_id,
            "provenance": self.provenance,
            "initiation_window": normalized_decimal(self.initiation_window),
            "notice_delay": normalized_decimal(self.notice_delay),
            "response_deadline": normalized_decimal(self.response_deadline),
            "review_capacity": normalized_decimal(self.review_capacity),
            "review_service_time": normalized_decimal(self.review_service_time),
            "extension_duration": normalized_decimal(self.extension_duration),
            "notice_delivery_probability": normalized_decimal(self.notice_delivery_probability),
            "administrative_access_probability": normalized_decimal(self.administrative_access_probability),
            "comprehension_probability": normalized_decimal(self.comprehension_probability),
            "record_availability_probability": normalized_decimal(self.record_availability_probability),
            "response_effort_limit": normalized_decimal(self.response_effort_limit),
            "assistance_effort_bonus": normalized_decimal(self.assistance_effort_bonus),
            "extension_effort_bonus": normalized_decimal(self.extension_effort_bonus),
            "extension_need_probability": normalized_decimal(self.extension_need_probability),
            "evidence_retrieval_success_probability": normalized_decimal(self.evidence_retrieval_success_probability),
            "evidence_retrieval_latency_scale": normalized_decimal(self.evidence_retrieval_latency_scale),
        }

    def to_compilation_overlay(self) -> ScenarioOverlaySpec:
        values = self.canonical_value()
        parameters = tuple(
            ParameterValue(
                slot_id=slot_id, value=value, provenance=self.provenance, owner_id=self.overlay_id,
            )
            for slot_id, value in values.items()
            if slot_id not in {"overlay_id", "provenance"}
        )
        return ScenarioOverlaySpec(overlay_id=self.overlay_id, parameters=parameters)


@dataclass(frozen=True)
class StochasticCohortSpec:
    scenario_id: str
    seed_id: str
    case_ids: tuple[str, ...]
    overlay: StochasticInputOverlay

    def __post_init__(self) -> None:
        if any(not isinstance(value, str) or not value for value in (self.scenario_id, self.seed_id)):
            raise ContractError("SCENARIO_INVALID", "scenario and seed IDs must be nonempty")
        if not isinstance(self.case_ids, tuple) or not self.case_ids or any(not isinstance(case_id, str) or not case_id for case_id in self.case_ids):
            raise ContractError("SCENARIO_INVALID", "finite cohort requires nonempty case IDs")
        if len(self.case_ids) != len(set(self.case_ids)):
            raise ContractError("SCENARIO_INVALID", "finite cohort case IDs must be unique")
        if not isinstance(self.overlay, StochasticInputOverlay):
            raise ContractError("SCENARIO_PARAMETER_INVALID", "stochastic cohort requires a typed input overlay")


@dataclass(frozen=True)
class StochasticCase:
    case_id: str
    arrival_time: Decimal
    keyed_draws: tuple[KeyedDraw, ...]

    @property
    def draw_map(self) -> dict[tuple[str, int], Decimal]:
        return {
            (draw.key.event_family_id, draw.key.draw_index): draw.unit_interval_value
            for draw in self.keyed_draws
        }

    @property
    def draw_hash(self) -> str:
        values = [draw.content_hash for draw in self.keyed_draws]
        return sha256(json.dumps(values, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class RunTelemetry:
    case_count: int
    keyed_draw_count: int
    draw_family_counts: tuple[tuple[str, int], ...]
    duplicate_draw_key_count: int
    cohort_hash: str


@dataclass(frozen=True)
class StochasticCohort:
    scenario_id: str
    overlay: StochasticInputOverlay
    seed_id: str
    cases: tuple[StochasticCase, ...]
    telemetry: RunTelemetry


@dataclass(frozen=True)
class EngagementTrace:
    case_id: str
    policy_id: str
    decision: EngagementDecision
    events: tuple[Event, ...]
    exogenous_draw_hash: str
    event_hash: str


@dataclass(frozen=True)
class EngagementRunTelemetry:
    case_count: int
    event_count: int
    response_count: int
    adequate_response_evidence_count: int
    assistance_count: int
    extension_count: int
    retrieval_request_count: int
    retrieved_evidence_count: int
    review_queue_count: int
    event_hash: str


@dataclass(frozen=True)
class EngagementRun:
    scenario_id: str
    policy_id: str
    cohort_hash: str
    traces: tuple[EngagementTrace, ...]
    telemetry: EngagementRunTelemetry


def _cohort_hash(spec: StochasticCohortSpec, cases: tuple[StochasticCase, ...]) -> str:
    value = {
        "case_draw_hashes": {case.case_id: case.draw_hash for case in cases},
        "overlay": spec.overlay.canonical_value(),
        "scenario_id": spec.scenario_id,
        "seed_id": spec.seed_id,
    }
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def generate_stochastic_cohort(spec: StochasticCohortSpec) -> StochasticCohort:
    """Generate shared exogenous latents; policy mappings consume them later."""

    stream = KeyedRandomStream(spec.seed_id)
    cases: list[StochasticCase] = []
    for case_id in sorted(spec.case_ids):
        draws = tuple(stream.draw(case_id, family_id) for family_id in sorted(DRAW_FAMILY_IDS))
        initiation = next(draw for draw in draws if draw.key.event_family_id == "initiation")
        with localcontext() as context:
            context.prec = 50
            arrival_time = initiation.unit_interval_value * spec.overlay.initiation_window
        cases.append(StochasticCase(case_id, arrival_time, draws))
    frozen_cases = tuple(cases)
    all_draws = tuple(draw for case in frozen_cases for draw in case.keyed_draws)
    keys = [draw.key for draw in all_draws]
    family_counts = Counter(draw.key.event_family_id for draw in all_draws)
    cohort_hash = _cohort_hash(spec, frozen_cases)
    telemetry = RunTelemetry(
        case_count=len(frozen_cases),
        keyed_draw_count=len(all_draws),
        draw_family_counts=tuple(sorted(family_counts.items())),
        duplicate_draw_key_count=len(keys) - len(set(keys)),
        cohort_hash=cohort_hash,
    )
    if telemetry.duplicate_draw_key_count:
        raise ContractError("RANDOM_DRAW_KEY_INVALID", "duplicate keyed draw identity in cohort")
    return StochasticCohort(spec.scenario_id, spec.overlay, spec.seed_id, frozen_cases, telemetry)


def _event_hash(events: tuple[Event, ...]) -> str:
    value = [
        {
            "case_id": event.case_id,
            "causal_event_key": event.causal_event_key,
            "details": event.details,
            "event_type_id": event.event_type_id,
            "timestamp": normalized_decimal(event.timestamp),
        }
        for event in events
    ]
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _case_engagement_trace(case: StochasticCase, policy_id: str, overlay: StochasticInputOverlay) -> EngagementTrace:
    behavior = policy_behavior(policy_id)
    draws = case.draw_map
    draw_ids = {
        draw.key.event_family_id: draw.keyed_draw_id
        for draw in case.keyed_draws
        if draw.key.draw_index == 0
    }
    inputs = EngagementInputs(
        notice_delivered=draws[("notice_delivery", 0)] < overlay.notice_delivery_probability,
        administrative_access=draws[("administrative_access", 0)] < overlay.administrative_access_probability,
        comprehension=draws[("comprehension", 0)] < overlay.comprehension_probability,
        records_available=draws[("record_availability", 0)] < overlay.record_availability_probability,
        response_effort=draws[("response_effort", 0)],
        extension_needed=draws[("extension_need", 0)] < overlay.extension_need_probability,
        retrieval_success=draws[("evidence_retrieval_success", 0)] < overlay.evidence_retrieval_success_probability,
    )
    decision = map_engagement(
        policy_id=policy_id,
        inputs=inputs,
        response_effort_limit=overlay.response_effort_limit,
        assistance_effort_bonus=overlay.assistance_effort_bonus,
        extension_effort_bonus=overlay.extension_effort_bonus,
    )
    queue = EventQueue()
    root_key = f"{case.case_id}:ENGAGEMENT"

    def emit(event_type_id: str, timestamp: Decimal, cause_id: str, used_draw_families: tuple[str, ...] = ()) -> None:
        causal_key = f"{root_key}:{cause_id}:{event_type_id}"
        queue.push(Event(
            event_id=f"{policy_id}:{causal_key}", event_type_id=event_type_id, timestamp=timestamp,
            causal_event_key=causal_key, root_event_key=root_key, descendant_path=(cause_id, event_type_id),
            transition_rank=DEFAULT_PRIORITIES[event_type_id], case_id=case.case_id,
            details={
                "policy_id": policy_id,
                "keyed_draw_ids": tuple(draw_ids[family] for family in used_draw_families),
            },
        ))

    with localcontext() as context:
        context.prec = 50
        notice_time = case.arrival_time + overlay.notice_delay
        initial_deadline = notice_time + overlay.response_deadline
        extension_amount = (
            draws[("deadline_extension", 0)] * overlay.extension_duration
            if decision.extension_granted else Decimal(0)
        )
        effective_deadline = initial_deadline + extension_amount
        response_time = notice_time + draws[("response_effort", 0)] * (effective_deadline - notice_time)

    emit("CASE_ARRIVAL", case.arrival_time, "arrival", ("initiation",))
    emit("SOURCE_EVIDENCE_INGESTED", case.arrival_time, "source")
    emit("NOTICE_SENT", notice_time, "notice")
    if inputs.notice_delivered:
        emit("NOTICE_DELIVERED", notice_time, "notice", ("notice_delivery",))
        emit("ACCESS_ATTEMPTED", notice_time, "access", ("administrative_access",))
    else:
        emit("NOTICE_FAILED", notice_time, "notice", ("notice_delivery",))

    if decision.extension_granted:
        extension_request_time = notice_time + overlay.response_deadline / Decimal(2)
        emit("EXTENSION_REQUESTED", extension_request_time, "extension", ("extension_need",))
        emit("EXTENSION_GRANTED", extension_request_time, "extension", ("deadline_extension",))

    if decision.responded:
        emit("SUBJECT_RESPONDED", response_time, "response", ("response_effort", "comprehension"))
        emit("EVIDENCE_SUBMITTED", response_time, "response", ("record_availability",))
        emit(
            "EVIDENCE_ACCEPTED" if decision.adequate_response_evidence else "EVIDENCE_REJECTED",
            response_time, "response", ("record_availability",),
        )
    else:
        emit("SUBJECT_NONRESPONSE", effective_deadline, "response", ("response_effort",))

    routing_time = effective_deadline
    if decision.proactive_retrieval_requested:
        request_time = response_time if decision.responded else notice_time + overlay.response_deadline / Decimal(2)
        with localcontext() as context:
            context.prec = 50
            return_time = request_time + draws[("evidence_retrieval_latency", 0)] * overlay.evidence_retrieval_latency_scale
        emit("EVIDENCE_REQUESTED", request_time, "external_evidence")
        emit("EXTERNAL_EVIDENCE_RETURNED", return_time, "external_evidence", ("evidence_retrieval_latency",))
        emit(
            "EVIDENCE_ACCEPTED" if decision.retrieved_evidence else "EVIDENCE_REJECTED",
            return_time, "external_evidence", ("evidence_retrieval_success",),
        )
        routing_time = max(routing_time, return_time)

    evidence_sufficient = decision.adequate_response_evidence or decision.retrieved_evidence
    representation_mode = (
        "period_specific_evidence" if evidence_sufficient
        else "imputed_unflagged" if behavior.policy_id == "U1"
        else "imputed_flagged" if behavior.permits_imputation
        else "evidence_status_preserved"
    )
    emit("DEADLINE_REACHED", effective_deadline, "deadline", ("deadline_extension",) if decision.extension_granted else ())
    emit("REPRESENTATION_APPLIED", routing_time, "representation")
    emit("REPRESENTATION_SURFACED", routing_time, "representation")
    emit("ROUTING_COMPLETED", routing_time, "routing")
    review_required = behavior.review_scope == "all_progression" or (
        behavior.review_scope == "unresolved_only" and not evidence_sufficient
    )
    if review_required:
        emit("REVIEW_QUEUED", routing_time, "review")

    events = tuple(
        replace(
            event,
            details=event.details | {"representation_mode": representation_mode}
            if event.event_type_id == "REPRESENTATION_APPLIED" else event.details,
        )
        for event in queue.drain()
    )
    return EngagementTrace(case.case_id, policy_id, decision, events, case.draw_hash, _event_hash(events))


def _validate_engagement_configuration(cohort: StochasticCohort, compiled: CompiledConfigurationSpec) -> str:
    policy_id = compiled.policy_profile.profile_id
    policy_behavior(policy_id)
    if compiled.overlay_id != cohort.overlay.overlay_id or compiled.unresolved_parameter_slot_ids:
        raise ContractError("SCENARIO_CONFIGURATION_INCOMPLETE", "compiled configuration does not bind the cohort overlay")
    expected = cohort.overlay.canonical_value()
    expected_values = {key: value for key, value in expected.items() if key not in {"overlay_id", "provenance"}}
    observed_values = {receipt.slot_id: str(receipt.value) for receipt in compiled.receipts}
    if observed_values != expected_values:
        raise ContractError("SCENARIO_CONFIGURATION_INCOMPLETE", "compiled parameter receipts differ from the cohort overlay")
    if any(receipt.provenance != cohort.overlay.provenance for receipt in compiled.receipts):
        raise ContractError("SCENARIO_CONFIGURATION_INCOMPLETE", "compiled parameter provenance differs from the cohort overlay")
    return policy_id


def run_engagement_stage(cohort: StochasticCohort, compiled: CompiledConfigurationSpec) -> EngagementRun:
    policy_id = _validate_engagement_configuration(cohort, compiled)
    traces = tuple(_case_engagement_trace(case, policy_id, cohort.overlay) for case in cohort.cases)
    all_events = tuple(event for trace in traces for event in trace.events)
    event_hash = _event_hash(all_events)
    telemetry = EngagementRunTelemetry(
        case_count=len(traces),
        event_count=len(all_events),
        response_count=sum(trace.decision.responded for trace in traces),
        adequate_response_evidence_count=sum(trace.decision.adequate_response_evidence for trace in traces),
        assistance_count=sum(trace.decision.assistance_used for trace in traces),
        extension_count=sum(trace.decision.extension_granted for trace in traces),
        retrieval_request_count=sum(trace.decision.proactive_retrieval_requested for trace in traces),
        retrieved_evidence_count=sum(trace.decision.retrieved_evidence for trace in traces),
        review_queue_count=sum(event.event_type_id == "REVIEW_QUEUED" for event in all_events),
        event_hash=event_hash,
    )
    return EngagementRun(cohort.scenario_id, policy_id, cohort.telemetry.cohort_hash, traces, telemetry)
