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


def engagement_metrics(run: EngagementRun) -> dict[str, int | str | None]:
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
    assistance_counts = {
        "assistance_request": run.telemetry.assistance_request_count,
        "assistance_started": run.telemetry.assistance_started_count,
        "assistance_completed": run.telemetry.assistance_completed_count,
        "timely_assistance": run.telemetry.timely_assistance_count,
        "late_assistance": run.telemetry.late_assistance_count,
        "assistance_right_censored": run.telemetry.assistance_right_censored_count,
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
        "recovery_queue": run.telemetry.recovery_queue_count,
        "recovery_service_started": run.telemetry.recovery_service_started_count,
        "recovery_started": run.telemetry.recovery_started_count,
        "timely_recovery": run.telemetry.timely_recovery_count,
        "late_recovery": run.telemetry.late_recovery_count,
        "recovery_right_censored": run.telemetry.recovery_right_censored_count,
        "recovery_not_queued_by_cutoff": run.telemetry.recovery_not_queued_by_cutoff_count,
        "supported_exposure": run.telemetry.supported_exposure_count,
        "unsupported_exposure": run.telemetry.unsupported_exposure_count,
        "evidentially_unsupported_exposure": run.telemetry.evidentially_unsupported_exposure_count,
        "unauthorized_exposure": run.telemetry.unauthorized_exposure_count,
    }
    correction_counts = {
        "correction_eligible": run.telemetry.correction_eligible_count,
        "correction_request": run.telemetry.correction_request_count,
        "correction_not_requested": run.telemetry.correction_not_requested_count,
        "correction_not_available_by_cutoff": run.telemetry.correction_not_available_by_cutoff_count,
        "correction_executed": run.telemetry.correction_executed_count,
        "timely_correction": run.telemetry.timely_correction_count,
        "late_correction": run.telemetry.late_correction_count,
        "correction_unresolved": run.telemetry.correction_unresolved_count,
        "recovery_active_after_correction": run.telemetry.recovery_active_after_correction_count,
    }
    restoration_counts = {
        "restoration_due": run.telemetry.restoration_due_count,
        "restoration_executed": run.telemetry.restoration_executed_count,
        "timely_restoration": run.telemetry.timely_restoration_count,
        "late_restoration": run.telemetry.late_restoration_count,
        "complete_restoration": run.telemetry.complete_restoration_count,
        "partial_restoration": run.telemetry.partial_restoration_count,
        "restoration_horizon_pending": run.telemetry.restoration_horizon_pending_count,
        "restoration_horizon_expired": run.telemetry.restoration_horizon_expired_count,
        "unresolved_external_consequence": run.telemetry.unresolved_external_consequence_count,
    }
    reassessment_counts = {
        "reassessment_started": run.telemetry.reassessment_started_count,
        "reassessment_completed": run.telemetry.reassessment_completed_count,
        "timely_reassessment": run.telemetry.timely_reassessment_count,
        "late_reassessment": run.telemetry.late_reassessment_count,
        "reassessment_right_censored": run.telemetry.reassessment_right_censored_count,
    }
    gate_counts = {
        "gate_safe": run.telemetry.gate_safe_count,
        "gate_unsafe": run.telemetry.gate_unsafe_count,
    }
    censoring_counts = {
        "case_closed": run.telemetry.case_closed_count,
        "resolved_case": run.telemetry.resolved_case_count,
        "right_censored_case": run.telemetry.right_censored_case_count,
    }
    result: dict[str, int | str | None] = {
        "case_count": denominator,
        "event_count": run.telemetry.event_count,
        **{
            f"{name}_count": value
            for name, value in (
                case_counts | assistance_counts | review_counts | action_counts | exposure_counts
                | correction_counts | restoration_counts | reassessment_counts
                | gate_counts | censoring_counts
            ).items()
        },
        "gate_applicable_count": run.telemetry.gate_applicable_count,
    }
    with localcontext() as context:
        context.prec = 50
        result.update({
            f"{name}_rate": (
                normalized_decimal(
                    Decimal(value) / Decimal(run.telemetry.assistance_request_count)
                ) if run.telemetry.assistance_request_count else "0"
            )
            for name, value in assistance_counts.items()
        })
        result.update({
            f"{name}_rate": normalized_decimal(Decimal(value) / Decimal(denominator))
            for name, value in (case_counts | action_counts | exposure_counts | censoring_counts).items()
        })
        result.update({
            f"{name}_case_rate": normalized_decimal(Decimal(value) / Decimal(denominator))
            for name, value in (correction_counts | restoration_counts).items()
        })
        correction_denominator = run.telemetry.correction_eligible_count
        result["correction_uptake_rate"] = (
            normalized_decimal(
                Decimal(run.telemetry.correction_request_count) / Decimal(correction_denominator)
            )
            if correction_denominator else "0"
        )
        result["correction_execution_rate"] = (
            normalized_decimal(
                Decimal(run.telemetry.correction_executed_count) / Decimal(correction_denominator)
            )
            if correction_denominator else "0"
        )
        correction_outcome_denominator = run.telemetry.correction_executed_count
        result.update({
            "timely_correction_rate": (
                normalized_decimal(
                    Decimal(run.telemetry.timely_correction_count)
                    / Decimal(correction_outcome_denominator)
                )
                if correction_outcome_denominator else "0"
            ),
            "late_correction_rate": (
                normalized_decimal(
                    Decimal(run.telemetry.late_correction_count)
                    / Decimal(correction_outcome_denominator)
                )
                if correction_outcome_denominator else "0"
            ),
        })
        restoration_denominator = run.telemetry.restoration_due_count
        result.update({
            "restoration_execution_rate": (
                normalized_decimal(
                    Decimal(run.telemetry.restoration_executed_count)
                    / Decimal(restoration_denominator)
                ) if restoration_denominator else "0"
            ),
            "complete_restoration_rate": (
                normalized_decimal(
                    Decimal(run.telemetry.complete_restoration_count)
                    / Decimal(restoration_denominator)
                ) if restoration_denominator else "0"
            ),
            "partial_restoration_rate": (
                normalized_decimal(
                    Decimal(run.telemetry.partial_restoration_count)
                    / Decimal(restoration_denominator)
                ) if restoration_denominator else "0"
            ),
        })
        queue_denominator = run.telemetry.review_queue_count
        result.update({
            f"{name}_rate": (
                normalized_decimal(Decimal(value) / Decimal(queue_denominator))
                if queue_denominator else None
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
                if gate_denominator else None
            )
            for name, value in gate_counts.items()
        })
        result.update({
            "review_mean_wait_time": normalized_decimal(
                run.telemetry.review_total_wait_time / Decimal(run.telemetry.review_queue_count)
            ) if run.telemetry.review_queue_count else "0",
            "review_max_wait_time": normalized_decimal(run.telemetry.review_max_wait_time),
            "assistance_mean_wait_time": normalized_decimal(
                run.telemetry.assistance_total_wait_time
                / Decimal(run.telemetry.assistance_started_count)
            ) if run.telemetry.assistance_started_count else "0",
            "assistance_max_wait_time": normalized_decimal(
                run.telemetry.assistance_max_wait_time
            ),
            "recovery_mean_wait_time": normalized_decimal(
                run.telemetry.recovery_total_wait_time
                / Decimal(run.telemetry.recovery_service_started_count)
            ) if run.telemetry.recovery_service_started_count else "0",
            "recovery_max_wait_time": normalized_decimal(run.telemetry.recovery_max_wait_time),
            "reassessment_mean_wait_time": normalized_decimal(
                run.telemetry.reassessment_total_wait_time / Decimal(reassessment_denominator)
            ) if reassessment_denominator else "0",
            "reassessment_max_wait_time": normalized_decimal(run.telemetry.reassessment_max_wait_time),
            "correction_mean_exposure_time": normalized_decimal(
                run.telemetry.correction_total_exposure_time
                / Decimal(correction_outcome_denominator)
            ) if correction_outcome_denominator else "0",
            "correction_max_exposure_time": normalized_decimal(
                run.telemetry.correction_max_exposure_time
            ),
            "restoration_mean_time_from_correction": normalized_decimal(
                run.telemetry.restoration_total_time_from_correction
                / Decimal(run.telemetry.restoration_executed_count)
            ) if run.telemetry.restoration_executed_count else "0",
            "restoration_max_time_from_correction": normalized_decimal(
                run.telemetry.restoration_max_time_from_correction
            ),
        })
    return result
