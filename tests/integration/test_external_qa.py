from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import shutil

import pytest

from uncertainty_permission_simulation.qa import (
    QAReturnError,
    blank_return_template,
    expected_profile,
    verify_external_qa_gate,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def _qa_root(tmp_path: Path) -> Path:
    for relative in (
        "data/golden_traces/robodebt_worked_trace_v1.json",
        "docs/PROCESS_RED_TEAM_PROTOCOL.md",
        "docs/ROBODEBT_WORKED_TRACE_PACKET.md",
        "docs/TRANSFER_CANARY.md",
    ):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPOSITORY_ROOT / relative, target)
    (tmp_path / "outputs/cold_reader").mkdir(parents=True)
    return tmp_path


def _exact_return(root: Path, reader_id: str, run_id: str, archive_bytes: bytes) -> dict[str, object]:
    archive = root / "outputs/cold_reader" / f"{reader_id}.zip"
    archive.write_bytes(archive_bytes)
    value = blank_return_template(root, reader_id)
    targets = {row["row_key"]: row for row in expected_profile(root)["rows"]}
    for assessment in value["assessments"]:
        target = targets[assessment["row_key"]]
        assessment.update({
            "application_level": target["application_level"],
            "evaluation_state": target["evaluation_state"],
            "status": target["status"],
            "completeness": target["completeness"],
            "located_transition": target["located_transition"],
            "evidence": "packet evidence cited by the row",
            "diagnostics": list(target["diagnostics"]),
            "missing_information_or_claim_limit": "none beyond the row's declared scope",
            "diagnostic_owner": "artifact owner",
            "intervention": "retain or repair the identified transition",
            "intervention_owner": "workflow owner",
            "tradeoff": "additional delay or workload may result",
            "ambiguity": "none",
        })
    value["run_control"].update({
        "qa_run_id": run_id,
        "oracle_custodian_id": "CUSTODIAN-TEST",
        "distribution_archive_sha256": sha256(archive_bytes).hexdigest(),
        "distribution_timestamp": "2026-11-01T12:00:00-04:00",
        "locked_return_timestamp": "2026-11-01T13:00:00-04:00",
        "reader_did_not_draft_protocol_or_packets": True,
        "packet_only_distribution_confirmed": True,
        "oracle_or_repository_exposure_before_return": "none",
        "blind_run_validity": "valid",
        "practice_only": False,
        "custodian_locked_return_before_oracle_access": True,
        "no_personal_data_collected": True,
    })
    value.update({
        "strongest_supported_finding": "bounded finding",
        "known_failures": "all failures are enumerated in rows",
        "unresolved_or_omitted_conclusions": "claim limits retained",
        "required_escalation": "escalate semantic ambiguity",
        "prohibited_claims_acknowledged": "no prevalence, legality, or performance claim",
        "ambiguity_log": "none",
    })
    return value


def test_blank_template_contains_row_identity_but_no_oracle_answers(tmp_path: Path) -> None:
    root = _qa_root(tmp_path)
    value = blank_return_template(root, "CR-S3-001")
    assert len(value["assessments"]) == 29
    assert all(row["status"] is None for row in value["assessments"])
    assert all(row["completeness"] is None for row in value["assessments"])
    assert all(row["diagnostics"] == [] for row in value["assessments"])
    assert "profile_hash" not in str(value)


def test_two_distinct_exact_locked_returns_pass_gate(tmp_path: Path) -> None:
    root = _qa_root(tmp_path)
    first = _exact_return(root, "CR-S3-001", "QA-001", b"archive-one")
    second = _exact_return(root, "CR-S3-002", "QA-002", b"archive-two")
    result = verify_external_qa_gate(root, [first, second])
    assert result["external_qa_gate_passed"] is True
    assert result["protocol_1_0_promotion_authorized"] is True
    assert result["reader_count"] == 2


def test_status_mutation_fails_gate_without_becoming_acceptable_variant(tmp_path: Path) -> None:
    root = _qa_root(tmp_path)
    first = _exact_return(root, "CR-S3-001", "QA-001", b"archive-one")
    second = _exact_return(root, "CR-S3-002", "QA-002", b"archive-two")
    mutated = deepcopy(second)
    mutated["assessments"][0]["status"] = "pass" if mutated["assessments"][0]["status"] != "pass" else "fail"
    result = verify_external_qa_gate(root, [first, mutated])
    assert result["external_qa_gate_passed"] is False
    assert result["protocol_1_0_promotion_authorized"] is False


def test_exposure_and_duplicate_reader_identity_are_blocking(tmp_path: Path) -> None:
    root = _qa_root(tmp_path)
    first = _exact_return(root, "CR-S3-001", "QA-001", b"archive-one")
    exposed = deepcopy(first)
    exposed["run_control"]["oracle_or_repository_exposure_before_return"] = "possible"
    with pytest.raises(QAReturnError, match="QA_ORACLE_EXPOSURE"):
        verify_external_qa_gate(root, [first, exposed])

    duplicate = deepcopy(first)
    duplicate["run_control"]["qa_run_id"] = "QA-002"
    with pytest.raises(QAReturnError, match="reader IDs must be distinct"):
        verify_external_qa_gate(root, [first, duplicate])
