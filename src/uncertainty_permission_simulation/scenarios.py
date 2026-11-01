"""Constrained, case-neutral scenario generation for pilot and confirmatory runs."""

from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from itertools import product
from typing import Iterable, Mapping

from .random_streams import normalized_decimal
from .schemas import ContractError
from .simulator import StochasticInputOverlay


LOAD_LEVELS = (Decimal("0.6"), Decimal("0.95"), Decimal("1.2"))
MISSING_EVIDENCE_LEVELS = (Decimal("0.10"), Decimal("0.30"), Decimal("0.50"))
ACCESS_BARRIER_LEVELS = (Decimal("0.10"), Decimal("0.30"), Decimal("0.50"))
RETRIEVABILITY_LEVELS = ("low", "high")
STAFF_ACCESS_LEVELS = ("partial", "complete")


@dataclass(frozen=True, order=True)
class ScenarioFactors:
    load: Decimal
    missing_evidence: Decimal
    access_barrier: Decimal
    retrievability: str
    staff_access: str

    def __post_init__(self) -> None:
        if self.load not in LOAD_LEVELS:
            raise ContractError("SCENARIO_FACTOR_INVALID", f"unsupported load level {self.load}")
        if self.missing_evidence not in MISSING_EVIDENCE_LEVELS:
            raise ContractError(
                "SCENARIO_FACTOR_INVALID",
                f"unsupported missing-evidence level {self.missing_evidence}",
            )
        if self.access_barrier not in ACCESS_BARRIER_LEVELS:
            raise ContractError(
                "SCENARIO_FACTOR_INVALID",
                f"unsupported access-barrier level {self.access_barrier}",
            )
        if self.retrievability not in RETRIEVABILITY_LEVELS:
            raise ContractError(
                "SCENARIO_FACTOR_INVALID",
                f"unsupported retrievability level {self.retrievability}",
            )
        if self.staff_access not in STAFF_ACCESS_LEVELS:
            raise ContractError(
                "SCENARIO_FACTOR_INVALID",
                f"unsupported staff-access level {self.staff_access}",
            )

    @property
    def scenario_id(self) -> str:
        return (
            f"CORE-L{normalized_decimal(self.load).replace('.', 'P')}"
            f"-M{normalized_decimal(self.missing_evidence).replace('.', 'P')}"
            f"-A{normalized_decimal(self.access_barrier).replace('.', 'P')}"
            f"-R{self.retrievability.upper()}-S{self.staff_access.upper()}"
        )

    def canonical_value(self) -> dict[str, str]:
        return {
            "load": normalized_decimal(self.load),
            "missing_evidence": normalized_decimal(self.missing_evidence),
            "access_barrier": normalized_decimal(self.access_barrier),
            "retrievability": self.retrievability,
            "staff_access": self.staff_access,
        }

    def level_tokens(self) -> tuple[str, ...]:
        values = self.canonical_value()
        return tuple(f"{key}={values[key]}" for key in sorted(values))


@dataclass(frozen=True)
class ScenarioFamily:
    family_id: str
    factors: ScenarioFactors
    overlay: StochasticInputOverlay
    validity_status: str = "valid"
    invalid_reason: str | None = None

    def canonical_value(self) -> dict[str, object]:
        return {
            "family_id": self.family_id,
            "factors": self.factors.canonical_value(),
            "overlay": self.overlay.canonical_value(),
            "validity_status": self.validity_status,
            "invalid_reason": self.invalid_reason,
        }


def overlay_from_mapping(values: Mapping[str, object]) -> StochasticInputOverlay:
    """Build the closed overlay type from YAML-safe scalar values."""

    string_fields = {"overlay_id", "provenance"}
    expected = set(StochasticInputOverlay.__dataclass_fields__)
    missing = expected - set(values)
    unknown = set(values) - expected
    if missing or unknown:
        raise ContractError(
            "SCENARIO_CONFIGURATION_INCOMPLETE",
            f"overlay fields missing={sorted(missing)} unknown={sorted(unknown)}",
        )
    converted = {
        key: value if key in string_fields else Decimal(str(value))
        for key, value in values.items()
    }
    return StochasticInputOverlay(**converted)  # type: ignore[arg-type]


def core_factor_grid() -> tuple[ScenarioFactors, ...]:
    result = tuple(
        ScenarioFactors(*values)
        for values in product(
            LOAD_LEVELS,
            MISSING_EVIDENCE_LEVELS,
            ACCESS_BARRIER_LEVELS,
            RETRIEVABILITY_LEVELS,
            STAFF_ACCESS_LEVELS,
        )
    )
    if len(result) != 108 or len({item.scenario_id for item in result}) != 108:
        raise ContractError("SCENARIO_GRID_INVALID", "core factor grid must contain 108 unique families")
    return result


def _pair_tokens(factors: ScenarioFactors) -> frozenset[str]:
    levels = factors.level_tokens()
    return frozenset(
        f"{levels[left]}|{levels[right]}"
        for left in range(len(levels))
        for right in range(left + 1, len(levels))
    )


def development_factor_subset(count: int = 15) -> tuple[ScenarioFactors, ...]:
    """Greedy pairwise-coverage subset selected without outcome inspection."""

    if not isinstance(count, int) or isinstance(count, bool) or not 12 <= count <= 18:
        raise ContractError("SCENARIO_PILOT_SIZE_INVALID", "development subset must contain 12-18 families")
    candidates = list(core_factor_grid())
    selected: list[ScenarioFactors] = []
    covered_levels: set[str] = set()
    covered_pairs: set[str] = set()
    while len(selected) < count:
        def score(item: ScenarioFactors) -> tuple[int, int, int, str]:
            levels = set(item.level_tokens())
            pairs = set(_pair_tokens(item))
            minimum_distance = min(
                (
                    sum(a != b for a, b in zip(item.level_tokens(), prior.level_tokens(), strict=True))
                    for prior in selected
                ),
                default=5,
            )
            return (
                len(pairs - covered_pairs),
                len(levels - covered_levels),
                minimum_distance,
                item.scenario_id,
            )

        chosen = max(candidates, key=score)
        selected.append(chosen)
        candidates.remove(chosen)
        covered_levels.update(chosen.level_tokens())
        covered_pairs.update(_pair_tokens(chosen))
    return tuple(sorted(selected, key=lambda item: item.scenario_id))


def _probability(value: Decimal, field_name: str) -> Decimal:
    if not Decimal(0) <= value <= Decimal(1):
        raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must lie in [0, 1]")
    return value


def materialize_family(
    factors: ScenarioFactors,
    base_overlay: StochasticInputOverlay,
    cohort_size: int,
) -> ScenarioFamily:
    """Translate declared factors into a complete, visibly stylized overlay."""

    if not isinstance(cohort_size, int) or isinstance(cohort_size, bool) or cohort_size <= 0:
        raise ContractError("SCENARIO_PARAMETER_INVALID", "cohort_size must be a positive integer")
    review_capacity = int(base_overlay.review_capacity)
    if review_capacity <= 0:
        raise ContractError("SCENARIO_PARAMETER_INVALID", "review capacity must be positive")
    staff_multiplier = Decimal("1.5") if factors.staff_access == "partial" else Decimal(1)
    review_service_time = base_overlay.review_service_time * staff_multiplier
    with localcontext() as context:
        context.prec = 50
        # Service times are uniform draws scaled by review_service_time, so E[S] = scale / 2.
        initiation_window = (
            Decimal(cohort_size) * review_service_time
            / (Decimal(2) * Decimal(review_capacity) * factors.load)
        )
    retrievability = Decimal("0.35") if factors.retrievability == "low" else Decimal("0.85")
    access_probability = _probability(Decimal(1) - factors.access_barrier, "administrative_access_probability")
    notice_probability = _probability(Decimal(1) - factors.access_barrier / Decimal(4), "notice_delivery_probability")
    comprehension_probability = _probability(Decimal(1) - factors.access_barrier / Decimal(2), "comprehension_probability")
    overlay_id = f"{factors.scenario_id}-OVERLAY@1"
    overlay = replace(
        base_overlay,
        overlay_id=overlay_id,
        initiation_window=initiation_window,
        record_availability_probability=Decimal(1) - factors.missing_evidence,
        administrative_access_probability=access_probability,
        notice_delivery_probability=notice_probability,
        comprehension_probability=comprehension_probability,
        evidence_retrieval_success_probability=retrievability,
        review_service_time=review_service_time,
    )
    if overlay.administrative_cutoff <= overlay.initiation_window + overlay.response_deadline:
        return ScenarioFamily(
            factors.scenario_id,
            factors,
            overlay,
            "invalid",
            "administrative cutoff does not permit any post-response observation window",
        )
    return ScenarioFamily(factors.scenario_id, factors, overlay)


def materialize_families(
    factors: Iterable[ScenarioFactors],
    base_overlay: StochasticInputOverlay,
    cohort_size: int,
) -> tuple[ScenarioFamily, ...]:
    families = tuple(materialize_family(item, base_overlay, cohort_size) for item in factors)
    if len({family.family_id for family in families}) != len(families):
        raise ContractError("SCENARIO_GRID_INVALID", "scenario family IDs must be unique")
    return families
