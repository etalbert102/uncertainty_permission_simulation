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


def _row(*, replication: int = 1, policy_id: str = "U3") -> dict[str, object]:
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
        "timely_review_count": 0,
        "timeout_activation_count": 0,
        "gate_applicable_count": 0,
        "gate_safe_count": 0,
        "supported_progression_count": 4,
        "unsupported_progression_count": 1,
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


def test_conditional_review_uses_ratio_of_sums_and_replication_jackknife() -> None:
    first = _row(replication=1)
    first.update({
        "review_request_count": 1,
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
            _row(replication=replication, policy_id="U3"),
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
    original = _summarize_cells([_row(policy_id="U3")])[0]
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
        for policy_id, metric in (
            ("U2C", "timeout_activation_rate"),
            ("U3", "unresolved_nonprogression_rate"),
        ):
            cells.append({
                "family_id": factors.scenario_id,
                "policy_id": policy_id,
                "factors": canonical,
                metric: float(factors.load) / 2 if policy_id == "U2C" else float(factors.access_barrier),
                f"{metric}_mcse": 0.01,
            })
    summaries = _designed_grid_summaries(cells)
    assert [level["cell_count"] for level in summaries["u2c_timeout_by_load"]["levels"]] == [36, 36, 36]
    assert [level["cell_count"] for level in summaries["u3_unresolved_by_access_barrier"]["levels"]] == [36, 36, 36]
    assert [level["cell_count"] for level in summaries["u3_unresolved_by_retrievability"]["levels"]] == [54, 54]
    assert [level["cell_count"] for level in summaries["u3_unresolved_by_staff_access"]["levels"]] == [54, 54]
