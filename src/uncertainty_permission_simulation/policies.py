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


POLICY_BEHAVIORS = {
    "U0": PolicyBehavior("U0", False, True, "none", False, False, True, False),
    "U1": PolicyBehavior("U1", True, False, "none", False, False, False, False),
    "U2C": PolicyBehavior("U2C", True, True, "all_progression", False, False, False, False),
    "U2O": PolicyBehavior("U2O", True, True, "all_progression", True, False, False, False),
    "U3": PolicyBehavior("U3", False, True, "unresolved_only", False, True, True, True),
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
    assistance_used = behavior.offers_assistance and inputs.notice_delivered and (
        not inputs.administrative_access
        or not inputs.comprehension
        or inputs.response_effort > response_effort_limit
    )
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


def decide(*, policy_id: str, material_uncertainty_visible: bool, action_evidence: bool, review_complete: bool, deadline_reached: bool) -> Decision:
    policy_behavior(policy_id)
    if material_uncertainty_visible and not review_complete:
        return Decision("enhanced_scrutiny", "hold", "closed", False)
    if action_evidence:
        return Decision("supported_progression", "progress", "satisfied", True)
    if policy_id == "U2C" and deadline_reached:
        return Decision("review_timeout", "hold", "closed", False)
    if policy_id in {"U0", "U3"} and deadline_reached:
        return Decision("insufficient_evidence_hold", "hold", "closed", False)
    if policy_id in {"U1", "U2O"} and deadline_reached:
        return Decision("timeout_progression", "progress", "absent" if policy_id == "U1" else "open", True)
    return Decision("pending", "hold", "pending", False)
