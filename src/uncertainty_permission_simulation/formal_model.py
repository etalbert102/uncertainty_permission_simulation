"""Executable Slice 1 formal assessments for deterministic traces."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .process_model import TraceResult


@dataclass(frozen=True)
class Assessment:
    property_id: str
    status: str
    completeness: str
    diagnostic_codes: tuple[str, ...] = ()
    value: bool | None = None
    trace_id: str = ""


def p0_profile(trace: TraceResult, *, arm: str) -> dict[str, Assessment]:
    preserve = arm == "preserve"
    values = {
        "F0": Assessment("F0", "pass" if preserve else "fail", "complete", () if preserve else ("FM_EVIDENCE_TYPE_COLLAPSED", "FM_LINEAGE_INCOMPLETE", "FM_POLICY_NOT_INSPECTABLE"), trace_id=trace.trace_id),
        "F1": Assessment("F1", "not_applicable", "complete", trace_id=trace.trace_id),
        "F2": Assessment("F2", "not_applicable", "complete", trace_id=trace.trace_id),
        "F3": Assessment("F3", "unassessable" if preserve else "not_applicable", "incomplete" if preserve else "complete", ("FM_REVIEW_UNRECORDED",) if preserve else (), trace_id=trace.trace_id),
        "F4": Assessment("F4", "pass" if preserve else "fail", "complete", () if preserve else ("FM_MATERIAL_ITEM_UNSURFACED",), trace_id=trace.trace_id),
        "F5": Assessment("F5", "unassessable", "incomplete", ("FM_APPLICABILITY_UNDETERMINED",), trace_id=trace.trace_id),
        "GateSafe": Assessment("GateSafe", "pass" if preserve else "not_applicable", "complete", value=True if preserve else None, trace_id=trace.trace_id),
        "ReviewEffective": Assessment("ReviewEffective", "unassessable" if preserve else "fail", "incomplete" if preserve else "complete", ("FM_REVIEW_UNRECORDED",) if preserve else ("FM_REQUIRED_GATE_MISSING", "FM_REVIEW_EVIDENCE_MISSING"), value=None if preserve else False, trace_id=trace.trace_id),
        "DecisionServiceEffective": Assessment("DecisionServiceEffective", "unassessable", "incomplete", ("FM_REQUIRED_INPUT_MISSING",), trace_id=trace.trace_id),
    }
    return values


def render_p0_report(preserve: TraceResult, fallback: TraceResult) -> dict[str, object]:
    if preserve.held_bundle_hash != fallback.held_bundle_hash:
        raise ValueError("P0_HELD_INPUT_MISMATCH")
    return {
        "protocol_version": "0.2",
        "application_level": "bounded_deterministic_trace",
        "evaluation_unit": "controlled_pair",
        "comparison_id": "P0-E-PRESERVE__P0-E-FALLBACK",
        "held_bundle_hash": preserve.held_bundle_hash,
        "random_draw_count": 0,
        "assessment_profile": {
            "preserve": {key: asdict(value) for key, value in p0_profile(preserve, arm="preserve").items()},
            "fallback": {key: asdict(value) for key, value in p0_profile(fallback, arm="fallback").items()},
        },
        "conclusion": {
            "strongest_supported_finding": "representation_induced_routing_and_permission_change",
            "overall_score": "prohibited",
        },
        "claim_limit_receipts": {
            "capacity_boundary": {"evaluation_state": "omitted_by_claim_limit", "required_level": "dynamic_system_simulation"}
        },
    }
