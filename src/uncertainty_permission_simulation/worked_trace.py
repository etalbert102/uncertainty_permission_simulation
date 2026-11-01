"""Executable renderer for the prespecified Robodebt worked-trace pair."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

import yaml

from .applications.robodebt import load_early_stochastic_adapter
from .configuration import CompiledConfigurationSpec, compile_configuration
from .experiments import canonical_hash
from .profiles import policy
from .scenarios import overlay_from_mapping


TRACE_ARTIFACT_VERSION = 1


def _configuration_value(compiled: CompiledConfigurationSpec) -> dict[str, object]:
    return compiled.model_dump(mode="json")


def _event(event_id: str, day: int, event_type: str, details: Mapping[str, object]) -> dict[str, object]:
    return {
        "event_id": event_id,
        "day": day,
        "event_type": event_type,
        "details": dict(details),
    }


def _baseline_events(spec: Mapping[str, object]) -> list[dict[str, object]]:
    timing = spec["timing"]
    return [
        _event("B-01", int(timing["initiation_day"]), "SOURCE_EVIDENCE_INGESTED", {
            "evidence_type": "annual_aggregate",
            "provenance": "observed_aggregate",
            "amount": spec["case"]["aggregate_income"],
        }),
        _event("B-02", int(timing["initiation_day"]), "NOTICE_FAILED", {
            "status": "not_received_before_deadline",
        }),
        _event("B-03", int(timing["early_profile_response_deadline_day"]), "DEADLINE_REACHED", {
            "deadline_basis": "documented_early_profile_21_day_clock",
        }),
        _event("B-04", int(timing["baseline_progression_day"]), "REPRESENTATION_APPLIED", {
            "transformation": "aggregate_evenly_apportioned_across_periods",
            "inferential_status": "imputed",
            "uncertainty_surfaced": False,
        }),
        _event("B-05", int(timing["baseline_progression_day"]), "PROGRESSION_EXECUTED", {
            "action": "modeled_debt_assertion",
            "period_specific_support": False,
            "functional_permission": True,
            "formal_authority_claim": "source_attributed_only_not_decided_by_simulation",
        }),
        _event("B-06", int(timing["baseline_recovery_start_day"]), "EXTERNAL_CONSEQUENCE_STARTED", {
            "action": "modeled_recovery_exposure",
        }),
        _event("B-07", int(spec["access_and_evidence"]["later_recipient_evidence_available_day"]), "EVIDENCE_SUBMITTED", {
            "evidence_type": "period_specific_records",
            "provenance": "stylized_later_recipient_evidence",
        }),
        _event("B-08", int(timing["later_reassessment_day"]), "REASSESSMENT_COMPLETED", {
            "decision": "modeled_debt_reduced_or_zeroed",
        }),
        _event("B-09", int(timing["later_reassessment_day"]), "CORRECTION_EXECUTED", {
            "decision_state": "baseline",
            "recovery_state": "baseline",
        }),
        _event("B-10", int(timing["restoration_evaluation_day"]), "RESTORATION_EVALUATED", {
            "restoration_status": "partial",
            "residual_external_consequence": True,
        }),
    ]


def _repair_events(spec: Mapping[str, object]) -> list[dict[str, object]]:
    timing = spec["timing"]
    return [
        _event("R-01", int(timing["initiation_day"]), "SOURCE_EVIDENCE_INGESTED", {
            "evidence_type": "annual_aggregate",
            "provenance": "observed_aggregate",
            "amount": spec["case"]["aggregate_income"],
        }),
        _event("R-02", int(timing["initiation_day"]), "ACCESS_PROBLEM_RECORDED", {
            "notice_received_before_deadline": False,
        }),
        _event("R-03", int(timing["repair_information_request_day"]), "PROGRESSION_HELD", {
            "reason": "period_specific_support_missing",
        }),
        _event("R-04", int(timing["repair_information_request_day"]), "EVIDENCE_REQUESTED", {
            "owner": "agency",
            "evidence_type": "period_specific_records",
        }),
        _event("R-05", int(timing["repair_evidence_return_day"]), "EXTERNAL_EVIDENCE_RETURNED", {
            "retrieval_success": True,
            "provenance": "stylized_third_party_record",
        }),
        _event("R-06", int(timing["repair_supported_disposition_day"]), "SUPPORTED_DISPOSITION_RECORDED", {
            "period_specific_support": True,
            "action": "no_unsupported_progression",
        }),
        _event("R-07", int(timing["repair_supported_disposition_day"]), "CASE_CLOSED", {
            "external_consequence_started": False,
        }),
    ]


def _assessments() -> dict[str, list[dict[str, object]]]:
    shared_limit = "bounded explanatory trace; not representative, historical calibration, legal conclusion, or attackability evidence"
    baseline = [
        ("F0", "fail", "complete", "IMPUTATION_PROVENANCE_SUPPRESSED", "representation owner", "interface and policy owner", "surfacing may slow progression"),
        ("F1", "fail", "complete", "ROBUST_PERMISSION_VIOLATION", "permission-rule owner", "gate owner", "holding action delays disposition"),
        ("F2", "unassessable", "partial", "INTERVENTION_SCOPE_INCOMPLETE", "simulation owner", "simulation owner", "cohort spillovers are outside this one-case trace"),
        ("F3", "fail", "complete", "EFFECTIVE_REVIEW_ABSENT", "process owner", "review and gate owner", "pre-action review consumes capacity"),
        ("F4", "fail", "complete", "MATERIAL_UNCERTAINTY_NOT_SURFACED", "representation owner", "interface owner", "additional context may increase reviewer burden"),
        ("F5", "fail", "complete", "RESTORATION_PARTIAL", "reassessment owner", "restoration owner", "complete restoration may require broader remediation"),
    ]
    repair = [
        ("F0", "pass", "complete", "EVIDENCE_STATUS_PRESERVED", "evidence owner", "information-service owner", "evidence acquisition adds workload"),
        ("F1", "pass", "complete", "PROGRESSION_WITHHELD_UNTIL_SUPPORTED", "permission-rule owner", "gate owner", "supported disposition takes longer"),
        ("F2", "unassessable", "partial", "INTERVENTION_SCOPE_INCOMPLETE", "simulation owner", "simulation owner", "cohort spillovers are outside this one-case trace"),
        ("F3", "not_applicable", "complete", "NO_PRE_ACTION_PROGRESSION_REQUIRING_REVIEW", "process owner", "policy owner", "a different progression path could require review"),
        ("F4", "pass", "complete", "ACTION_RELEVANT_EVIDENCE_SURFACED", "representation owner", "interface owner", "surfacing requires provenance maintenance"),
        ("F5", "not_applicable", "complete", "NO_ADVERSE_ACTION_OR_RESTORATION_DUE", "process owner", "policy owner", "avoidance is not evidence of restoration capability"),
    ]

    def render(rows: list[tuple[str, str, str, str, str, str, str]], arm: str) -> list[dict[str, object]]:
        return [
            {
                "arm": arm,
                "application_level": "bounded_deterministic_trace",
                "evaluation_state": "assessed",
                "property_id": property_id,
                "status": status,
                "completeness": completeness,
                "diagnostic": diagnostic,
                "diagnostic_owner": diagnostic_owner,
                "intervention_owner": intervention_owner,
                "tradeoff": tradeoff,
                "claim_limit": shared_limit,
            }
            for property_id, status, completeness, diagnostic, diagnostic_owner, intervention_owner, tradeoff in rows
        ]

    return {"baseline": render(baseline, "baseline"), "repair": render(repair, "repair")}


def build_worked_trace(root: Path, pilot_config_path: Path) -> dict[str, object]:
    spec_path = root / "data/scenarios/worked_trace_spec_v1.yaml"
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    pilot = yaml.safe_load(pilot_config_path.read_text(encoding="utf-8"))
    overlay_values = dict(pilot["base_overlay"])
    overlay_values.update({
        "overlay_id": "RB-WORKED-TRACE-STYLIZED-OVERLAY@1",
        "initiation_window": "1",
        "response_deadline": "21",
        "administrative_cutoff": "60",
    })
    overlay = overlay_from_mapping(overlay_values)
    process, _ = load_early_stochastic_adapter(root / "data/sources/robodebt/r_oci_early.yaml")
    baseline = compile_configuration(
        configuration_id="RB-WORKED-TRACE-001-U1",
        process=process,
        policy=policy("U1"),
        overlay=overlay.to_compilation_overlay(exclude_slot_ids=frozenset({"response_deadline"})),
        evaluation_spec_id="RB-WORKED-TRACE-EVALUATION@1",
        application_mapping_id="R-OCI-EARLY-WORKED-TRACE-MAPPING@1",
    )
    counterfactual_process = process.model_copy(update={
        "profile_id": "R-OCI-EARLY-COUNTERFACTUAL-CAPABILITIES@1",
        "capabilities": process.capabilities | {"assistance", "extension", "evidence_acquisition"},
    })
    repair = compile_configuration(
        configuration_id="RB-WORKED-TRACE-001-U3",
        process=counterfactual_process,
        policy=policy("U3"),
        overlay=overlay.to_compilation_overlay(exclude_slot_ids=frozenset({"response_deadline"})),
        evaluation_spec_id="RB-WORKED-TRACE-EVALUATION@1",
        application_mapping_id="R-OCI-EARLY-WORKED-TRACE-MAPPING@1",
    )
    held_value = {
        "case": spec["case"],
        "access_and_evidence": spec["access_and_evidence"],
        "timing": spec["timing"],
        "evaluation_specification_id": "RB-WORKED-TRACE-EVALUATION@1",
    }
    artifact = {
        "schema_version": TRACE_ARTIFACT_VERSION,
        "artifact_kind": "prespecified_worked_trace",
        "specification_id": spec["specification_id"],
        "specification_version": spec["specification_version"],
        "specification_hash": sha256(spec_path.read_bytes()).hexdigest(),
        "held_input_hash": canonical_hash(held_value),
        "randomness": {"mode": "deterministic", "keyed_draws": []},
        "compilation": {
            "baseline": _configuration_value(baseline),
            "repair": _configuration_value(repair),
            "counterfactual_process_extension": {
                "provenance": "stylized_counterfactual",
                "capabilities": ["assistance", "evidence_acquisition", "extension"],
                "historical_claim": False,
            },
        },
        "arms": {
            "baseline": {"policy_id": "U1", "events": _baseline_events(spec)},
            "repair": {"policy_id": "U3", "events": _repair_events(spec)},
        },
        "assessments": _assessments(),
        "claim_limits": spec["claim_limits"],
    }
    artifact["artifact_hash"] = canonical_hash(artifact)
    return artifact


def _render_packet(artifact: Mapping[str, object]) -> str:
    lines = [
        "# Robodebt Worked-Trace Cold-Reader Packet",
        "",
        "Packet version: `1.0-candidate`",
        "",
        "Use only this packet and the supplied protocol. The expected profile is withheld.",
        "This is a bounded explanatory trace, not a historical reconstruction or legal conclusion.",
        "",
        f"Specification: `{artifact['specification_id']}`",
        f"Held-input hash: `{artifact['held_input_hash']}`",
        "",
    ]
    for arm_name, arm in artifact["arms"].items():
        lines.extend([f"## {arm_name.title()} arm (`{arm['policy_id']}`)", "", "| Day | Event | Relevant details |", "| ---: | --- | --- |"])
        for event in arm["events"]:
            details = "; ".join(f"{key}={value}" for key, value in sorted(event["details"].items()))
            lines.append(f"| {event['day']} | `{event['event_type']}` | {details} |")
        lines.extend(["", "Apply the protocol and record F0–F5 separately. Do not produce a composite score.", ""])
    lines.extend([
        "## Required claim boundary",
        "",
        "Record application level, evaluation state, status, completeness, located transition, evidence, diagnostic, missing information, diagnostic owner, intervention owner, tradeoff, ambiguity, and claim limit for every row.",
        "Do not infer historical prevalence, legal validity, or adversarial exploitability.",
        "",
    ])
    return "\n".join(lines)


def _render_oracle(artifact: Mapping[str, object]) -> str:
    lines = [
        "# Robodebt Worked-Trace Withheld Expected Profile",
        "",
        "Oracle version: `1.0-candidate`",
        "",
        f"Artifact hash: `{artifact['artifact_hash']}`",
        "",
    ]
    for arm_name, assessments in artifact["assessments"].items():
        lines.extend([f"## {arm_name.title()} arm", "", "| Property | Status | Completeness | Diagnostic | Diagnostic owner | Intervention owner | Tradeoff |", "| --- | --- | --- | --- | --- | --- | --- |"])
        for row in assessments:
            lines.append(
                f"| {row['property_id']} | `{row['status']}` | `{row['completeness']}` | `{row['diagnostic']}` | {row['diagnostic_owner']} | {row['intervention_owner']} | {row['tradeoff']} |"
            )
        lines.append("")
    lines.extend(["## Shared claim limit", "", artifact["assessments"]["baseline"][0]["claim_limit"], ""])
    return "\n".join(lines)


def write_worked_trace_artifacts(root: Path, pilot_config_path: Path) -> dict[str, object]:
    artifact = build_worked_trace(root, pilot_config_path)
    artifact_path = root / "data/golden_traces/robodebt_worked_trace_v1.json"
    artifact_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / "docs/ROBODEBT_WORKED_TRACE_PACKET.md").write_text(_render_packet(artifact), encoding="utf-8")
    (root / "docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md").write_text(_render_oracle(artifact), encoding="utf-8")
    return artifact
