import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from uncertainty_permission_simulation import confirmatory, freeze
from uncertainty_permission_simulation.confirmatory import (
    analyze_frozen_experiment,
    planned_attempt_count,
    reconcile_frozen_experiment,
    run_frozen_experiment,
)
from uncertainty_permission_simulation.experiments import PRIMARY_METRICS, canonical_hash
from uncertainty_permission_simulation.freeze import FREEZE_ID, verify_freeze_manifest
from uncertainty_permission_simulation.policies import POLICY_IDS
from uncertainty_permission_simulation.schemas import ContractError


ROOT = Path(__file__).resolve().parents[2]
CONFIRMATORY = ROOT / "experiments/configs/confirmatory_v1.yaml"
SENSITIVITY = ROOT / "experiments/configs/sensitivity_information_latency_v1.yaml"


def _write_test_manifest(root: Path) -> Path:
    inventory = freeze.frozen_inventory(root)
    value = {
        "schema_version": 1,
        "artifact_kind": "confirmatory_freeze_manifest",
        "freeze_id": FREEZE_ID,
        "files": freeze._file_entries(root, inventory),
        "inventory_path_hash": canonical_hash(sorted(inventory)),
        "environment": freeze.environment_identity(),
    }
    value["manifest_hash"] = canonical_hash(value)
    path = root / "manifest.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_freeze_manifest_detects_file_and_inventory_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "code").mkdir()
    (tmp_path / "contract.md").write_text("frozen\n", encoding="utf-8")
    code = tmp_path / "code/kernel.py"
    code.write_text("VALUE = 1\n", encoding="utf-8")
    monkeypatch.setattr(freeze, "FROZEN_DOCUMENT_PATHS", ("contract.md",))
    monkeypatch.setattr(freeze, "FROZEN_TREE_RULES", (("code", "*.py", "code"),))
    monkeypatch.setattr(freeze, "environment_identity", lambda: {"test": "environment"})
    manifest_path = _write_test_manifest(tmp_path)
    assert verify_freeze_manifest(tmp_path, manifest_path)["freeze_id"] == FREEZE_ID

    code.write_text("VALUE = 2\n", encoding="utf-8")
    with pytest.raises(ContractError, match="FREEZE_FILE_HASH_MISMATCH"):
        verify_freeze_manifest(tmp_path, manifest_path)

    code.write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "code/new.py").write_text("VALUE = 3\n", encoding="utf-8")
    with pytest.raises(ContractError, match="FREEZE_INVENTORY_DRIFT"):
        verify_freeze_manifest(tmp_path, manifest_path)


def test_freeze_manifest_detects_self_hash_and_environment_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "contract.md").write_text("frozen\n", encoding="utf-8")
    monkeypatch.setattr(freeze, "FROZEN_DOCUMENT_PATHS", ("contract.md",))
    monkeypatch.setattr(freeze, "FROZEN_TREE_RULES", ())
    monkeypatch.setattr(freeze, "environment_identity", lambda: {"test": "environment"})
    manifest_path = _write_test_manifest(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["freeze_id"] = "MUTATED"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ContractError, match="FREEZE_MANIFEST_INVALID"):
        verify_freeze_manifest(tmp_path, manifest_path)

    manifest["freeze_id"] = FREEZE_ID
    manifest["manifest_hash"] = canonical_hash({
        key: value for key, value in manifest.items() if key != "manifest_hash"
    })
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(freeze, "environment_identity", lambda: {"test": "changed"})
    with pytest.raises(ContractError, match="FREEZE_ENVIRONMENT_DRIFT"):
        verify_freeze_manifest(tmp_path, manifest_path)


def test_creation_and_execution_propagate_freeze_guards(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        freeze,
        "_assert_freeze_ready",
        lambda root: (_ for _ in ()).throw(
            ContractError("FREEZE_NOT_READY", "candidate is not ready")
        ),
    )
    with pytest.raises(ContractError, match="FREEZE_NOT_READY"):
        freeze.build_freeze_manifest(tmp_path)

    config_path = tmp_path / "experiments/configs/candidate.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("config_id: CANDIDATE\n", encoding="utf-8")
    monkeypatch.setattr(
        confirmatory,
        "verify_freeze_manifest",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            ContractError("FREEZE_MANIFEST_MISSING", "manifest is missing")
        ),
    )
    with pytest.raises(ContractError, match="FREEZE_MANIFEST_MISSING"):
        run_frozen_experiment(tmp_path, config_path)
    assert not (tmp_path / "outputs").exists()


def test_frozen_attempt_inventory_has_closed_cardinality() -> None:
    assert planned_attempt_count(CONFIRMATORY) == 108 * 30 * 5
    assert planned_attempt_count(CONFIRMATORY, extension=True) == 108 * 30 * 5
    assert planned_attempt_count(SENSITIVITY) == 108 * 30 * 5
    assert planned_attempt_count(SENSITIVITY, extension=True) == 0


def test_repository_freeze_inventory_covers_load_bearing_inputs() -> None:
    inventory = freeze.frozen_inventory(ROOT)
    for path in (
        "docs/FORMAL_MODEL.md",
        "docs/PREREGISTRATION.md",
        "docs/PROCESS_RED_TEAM_PROTOCOL.md",
        "experiments/configs/confirmatory_v1.yaml",
        "src/uncertainty_permission_simulation/simulator.py",
        "src/uncertainty_permission_simulation/confirmatory.py",
        "scripts/verify_repo.py",
        "data/golden_traces/slice4_negative_control_receipt_v2.json",
        "experiments/evaluation_specs/period_evidence_v2.json",
    ):
        assert path in inventory
    source_identity = freeze._source_identity(ROOT)
    assert source_identity["selected_source_count"] == 10
    assert all(source["local_record_hash"] for source in source_identity["sources"])


def _mini_config() -> dict[str, object]:
    return {
        "config_id": "MINI-FROZEN",
        "mode": "sensitivity",
        "replications": 2,
        "cohort_size": 4,
        "seed_prefix": "MINI-SEED",
        "precision": {
            "minimum_replications": 2,
            "maximum_replications": 2,
            "target_rate_mcse": 0.5,
            "target_paired_mcse": 0.5,
            "extension_rule": "none",
        },
        "outputs": {
            "attempts_directory": "outputs/mini/attempts",
            "run_index_path": "outputs/mini/run_index.json",
            "reconciliation_path": "outputs/mini/reconciliation.json",
            "analysis_directory": "outputs/mini/analysis",
        },
        "freeze_readiness": {"status": "ready", "unresolved_items": []},
    }


def test_append_only_run_reconcile_and_analysis_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path = tmp_path / "experiments/configs/mini.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("config_id: MINI-FROZEN\n", encoding="utf-8")
    config = _mini_config()
    manifest = {"manifest_hash": "f" * 64, "validated_config": {}}
    families = (
        SimpleNamespace(family_id="FAMILY-A"),
        SimpleNamespace(family_id="FAMILY-B"),
    )
    monkeypatch.setattr(
        confirmatory,
        "_assert_executable_config",
        lambda path: (
            config,
            manifest,
            confirmatory.load_evaluation_specification(
                ROOT / "experiments/evaluation_specs/period_evidence_v2.json"
            ),
        ),
    )
    monkeypatch.setattr(confirmatory, "_families", lambda value: families)

    def fake_attempt_artifact(**kwargs: object) -> dict[str, object]:
        family = kwargs["family"]
        replication = int(kwargs["replication"])
        policy_id = str(kwargs["policy_id"])
        attempt_id = confirmatory._attempt_id(family.family_id, replication, policy_id)
        metric_value = (replication + POLICY_IDS.index(policy_id)) / 20
        row = {
            "family_id": family.family_id,
            "load": "0.95",
            "missing_evidence": "0.30",
            "access_barrier": "0.30",
            "retrievability": "high",
            "staff_access": "complete",
            "replication": replication,
            "policy_id": policy_id,
            "case_count": 4,
            "event_count": 10,
            "cohort_hash": f"COHORT-{family.family_id}-{replication}",
            "event_hash": f"EVENT-{attempt_id}",
            **{metric: metric_value for metric in PRIMARY_METRICS},
            "review_mean_wait_time": 0.0,
            "correction_mean_exposure_time": 0.0,
        }
        artifact = {
            "schema_version": 2,
            "artifact_kind": "confirmatory_attempt",
            "attempt_id": attempt_id,
            "config_id": config["config_id"],
            "manifest_hash": manifest["manifest_hash"],
            "evaluation_bridge_receipt": {
                "evaluation_spec_id": "CONFIRMATORY-PERIOD-EVIDENCE@2",
                "evaluation_specification_hash": "e" * 64,
                "implementation_code_hash": "i" * 64,
                "routing_receipt_count": 4,
                "action_receipt_count": 4,
                "routing_action_compared_count": 4,
                "routing_action_mismatch_count": 0,
                "action_missing_by_cutoff_count": 0,
                "certificate_counts": {"CERT": 4},
                "evidence_state_counts": {"STATE": 4},
                "support_outcome_counts": {"true": 4},
                "receipt_hash": f"RECEIPT-{attempt_id}",
            },
            "row": row,
        }
        return artifact | {"attempt_hash": canonical_hash(artifact)}

    monkeypatch.setattr(confirmatory, "_attempt_artifact", fake_attempt_artifact)
    first = run_frozen_experiment(tmp_path, config_path)
    assert first["created_attempts"] == 2 * 2 * 5
    second = run_frozen_experiment(tmp_path, config_path)
    assert second["created_attempts"] == 0
    assert second["retained_attempts"] == 20

    reconciliation = reconcile_frozen_experiment(tmp_path, config_path)
    assert reconciliation["status"] == "complete"
    assert reconciliation["observed_attempt_count"] == 20
    analysis = analyze_frozen_experiment(tmp_path, config_path)
    assert analysis["attempt_count"] == 20
    assert analysis["replications"] == 2
    assert analyze_frozen_experiment(tmp_path, config_path) == analysis

    first_attempt = next((tmp_path / "outputs/mini/attempts").glob("*.json"))
    mutated = json.loads(first_attempt.read_text(encoding="utf-8"))
    mutated["row"]["case_count"] = 999
    first_attempt.write_text(json.dumps(mutated), encoding="utf-8")
    with pytest.raises(ContractError, match="RUN_ATTEMPT_INVALID"):
        run_frozen_experiment(tmp_path, config_path)
