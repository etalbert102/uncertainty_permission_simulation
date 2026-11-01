from decimal import Decimal

import pytest

from uncertainty_permission_simulation.events import Event, EventQueue
from uncertainty_permission_simulation.schemas import ContractError


def event(event_id: str, kind: str, time: str, key: str) -> Event:
    return Event(event_id, kind, Decimal(time), key, "ROOT")


def test_simultaneous_events_use_frozen_priority_then_key() -> None:
    queue = EventQueue()
    queue.push(event("2", "CASE_CLOSED", "1", "B"))
    queue.push(event("1", "CASE_ARRIVAL", "1", "A"))
    assert [item.event_type_id for item in queue.drain()] == ["CASE_ARRIVAL", "CASE_CLOSED"]


def test_review_completion_wins_an_exact_deadline_tie() -> None:
    queue = EventQueue()
    queue.push(event("2", "DEADLINE_REACHED", "10", "DEADLINE"))
    queue.push(event("1", "REVIEW_COMPLETED", "10", "COMPLETION"))
    assert [item.event_type_id for item in queue.drain()] == ["REVIEW_COMPLETED", "DEADLINE_REACHED"]


def test_duplicate_causal_key_is_blocking() -> None:
    queue = EventQueue()
    queue.push(event("1", "CASE_ARRIVAL", "0", "SAME"))
    with pytest.raises(ContractError, match="SIM_EVENT_ORDER_INVALID"):
        queue.push(event("2", "CASE_CLOSED", "1", "SAME"))


def test_microstep_bound_rejects_same_time_livelock() -> None:
    queue = EventQueue(max_microstep=2)
    with pytest.raises(ContractError, match="SIM_EVENT_LIVELOCK"):
        queue.push(Event("1", "CASE_ARRIVAL", Decimal(0), "K", "ROOT", microstep_rank=3))
