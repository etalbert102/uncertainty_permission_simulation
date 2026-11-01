"""Trace-derived metric skeleton; prose never owns computed values."""

from __future__ import annotations

from decimal import Decimal, localcontext

from .process_model import TraceResult
from .random_streams import normalized_decimal
from .simulator import EngagementRun


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


def engagement_metrics(run: EngagementRun) -> dict[str, int | str]:
    """Render separate engagement and review-queue measures; never a composite score."""

    denominator = run.telemetry.case_count
    notice_failure_count = sum(
        event.event_type_id == "NOTICE_FAILED"
        for trace in run.traces
        for event in trace.events
    )
    case_counts = {
        "notice_failure": notice_failure_count,
        "response": run.telemetry.response_count,
        "adequate_response_evidence": run.telemetry.adequate_response_evidence_count,
        "assistance": run.telemetry.assistance_count,
        "extension": run.telemetry.extension_count,
        "retrieval_request": run.telemetry.retrieval_request_count,
        "retrieved_evidence": run.telemetry.retrieved_evidence_count,
        "review_queue": run.telemetry.review_queue_count,
    }
    review_counts = {
        "review_started": run.telemetry.review_started_count,
        "review_completed": run.telemetry.review_completed_count,
        "timely_review": run.telemetry.timely_review_count,
        "late_review": run.telemetry.late_review_count,
    }
    action_counts = {
        "action": run.telemetry.action_count,
        "progression": run.telemetry.progression_count,
        "hold": run.telemetry.hold_count,
        "request_evidence_action": run.telemetry.request_evidence_action_count,
        "supported_progression": run.telemetry.supported_progression_count,
        "unsupported_progression": run.telemetry.unsupported_progression_count,
        "evidentially_supported_progression": run.telemetry.evidentially_supported_progression_count,
        "evidentially_unsupported_progression": run.telemetry.evidentially_unsupported_progression_count,
        "unauthorized_progression": run.telemetry.unauthorized_progression_count,
        "review_authorization": run.telemetry.review_authorization_count,
        "fail_open_timeout_progression": run.telemetry.fail_open_timeout_progression_count,
        "fail_closed_timeout_hold": run.telemetry.fail_closed_timeout_hold_count,
    }
    gate_counts = {
        "gate_safe": run.telemetry.gate_safe_count,
        "gate_unsafe": run.telemetry.gate_unsafe_count,
    }
    result: dict[str, int | str] = {
        "case_count": denominator,
        "event_count": run.telemetry.event_count,
        **{
            f"{name}_count": value
            for name, value in (case_counts | review_counts | action_counts | gate_counts).items()
        },
        "gate_applicable_count": run.telemetry.gate_applicable_count,
    }
    with localcontext() as context:
        context.prec = 50
        result.update({
            f"{name}_rate": normalized_decimal(Decimal(value) / Decimal(denominator))
            for name, value in (case_counts | action_counts).items()
        })
        queue_denominator = run.telemetry.review_queue_count
        result.update({
            f"{name}_rate": (
                normalized_decimal(Decimal(value) / Decimal(queue_denominator))
                if queue_denominator else "0"
            )
            for name, value in review_counts.items()
        })
        gate_denominator = run.telemetry.gate_applicable_count
        result.update({
            f"{name}_rate": (
                normalized_decimal(Decimal(value) / Decimal(gate_denominator))
                if gate_denominator else "0"
            )
            for name, value in gate_counts.items()
        })
        result.update({
            "review_mean_wait_time": normalized_decimal(
                run.telemetry.review_total_wait_time / Decimal(run.telemetry.review_queue_count)
            ) if run.telemetry.review_queue_count else "0",
            "review_max_wait_time": normalized_decimal(run.telemetry.review_max_wait_time),
        })
    return result
