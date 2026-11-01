from copy import deepcopy
import json
from pathlib import Path

import pytest
import yaml

from uncertainty_permission_simulation import negative_controls
from uncertainty_permission_simulation.negative_controls import (
    CONFIRMATORY_NEGATIVE_CONTROL_IDS,
    NEGATIVE_CONTROL_RECEIPT_PATH,
    build_negative_control_receipt,
    verify_stored_negative_control_receipt,
    write_negative_control_receipt,
)
from uncertainty_permission_simulation.schemas import ContractError


ROOT = Path(__file__).resolve().parents[2]
CONFIRMATORY = ROOT / "experiments/configs/confirmatory_v1.yaml"


def test_negative_control_receipt_covers_closed_controls_outside_primary_grid() -> None:
    receipt = build_negative_control_receipt(CONFIRMATORY)
    assert receipt["control_ids"] == list(CONFIRMATORY_NEGATIVE_CONTROL_IDS)
    assert receipt["control_count"] == 5
    assert receipt["primary_family_count"] == 0
    assert receipt["robust_permission_violation_count"] == 0
    assert receipt["all_controls_pass"] is True
    assert {control["status"] for control in receipt["controls"]} == {"pass"}
    assert len(receipt["receipt_hash"]) == 64


def test_negative_controls_keep_pairwise_and_action_support_rules_distinct() -> None:
    receipt = build_negative_control_receipt(CONFIRMATORY)
    controls = {control["control_id"]: control for control in receipt["controls"]}
    for control_id in (
        "P0-SAME-RULE-SEMANTIC-NULL",
        "P0-ROUTING-INVARIANCE",
    ):
        assert controls[control_id]["control_kind"] == "matched_representation_pair"
        assert controls[control_id]["observed"]["semantic_projection_equal"] is True
        assert controls[control_id]["action_support_scope"].startswith("omitted_by_claim_limit")
    verified = controls["VERIFIED-MATCH-PROGRESSION"]
    assert verified["observed"]["action"] == "progress"
    assert verified["observed"]["progression_supported"] is True
    assert controls["NO-SUPPORT-NO-PROGRESSION"]["observed"]["actions"] == ["hold", "hold"]
    no_threshold = controls["NO-THRESHOLD-NO-PROGRESSION"]["observed"]
    assert no_threshold["progression_threshold_crossed"] is False
    assert no_threshold["action"] == "hold"


def test_negative_control_receipt_replays_byte_equivalent(tmp_path: Path) -> None:
    first = write_negative_control_receipt(tmp_path, CONFIRMATORY)
    stored_path = tmp_path / NEGATIVE_CONTROL_RECEIPT_PATH
    first_bytes = stored_path.read_bytes()
    second = write_negative_control_receipt(tmp_path, CONFIRMATORY)
    assert stored_path.read_bytes() == first_bytes
    assert second == first
    assert verify_stored_negative_control_receipt(tmp_path, CONFIRMATORY) == first


def test_negative_control_receipt_is_stable_when_readiness_metadata_changes(
    tmp_path: Path,
) -> None:
    config = yaml.safe_load(CONFIRMATORY.read_text(encoding="utf-8"))
    config["freeze_readiness"] = {"status": "ready", "unresolved_items": []}
    promoted = tmp_path / "promoted.yaml"
    promoted.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    assert build_negative_control_receipt(promoted) == build_negative_control_receipt(CONFIRMATORY)


def test_negative_control_receipt_rejects_stored_mutation(tmp_path: Path) -> None:
    write_negative_control_receipt(tmp_path, CONFIRMATORY)
    stored_path = tmp_path / NEGATIVE_CONTROL_RECEIPT_PATH
    mutated = json.loads(stored_path.read_text(encoding="utf-8"))
    mutated["controls"][0]["status"] = "fail"
    stored_path.write_text(json.dumps(mutated), encoding="utf-8")
    with pytest.raises(ContractError, match="self-hash does not match"):
        verify_stored_negative_control_receipt(tmp_path, CONFIRMATORY)


def test_negative_control_execution_fails_closed_on_unexpected_violation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = negative_controls._run_control

    def violate(control_id: str) -> dict[str, object]:
        result = deepcopy(original(control_id))
        if control_id == "VERIFIED-MATCH-PROGRESSION":
            result["robust_permission_violation_count"] = 1
        return result

    monkeypatch.setattr(negative_controls, "_run_control", violate)
    with pytest.raises(ContractError, match="NEGATIVE_CONTROL_FAILED"):
        build_negative_control_receipt(CONFIRMATORY)
