"""R-OCI source-fixture adapter into generic profile contracts."""

from __future__ import annotations

from pathlib import Path

import yaml

from ..configuration import ParameterValue, PolicyProfileSpec, ProcessProfileSpec


SEMANTIC_CAPABILITIES = frozenset({"notice", "response", "representation", "routing", "review", "progression", "correction", "restoration"})


def load_early_adapter(path: Path) -> tuple[ProcessProfileSpec, PolicyProfileSpec]:
    source = yaml.safe_load(path.read_text(encoding="utf-8"))
    if source["profile_id"] != "R-OCI-Early" or source["profile_version"] != 1:
        raise ValueError("PROFILE_APPLICATION_MAPPING_INVALID")
    parameters: list[ParameterValue] = []
    slot_map = {
        "response_days": "response_deadline",
        "queue_capacity": "review_capacity",
        "service_time_distribution": "review_service_time",
    }
    for source_name, slot in slot_map.items():
        item = source["historical_parameters"][source_name]
        provenance = "documented" if item["provenance"] == "documented" else "unsupported"
        parameters.append(ParameterValue(slot_id=slot, value=item["value"], provenance=provenance, owner_id="R-OCI-Early@1"))
    process = ProcessProfileSpec(
        profile_id="R-OCI-Early-CAPABILITIES@1",
        stage_ids=tuple(dict.fromkeys([transition["from"] for transition in source["transitions"]] + [transition["to"] for transition in source["transitions"]])),
        capabilities=SEMANTIC_CAPABILITIES,
        action_type_ids=frozenset({"hold", "request_evidence", "review", "progress", "correct", "restore"}),
        parameter_slot_ids=frozenset({"notice_delay", "response_deadline", "review_capacity", "review_service_time"}),
        documented_parameters=tuple(parameters),
    )
    policy = PolicyProfileSpec(
        profile_id="R-OCI-Early-HISTORICAL@1",
        required_capabilities=frozenset({"notice", "response", "representation", "routing", "progression", "correction"}),
        required_action_type_ids=frozenset({"progress", "correct"}),
        parameter_slot_ids=process.parameter_slot_ids,
        gate_semantics="none",
    )
    return process, policy
