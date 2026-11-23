from copy import deepcopy

import pytest

from uncertainty_permission_simulation.confirmatory import _designed_grid_summaries
from uncertainty_permission_simulation.experiments import (
    PRIMARY_METRICS,
    _cluster_jackknife_ratio,
    _paired_estimates,
    _summarize_cells,
    _validate_metric_row,
)
from uncertainty_permission_simulation.scenarios import core_factor_grid
from uncertainty_permission_simulation.schemas import ContractError


def _row(*, replication: int = 1, policy_id: str = "GENERIC") -> dict[str, object]:
    return {
        "family_id": "FAMILY-A",
        "load": "0.95",
        "missing_evidence": "0.30",
        "access_barrier": "0.30",
        "retrievability": "high",
        "staff_access": "complete",
        "replication": replication,
        "policy_id": policy_id,
        "case_count": 10,
        "event_count": 20,
        "cohort_hash": f"COHORT-{replication}",
        "event_hash": f"EVENT-{policy_id}-{replication}",
        "review_request_count": 0,
        "review_request_rate": 0.0,
        "timely_review_count": 0,
        "timeout_activation_count": 0,
        "gate_applicable_count": 0,
        "gate_safe_count": 0,
        "supported_progression_count": 4,
        "unsupported_progression_count": 1,
        "evidence_only_failure_count": 0,
        "authorization_only_failure_count": 0,
        "joint_evidence_authorization_failure_count": 1,
        "evidentially_unsupported_progression_count": 1,
        "unauthorized_progression_count": 1,
        "adequate_response_evidence_count": 4,
        "retrieval_request_count": 6,
        "retrieved_evidence_count": 1,
        "unresolved_after_acquisition_count": 5,
        "evidence_requested_count": 2,
        "held_count": 1,
        "pre_action_open_count": 2,
        "unresolved_nonprogression_count": 5,
        "supported_recovery_entry_count": 3,
        "unsupported_recovery_entry_count": 1,
        "no_recovery_entry_count": 6,
        "timeout_activation_rate": 0.0,
        "conditional_timely_review_rate": None,
        "conditional_gate_safety_rate": None,
        "supported_progression_rate": 0.4,
        "unsupported_progression_rate": 0.1,
        "evidence_only_failure_rate": 0.0,
        "authorization_only_failure_rate": 0.0,
        "joint_evidence_authorization_failure_rate": 0.1,
        "evidentially_unsupported_progression_rate": 0.1,
        "unauthorized_progression_rate": 0.1,
        "adequate_response_evidence_rate": 0.4,
        "retrieval_request_rate": 0.6,
        "retrieved_evidence_rate": 0.1,
        "unresolved_after_acquisition_rate": 0.5,
        "evidence_requested_rate": 0.2,
        "held_rate": 0.1,
        "pre_action_open_rate": 0.2,
        "unresolved_nonprogression_rate": 0.5,
        "supported_recovery_entry_rate": 0.3,
        "unsupported_recovery_entry_rate": 0.1,
        "no_recovery_entry_rate": 0.6,
        "recipient_burden_rate": 0.2,
        "agency_workload_rate": 0.3,
        "censoring_reason_counts": {"evidence_pending": 2},
        "review_mean_wait_time": 0.0,
        "correction_mean_exposure_time": 0.0,
    }


def _u3_row(*, replication: int = 1) -> dict[str, object]:
    row = _row(replication=replication, policy_id="U3")
    row.update({
        "review_request_count": 6,
        "review_request_rate": 0.6,
        "timely_review_count": 2,
        "timeout_activation_count": 4,
        "timeout_activation_rate": 0.4,
        "gate_applicable_count": 6,
        "gate_safe_count": 6,
        "conditional_timely_review_rate": 2 / 6,
        "conditional_gate_safety_rate": 1.0,
        "unsupported_progression_count": 0,
        "unsupported_progression_rate": 0.0,
        "joint_evidence_authorization_failure_count": 0,
        "joint_evidence_authorization_failure_rate": 0.0,
        "evidentially_unsupported_progression_count": 0,
        "evidentially_unsupported_progression_rate": 0.0,
        "unauthorized_progression_count": 0,
        "unauthorized_progression_rate": 0.0,
        "adequate_response_evidence_count": 3,
        "adequate_response_evidence_rate": 0.3,
        "retrieved_evidence_count": 1,
        "retrieved_evidence_rate": 0.1,
        "unresolved_after_acquisition_count": 6,
        "unresolved_after_acquisition_rate": 0.6,
        "pre_action_open_count": 3,
        "pre_action_open_rate": 0.3,
        "unresolved_nonprogression_count": 6,
        "unresolved_nonprogression_rate": 0.6,
        "unsupported_recovery_entry_count": 0,
        "unsupported_recovery_entry_rate": 0.0,
        "no_recovery_entry_count": 7,
        "no_recovery_entry_rate": 0.7,
    })
    return row


def test_zero_review_requests_are_null_not_zero() -> None:
    row = _row()
    _validate_metric_row(row)
    summary = _cluster_jackknife_ratio(
        [row], "timely_review_count", "review_request_count"
    )
    assert summary == {
        "numerator_count": 0,
        "denominator_count": 0,
        "zero_denominator_replications": 1,
        "rate": None,
        "cluster_jackknife_mcse": None,
        "cluster_count": 1,
    }


def test_u3_stage_accounting_conserves_cases_and_review_entry() -> None:
    row = _u3_row()
    _validate_metric_row(row)
    assert (
        row["adequate_response_evidence_count"]
        + row["retrieved_evidence_count"]
        + row["unresolved_after_acquisition_count"]
        == row["case_count"]
    )
    assert row["unresolved_after_acquisition_count"] == row["review_request_count"]


@pytest.mark.parametrize(
    ("field", "replacement", "diagnostic"),
    (
        ("adequate_response_evidence_count", 2, "METRIC_ACQUISITION_PARTITION_INVALID"),
        ("review_request_count", 5, "METRIC_U3_REVIEW_STAGE_INVALID"),
    ),
)
def test_u3_stage_drift_fails_closed(
    field: str,
    replacement: object,
    diagnostic: str,
) -> None:
    row = _u3_row()
    row[field] = replacement
    if field == "review_request_count":
        row["review_request_rate"] = 0.5
        row["timeout_activation_count"] = 3
        row["timeout_activation_rate"] = 0.3
    with pytest.raises(ContractError, match=diagnostic):
        _validate_metric_row(row)


def test_conditional_review_uses_ratio_of_sums_and_replication_jackknife() -> None:
    first = _row(replication=1)
    first.update({
        "review_request_count": 1,
        "review_request_rate": 0.1,
        "timely_review_count": 1,
        "timeout_activation_count": 0,
        "gate_applicable_count": 1,
        "gate_safe_count": 1,
        "conditional_timely_review_rate": 1.0,
        "conditional_gate_safety_rate": 1.0,
    })
    second = _row(replication=2)
    second.update({
        "review_request_count": 9,
        "review_request_rate": 0.9,
        "timely_review_count": 0,
        "timeout_activation_count": 9,
        "gate_applicable_count": 9,
        "gate_safe_count": 0,
        "timeout_activation_rate": 0.9,
        "conditional_timely_review_rate": 0.0,
        "conditional_gate_safety_rate": 0.0,
    })
    for row in (first, second):
        _validate_metric_row(row)
    summary = _cluster_jackknife_ratio(
        [first, second], "timely_review_count", "review_request_count"
    )
    assert summary["rate"] == pytest.approx(0.1)
    assert summary["rate"] != pytest.approx(0.5)
    assert summary["cluster_jackknife_mcse"] == pytest.approx(0.5)


def test_decision_and_recovery_partitions_include_open_cases() -> None:
    row = _row()
    _validate_metric_row(row)
    assert sum(row[name] for name in (
        "supported_progression_count",
        "unsupported_progression_count",
        "evidence_requested_count",
        "held_count",
        "pre_action_open_count",
    )) == row["case_count"]
    assert row["unresolved_nonprogression_count"] == 5
    assert sum(row[name] for name in (
        "supported_recovery_entry_count",
        "unsupported_recovery_entry_count",
        "no_recovery_entry_count",
    )) == row["case_count"]


@pytest.mark.parametrize(
    ("field", "replacement", "diagnostic"),
    (
        ("pre_action_open_count", 1, "METRIC_DECISION_PARTITION_INVALID"),
        ("supported_progression_count", 5, "METRIC_DECISION_PARTITION_INVALID"),
        ("unresolved_nonprogression_count", 4, "METRIC_UNRESOLVED_COUNT_INVALID"),
        ("no_recovery_entry_count", 5, "METRIC_RECOVERY_PARTITION_INVALID"),
        ("timely_review_count", 1, "METRIC_NUMERATOR_EXCEEDS_DENOMINATOR"),
        ("conditional_timely_review_rate", 0.0, "METRIC_NULLABILITY_INVALID"),
        ("evidence_only_failure_count", 1, "METRIC_PROGRESSION_FAILURE_PARTITION_INVALID"),
        ("evidentially_unsupported_progression_count", 0, "METRIC_EVIDENCE_FAILURE_UNION_INVALID"),
        ("unauthorized_progression_count", 0, "METRIC_AUTHORIZATION_FAILURE_UNION_INVALID"),
        ("retrieved_evidence_count", 7, "METRIC_RETRIEVAL_NUMERATOR_INVALID"),
        ("unresolved_after_acquisition_count", 4, "METRIC_ACQUISITION_PARTITION_INVALID"),
    ),
)
def test_adversarial_metric_rows_fail_closed(
    field: str,
    replacement: object,
    diagnostic: str,
) -> None:
    row = _row()
    row[field] = replacement
    with pytest.raises(ContractError, match=diagnostic):
        _validate_metric_row(row)


def test_orphaned_recovery_entry_fails_closed() -> None:
    row = _row()
    row["supported_recovery_entry_count"] = 5
    row["no_recovery_entry_count"] = 4
    row["supported_recovery_entry_rate"] = 0.5
    row["no_recovery_entry_rate"] = 0.4
    with pytest.raises(ContractError, match="METRIC_RECOVERY_ENTRY_ORPHANED"):
        _validate_metric_row(row)


def test_summaries_are_order_invariant_and_ignore_irrelevant_fields() -> None:
    first = _row(replication=1)
    second = _row(replication=2)
    baseline = _summarize_cells([first, second])
    first_with_irrelevant = deepcopy(first)
    first_with_irrelevant["irrelevant_event_annotation"] = "ignored"
    reordered = _summarize_cells([second, first_with_irrelevant])
    assert baseline == reordered


def test_completed_review_can_leave_the_case_unresolved() -> None:
    row = _row()
    row.update({
        "review_request_count": 2,
        "review_request_rate": 0.2,
        "timely_review_count": 2,
        "timeout_activation_count": 0,
        "gate_applicable_count": 2,
        "gate_safe_count": 2,
        "conditional_timely_review_rate": 1.0,
        "conditional_gate_safety_rate": 1.0,
    })
    _validate_metric_row(row)
    assert row["evidence_requested_count"] == 2
    assert row["unresolved_nonprogression_count"] == 5


def test_primary_analysis_does_not_repeat_accounting_complements() -> None:
    rows = []
    for replication in (1, 2):
        rows.extend((
            _row(replication=replication, policy_id="U0"),
            _u3_row(replication=replication),
        ))
    pairs = _paired_estimates(rows)
    assert PRIMARY_METRICS == (
        "timeout_activation_rate",
        "unresolved_nonprogression_rate",
    )
    assert {(item["contrast_id"], item["metric"]) for item in pairs} == {
        ("U3-minus-U0", "unresolved_nonprogression_rate")
    }


def test_semantic_policy_relabeling_changes_identity_not_values() -> None:
    original = _summarize_cells([_row(policy_id="INFORMATION-FIRST")])[0]
    renamed = _summarize_cells([_row(policy_id="RENAMED-INFORMATION-FIRST")])[0]
    original.pop("policy_id")
    renamed.pop("policy_id")
    assert original == renamed


def test_duplicating_equivalent_replications_preserves_rates() -> None:
    single = _summarize_cells([_row(replication=1)])[0]
    duplicated = _summarize_cells([_row(replication=1), _row(replication=2)])[0]
    for metric in (
        "timeout_activation_rate",
        "unresolved_nonprogression_rate",
        "supported_recovery_entry_rate",
    ):
        assert single[metric] == duplicated[metric]


def test_prespecified_factor_margins_have_declared_balanced_counts() -> None:
    cells: list[dict[str, object]] = []
    for factors in core_factor_grid():
        canonical = factors.canonical_value()
        cells.append({
            "family_id": factors.scenario_id,
            "policy_id": "U2C",
            "factors": canonical,
            "timeout_activation_rate": float(factors.load) / 2,
            "timeout_activation_rate_mcse": 0.01,
        })
        cells.append({
            "family_id": factors.scenario_id,
            "policy_id": "U2O",
            "factors": canonical,
            "unsupported_progression_rate": 0.4,
            "evidence_only_failure_rate": 0.1,
            "authorization_only_failure_rate": 0.1,
            "joint_evidence_authorization_failure_rate": 0.2,
            "evidentially_unsupported_progression_rate": 0.3,
            "unauthorized_progression_rate": 0.3,
        })
        cells.append({
            "family_id": factors.scenario_id,
            "policy_id": "U3",
            "factors": canonical,
            "unresolved_nonprogression_rate": float(factors.access_barrier),
            "unresolved_nonprogression_rate_mcse": 0.01,
            "adequate_response_evidence_rate": 0.5,
            "retrieval_request_rate": 0.5,
            "retrieved_evidence_rate": 0.3,
            "unresolved_after_acquisition_rate": 0.2,
            "review_request_rate": 0.2,
            "evidence_requested_rate": 0.15,
            "held_rate": 0.05,
            "pre_action_open_rate": 0.0,
            "supported_progression_rate": 0.8,
        })
    summaries = _designed_grid_summaries(cells)
    assert [level["cell_count"] for level in summaries["u2c_timeout_by_load"]["levels"]] == [36, 36, 36]
    assert [level["cell_count"] for level in summaries["u3_unresolved_by_access_barrier"]["levels"]] == [36, 36, 36]
    assert [level["cell_count"] for level in summaries["u3_unresolved_by_retrievability"]["levels"]] == [54, 54]
    assert [level["cell_count"] for level in summaries["u3_unresolved_by_staff_access"]["levels"]] == [54, 54]
    assert summaries["u2o_progression_failure_partition"]["estimates"] == {
        "unsupported_progression_rate": pytest.approx(0.4),
        "evidence_only_failure_rate": pytest.approx(0.1),
        "authorization_only_failure_rate": pytest.approx(0.1),
        "joint_evidence_authorization_failure_rate": pytest.approx(0.2),
        "evidentially_unsupported_progression_rate": pytest.approx(0.3),
        "unauthorized_progression_rate": pytest.approx(0.3),
    }
    assert summaries["u3_evidence_stage_accounting"]["claim_boundary"].endswith(
        "not independent component effects"
    )
