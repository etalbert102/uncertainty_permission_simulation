"""Finite-cohort stochastic substrate built from policy-neutral keyed latents."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from typing import Literal

from .configuration import (
    CompiledConfigurationSpec,
    EvaluationSpecificationSpec,
    ParameterValue,
    SUPPORTED_EVIDENCE_STATE_ID,
    ScenarioOverlaySpec,
    UNRESOLVED_EVIDENCE_STATE_ID,
    evaluate_robust_action_support,
    progression_action_instance,
)
from .events import DEFAULT_PRIORITIES, Event, EventQueue
from .policies import ActionDecision, EngagementDecision, EngagementInputs, decide_action, map_engagement, policy_behavior
from .random_streams import DRAW_FAMILY_IDS, KeyedDraw, KeyedRandomStream, normalized_decimal
from .schemas import ContractError


RESTORATION_DIMENSION_IDS = (
    "decision_state",
    "recovery_state",
    "residual_external_consequence",
)
RESTORATION_BASELINE_STATES = {
    dimension_id: "baseline" for dimension_id in RESTORATION_DIMENSION_IDS
}


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
    assistance_capacity: Decimal
    assistance_service_time: Decimal
    assistance_service_window: Decimal
    extension_effort_bonus: Decimal
    extension_need_probability: Decimal
    evidence_retrieval_success_probability: Decimal
    evidence_retrieval_latency_scale: Decimal
    external_consequence_delay: Decimal
    recovery_start_delay: Decimal
    recovery_capacity: Decimal
    recovery_service_time: Decimal
    recovery_window: Decimal
    correction_request_delay: Decimal
    correction_uptake_probability: Decimal
    reassessment_capacity: Decimal
    reassessment_service_time: Decimal
    correction_window: Decimal
    restoration_delay: Decimal
    restoration_window: Decimal
    administrative_cutoff: Decimal

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
            "assistance_service_time": self.assistance_service_time,
            "assistance_service_window": self.assistance_service_window,
            "extension_duration": self.extension_duration,
            "evidence_retrieval_latency_scale": self.evidence_retrieval_latency_scale,
            "external_consequence_delay": self.external_consequence_delay,
            "recovery_start_delay": self.recovery_start_delay,
            "recovery_service_time": self.recovery_service_time,
            "recovery_window": self.recovery_window,
            "correction_request_delay": self.correction_request_delay,
            "reassessment_service_time": self.reassessment_service_time,
            "correction_window": self.correction_window,
            "restoration_delay": self.restoration_delay,
            "restoration_window": self.restoration_window,
            "administrative_cutoff": self.administrative_cutoff,
        }
        for field_name, value in nonnegative.items():
            if not isinstance(value, Decimal) or not value.is_finite() or value < 0:
                raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must be finite and nonnegative")
        if self.administrative_cutoff < self.initiation_window:
            raise ContractError(
                "SCENARIO_PARAMETER_INVALID",
                "administrative_cutoff must not precede the initiation window",
            )
        if self.response_deadline == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "response_deadline must be positive")
        if self.review_service_window == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "review_service_window must be positive")
        if self.assistance_service_window == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "assistance_service_window must be positive")
        if self.recovery_service_time == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "recovery_service_time must be positive")
        if self.recovery_window == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "recovery_window must be positive")
        if self.reassessment_service_time == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "reassessment_service_time must be positive")
        if self.correction_window == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "correction_window must be positive")
        if self.restoration_window == 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "restoration_window must be positive")
        capacities = {
            "assistance_capacity": self.assistance_capacity,
            "review_capacity": self.review_capacity,
            "recovery_capacity": self.recovery_capacity,
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
            "assistance_capacity": normalized_decimal(self.assistance_capacity),
            "assistance_service_time": normalized_decimal(self.assistance_service_time),
            "assistance_service_window": normalized_decimal(self.assistance_service_window),
            "extension_effort_bonus": normalized_decimal(self.extension_effort_bonus),
            "extension_need_probability": normalized_decimal(self.extension_need_probability),
            "evidence_retrieval_success_probability": normalized_decimal(self.evidence_retrieval_success_probability),
            "evidence_retrieval_latency_scale": normalized_decimal(self.evidence_retrieval_latency_scale),
            "external_consequence_delay": normalized_decimal(self.external_consequence_delay),
            "recovery_start_delay": normalized_decimal(self.recovery_start_delay),
            "recovery_capacity": normalized_decimal(self.recovery_capacity),
            "recovery_service_time": normalized_decimal(self.recovery_service_time),
            "recovery_window": normalized_decimal(self.recovery_window),
            "correction_request_delay": normalized_decimal(self.correction_request_delay),
            "correction_uptake_probability": normalized_decimal(self.correction_uptake_probability),
            "reassessment_capacity": normalized_decimal(self.reassessment_capacity),
            "reassessment_service_time": normalized_decimal(self.reassessment_service_time),
            "correction_window": normalized_decimal(self.correction_window),
            "restoration_delay": normalized_decimal(self.restoration_delay),
            "restoration_window": normalized_decimal(self.restoration_window),
            "administrative_cutoff": normalized_decimal(self.administrative_cutoff),
        }

    def to_compilation_overlay(
        self,
        *,
        exclude_slot_ids: frozenset[str] = frozenset(),
    ) -> ScenarioOverlaySpec:
        values = self.canonical_value()
        unknown = exclude_slot_ids - (set(values) - {"overlay_id", "provenance"})
        if unknown:
            raise ContractError(
                "SCENARIO_PARAMETER_INVALID",
                f"cannot exclude unknown overlay slots: {sorted(unknown)}",
            )
        parameters = tuple(
            ParameterValue(
                slot_id=slot_id, value=value, provenance=self.provenance, owner_id=self.overlay_id,
            )
            for slot_id, value in values.items()
            if slot_id not in {"overlay_id", "provenance"} | exclude_slot_ids
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
    started_by_cutoff: bool
    completed_by_cutoff: bool
    right_censored: bool
    censoring_reason: str | None


@dataclass(frozen=True)
class ServiceQueueTelemetry:
    request_count: int
    immediate_start_count: int
    timely_completion_count: int
    late_completion_count: int
    started_by_cutoff_count: int
    completed_by_cutoff_count: int
    right_censored_count: int
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
                "started_by_cutoff": visit.started_by_cutoff,
                "completed_by_cutoff": visit.completed_by_cutoff,
                "right_censored": visit.right_censored,
                "censoring_reason": visit.censoring_reason,
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
    administrative_cutoff: Decimal | None = None,
) -> ServiceQueueRun:
    """Schedule a finite, work-conserving FIFO queue with deterministic server ties."""

    if not isinstance(config, ServiceQueueConfig):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "service queue requires a typed configuration")
    if not isinstance(requests, tuple):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "service requests must be a tuple")
    if any(not isinstance(request, ServiceRequest) for request in requests):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "service queue requires typed requests")
    if administrative_cutoff is not None and (
        not isinstance(administrative_cutoff, Decimal)
        or not administrative_cutoff.is_finite()
        or administrative_cutoff < 0
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "administrative cutoff must be finite and nonnegative")
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
        started_by_cutoff = administrative_cutoff is None or started_at <= administrative_cutoff
        completed_by_cutoff = administrative_cutoff is None or completed_at <= administrative_cutoff
        censoring_reason = None
        if not completed_by_cutoff:
            censoring_reason = (
                "service_in_progress_at_cutoff"
                if started_by_cutoff else "service_not_started_by_cutoff"
            )
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
            started_by_cutoff=started_by_cutoff,
            completed_by_cutoff=completed_by_cutoff,
            right_censored=not completed_by_cutoff,
            censoring_reason=censoring_reason,
        ))
    frozen_visits = tuple(visits)
    with localcontext() as context:
        context.prec = 50
        total_wait = sum((visit.wait_time for visit in frozen_visits if visit.started_by_cutoff), Decimal(0))
        total_service = sum((visit.service_time for visit in frozen_visits if visit.completed_by_cutoff), Decimal(0))
    max_wait = max((visit.wait_time for visit in frozen_visits if visit.started_by_cutoff), default=Decimal(0))
    schedule_hash = _service_schedule_hash(config, frozen_visits)
    timely_count = sum(
        visit.completed_by_cutoff and visit.completed_by_deadline for visit in frozen_visits
    )
    late_count = sum(
        visit.completed_by_cutoff and not visit.completed_by_deadline for visit in frozen_visits
    )
    telemetry = ServiceQueueTelemetry(
        request_count=len(frozen_visits),
        immediate_start_count=sum(visit.started_by_cutoff and visit.wait_time == 0 for visit in frozen_visits),
        timely_completion_count=timely_count,
        late_completion_count=late_count,
        started_by_cutoff_count=sum(visit.started_by_cutoff for visit in frozen_visits),
        completed_by_cutoff_count=sum(visit.completed_by_cutoff for visit in frozen_visits),
        right_censored_count=sum(visit.right_censored for visit in frozen_visits),
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
    assistance_request_count: int
    assistance_started_count: int
    assistance_completed_count: int
    timely_assistance_count: int
    late_assistance_count: int
    assistance_right_censored_count: int
    assistance_total_wait_time: Decimal
    assistance_max_wait_time: Decimal
    assistance_schedule_hash: str
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
    recovery_queue_count: int
    recovery_service_started_count: int
    recovery_started_count: int
    timely_recovery_count: int
    late_recovery_count: int
    recovery_right_censored_count: int
    recovery_not_queued_by_cutoff_count: int
    recovery_total_wait_time: Decimal
    recovery_max_wait_time: Decimal
    recovery_schedule_hash: str
    supported_exposure_count: int
    unsupported_exposure_count: int
    evidentially_unsupported_exposure_count: int
    unauthorized_exposure_count: int
    correction_eligible_count: int
    correction_request_count: int
    correction_not_requested_count: int
    correction_not_available_by_cutoff_count: int
    reassessment_started_count: int
    reassessment_completed_count: int
    timely_reassessment_count: int
    late_reassessment_count: int
    reassessment_right_censored_count: int
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
    restoration_due_count: int
    restoration_executed_count: int
    timely_restoration_count: int
    late_restoration_count: int
    complete_restoration_count: int
    partial_restoration_count: int
    restoration_horizon_pending_count: int
    restoration_horizon_expired_count: int
    unresolved_external_consequence_count: int
    restoration_total_time_from_correction: Decimal
    restoration_max_time_from_correction: Decimal
    case_closed_count: int
    resolved_case_count: int
    right_censored_case_count: int
    event_hash: str


@dataclass(frozen=True)
class EngagementRun:
    scenario_id: str
    policy_id: str
    cohort_hash: str
    traces: tuple[EngagementTrace, ...]
    system_events: tuple[Event, ...]
    assistance_queue: ServiceQueueRun
    review_queue: ServiceQueueRun
    recovery_queue: ServiceQueueRun
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


def _engagement_inputs(case: StochasticCase, overlay: StochasticInputOverlay) -> EngagementInputs:
    draws = case.draw_map
    return EngagementInputs(
        notice_delivered=draws[("notice_delivery", 0)] < overlay.notice_delivery_probability,
        administrative_access=draws[("administrative_access", 0)] < overlay.administrative_access_probability,
        comprehension=draws[("comprehension", 0)] < overlay.comprehension_probability,
        records_available=draws[("record_availability", 0)] < overlay.record_availability_probability,
        response_effort=draws[("response_effort", 0)],
        extension_needed=draws[("extension_need", 0)] < overlay.extension_need_probability,
        retrieval_success=draws[("evidence_retrieval_success", 0)] < overlay.evidence_retrieval_success_probability,
    )


def _assistance_queue_run(
    cohort: StochasticCohort,
    policy_id: str,
) -> ServiceQueueRun:
    behavior = policy_behavior(policy_id)
    requests: list[ServiceRequest] = []
    if behavior.offers_assistance:
        for case in cohort.cases:
            inputs = _engagement_inputs(case, cohort.overlay)
            assistance_needed = inputs.notice_delivered and (
                not inputs.administrative_access
                or not inputs.comprehension
                or inputs.response_effort > cohort.overlay.response_effort_limit
            )
            if not assistance_needed:
                continue
            with localcontext() as context:
                context.prec = 50
                queued_at = case.arrival_time + cohort.overlay.notice_delay
                service_time = (
                    case.draw_map[("assistance_service", 0)]
                    * cohort.overlay.assistance_service_time
                )
                deadline = queued_at + cohort.overlay.assistance_service_window
            if queued_at > cohort.overlay.administrative_cutoff:
                continue
            requests.append(ServiceRequest(
                request_id=f"{case.case_id}:assistance",
                case_id=case.case_id,
                queued_at=queued_at,
                service_time=service_time,
                deadline=deadline,
            ))
    return schedule_service_queue(
        ServiceQueueConfig(
            queue_id=f"{cohort.scenario_id}:assistance",
            capacity=int(cohort.overlay.assistance_capacity),
        ),
        tuple(requests),
        cohort.overlay.administrative_cutoff,
    )


def _case_engagement_trace(
    case: StochasticCase,
    policy_id: str,
    overlay: StochasticInputOverlay,
    assistance_visit: ServiceVisit | None,
    assistance_queue_id: str,
    evaluation_specification: EvaluationSpecificationSpec,
) -> EngagementTrace:
    behavior = policy_behavior(policy_id)
    draws = case.draw_map
    draw_ids = {
        draw.key.event_family_id: draw.keyed_draw_id
        for draw in case.keyed_draws
        if draw.key.draw_index == 0
    }
    inputs = _engagement_inputs(case, overlay)
    assistance_completed = bool(
        assistance_visit is not None
        and assistance_visit.completed_by_cutoff
        and assistance_visit.completed_by_deadline
    )
    decision = map_engagement(
        policy_id=policy_id,
        inputs=inputs,
        response_effort_limit=overlay.response_effort_limit,
        assistance_effort_bonus=overlay.assistance_effort_bonus,
        extension_effort_bonus=overlay.extension_effort_bonus,
        assistance_completed=assistance_completed,
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

    if assistance_visit is not None:
        assistance_common = {
            "service_kind": "engagement_assistance",
            "queue_id": assistance_queue_id,
            "service_request_id": assistance_visit.request_id,
            "server_id": assistance_visit.server_id,
            "service_deadline": normalized_decimal(assistance_visit.deadline),
            "service_time": normalized_decimal(assistance_visit.service_time),
            "wait_time": normalized_decimal(assistance_visit.wait_time),
        }
        emit(
            "ASSISTANCE_REQUESTED", assistance_visit.queued_at, "assistance_request",
            extra_details=assistance_common,
        )
        emit(
            "ASSISTANCE_STARTED", assistance_visit.started_at, "assistance_service",
            ("assistance_service",), assistance_common,
        )
        emit(
            "ASSISTANCE_COMPLETED", assistance_visit.completed_at, "assistance_completion",
            ("assistance_service",),
            assistance_common | {
                "completed_by_deadline": assistance_visit.completed_by_deadline,
                "engagement_effect_applied": assistance_completed,
            },
        )

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

    evidence_state_id = (
        SUPPORTED_EVIDENCE_STATE_ID
        if decision.adequate_response_evidence or decision.retrieved_evidence
        else UNRESOLVED_EVIDENCE_STATE_ID
    )
    support_receipt = evaluate_robust_action_support(
        evaluation_specification,
        action=progression_action_instance(evaluation_specification, case_id=case.case_id),
        evidence_state_id=evidence_state_id,
    )
    evidence_sufficient = support_receipt.robust_action_support
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
    emit(
        "REPRESENTATION_APPLIED",
        routing_time,
        "representation",
        extra_details={
            "evidence_state_id": evidence_state_id,
            **support_receipt.model_dump(mode="json"),
        },
    )
    emit("REPRESENTATION_SURFACED", routing_time, "representation")
    emit("ROUTING_COMPLETED", routing_time, "routing")
    review_required = behavior.review_scope == "all_progression" or (
        behavior.review_scope == "unresolved_only" and not evidence_sufficient
    )
    if review_required:
        emit(
            "REVIEW_QUEUED", routing_time, "review",
            extra_details={"review_kind": "pre_action"},
        )

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
        queued_events = tuple(
            event for event in trace.events
            if event.event_type_id == "REVIEW_QUEUED"
            and event.details.get("review_kind") == "pre_action"
        )
        if len(queued_events) > 1:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"multiple review queue entries for {trace.case_id}")
        if not queued_events:
            continue
        queued_at = queued_events[0].timestamp
        if queued_at > cohort.overlay.administrative_cutoff:
            continue
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
        cohort.overlay.administrative_cutoff,
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
    administrative_cutoff: Decimal,
    evaluation_specification: EvaluationSpecificationSpec,
) -> EngagementTrace:
    review_required = visit is not None
    review_completed_by_deadline = visit.completed_by_deadline if visit is not None else False
    routing_events = tuple(event for event in trace.events if event.event_type_id == "ROUTING_COMPLETED")
    if len(routing_events) != 1:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"expected one routing event for {trace.case_id}")
    evidence_state_id = (
        SUPPORTED_EVIDENCE_STATE_ID
        if trace.decision.adequate_response_evidence or trace.decision.retrieved_evidence
        else UNRESOLVED_EVIDENCE_STATE_ID
    )
    support_receipt = evaluate_robust_action_support(
        evaluation_specification,
        action=progression_action_instance(evaluation_specification, case_id=trace.case_id),
        evidence_state_id=evidence_state_id,
    )
    evidence_sufficient = support_receipt.robust_action_support
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
    if action_time > administrative_cutoff:
        return trace
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
        "evidence_state_id": evidence_state_id,
        **support_receipt.model_dump(mode="json"),
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


def _add_exposure_event(
    trace: EngagementTrace,
    overlay: StochasticInputOverlay,
) -> EngagementTrace:
    """Extend executed progression only; permission and computation never imply exposure."""

    progression_events = tuple(
        event for event in trace.events if event.event_type_id == "PROGRESSION_EXECUTED"
    )
    if trace.action_decision is None:
        if progression_events:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", f"unobserved action has progression event for {trace.case_id}")
        return trace
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
    if exposure_time > overlay.administrative_cutoff:
        return trace
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
    queue = EventQueue()
    for event in trace.events + (exposure_event,):
        queue.push(event)
    events = queue.drain()
    return replace(trace, events=events, event_hash=_event_hash(events))


def _recovery_queue_run(
    cohort: StochasticCohort,
    traces: tuple[EngagementTrace, ...],
) -> tuple[ServiceQueueRun, int]:
    """Queue fixed recovery work without adding a new exogenous draw family."""

    requests: list[ServiceRequest] = []
    not_queued_by_cutoff = 0
    for trace in traces:
        exposure_events = tuple(
            event for event in trace.events
            if event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
        )
        if len(exposure_events) > 1:
            raise ContractError(
                "SIM_SYSTEM_STATE_INCOMPLETE",
                f"multiple external exposures for {trace.case_id}",
            )
        if not exposure_events:
            continue
        exposure = exposure_events[0]
        with localcontext() as context:
            context.prec = 50
            queued_at = exposure.timestamp + cohort.overlay.recovery_start_delay
            deadline = queued_at + cohort.overlay.recovery_window
        if queued_at > cohort.overlay.administrative_cutoff:
            not_queued_by_cutoff += 1
            continue
        requests.append(ServiceRequest(
            request_id=f"{trace.case_id}:recovery",
            case_id=trace.case_id,
            queued_at=queued_at,
            service_time=cohort.overlay.recovery_service_time,
            deadline=deadline,
        ))
    run = schedule_service_queue(
        ServiceQueueConfig(
            queue_id=f"{cohort.scenario_id}:recovery",
            capacity=int(cohort.overlay.recovery_capacity),
        ),
        tuple(requests),
        cohort.overlay.administrative_cutoff,
    )
    return run, not_queued_by_cutoff


def _add_recovery_event(
    trace: EngagementTrace,
    visit: ServiceVisit | None,
    queue_id: str,
) -> EngagementTrace:
    if visit is None or not visit.completed_by_cutoff:
        return trace
    exposures = tuple(
        event for event in trace.events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
    )
    if len(exposures) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"recovery completion requires one external exposure for {trace.case_id}",
        )
    exposure = exposures[0]
    root_key = f"{trace.case_id}:ENGAGEMENT"
    causal_key = f"{root_key}:recovery:EXTERNAL_CONSEQUENCE_UPDATED"
    recovery = Event(
        event_id=f"{trace.policy_id}:{causal_key}",
        event_type_id="EXTERNAL_CONSEQUENCE_UPDATED",
        timestamp=visit.completed_at,
        causal_event_key=causal_key,
        root_event_key=root_key,
        descendant_path=("progression", "external_consequence", "recovery"),
        transition_rank=DEFAULT_PRIORITIES["EXTERNAL_CONSEQUENCE_UPDATED"],
        case_id=trace.case_id,
        details=exposure.details | {
            "policy_id": trace.policy_id,
            "keyed_draw_ids": (),
            "action_type_id": "recover",
            "consequence_dimension_id": "recovery_exposure",
            "exposure_state": "active",
            "recovery_state": "active",
            "source_external_consequence_event_key": exposure.causal_event_key,
            "recovery_start_delay": normalized_decimal(
                visit.queued_at - exposure.timestamp
            ),
            "queue_id": queue_id,
            "service_request_id": visit.request_id,
            "server_id": visit.server_id,
            "service_deadline": normalized_decimal(visit.deadline),
            "service_time": normalized_decimal(visit.service_time),
            "wait_time": normalized_decimal(visit.wait_time),
            "completed_by_deadline": visit.completed_by_deadline,
        },
    )
    queue = EventQueue()
    for event in trace.events + (recovery,):
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
        return trace
    correction_eligible = decision.action == "progress" and not decision.progression_supported
    if not correction_eligible:
        return trace

    recovery_events = tuple(
        event for event in trace.events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
        and event.details.get("recovery_state") == "active"
    )
    if not recovery_events:
        return trace
    if len(recovery_events) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"correction-eligible case has multiple active recovery events for {trace.case_id}",
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
    if request_time > overlay.administrative_cutoff:
        return trace
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
        cohort.overlay.administrative_cutoff,
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
    added: list[Event] = []
    if visit.completed_by_cutoff:
        added.append(reassessment_event(
            "REVIEW_COMPLETED",
            visit.completed_at,
            "reassessment_service",
            common | {
                "completed_by_deadline": visit.completed_by_deadline,
                "keyed_draw_ids": (service_draw_id,),
                "correction_executed": False,
                "restoration_executed": False,
            },
        ))
    added.append(reassessment_event(
            "DEADLINE_REACHED",
            visit.deadline,
            "reassessment_deadline",
            {
                "deadline_kind": "correction_service",
                "reassessment_completed_by_deadline": visit.completed_by_deadline,
                "service_request_id": visit.request_id,
                "source_correction_request_event_key": request.causal_event_key,
            },
        ))
    queue = EventQueue()
    for event in trace.events + tuple(added):
        queue.push(event)
    events = queue.drain()
    return replace(trace, events=events, event_hash=_event_hash(events))


def _add_correction_outcome_event(
    trace: EngagementTrace,
    visit: ServiceVisit | None,
) -> EngagementTrace:
    """Correct the decision coordinate without implying recovery reversal or restoration."""

    if visit is None or not visit.completed_by_cutoff:
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


def _restoration_deadline(
    trace: EngagementTrace,
    overlay: StochasticInputOverlay,
) -> Decimal:
    exposures = tuple(
        event for event in trace.events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
    )
    if len(exposures) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"restoration obligation requires one external exposure for {trace.case_id}",
        )
    with localcontext() as context:
        context.prec = 50
        return exposures[0].timestamp + overlay.restoration_window


def _add_restoration_event(
    trace: EngagementTrace,
    overlay: StochasticInputOverlay,
) -> EngagementTrace:
    """Repair modeled consequence dimensions without equating action with completeness."""

    corrections = tuple(
        event for event in trace.events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
        and event.details.get("correction_outcome") == "decision_corrected"
    )
    if not corrections:
        return trace
    if len(corrections) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"restoration requires one decision correction for {trace.case_id}",
        )
    correction = corrections[0]
    if not policy_behavior(trace.policy_id).restores_after_correction:
        return trace
    exposures = tuple(
        event for event in trace.events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
    )
    recoveries = tuple(
        event for event in trace.events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
        and event.details.get("action_type_id") == "recover"
    )
    if len(exposures) != 1 or len(recoveries) != 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"restoration requires one exposure and active recovery state for {trace.case_id}",
        )
    exposure = exposures[0]
    recovery = recoveries[0]
    with localcontext() as context:
        context.prec = 50
        restoration_time = correction.timestamp + overlay.restoration_delay
        deadline = _restoration_deadline(trace, overlay)
        time_from_correction = restoration_time - correction.timestamp
        time_from_exposure = restoration_time - exposure.timestamp
    if restoration_time > overlay.administrative_cutoff:
        return trace
    timely = restoration_time <= deadline
    restored_dimensions = (
        RESTORATION_DIMENSION_IDS
        if timely else ("decision_state", "recovery_state")
    )
    unrestored_dimensions = () if timely else ("residual_external_consequence",)
    dimension_states = {
        "decision_state": "baseline",
        "recovery_state": "baseline",
        "residual_external_consequence": "baseline" if timely else "irreversible_residual",
    }
    root_key = f"{trace.case_id}:ENGAGEMENT"
    causal_key = f"{root_key}:restoration:RESTORATION_EXECUTED"
    restoration = Event(
        event_id=f"{trace.policy_id}:{causal_key}",
        event_type_id="RESTORATION_EXECUTED",
        timestamp=restoration_time,
        causal_event_key=causal_key,
        root_event_key=root_key,
        descendant_path=("correction", "restoration"),
        transition_rank=DEFAULT_PRIORITIES["RESTORATION_EXECUTED"],
        case_id=trace.case_id,
        details={
            "policy_id": trace.policy_id,
            "keyed_draw_ids": (),
            "action_type_id": "restore",
            "modeled_consequence_dimension_ids": RESTORATION_DIMENSION_IDS,
            "baseline_dimension_states": dict(RESTORATION_BASELINE_STATES),
            "restored_dimension_ids": restored_dimensions,
            "unrestored_dimension_ids": unrestored_dimensions,
            "dimension_states": dimension_states,
            "decision_state": "corrected_to_baseline",
            "recovery_state": "baseline",
            "exposure_state": "resolved" if timely else "residual",
            "restoration_state": "complete" if timely else "partial",
            "restoration_complete": timely,
            "restoration_timely": timely,
            "irreversible_residual": not timely,
            "restoration_deadline": normalized_decimal(deadline),
            "restoration_delay": normalized_decimal(overlay.restoration_delay),
            "time_from_correction": normalized_decimal(time_from_correction),
            "time_from_exposure": normalized_decimal(time_from_exposure),
            "source_exposure_event_key": exposure.causal_event_key,
            "source_recovery_event_key": recovery.causal_event_key,
            "source_correction_event_key": correction.causal_event_key,
        },
    )
    queue = EventQueue()
    for event in trace.events + (restoration,):
        queue.push(event)
    events = queue.drain()
    return replace(trace, events=events, event_hash=_event_hash(events))


def _apply_administrative_cutoff(
    trace: EngagementTrace,
    overlay: StochasticInputOverlay,
) -> EngagementTrace:
    """Close observation at any stage without inventing unobserved transitions."""

    cutoff = overlay.administrative_cutoff
    observed = tuple(event for event in trace.events if event.timestamp <= cutoff)
    notice = any(event.event_type_id in {"NOTICE_DELIVERED", "NOTICE_FAILED"} for event in observed)
    routing = any(event.event_type_id == "ROUTING_COMPLETED" for event in observed)
    action = any(event.event_type_id == "ACTION_COMPUTED" for event in observed)
    exposure = any(
        event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED" for event in observed
    )
    recovery = any(
        event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
        and event.details.get("action_type_id") == "recover"
        for event in observed
    )
    request = any(event.event_type_id == "CORRECTION_REQUESTED" for event in observed)
    correction = any(
        event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
        and event.details.get("correction_outcome") == "decision_corrected"
        for event in observed
    )
    restoration_events = tuple(
        event for event in observed if event.event_type_id == "RESTORATION_EXECUTED"
    )
    if len(restoration_events) > 1:
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            f"multiple restoration actions for {trace.case_id}",
        )
    restoration = restoration_events[0] if restoration_events else None
    restoration_due = (
        exposure
        and trace.action_decision is not None
        and trace.action_decision.action == "progress"
        and not trace.action_decision.progression_supported
    )
    restoration_deadline = (
        _restoration_deadline(trace, overlay) if restoration_due else None
    )
    restoration_complete = bool(
        restoration and restoration.details.get("restoration_complete") is True
    )
    irreversible_residual = bool(
        restoration and restoration.details.get("irreversible_residual") is True
    )
    restoration_horizon_status = "not_applicable"
    if restoration_complete:
        restoration_horizon_status = "completed_timely"
    elif restoration is not None:
        restoration_horizon_status = "completed_late"
    elif restoration_due and restoration_deadline is not None:
        restoration_horizon_status = (
            "expired_without_completion"
            if cutoff >= restoration_deadline else "pending"
        )
    if restoration_complete:
        reason = "complete_restoration_observed"
        right_censored = False
    elif restoration is not None:
        reason = "partial_restoration_irreversible_residual"
        right_censored = False
    elif restoration_due and restoration_deadline is not None and cutoff >= restoration_deadline:
        reason = "restoration_horizon_expired_without_completion"
        right_censored = False
    elif correction:
        reason = "restoration_pending_at_cutoff"
        right_censored = True
    elif not notice:
        reason = "notice_stage_open_at_cutoff"
        right_censored = True
    elif not routing:
        reason = "engagement_stage_open_at_cutoff"
        right_censored = True
    elif not action:
        reason = "review_or_action_stage_open_at_cutoff"
        right_censored = True
    elif not exposure:
        reason = "post_action_path_open_at_cutoff"
        right_censored = True
    elif not recovery:
        reason = "recovery_service_open"
        right_censored = True
    elif request and not correction:
        reason = "reassessment_open"
        right_censored = True
    elif trace.action_decision is not None and not trace.action_decision.progression_supported:
        reason = "correction_path_unresolved_by_cutoff"
        right_censored = True
    else:
        reason = "recovery_exposure_open"
        right_censored = True
    root_key = f"{trace.case_id}:ENGAGEMENT"
    causal_key = f"{root_key}:administrative_cutoff:CASE_CLOSED"
    closed = Event(
        event_id=f"{trace.policy_id}:{causal_key}",
        event_type_id="CASE_CLOSED",
        timestamp=cutoff,
        causal_event_key=causal_key,
        root_event_key=root_key,
        descendant_path=("administrative_cutoff", "CASE_CLOSED"),
        transition_rank=DEFAULT_PRIORITIES["CASE_CLOSED"],
        case_id=trace.case_id,
        details={
            "policy_id": trace.policy_id,
            "keyed_draw_ids": (),
            "closure_kind": (
                "administrative_right_censor" if right_censored else "observed_outcome"
            ),
            "right_censored": right_censored,
            "censoring_reason": reason,
            "decision_corrected": correction,
            "recovery_state": (
                restoration.details.get("recovery_state")
                if restoration is not None else "active" if recovery else "not_started"
            ),
            "restoration_due": restoration_due,
            "restoration_deadline": (
                normalized_decimal(restoration_deadline)
                if restoration_deadline is not None else None
            ),
            "restoration_complete": restoration_complete,
            "restoration_horizon_status": restoration_horizon_status,
            "irreversible_residual": irreversible_residual,
        },
    )
    queue = EventQueue()
    for event in observed + (closed,):
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
    if any(
        receipt.provenance not in {cohort.overlay.provenance, "documented"}
        for receipt in compiled.receipts
    ):
        raise ContractError(
            "SCENARIO_CONFIGURATION_INCOMPLETE",
            "compiled parameter provenance is neither documented nor owned by the cohort overlay",
        )
    if not {"progression", "recovery", "correction", "reassessment", "restoration"} <= compiled.process_profile.capabilities:
        raise ContractError(
            "SCENARIO_CONFIGURATION_INCOMPLETE",
            "process lacks progression, recovery, correction, reassessment, or restoration capability",
        )
    if not {"recovery", "correction", "reassessment", "restoration"} <= set(compiled.process_profile.stage_ids):
        raise ContractError(
            "SCENARIO_CONFIGURATION_INCOMPLETE",
            "process topology lacks a recovery, correction, reassessment, or restoration stage",
        )
    if not {"progress", "recover", "correct", "reassess", "restore"} <= compiled.process_profile.action_type_ids:
        raise ContractError(
            "SCENARIO_CONFIGURATION_INCOMPLETE",
            "process lacks a typed progression, recovery, correction, reassessment, or restoration action",
        )
    return policy_id


def run_engagement_stage(cohort: StochasticCohort, compiled: CompiledConfigurationSpec) -> EngagementRun:
    policy_id = _validate_engagement_configuration(cohort, compiled)
    assistance_queue = _assistance_queue_run(cohort, policy_id)
    assistance_visit_by_case = {
        visit.case_id: visit for visit in assistance_queue.visits
    }
    engagement_traces = tuple(
        _case_engagement_trace(
            case,
            policy_id,
            cohort.overlay,
            assistance_visit_by_case.get(case.case_id),
            assistance_queue.config.queue_id,
            compiled.evaluation_specification,
        )
        for case in cohort.cases
    )
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
        _add_action_events(
            trace,
            visit_by_case.get(trace.case_id),
            cohort.overlay.administrative_cutoff,
            compiled.evaluation_specification,
        )
        for trace in review_traces
    )
    exposure_traces = tuple(
        _add_exposure_event(trace, cohort.overlay)
        for trace in action_traces
    )
    recovery_queue, recovery_not_queued_by_cutoff = _recovery_queue_run(
        cohort, exposure_traces
    )
    recovery_visit_by_case = {
        visit.case_id: visit for visit in recovery_queue.visits
    }
    recovery_traces = tuple(
        _add_recovery_event(
            trace,
            recovery_visit_by_case.get(trace.case_id),
            recovery_queue.config.queue_id,
        )
        for trace in exposure_traces
    )
    correction_traces = tuple(
        _add_correction_request_event(trace, case_by_id[trace.case_id], cohort.overlay)
        for trace in recovery_traces
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
    outcome_traces = tuple(
        _add_correction_outcome_event(
            trace,
            reassessment_visit_by_case.get(trace.case_id),
        )
        for trace in reassessment_traces
    )
    restoration_traces = tuple(
        _add_restoration_event(trace, cohort.overlay)
        for trace in outcome_traces
    )
    traces = tuple(
        _apply_administrative_cutoff(trace, cohort.overlay)
        for trace in restoration_traces
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
    restoration_events = tuple(
        event for event in system_events
        if event.event_type_id == "RESTORATION_EXECUTED"
    )
    restoration_times = tuple(
        Decimal(str(event.details["time_from_correction"]))
        for event in restoration_events
    )
    with localcontext() as context:
        context.prec = 50
        restoration_total_time = sum(restoration_times, Decimal(0))
    restoration_max_time = max(restoration_times, default=Decimal(0))
    closure_events = tuple(
        event for event in system_events if event.event_type_id == "CASE_CLOSED"
    )

    def correction_availability(trace: EngagementTrace) -> str | None:
        decision = trace.action_decision
        if decision is None or decision.action != "progress" or decision.progression_supported:
            return None
        if not any(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
            for event in trace.events
        ):
            return None
        if any(event.event_type_id == "CORRECTION_REQUESTED" for event in trace.events):
            return "requested"
        recoveries = tuple(
            event for event in trace.events
            if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
            and event.details.get("action_type_id") == "recover"
        )
        if not recoveries:
            return "not_available_by_cutoff"
        with localcontext() as context:
            context.prec = 50
            available_at = recoveries[0].timestamp + cohort.overlay.correction_request_delay
        if available_at > cohort.overlay.administrative_cutoff:
            return "not_available_by_cutoff"
        return "not_requested"

    correction_availability_states = tuple(
        correction_availability(trace) for trace in traces
    )
    telemetry = EngagementRunTelemetry(
        case_count=len(traces),
        event_count=len(system_events),
        response_count=sum(
            event.event_type_id == "SUBJECT_RESPONDED" for event in system_events
        ),
        adequate_response_evidence_count=sum(
            event.event_type_id == "EVIDENCE_ACCEPTED"
            and "response" in event.descendant_path
            for event in system_events
        ),
        assistance_count=sum(
            event.event_type_id == "ASSISTANCE_COMPLETED"
            and event.details.get("engagement_effect_applied") is True
            for event in system_events
        ),
        assistance_request_count=assistance_queue.telemetry.request_count,
        assistance_started_count=assistance_queue.telemetry.started_by_cutoff_count,
        assistance_completed_count=assistance_queue.telemetry.completed_by_cutoff_count,
        timely_assistance_count=assistance_queue.telemetry.timely_completion_count,
        late_assistance_count=assistance_queue.telemetry.late_completion_count,
        assistance_right_censored_count=assistance_queue.telemetry.right_censored_count,
        assistance_total_wait_time=assistance_queue.telemetry.total_wait_time,
        assistance_max_wait_time=assistance_queue.telemetry.max_wait_time,
        assistance_schedule_hash=assistance_queue.telemetry.schedule_hash,
        extension_count=sum(
            event.event_type_id == "EXTENSION_GRANTED" for event in system_events
        ),
        retrieval_request_count=sum(
            event.event_type_id == "EVIDENCE_REQUESTED" for event in system_events
        ),
        retrieved_evidence_count=sum(
            event.event_type_id == "EVIDENCE_ACCEPTED"
            and "external_evidence" in event.descendant_path
            for event in system_events
        ),
        review_queue_count=sum(
            event.event_type_id == "REVIEW_QUEUED"
            and event.details.get("review_kind") == "pre_action"
            for event in system_events
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
        recovery_queue_count=recovery_queue.telemetry.request_count,
        recovery_service_started_count=recovery_queue.telemetry.started_by_cutoff_count,
        recovery_started_count=sum(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
            and event.details.get("action_type_id") == "recover"
            and event.details.get("recovery_state") == "active"
            for event in system_events
        ),
        timely_recovery_count=recovery_queue.telemetry.timely_completion_count,
        late_recovery_count=recovery_queue.telemetry.late_completion_count,
        recovery_right_censored_count=recovery_queue.telemetry.right_censored_count,
        recovery_not_queued_by_cutoff_count=recovery_not_queued_by_cutoff,
        recovery_total_wait_time=recovery_queue.telemetry.total_wait_time,
        recovery_max_wait_time=recovery_queue.telemetry.max_wait_time,
        recovery_schedule_hash=recovery_queue.telemetry.schedule_hash,
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
            event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
            and event.details.get("progression_supported") is False
            for event in system_events
        ),
        correction_request_count=sum(
            event.event_type_id == "CORRECTION_REQUESTED"
            for event in system_events
        ),
        correction_not_requested_count=correction_availability_states.count("not_requested"),
        correction_not_available_by_cutoff_count=correction_availability_states.count(
            "not_available_by_cutoff"
        ),
        reassessment_started_count=reassessment_queue.telemetry.started_by_cutoff_count,
        reassessment_completed_count=sum(
            event.event_type_id == "REVIEW_COMPLETED"
            and event.details.get("review_kind") == "reassessment"
            for event in system_events
        ),
        timely_reassessment_count=reassessment_queue.telemetry.timely_completion_count,
        late_reassessment_count=reassessment_queue.telemetry.late_completion_count,
        reassessment_right_censored_count=reassessment_queue.telemetry.right_censored_count,
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
            any(
                event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
                and event.details.get("progression_supported") is False
                for event in trace.events
            ) and not any(
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
        restoration_due_count=sum(
            event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED"
            and event.details.get("progression_supported") is False
            for event in system_events
        ),
        restoration_executed_count=len(restoration_events),
        timely_restoration_count=sum(
            event.details.get("restoration_timely") is True
            for event in restoration_events
        ),
        late_restoration_count=sum(
            event.details.get("restoration_timely") is False
            for event in restoration_events
        ),
        complete_restoration_count=sum(
            event.details.get("restoration_complete") is True
            for event in restoration_events
        ),
        partial_restoration_count=sum(
            event.details.get("restoration_complete") is False
            for event in restoration_events
        ),
        restoration_horizon_pending_count=sum(
            event.details.get("restoration_horizon_status") == "pending"
            for event in closure_events
        ),
        restoration_horizon_expired_count=sum(
            event.details.get("restoration_horizon_status")
            == "expired_without_completion"
            for event in closure_events
        ),
        unresolved_external_consequence_count=sum(
            event.details.get("restoration_due") is True
            and event.details.get("restoration_complete") is not True
            for event in closure_events
        ),
        restoration_total_time_from_correction=restoration_total_time,
        restoration_max_time_from_correction=restoration_max_time,
        case_closed_count=len(closure_events),
        resolved_case_count=sum(
            event.details.get("right_censored") is False
            for event in closure_events
        ),
        right_censored_case_count=sum(
            event.details.get("right_censored") is True
            for event in closure_events
        ),
        event_hash=event_hash,
    )
    if telemetry.progression_count + telemetry.hold_count + telemetry.request_evidence_action_count != telemetry.action_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "action dispositions do not partition the cohort")
    if (
        telemetry.timely_assistance_count
        + telemetry.late_assistance_count
        + telemetry.assistance_right_censored_count
        != telemetry.assistance_request_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "assistance outcomes do not partition requests")
    if telemetry.assistance_count != telemetry.timely_assistance_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "engagement assistance differs from timely service completion")
    if telemetry.supported_progression_count + telemetry.unsupported_progression_count != telemetry.progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "progression support does not partition progression")
    if telemetry.evidentially_supported_progression_count + telemetry.evidentially_unsupported_progression_count != telemetry.progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "evidentiary support does not partition progression")
    if telemetry.gate_safe_count + telemetry.gate_unsafe_count != telemetry.gate_applicable_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "gate safety does not partition applicable cases")
    if telemetry.external_exposure_count > telemetry.progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "external exposure exists without observed progression")
    if (
        telemetry.recovery_started_count
        + telemetry.recovery_right_censored_count
        + telemetry.recovery_not_queued_by_cutoff_count
        != telemetry.external_exposure_count
    ):
        raise ContractError(
            "SIM_SYSTEM_STATE_INCOMPLETE",
            "recovery completion, censoring, and unavailable queue entry do not partition exposure",
        )
    if telemetry.recovery_started_count != (
        telemetry.timely_recovery_count + telemetry.late_recovery_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "recovery timeliness does not partition observed completion")
    if telemetry.supported_exposure_count + telemetry.unsupported_exposure_count != telemetry.external_exposure_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "support does not partition exposure")
    if telemetry.evidentially_unsupported_exposure_count > telemetry.evidentially_unsupported_progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "unsupported exposure lacks an observed progression")
    if telemetry.unauthorized_exposure_count > telemetry.unauthorized_progression_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "unauthorized exposure lacks an observed progression")
    if telemetry.correction_eligible_count != telemetry.unsupported_exposure_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction eligibility differs from unsupported exposure")
    if (
        telemetry.correction_request_count
        + telemetry.correction_not_requested_count
        + telemetry.correction_not_available_by_cutoff_count
        != telemetry.correction_eligible_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "correction uptake does not partition eligible exposure")
    if telemetry.reassessment_completed_count > telemetry.reassessment_started_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reassessment completed without starting by cutoff")
    if (
        telemetry.timely_reassessment_count
        + telemetry.late_reassessment_count
        != telemetry.reassessment_completed_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reassessment timeliness does not partition completions")
    if (
        telemetry.reassessment_completed_count
        + telemetry.reassessment_right_censored_count
        != telemetry.correction_request_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reassessment completion and censoring do not partition requests")
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
    if telemetry.restoration_due_count != telemetry.correction_eligible_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration obligations differ from unsupported exposure")
    for event in restoration_events:
        dimensions = tuple(event.details.get("modeled_consequence_dimension_ids", ()))
        baselines = event.details.get("baseline_dimension_states")
        states = event.details.get("dimension_states")
        if (
            dimensions != RESTORATION_DIMENSION_IDS
            or baselines != RESTORATION_BASELINE_STATES
            or not isinstance(states, dict)
        ):
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration consequence vector is incomplete")
        if tuple(states) != RESTORATION_DIMENSION_IDS:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration dimension-state order or coverage changed")
        vector_complete = all(
            states[dimension] == baselines[dimension] for dimension in dimensions
        )
        if vector_complete != (event.details.get("restoration_complete") is True):
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration completeness differs from consequence vector")
    if telemetry.restoration_executed_count > telemetry.correction_executed_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration executed without decision correction")
    if (
        telemetry.timely_restoration_count + telemetry.late_restoration_count
        != telemetry.restoration_executed_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration timeliness does not partition execution")
    if (
        telemetry.complete_restoration_count + telemetry.partial_restoration_count
        != telemetry.restoration_executed_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration completeness does not partition execution")
    if (
        telemetry.complete_restoration_count != telemetry.timely_restoration_count
        or telemetry.partial_restoration_count != telemetry.late_restoration_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration vector completeness differs from horizon timing")
    if (
        telemetry.restoration_executed_count
        + telemetry.restoration_horizon_pending_count
        + telemetry.restoration_horizon_expired_count
        != telemetry.restoration_due_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "restoration outcomes do not partition obligations")
    if (
        telemetry.unresolved_external_consequence_count
        != telemetry.restoration_due_count - telemetry.complete_restoration_count
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "unresolved consequences differ from incomplete restoration")
    if telemetry.case_closed_count != telemetry.case_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "administrative cutoff must close every case exactly once")
    if telemetry.resolved_case_count + telemetry.right_censored_case_count != telemetry.case_count:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "resolved and right-censored closure do not partition cases")
    if any(event.timestamp > cohort.overlay.administrative_cutoff for event in system_events):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "post-cutoff event survived observation closure")
    return EngagementRun(
        cohort.scenario_id, policy_id, cohort.telemetry.cohort_hash,
        traces, system_events, assistance_queue, review_queue, recovery_queue,
        reassessment_queue, telemetry,
    )
