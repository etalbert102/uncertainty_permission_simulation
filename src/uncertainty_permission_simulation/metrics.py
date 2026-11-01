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
    exposure_counts = {
        "external_exposure": run.telemetry.external_exposure_count,
        "recovery_started": run.telemetry.recovery_started_count,
        "supported_exposure": run.telemetry.supported_exposure_count,
        "unsupported_exposure": run.telemetry.unsupported_exposure_count,
        "evidentially_unsupported_exposure": run.telemetry.evidentially_unsupported_exposure_count,
        "unauthorized_exposure": run.telemetry.unauthorized_exposure_count,
    }
    correction_counts = {
        "correction_eligible": run.telemetry.correction_eligible_count,
        "correction_request": run.telemetry.correction_request_count,
        "correction_not_requested": run.telemetry.correction_not_requested_count,
    }
    reassessment_counts = {
        "reassessment_started": run.telemetry.reassessment_started_count,
        "reassessment_completed": run.telemetry.reassessment_completed_count,
        "timely_reassessment": run.telemetry.timely_reassessment_count,
        "late_reassessment": run.telemetry.late_reassessment_count,
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
            for name, value in (
                case_counts | review_counts | action_counts | exposure_counts
                | correction_counts | reassessment_counts | gate_counts
            ).items()
        },
        "gate_applicable_count": run.telemetry.gate_applicable_count,
    }
    with localcontext() as context:
        context.prec = 50
        result.update({
            f"{name}_rate": normalized_decimal(Decimal(value) / Decimal(denominator))
            for name, value in (case_counts | action_counts | exposure_counts).items()
        })
        result.update({
            f"{name}_case_rate": normalized_decimal(Decimal(value) / Decimal(denominator))
            for name, value in correction_counts.items()
        })
        correction_denominator = run.telemetry.correction_eligible_count
        result["correction_uptake_rate"] = (
            normalized_decimal(
                Decimal(run.telemetry.correction_request_count) / Decimal(correction_denominator)
            )
            if correction_denominator else "0"
        )
        queue_denominator = run.telemetry.review_queue_count
        result.update({
            f"{name}_rate": (
                normalized_decimal(Decimal(value) / Decimal(queue_denominator))
                if queue_denominator else "0"
            )
            for name, value in review_counts.items()
        })
        reassessment_denominator = run.telemetry.correction_request_count
        result.update({
            f"{name}_rate": (
                normalized_decimal(Decimal(value) / Decimal(reassessment_denominator))
                if reassessment_denominator else "0"
            )
            for name, value in reassessment_counts.items()
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
            "reassessment_mean_wait_time": normalized_decimal(
                run.telemetry.reassessment_total_wait_time / Decimal(reassessment_denominator)
            ) if reassessment_denominator else "0",
            "reassessment_max_wait_time": normalized_decimal(run.telemetry.reassessment_max_wait_time),
        })
    return result
