"""Deterministic closed configuration compilation."""

from __future__ import annotations

from hashlib import sha256
import inspect
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from .rules import RULE_IMPLEMENTATIONS, implementation_code_hash


class CompilationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ParameterValue(FrozenModel):
    slot_id: str
    value: Any | None
    provenance: Literal["documented", "unsupported", "stylized", "sensitivity"]
    owner_id: str


class ProcessProfileSpec(FrozenModel):
    profile_id: str
    stage_ids: tuple[str, ...]
    capabilities: frozenset[str]
    action_type_ids: frozenset[str]
    parameter_slot_ids: frozenset[str]
    documented_parameters: tuple[ParameterValue, ...] = ()


class PolicyProfileSpec(FrozenModel):
    profile_id: str
    required_capabilities: frozenset[str]
    required_action_type_ids: frozenset[str]
    parameter_slot_ids: frozenset[str]
    gate_semantics: Literal["none", "fail_closed", "fail_open"]


class ScenarioOverlaySpec(FrozenModel):
    overlay_id: str
    parameters: tuple[ParameterValue, ...]


class BindingReceipt(FrozenModel):
    slot_id: str
    owner_id: str
    provenance: Literal["documented", "stylized", "sensitivity"]
    value: Any


class RefinementStateSpec(FrozenModel):
    refinement_id: str
    satisfied_support_condition_ids: tuple[str, ...]


class RefinementCertificateSpec(FrozenModel):
    certificate_id: str
    evidence_state_id: str
    coverage_mode: Literal["finite_exact"]
    owner_id: str
    refinements: tuple[RefinementStateSpec, ...]


class ActionSupportRuleSpec(FrozenModel):
    action_type_id: str
    implementation_id: str
    implementation_code_hash: str
    support_condition_ids: tuple[str, ...]


class EvaluationSpecificationSpec(FrozenModel):
    evaluation_spec_id: str
    owner_id: str
    action_support_rules: tuple[ActionSupportRuleSpec, ...]
    refinement_certificates: tuple[RefinementCertificateSpec, ...]
    specification_hash: str


PERIOD_EVIDENCE_SUPPORT_CONDITION_ID = "PERIOD-SPECIFIC-EVIDENCE"
SUPPORTED_EVIDENCE_STATE_ID = "PERIOD-SPECIFIC-EVIDENCE-PRESENT"
UNRESOLVED_EVIDENCE_STATE_ID = "PERIOD-SPECIFIC-EVIDENCE-UNRESOLVED"


def _canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def period_evidence_evaluation_specification(
    evaluation_spec_id: str,
    *,
    owner_id: str = "INDEPENDENT-EVALUATION-OWNER",
) -> EvaluationSpecificationSpec:
    """Build the closed binary support specification used by the stylized kernel."""

    rule = ActionSupportRuleSpec(
        action_type_id="progress",
        implementation_id="action_support_membership",
        implementation_code_hash=implementation_code_hash("action_support_membership"),
        support_condition_ids=(PERIOD_EVIDENCE_SUPPORT_CONDITION_ID,),
    )
    certificates = (
        RefinementCertificateSpec(
            certificate_id="CERT-PERIOD-EVIDENCE-PRESENT@1",
            evidence_state_id=SUPPORTED_EVIDENCE_STATE_ID,
            coverage_mode="finite_exact",
            owner_id=owner_id,
            refinements=(RefinementStateSpec(
                refinement_id="REF-PERIOD-EVIDENCE-PRESENT",
                satisfied_support_condition_ids=(PERIOD_EVIDENCE_SUPPORT_CONDITION_ID,),
            ),),
        ),
        RefinementCertificateSpec(
            certificate_id="CERT-PERIOD-EVIDENCE-UNRESOLVED@1",
            evidence_state_id=UNRESOLVED_EVIDENCE_STATE_ID,
            coverage_mode="finite_exact",
            owner_id=owner_id,
            refinements=(
                RefinementStateSpec(
                    refinement_id="REF-PERIOD-EVIDENCE-AVAILABLE",
                    satisfied_support_condition_ids=(PERIOD_EVIDENCE_SUPPORT_CONDITION_ID,),
                ),
                RefinementStateSpec(
                    refinement_id="REF-PERIOD-EVIDENCE-ABSENT",
                    satisfied_support_condition_ids=(),
                ),
            ),
        ),
    )
    content = {
        "evaluation_spec_id": evaluation_spec_id,
        "owner_id": owner_id,
        "action_support_rules": [rule.model_dump(mode="json")],
        "refinement_certificates": [item.model_dump(mode="json") for item in certificates],
    }
    return EvaluationSpecificationSpec(
        **content,
        specification_hash=_canonical_hash(content),
    )


def evaluate_robust_action_support(
    specification: EvaluationSpecificationSpec,
    *,
    action_type_id: str,
    evidence_state_id: str,
) -> tuple[bool, str]:
    """Evaluate support across every refinement in a validated finite certificate."""

    content = specification.model_dump(mode="json", exclude={"specification_hash"})
    if specification.specification_hash != _canonical_hash(content):
        raise CompilationError("EVALUATION_SPEC_HASH_MISMATCH", specification.evaluation_spec_id)
    rules = tuple(
        rule for rule in specification.action_support_rules
        if rule.action_type_id == action_type_id
    )
    if len(rules) != 1:
        raise CompilationError("EVALUATION_ACTION_RULE_INVALID", action_type_id)
    rule = rules[0]
    if (
        rule.implementation_id not in RULE_IMPLEMENTATIONS
        or rule.implementation_code_hash != implementation_code_hash(rule.implementation_id)
    ):
        raise CompilationError("EVALUATION_IMPLEMENTATION_HASH_MISMATCH", rule.implementation_id)
    certificates = tuple(
        certificate for certificate in specification.refinement_certificates
        if certificate.evidence_state_id == evidence_state_id
    )
    if len(certificates) != 1 or not certificates[0].refinements:
        raise CompilationError("EVALUATION_REFINEMENT_CERTIFICATE_INVALID", evidence_state_id)
    certificate = certificates[0]
    parameters = {
        "support_condition_refs": [
            {"object_id": condition_id} for condition_id in rule.support_condition_ids
        ],
    }
    supported = all(
        bool(RULE_IMPLEMENTATIONS[rule.implementation_id](
            {"evidence_state": {
                "satisfied_support_condition_ids": refinement.satisfied_support_condition_ids,
            }},
            parameters,
        ))
        for refinement in certificate.refinements
    )
    return supported, certificate.certificate_id


class CompiledConfigurationSpec(FrozenModel):
    configuration_id: str
    process_profile: ProcessProfileSpec
    policy_profile: PolicyProfileSpec
    evaluation_spec_id: str
    evaluation_specification: EvaluationSpecificationSpec
    application_mapping_id: str | None
    overlay_id: str
    receipts: tuple[BindingReceipt, ...]
    unresolved_parameter_slot_ids: tuple[str, ...] = ()
    compiler_code_hash: str


def _compiler_hash() -> str:
    return sha256(inspect.getsource(compile_configuration).encode()).hexdigest()


def compile_configuration(
    *,
    configuration_id: str,
    process: ProcessProfileSpec,
    policy: PolicyProfileSpec,
    overlay: ScenarioOverlaySpec,
    evaluation_spec_id: str,
    evaluation_specification: EvaluationSpecificationSpec | None = None,
    application_mapping_id: str | None = None,
) -> CompiledConfigurationSpec:
    evaluation = evaluation_specification or period_evidence_evaluation_specification(
        evaluation_spec_id
    )
    if evaluation.evaluation_spec_id != evaluation_spec_id:
        raise CompilationError(
            "EVALUATION_SPEC_ID_MISMATCH",
            f"{evaluation_spec_id} != {evaluation.evaluation_spec_id}",
        )
    for evidence_state_id in (SUPPORTED_EVIDENCE_STATE_ID, UNRESOLVED_EVIDENCE_STATE_ID):
        evaluate_robust_action_support(
            evaluation,
            action_type_id="progress",
            evidence_state_id=evidence_state_id,
        )
    if not policy.required_capabilities <= process.capabilities:
        missing = sorted(policy.required_capabilities - process.capabilities)
        raise CompilationError("PROFILE_POLICY_PROCESS_OVERLAP", f"undeclared capabilities: {missing}")
    if not policy.required_action_type_ids <= process.action_type_ids:
        missing = sorted(policy.required_action_type_ids - process.action_type_ids)
        raise CompilationError("PROFILE_POLICY_PROCESS_OVERLAP", f"undeclared actions: {missing}")
    required = process.parameter_slot_ids | policy.parameter_slot_ids
    documented: dict[str, ParameterValue] = {}
    unsupported: set[str] = set()
    for parameter in process.documented_parameters:
        if parameter.slot_id not in process.parameter_slot_ids:
            raise CompilationError("SCENARIO_PARAMETER_INVALID", parameter.slot_id)
        if parameter.provenance == "unsupported":
            unsupported.add(parameter.slot_id)
        else:
            documented[parameter.slot_id] = parameter
    overlay_values: dict[str, ParameterValue] = {}
    for parameter in overlay.parameters:
        if parameter.slot_id not in required:
            raise CompilationError("SCENARIO_PARAMETER_INVALID", parameter.slot_id)
        if parameter.slot_id in documented:
            raise CompilationError("PROFILE_PARAMETER_CONFLICT", parameter.slot_id)
        if parameter.slot_id in overlay_values:
            raise CompilationError("PROFILE_PARAMETER_CONFLICT", parameter.slot_id)
        if parameter.provenance not in {"stylized", "sensitivity"}:
            raise CompilationError("SCENARIO_PARAMETER_INVALID", "overlay value must be stylized or sensitivity")
        overlay_values[parameter.slot_id] = parameter
    receipts: list[BindingReceipt] = []
    for slot_id in sorted(required):
        parameter = documented.get(slot_id) or overlay_values.get(slot_id)
        if parameter is None or parameter.value is None:
            code = "PROFILE_UNSUPPORTED_PARAMETER" if slot_id in unsupported else "SCENARIO_CONFIGURATION_INCOMPLETE"
            raise CompilationError(code, slot_id)
        receipts.append(BindingReceipt(slot_id=slot_id, owner_id=parameter.owner_id, provenance=parameter.provenance, value=parameter.value))
    return CompiledConfigurationSpec(
        configuration_id=configuration_id,
        process_profile=process,
        policy_profile=policy,
        evaluation_spec_id=evaluation_spec_id,
        evaluation_specification=evaluation,
        application_mapping_id=application_mapping_id,
        overlay_id=overlay.overlay_id,
        receipts=tuple(receipts),
        compiler_code_hash=_compiler_hash(),
    )
