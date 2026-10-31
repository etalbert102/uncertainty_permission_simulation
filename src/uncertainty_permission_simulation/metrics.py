"""Trace-derived metric skeleton; prose never owns computed values."""

from __future__ import annotations

from .process_model import TraceResult


def trace_metrics(trace: TraceResult) -> dict[str, int | bool | None]:
    event_types = [event.event_type_id for event in trace.events]
    return {
        "event_count": len(event_types),
        "progression_count": event_types.count("PROGRESSION_EXECUTED"),
        "review_completed_count": event_types.count("REVIEW_COMPLETED"),
        "external_exposure_count": event_types.count("EXTERNAL_CONSEQUENCE_STARTED"),
        "functional_permission": trace.functional_permission,
        "restoration_complete": trace.restoration_complete,
    }
