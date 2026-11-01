from dataclasses import replace
from decimal import Decimal, localcontext

import pytest

from uncertainty_permission_simulation.configuration import compile_configuration
from uncertainty_permission_simulation.profiles import policy, stochastic_process
from uncertainty_permission_simulation.random_streams import DRAW_FAMILY_IDS
from uncertainty_permission_simulation.schemas import ContractError
from uncertainty_permission_simulation.simulator import (
    ServiceQueueConfig,
    ServiceRequest,
    StochasticCohortSpec,
    StochasticInputOverlay,
    generate_stochastic_cohort,
    run_engagement_stage,
    schedule_service_queue,
)


def overlay(**updates: object) -> StochasticInputOverlay:
    base = StochasticInputOverlay(
        overlay_id="STYLIZED-OVERLAY-1", provenance="stylized", initiation_window=Decimal("10"),
        notice_delay=Decimal("1"), response_deadline=Decimal("21"),
        review_capacity=Decimal("1"), review_service_time=Decimal("30"), review_service_window=Decimal("14"),
        extension_duration=Decimal("7"),
        notice_delivery_probability=Decimal("0.9"), administrative_access_probability=Decimal("0.75"),
        comprehension_probability=Decimal("0.8"), record_availability_probability=Decimal("0.65"),
        response_effort_limit=Decimal("0.55"), assistance_effort_bonus=Decimal("0.3"),
        extension_effort_bonus=Decimal("0.15"),
        extension_need_probability=Decimal("0.25"), evidence_retrieval_success_probability=Decimal("0.7"),
        evidence_retrieval_latency_scale=Decimal("10"),
        external_consequence_delay=Decimal("1"), recovery_start_delay=Decimal("2"),
        correction_request_delay=Decimal("7"), correction_uptake_probability=Decimal("0.75"),
        reassessment_capacity=Decimal("1"), reassessment_service_time=Decimal("30"),
        correction_window=Decimal("14"),
    )
    return replace(base, **updates)


def compiled(policy_id: str, input_overlay: StochasticInputOverlay):
    return compile_configuration(
        configuration_id=f"TEST-{policy_id}", process=stochastic_process(), policy=policy(policy_id),
        overlay=input_overlay.to_compilation_overlay(), evaluation_spec_id="TEST-EVALUATION",
    )


def spec(**updates: object) -> StochasticCohortSpec:
    base = StochasticCohortSpec(
        scenario_id="SCENARIO-1", seed_id="SEED-1", case_ids=("CASE-3", "CASE-1", "CASE-2"),
        overlay=overlay(),
    )
    return replace(base, **updates)


def test_finite_cohort_replays_with_identical_hash_and_telemetry() -> None:
    first = generate_stochastic_cohort(spec())
    second = generate_stochastic_cohort(spec())
    assert first == second
    assert first.telemetry.cohort_hash == second.telemetry.cohort_hash
    assert first.telemetry.case_count == 3
    assert first.telemetry.keyed_draw_count == 3 * len(DRAW_FAMILY_IDS)
    assert first.telemetry.duplicate_draw_key_count == 0


def test_case_input_order_does_not_change_cohort_artifact() -> None:
    first = generate_stochastic_cohort(spec(case_ids=("CASE-1", "CASE-2", "CASE-3")))
    second = generate_stochastic_cohort(spec(case_ids=("CASE-3", "CASE-1", "CASE-2")))
    assert [case.case_id for case in first.cases] == ["CASE-1", "CASE-2", "CASE-3"]
    assert first.telemetry.cohort_hash == second.telemetry.cohort_hash
    assert tuple(case.draw_hash for case in first.cases) == tuple(case.draw_hash for case in second.cases)


def test_paired_policy_consumers_can_share_exact_exogenous_cases() -> None:
    u2c_input = generate_stochastic_cohort(spec())
    u2o_input = generate_stochastic_cohort(spec())
    u2c_case_hashes = {case.case_id: case.draw_hash for case in u2c_input.cases}
    u2o_case_hashes = {case.case_id: case.draw_hash for case in u2o_input.cases}
    assert u2c_case_hashes == u2o_case_hashes


def test_seed_change_changes_draws_but_not_case_membership() -> None:
    first = generate_stochastic_cohort(spec(seed_id="SEED-1"))
    second = generate_stochastic_cohort(spec(seed_id="SEED-2"))
    assert tuple(case.case_id for case in first.cases) == tuple(case.case_id for case in second.cases)
    assert first.telemetry.cohort_hash != second.telemetry.cohort_hash


def test_arrivals_stay_inside_closed_initiation_window() -> None:
    cohort = generate_stochastic_cohort(spec(overlay=overlay(overlay_id="STYLIZED-OVERLAY-2", initiation_window=Decimal("12.5"))))
    assert all(Decimal(0) < case.arrival_time < Decimal("12.5") for case in cohort.cases)


@pytest.mark.parametrize(
    "updates",
    (
        {"case_ids": ()},
        {"case_ids": ("CASE-1", "CASE-1")},
        {"case_ids": ["CASE-1"]},
        {"overlay": "not-an-overlay"},
    ),
)
def test_invalid_cohort_specs_fail_before_draws(updates: dict[str, object]) -> None:
    with pytest.raises(ContractError, match="SCENARIO_(INVALID|PARAMETER_INVALID)"):
        spec(**updates)


@pytest.mark.parametrize(("field", "value"), (
    ("provenance", "documented"),
    ("initiation_window", Decimal("-1")),
    ("initiation_window", Decimal("NaN")),
    ("initiation_window", "10"),
    ("response_deadline", Decimal("0")),
    ("review_service_window", Decimal("0")),
    ("external_consequence_delay", Decimal("-1")),
    ("recovery_start_delay", Decimal("NaN")),
    ("correction_request_delay", Decimal("-1")),
    ("correction_uptake_probability", Decimal("1.1")),
    ("reassessment_capacity", Decimal("0")),
    ("reassessment_capacity", Decimal("1.5")),
    ("reassessment_service_time", Decimal("0")),
    ("correction_window", Decimal("0")),
    ("notice_delivery_probability", Decimal("1.1")),
))
def test_invalid_stochastic_overlay_values_are_rejected(field: str, value: object) -> None:
    with pytest.raises(ContractError, match="SCENARIO_PARAMETER_INVALID"):
        overlay(**{field: value})


def test_all_policy_runs_share_cases_and_exogenous_draws() -> None:
    cohort = generate_stochastic_cohort(spec())
    runs = {policy_id: run_engagement_stage(cohort, compiled(policy_id, cohort.overlay)) for policy_id in ("U0", "U1", "U2C", "U2O", "U3")}
    expected = {case.case_id: case.draw_hash for case in cohort.cases}
    assert all(run.cohort_hash == cohort.telemetry.cohort_hash for run in runs.values())
    assert all({trace.case_id: trace.exogenous_draw_hash for trace in run.traces} == expected for run in runs.values())


def test_policy_path_divergence_preserves_common_causal_keys() -> None:
    forced = overlay(
        notice_delivery_probability=Decimal("1"), administrative_access_probability=Decimal("0"),
        comprehension_probability=Decimal("0"), record_availability_probability=Decimal("0"),
        response_effort_limit=Decimal("0"), assistance_effort_bonus=Decimal("1"),
        extension_need_probability=Decimal("1"), evidence_retrieval_success_probability=Decimal("1"),
    )
    cohort = generate_stochastic_cohort(spec(case_ids=("CASE-1",), overlay=forced))
    u1 = run_engagement_stage(cohort, compiled("U1", cohort.overlay)).traces[0]
    u3 = run_engagement_stage(cohort, compiled("U3", cohort.overlay)).traces[0]
    assert len(u1.events) != len(u3.events)
    assert u1.exogenous_draw_hash == u3.exogenous_draw_hash
    u1_keys = {event.event_type_id: event.causal_event_key for event in u1.events}
    u3_keys = {event.event_type_id: event.causal_event_key for event in u3.events}
    for event_type in {"CASE_ARRIVAL", "SOURCE_EVIDENCE_INGESTED", "NOTICE_SENT", "NOTICE_DELIVERED", "ACCESS_ATTEMPTED", "REPRESENTATION_APPLIED", "REPRESENTATION_SURFACED", "ROUTING_COMPLETED"}:
        assert u1_keys[event_type] == u3_keys[event_type]
    u1_response_deadline = next(
        event for event in u1.events
        if event.event_type_id == "DEADLINE_REACHED"
        and event.details.get("deadline_kind") == "response"
    )
    u3_response_deadline = next(
        event for event in u3.events
        if event.event_type_id == "DEADLINE_REACHED"
        and event.details.get("deadline_kind") == "response"
    )
    assert u1_response_deadline.causal_event_key == u3_response_deadline.causal_event_key
    assert "EXTENSION_GRANTED" not in u1_keys and "EXTENSION_GRANTED" in u3_keys
    assert "EXTERNAL_EVIDENCE_RETURNED" not in u1_keys and "EXTERNAL_EVIDENCE_RETURNED" in u3_keys


def test_action_stage_replays_event_hashes_through_decision_correction() -> None:
    cohort = generate_stochastic_cohort(spec())
    configuration = compiled("U2C", cohort.overlay)
    first = run_engagement_stage(cohort, configuration)
    second = run_engagement_stage(cohort, configuration)
    assert first == second
    assert first.telemetry.event_hash == second.telemetry.event_hash
    assert first.telemetry.action_count == len(cohort.cases)
    assert all(trace.action_decision is not None for trace in first.traces)
    assert first.telemetry.external_exposure_count == first.telemetry.progression_count
    assert first.telemetry.recovery_started_count == first.telemetry.external_exposure_count
    assert all(
        event.event_type_id not in {"RESTORATION_EXECUTED", "CASE_CLOSED"}
        for trace in first.traces for event in trace.events
    )


def test_exposure_descends_only_from_executed_progression_and_preserves_support() -> None:
    cohort = generate_stochastic_cohort(spec())
    for policy_id in ("U0", "U1", "U2C", "U2O", "U3"):
        run = run_engagement_stage(cohort, compiled(policy_id, cohort.overlay))
        for trace in run.traces:
            types = tuple(event.event_type_id for event in trace.events)
            if trace.action_decision is not None and trace.action_decision.action == "progress":
                assert types.index("PROGRESSION_EXECUTED") < types.index("EXTERNAL_CONSEQUENCE_STARTED")
                assert types.index("EXTERNAL_CONSEQUENCE_STARTED") < types.index("EXTERNAL_CONSEQUENCE_UPDATED")
                exposure = next(event for event in trace.events if event.event_type_id == "EXTERNAL_CONSEQUENCE_STARTED")
                recovery = next(
                    event for event in trace.events
                    if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
                    and event.details.get("action_type_id") == "recover"
                )
                progression = next(event for event in trace.events if event.event_type_id == "PROGRESSION_EXECUTED")
                with localcontext() as context:
                    context.prec = 50
                    assert exposure.timestamp == progression.timestamp + cohort.overlay.external_consequence_delay
                    assert recovery.timestamp == exposure.timestamp + cohort.overlay.recovery_start_delay
                assert exposure.details["source_progression_event_key"] == progression.causal_event_key
                assert recovery.details["source_external_consequence_event_key"] == exposure.causal_event_key
                assert exposure.details["progression_supported"] is trace.action_decision.progression_supported
                assert recovery.details["unsupported_reason_codes"] == trace.action_decision.unsupported_reason_codes
            else:
                assert "EXTERNAL_CONSEQUENCE_STARTED" not in types
                assert "EXTERNAL_CONSEQUENCE_UPDATED" not in types


def test_zero_delays_use_frozen_progression_exposure_recovery_order() -> None:
    zero_delay = overlay(external_consequence_delay=Decimal("0"), recovery_start_delay=Decimal("0"))
    cohort = generate_stochastic_cohort(spec(case_ids=("CASE-1",), overlay=zero_delay))
    trace = run_engagement_stage(cohort, compiled("U1", cohort.overlay)).traces[0]
    ordered = tuple(
        event.event_type_id for event in trace.events
        if event.event_type_id in {
            "ACTION_COMPUTED", "PROGRESSION_EXECUTED",
            "EXTERNAL_CONSEQUENCE_STARTED",
        }
        or (
            event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
            and event.details.get("action_type_id") == "recover"
        )
    )
    assert ordered == (
        "ACTION_COMPUTED", "PROGRESSION_EXECUTED",
        "EXTERNAL_CONSEQUENCE_STARTED", "EXTERNAL_CONSEQUENCE_UPDATED",
    )


def test_unsupported_exposure_can_request_correction_and_enter_reassessment() -> None:
    correction_overlay = overlay(
        record_availability_probability=Decimal("0"),
        correction_uptake_probability=Decimal("1"),
    )
    cohort = generate_stochastic_cohort(spec(overlay=correction_overlay))
    run = run_engagement_stage(cohort, compiled("U1", cohort.overlay))
    assert run.telemetry.correction_eligible_count == len(cohort.cases)
    assert run.telemetry.correction_request_count == len(cohort.cases)
    assert run.telemetry.correction_not_requested_count == 0
    assert run.telemetry.reassessment_started_count == len(cohort.cases)
    assert run.telemetry.reassessment_completed_count == len(cohort.cases)
    assert run.telemetry.correction_executed_count == len(cohort.cases)
    assert run.telemetry.correction_unresolved_count == 0
    assert run.telemetry.recovery_active_after_correction_count == len(cohort.cases)
    assert (
        run.telemetry.timely_correction_count + run.telemetry.late_correction_count
        == len(cohort.cases)
    )
    assert len(run.reassessment_queue.visits) == len(cohort.cases)
    for trace in run.traces:
        recovery = next(
            event for event in trace.events
            if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
            and event.details.get("recovery_state") == "active"
        )
        request = next(event for event in trace.events if event.event_type_id == "CORRECTION_REQUESTED")
        completion = next(
            event for event in trace.events
            if event.event_type_id == "REVIEW_COMPLETED"
            and event.details.get("review_kind") == "reassessment"
        )
        outcome = next(
            event for event in trace.events
            if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
            and event.details.get("correction_outcome") == "decision_corrected"
        )
        assert recovery.timestamp < request.timestamp < completion.timestamp
        assert completion.timestamp == outcome.timestamp
        assert trace.events.index(completion) < trace.events.index(outcome)
        assert request.details["source_recovery_event_key"] == recovery.causal_event_key
        assert completion.details["source_correction_request_event_key"] == request.causal_event_key
        assert completion.details["correction_executed"] is False
        assert completion.details["restoration_executed"] is False
        assert outcome.details["source_reassessment_event_key"] == completion.causal_event_key
        assert outcome.details["correction_basis"] == "unsupported_progression_confirmed"
        assert (
            outcome.details["unsupported_reason_codes"]
            == trace.action_decision.unsupported_reason_codes
        )
        assert outcome.details["decision_state"] == "corrected_to_baseline"
        assert outcome.details["recovery_state"] == "active"
        assert outcome.details["restoration_state"] == "incomplete"
        assert outcome.details["restoration_complete"] is False
        assert Decimal(outcome.details["exposure_duration_to_correction"]) > 0
        assert not any(event.event_type_id == "RESTORATION_EXECUTED" for event in trace.events)


def test_correction_uptake_zero_leaves_eligible_exposure_unrequested() -> None:
    no_uptake = overlay(
        record_availability_probability=Decimal("0"),
        correction_uptake_probability=Decimal("0"),
    )
    cohort = generate_stochastic_cohort(spec(overlay=no_uptake))
    run = run_engagement_stage(cohort, compiled("U1", cohort.overlay))
    assert run.telemetry.correction_eligible_count == len(cohort.cases)
    assert run.telemetry.correction_request_count == 0
    assert run.telemetry.correction_not_requested_count == len(cohort.cases)
    assert run.telemetry.correction_executed_count == 0
    assert run.telemetry.correction_unresolved_count == len(cohort.cases)
    assert run.reassessment_queue.visits == ()
    assert run.telemetry.reassessment_completed_count == 0


def test_reassessment_completion_at_correction_deadline_is_timely_and_ordered() -> None:
    base = overlay(
        record_availability_probability=Decimal("0"),
        correction_uptake_probability=Decimal("1"),
    )
    probe = generate_stochastic_cohort(spec(case_ids=("CASE-1",), overlay=base))
    service_draw = probe.cases[0].draw_map[("reassessment_service", 0)]
    with localcontext() as context:
        context.prec = 50
        exact_window = service_draw * base.reassessment_service_time
    exact = replace(base, correction_window=exact_window)
    cohort = generate_stochastic_cohort(spec(case_ids=("CASE-1",), overlay=exact))
    run = run_engagement_stage(cohort, compiled("U1", cohort.overlay))
    visit = run.reassessment_queue.visits[0]
    assert visit.completed_at == visit.deadline
    assert visit.completed_by_deadline is True
    completion = next(
        event for event in run.traces[0].events
        if event.event_type_id == "REVIEW_COMPLETED"
        and event.details.get("review_kind") == "reassessment"
    )
    deadline = next(
        event for event in run.traces[0].events
        if event.event_type_id == "DEADLINE_REACHED"
        and event.details.get("deadline_kind") == "correction_service"
    )
    outcome = next(
        event for event in run.traces[0].events
        if event.event_type_id == "EXTERNAL_CONSEQUENCE_UPDATED"
        and event.details.get("correction_outcome") == "decision_corrected"
    )
    assert completion.timestamp == deadline.timestamp
    assert outcome.timestamp == deadline.timestamp
    assert run.traces[0].events.index(completion) < run.traces[0].events.index(deadline)
    assert run.traces[0].events.index(deadline) < run.traces[0].events.index(outcome)
    assert outcome.details["correction_timely"] is True


def test_u2_fail_closed_and_fail_open_share_queue_semantics_before_actions() -> None:
    cohort = generate_stochastic_cohort(spec())
    closed = run_engagement_stage(cohort, compiled("U2C", cohort.overlay))
    opened = run_engagement_stage(cohort, compiled("U2O", cohort.overlay))
    assert closed.review_queue == opened.review_queue
    assert closed.telemetry.review_queue_count == len(cohort.cases)
    assert opened.telemetry.review_queue_count == len(cohort.cases)
    assert closed.telemetry.fail_open_timeout_progression_count == 0
    assert opened.telemetry.fail_closed_timeout_hold_count == 0


def test_sufficient_evidence_is_not_labeled_as_imputation() -> None:
    forced = overlay(
        notice_delivery_probability=Decimal("1"), administrative_access_probability=Decimal("1"),
        comprehension_probability=Decimal("1"), record_availability_probability=Decimal("1"),
        response_effort_limit=Decimal("1"),
    )
    cohort = generate_stochastic_cohort(spec(case_ids=("CASE-1",), overlay=forced))
    trace = run_engagement_stage(cohort, compiled("U2C", cohort.overlay)).traces[0]
    representation = next(event for event in trace.events if event.event_type_id == "REPRESENTATION_APPLIED")
    assert representation.details["representation_mode"] == "period_specific_evidence"


def test_engagement_runner_rejects_configuration_overlay_drift() -> None:
    cohort = generate_stochastic_cohort(spec())
    drifted_overlay = overlay(response_effort_limit=Decimal("0.2"))
    with pytest.raises(ContractError, match="SCENARIO_CONFIGURATION_INCOMPLETE"):
        run_engagement_stage(cohort, compiled("U1", drifted_overlay))

    sensitivity_overlay = overlay(provenance="sensitivity")
    with pytest.raises(ContractError, match="SCENARIO_CONFIGURATION_INCOMPLETE"):
        run_engagement_stage(cohort, compiled("U1", sensitivity_overlay))


@pytest.mark.parametrize(
    ("field_name", "missing_id"),
    (
        ("stage_ids", "reassessment"),
        ("capabilities", "recovery"),
        ("capabilities", "reassessment"),
        ("action_type_ids", "recover"),
        ("action_type_ids", "reassess"),
    ),
)
def test_engagement_runner_rejects_incomplete_consequence_process(
    field_name: str,
    missing_id: str,
) -> None:
    cohort = generate_stochastic_cohort(spec())
    process = stochastic_process()
    current = getattr(process, field_name)
    incomplete = (
        tuple(value for value in current if value != missing_id)
        if isinstance(current, tuple)
        else current - {missing_id}
    )
    process = process.model_copy(update={field_name: incomplete})
    configuration = compile_configuration(
        configuration_id=f"MISSING-{missing_id}",
        process=process,
        policy=policy("U1"),
        overlay=cohort.overlay.to_compilation_overlay(),
        evaluation_spec_id="TEST-EVALUATION",
    )
    with pytest.raises(ContractError, match="SCENARIO_CONFIGURATION_INCOMPLETE"):
        run_engagement_stage(cohort, configuration)


def test_fifo_service_queue_is_input_order_invariant_and_work_conserving() -> None:
    queue = ServiceQueueConfig("REVIEW", 1)
    first = ServiceRequest("R-1", "CASE-1", Decimal("0"), Decimal("2"), Decimal("10"))
    second = ServiceRequest("R-2", "CASE-2", Decimal("1"), Decimal("1"), Decimal("10"))
    forward = schedule_service_queue(queue, (first, second))
    reversed_input = schedule_service_queue(queue, (second, first))
    assert forward == reversed_input
    assert [(visit.started_at, visit.completed_at, visit.wait_time) for visit in forward.visits] == [
        (Decimal("0"), Decimal("2"), Decimal("0")),
        (Decimal("2"), Decimal("3"), Decimal("1")),
    ]
    assert forward.telemetry.immediate_start_count == 1
    assert forward.telemetry.timely_completion_count == 2


def test_service_capacity_and_exact_deadline_boundary_are_explicit() -> None:
    requests = (
        ServiceRequest("R-1", "CASE-1", Decimal("0"), Decimal("2"), Decimal("2")),
        ServiceRequest("R-2", "CASE-2", Decimal("0"), Decimal("2"), Decimal("2")),
    )
    single = schedule_service_queue(ServiceQueueConfig("REVIEW", 1), requests)
    parallel = schedule_service_queue(ServiceQueueConfig("REVIEW", 2), requests)
    assert [visit.completed_by_deadline for visit in single.visits] == [True, False]
    assert [visit.completed_by_deadline for visit in parallel.visits] == [True, True]
    assert parallel.telemetry.max_wait_time == 0
    assert single.telemetry.schedule_hash != parallel.telemetry.schedule_hash


@pytest.mark.parametrize(
    ("config", "requests"),
    (
        (ServiceQueueConfig("REVIEW", 1), [ServiceRequest("R", "C", Decimal(0), Decimal(1), Decimal(2))]),
        (ServiceQueueConfig("REVIEW", 1), ("not-a-request",)),
        (ServiceQueueConfig("REVIEW", 1), (
            ServiceRequest("R", "C-1", Decimal(0), Decimal(1), Decimal(2)),
            ServiceRequest("R", "C-2", Decimal(0), Decimal(1), Decimal(2)),
        )),
    ),
)
def test_invalid_service_request_collections_are_rejected(config: object, requests: object) -> None:
    with pytest.raises(ContractError, match="SIM_SYSTEM_STATE_INCOMPLETE"):
        schedule_service_queue(config, requests)  # type: ignore[arg-type]


def test_invalid_service_queue_and_request_values_are_rejected() -> None:
    with pytest.raises(ContractError, match="SIM_SYSTEM_STATE_INCOMPLETE"):
        schedule_service_queue("not-a-config", ())  # type: ignore[arg-type]
    with pytest.raises(ContractError, match="SIM_SYSTEM_STATE_INCOMPLETE"):
        ServiceQueueConfig("REVIEW", 0)
    with pytest.raises(ContractError, match="SIM_SYSTEM_STATE_INCOMPLETE"):
        ServiceRequest("R", "C", Decimal("2"), Decimal("1"), Decimal("1"))
