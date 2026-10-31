"""Deterministic closed configuration compilation."""

from __future__ import annotations

from hashlib import sha256
import inspect
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


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


class CompiledConfigurationSpec(FrozenModel):
    configuration_id: str
    process_profile: ProcessProfileSpec
    policy_profile: PolicyProfileSpec
    evaluation_spec_id: str
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
    application_mapping_id: str | None = None,
) -> CompiledConfigurationSpec:
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
        application_mapping_id=application_mapping_id,
        overlay_id=overlay.overlay_id,
        receipts=tuple(receipts),
        compiler_code_hash=_compiler_hash(),
    )
