"""Machine-checkable intake for independent pre-freeze artifact QA returns."""

from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

from .schemas import MANIFEST


STATUS_IDS = frozenset({"pass", "fail", "unassessable", "not_applicable"})
COMPLETENESS_IDS = frozenset({"complete", "incomplete", "invalid"})
APPLICATION_LEVEL_ID = "bounded_deterministic_trace"
EVALUATION_STATE_IDS = frozenset({"assessed", "omitted_by_claim_limit"})


class QAReturnError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def _hash_bytes(value: bytes) -> str:
    return sha256(value).hexdigest()


def _hash_file(path: Path) -> str:
    return _hash_bytes(path.read_bytes())


def _row_key(packet: str, arm: str, property_id: str) -> str:
    return f"{packet}:{arm}:{property_id}"


def _transfer_expected_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(
        arm: str,
        property_id: str,
        status: str | None,
        completeness: str | None,
        diagnostics: tuple[str, ...],
        transition: str,
        evaluation_state: str = "assessed",
    ) -> None:
        rows.append({
            "row_key": _row_key("transfer", arm, property_id),
            "packet": "transfer",
            "arm": arm,
            "property_id": property_id,
            "application_level": APPLICATION_LEVEL_ID,
            "evaluation_state": evaluation_state,
            "status": status,
            "completeness": completeness,
            "diagnostics": diagnostics,
            "located_transition": transition,
        })

    for arm, values in {
        "conflict_preserving": {
            "F0": ("pass", "complete", (), "TC-SUMMARY-PRESERVE"),
            "F3": ("unassessable", "incomplete", ("FM_REVIEW_UNRECORDED",), "security_review"),
            "F4": ("pass", "complete", (), "TC-SUMMARY-PRESERVE"),
            "F5": ("unassessable", "incomplete", ("FM_APPLICABILITY_UNDETERMINED",), "trace_boundary"),
            "GateSafe": ("pass", "complete", (), "fail_closed_review_gate"),
            "ReviewEffective": ("unassessable", "incomplete", ("FM_REVIEW_UNRECORDED",), "security_review"),
            "DecisionServiceEffective": ("unassessable", "incomplete", ("FM_REQUIRED_INPUT_MISSING",), "trace_boundary"),
        },
        "fluent_compressed": {
            "F0": ("fail", "complete", ("FM_EVIDENCE_TYPE_COLLAPSED", "FM_LINEAGE_INCOMPLETE", "FM_POLICY_NOT_INSPECTABLE"), "TC-SUMMARY-COMPRESS"),
            "F3": ("not_applicable", "complete", (), "routine_provisioning"),
            "F4": ("fail", "complete", ("FM_MATERIAL_ITEM_UNSURFACED",), "TC-SUMMARY-COMPRESS"),
            "F5": ("unassessable", "incomplete", ("FM_APPLICABILITY_UNDETERMINED",), "trace_boundary"),
            "GateSafe": ("not_applicable", "complete", (), "routine_provisioning"),
            "ReviewEffective": ("fail", "complete", ("FM_REQUIRED_GATE_MISSING", "FM_REVIEW_EVIDENCE_MISSING"), "routine_provisioning"),
            "DecisionServiceEffective": ("unassessable", "incomplete", ("FM_REQUIRED_INPUT_MISSING",), "trace_boundary"),
        },
    }.items():
        for property_id, (status, completeness, diagnostics, transition) in values.items():
            add(arm, property_id, status, completeness, diagnostics, transition)
    add("comparison", "F1", "not_applicable", "complete", (), "frozen_scope_exclusion")
    add("comparison", "F2", "not_applicable", "complete", (), "frozen_scope_exclusion")
    add(
        "shared",
        "CapacityServiceBoundary",
        None,
        None,
        (),
        "level_b_claim_boundary",
        evaluation_state="omitted_by_claim_limit",
    )
    return rows


def expected_profile(root: Path) -> dict[str, object]:
    trace = json.loads(
        (root / "data/golden_traces/robodebt_worked_trace_v1.json").read_text(
            encoding="utf-8"
        )
    )
    rows: list[dict[str, object]] = []
    for arm, assessments in trace["assessments"].items():
        for assessment in assessments:
            rows.append({
                "row_key": _row_key("robodebt", arm, assessment["property_id"]),
                "packet": "robodebt",
                "arm": arm,
                "property_id": assessment["property_id"],
                "application_level": assessment["application_level"],
                "evaluation_state": assessment["evaluation_state"],
                "status": assessment["status"],
                "completeness": assessment["completeness"],
                "diagnostics": tuple(assessment["diagnostics"]),
                "located_transition": assessment["located_transition"],
            })
    rows.extend(_transfer_expected_rows())
    keys = [str(row["row_key"]) for row in rows]
    if len(rows) != 29 or len(keys) != len(set(keys)):
        raise QAReturnError(
            "QA_ORACLE_INVALID", "expected profile must contain 29 unique rows"
        )
    profile = {
        "schema_version": 1,
        "artifact_kind": "slice3_external_qa_expected_profile",
        "rows": sorted(rows, key=lambda row: str(row["row_key"])),
    }
    return profile | {"profile_hash": _hash_bytes(_canonical_json(profile))}


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def blank_return_template(root: Path, reader_id: str) -> dict[str, object]:
    expected = expected_profile(root)
    rows = [
        {
            "row_key": row["row_key"],
            "packet": row["packet"],
            "arm": row["arm"],
            "property_id": row["property_id"],
            "application_level": "",
            "evaluation_state": "",
            "status": None,
            "completeness": None,
            "located_transition": "",
            "evidence": "",
            "diagnostics": [],
            "missing_information_or_claim_limit": "",
            "diagnostic_owner": "",
            "intervention": "",
            "intervention_owner": "",
            "tradeoff": "",
            "ambiguity": "",
        }
        for row in expected["rows"]
    ]
    return {
        "schema_version": 1,
        "artifact_kind": "slice3_external_qa_return",
        "reader_id": reader_id,
        "run_control": {
            "qa_run_id": "",
            "oracle_custodian_id": "",
            "protocol_sha256": _hash_file(root / "docs/PROCESS_RED_TEAM_PROTOCOL.md"),
            "robodebt_packet_sha256": _hash_file(root / "docs/ROBODEBT_WORKED_TRACE_PACKET.md"),
            "transfer_packet_sha256": _hash_file(root / "docs/TRANSFER_CANARY.md"),
            "distribution_archive_sha256": "",
            "distribution_timestamp": "",
            "locked_return_timestamp": "",
            "reader_did_not_draft_protocol_or_packets": None,
            "packet_only_distribution_confirmed": None,
            "oracle_or_repository_exposure_before_return": "",
            "blind_run_validity": "",
            "practice_only": None,
            "custodian_locked_return_before_oracle_access": None,
            "no_personal_data_collected": None,
        },
        "assessments": rows,
        "strongest_supported_finding": "",
        "known_failures": "",
        "unresolved_or_omitted_conclusions": "",
        "required_escalation": "",
        "prohibited_claims_acknowledged": "",
        "ambiguity_log": "",
    }


def _parse_timestamp(value: object, field_name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise QAReturnError("QA_RUN_CONTROL_INVALID", f"{field_name} is required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise QAReturnError(
            "QA_RUN_CONTROL_INVALID", f"{field_name} must be ISO-8601"
        ) from exc
    if parsed.tzinfo is None:
        raise QAReturnError(
            "QA_RUN_CONTROL_INVALID", f"{field_name} must include a timezone"
        )
    return parsed


def _require_nonempty_text(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise QAReturnError("QA_RETURN_INCOMPLETE", f"{field_name} is required")


def compare_return(root: Path, value: Mapping[str, object]) -> dict[str, object]:
    if value.get("schema_version") != 1 or value.get("artifact_kind") != "slice3_external_qa_return":
        raise QAReturnError("QA_RETURN_SCHEMA_INVALID", "return identity mismatch")
    reader_id = value.get("reader_id")
    _require_nonempty_text(reader_id, "reader_id")
    run_control = value.get("run_control")
    if not isinstance(run_control, Mapping):
        raise QAReturnError("QA_RUN_CONTROL_INVALID", "run_control must be a mapping")
    for field_name in ("qa_run_id", "oracle_custodian_id", "distribution_archive_sha256"):
        _require_nonempty_text(run_control.get(field_name), field_name)
    distributed = _parse_timestamp(run_control.get("distribution_timestamp"), "distribution_timestamp")
    locked = _parse_timestamp(run_control.get("locked_return_timestamp"), "locked_return_timestamp")
    if locked <= distributed:
        raise QAReturnError(
            "QA_RUN_CONTROL_INVALID", "locked return must follow distribution"
        )
    expected_hashes = {
        "protocol_sha256": _hash_file(root / "docs/PROCESS_RED_TEAM_PROTOCOL.md"),
        "robodebt_packet_sha256": _hash_file(root / "docs/ROBODEBT_WORKED_TRACE_PACKET.md"),
        "transfer_packet_sha256": _hash_file(root / "docs/TRANSFER_CANARY.md"),
    }
    for field_name, expected_hash in expected_hashes.items():
        if run_control.get(field_name) != expected_hash:
            raise QAReturnError(
                "QA_PACKET_IDENTITY_MISMATCH", f"{field_name} does not match repository candidate"
            )
    archive_path = root / "outputs/cold_reader" / f"{reader_id}.zip"
    if not archive_path.exists() or run_control.get("distribution_archive_sha256") != _hash_file(archive_path):
        raise QAReturnError(
            "QA_PACKET_IDENTITY_MISMATCH", "distribution archive is absent or hash-mismatched"
        )
    required_true = (
        "reader_did_not_draft_protocol_or_packets",
        "packet_only_distribution_confirmed",
        "custodian_locked_return_before_oracle_access",
        "no_personal_data_collected",
    )
    for field_name in required_true:
        if run_control.get(field_name) is not True:
            raise QAReturnError("QA_INDEPENDENCE_INVALID", f"{field_name} must be true")
    if run_control.get("oracle_or_repository_exposure_before_return") != "none":
        raise QAReturnError("QA_ORACLE_EXPOSURE", "blind return has possible or confirmed exposure")
    if run_control.get("blind_run_validity") != "valid" or run_control.get("practice_only") is not False:
        raise QAReturnError("QA_INDEPENDENCE_INVALID", "return is not a valid blind run")

    expected = expected_profile(root)
    expected_by_key = {str(row["row_key"]): row for row in expected["rows"]}
    assessments = value.get("assessments")
    if not isinstance(assessments, list):
        raise QAReturnError("QA_RETURN_SCHEMA_INVALID", "assessments must be a list")
    observed_by_key: dict[str, Mapping[str, object]] = {}
    for assessment in assessments:
        if not isinstance(assessment, Mapping):
            raise QAReturnError("QA_RETURN_SCHEMA_INVALID", "assessment must be a mapping")
        key = assessment.get("row_key")
        if not isinstance(key, str) or key in observed_by_key:
            raise QAReturnError("QA_RETURN_SCHEMA_INVALID", f"duplicate or invalid row key {key}")
        observed_by_key[key] = assessment
    if set(observed_by_key) != set(expected_by_key):
        missing = sorted(set(expected_by_key) - set(observed_by_key))
        extra = sorted(set(observed_by_key) - set(expected_by_key))
        raise QAReturnError(
            "QA_RETURN_INCOMPLETE", f"assessment inventory missing={missing} extra={extra}"
        )

    comparisons: list[dict[str, object]] = []
    closed_diagnostics = set(MANIFEST["closed_diagnostic_codes"])
    for key in sorted(expected_by_key):
        target = expected_by_key[key]
        observed = observed_by_key[key]
        for identity_field in ("packet", "arm", "property_id"):
            if observed.get(identity_field) != target[identity_field]:
                raise QAReturnError(
                    "QA_RETURN_SCHEMA_INVALID", f"{key} changed {identity_field}"
                )
        if observed.get("application_level") != APPLICATION_LEVEL_ID:
            raise QAReturnError("QA_APPLICATION_LEVEL_INVALID", f"{key} application level mismatch")
        if observed.get("evaluation_state") not in EVALUATION_STATE_IDS:
            raise QAReturnError("QA_EVALUATION_STATE_INVALID", f"{key} evaluation state invalid")
        omitted = target["evaluation_state"] == "omitted_by_claim_limit"
        if omitted:
            if observed.get("status") is not None or observed.get("completeness") is not None:
                raise QAReturnError(
                    "QA_CLAIM_LIMIT_INVALID", f"{key} omitted row must leave status/completeness null"
                )
        else:
            if observed.get("status") not in STATUS_IDS:
                raise QAReturnError("QA_STATUS_INVALID", f"{key} status invalid")
            if observed.get("completeness") not in COMPLETENESS_IDS:
                raise QAReturnError("QA_COMPLETENESS_INVALID", f"{key} completeness invalid")
        observed_diagnostics = observed.get("diagnostics")
        if not isinstance(observed_diagnostics, list) or any(
            not isinstance(item, str) for item in observed_diagnostics
        ):
            raise QAReturnError("QA_DIAGNOSTIC_INVALID", f"{key} diagnostics must be strings")
        unknown = set(observed_diagnostics) - closed_diagnostics
        if unknown:
            raise QAReturnError(
                "QA_DIAGNOSTIC_INVALID", f"{key} unknown diagnostics {sorted(unknown)}"
            )
        for field_name in (
            "located_transition", "evidence", "missing_information_or_claim_limit",
            "diagnostic_owner", "intervention", "intervention_owner", "tradeoff",
        ):
            _require_nonempty_text(observed.get(field_name), f"{key}.{field_name}")
        expected_diagnostics = set(target["diagnostics"])
        checks = {
            "evaluation_state_match": observed.get("evaluation_state") == target["evaluation_state"],
            "status_match": observed.get("status") == target["status"],
            "completeness_match": observed.get("completeness") == target["completeness"],
            "diagnostics_match": set(observed_diagnostics) == expected_diagnostics,
            "located_transition_match": observed.get("located_transition") == target["located_transition"],
        }
        comparisons.append({
            "row_key": key,
            **checks,
            "automated_result": "exact" if all(checks.values()) else "mismatch",
        })
    for field_name in (
        "strongest_supported_finding", "known_failures", "unresolved_or_omitted_conclusions",
        "required_escalation", "prohibited_claims_acknowledged", "ambiguity_log",
    ):
        _require_nonempty_text(value.get(field_name), field_name)
    exact = all(row["automated_result"] == "exact" for row in comparisons)
    report = {
        "schema_version": 1,
        "artifact_kind": "slice3_external_qa_return_comparison",
        "reader_id": reader_id,
        "qa_run_id": run_control["qa_run_id"],
        "return_hash": _hash_bytes(_canonical_json(value)),
        "expected_profile_hash": expected["profile_hash"],
        "control_valid": True,
        "row_count": len(comparisons),
        "exact_row_count": sum(row["automated_result"] == "exact" for row in comparisons),
        "mismatch_row_count": sum(row["automated_result"] != "exact" for row in comparisons),
        "comparisons": comparisons,
        "automated_exact_match": exact,
        "freeze_eligible": exact,
        "claim_limit": "artifact QA only; no inference about reader or population performance",
    }
    return report | {"comparison_hash": _hash_bytes(_canonical_json(report))}


def verify_external_qa_gate(root: Path, returns: list[Mapping[str, object]]) -> dict[str, object]:
    if len(returns) < 2:
        raise QAReturnError("QA_READER_COUNT_INSUFFICIENT", "at least two returns are required")
    reports = [compare_return(root, item) for item in returns]
    reader_ids = [str(report["reader_id"]) for report in reports]
    run_ids = [str(report["qa_run_id"]) for report in reports]
    return_hashes = [str(report["return_hash"]) for report in reports]
    if len(reader_ids) != len(set(reader_ids)):
        raise QAReturnError("QA_INDEPENDENCE_INVALID", "reader IDs must be distinct")
    if len(run_ids) != len(set(run_ids)):
        raise QAReturnError("QA_INDEPENDENCE_INVALID", "QA run IDs must be distinct")
    if len(return_hashes) != len(set(return_hashes)):
        raise QAReturnError("QA_INDEPENDENCE_INVALID", "locked returns must be distinct")
    passed = all(bool(report["freeze_eligible"]) for report in reports)
    result = {
        "schema_version": 1,
        "artifact_kind": "slice3_external_qa_gate_receipt",
        "reader_count": len(reports),
        "reader_ids": sorted(reader_ids),
        "return_hashes": sorted(return_hashes),
        "comparison_hashes": sorted(str(report["comparison_hash"]) for report in reports),
        "external_qa_gate_passed": passed,
        "protocol_1_0_promotion_authorized": passed,
        "claim_limit": "artifact QA only; no inference about human performance",
    }
    return result | {"gate_receipt_hash": _hash_bytes(_canonical_json(result))}
