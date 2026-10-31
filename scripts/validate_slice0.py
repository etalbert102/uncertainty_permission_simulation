"""Validate Slice 0 research-contract artifacts without importing simulator code."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "AGENTS.md",
    "README.md",
    "data/model/schema_manifest_v1.yaml",
    "data/scenarios/worked_trace_spec_v1.yaml",
    "data/sources/robodebt/source_manifest.yaml",
    "data/sources/robodebt/r_oci_early.yaml",
    "data/sources/robodebt/r_oci_enhanced.yaml",
    "docs/ARTICLE_OUTLINE.md",
    "docs/COLD_READER_DISTRIBUTION.md",
    "docs/COLD_READER_QA_RECEIPT.md",
    "docs/CONTINUITY_AND_CLAIM_BOUNDARY.md",
    "docs/CONFIGURATION_COMPILATION.md",
    "docs/DEFERRED.md",
    "docs/EXECUTION_LEDGER.md",
    "docs/FORMAL_MODEL.md",
    "docs/LITERATURE_AND_ORIGINALITY_MAP.md",
    "docs/P0_COLD_READER_PACKET.md",
    "docs/P0_USABILITY_WALKTHROUGH.md",
    "docs/PLAN_COMPLETION_RECEIPT.md",
    "docs/PRECURSOR_FIDELITY_FIXTURE.md",
    "docs/PREREGISTRATION.md",
    "docs/PROCESS_RED_TEAM_PROTOCOL.md",
    "docs/ROBODEBT_CASE_STUDY.md",
    "docs/STUDY_PLAN.md",
    "docs/TRANSFER_CANARY.md",
    "docs/TRANSFER_CANARY_EXPECTED_PROFILE.md",
    "docs/WORKED_TRACE_SELECTION.md",
    "scripts/build_cold_reader_bundle.py",
    "scripts/validate_plan.py",
}

BLINDED_PACKETS = {
    "docs/P0_COLD_READER_PACKET.md",
    "docs/TRANSFER_CANARY.md",
}

FORBIDDEN_BLINDED_PATTERNS = {
    r"\bFM_[A-Z0-9_]+\b": "formal diagnostic code",
    r"\bP0_[A-Z0-9_]+\b": "fixture diagnostic code",
    r"\bSCHEMA_[A-Z0-9_]+\b": "schema diagnostic code",
    r"\bSIM_[A-Z0-9_]+\b": "simulation diagnostic code",
    r"expected profile": "expected-profile label",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(
                f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}"
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping
)


def load_yaml(relative: str) -> object:
    path = ROOT / relative
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UniqueKeyLoader)


def nested_source_refs(value: object) -> Iterable[str]:
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "source_refs" and isinstance(item, list):
                for ref in item:
                    if isinstance(ref, str):
                        yield ref
            yield from nested_source_refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from nested_source_refs(item)


def validate_source_ref(
    ref: str, source_ids: set[str], anchors: dict[str, set[str]], claim_ids: set[str]
) -> None:
    if ref in claim_ids:
        return
    source_id, separator, anchor_id = ref.partition("#")
    if source_id not in source_ids:
        raise ValueError(f"unknown source or claim reference: {ref}")
    if separator and anchor_id not in anchors[source_id]:
        raise ValueError(f"unknown anchor reference: {ref}")


def validate_markdown() -> None:
    local_link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        relative = path.relative_to(ROOT)
        if any(part in {".git", ".venv", "build", "dist"} for part in relative.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if text.count("```") % 2:
            raise ValueError(f"unbalanced Markdown fence: {relative}")
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                raise ValueError(
                    f"trailing whitespace: {relative}:{line_number}"
                )
        for target in local_link.findall(text):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            clean_target = target.split("#", 1)[0]
            if clean_target and not (path.parent / clean_target).resolve().exists():
                raise ValueError(
                    f"broken local link: {relative} -> {target}"
                )


def validate_blinded_packets() -> None:
    for relative in BLINDED_PACKETS:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for pattern, label in FORBIDDEN_BLINDED_PATTERNS.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                raise ValueError(f"{label} leaked into blinded packet {relative}")
        if re.search(
            r"\b(pass|fail|unassessable|not_applicable)\s*[/,:-]\s*(complete|incomplete|invalid)\b",
            text,
            flags=re.IGNORECASE,
        ):
            raise ValueError(f"status/completeness answer pair leaked into {relative}")


def validate_configuration_architecture(schema_manifest: dict[object, object]) -> None:
    payload_kinds = schema_manifest.get("payload_kinds")
    if not isinstance(payload_kinds, dict):
        raise ValueError("schema manifest requires payload_kinds")

    required_payloads = {
        "TemporalScope",
        "ProcessProfile",
        "PolicyProfile",
        "SourceApplicationFixture",
        "ApplicationBinding",
        "ApplicationMapping",
        "ScenarioParameter",
        "ScenarioOverlay",
        "ParameterBindingReceipt",
        "CompiledConfiguration",
        "CaseAttribute",
        "SimulationCase",
        "Scenario",
        "Run",
    }
    missing_payloads = sorted(required_payloads - set(payload_kinds))
    if missing_payloads:
        raise ValueError(f"configuration contract payloads missing: {missing_payloads}")

    event_ids = schema_manifest.get("closed_event_type_ids")
    if not isinstance(event_ids, list) or len(event_ids) != len(set(event_ids)):
        raise ValueError("closed event registry is missing, malformed, or duplicated")
    forbidden_event_tokens = ("CUSTOMER", "DEBT", "RECOVERY", "INCOME", "ROBODEBT", "OCI")
    leaked_event_ids = sorted(
        event_id
        for event_id in event_ids
        if any(token in event_id for token in forbidden_event_tokens)
    )
    if leaked_event_ids:
        raise ValueError(f"application-specific kernel event IDs: {leaked_event_ids}")
    required_event_ids = {
        "SUBJECT_RESPONDED",
        "SUBJECT_NONRESPONSE",
        "PROGRESSION_EXECUTED",
        "EXTERNAL_CONSEQUENCE_STARTED",
        "CORRECTION_REQUESTED",
        "RESTORATION_EXECUTED",
    }
    if not required_event_ids.issubset(event_ids):
        raise ValueError("generic kernel event families are incomplete")

    def fields(payload_name: str) -> set[str]:
        payload = payload_kinds[payload_name]
        if not isinstance(payload, dict) or not isinstance(payload.get("fields"), dict):
            raise ValueError(f"payload fields missing: {payload_name}")
        return set(payload["fields"])

    case_fields = fields("SimulationCase")
    forbidden_case_fields = {"latent_income", "debt", "recovery", "recipient_id"}
    if case_fields & forbidden_case_fields:
        raise ValueError(
            f"application-specific SimulationCase fields: {sorted(case_fields & forbidden_case_fields)}"
        )
    if not {
        "case_kind_id",
        "latent_state_attribute_refs",
        "administrative_access_attribute_refs",
    }.issubset(case_fields):
        raise ValueError("SimulationCase lacks generic case-attribute bindings")

    process_fields = fields("ProcessProfile")
    if {"effective_start", "effective_end"} & process_fields:
        raise ValueError("ProcessProfile bypasses mixed-precision TemporalScope")
    if not {"temporal_scope_ref", "action_type_ids", "parameter_slot_ids"}.issubset(
        process_fields
    ):
        raise ValueError("ProcessProfile lacks capability or temporal contracts")

    policy_fields = fields("PolicyProfile")
    required_policy_fields = {
        "transformation_rule_refs",
        "routing_rule_refs",
        "permission_rule_refs",
        "gate_policy_rule_refs",
        "timeout_rule_refs",
        "correction_rule_refs",
        "restoration_rule_refs",
    }
    if not required_policy_fields.issubset(policy_fields):
        raise ValueError("PolicyProfile does not own the complete active behavior contract")

    queue_fields = fields("QueueConfig")
    if "capacity" in queue_fields or "capacity_parameter_slot_id" not in queue_fields:
        raise ValueError("QueueConfig must bind capacity through a declared parameter slot")

    scenario_fields = fields("Scenario")
    if "compiled_configuration_refs" not in scenario_fields or "policy_refs" in scenario_fields:
        raise ValueError("Scenario must reference compiled configurations, not loose policies")
    run_fields = fields("Run")
    if "compiled_configuration_ref" not in run_fields or "policy_ref" in run_fields:
        raise ValueError("Run must reference one compiled configuration")

    compiled_fields = fields("CompiledConfiguration")
    required_compiled_fields = {
        "process_profile_ref",
        "policy_profile_ref",
        "evaluation_spec_ref",
        "scenario_overlay_ref",
        "parameter_binding_receipt_refs",
        "compiler_code_hash",
        "unresolved_parameter_slot_ids",
    }
    if not required_compiled_fields.issubset(compiled_fields):
        raise ValueError("CompiledConfiguration lacks replay-complete inputs or receipts")

    gate_ids = {
        gate.get("id")
        for gate in schema_manifest.get("manifest_gates", [])
        if isinstance(gate, dict)
    }
    if "SCHEMA_CONFIGURATION_COMPOSITION" not in gate_ids:
        raise ValueError("configuration-composition manifest gate is missing")


def main() -> int:
    missing = sorted(relative for relative in REQUIRED_FILES if not (ROOT / relative).is_file())
    if missing:
        raise ValueError(f"missing Slice 0 files: {missing}")

    yaml_paths = sorted(ROOT.rglob("*.yaml"))
    for path in yaml_paths:
        with path.open(encoding="utf-8") as handle:
            yaml.load(handle, Loader=UniqueKeyLoader)

    schema_manifest = load_yaml("data/model/schema_manifest_v1.yaml")
    if not isinstance(schema_manifest, dict):
        raise ValueError("schema manifest must be a mapping")
    validate_configuration_architecture(schema_manifest)
    closed_registry_keys = (
        "closed_diagnostic_codes",
        "closed_property_or_helper_ids",
        "closed_protocol_application_level_ids",
        "closed_report_evaluation_state_ids",
        "closed_run_status_ids",
        "closed_scenario_validity_status_ids",
    )
    for key in closed_registry_keys:
        values = schema_manifest.get(key)
        if not isinstance(values, list) or len(values) != len(set(values)):
            raise ValueError(f"closed registry is missing, malformed, or duplicated: {key}")
    closed_diagnostics = set(schema_manifest["closed_diagnostic_codes"])
    specification_text = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8")
        for relative in (
            "docs/FORMAL_MODEL.md",
            "docs/CONFIGURATION_COMPILATION.md",
            "docs/PRECURSOR_FIDELITY_FIXTURE.md",
            "docs/PROCESS_RED_TEAM_PROTOCOL.md",
        )
    )
    candidate_diagnostics = set(
        re.findall(r"\b(?:FM|P0|SCHEMA|SIM)_[A-Z0-9_]+\b", specification_text)
    )
    nondiagnostic_tokens = {
        "P0_COLD_READER_PACKET",
        "P0_USABILITY_WALKTHROUGH",
    }
    candidate_diagnostics = {
        token
        for token in candidate_diagnostics
        if token not in nondiagnostic_tokens and not token.startswith("P0_NO_")
    }
    unregistered = sorted(candidate_diagnostics - closed_diagnostics)
    if unregistered:
        raise ValueError(f"unregistered diagnostic-like tokens: {unregistered}")
    configuration_text = (ROOT / "docs/CONFIGURATION_COMPILATION.md").read_text(
        encoding="utf-8"
    )
    configuration_diagnostics = set(
        re.findall(r"\b(?:PROFILE|SCENARIO)_[A-Z0-9_]+\b", configuration_text)
    )
    unregistered_configuration = sorted(configuration_diagnostics - closed_diagnostics)
    if unregistered_configuration:
        raise ValueError(
            "unregistered configuration diagnostics: "
            f"{unregistered_configuration}"
        )

    manifest = load_yaml("data/sources/robodebt/source_manifest.yaml")
    if not isinstance(manifest, dict):
        raise ValueError("source manifest must be a mapping")
    source_rows = manifest.get("sources")
    claim_rows = manifest.get("claims")
    if not isinstance(source_rows, list) or not isinstance(claim_rows, list):
        raise ValueError("source manifest requires source and claim lists")

    source_ids = {row["source_id"] for row in source_rows}
    if len(source_ids) != len(source_rows):
        raise ValueError("duplicate source_id")
    claim_ids = {row["claim_id"] for row in claim_rows}
    if len(claim_ids) != len(claim_rows):
        raise ValueError("duplicate claim_id")
    anchors = {
        row["source_id"]: {
            anchor["anchor_id"] for anchor in row.get("anchors", [])
        }
        for row in source_rows
    }

    for row in source_rows:
        if row.get("local_copy") is False and row.get("content_hash") is not None:
            raise ValueError(f"remote-only source has unexpected content hash: {row['source_id']}")
    for claim in claim_rows:
        for ref in claim.get("source_refs", []):
            validate_source_ref(ref, source_ids, anchors, claim_ids)

    profiles = [
        load_yaml("data/sources/robodebt/r_oci_early.yaml"),
        load_yaml("data/sources/robodebt/r_oci_enhanced.yaml"),
    ]
    profile_keys: set[str] = set()
    for profile in profiles:
        if not isinstance(profile, dict):
            raise ValueError("profile must be a mapping")
        key = f"{profile['profile_id']}@{profile['profile_version']}"
        if key in profile_keys:
            raise ValueError(f"duplicate profile key: {key}")
        profile_keys.add(key)
        temporal_scope = profile.get("temporal_scope")
        if not isinstance(temporal_scope, dict) or not temporal_scope.get(
            "temporal_scope_id"
        ):
            raise ValueError(f"{key} must declare a versionable temporal scope")
        compilation_contract = profile.get("compilation_contract")
        expected_contract = {
            "source_fixture_role": "immutable_application_input",
            "compile_outputs": [
                "process_capability_profile",
                "historical_policy_profile",
            ],
            "raw_descriptions_and_guards_executable": False,
            "unsupported_parameters_supply_runtime_values": False,
        }
        if compilation_contract != expected_contract:
            raise ValueError(f"{key} has an invalid source-fixture compilation contract")
        for claim_ref in profile.get("source_claim_refs", []):
            if claim_ref not in claim_ids:
                raise ValueError(f"unknown profile claim ref: {claim_ref}")
        for ref in nested_source_refs(profile):
            validate_source_ref(ref, source_ids, anchors, claim_ids)
        parameters = profile.get("historical_parameters", {})
        for parameter_name in (
            "queue_capacity",
            "service_time_distribution",
            "engagement_probability",
            "evidence_retrieval_distribution",
        ):
            parameter = parameters.get(parameter_name)
            if parameter != {"value": None, "provenance": "unsupported"}:
                raise ValueError(
                    f"{key} must keep {parameter_name} explicitly unsupported"
                )

    enhanced_scope = profiles[1]["temporal_scope"]
    if enhanced_scope.get("mode") != "as_documented_bundle":
        raise ValueError("enhanced profile must remain an as-documented temporal bundle")
    if enhanced_scope.get("simultaneous_activation_claimed") is not False:
        raise ValueError("enhanced profile cannot claim simultaneous activation")

    worked_trace = load_yaml("data/scenarios/worked_trace_spec_v1.yaml")
    if not isinstance(worked_trace, dict):
        raise ValueError("worked-trace specification must be a mapping")
    if worked_trace.get("profile_ref") not in profile_keys:
        raise ValueError("worked trace references an unknown profile version")
    if worked_trace.get("configuration_role") != "stylized_scenario_overlay":
        raise ValueError("worked trace must declare its stylized overlay role")
    profile_boundary = worked_trace.get("profile_boundary", "")
    if "documented structure only" not in profile_boundary:
        raise ValueError("worked trace must preserve the source-profile/overlay boundary")
    expected_compilation_requirements = {
        "process_profile_role": "source_grounded_capability_graph",
        "policy_profile_source": "comparison_arm",
        "evaluation_specification_required": True,
        "parameter_binding_receipt_required_per_runtime_slot": True,
        "unresolved_parameter_slot_count": 0,
        "documented_value_overwrite_allowed": False,
        "raw_source_description_executable": False,
    }
    if worked_trace.get("compilation_requirements") != expected_compilation_requirements:
        raise ValueError("worked trace lost compiled-configuration closure")
    if worked_trace.get("randomness") != {"mode": "deterministic", "keyed_draws": []}:
        raise ValueError("worked trace must remain deterministic with zero draws")

    validate_markdown()
    validate_blinded_packets()

    study_plan = (ROOT / "docs/STUDY_PLAN.md").read_text(encoding="utf-8")
    if "P0 must not be mislabeled as a Robodebt trace" not in study_plan:
        raise ValueError("study plan lost the P0/Robodebt packet boundary")
    for required_boundary in (
        "case-neutral study kernel",
        "Minimum defensible case threshold",
        "External QA gate",
        "stylized scenario overlay",
    ):
        if required_boundary not in study_plan:
            raise ValueError(
                f"study plan lost flexible-kernel boundary: {required_boundary}"
            )
    agent_contract = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "may not branch on `Robodebt`" not in agent_contract:
        raise ValueError("agent contract permits case-specific kernel behavior")
    if "no stochastic simulator or confirmatory results" not in (
        ROOT / "README.md"
    ).read_text(encoding="utf-8").lower():
        raise ValueError("README must state the no-results boundary")

    print(
        f"SLICE0_VALID sources={len(source_ids)} claims={len(claim_ids)} "
        f"profiles={len(profile_keys)} yaml_files={len(yaml_paths)} "
        f"diagnostics={len(closed_diagnostics)}"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyError, TypeError, ValueError, yaml.YAMLError) as error:
        print(f"SLICE0_INVALID {error}", file=sys.stderr)
        sys.exit(1)
