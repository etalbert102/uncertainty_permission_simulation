"""Small, deliberately slow queue oracle for differential validation only."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext

from .schemas import ContractError


@dataclass(frozen=True)
class ReferenceRequest:
    request_id: str
    case_id: str
    queued_at: Decimal
    service_time: Decimal
    deadline: Decimal


@dataclass(frozen=True)
class ReferenceVisit:
    request_id: str
    case_id: str
    server_index: int
    queued_at: Decimal
    started_at: Decimal
    completed_at: Decimal
    service_time: Decimal
    wait_time: Decimal
    deadline: Decimal
    completed_by_deadline: bool
    started_by_cutoff: bool
    completed_by_cutoff: bool
    right_censored: bool
    censoring_reason: str | None


def _validate_requests(
    requests: tuple[ReferenceRequest, ...],
    capacity: int,
    administrative_cutoff: Decimal | None,
) -> None:
    if not isinstance(requests, tuple) or any(
        not isinstance(request, ReferenceRequest) for request in requests
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reference requests must be typed tuple")
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reference capacity must be positive")
    if administrative_cutoff is not None and (
        not isinstance(administrative_cutoff, Decimal)
        or not administrative_cutoff.is_finite()
        or administrative_cutoff < 0
    ):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "invalid reference cutoff")
    identities = [request.request_id for request in requests]
    if len(identities) != len(set(identities)):
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "duplicate reference request")
    for request in requests:
        if not request.request_id or not request.case_id:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "empty reference identity")
        if any(
            not isinstance(value, Decimal) or not value.is_finite() or value < 0
            for value in (request.queued_at, request.service_time, request.deadline)
        ):
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "invalid reference time")
        if request.deadline < request.queued_at:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reference deadline precedes arrival")


def run_reference_fifo(
    requests: tuple[ReferenceRequest, ...],
    *,
    capacity: int,
    administrative_cutoff: Decimal | None = None,
) -> tuple[ReferenceVisit, ...]:
    """Advance between arrivals/completions and assign FIFO work to idle servers."""

    _validate_requests(requests, capacity, administrative_cutoff)
    pending = list(sorted(
        requests,
        key=lambda request: (request.queued_at, request.case_id, request.request_id),
    ))
    waiting: list[ReferenceRequest] = []
    active: dict[int, tuple[Decimal, ReferenceRequest, Decimal]] = {}
    server_available_at = [Decimal(0) for _ in range(capacity)]
    visits: dict[str, ReferenceVisit] = {}
    current = Decimal(0)

    while pending or waiting or active:
        next_arrival = pending[0].queued_at if pending else None
        next_completion = min(
            (completion for completion, _, _ in active.values()),
            default=None,
        )
        candidates = tuple(
            value for value in (next_arrival, next_completion) if value is not None
        )
        if not candidates and waiting:
            raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "reference queue deadlock")
        if candidates:
            current = min(candidates)

        completed_servers = tuple(
            server_index
            for server_index, (completion, _, _) in active.items()
            if completion == current
        )
        for server_index in sorted(completed_servers):
            completion, request, started_at = active.pop(server_index)
            server_available_at[server_index] = completion
            with localcontext() as context:
                context.prec = 50
                wait_time = started_at - request.queued_at
            started_by_cutoff = (
                administrative_cutoff is None or started_at <= administrative_cutoff
            )
            completed_by_cutoff = (
                administrative_cutoff is None or completion <= administrative_cutoff
            )
            visits[request.request_id] = ReferenceVisit(
                request_id=request.request_id,
                case_id=request.case_id,
                server_index=server_index,
                queued_at=request.queued_at,
                started_at=started_at,
                completed_at=completion,
                service_time=request.service_time,
                wait_time=wait_time,
                deadline=request.deadline,
                completed_by_deadline=completion <= request.deadline,
                started_by_cutoff=started_by_cutoff,
                completed_by_cutoff=completed_by_cutoff,
                right_censored=not completed_by_cutoff,
                censoring_reason=(
                    None if completed_by_cutoff
                    else "service_in_progress_at_cutoff" if started_by_cutoff
                    else "service_not_started_by_cutoff"
                ),
            )

        while pending and pending[0].queued_at == current:
            waiting.append(pending.pop(0))
        waiting.sort(key=lambda request: (
            request.queued_at, request.case_id, request.request_id,
        ))

        idle_servers = sorted([
            server_index for server_index in range(capacity)
            if server_index not in active
        ], key=lambda server_index: (server_available_at[server_index], server_index))
        while waiting and idle_servers:
            server_index = idle_servers.pop(0)
            request = waiting.pop(0)
            with localcontext() as context:
                context.prec = 50
                completion = current + request.service_time
            if request.service_time == 0:
                server_available_at[server_index] = current
                started_by_cutoff = (
                    administrative_cutoff is None or current <= administrative_cutoff
                )
                visits[request.request_id] = ReferenceVisit(
                    request_id=request.request_id,
                    case_id=request.case_id,
                    server_index=server_index,
                    queued_at=request.queued_at,
                    started_at=current,
                    completed_at=current,
                    service_time=request.service_time,
                    wait_time=current - request.queued_at,
                    deadline=request.deadline,
                    completed_by_deadline=current <= request.deadline,
                    started_by_cutoff=started_by_cutoff,
                    completed_by_cutoff=started_by_cutoff,
                    right_censored=not started_by_cutoff,
                    censoring_reason=(
                        None if started_by_cutoff else "service_not_started_by_cutoff"
                    ),
                )
                idle_servers.append(server_index)
                idle_servers.sort(
                    key=lambda index: (server_available_at[index], index)
                )
            else:
                active[server_index] = (completion, request, current)
                server_available_at[server_index] = completion

    ordered = tuple(sorted(
        requests,
        key=lambda request: (request.queued_at, request.case_id, request.request_id),
    ))
    return tuple(visits[request.request_id] for request in ordered)


def analytical_dd1(
    requests: tuple[ReferenceRequest, ...],
) -> tuple[tuple[Decimal, Decimal], ...]:
    """Closed recurrence for one deterministic FIFO server (D/D/1)."""

    _validate_requests(requests, 1, None)
    ordered = tuple(sorted(
        requests,
        key=lambda request: (request.queued_at, request.case_id, request.request_id),
    ))
    available_at = Decimal(0)
    result: list[tuple[Decimal, Decimal]] = []
    for request in ordered:
        started_at = max(request.queued_at, available_at)
        with localcontext() as context:
            context.prec = 50
            completed_at = started_at + request.service_time
        result.append((started_at, completed_at))
        available_at = completed_at
    return tuple(result)
