"""Deterministic closed configuration compilation."""

from __future__ import annotations

from hashlib import sha256
import inspect
import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, ValidationError

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
    generator_id: str
    generator_version: str
    generator_hash: str
    admissibility_assumptions: tuple[str, ...]
    excluded_refinement_classes: tuple[str, ...]
    coverage_argument: str
    proof_artifact_id: str
    conclusion_validity: Literal["universal_pass_and_failure"]
    refinements: tuple[RefinementStateSpec, ...]


class ActionSupportRuleSpec(FrozenModel):
    action_family_id: str
    implementation_id: str
    implementation_code_hash: str
    support_condition_ids: tuple[str, ...]


class ActionComparisonSchemaSpec(FrozenModel):
    schema_id: str
    material_field_names: tuple[str, ...]


class SymbolicActionFamilySpec(FrozenModel):
    action_family_id: str
    action_type_id: str
    actor_role_id: str
    target_binding: Literal["case_id"]
    parameter_vector: tuple[tuple[str, str], ...]
    operational_consequence: str
    authority_direction: str


class ActionInstanceSpec(FrozenModel):
    action_instance_id: str
    action_family_id: str
    action_type_id: str
    actor_role_id: str
    target_id: str
    parameter_vector: tuple[tuple[str, str], ...]
    operational_consequence: str
    authority_direction: str


class EvaluationSpecificationSpec(FrozenModel):
    schema_version: int
    artifact_kind: Literal["evaluation_specification"]
    evaluation_spec_id: str
    evaluation_spec_version: str
    owner_id: str
    evidence_universe: tuple[str, ...]
    action_comparison_schema: ActionComparisonSchemaSpec
    symbolic_action_families: tuple[SymbolicActionFamilySpec, ...]
    action_support_rules: tuple[ActionSupportRuleSpec, ...]
    refinement_certificates: tuple[RefinementCertificateSpec, ...]
    specification_hash: str


class RobustSupportReceipt(FrozenModel):
    evaluation_spec_id: str
    evaluation_specification_hash: str
    action_comparison_schema_id: str
    action_family_id: str
    action_instance_id: str
    action_instance_hash: str
    evidence_state_id: str
    refinement_certificate_id: str
    refinement_certificate_hash: str
    implementation_id: str
    implementation_code_hash: str
    robust_action_support: bool


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

    action_schema = ActionComparisonSchemaSpec(
        schema_id="PROGRESSION-ACTION-COMPARISON@2",
        material_field_names=(
            "action_family_id", "action_type_id", "actor_role_id", "target_id",
            "parameter_vector", "operational_consequence", "authority_direction",
        ),
    )
    action_family = SymbolicActionFamilySpec(
        action_family_id="CASE-PROGRESSION@2",
        action_type_id="progress",
        actor_role_id="SYSTEM",
        target_binding="case_id",
        parameter_vector=(("disposition", "advance_to_recovery_eligible_state"),),
        operational_consequence="case_progresses_to_modeled_external_consequence_path",
        authority_direction="expands_progression",
    )
    rule = ActionSupportRuleSpec(
        action_family_id=action_family.action_family_id,
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
            generator_id="BINARY-PERIOD-EVIDENCE-ENUMERATOR",
            generator_version="2.0",
            generator_hash=_canonical_hash({
                "generator_id": "BINARY-PERIOD-EVIDENCE-ENUMERATOR",
                "generator_version": "2.0",
                "evidence_state_id": SUPPORTED_EVIDENCE_STATE_ID,
                "refinement_ids": ["REF-PERIOD-EVIDENCE-PRESENT"],
            }),
            admissibility_assumptions=(
                "The stylized kernel represents decision-relevant period evidence as present or absent.",
                "No latent evidence class exists inside the declared binary kernel state.",
            ),
            excluded_refinement_classes=(
                "Evidence quality, provenance, and partial sufficiency are outside this binary kernel.",
            ),
            coverage_argument="The supported state denotes one binary refinement: period evidence present.",
            proof_artifact_id="BINARY-ENUMERATION-PROOF@2",
            conclusion_validity="universal_pass_and_failure",
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
            generator_id="BINARY-PERIOD-EVIDENCE-ENUMERATOR",
            generator_version="2.0",
            generator_hash=_canonical_hash({
                "generator_id": "BINARY-PERIOD-EVIDENCE-ENUMERATOR",
                "generator_version": "2.0",
                "evidence_state_id": UNRESOLVED_EVIDENCE_STATE_ID,
                "refinement_ids": [
                    "REF-PERIOD-EVIDENCE-AVAILABLE", "REF-PERIOD-EVIDENCE-ABSENT",
                ],
            }),
            admissibility_assumptions=(
                "The stylized kernel represents unresolved evidence as compatible with presence or absence.",
                "No third evidence class exists inside the declared binary kernel state.",
            ),
            excluded_refinement_classes=(
                "Evidence quality, provenance, and partial sufficiency are outside this binary kernel.",
            ),
            coverage_argument="The unresolved state exhausts the two values of the declared binary evidence universe.",
            proof_artifact_id="BINARY-ENUMERATION-PROOF@2",
            conclusion_validity="universal_pass_and_failure",
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
        "schema_version": 2,
        "artifact_kind": "evaluation_specification",
        "evaluation_spec_id": evaluation_spec_id,
        "evaluation_spec_version": "2.0",
        "owner_id": owner_id,
        "evidence_universe": [SUPPORTED_EVIDENCE_STATE_ID, UNRESOLVED_EVIDENCE_STATE_ID],
        "action_comparison_schema": action_schema.model_dump(mode="json"),
        "symbolic_action_families": [action_family.model_dump(mode="json")],
        "action_support_rules": [rule.model_dump(mode="json")],
        "refinement_certificates": [item.model_dump(mode="json") for item in certificates],
    }
    return EvaluationSpecificationSpec(
        **content,
        specification_hash=_canonical_hash(content),
    )


def load_evaluation_specification(path: Path) -> EvaluationSpecificationSpec:
    """Load a separately owned, content-addressed evaluation specification."""

    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CompilationError("EVALUATION_SPEC_INVALID", str(path)) from exc
    if not isinstance(content, dict) or "specification_hash" in content:
        raise CompilationError(
            "EVALUATION_SPEC_INVALID",
            "stored specification must be a mapping without a self-authored hash",
        )
    try:
        specification = EvaluationSpecificationSpec(
            **content,
            specification_hash=_canonical_hash(content),
        )
    except ValidationError as exc:
        raise CompilationError("EVALUATION_SPEC_INVALID", str(path)) from exc
    declared_states = set(specification.evidence_universe)
    certified_states = {
        certificate.evidence_state_id
        for certificate in specification.refinement_certificates
    }
    if declared_states != {
        SUPPORTED_EVIDENCE_STATE_ID,
        UNRESOLVED_EVIDENCE_STATE_ID,
    } or certified_states != declared_states:
        raise CompilationError("EVALUATION_EVIDENCE_UNIVERSE_INVALID", str(path))
    for evidence_state_id in specification.evidence_universe:
        evaluate_robust_action_support(
            specification,
            action=progression_action_instance(specification, case_id="LOAD-PROBE"),
            evidence_state_id=evidence_state_id,
        )
    return specification


def progression_action_instance(
    specification: EvaluationSpecificationSpec,
    *,
    case_id: str,
) -> ActionInstanceSpec:
    families = tuple(
        family for family in specification.symbolic_action_families
        if family.action_type_id == "progress"
    )
    if len(families) != 1 or not case_id:
        raise CompilationError("EVALUATION_ACTION_FAMILY_INVALID", "progress")
    family = families[0]
    return ActionInstanceSpec(
        action_instance_id=f"{case_id}:PROGRESS",
        action_family_id=family.action_family_id,
        action_type_id=family.action_type_id,
        actor_role_id=family.actor_role_id,
        target_id=case_id,
        parameter_vector=family.parameter_vector,
        operational_consequence=family.operational_consequence,
        authority_direction=family.authority_direction,
    )


def evaluate_robust_action_support(
    specification: EvaluationSpecificationSpec,
    *,
    action: ActionInstanceSpec,
    evidence_state_id: str,
) -> RobustSupportReceipt:
    """Evaluate support across every refinement in a validated finite certificate."""

    content = specification.model_dump(mode="json", exclude={"specification_hash"})
    if specification.specification_hash != _canonical_hash(content):
        raise CompilationError("EVALUATION_SPEC_HASH_MISMATCH", specification.evaluation_spec_id)
    required_material_fields = {
        "action_family_id", "action_type_id", "actor_role_id", "target_id",
        "parameter_vector", "operational_consequence", "authority_direction",
    }
    if set(specification.action_comparison_schema.material_field_names) != required_material_fields:
        raise CompilationError("EVALUATION_ACTION_COMPARISON_INVALID", specification.evaluation_spec_id)
    families = tuple(
        family for family in specification.symbolic_action_families
        if family.action_family_id == action.action_family_id
    )
    if len(families) != 1:
        raise CompilationError("EVALUATION_ACTION_FAMILY_INVALID", action.action_family_id)
    family = families[0]
    if action != progression_action_instance(specification, case_id=action.target_id):
        raise CompilationError("EVALUATION_ACTION_INSTANCE_INVALID", action.action_instance_id)
    rules = tuple(
        rule for rule in specification.action_support_rules
        if rule.action_family_id == action.action_family_id
    )
    if len(rules) != 1:
        raise CompilationError("EVALUATION_ACTION_RULE_INVALID", action.action_family_id)
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
    if (
        certificate.coverage_mode != "finite_exact"
        or certificate.conclusion_validity != "universal_pass_and_failure"
        or not certificate.generator_id
        or not certificate.generator_version
        or not certificate.generator_hash
        or not certificate.admissibility_assumptions
        or not certificate.excluded_refinement_classes
        or not certificate.coverage_argument
        or not certificate.proof_artifact_id
        or len({item.refinement_id for item in certificate.refinements}) != len(certificate.refinements)
    ):
        raise CompilationError("EVALUATION_REFINEMENT_CERTIFICATE_INVALID", evidence_state_id)
    generator_input = {
        "generator_id": certificate.generator_id,
        "generator_version": certificate.generator_version,
        "evidence_state_id": certificate.evidence_state_id,
        "refinement_ids": [item.refinement_id for item in certificate.refinements],
    }
    if certificate.generator_hash != _canonical_hash(generator_input):
        raise CompilationError("EVALUATION_GENERATOR_HASH_MISMATCH", certificate.certificate_id)
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
    return RobustSupportReceipt(
        evaluation_spec_id=specification.evaluation_spec_id,
        evaluation_specification_hash=specification.specification_hash,
        action_comparison_schema_id=specification.action_comparison_schema.schema_id,
        action_family_id=family.action_family_id,
        action_instance_id=action.action_instance_id,
        action_instance_hash=_canonical_hash(action.model_dump(mode="json")),
        evidence_state_id=evidence_state_id,
        refinement_certificate_id=certificate.certificate_id,
        refinement_certificate_hash=_canonical_hash(certificate.model_dump(mode="json")),
        implementation_id=rule.implementation_id,
        implementation_code_hash=rule.implementation_code_hash,
        robust_action_support=supported,
    )


class CompiledConfigurationSpec(FrozenModel):
    configuration_id: str
    process_profile: ProcessProfileSpec
    policy_profile: PolicyProfileSpec
    evaluation_spec_id: str
    evaluation_specification: EvaluationSpecificationSpec
    evaluation_specification_origin: Literal["external", "generated_development_fixture"]
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
        evaluation_spec_id,
        owner_id="GENERATED-DEVELOPMENT-FIXTURE",
    )
    evaluation_origin = (
        "external" if evaluation_specification is not None
        else "generated_development_fixture"
    )
    if evaluation.evaluation_spec_id != evaluation_spec_id:
        raise CompilationError(
            "EVALUATION_SPEC_ID_MISMATCH",
            f"{evaluation_spec_id} != {evaluation.evaluation_spec_id}",
        )
    for evidence_state_id in (SUPPORTED_EVIDENCE_STATE_ID, UNRESOLVED_EVIDENCE_STATE_ID):
        evaluate_robust_action_support(
            evaluation,
            action=progression_action_instance(evaluation, case_id="COMPILATION-PROBE"),
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
        evaluation_specification_origin=evaluation_origin,
        application_mapping_id=application_mapping_id,
        overlay_id=overlay.overlay_id,
        receipts=tuple(receipts),
        compiler_code_hash=_compiler_hash(),
    )
