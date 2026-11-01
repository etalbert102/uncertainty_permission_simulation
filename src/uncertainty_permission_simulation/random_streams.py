"""Order-independent keyed random draws for the stochastic simulator."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from hashlib import sha256
import json

from .schemas import ContractError, MANIFEST


ALGORITHM_ID = "UPS-SHA256-KEYED-UNIFORM"
ALGORITHM_VERSION = 1
DRAW_FAMILY_IDS = frozenset(MANIFEST["closed_draw_family_ids"])
_DENOMINATOR = Decimal((1 << 128) + 1)


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def normalized_decimal(value: Decimal) -> str:
    if not value.is_finite():
        raise ContractError("RANDOM_DRAW_KEY_INVALID", "draw value must be finite")
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return "0" if rendered in {"-0", ""} else rendered


@dataclass(frozen=True, order=True)
class DrawKey:
    case_id: str
    event_family_id: str
    draw_index: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.case_id, str) or not self.case_id:
            raise ContractError("RANDOM_DRAW_KEY_INVALID", "case_id must be nonempty")
        if not isinstance(self.event_family_id, str) or self.event_family_id not in DRAW_FAMILY_IDS:
            raise ContractError("RANDOM_DRAW_KEY_INVALID", f"unknown draw family {self.event_family_id}")
        if not isinstance(self.draw_index, int) or isinstance(self.draw_index, bool) or self.draw_index < 0:
            raise ContractError("RANDOM_DRAW_KEY_INVALID", "draw_index must be a nonnegative integer")

    def canonical_value(self) -> dict[str, object]:
        return {
            "case_id": self.case_id,
            "draw_index": self.draw_index,
            "event_family_id": self.event_family_id,
        }


@dataclass(frozen=True)
class KeyedDraw:
    keyed_draw_id: str
    seed_id: str
    key: DrawKey
    unit_interval_value: Decimal
    content_hash: str

    def canonical_value(self) -> dict[str, object]:
        return {
            "algorithm_id": ALGORITHM_ID,
            "algorithm_version": ALGORITHM_VERSION,
            "keyed_draw_id": self.keyed_draw_id,
            "seed_id": self.seed_id,
            **self.key.canonical_value(),
            "unit_interval_value": normalized_decimal(self.unit_interval_value),
        }


class KeyedRandomStream:
    """Derive each latent uniform directly from its stable key, never queue order."""

    def __init__(self, seed_id: str):
        if not isinstance(seed_id, str) or not seed_id:
            raise ContractError("RANDOM_DRAW_KEY_INVALID", "seed_id must be nonempty")
        self.seed_id = seed_id
        self._draws: dict[DrawKey, KeyedDraw] = {}

    def draw(self, case_id: str, event_family_id: str, draw_index: int = 0) -> KeyedDraw:
        key = DrawKey(case_id, event_family_id, draw_index)
        existing = self._draws.get(key)
        if existing is not None:
            return existing
        identity = {
            "algorithm_id": ALGORITHM_ID,
            "algorithm_version": ALGORITHM_VERSION,
            "seed_id": self.seed_id,
            **key.canonical_value(),
        }
        digest = sha256(_canonical_json(identity)).digest()
        numerator = Decimal(int.from_bytes(digest[:16], "big") + 1)
        with localcontext() as context:
            context.prec = 50
            value = numerator / _DENOMINATOR
        keyed_draw_id = f"KEYED-DRAW-{sha256(_canonical_json(identity)).hexdigest()}"
        canonical = {
            **identity,
            "keyed_draw_id": keyed_draw_id,
            "unit_interval_value": normalized_decimal(value),
        }
        draw = KeyedDraw(
            keyed_draw_id=keyed_draw_id,
            seed_id=self.seed_id,
            key=key,
            unit_interval_value=value,
            content_hash=sha256(_canonical_json(canonical)).hexdigest(),
        )
        self._draws[key] = draw
        return draw

    def draws(self) -> tuple[KeyedDraw, ...]:
        return tuple(self._draws[key] for key in sorted(self._draws))
