"""Finite-cohort stochastic substrate built from policy-neutral keyed latents."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, localcontext
from hashlib import sha256
import json
from typing import Literal

from .random_streams import DRAW_FAMILY_IDS, KeyedDraw, KeyedRandomStream, normalized_decimal
from .schemas import ContractError


@dataclass(frozen=True)
class StochasticInputOverlay:
    overlay_id: str
    provenance: Literal["stylized", "sensitivity"]
    initiation_window: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.overlay_id, str) or not self.overlay_id:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "overlay_id must be nonempty")
        if self.provenance not in {"stylized", "sensitivity"}:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "stochastic inputs require stylized or sensitivity provenance")
        if not isinstance(self.initiation_window, Decimal) or not self.initiation_window.is_finite() or self.initiation_window < 0:
            raise ContractError("SCENARIO_PARAMETER_INVALID", "initiation_window must be finite and nonnegative")


@dataclass(frozen=True)
class StochasticCohortSpec:
    scenario_id: str
    seed_id: str
    case_ids: tuple[str, ...]
    overlay: StochasticInputOverlay

    def __post_init__(self) -> None:
        if any(not isinstance(value, str) or not value for value in (self.scenario_id, self.seed_id)):
            raise ContractError("SCENARIO_INVALID", "scenario and seed IDs must be nonempty")
        if not isinstance(self.case_ids, tuple) or not self.case_ids or any(not isinstance(case_id, str) or not case_id for case_id in self.case_ids):
            raise ContractError("SCENARIO_INVALID", "finite cohort requires nonempty case IDs")
        if len(self.case_ids) != len(set(self.case_ids)):
            raise ContractError("SCENARIO_INVALID", "finite cohort case IDs must be unique")
        if not isinstance(self.overlay, StochasticInputOverlay):
            raise ContractError("SCENARIO_PARAMETER_INVALID", "stochastic cohort requires a typed input overlay")


@dataclass(frozen=True)
class StochasticCase:
    case_id: str
    arrival_time: Decimal
    keyed_draws: tuple[KeyedDraw, ...]

    @property
    def draw_map(self) -> dict[tuple[str, int], Decimal]:
        return {
            (draw.key.event_family_id, draw.key.draw_index): draw.unit_interval_value
            for draw in self.keyed_draws
        }

    @property
    def draw_hash(self) -> str:
        values = [draw.content_hash for draw in self.keyed_draws]
        return sha256(json.dumps(values, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class RunTelemetry:
    case_count: int
    keyed_draw_count: int
    draw_family_counts: tuple[tuple[str, int], ...]
    duplicate_draw_key_count: int
    cohort_hash: str


@dataclass(frozen=True)
class StochasticCohort:
    scenario_id: str
    overlay_id: str
    seed_id: str
    cases: tuple[StochasticCase, ...]
    telemetry: RunTelemetry


def _cohort_hash(spec: StochasticCohortSpec, cases: tuple[StochasticCase, ...]) -> str:
    value = {
        "case_draw_hashes": {case.case_id: case.draw_hash for case in cases},
        "initiation_window": normalized_decimal(spec.overlay.initiation_window),
        "overlay_id": spec.overlay.overlay_id,
        "overlay_provenance": spec.overlay.provenance,
        "scenario_id": spec.scenario_id,
        "seed_id": spec.seed_id,
    }
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def generate_stochastic_cohort(spec: StochasticCohortSpec) -> StochasticCohort:
    """Generate shared exogenous latents; policy mappings consume them later."""

    stream = KeyedRandomStream(spec.seed_id)
    cases: list[StochasticCase] = []
    for case_id in sorted(spec.case_ids):
        draws = tuple(stream.draw(case_id, family_id) for family_id in sorted(DRAW_FAMILY_IDS))
        initiation = next(draw for draw in draws if draw.key.event_family_id == "initiation")
        with localcontext() as context:
            context.prec = 50
            arrival_time = initiation.unit_interval_value * spec.overlay.initiation_window
        cases.append(StochasticCase(case_id, arrival_time, draws))
    frozen_cases = tuple(cases)
    all_draws = tuple(draw for case in frozen_cases for draw in case.keyed_draws)
    keys = [draw.key for draw in all_draws]
    family_counts = Counter(draw.key.event_family_id for draw in all_draws)
    cohort_hash = _cohort_hash(spec, frozen_cases)
    telemetry = RunTelemetry(
        case_count=len(frozen_cases),
        keyed_draw_count=len(all_draws),
        draw_family_counts=tuple(sorted(family_counts.items())),
        duplicate_draw_key_count=len(keys) - len(set(keys)),
        cohort_hash=cohort_hash,
    )
    if telemetry.duplicate_draw_key_count:
        raise ContractError("RANDOM_DRAW_KEY_INVALID", "duplicate keyed draw identity in cohort")
    return StochasticCohort(spec.scenario_id, spec.overlay.overlay_id, spec.seed_id, frozen_cases, telemetry)
