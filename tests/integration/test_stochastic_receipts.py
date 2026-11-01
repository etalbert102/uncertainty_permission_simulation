from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path

import yaml

from uncertainty_permission_simulation.applications.robodebt import (
    load_early_stochastic_adapter,
    load_enhanced_adapter,
)
from uncertainty_permission_simulation.configuration import compile_configuration
from uncertainty_permission_simulation.metrics import engagement_metrics
from uncertainty_permission_simulation.profiles import policy, stochastic_process
from uncertainty_permission_simulation.random_streams import normalized_decimal
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
RECEIPT_PATH = ROOT / "data/golden_traces/slice2_stochastic_validation_v1.json"
SMOKE_PATH = ROOT / "experiments/configs/stochastic_smoke_v1.yaml"
APPLICATION_PATH = ROOT / "experiments/configs/application_validation_v1.yaml"
VALIDATION_PATH = ROOT / "experiments/configs/slice2_validation_v1.yaml"


def _hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _overlay(values: dict[str, object]) -> StochasticInputOverlay:
    return StochasticInputOverlay(**{
        key: value if key in {"overlay_id", "provenance"} else Decimal(str(value))
        for key, value in values.items()
    })


def _smoke_runs():
    config = yaml.safe_load(SMOKE_PATH.read_text(encoding="utf-8"))
    input_overlay = _overlay(config["overlay"])
    cohort = generate_stochastic_cohort(StochasticCohortSpec(
        scenario_id=config["scenario_id"],
        seed_id=config["seed_id"],
        case_ids=tuple(
            f"CASE-{index:04d}" for index in range(1, config["cohort_size"] + 1)
        ),
        overlay=input_overlay,
    ))
    runs = {
        policy_id: run_engagement_stage(
            cohort,
            compile_configuration(
                configuration_id=f"RECEIPT-{policy_id}",
                process=stochastic_process(),
                policy=policy(policy_id),
                overlay=input_overlay.to_compilation_overlay(),
                evaluation_spec_id="STOCHASTIC-RECEIPT@1",
            ),
        )
        for policy_id in config["policy_ids"]
    }
    return cohort, runs


def test_stored_receipt_inputs_and_replays_match_exactly() -> None:
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    for relative_path, expected_hash in receipt["config_hashes"].items():
        assert sha256((ROOT / relative_path).read_bytes()).hexdigest() == expected_hash

    cohort, runs = _smoke_runs()
    paired = receipt["paired_draw_receipt"]
    assert paired["comparison_status"] == "match"
    assert cohort.telemetry.cohort_hash == paired["cohort_hash"]
    actual_case_hashes = {case.case_id: case.draw_hash for case in cohort.cases}
    assert actual_case_hashes == paired["case_draw_hashes"]
    canary = paired["event_count_invariance_canary"]
    for policy_id in ("U1", "U3"):
        trace = next(
            trace for trace in runs[policy_id].traces
            if trace.case_id == canary["case_id"]
        )
        assert len(trace.events) == canary[f"{policy_id}_event_count"]
        assert trace.exogenous_draw_hash == canary["shared_draw_hash"]
    assert canary["U1_event_count"] != canary["U3_event_count"]

    for policy_id, expected in receipt["replay_receipts"].items():
        run = runs[policy_id]
        metric_hash = _hash(engagement_metrics(run))
        assert expected["comparison_status"] == "match"
        assert expected["expected_event_hash"] == expected["observed_event_hash"]
        assert expected["expected_metric_hash"] == expected["observed_metric_hash"]
        assert run.telemetry.event_hash == expected["expected_event_hash"]
        assert metric_hash == expected["expected_metric_hash"]

    replay = _smoke_runs()[1]
    assert {
        policy_id: (run.telemetry.event_hash, _hash(engagement_metrics(run)))
        for policy_id, run in replay.items()
    } == {
        policy_id: (run.telemetry.event_hash, _hash(engagement_metrics(run)))
        for policy_id, run in runs.items()
    }


def test_stochastic_golden_trace_hashes_and_milestones_match_exactly() -> None:
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    _, runs = _smoke_runs()
    assert {trace["policy_id"] for trace in receipt["golden_traces"]} == {
        "U0", "U1", "U2C", "U2O", "U3",
    }
    for expected in receipt["golden_traces"]:
        trace = next(
            trace for trace in runs[expected["policy_id"]].traces
            if trace.case_id == expected["case_id"]
        )
        assert trace.event_hash == expected["expected_trace_hash"]
        for milestone in expected["milestones"]:
            matches = tuple(
                event for event in trace.events
                if event.event_type_id == milestone["event_type_id"]
                and normalized_decimal(event.timestamp) == milestone["timestamp"]
                and all(
                    event.details.get(key) == value
                    for key, value in milestone["details"].items()
                )
            )
            assert len(matches) == 1, (
                expected["golden_trace_id"], milestone, matches,
            )


def test_stored_application_equivalence_receipts_match() -> None:
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    config = yaml.safe_load(APPLICATION_PATH.read_text(encoding="utf-8"))
    loaders = {
        "early": load_early_stochastic_adapter,
        "enhanced": load_enhanced_adapter,
    }
    for application_id, loader in loaders.items():
        application = config["applications"][application_id]
        values = dict(config["stylized_overlay"]) | application["documented_runtime_parameters"]
        input_overlay = _overlay(values)
        cohort = generate_stochastic_cohort(StochasticCohortSpec(
            scenario_id=f"APPLICATION-EQUIVALENCE-{application_id.upper()}",
            seed_id=config["seed_id"],
            case_ids=tuple(config["case_ids"]),
            overlay=input_overlay,
        ))
        process, _ = loader(ROOT / application["source_fixture"])
        application_configuration = compile_configuration(
            configuration_id=f"RECEIPT-APPLICATION-{application_id.upper()}",
            process=process,
            policy=policy(config["active_policy_id"]),
            overlay=input_overlay.to_compilation_overlay(
                exclude_slot_ids=frozenset({"response_deadline"}),
            ),
            evaluation_spec_id=config["evaluation_spec_id"],
            application_mapping_id=application["application_mapping_id"],
        )
        synthetic_configuration = compile_configuration(
            configuration_id=f"RECEIPT-SYNTHETIC-{application_id.upper()}",
            process=stochastic_process(),
            policy=policy(config["active_policy_id"]),
            overlay=input_overlay.to_compilation_overlay(),
            evaluation_spec_id=config["evaluation_spec_id"],
        )
        application_run = run_engagement_stage(cohort, application_configuration)
        synthetic_run = run_engagement_stage(cohort, synthetic_configuration)
        expected = receipt["application_equivalence_receipts"][application_id]
        assert expected["comparison_status"] == "match"
        assert application_run == synthetic_run
        assert application_run.telemetry.event_hash == expected["application_event_hash"]
        assert synthetic_run.telemetry.event_hash == expected["synthetic_event_hash"]
        assert _hash(engagement_metrics(application_run)) == expected["application_metric_hash"]
        assert _hash(engagement_metrics(synthetic_run)) == expected["synthetic_metric_hash"]


def test_stored_queue_validation_receipts_match() -> None:
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    config = yaml.safe_load(VALIDATION_PATH.read_text(encoding="utf-8"))
    analytical = config["analytical_benchmark"]
    analytical_requests = tuple(
        ReferenceRequest(
            request_id=value["request_id"], case_id=value["case_id"],
            queued_at=Decimal(value["queued_at"]),
            service_time=Decimal(value["service_time"]),
            deadline=Decimal(value["deadline"]),
        )
        for value in analytical["requests"]
    )
    analytical_result = analytical_dd1(analytical_requests)
    expected_times = tuple(
        (Decimal(value["started_at"]), Decimal(value["completed_at"]))
        for value in analytical["expected"]
    )
    assert analytical_result == expected_times
    production = schedule_service_queue(
        ServiceQueueConfig(analytical["benchmark_id"], analytical["capacity"]),
        tuple(
            ServiceRequest(
                request.request_id, request.case_id, request.queued_at,
                request.service_time, request.deadline,
            ) for request in analytical_requests
        ),
    )
    stored_analytical = receipt["queue_validation_receipts"]["analytical_DD1"]
    assert stored_analytical["comparison_status"] == "match"
    assert stored_analytical["absolute_time_tolerance"] == analytical["absolute_time_tolerance"]
    assert production.telemetry.schedule_hash == stored_analytical["production_schedule_hash"]

    for fixture in config["reference_fixtures"]:
        reference_requests = tuple(
            ReferenceRequest(
                request_id=value["request_id"], case_id=value["case_id"],
                queued_at=Decimal(value["queued_at"]),
                service_time=Decimal(value["service_time"]),
                deadline=Decimal(value["deadline"]),
            )
            for value in fixture["requests"]
        )
        production = schedule_service_queue(
            ServiceQueueConfig(fixture["fixture_id"], fixture["capacity"]),
            tuple(
                ServiceRequest(
                    request.request_id, request.case_id, request.queued_at,
                    request.service_time, request.deadline,
                ) for request in reference_requests
            ),
            Decimal(fixture["administrative_cutoff"]),
        )
        reference = run_reference_fifo(
            reference_requests,
            capacity=fixture["capacity"],
            administrative_cutoff=Decimal(fixture["administrative_cutoff"]),
        )
        assert tuple(
            (visit.started_at, visit.completed_at, visit.right_censored)
            for visit in production.visits
        ) == tuple(
            (visit.started_at, visit.completed_at, visit.right_censored)
            for visit in reference
        )
        receipt_id = "reference_" + fixture["fixture_id"].replace("-", "_")
        stored = receipt["queue_validation_receipts"][receipt_id]
        assert stored["comparison_status"] == "match"
        assert production.telemetry.schedule_hash == stored["production_schedule_hash"]
