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
        }
        for field_name, value in nonnegative.items():
            if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
                raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must be finite and nonnegative")
        if self.response_deadline == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "response_deadline must be positive")
        if self.review_service_window == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "review_service_window must be positive")
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
    event_hash: str


@dataclass(frozen=True)
class EngagementRun:
    scenario_id: str
    policy_id: str
    cohort_hash: str
    traces: tuple[EngagementTrace, ...]
    system_events: tuple[Event, ...]
    review_queue: ServiceQueueRun
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
    engagement_traces = tuple(_case_engagement_trace(case, policy_id, cohort.overlay) for case in cohort.cases)
    review_queue = _review_queue_run(cohort, engagement_traces)
    visit_by_case = {visit.case_id: visit for visit in review_queue.visits}
    case_by_id = {case.case_id: case for case in cohort.cases}
    traces = tuple(
        _add_review_events(
            trace,
            visit_by_case.get(trace.case_id),
            case_by_id[trace.case_id],
            review_queue.config.queue_id,
        )
        for trace in engagement_traces
    )
    system_queue = EventQueue()
    for trace in traces:
        for event in trace.events:
            system_queue.push(event)
    system_events = system_queue.drain()
    event_hash = _event_hash(system_events)
    telemetry = EngagementRunTelemetry(
        case_count=len(traces),
        event_count=len(system_events),
        response_count=sum(trace.decision.responded for trace in traces),
        adequate_response_evidence_count=sum(trace.decision.adequate_response_evidence for trace in traces),
        assistance_count=sum(trace.decision.assistance_used for trace in traces),
        extension_count=sum(trace.decision.extension_granted for trace in traces),
        retrieval_request_count=sum(trace.decision.proactive_retrieval_requested for trace in traces),
        retrieved_evidence_count=sum(trace.decision.retrieved_evidence for trace in traces),
        review_queue_count=sum(event.event_type_id == "REVIEW_QUEUED" for event in system_events),
        review_started_count=sum(event.event_type_id == "REVIEW_STARTED" for event in system_events),
        review_completed_count=sum(event.event_type_id == "REVIEW_COMPLETED" for event in system_events),
        timely_review_count=review_queue.telemetry.timely_completion_count,
        late_review_count=review_queue.telemetry.late_completion_count,
        review_total_wait_time=review_queue.telemetry.total_wait_time,
        review_max_wait_time=review_queue.telemetry.max_wait_time,
        review_schedule_hash=review_queue.telemetry.schedule_hash,
        event_hash=event_hash,
    )
    return EngagementRun(
        cohort.scenario_id, policy_id, cohort.telemetry.cohort_hash,
        traces, system_events, review_queue, telemetry,
    )
