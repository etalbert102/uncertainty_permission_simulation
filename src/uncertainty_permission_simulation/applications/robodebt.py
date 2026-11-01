"""R-OCI source-fixture adapter into generic profile contracts."""

from __future__ import annotations

from pathlib import Path

import yaml

from ..configuration import ParameterValue, PolicyProfileSpec, ProcessProfileSpec
from ..profiles import CORE_SLOTS, STOCHASTIC_SLOTS


SLICE1_CAPABILITIES = frozenset({
    "notice", "response", "representation", "routing", "review", "progression",
    "correction", "restoration",
})
SEMANTIC_CAPABILITIES = frozenset({
    "notice", "response", "representation", "routing", "review", "progression",
    "recovery", "correction", "reassessment", "restoration",
})
SEMANTIC_ACTIONS = frozenset({
    "hold", "request_evidence", "review", "progress", "recover", "correct",
    "reassess", "restore",
})
KERNEL_STAGES = (
    "arrival", "notice", "response", "routing", "review", "action", "recovery",
    "correction", "reassessment", "restoration", "closed",
)
KERNEL_SLOTS = CORE_SLOTS | STOCHASTIC_SLOTS


def _parameter(
    source: dict[str, object],
    source_name: str,
    slot_id: str,
    owner_id: str,
) -> ParameterValue:
    item = source["historical_parameters"][source_name]
    provenance = "documented" if item["provenance"] == "documented" else "unsupported"
    return ParameterValue(
        slot_id=slot_id,
        value=item["value"],
        provenance=provenance,
        owner_id=owner_id,
    )


def load_early_adapter(path: Path) -> tuple[ProcessProfileSpec, PolicyProfileSpec]:
    source = yaml.safe_load(path.read_text(encoding="utf-8"))
    if source["profile_id"] != "R-OCI-Early" or source["profile_version"] != 1:
        raise ValueError("PROFILE_APPLICATION_MAPPING_INVALID")
    parameters = tuple(
        _parameter(source, source_name, slot_id, "R-OCI-Early@1")
        for source_name, slot_id in {
            "response_days": "response_deadline",
            "queue_capacity": "review_capacity",
            "service_time_distribution": "review_service_time",
        }.items()
    )
    source_stages = tuple(dict.fromkeys(
        [transition["from"] for transition in source["transitions"]]
        + [transition["to"] for transition in source["transitions"]]
    ))
    process = ProcessProfileSpec(
        profile_id="R-OCI-Early-CAPABILITIES@1",
        stage_ids=source_stages,
        capabilities=SLICE1_CAPABILITIES,
        action_type_ids=frozenset({
            "hold", "request_evidence", "review", "progress", "correct", "restore",
        }),
        parameter_slot_ids=CORE_SLOTS,
        documented_parameters=parameters,
    )
    policy = PolicyProfileSpec(
        profile_id="R-OCI-Early-HISTORICAL@1",
        required_capabilities=frozenset({"notice", "response", "representation", "routing", "progression", "correction"}),
        required_action_type_ids=frozenset({"progress", "correct"}),
        parameter_slot_ids=process.parameter_slot_ids,
        gate_semantics="none",
    )
    return process, policy


def load_early_stochastic_adapter(
    path: Path,
) -> tuple[ProcessProfileSpec, PolicyProfileSpec]:
    source = yaml.safe_load(path.read_text(encoding="utf-8"))
    if source["profile_id"] != "R-OCI-Early" or source["profile_version"] != 1:
        raise ValueError("PROFILE_APPLICATION_MAPPING_INVALID")
    parameters = tuple(
        _parameter(source, source_name, slot_id, "R-OCI-Early@1")
        for source_name, slot_id in {
            "response_days": "response_deadline",
            "queue_capacity": "review_capacity",
            "service_time_distribution": "review_service_time",
        }.items()
    )
    source_stages = tuple(dict.fromkeys(
        [transition["from"] for transition in source["transitions"]]
        + [transition["to"] for transition in source["transitions"]]
    ))
    process = ProcessProfileSpec(
        profile_id="R-OCI-Early-STOCHASTIC-CAPABILITIES@1",
        stage_ids=tuple(dict.fromkeys(source_stages + KERNEL_STAGES)),
        capabilities=SEMANTIC_CAPABILITIES,
        action_type_ids=SEMANTIC_ACTIONS,
        parameter_slot_ids=KERNEL_SLOTS,
        documented_parameters=parameters,
    )
    historical = PolicyProfileSpec(
        profile_id="R-OCI-Early-STOCHASTIC-HISTORICAL@1",
        required_capabilities=frozenset({
            "notice", "response", "representation", "routing", "progression",
            "recovery", "correction", "reassessment",
        }),
        required_action_type_ids=frozenset({"progress", "recover", "correct", "reassess"}),
        parameter_slot_ids=process.parameter_slot_ids,
        gate_semantics="none",
    )
    return process, historical


def load_enhanced_adapter(path: Path) -> tuple[ProcessProfileSpec, PolicyProfileSpec]:
    source = yaml.safe_load(path.read_text(encoding="utf-8"))
    if source["profile_id"] != "R-OCI-Enhanced" or source["profile_version"] != 1:
        raise ValueError("PROFILE_APPLICATION_MAPPING_INVALID")
    owner_id = "R-OCI-Enhanced@1"
    parameters = tuple(
        _parameter(source, source_name, slot_id, owner_id)
        for source_name, slot_id in {
            "initial_response_days": "response_deadline",
            "queue_capacity": "review_capacity",
            "service_time_distribution": "review_service_time",
        }.items()
    )
    repair_stages = tuple(
        transition["target_transition"] for transition in source["repair_transitions"]
    )
    capabilities = SEMANTIC_CAPABILITIES | {
        "assistance", "extension", "evidence_acquisition",
    }
    process = ProcessProfileSpec(
        profile_id="R-OCI-Enhanced-CAPABILITIES@1",
        stage_ids=tuple(dict.fromkeys(repair_stages + KERNEL_STAGES)),
        capabilities=capabilities,
        action_type_ids=SEMANTIC_ACTIONS,
        parameter_slot_ids=KERNEL_SLOTS,
        documented_parameters=parameters,
    )
    policy = PolicyProfileSpec(
        profile_id="R-OCI-Enhanced-HISTORICAL@1",
        required_capabilities=frozenset({
            "notice", "response", "representation", "routing", "review",
            "progression", "recovery", "correction", "reassessment",
        }),
        required_action_type_ids=frozenset({"review", "progress", "recover", "correct", "reassess"}),
        parameter_slot_ids=process.parameter_slot_ids,
        gate_semantics="fail_closed",
    )
    return process, policy
