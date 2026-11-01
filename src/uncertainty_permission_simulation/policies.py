"""Closed counterfactual policy behavior and deterministic decisions."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

from .schemas import ContractError


POLICY_IDS = ("U0", "U1", "U2C", "U2O", "U3")


@dataclass(frozen=True)
class PolicyBehavior:
    policy_id: str
    permits_imputation: bool
    preserves_evidence_status: bool
    review_scope: Literal["none", "all_progression", "unresolved_only"]
    fail_open_on_review_timeout: bool
    offers_assistance: bool
    grants_extensions: bool
    proactive_evidence_retrieval: bool
    restores_after_correction: bool


POLICY_BEHAVIORS = {
    "U0": PolicyBehavior(
        policy_id="U0", permits_imputation=False, preserves_evidence_status=True,
        review_scope="none", fail_open_on_review_timeout=False,
        offers_assistance=False, grants_extensions=True,
        proactive_evidence_retrieval=False, restores_after_correction=False,
    ),
    "U1": PolicyBehavior(
        policy_id="U1", permits_imputation=True, preserves_evidence_status=False,
        review_scope="none", fail_open_on_review_timeout=False,
        offers_assistance=False, grants_extensions=False,
        proactive_evidence_retrieval=False, restores_after_correction=True,
    ),
    "U2C": PolicyBehavior(
        policy_id="U2C", permits_imputation=True, preserves_evidence_status=True,
        review_scope="all_progression", fail_open_on_review_timeout=False,
        offers_assistance=False, grants_extensions=False,
        proactive_evidence_retrieval=False, restores_after_correction=False,
    ),
    "U2O": PolicyBehavior(
        policy_id="U2O", permits_imputation=True, preserves_evidence_status=True,
        review_scope="all_progression", fail_open_on_review_timeout=True,
        offers_assistance=False, grants_extensions=False,
        proactive_evidence_retrieval=False, restores_after_correction=True,
    ),
    "U3": PolicyBehavior(
        policy_id="U3", permits_imputation=False, preserves_evidence_status=True,
        review_scope="unresolved_only", fail_open_on_review_timeout=False,
        offers_assistance=True, grants_extensions=True,
        proactive_evidence_retrieval=True, restores_after_correction=False,
    ),
}


@dataclass(frozen=True)
class EngagementInputs:
    notice_delivered: bool
    administrative_access: bool
    comprehension: bool
    records_available: bool
    response_effort: Decimal
    extension_needed: bool
    retrieval_success: bool

    def __post_init__(self) -> None:
        for field_name in (
            "notice_delivered", "administrative_access", "comprehension", "records_available",
            "extension_needed", "retrieval_success",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must be boolean")
        if not isinstance(self.response_effort, Decimal) or not self.response_effort.is_finite() or not (Decimal(0) <= self.response_effort <= Decimal(1)):
            raise ContractError("SCENARIO_PARAMETER_INVALID", "response_effort must lie in [0, 1]")


@dataclass(frozen=True)
class EngagementDecision:
    policy_id: str
    assistance_used: bool
    extension_granted: bool
    responded: bool
    adequate_response_evidence: bool
    proactive_retrieval_requested: bool
    retrieved_evidence: bool


def policy_behavior(policy_id: str) -> PolicyBehavior:
    try:
        return POLICY_BEHAVIORS[policy_id]
    except KeyError as exc:
        raise ContractError("PROFILE_POLICY_PROCESS_OVERLAP", f"unknown policy {policy_id}") from exc


def map_engagement(
    *,
    policy_id: str,
    inputs: EngagementInputs,
    response_effort_limit: Decimal,
    assistance_effort_bonus: Decimal,
    extension_effort_bonus: Decimal,
    assistance_completed: bool,
) -> EngagementDecision:
    behavior = policy_behavior(policy_id)
    for field_name, value in {
        "response_effort_limit": response_effort_limit,
        "assistance_effort_bonus": assistance_effort_bonus,
        "extension_effort_bonus": extension_effort_bonus,
    }.items():
        if not isinstance(value, Decimal) or not value.is_finite() or not (Decimal(0) <= value <= Decimal(1)):
            raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must lie in [0, 1]")
    extension_granted = behavior.grants_extensions and inputs.notice_delivered and inputs.extension_needed
    if not isinstance(assistance_completed, bool):
        raise ContractError("SCENARIO_PARAMETER_INVALID", "assistance_completed must be boolean")
    assistance_needed = inputs.notice_delivered and (
        not inputs.administrative_access
        or not inputs.comprehension
        or inputs.response_effort > response_effort_limit
    )
    assistance_used = behavior.offers_assistance and assistance_needed and assistance_completed
    effective_access = inputs.administrative_access or assistance_used
    effective_comprehension = inputs.comprehension or assistance_used
    effort_limit = min(
        Decimal(1),
        response_effort_limit
        + (assistance_effort_bonus if assistance_used else Decimal(0))
        + (extension_effort_bonus if extension_granted else Decimal(0)),
    )
    responded = (
        inputs.notice_delivered
        and effective_access
        and effective_comprehension
        and inputs.response_effort <= effort_limit
    )
    adequate_response_evidence = responded and inputs.records_available
    proactive_retrieval_requested = behavior.proactive_evidence_retrieval and not adequate_response_evidence
    retrieved_evidence = proactive_retrieval_requested and inputs.retrieval_success
    return EngagementDecision(
        policy_id=policy_id,
        assistance_used=assistance_used,
        extension_granted=extension_granted,
        responded=responded,
        adequate_response_evidence=adequate_response_evidence,
        proactive_retrieval_requested=proactive_retrieval_requested,
        retrieved_evidence=retrieved_evidence,
    )


@dataclass(frozen=True)
class Decision:
    route: str
    action: str
    gate_state: str
    functional_permission: bool


@dataclass(frozen=True)
class ActionDecision:
    policy_id: str
    action: Literal["progress", "hold", "request_evidence"]
    reason_code: str
    evidence_sufficient: bool
    review_required: bool
    review_completed_by_deadline: bool
    review_authorization_recorded: bool
    timeout_triggered: bool
    gate_state: Literal["not_applicable", "satisfied", "closed", "open", "pending"]
    functional_permission: bool

    @property
    def progression_supported(self) -> bool:
        return (
            self.action == "progress"
            and self.evidence_sufficient
            and (not self.review_required or self.review_authorization_recorded)
        )

    @property
    def evidentially_supported_progression(self) -> bool:
        return self.action == "progress" and self.evidence_sufficient

    @property
    def unauthorized_progression(self) -> bool:
        return (
            self.action == "progress"
            and self.review_required
            and not self.review_authorization_recorded
        )

    @property
    def gate_safe(self) -> bool | None:
        if not self.review_required:
            return None
        return not self.unauthorized_progression

    @property
    def unsupported_reason_codes(self) -> tuple[str, ...]:
        if self.action != "progress":
            return ()
        reasons: list[str] = []
        if not self.evidence_sufficient:
            reasons.append("insufficient_evidence")
        if self.review_required and not self.review_authorization_recorded:
            reasons.append("missing_timely_review_authorization")
        return tuple(reasons)


def decide_action(
    *,
    policy_id: str,
    evidence_sufficient: bool,
    review_required: bool,
    review_completed_by_deadline: bool,
    deadline_reached: bool,
) -> ActionDecision:
    behavior = policy_behavior(policy_id)
    for field_name, value in {
        "evidence_sufficient": evidence_sufficient,
        "review_required": review_required,
        "review_completed_by_deadline": review_completed_by_deadline,
        "deadline_reached": deadline_reached,
    }.items():
        if not isinstance(value, bool):
            raise ContractError("SCENARIO_PARAMETER_INVALID", f"{field_name} must be boolean")
    if review_completed_by_deadline and not review_required:
        raise ContractError("SIM_SYSTEM_STATE_INCOMPLETE", "review cannot complete when it is not required")
    if review_required:
        if review_completed_by_deadline:
            if evidence_sufficient:
                return ActionDecision(
                    policy_id, "progress", "supported_after_timely_review", True, True, True,
                    True, False, "satisfied", True,
                )
            return ActionDecision(
                policy_id, "request_evidence", "insufficient_evidence_after_timely_review",
                False, True, True, False, False, "closed", False,
            )
        if deadline_reached:
            if behavior.fail_open_on_review_timeout:
                return ActionDecision(
                    policy_id, "progress", "review_timeout_fail_open", evidence_sufficient,
                    True, False, False, True, "open", True,
                )
            return ActionDecision(
                policy_id, "hold", "review_timeout_fail_closed", evidence_sufficient,
                True, False, False, True, "closed", False,
            )
        return ActionDecision(
            policy_id, "hold", "review_pending", evidence_sufficient,
            True, False, False, False, "pending", False,
        )
    if evidence_sufficient:
        return ActionDecision(
            policy_id, "progress", "supported_without_review", True,
            False, False, False, False, "not_applicable", True,
        )
    if deadline_reached and behavior.permits_imputation:
        return ActionDecision(
            policy_id, "progress", "imputation_progression", False,
            False, False, False, True, "not_applicable", True,
        )
    return ActionDecision(
        policy_id, "hold", "insufficient_evidence_hold" if deadline_reached else "pending",
        False, False, False, False, deadline_reached, "not_applicable", False,
    )


def decide(*, policy_id: str, material_uncertainty_visible: bool, action_evidence: bool, review_complete: bool, deadline_reached: bool) -> Decision:
    behavior = policy_behavior(policy_id)
    review_required = material_uncertainty_visible or behavior.review_scope == "all_progression"
    result = decide_action(
        policy_id=policy_id,
        evidence_sufficient=action_evidence,
        review_required=review_required,
        review_completed_by_deadline=review_complete and review_required,
        deadline_reached=deadline_reached,
    )
    route = {
        "supported_after_timely_review": "supported_progression",
        "supported_without_review": "supported_progression",
        "review_timeout_fail_closed": "enhanced_scrutiny" if material_uncertainty_visible else "review_timeout",
        "review_timeout_fail_open": "timeout_progression",
        "imputation_progression": "timeout_progression",
        "insufficient_evidence_after_timely_review": "enhanced_scrutiny",
        "insufficient_evidence_hold": "insufficient_evidence_hold",
        "review_pending": "pending",
        "pending": "pending",
    }[result.reason_code]
    gate_state = "absent" if policy_id == "U1" and result.gate_state == "not_applicable" else result.gate_state
    return Decision(route, result.action, gate_state, result.functional_permission)
