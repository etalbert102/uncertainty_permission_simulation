from decimal import Decimal

import pytest

from uncertainty_permission_simulation.configuration import ParameterValue, ScenarioOverlaySpec, compile_configuration
from uncertainty_permission_simulation.policies import (
    POLICY_BEHAVIORS,
    POLICY_IDS,
    EngagementInputs,
    decide,
    decide_action,
    map_engagement,
    policy_behavior,
)
from uncertainty_permission_simulation.profiles import CORE_SLOTS, STOCHASTIC_SLOTS, canonical_process, policy, stochastic_process
from uncertainty_permission_simulation.schemas import ContractError


def inputs(**updates: object) -> EngagementInputs:
    values = {
        "notice_delivered": True,
        "administrative_access": True,
        "comprehension": True,
        "records_available": True,
        "response_effort": Decimal("0.4"),
        "extension_needed": False,
        "retrieval_success": True,
    }
    values.update(updates)
    return EngagementInputs(**values)


def mapped(policy_id: str, **updates: object):
    return map_engagement(
        policy_id=policy_id, inputs=inputs(**updates),
        response_effort_limit=Decimal("0.5"), assistance_effort_bonus=Decimal("0.4"),
        extension_effort_bonus=Decimal("0.2"),
    )


def test_policy_registry_is_closed_and_all_profiles_compile_against_core_capabilities() -> None:
    assert tuple(POLICY_BEHAVIORS) == POLICY_IDS
    assert "recovery" in stochastic_process().capabilities
    assert "recover" in stochastic_process().action_type_ids
    assert "reassessment" in stochastic_process().capabilities
    assert "reassess" in stochastic_process().action_type_ids
    assert {"recovery", "correction", "reassessment"} <= set(stochastic_process().stage_ids)
    for policy_id in POLICY_IDS:
        profile = policy(policy_id)
        assert profile.required_capabilities <= canonical_process().capabilities
        assert profile.required_action_type_ids <= canonical_process().action_type_ids
        overlay = ScenarioOverlaySpec(
            overlay_id="POLICY-COMPILE-OVERLAY",
            parameters=tuple(
                ParameterValue(slot_id=slot_id, value="1", provenance="stylized", owner_id="POLICY-COMPILE-OVERLAY")
                for slot_id in sorted(CORE_SLOTS | STOCHASTIC_SLOTS)
            ),
        )
        compiled = compile_configuration(
            configuration_id=f"POLICY-COMPILE-{policy_id}", process=stochastic_process(),
            policy=profile, overlay=overlay, evaluation_spec_id="POLICY-COMPILE-EVALUATION",
        )
        assert not compiled.unresolved_parameter_slot_ids
    with pytest.raises(ContractError, match="unknown policy"):
        policy_behavior("U9")


def test_u3_assistance_changes_engagement_without_changing_inputs() -> None:
    shared = {"administrative_access": False, "comprehension": False, "response_effort": Decimal("0.8")}
    assert mapped("U1", **shared).responded is False
    assisted = mapped("U3", **shared)
    assert assisted.assistance_used is True
    assert assisted.responded is True


def test_extensions_are_policy_owned() -> None:
    assert mapped("U0", extension_needed=True).extension_granted is True
    assert mapped("U3", extension_needed=True).extension_granted is True
    assert mapped("U1", extension_needed=True).extension_granted is False
    assert mapped("U2C", extension_needed=True).extension_granted is False
    assert mapped("U2O", extension_needed=True).extension_granted is False
    assert mapped("U3", notice_delivered=False, extension_needed=True).extension_granted is False
    shared = {"response_effort": Decimal("0.6"), "extension_needed": True}
    assert mapped("U0", **shared).responded is True
    assert mapped("U1", **shared).responded is False


def test_only_u3_proactively_retrieves_missing_evidence() -> None:
    for policy_id in ("U0", "U1", "U2C", "U2O"):
        assert mapped(policy_id, records_available=False).proactive_retrieval_requested is False
    u3 = mapped("U3", records_available=False)
    assert u3.proactive_retrieval_requested is True
    assert u3.retrieved_evidence is True


def test_review_scope_distinguishes_all_progression_from_unresolved_only() -> None:
    assert policy_behavior("U2C").review_scope == "all_progression"
    assert policy_behavior("U2O").review_scope == "all_progression"
    assert policy_behavior("U3").review_scope == "unresolved_only"
    assert policy_behavior("U0").review_scope == "none"


def test_deadline_decisions_keep_fail_closed_and_fail_open_distinct() -> None:
    common = dict(material_uncertainty_visible=False, action_evidence=False, review_complete=False, deadline_reached=True)
    assert decide(policy_id="U0", **common).action == "hold"
    assert decide(policy_id="U2C", **common).action == "hold"
    assert decide(policy_id="U3", **common).action == "hold"
    assert decide(policy_id="U1", **common).action == "progress"
    assert decide(policy_id="U2O", **common).action == "progress"


def test_final_action_matrix_separates_support_review_and_timeout() -> None:
    supported = decide_action(
        policy_id="U2C", evidence_sufficient=True, review_required=True,
        review_completed_by_deadline=True, deadline_reached=True,
    )
    assert supported.action == "progress"
    assert supported.review_authorization_recorded is True
    assert supported.progression_supported is True

    insufficient = decide_action(
        policy_id="U2C", evidence_sufficient=False, review_required=True,
        review_completed_by_deadline=True, deadline_reached=True,
    )
    assert insufficient.action == "request_evidence"
    assert insufficient.progression_supported is False

    closed = decide_action(
        policy_id="U2C", evidence_sufficient=False, review_required=True,
        review_completed_by_deadline=False, deadline_reached=True,
    )
    opened = decide_action(
        policy_id="U2O", evidence_sufficient=False, review_required=True,
        review_completed_by_deadline=False, deadline_reached=True,
    )
    assert (closed.action, closed.gate_state, closed.timeout_triggered) == ("hold", "closed", True)
    assert (opened.action, opened.gate_state, opened.timeout_triggered) == ("progress", "open", True)
    assert opened.progression_supported is False
    assert opened.evidentially_supported_progression is False
    assert opened.unauthorized_progression is True
    assert opened.gate_safe is False
    assert closed.gate_safe is True


def test_supported_evidence_does_not_bypass_a_required_review() -> None:
    late = decide_action(
        policy_id="U2C", evidence_sufficient=True, review_required=True,
        review_completed_by_deadline=False, deadline_reached=True,
    )
    assert late.action == "hold"
    assert late.evidence_sufficient is True
    assert late.review_authorization_recorded is False
    assert late.progression_supported is False
    assert late.gate_safe is True


def test_no_review_policies_distinguish_evidence_from_imputation() -> None:
    supported = decide_action(
        policy_id="U0", evidence_sufficient=True, review_required=False,
        review_completed_by_deadline=False, deadline_reached=True,
    )
    held = decide_action(
        policy_id="U0", evidence_sufficient=False, review_required=False,
        review_completed_by_deadline=False, deadline_reached=True,
    )
    imputed = decide_action(
        policy_id="U1", evidence_sufficient=False, review_required=False,
        review_completed_by_deadline=False, deadline_reached=True,
    )
    assert supported.progression_supported is True
    assert supported.gate_safe is None
    assert held.action == "hold"
    assert imputed.action == "progress" and imputed.progression_supported is False


def test_impossible_review_completion_is_rejected() -> None:
    with pytest.raises(ContractError, match="SIM_SYSTEM_STATE_INCOMPLETE"):
        decide_action(
            policy_id="U1", evidence_sufficient=False, review_required=False,
            review_completed_by_deadline=True, deadline_reached=True,
        )


@pytest.mark.parametrize(("field", "value"), (("response_effort", Decimal("1.1")), ("notice_delivered", "yes")))
def test_engagement_inputs_reject_invalid_latents(field: str, value: object) -> None:
    with pytest.raises(ContractError, match="SCENARIO_PARAMETER_INVALID"):
        inputs(**{field: value})
