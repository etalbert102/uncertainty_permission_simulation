from decimal import Decimal
from pathlib import Path

import yaml

from uncertainty_permission_simulation.scenarios import (
    ACCESS_BARRIER_LEVELS,
    LOAD_LEVELS,
    MISSING_EVIDENCE_LEVELS,
    RETRIEVABILITY_LEVELS,
    STAFF_ACCESS_LEVELS,
    core_factor_grid,
    development_factor_subset,
    materialize_family,
    overlay_from_mapping,
)


ROOT = Path(__file__).resolve().parents[2]


def _base_overlay():
    config = yaml.safe_load((ROOT / "experiments/configs/pilot_v1.yaml").read_text())
    return overlay_from_mapping(config["base_overlay"])


def test_core_grid_is_closed_and_unique() -> None:
    grid = core_factor_grid()
    assert len(grid) == 108
    assert len({item.scenario_id for item in grid}) == 108
    assert {item.load for item in grid} == set(LOAD_LEVELS)
    assert {item.missing_evidence for item in grid} == set(MISSING_EVIDENCE_LEVELS)
    assert {item.access_barrier for item in grid} == set(ACCESS_BARRIER_LEVELS)
    assert {item.retrievability for item in grid} == set(RETRIEVABILITY_LEVELS)
    assert {item.staff_access for item in grid} == set(STAFF_ACCESS_LEVELS)


def test_development_subset_is_stable_and_covers_every_factor_level() -> None:
    first = development_factor_subset()
    second = development_factor_subset()
    assert first == second
    assert len(first) == 15
    for index in range(5):
        assert {item.level_tokens()[index] for item in first} == {
            item.level_tokens()[index] for item in core_factor_grid()
        }


def test_materialization_maps_declared_factors_without_hidden_history() -> None:
    factors = next(
        item for item in core_factor_grid()
        if item.load == Decimal("1.2")
        and item.missing_evidence == Decimal("0.5")
        and item.access_barrier == Decimal("0.3")
        and item.retrievability == "low"
        and item.staff_access == "partial"
    )
    family = materialize_family(factors, _base_overlay(), 48)
    assert family.validity_status == "valid"
    assert family.overlay.record_availability_probability == Decimal("0.5")
    assert family.overlay.administrative_access_probability == Decimal("0.7")
    assert family.overlay.evidence_retrieval_success_probability == Decimal("0.35")
    assert family.overlay.review_service_time == Decimal("15")
    assert family.overlay.provenance == "stylized"
