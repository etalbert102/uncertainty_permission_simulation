"""Deterministic event ordering and causal-key enforcement."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
import heapq

from .schemas import ContractError, MANIFEST


EVENT_TYPES = tuple(MANIFEST["closed_event_type_ids"])
DEFAULT_PRIORITIES = {event_type: index for index, event_type in enumerate(EVENT_TYPES)}


@dataclass(frozen=True)
class Event:
    event_id: str
    event_type_id: str
    timestamp: Decimal
    causal_event_key: str
    root_event_key: str
    descendant_path: tuple[str, ...] = ()
    microstep_rank: int = 0
    transition_rank: int = 0
    case_id: str = "CASE-1"
    details: dict[str, object] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if self.event_type_id not in EVENT_TYPES:
            raise ContractError("SIM_EVENT_ORDER_INVALID", self.event_type_id)
        if self.microstep_rank < 0:
            raise ContractError("SIM_EVENT_ORDER_INVALID", "negative microstep")


class EventQueue:
    def __init__(self, priorities: dict[str, int] | None = None, *, max_microstep: int = 100):
        self.priorities = priorities or DEFAULT_PRIORITIES
        self.max_microstep = max_microstep
        self._heap: list[tuple[Decimal, int, int, int, str, Event]] = []
        self._keys: set[str] = set()

    def push(self, event: Event) -> None:
        if event.causal_event_key in self._keys:
            raise ContractError("SIM_EVENT_ORDER_INVALID", f"duplicate causal key {event.causal_event_key}")
        if event.microstep_rank > self.max_microstep:
            raise ContractError("SIM_EVENT_LIVELOCK", event.causal_event_key)
        self._keys.add(event.causal_event_key)
        heapq.heappush(self._heap, (event.timestamp, self.priorities[event.event_type_id], event.microstep_rank, event.transition_rank, event.causal_event_key, event))

    def pop(self) -> Event:
        return heapq.heappop(self._heap)[-1]

    def __bool__(self) -> bool:
        return bool(self._heap)

    def drain(self) -> tuple[Event, ...]:
        result: list[Event] = []
        while self:
            result.append(self.pop())
        return tuple(result)
