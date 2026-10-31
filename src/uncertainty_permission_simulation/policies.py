"""Deterministic Slice 1 policy decisions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    route: str
    action: str
    gate_state: str
    functional_permission: bool


def decide(*, policy_id: str, material_uncertainty_visible: bool, action_evidence: bool, review_complete: bool, deadline_reached: bool) -> Decision:
    if material_uncertainty_visible and not review_complete:
        return Decision("enhanced_scrutiny", "hold", "closed", False)
    if action_evidence:
        return Decision("supported_progression", "progress", "satisfied", True)
    if policy_id == "U2C" and deadline_reached:
        return Decision("review_timeout", "hold", "closed", False)
    if policy_id in {"U1", "U2O"} and deadline_reached:
        return Decision("timeout_progression", "progress", "absent" if policy_id == "U1" else "open", True)
    return Decision("pending", "hold", "pending", False)
