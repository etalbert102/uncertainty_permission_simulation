"""Case-neutral deterministic process vertical slice."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from hashlib import sha256
import json

from .events import Event, EventQueue
from .policies import decide


@dataclass(frozen=True)
class TraceSpec:
    trace_id: str
    policy_id: str
    representation: str = "fallback"
    material_uncertainty: bool = False
    response: bool = False
    action_evidence: bool = False
    review_delay: int = 0
    deadline: int = 21
    external_exposure: bool = False
    correction: bool = False
    force_scrutiny: bool = False


@dataclass(frozen=True)
class TraceResult:
    trace_id: str
    events: tuple[Event, ...]
    route: str
    final_action: str
    functional_permission: bool
    gate_state: str
    restoration_complete: bool | None
    held_bundle_hash: str

    @property
    def semantic_projection(self) -> tuple[tuple[str, ...], str, str, bool]:
        return (tuple(event.event_type_id for event in self.events), self.route, self.final_action, self.functional_permission)


def _held_hash(spec: TraceSpec) -> str:
    held = {"case": "CASE-1", "model_output": "UNCERTAIN-OUTPUT-1", "rule": "ROUTE-1", "deadline": spec.deadline}
    return sha256(json.dumps(held, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def run_trace(spec: TraceSpec) -> TraceResult:
    queue = EventQueue()
    counter = 0

    def emit(kind: str, time: int, **details: object) -> None:
        nonlocal counter
        counter += 1
        key = f"CASE-1:{counter:03d}:{kind}"
        queue.push(Event(f"{spec.trace_id}-E{counter:03d}", kind, Decimal(time), key, "CASE-1:ROOT", (str(counter),), transition_rank=counter, details=details))

    emit("CASE_ARRIVAL", 0)
    emit("SOURCE_EVIDENCE_INGESTED", 0)
    emit("NOTICE_SENT", 1)
    emit("NOTICE_DELIVERED", 1)
    emit("SUBJECT_RESPONDED" if spec.response else "SUBJECT_NONRESPONSE", 2 if spec.response else spec.deadline)
    emit("REPRESENTATION_APPLIED", 2 if spec.response else spec.deadline, representation=spec.representation)
    visible = spec.material_uncertainty and spec.representation == "preserve"
    emit("REPRESENTATION_SURFACED", 2 if spec.response else spec.deadline, material_visible=visible)
    emit("ROUTING_COMPLETED", 2 if spec.response else spec.deadline)
    review_complete = False
    if visible or spec.force_scrutiny or spec.policy_id in {"U2C", "U2O"}:
        emit("REVIEW_QUEUED", 3)
        if spec.review_delay <= spec.deadline - 3:
            emit("REVIEW_STARTED", 3)
            emit("REVIEW_COMPLETED", 3 + spec.review_delay)
            review_complete = True
    if spec.action_evidence:
        emit("EVIDENCE_SUBMITTED", 2)
        emit("EVIDENCE_ACCEPTED", 3)
    emit("DEADLINE_REACHED", spec.deadline)
    decision = decide(policy_id=spec.policy_id, material_uncertainty_visible=visible or spec.force_scrutiny, action_evidence=spec.action_evidence, review_complete=review_complete, deadline_reached=True)
    emit("ACTION_COMPUTED", spec.deadline, action=decision.action)
    if decision.action == "progress":
        emit("PROGRESSION_EXECUTED", spec.deadline)
    if spec.external_exposure:
        emit("EXTERNAL_CONSEQUENCE_STARTED", spec.deadline + 1)
    restoration: bool | None = None
    if spec.correction:
        emit("CORRECTION_REQUESTED", spec.deadline + 2)
        emit("RESTORATION_EXECUTED", spec.deadline + 3)
        restoration = not spec.external_exposure
    emit("CASE_CLOSED", spec.deadline + 4)
    events = queue.drain()
    return TraceResult(spec.trace_id, events, decision.route, decision.action, decision.functional_permission, decision.gate_state, restoration, _held_hash(spec))


def execute_topology(event_type_ids: tuple[str, ...]) -> tuple[str, ...]:
    queue = EventQueue()
    for index, event_type in enumerate(event_type_ids):
        queue.push(Event(f"TOPO-E{index}", event_type, Decimal(index), f"TOPO:{index}:{event_type}", "TOPO:ROOT", (str(index),), transition_rank=index))
    return tuple(event.event_type_id for event in queue.drain())
