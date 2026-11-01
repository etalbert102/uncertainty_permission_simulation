from dataclasses import replace
from decimal import Decimal

import pytest

from uncertainty_permission_simulation.random_streams import DRAW_FAMILY_IDS
from uncertainty_permission_simulation.schemas import ContractError
from uncertainty_permission_simulation.simulator import StochasticCohortSpec, StochasticInputOverlay, generate_stochastic_cohort


def spec(**updates: object) -> StochasticCohortSpec:
    base = StochasticCohortSpec(
        scenario_id="SCENARIO-1", seed_id="SEED-1", case_ids=("CASE-3", "CASE-1", "CASE-2"),
        overlay=StochasticInputOverlay("STYLIZED-OVERLAY-1", "stylized", Decimal("10")),
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
    overlay = StochasticInputOverlay("STYLIZED-OVERLAY-2", "stylized", Decimal("12.5"))
    cohort = generate_stochastic_cohort(spec(overlay=overlay))
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


@pytest.mark.parametrize(
    "overlay",
    (
        ("OVERLAY", "documented", Decimal("10")),
        ("OVERLAY", "stylized", Decimal("-1")),
        ("OVERLAY", "stylized", Decimal("NaN")),
        ("OVERLAY", "stylized", "10"),
    ),
)
def test_invalid_stochastic_overlay_values_are_rejected(overlay: tuple[object, object, object]) -> None:
    with pytest.raises(ContractError, match="SCENARIO_PARAMETER_INVALID"):
        StochasticInputOverlay(*overlay)
