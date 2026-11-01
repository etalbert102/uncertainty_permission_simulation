from decimal import Decimal

from uncertainty_permission_simulation.configuration import compile_configuration
from uncertainty_permission_simulation.metrics import engagement_metrics
from uncertainty_permission_simulation.profiles import policy, stochastic_process
from uncertainty_permission_simulation.simulator import StochasticCohortSpec, StochasticInputOverlay, generate_stochastic_cohort, run_engagement_stage


def _run(policy_id: str):
    overlay = StochasticInputOverlay(
        overlay_id="METRIC-OVERLAY", provenance="stylized", initiation_window=Decimal("0"),
        notice_delay=Decimal("1"), response_deadline=Decimal("21"),
        review_capacity=Decimal("1"), review_service_time=Decimal("30"), review_service_window=Decimal("14"),
        extension_duration=Decimal("7"),
        notice_delivery_probability=Decimal("1"), administrative_access_probability=Decimal("1"),
        comprehension_probability=Decimal("1"), record_availability_probability=Decimal("1"),
        response_effort_limit=Decimal("1"), assistance_effort_bonus=Decimal("0"),
        extension_effort_bonus=Decimal("0"),
        extension_need_probability=Decimal("0"), evidence_retrieval_success_probability=Decimal("1"),
        evidence_retrieval_latency_scale=Decimal("0"),
    )
    cohort = generate_stochastic_cohort(StochasticCohortSpec(
        scenario_id="METRIC-SCENARIO", seed_id="METRIC-SEED",
        case_ids=("CASE-1", "CASE-2"), overlay=overlay,
    ))
    compiled = compile_configuration(
        configuration_id=f"METRIC-{policy_id}", process=stochastic_process(), policy=policy(policy_id),
        overlay=overlay.to_compilation_overlay(), evaluation_spec_id="METRIC-EVALUATION",
    )
    return run_engagement_stage(cohort, compiled)


def test_engagement_metrics_keep_dimensions_separate() -> None:
    metrics = engagement_metrics(_run("U2C"))
    assert metrics["case_count"] == 2
    assert metrics["response_count"] == 2
    assert metrics["adequate_response_evidence_count"] == 2
    assert metrics["review_queue_count"] == 2
    assert metrics["review_started_count"] == 2
    assert metrics["review_completed_count"] == 2
    assert metrics["timely_review_count"] + metrics["late_review_count"] == 2
    assert Decimal(metrics["timely_review_rate"]) + Decimal(metrics["late_review_rate"]) == Decimal(1)
    assert metrics["review_started_rate"] == "1"
    assert metrics["review_completed_rate"] == "1"
    assert metrics["action_count"] == 2
    assert metrics["action_rate"] == "1"
    assert metrics["progression_count"] + metrics["hold_count"] + metrics["request_evidence_action_count"] == 2
    assert metrics["supported_progression_count"] + metrics["unsupported_progression_count"] == metrics["progression_count"]
    assert metrics["evidentially_supported_progression_count"] + metrics["evidentially_unsupported_progression_count"] == metrics["progression_count"]
    assert metrics["gate_safe_count"] + metrics["gate_unsafe_count"] == metrics["gate_applicable_count"]
    assert Decimal(metrics["review_max_wait_time"]) >= Decimal(0)
    assert metrics["response_rate"] == "1"
    assert metrics["notice_failure_rate"] == "0"
    assert "score" not in metrics and "utility" not in metrics


def test_engagement_metrics_are_policy_specific_but_share_denominator() -> None:
    u1 = engagement_metrics(_run("U1"))
    u2c = engagement_metrics(_run("U2C"))
    assert u1["case_count"] == u2c["case_count"] == 2
    assert u1["review_queue_count"] == 0
    assert u1["review_mean_wait_time"] == "0"
    assert u1["progression_count"] == 2
    assert u1["supported_progression_count"] == 2
    assert u1["gate_applicable_count"] == 0
    assert u1["gate_safe_rate"] == "0"
    assert u2c["review_queue_count"] == 2
    assert u2c["gate_safe_rate"] == "1"
