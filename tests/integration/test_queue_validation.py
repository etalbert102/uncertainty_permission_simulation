from dataclasses import replace
from decimal import Decimal

from uncertainty_permission_simulation.configuration import compile_configuration
from uncertainty_permission_simulation.profiles import policy, stochastic_process
from uncertainty_permission_simulation.simulator import (
    ServiceQueueConfig,
    ServiceRequest,
    StochasticCohortSpec,
    StochasticInputOverlay,
    generate_stochastic_cohort,
    run_engagement_stage,
    schedule_service_queue,
)


def _overlay(**updates: object) -> StochasticInputOverlay:
    base = StochasticInputOverlay(
        overlay_id="QUEUE-OVERLAY", provenance="stylized", initiation_window=Decimal("0"),
        notice_delay=Decimal("1"), response_deadline=Decimal("21"),
        review_capacity=Decimal("1"), review_service_time=Decimal("30"),
        review_service_window=Decimal("14"), extension_duration=Decimal("7"),
        notice_delivery_probability=Decimal("1"), administrative_access_probability=Decimal("1"),
        comprehension_probability=Decimal("1"), record_availability_probability=Decimal("0"),
        response_effort_limit=Decimal("1"), assistance_effort_bonus=Decimal("0"),
        extension_effort_bonus=Decimal("0"), extension_need_probability=Decimal("0"),
        evidence_retrieval_success_probability=Decimal("0"),
        evidence_retrieval_latency_scale=Decimal("0"),
    )
    return replace(base, **updates)


def _run(policy_id: str, input_overlay: StochasticInputOverlay):
    cohort = generate_stochastic_cohort(StochasticCohortSpec(
        scenario_id="QUEUE-SCENARIO", seed_id="QUEUE-SEED",
        case_ids=("CASE-4", "CASE-2", "CASE-1", "CASE-3"), overlay=input_overlay,
    ))
    configuration = compile_configuration(
        configuration_id=f"QUEUE-{policy_id}", process=stochastic_process(),
        policy=policy(policy_id), overlay=input_overlay.to_compilation_overlay(),
        evaluation_spec_id="QUEUE-EVALUATION",
    )
    return cohort, run_engagement_stage(cohort, configuration)


def test_u2_policies_share_the_exact_review_schedule_before_timeout_behavior() -> None:
    input_overlay = _overlay()
    cohort, closed = _run("U2C", input_overlay)
    _, opened = _run("U2O", input_overlay)
    assert closed.review_queue == opened.review_queue
    assert closed.telemetry.review_schedule_hash == opened.telemetry.review_schedule_hash
    assert closed.telemetry.review_queue_count == len(cohort.cases)
    assert closed.telemetry.review_started_count == len(cohort.cases)
    assert closed.telemetry.review_completed_count == len(cohort.cases)
    assert closed.telemetry.timely_review_count + closed.telemetry.late_review_count == len(cohort.cases)
    assert tuple(event.timestamp for event in closed.system_events) == tuple(
        sorted(event.timestamp for event in closed.system_events)
    )
    for trace in closed.traces:
        assert tuple(event for event in closed.system_events if event.case_id == trace.case_id) == trace.events


def test_more_review_capacity_never_delays_a_paired_case() -> None:
    low_cohort, low = _run("U2C", _overlay(review_capacity=Decimal("1")))
    high_cohort, high = _run("U2C", _overlay(review_capacity=Decimal("4")))
    assert [case.draw_hash for case in low_cohort.cases] == [case.draw_hash for case in high_cohort.cases]
    low_visits = {visit.case_id: visit for visit in low.review_queue.visits}
    high_visits = {visit.case_id: visit for visit in high.review_queue.visits}
    assert all(high_visits[case_id].started_at <= visit.started_at for case_id, visit in low_visits.items())
    assert all(high_visits[case_id].completed_at <= visit.completed_at for case_id, visit in low_visits.items())
    assert high.telemetry.timely_review_count >= low.telemetry.timely_review_count


def test_review_completion_and_deadline_race_uses_frozen_event_priority() -> None:
    _, run = _run(
        "U2C",
        _overlay(review_service_time=Decimal("0"), review_service_window=Decimal("1")),
    )
    for trace in run.traces:
        review_completion = next(event for event in trace.events if event.event_type_id == "REVIEW_COMPLETED")
        review_deadline = next(
            event for event in trace.events
            if event.event_type_id == "DEADLINE_REACHED"
            and event.details.get("deadline_kind") == "review_service"
        )
        assert review_completion.timestamp < review_deadline.timestamp
        assert review_completion.details["completed_by_deadline"] is True


def test_unreviewed_policy_has_a_closed_empty_queue_artifact() -> None:
    _, run = _run("U1", _overlay())
    assert run.review_queue.visits == ()
    assert run.telemetry.review_queue_count == 0
    assert run.telemetry.review_started_count == 0
    assert run.telemetry.review_completed_count == 0
    assert run.telemetry.review_schedule_hash == run.review_queue.telemetry.schedule_hash


def test_finite_window_capacity_bound_matches_hand_calculation() -> None:
    queue = ServiceQueueConfig("BOUND", 2)

    def requests(count: int) -> tuple[ServiceRequest, ...]:
        return tuple(
            ServiceRequest(
                request_id=f"R-{index}", case_id=f"CASE-{index}",
                queued_at=Decimal("0"), service_time=Decimal("2"), deadline=Decimal("4"),
            )
            for index in range(count)
        )

    equality = schedule_service_queue(queue, requests(4))
    overload = schedule_service_queue(queue, requests(5))
    assert sum(visit.service_time for visit in equality.visits) == Decimal("8") == Decimal(2) * Decimal(4)
    assert equality.telemetry.timely_completion_count == 4
    assert max(visit.completed_at for visit in equality.visits) == Decimal("4")
    assert sum(visit.service_time for visit in overload.visits) == Decimal("10") > Decimal(2) * Decimal(4)
    assert overload.telemetry.timely_completion_count == 4
    assert overload.telemetry.late_completion_count == 1
