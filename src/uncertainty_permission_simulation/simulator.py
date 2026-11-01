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
from .policies import ActionDecision, EngagementDecision, EngagementInputs, decide_action, map_engagement, policy_behavior
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
    review_service_window: Decimal
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
    external_consequence_delay: Decimal
    recovery_start_delay: Decimal
    correction_request_delay: Decimal
    correction_uptake_probability: Decimal
    reassessment_capacity: Decimal
    reassessment_service_time: Decimal
    correction_window: Decimal

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
            "review_service_window": self.review_service_window,
            "extension_duration": self.extension_duration,
            "evidence_retrieval_latency_scale": self.evidence_retrieval_latency_scale,
            "external_consequence_delay": self.external_consequence_delay,
            "recovery_start_delay": self.recovery_start_delay,
            "correction_request_delay": self.correction_request_delay,
            "reassessment_service_time": self.reassessment_service_time,
            "correction_window": self.correction_window,
        }
        for field_name, value in nonnegative.items():
            if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
                raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must be finite and nonnegative")
        if self.response_deadline == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "response_deadline must be positive")
        if self.review_service_window == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "review_service_window must be positive")
        if self.reassessment_service_time == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "reassessment_service_time must be positive")
        if self.correction_window == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "correction_window must be positive")
        capacities = {
            "review_capacity": self.review_capacity,
            "reassessment_capacity": self.reassessment_capacity,
        }
        for field_name, value in capacities.items():
            if not isinstance(value, Decimal) or value <= 0 or value != value.to_integral_value():
                raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must be a positive integer value")
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
            "correction_uptake_probability": self.correction_uptake_probability,
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
            "review_service_window": normalized_decimal(self.review_service_window),
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
            "external_consequence_delay": normalized_decimal(self.external_consequence_delay),
            "recovery_start_delay": normalized_decimal(self.recovery_start_delay),
            "correction_request_delay": normalized_decimal(self.correction_request_delay),
            "correction_uptake_probability": normalized_decimal(self.correction_uptake_probability),
            "reassessment_capacity": normalized_decimal(self.reassessment_capacity),
            "reassessment_service_time": normalized_decimal(self.reassessment_service_time),
            "correction_window": normalized_decimal(self.correction_window),
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
class ServiceQueueConfig:
    queue_id: str
    capacity: int
    discipline: Literal["fifo"] = "fifo"

    def __post_init__(self) -> None:
        if not isinstance(self.queue_id, str) or not self.queue_id:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "queue_id must be nonempty")
        if not isinstance(self.capacity, int) or isinstance(self.capacity, bool) or self.capacity <= 0:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "queue capacity must be a positive integer")
        if self.discipline != "fifo":
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "unsupported queue discipline")


@dataclass(frozen=True)
class ServiceRequest:
    request_id: str
    case_id: str
    queued_at: Decimal
    service_time: Decimal
    deadline: Decimal

    def __post_init__(self) -> None:
        if any(not isinstance(value, str) or not value for value in (self.request_id, self.case_id)):
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "service request IDs must be nonempty")
        for field_name in ("queued_at", "service_time", "deadline"):
            value = getattr(self, field_name)
            if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
                raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"{field_name} must be finite and nonnegative")
        if self.deadline < self.queued_at:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "service deadline precedes queue entry")


@dataclass(frozen=True)
class ServiceVisit:
    request_id: str
    case_id: str
    server_id: str
    queued_at: Decimal
    started_at: Decimal
    completed_at: Decimal
    service_time: Decimal
    wait_time: Decimal
    deadline: Decimal
    completed_by_deadline: bool


@dataclass(frozen=True)
class ServiceQueueTelemetry:
    request_count: int
    immediate_start_count: int
    timely_completion_count: int
    late_completion_count: int
    total_wait_time: Decimal
    max_wait_time: Decimal
    total_service_time: Decimal
    schedule_hash: str


@dataclass(frozen=True)
class ServiceQueueRun:
    config: ServiceQueueConfig
    visits: tuple[ServiceVisit, ...]
    telemetry: ServiceQueueTelemetry


def _service_schedule_hash(config: ServiceQueueConfig, visits: tuple[ServiceVisit, ...]) -> str:
    value = {
        "capacity": config.capacity,
        "discipline": config.discipline,
        "queue_id": config.queue_id,
        "visits": [
            {
                "case_id": visit.case_id,
                "completed_at": normalized_decimal(visit.completed_at),
                "completed_by_deadline": visit.completed_by_deadline,
                "deadline": normalized_decimal(visit.deadline),
                "queued_at": normalized_decimal(visit.queued_at),
                "request_id": visit.request_id,
                "server_id": visit.server_id,
                "service_time": normalized_decimal(visit.service_time),
                "started_at": normalized_decimal(visit.started_at),
                "wait_time": normalized_decimal(visit.wait_time),
            }
            for visit in visits
        ],
    }
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def schedule_service_queue(
    config: ServiceQueueConfig,
    requests: tuple[ServiceRequest, ...],
) -> ServiceQueueRun:
    """Schedule a finite, work-conserving FIFO queue with deterministic server ties."""

    if not isinstance(config, ServiceQueueConfig):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "service queue requires a typed configuration")
    if not isinstance(requests, tuple):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "service requests must be a tuple")
    if any(not isinstance(request, ServiceRequest) for request in requests):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "service queue requires typed requests")
    request_ids = [request.request_id for request in requests]
    if len(request_ids) != len(set(request_ids)):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "duplicate service request identity")
    ordered = sorted(requests, key=lambda request: (request.queued_at, request.case_id, request.request_id))
    available_at = [Decimal(0) for _ in range(config.capacity)]
    visits: list[ServiceVisit] = []
    for request in ordered:
        server_index = min(range(config.capacity), key=lambda index: (available_at[index], index))
        started_at = max(request.queued_at, available_at[server_index])
        with localcontext() as context:
            context.prec = 50
            completed_at = started_at + request.service_time
            wait_time = started_at - request.queued_at
        available_at[server_index] = completed_at
        visits.append(ServiceVisit(
            request_id=request.request_id,
            case_id=request.case_id,
            server_id=f"{config.queue_id}:SERVER-{server_index + 1}",
            queued_at=request.queued_at,
            started_at=started_at,
            completed_at=completed_at,
            service_time=request.service_time,
            wait_time=wait_time,
            deadline=request.deadline,
            completed_by_deadline=completed_at <= request.deadline,
        ))
    frozen_visits = tuple(visits)
    with localcontext() as context:
        context.prec = 50
        total_wait = sum((visit.wait_time for visit in frozen_visits), Decimal(0))
        total_service = sum((visit.service_time for visit in frozen_visits), Decimal(0))
    max_wait = max((visit.wait_time for visit in frozen_visits), default=Decimal(0))
    schedule_hash = _service_schedule_hash(config, frozen_visits)
    timely_count = sum(visit.completed_by_deadline for visit in frozen_visits)
    telemetry = ServiceQueueTelemetry(
        request_count=len(frozen_visits),
        immediate_start_count=sum(visit.wait_time == 0 for visit in frozen_visits),
        timely_completion_count=timely_count,
        late_completion_count=len(frozen_visits) - timely_count,
        total_wait_time=total_wait,
        max_wait_time=max_wait,
        total_service_time=total_service,
        schedule_hash=schedule_hash,
    )
    return ServiceQueueRun(config, frozen_visits, telemetry)


@dataclass(frozen=True)
class EngagementTrace:
    case_id: str
    policy_id: str
    decision: EngagementDecision
    events: tuple[Event, ...]
    exogenous_draw_hash: str
    event_hash: str
    action_decision: ActionDecision | None = None


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
    review_started_count: int
    review_completed_count: int
    timely_review_count: int
    late_review_count: int
    review_total_wait_time: Decimal
    review_max_wait_time: Decimal
    review_schedule_hash: str
    action_count: int
    progression_count: int
    hold_count: int
    request_evidence_action_count: int
    supported_progression_count: int
    unsupported_progression_count: int
    evidentially_supported_progression_count: int
    evidentially_unsupported_progression_count: int
    unauthorized_progression_count: int
    gate_applicable_count: int
    gate_safe_count: int
    gate_unsafe_count: int
    review_authorization_count: int
    fail_open_timeout_progression_count: int
    fail_closed_timeout_hold_count: int
    external_exposure_count: int
    recovery_started_count: int
    supported_exposure_count: int
    unsupported_exposure_count: int
    evidentially_unsupported_exposure_count: int
    unauthorized_exposure_count: int
    correction_eligible_count: int
    correction_request_count: int
    correction_not_requested_count: int
    reassessment_started_count: int
    reassessment_completed_count: int
    timely_reassessment_count: int
    late_reassessment_count: int
    reassessment_total_wait_time: Decimal
    reassessment_max_wait_time: Decimal
    reassessment_schedule_hash: str
    correction_executed_count: int
    timely_correction_count: int
    late_correction_count: int
    correction_unresolved_count: int
    recovery_active_after_correction_count: int
    correction_total_exposure_time: Decimal
    correction_max_exposure_time: Decimal
    event_hash: str


@dataclass(frozen=True)
class EngagementRun:
    scenario_id: str
    policy_id: str
    cohort_hash: str
    traces: tuple[EngagementTrace, ...]
    system_events: tuple[Event, ...]
    review_queue: ServiceQueueRun
    reassessment_queue: ServiceQueueRun
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

    def emit(
        event_type_id: str,
        timestamp: Decimal,
        cause_id: str,
        used_draw_families: tuple[str, ...] = (),
        extra_details: dict[str, object] | None = None,
    ) -> None:
        causal_key = f"{root_key}:{cause_id}:{event_type_id}"
        queue.push(Event(
            event_id=f"{policy_id}:{causal_key}", event_type_id=event_type_id, timestamp=timestamp,
            causal_event_key=causal_key, root_event_key=root_key, descendant_path=(cause_id, event_type_id),
            transition_rank=DEFAULT_PRIORITIES[event_type_id], case_id=case.case_id,
            details={
                "policy_id": policy_id,
                "keyed_draw_ids": tuple(draw_ids[family] for family in used_draw_families),
            } | (extra_details or {}),
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
    emit(
        "DEADLINE_REACHED", effective_deadline, "deadline",
        ("deadline_extension",) if decision.extension_granted else (),
        {"deadline_kind": "response"},
    )
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


def _review_queue_run(
    cohort: StochasticCohort,
    traces: tuple[EngagementTrace, ...],
) -> ServiceQueueRun:
    cases = {case.case_id: case for case in cohort.cases}
    requests: list[ServiceRequest] = []
    for trace in traces:
        queued_events = tuple(event for event in trace.events if event.event_type_id == "REVIEW_QUEUED")
        if len(queued_events) > 1:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"multiple review queue entries for {trace.case_id}")
        if not queued_events:
            continue
        queued_at = queued_events[0].timestamp
        service_draw = cases[trace.case_id].draw_map[("review_service", 0)]
        with localcontext() as context:
            context.prec = 50
            service_time = service_draw * cohort.overlay.review_service_time
            deadline = queued_at + cohort.overlay.review_service_window
        requests.append(ServiceRequest(
            request_id=f"{trace.case_id}:review",
            case_id=trace.case_id,
            queued_at=queued_at,
            service_time=service_time,
            deadline=deadline,
        ))
    return schedule_service_queue(
        ServiceQueueConfig(
            queue_id=f"{cohort.scenario_id}:review",
            capacity=int(cohort.overlay.review_capacity),
        ),
        tuple(requests),
    )


def _add_review_events(
    trace: EngagementTrace,
    visit: ServiceVisit | None,
    case: StochasticCase,
    queue_id: str,
) -> EngagementTrace:
    if visit is None:
        return trace
    policy_id = trace.policy_id
    root_key = f"{case.case_id}:ENGAGEMENT"
    review_draw_id = next(
        draw.keyed_draw_id
        for draw in case.keyed_draws
        if draw.key.event_family_id == "review_service" and draw.key.draw_index == 0
    )

    def service_event(
        event_type_id: str,
        timestamp: Decimal,
        cause_id: str,
        details: dict[str, object],
    ) -> Event:
        causal_key = f"{root_key}:{cause_id}:{event_type_id}"
        return Event(
            event_id=f"{policy_id}:{causal_key}",
            event_type_id=event_type_id,
            timestamp=timestamp,
            causal_event_key=causal_key,
            root_event_key=root_key,
            descendant_path=(cause_id, event_type_id),
            transition_rank=DEFAULT_PRIORITIES[event_type_id],
            case_id=case.case_id,
            details={"policy_id": policy_id, "keyed_draw_ids": (), "queue_id": queue_id} | details,
        )

    common = {
        "review_kind": "pre_action",
        "service_request_id": visit.request_id,
        "server_id": visit.server_id,
        "service_deadline": normalized_decimal(visit.deadline),
        "service_time": normalized_decimal(visit.service_time),
        "wait_time": normalized_decimal(visit.wait_time),
    }
    added = (
        service_event(
            "REVIEW_STARTED", visit.started_at, "review_service",
            common | {"keyed_draw_ids": (review_draw_id,)},
        ),
        service_event(
            "REVIEW_COMPLETED", visit.completed_at, "review_service",
            common | {
                "completed_by_deadline": visit.completed_by_deadline,
                "keyed_draw_ids": (review_draw_id,),
            },
        ),
        service_event(
            "DEADLINE_REACHED", visit.deadline, "review_deadline",
            {
                "deadline_kind": "review_service",
                "review_completed_by_deadline": visit.completed_by_deadline,
                "service_request_id": visit.request_id,
            },
        ),
    )
    queue = EventQueue()
    for event in trace.events + added:
        queue.push(event)
    events = queue.drain()
    return replace(trace, events=events, event_hash=_event_hash(events))


def _add_action_events(
    trace: EngagementTrace,
    visit: ServiceVisit | None,
) -> EngagementTrace:
    review_required = visit is not None
    review_completed_by_deadline = visit.completed_by_deadline if visit is not None else False
    routing_events = tuple(event for event in trace.events if event.event_type_id == "ROUTING_COMPLETED")
    if len(routing_events) != 1:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"expected one routing event for {trace.case_id}")
    evidence_sufficient = (
        trace.decision.adequate_response_evidence or trace.decision.retrieved_evidence
    )
    action_decision = decide_action(
        policy_id=trace.policy_id,
        evidence_sufficient=evidence_sufficient,
        review_required=review_required,
        review_completed_by_deadline=review_completed_by_deadline,
        deadline_reached=True,
    )
    if visit is None:
        action_time = routing_events[0].timestamp
    elif visit.completed_by_deadline:
        action_time = visit.completed_at
    else:
        action_time = visit.deadline
    root_key = f"{trace.case_id}:ENGAGEMENT"

    def action_event(event_type_id: str, cause_id: str, details: dict[str, object]) -> Event:
        causal_key = f"{root_key}:{cause_id}:{event_type_id}"
        return Event(
            event_id=f"{trace.policy_id}:{causal_key}",
            event_type_id=event_type_id,
            timestamp=action_time,
            causal_event_key=causal_key,
            root_event_key=root_key,
            descendant_path=(cause_id, event_type_id),
            transition_rank=DEFAULT_PRIORITIES[event_type_id],
            case_id=trace.case_id,
            details={"policy_id": trace.policy_id, "keyed_draw_ids": ()} | details,
        )

    decision_details = {
        "action": action_decision.action,
        "reason_code": action_decision.reason_code,
        "evidence_sufficient": action_decision.evidence_sufficient,
        "review_required": action_decision.review_required,
        "review_completed_by_deadline": action_decision.review_completed_by_deadline,
        "review_authorization_recorded": action_decision.review_authorization_recorded,
        "timeout_triggered": action_decision.timeout_triggered,
        "gate_state": action_decision.gate_state,
        "functional_permission": action_decision.functional_permission,
        "progression_supported": action_decision.progression_supported,
        "evidentially_supported_progression": action_decision.evidentially_supported_progression,
        "unauthorized_progression": action_decision.unauthorized_progression,
        "gate_safe": action_decision.gate_safe,
        "unsupported_reason_codes": action_decision.unsupported_reason_codes,
    }
    added: list[Event] = []
    if action_decision.review_authorization_recorded:
        added.append(action_event(
            "EXTERNAL_AUTHORIZATION_RECORDED", "authorization",
            {
                "authorization_scope": "exact_progression_action",
                "evidence_sufficient": action_decision.evidence_sufficient,
                "review_completed_by_deadline": True,
            },
        ))
    added.append(action_event("ACTION_COMPUTED", "decision", decision_details))
    if action_decision.action == "progress":
        added.append(action_event("PROGRESSION_EXECUTED", "progression", decision_details))

    queue = EventQueue()
    for event in trace.events + tuple(added):
        queue.push(event)
    events = queue.drain()
    return replace(
        trace,
        events=events,
        event_hash=_event_hash(events),
        action_decision=action_decision,
    )


def _add_exposure_and_recovery_events(
    trace: EngagementTrace,
    overlay: StochasticInputOverlay,
) -> EngagementTrace:
    """Extend executed progression only; permission and computation never imply exposure."""

    progression_events = tuple(
        event for event in trace.events if event.event_type_id == "PROGRESSION_EXECUTED"
    )
    if trace.action_decision is None:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"missing action decision for {trace.case_id}")
    if trace.action_decision.action != "progress":
        if progression_events:
            raise ContractError(
                "SIM_SYSTEM_STATE_INCOMPLETE",
                f"non-progression action has progression event for {trace.case_id}",
            )
        return trace
    if len(progression_events) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"progression action requires exactly one execution event for {trace.case_id}",
        )

    progression = progression_events[0]
    with localcontext() as context:
        context.prec = 50
        exposure_time = progression.timestamp + overlay.external_consequence_delay
        recovery_time = exposure_time + overlay.recovery_start_delay
    root_key = f"{trace.case_id}:ENGAGEMENT"
    decision = trace.action_decision
    support_details = {
        "evidence_sufficient": decision.evidence_sufficient,
        "review_required": decision.review_required,
        "review_authorization_recorded": decision.review_authorization_recorded,
        "progression_supported": decision.progression_supported,
        "evidentially_supported_progression": decision.evidentially_supported_progression,
        "unauthorized_progression": decision.unauthorized_progression,
        "unsupported_reason_codes": decision.unsupported_reason_codes,
        "source_progression_event_key": progression.causal_event_key,
    }

    def consequence_event(
        event_type_id: str,
        timestamp: Decimal,
        cause_id: str,
        details: dict[str, object],
    ) -> Event:
        causal_key = f"{root_key}:{cause_id}:{event_type_id}"
        return Event(
            event_id=f"{trace.policy_id}:{causal_key}",
            event_type_id=event_type_id,
            timestamp=timestamp,
            causal_event_key=causal_key,
            root_event_key=root_key,
            descendant_path=("progression", cause_id, event_type_id),
            transition_rank=DEFAULT_PRIORITIES[event_type_id],
            case_id=trace.case_id,
            details={"policy_id": trace.policy_id, "keyed_draw_ids": ()} | support_details | details,
        )

    exposure_event = consequence_event(
        "EXTERNAL_CONSEQUENCE_STARTED",
        exposure_time,
        "external_consequence",
        {
            "action_type_id": "progress",
            "consequence_dimension_id": "recovery_exposure",
            "exposure_state": "active",
            "recovery_state": "not_started",
            "external_consequence_delay": normalized_decimal(overlay.external_consequence_delay),
        },
    )
    recovery_event = consequence_event(
        "EXTERNAL_CONSEQUENCE_UPDATED",
        recovery_time,
        "recovery",
        {
            "action_type_id": "recover",
            "consequence_dimension_id": "recovery_exposure",
            "exposure_state": "active",
            "recovery_state": "active",
            "source_external_consequence_event_key": exposure_event.causal_event_key,
            "recovery_start_delay": normalized_decimal(overlay.recovery_start_delay),
        },
    )
    queue = EventQueue()
    for event in trace.events + (exposure_event, recovery_event):
        queue.push(event)
    events = queue.drain()
    return replace(trace, events=events, event_hash=_event_hash(events))


def _add_correction_request_event(
    trace: EngagementTrace,
    case: StochasticCase,
    overlay: StochasticInputOverlay,
) -> EngagementTrace:
    """Model correction uptake after unsupported exposure, not correction success."""

    decision = trace.action_decision
    if decision is None:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"missing action decision for {trace.case_id}")
    correction_eligible = decision.action == "progress" and not decision.progression_supported
    if not correction_eligible:
        return trace

    recovery_events = tuple(
        event for event in trace.events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
        and event.details.get("recovery_state") == "active"
    )
    if len(recovery_events) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"correction-eligible case requires one active recovery event for {trace.case_id}",
        )
    access_draw = next(
        draw for draw in case.keyed_draws
        if draw.key.event_family_id == "administrative_access" and draw.key.draw_index == 0
    )
    if access_draw.unit_interval_value >= overlay.correction_uptake_probability:
        return trace

    recovery = recovery_events[0]
    with localcontext() as context:
        context.prec = 50
        request_time = recovery.timestamp + overlay.correction_request_delay
    root_key = f"{trace.case_id}:ENGAGEMENT"
    causal_key = f"{root_key}:correction:CORRECTION_REQUESTED"
    request = Event(
        event_id=f"{trace.policy_id}:{causal_key}",
        event_type_id="CORRECTION_REQUESTED",
        timestamp=request_time,
        causal_event_key=causal_key,
        root_event_key=root_key,
        descendant_path=("progression", "external_consequence", "recovery", "correction"),
        transition_rank=DEFAULT_PRIORITIES["CORRECTION_REQUESTED"],
        case_id=trace.case_id,
        details={
            "policy_id": trace.policy_id,
            "keyed_draw_ids": (access_draw.keyed_draw_id,),
            "action_type_id": "correct",
            "correction_eligible": True,
            "correction_uptake": True,
            "eligibility_reason": "unsupported_progression",
            "source_recovery_event_key": recovery.causal_event_key,
            "correction_request_delay": normalized_decimal(overlay.correction_request_delay),
        },
    )
    queue = EventQueue()
    for event in trace.events + (request,):
        queue.push(event)
    events = queue.drain()
    return replace(trace, events=events, event_hash=_event_hash(events))


def _reassessment_queue_run(
    cohort: StochasticCohort,
    traces: tuple[EngagementTrace, ...],
) -> ServiceQueueRun:
    cases = {case.case_id: case for case in cohort.cases}
    requests: list[ServiceRequest] = []
    for trace in traces:
        correction_events = tuple(
            event for event in trace.events if event.event_type_id == "CORRECTION_REQUESTED"
        )
        if len(correction_events) > 1:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"multiple correction requests for {trace.case_id}")
        if not correction_events:
            continue
        queued_at = correction_events[0].timestamp
        service_draw = cases[trace.case_id].draw_map[("reassessment_service", 0)]
        with localcontext() as context:
            context.prec = 50
            service_time = service_draw * cohort.overlay.reassessment_service_time
            deadline = queued_at + cohort.overlay.correction_window
        requests.append(ServiceRequest(
            request_id=f"{trace.case_id}:reassessment",
            case_id=trace.case_id,
            queued_at=queued_at,
            service_time=service_time,
            deadline=deadline,
        ))
    return schedule_service_queue(
        ServiceQueueConfig(
            queue_id=f"{cohort.scenario_id}:reassessment",
            capacity=int(cohort.overlay.reassessment_capacity),
        ),
        tuple(requests),
    )


def _add_reassessment_events(
    trace: EngagementTrace,
    visit: ServiceVisit | None,
    case: StochasticCase,
    queue_id: str,
) -> EngagementTrace:
    if visit is None:
        return trace
    requests = tuple(
        event for event in trace.events if event.event_type_id == "CORRECTION_REQUESTED"
    )
    if len(requests) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"reassessment visit requires one correction request for {trace.case_id}",
        )
    request = requests[0]
    service_draw_id = next(
        draw.keyed_draw_id for draw in case.keyed_draws
        if draw.key.event_family_id == "reassessment_service" and draw.key.draw_index == 0
    )
    root_key = f"{trace.case_id}:ENGAGEMENT"

    def reassessment_event(
        event_type_id: str,
        timestamp: Decimal,
        cause_id: str,
        details: dict[str, object],
    ) -> Event:
        causal_key = f"{root_key}:{cause_id}:{event_type_id}"
        return Event(
            event_id=f"{trace.policy_id}:{causal_key}",
            event_type_id=event_type_id,
            timestamp=timestamp,
            causal_event_key=causal_key,
            root_event_key=root_key,
            descendant_path=("correction", cause_id, event_type_id),
            transition_rank=DEFAULT_PRIORITIES[event_type_id],
            case_id=trace.case_id,
            details={"policy_id": trace.policy_id, "keyed_draw_ids": (), "queue_id": queue_id} | details,
        )

    common = {
        "review_kind": "reassessment",
        "action_type_id": "reassess",
        "service_request_id": visit.request_id,
        "server_id": visit.server_id,
        "service_deadline": normalized_decimal(visit.deadline),
        "service_time": normalized_decimal(visit.service_time),
        "wait_time": normalized_decimal(visit.wait_time),
        "source_correction_request_event_key": request.causal_event_key,
    }
    added = (
        reassessment_event(
            "REVIEW_COMPLETED",
            visit.completed_at,
            "reassessment_service",
            common | {
                "completed_by_deadline": visit.completed_by_deadline,
                "keyed_draw_ids": (service_draw_id,),
                "correction_executed": False,
                "restoration_executed": False,
            },
        ),
        reassessment_event(
            "DEADLINE_REACHED",
            visit.deadline,
            "reassessment_deadline",
            {
                "deadline_kind": "correction_service",
                "reassessment_completed_by_deadline": visit.completed_by_deadline,
                "service_request_id": visit.request_id,
                "source_correction_request_event_key": request.causal_event_key,
            },
        ),
    )
    queue = EventQueue()
    for event in trace.events + added:
        queue.push(event)
    events = queue.drain()
    return replace(trace, events=events, event_hash=_event_hash(events))


def _add_correction_outcome_event(
    trace: EngagementTrace,
    visit: ServiceVisit | None,
) -> EngagementTrace:
    """Correct the decision coordinate without implying recovery reversal or restoration."""

    if visit is None:
        return trace
    decision = trace.action_decision
    if decision is None or decision.action != "progress" or decision.progression_supported:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"correction outcome lacks an unsupported progression basis for {trace.case_id}",
        )
    requests = tuple(
        event for event in trace.events if event.event_type_id == "CORRECTION_REQUESTED"
    )
    completions = tuple(
        event for event in trace.events
        if event.event_type_id == "REVIEW_COMPLETED"
        and event.details.get("review_kind") == "reassessment"
    )
    exposures = tuple(
        event for event in trace.events if event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
    )
    if len(requests) != 1 or len(completions) != 1 or len(exposures) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"correction outcome requires one exposure, request, and reassessment completion for {trace.case_id}",
        )
    request = requests[0]
    completion = completions[0]
    exposure = exposures[0]
    if completion.timestamp != visit.completed_at:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"reassessment completion differs from queue visit for {trace.case_id}",
        )
    with localcontext() as context:
        context.prec = 50
        exposure_duration = completion.timestamp - exposure.timestamp
    if exposure_duration < 0:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"correction precedes exposure for {trace.case_id}",
        )

    root_key = f"{trace.case_id}:ENGAGEMENT"
    causal_key = f"{root_key}:correction_outcome:EXTERNAL_CONSEQUENCE_UPDATED"
    outcome = Event(
        event_id=f"{trace.policy_id}:{causal_key}",
        event_type_id="EXTERNAL_CONSEQUENCE_UPDATED",
        timestamp=completion.timestamp,
        causal_event_key=causal_key,
        root_event_key=root_key,
        descendant_path=("correction", "reassessment_service", "correction_outcome"),
        transition_rank=DEFAULT_PRIORITIES["EXTERNAL_CONSEQUENCE_UPDATED"],
        case_id=trace.case_id,
        details={
            "policy_id": trace.policy_id,
            "keyed_draw_ids": (),
            "action_type_id": "correct",
            "consequence_dimension_id": "decision_state",
            "correction_outcome": "decision_corrected",
            "correction_basis": "unsupported_progression_confirmed",
            "unsupported_reason_codes": decision.unsupported_reason_codes,
            "decision_state": "corrected_to_baseline",
            "correction_timely": visit.completed_by_deadline,
            "exposure_state": "active",
            "recovery_state": "active",
            "restoration_state": "incomplete",
            "restoration_complete": False,
            "exposure_duration_to_correction": normalized_decimal(exposure_duration),
            "source_exposure_event_key": exposure.causal_event_key,
            "source_correction_request_event_key": request.causal_event_key,
            "source_reassessment_event_key": completion.causal_event_key,
        },
    )
    queue = EventQueue()
    for event in trace.events + (outcome,):
        queue.push(event)
    events = queue.drain()
    return replace(trace, events=events, event_hash=_event_hash(events))


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
    if not {"progression", "recovery", "correction", "reassessment"} <= compiled.process_profile.capabilities:
        raise ContractError(
            "SCENARIO_CONFIGURATION_INCOMPLETE",
            "process lacks progression, recovery, correction, or reassessment capability",
        )
    if not {"recovery", "correction", "reassessment"} <= set(compiled.process_profile.stage_ids):
        raise ContractError(
            "SCENARIO_CONFIGURATION_INCOMPLETE",
            "process topology lacks a recovery, correction, or reassessment stage",
        )
    if not {"progress", "recover", "correct", "reassess"} <= compiled.process_profile.action_type_ids:
        raise ContractError(
            "SCENARIO_CONFIGURATION_INCOMPLETE",
            "process lacks a typed progression, recovery, correction, or reassessment action",
        )
    return policy_id


def run_engagement_stage(cohort: StochasticCohort, compiled: CompiledConfigurationSpec) -> EngagementRun:
    policy_id = _validate_engagement_configuration(cohort, compiled)
    engagement_traces = tuple(_case_engagement_trace(case, policy_id, cohort.overlay) for case in cohort.cases)
    review_queue = _review_queue_run(cohort, engagement_traces)
    visit_by_case = {visit.case_id: visit for visit in review_queue.visits}
    case_by_id = {case.case_id: case for case in cohort.cases}
    review_traces = tuple(
        _add_review_events(
            trace,
            visit_by_case.get(trace.case_id),
            case_by_id[trace.case_id],
            review_queue.config.queue_id,
        )
        for trace in engagement_traces
    )
    action_traces = tuple(
        _add_action_events(trace, visit_by_case.get(trace.case_id))
        for trace in review_traces
    )
    exposure_traces = tuple(
        _add_exposure_and_recovery_events(trace, cohort.overlay)
        for trace in action_traces
    )
    correction_traces = tuple(
        _add_correction_request_event(trace, case_by_id[trace.case_id], cohort.overlay)
        for trace in exposure_traces
    )
    reassessment_queue = _reassessment_queue_run(cohort, correction_traces)
    reassessment_visit_by_case = {
        visit.case_id: visit for visit in reassessment_queue.visits
    }
    reassessment_traces = tuple(
        _add_reassessment_events(
            trace,
            reassessment_visit_by_case.get(trace.case_id),
            case_by_id[trace.case_id],
            reassessment_queue.config.queue_id,
        )
        for trace in correction_traces
    )
    traces = tuple(
        _add_correction_outcome_event(
            trace,
            reassessment_visit_by_case.get(trace.case_id),
        )
        for trace in reassessment_traces
    )
    system_queue = EventQueue()
    for trace in traces:
        for event in trace.events:
            system_queue.push(event)
    system_events = system_queue.drain()
    event_hash = _event_hash(system_events)
    correction_outcome_events = tuple(
        event for event in system_events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
        and event.details.get("correction_outcome") == "decision_corrected"
    )
    correction_exposure_times = tuple(
        Decimal(str(event.details["exposure_duration_to_correction"]))
        for event in correction_outcome_events
    )
    with localcontext() as context:
        context.prec = 50
        correction_total_exposure_time = sum(correction_exposure_times, Decimal(0))
    correction_max_exposure_time = max(correction_exposure_times, default=Decimal(0))
    telemetry = EngagementRunTelemetry(
        case_count=len(traces),
        event_count=len(system_events),
        response_count=sum(trace.decision.responded for trace in traces),
        adequate_response_evidence_count=sum(trace.decision.adequate_response_evidence for trace in traces),
        assistance_count=sum(trace.decision.assistance_used for trace in traces),
        extension_count=sum(trace.decision.extension_granted for trace in traces),
        retrieval_request_count=sum(trace.decision.proactive_retrieval_requested for trace in traces),
        retrieved_evidence_count=sum(trace.decision.retrieved_evidence for trace in traces),
        review_queue_count=sum(
            event.event_type_id == "REVIEW_QUEUED" for event in system_events
        ),
        review_started_count=sum(
            event.event_type_id == "REVIEW_STARTED"
            and event.details.get("review_kind") == "pre_action"
            for event in system_events
        ),
        review_completed_count=sum(
            event.event_type_id == "REVIEW_COMPLETED"
            and event.details.get("review_kind") == "pre_action"
            for event in system_events
        ),
        timely_review_count=review_queue.telemetry.timely_completion_count,
        late_review_count=review_queue.telemetry.late_completion_count,
        review_total_wait_time=review_queue.telemetry.total_wait_time,
        review_max_wait_time=review_queue.telemetry.max_wait_time,
        review_schedule_hash=review_queue.telemetry.schedule_hash,
        action_count=sum(trace.action_decision is not None for trace in traces),
        progression_count=sum(
            trace.action_decision is not None and trace.action_decision.action == "progress"
            for trace in traces
        ),
        hold_count=sum(
            trace.action_decision is not None and trace.action_decision.action == "hold"
            for trace in traces
        ),
        request_evidence_action_count=sum(
            trace.action_decision is not None and trace.action_decision.action == "request_evidence"
            for trace in traces
        ),
        supported_progression_count=sum(
            trace.action_decision is not None and trace.action_decision.progression_supported
            for trace in traces
        ),
        unsupported_progression_count=sum(
            trace.action_decision is not None
            and trace.action_decision.action == "progress"
            and not trace.action_decision.progression_supported
            for trace in traces
        ),
        evidentially_supported_progression_count=sum(
            trace.action_decision is not None
            and trace.action_decision.evidentially_supported_progression
            for trace in traces
        ),
        evidentially_unsupported_progression_count=sum(
            trace.action_decision is not None
            and trace.action_decision.action == "progress"
            and not trace.action_decision.evidence_sufficient
            for trace in traces
        ),
        unauthorized_progression_count=sum(
            trace.action_decision is not None and trace.action_decision.unauthorized_progression
            for trace in traces
        ),
        gate_applicable_count=sum(
            trace.action_decision is not None and trace.action_decision.gate_safe is not None
            for trace in traces
        ),
        gate_safe_count=sum(
            trace.action_decision is not None and trace.action_decision.gate_safe is True
            for trace in traces
        ),
        gate_unsafe_count=sum(
            trace.action_decision is not None and trace.action_decision.gate_safe is False
            for trace in traces
        ),
        review_authorization_count=sum(
            trace.action_decision is not None and trace.action_decision.review_authorization_recorded
            for trace in traces
        ),
        fail_open_timeout_progression_count=sum(
            trace.action_decision is not None
            and trace.action_decision.reason_code == "review_timeout_fail_open"
            for trace in traces
        ),
        fail_closed_timeout_hold_count=sum(
            trace.action_decision is not None
            and trace.action_decision.reason_code == "review_timeout_fail_closed"
            for trace in traces
        ),
        external_exposure_count=sum(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
            for event in system_events
        ),
        recovery_started_count=sum(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
            and event.details.get("action_type_id") == "recover"
            and event.details.get("recovery_state") == "active"
            for event in system_events
        ),
        supported_exposure_count=sum(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
            and event.details.get("progression_supported") is True
            for event in system_events
        ),
        unsupported_exposure_count=sum(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
            and event.details.get("progression_supported") is False
            for event in system_events
        ),
        evidentially_unsupported_exposure_count=sum(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
            and event.details.get("evidence_sufficient") is False
            for event in system_events
        ),
        unauthorized_exposure_count=sum(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
            and event.details.get("unauthorized_progression") is True
            for event in system_events
        ),
        correction_eligible_count=sum(
            trace.action_decision is not None
            and trace.action_decision.action == "progress"
            and not trace.action_decision.progression_supported
            for trace in traces
        ),
        correction_request_count=sum(
            event.event_type_id == "CORRECTION_REQUESTED"
            for event in system_events
        ),
        correction_not_requested_count=sum(
            trace.action_decision is not None
            and trace.action_decision.action == "progress"
            and not trace.action_decision.progression_supported
            and not any(event.event_type_id == "CORRECTION_REQUESTED" for event in trace.events)
            for trace in traces
        ),
        reassessment_started_count=len(reassessment_queue.visits),
        reassessment_completed_count=sum(
            event.event_type_id == "REVIEW_COMPLETED"
            and event.details.get("review_kind") == "reassessment"
            for event in system_events
        ),
        timely_reassessment_count=reassessment_queue.telemetry.timely_completion_count,
        late_reassessment_count=reassessment_queue.telemetry.late_completion_count,
        reassessment_total_wait_time=reassessment_queue.telemetry.total_wait_time,
        reassessment_max_wait_time=reassessment_queue.telemetry.max_wait_time,
        reassessment_schedule_hash=reassessment_queue.telemetry.schedule_hash,
        correction_executed_count=len(correction_outcome_events),
        timely_correction_count=sum(
            event.details.get("correction_timely") is True
            for event in correction_outcome_events
        ),
        late_correction_count=sum(
            event.details.get("correction_timely") is False
            for event in correction_outcome_events
        ),
        correction_unresolved_count=sum(
            trace.action_decision is not None
            and trace.action_decision.action == "progress"
            and not trace.action_decision.progression_supported
            and not any(
                event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
                and event.details.get("correction_outcome") == "decision_corrected"
                for event in trace.events
            )
            for trace in traces
        ),
        recovery_active_after_correction_count=sum(
            event.details.get("recovery_state") == "active"
            and event.details.get("restoration_complete") is False
            for event in correction_outcome_events
        ),
        correction_total_exposure_time=correction_total_exposure_time,
        correction_max_exposure_time=correction_max_exposure_time,
        event_hash=event_hash,
    )
    if telemetry.action_count != telemetry.case_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "each case requires exactly one action decision")
    if telemetry.progression_count + telemetry.hold_count + telemetry.request_evidence_action_count != telemetry.action_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "action dispositions do not partition the cohort")
    if telemetry.supported_progression_count + telemetry.unsupported_progression_count != telemetry.progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "progression support does not partition progression")
    if telemetry.evidentially_supported_progression_count + telemetry.evidentially_unsupported_progression_count != telemetry.progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "evidentiary support does not partition progression")
    if telemetry.gate_safe_count + telemetry.gate_unsafe_count != telemetry.gate_applicable_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "gate safety does not partition applicable cases")
    if telemetry.external_exposure_count != telemetry.progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "executed progression and exposure counts differ")
    if telemetry.recovery_started_count != telemetry.external_exposure_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "exposure and recovery-start counts differ")
    if telemetry.supported_exposure_count + telemetry.unsupported_exposure_count != telemetry.external_exposure_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "support does not partition exposure")
    if telemetry.evidentially_unsupported_exposure_count != telemetry.evidentially_unsupported_progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "evidentiary status changed between progression and exposure")
    if telemetry.unauthorized_exposure_count != telemetry.unauthorized_progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "authorization status changed between progression and exposure")
    if telemetry.correction_eligible_count != telemetry.unsupported_exposure_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction eligibility differs from unsupported exposure")
    if telemetry.correction_request_count + telemetry.correction_not_requested_count != telemetry.correction_eligible_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction uptake does not partition eligible exposure")
    if telemetry.reassessment_started_count != telemetry.correction_request_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction requests and reassessment starts differ")
    if telemetry.reassessment_completed_count != telemetry.reassessment_started_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reassessment visits and completion events differ")
    if telemetry.timely_reassessment_count + telemetry.late_reassessment_count != telemetry.reassessment_completed_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reassessment timeliness does not partition completions")
    if telemetry.correction_executed_count != telemetry.reassessment_completed_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reassessment completion and correction execution differ")
    if telemetry.timely_correction_count + telemetry.late_correction_count != telemetry.correction_executed_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction timeliness does not partition outcomes")
    if (
        telemetry.timely_correction_count != telemetry.timely_reassessment_count
        or telemetry.late_correction_count != telemetry.late_reassessment_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction timing differs from reassessment completion")
    if (
        telemetry.correction_executed_count + telemetry.correction_unresolved_count
        != telemetry.correction_eligible_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction outcomes do not partition eligible exposure")
    if telemetry.recovery_active_after_correction_count != telemetry.correction_executed_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "decision correction silently changed recovery or restoration state")
    if any(event.event_type_id == "RESTORATION_EXECUTED" for event in system_events):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction checkpoint emitted premature restoration")
    return EngagementRun(
        cohort.scenario_id, policy_id, cohort.telemetry.cohort_hash,
        traces, system_events, review_queue, reassessment_queue, telemetry,
    )
