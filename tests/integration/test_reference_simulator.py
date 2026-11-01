from decimal import Decimal
from pathlib import Path

import yaml

from uncertainty_permission_simulation.configuration import compile_configuration
from uncertainty_permission_simulation.profiles import policy, stochastic_process
from uncertainty_permission_simulation.reference_simulator import (
    ReferenceRequest,
    analytical_dd1,
    run_reference_fifo,
)
from uncertainty_permission_simulation.simulator import (
    ServiceQueueConfig,
    ServiceRequest,
    StochasticCohortSpec,
    StochasticInputOverlay,
    generate_stochastic_cohort,
    run_engagement_stage,
    schedule_service_queue,
)


ROOT = Path(__file__).resolve().parents[2]
VALIDATION_CONFIG = ROOT / "experiments/configs/slice2_validation_v1.yaml"
SMOKE_CONFIG = ROOT / "experiments/configs/stochastic_smoke_v1.yaml"


def _reference_requests(values: list[dict[str, str]]) -> tuple[ReferenceRequest, ...]:
    return tuple(
        ReferenceRequest(
            request_id=value["request_id"],
            case_id=value["case_id"],
            queued_at=Decimal(value["queued_at"]),
            service_time=Decimal(value["service_time"]),
            deadline=Decimal(value["deadline"]),
        )
        for value in values
    )


def _production_requests(
    requests: tuple[ReferenceRequest, ...],
) -> tuple[ServiceRequest, ...]:
    return tuple(
        ServiceRequest(
            request_id=request.request_id,
            case_id=request.case_id,
            queued_at=request.queued_at,
            service_time=request.service_time,
            deadline=request.deadline,
        )
        for request in requests
    )


def _assert_differential_equal(production, reference) -> None:
    assert len(production.visits) == len(reference)
    for observed, expected in zip(production.visits, reference, strict=True):
        assert observed.request_id == expected.request_id
        assert observed.case_id == expected.case_id
        assert observed.server_id.endswith(f":SERVER-{expected.server_index + 1}")
        for field_name in (
            "queued_at", "started_at", "completed_at", "service_time", "wait_time",
            "deadline", "completed_by_deadline", "started_by_cutoff",
            "completed_by_cutoff", "right_censored", "censoring_reason",
        ):
            assert getattr(observed, field_name) == getattr(expected, field_name)


def test_analytical_dd1_benchmark_matches_within_frozen_tolerance() -> None:
    config = yaml.safe_load(VALIDATION_CONFIG.read_text(encoding="utf-8"))
    benchmark = config["analytical_benchmark"]
    requests = _reference_requests(benchmark["requests"])
    tolerance = Decimal(benchmark["absolute_time_tolerance"])
    analytical = analytical_dd1(requests)
    production = schedule_service_queue(
        ServiceQueueConfig(benchmark["benchmark_id"], benchmark["capacity"]),
        _production_requests(requests),
    )
    expected_by_id = {
        value["request_id"]: (Decimal(value["started_at"]), Decimal(value["completed_at"]))
        for value in benchmark["expected"]
    }
    for visit, (started_at, completed_at) in zip(
        production.visits, analytical, strict=True,
    ):
        expected_start, expected_completion = expected_by_id[visit.request_id]
        assert abs(started_at - expected_start) <= tolerance
        assert abs(completed_at - expected_completion) <= tolerance
        assert abs(visit.started_at - started_at) <= tolerance
        assert abs(visit.completed_at - completed_at) <= tolerance


def test_frozen_reference_fixtures_match_production_scheduler_exactly() -> None:
    config = yaml.safe_load(VALIDATION_CONFIG.read_text(encoding="utf-8"))
    for fixture in config["reference_fixtures"]:
        requests = _reference_requests(fixture["requests"])
        cutoff = Decimal(fixture["administrative_cutoff"])
        production = schedule_service_queue(
            ServiceQueueConfig(fixture["fixture_id"], fixture["capacity"]),
            _production_requests(requests),
            cutoff,
        )
        reference = run_reference_fifo(
            requests,
            capacity=fixture["capacity"],
            administrative_cutoff=cutoff,
        )
        _assert_differential_equal(production, reference)


def test_reference_simulator_matches_every_kernel_service_resource() -> None:
    config = yaml.safe_load(SMOKE_CONFIG.read_text(encoding="utf-8"))
    overlay_values = config["overlay"]
    input_overlay = StochasticInputOverlay(**{
        key: value if key in {"overlay_id", "provenance"} else Decimal(str(value))
        for key, value in overlay_values.items()
    })
    cohort = generate_stochastic_cohort(StochasticCohortSpec(
        scenario_id=config["scenario_id"],
        seed_id=config["seed_id"],
        case_ids=tuple(f"CASE-{index:04d}" for index in range(1, config["cohort_size"] + 1)),
        overlay=input_overlay,
    ))
    observed_nonempty_resources: set[str] = set()
    for policy_id in config["policy_ids"]:
        compiled = compile_configuration(
            configuration_id=f"REFERENCE-{policy_id}",
            process=stochastic_process(),
            policy=policy(policy_id),
            overlay=input_overlay.to_compilation_overlay(),
            evaluation_spec_id="REFERENCE-DIFFERENTIAL@1",
        )
        run = run_engagement_stage(cohort, compiled)
        queues = {
            "assistance": run.assistance_queue,
            "review": run.review_queue,
            "recovery": run.recovery_queue,
            "reassessment": run.reassessment_queue,
        }
        for resource_id, queue in queues.items():
            if queue.visits:
                observed_nonempty_resources.add(resource_id)
            requests = tuple(
                ReferenceRequest(
                    request_id=visit.request_id,
                    case_id=visit.case_id,
                    queued_at=visit.queued_at,
                    service_time=visit.service_time,
                    deadline=visit.deadline,
                )
                for visit in queue.visits
            )
            reference = run_reference_fifo(
                requests,
                capacity=queue.config.capacity,
                administrative_cutoff=input_overlay.administrative_cutoff,
            )
            _assert_differential_equal(queue, reference)
    assert observed_nonempty_resources == {
        "assistance", "review", "recovery", "reassessment",
    }


def test_limiting_queue_cases_are_exact() -> None:
    assert run_reference_fifo((), capacity=1) == ()
    requests = (
        ReferenceRequest("R1", "C1", Decimal(0), Decimal(0), Decimal("1000000")),
        ReferenceRequest("R2", "C2", Decimal(1), Decimal(0), Decimal("1000000")),
        ReferenceRequest("R3", "C3", Decimal(1), Decimal(0), Decimal("1000000")),
    )
    production = schedule_service_queue(
        ServiceQueueConfig("LIMIT", len(requests)),
        _production_requests(requests),
    )
    assert all(visit.started_at == visit.queued_at for visit in production.visits)
    assert all(visit.completed_at == visit.queued_at for visit in production.visits)
    assert all(visit.completed_by_deadline for visit in production.visits)
    _assert_differential_equal(
        production,
        run_reference_fifo(requests, capacity=len(requests)),
    )


def test_complete_evidence_and_universal_response_remove_unsupported_progression() -> None:
    config = yaml.safe_load(SMOKE_CONFIG.read_text(encoding="utf-8"))
    values = dict(config["overlay"])
    values.update({
        "initiation_window": "0",
        "notice_delivery_probability": "1",
        "administrative_access_probability": "1",
        "comprehension_probability": "1",
        "record_availability_probability": "1",
        "response_effort_limit": "1",
        "review_capacity": "3",
        "review_service_time": "0",
        "administrative_cutoff": "1000",
    })
    input_overlay = StochasticInputOverlay(**{
        key: value if key in {"overlay_id", "provenance"} else Decimal(str(value))
        for key, value in values.items()
    })
    cohort = generate_stochastic_cohort(StochasticCohortSpec(
        scenario_id="LIMIT-COMPLETE-EVIDENCE",
        seed_id="LIMIT-COMPLETE-EVIDENCE-SEED",
        case_ids=("C1", "C2", "C3"),
        overlay=input_overlay,
    ))
    for policy_id in config["policy_ids"]:
        compiled = compile_configuration(
            configuration_id=f"LIMIT-{policy_id}",
            process=stochastic_process(),
            policy=policy(policy_id),
            overlay=input_overlay.to_compilation_overlay(),
            evaluation_spec_id="LIMITING-CASE@1",
        )
        run = run_engagement_stage(cohort, compiled)
        assert run.telemetry.response_count == len(cohort.cases)
        assert run.telemetry.adequate_response_evidence_count == len(cohort.cases)
        assert run.telemetry.unsupported_progression_count == 0
        assert run.telemetry.unsupported_exposure_count == 0
