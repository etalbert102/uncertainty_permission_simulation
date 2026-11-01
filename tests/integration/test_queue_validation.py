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
        external_consequence_delay=Decimal("1"), recovery_start_delay=Decimal("2"),
        correction_request_delay=Decimal("7"), correction_uptake_probability=Decimal("1"),
        reassessment_capacity=Decimal("1"), reassessment_service_time=Decimal("30"),
        correction_window=Decimal("14"),
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

    closed_by_case = {trace.case_id: trace for trace in closed.traces}
    opened_by_case = {trace.case_id: trace for trace in opened.traces}
    for visit in closed.review_queue.visits:
        closed_decision = closed_by_case[visit.case_id].action_decision
        opened_decision = opened_by_case[visit.case_id].action_decision
        assert closed_decision is not None and opened_decision is not None
        if visit.completed_by_deadline:
            assert closed_decision.action == opened_decision.action == "request_evidence"
        else:
            assert closed_decision.action == "hold"
            assert closed_decision.reason_code == "review_timeout_fail_closed"
            assert opened_decision.action == "progress"
            assert opened_decision.reason_code == "review_timeout_fail_open"
            assert opened_decision.progression_supported is False
            assert opened_decision.gate_safe is False
            closed_action = next(
                event for event in closed_by_case[visit.case_id].events
                if event.event_type_id == "ACTION_COMPUTED"
            )
            opened_action = next(
                event for event in opened_by_case[visit.case_id].events
                if event.event_type_id == "ACTION_COMPUTED"
            )
            assert closed_action.causal_event_key == opened_action.causal_event_key
            closed_types = {event.event_type_id for event in closed_by_case[visit.case_id].events}
            opened_types = {event.event_type_id for event in opened_by_case[visit.case_id].events}
            assert "EXTERNAL_CONSEQUENCE_STARTED" not in closed_types
            assert "EXTERNAL_CONSEQUENCE_STARTED" in opened_types


def test_fail_open_timeout_converts_queue_delay_into_unauthorized_recovery_exposure() -> None:
    _, closed = _run(
        "U2C",
        _overlay(review_service_time=Decimal("30"), review_service_window=Decimal("0.0000000001")),
    )
    _, opened = _run(
        "U2O",
        _overlay(review_service_time=Decimal("30"), review_service_window=Decimal("0.0000000001")),
    )
    assert closed.telemetry.external_exposure_count == 0
    assert closed.telemetry.recovery_started_count == 0
    assert opened.telemetry.external_exposure_count == len(opened.traces)
    assert opened.telemetry.recovery_started_count == len(opened.traces)
    assert opened.telemetry.unauthorized_exposure_count == len(opened.traces)
    assert opened.telemetry.correction_executed_count == len(opened.traces)
    assert opened.telemetry.recovery_active_after_correction_count == len(opened.traces)


def test_reassessment_capacity_never_delays_a_paired_correction_request() -> None:
    low_cohort, low = _run(
        "U1",
        _overlay(reassessment_capacity=Decimal("1")),
    )
    high_cohort, high = _run(
        "U1",
        _overlay(reassessment_capacity=Decimal("4")),
    )
    assert [case.draw_hash for case in low_cohort.cases] == [
        case.draw_hash for case in high_cohort.cases
    ]
    low_visits = {visit.case_id: visit for visit in low.reassessment_queue.visits}
    high_visits = {visit.case_id: visit for visit in high.reassessment_queue.visits}
    assert low_visits.keys() == high_visits.keys()
    assert all(
        high_visits[case_id].started_at <= visit.started_at
        for case_id, visit in low_visits.items()
    )
    assert all(
        high_visits[case_id].completed_at <= visit.completed_at
        for case_id, visit in low_visits.items()
    )
    assert high.telemetry.timely_reassessment_count >= low.telemetry.timely_reassessment_count
    assert low.telemetry.correction_executed_count == high.telemetry.correction_executed_count
    assert high.telemetry.timely_correction_count >= low.telemetry.timely_correction_count


def test_supported_exposure_does_not_enter_correction_queue() -> None:
    _, run = _run(
        "U1",
        _overlay(record_availability_probability=Decimal("1")),
    )
    assert run.telemetry.supported_exposure_count == len(run.traces)
    assert run.telemetry.correction_eligible_count == 0
    assert run.telemetry.correction_request_count == 0
    assert run.telemetry.correction_executed_count == 0
    assert run.reassessment_queue.visits == ()


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
        review_completion = next(
            event for event in trace.events
            if event.event_type_id == "REVIEW_COMPLETED"
            and event.details.get("review_kind") == "pre_action"
        )
        review_deadline = next(
            event for event in trace.events
            if event.event_type_id == "DEADLINE_REACHED"
            and event.details.get("deadline_kind") == "review_service"
        )
        assert review_completion.timestamp < review_deadline.timestamp
        assert review_completion.details["completed_by_deadline"] is True
        assert trace.action_decision is not None
        assert trace.action_decision.timeout_triggered is False


def test_timely_supported_review_records_authorization_before_progression() -> None:
    _, run = _run(
        "U2C",
        _overlay(
            record_availability_probability=Decimal("1"),
            review_service_time=Decimal("0"),
            review_service_window=Decimal("1"),
        ),
    )
    assert run.telemetry.supported_progression_count == len(run.traces)
    assert run.telemetry.review_authorization_count == len(run.traces)
    assert run.telemetry.gate_safe_count == len(run.traces)
    assert run.telemetry.gate_unsafe_count == 0
    for trace in run.traces:
        assert trace.action_decision is not None and trace.action_decision.progression_supported
        types = tuple(event.event_type_id for event in trace.events)
        assert types.index("REVIEW_COMPLETED") < types.index("EXTERNAL_AUTHORIZATION_RECORDED")
        assert types.index("EXTERNAL_AUTHORIZATION_RECORDED") < types.index("PROGRESSION_EXECUTED")


def test_fail_open_can_be_evidentially_supported_but_unauthorized() -> None:
    _, run = _run(
        "U2O",
        _overlay(
            record_availability_probability=Decimal("1"),
            review_service_time=Decimal("30"),
            review_service_window=Decimal("0.0000000001"),
        ),
    )
    assert run.telemetry.late_review_count == len(run.traces)
    assert run.telemetry.progression_count == len(run.traces)
    assert run.telemetry.evidentially_supported_progression_count == len(run.traces)
    assert run.telemetry.evidentially_unsupported_progression_count == 0
    assert run.telemetry.unauthorized_progression_count == len(run.traces)
    assert run.telemetry.supported_progression_count == 0
    assert run.telemetry.gate_unsafe_count == len(run.traces)
    for trace in run.traces:
        action = next(event for event in trace.events if event.event_type_id == "ACTION_COMPUTED")
        late_completion = next(
            event for event in trace.events
            if event.event_type_id == "REVIEW_COMPLETED"
            and event.details.get("review_kind") == "pre_action"
        )
        assert action.timestamp < late_completion.timestamp


def test_imputation_progression_and_evidence_hold_remain_distinct() -> None:
    _, u0 = _run("U0", _overlay())
    _, u1 = _run("U1", _overlay())
    assert all(trace.action_decision is not None and trace.action_decision.action == "hold" for trace in u0.traces)
    assert all(
        trace.action_decision is not None
        and trace.action_decision.reason_code == "imputation_progression"
        and not trace.action_decision.progression_supported
        for trace in u1.traces
    )
    assert u1.telemetry.unsupported_progression_count == len(u1.traces)
    assert u1.telemetry.evidentially_unsupported_progression_count == len(u1.traces)
    assert u1.telemetry.unauthorized_progression_count == 0
    assert u0.telemetry.progression_count == 0


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
