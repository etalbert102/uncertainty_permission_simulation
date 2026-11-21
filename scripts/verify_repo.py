#!/usr/bin/env python3
"""Blocking repository verifier for the frozen and executed study."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uncertainty_permission_simulation.experiments import canonical_hash, validate_experiment_config  # noqa: E402
from uncertainty_permission_simulation.freeze import (  # noqa: E402
    ACTIVE_OUTPUT_ROOTS,
    verify_freeze_manifest,
    verify_historical_freeze_attestations,
)
from uncertainty_permission_simulation.negative_controls import verify_stored_negative_control_receipt  # noqa: E402
from uncertainty_permission_simulation.schemas import ContractError  # noqa: E402


def _run_gate(arguments: list[str]) -> str:
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run(
        arguments,
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        detail = (result.stdout + result.stderr).strip()
        raise ContractError(
            "FREEZE_GATE_FAILED",
            f"gate failed ({' '.join(arguments)}): {detail}",
        )
    return result.stdout.strip()


def _load_self_hashed(path: Path, field: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ContractError(
            "RUN_ARTIFACT_INVALID",
            f"required artifact is unreadable: {path.relative_to(ROOT)}",
        ) from exc
    observed = value.get(field) if isinstance(value, dict) else None
    candidate = dict(value) if isinstance(value, dict) else {}
    candidate.pop(field, None)
    if observed != canonical_hash(candidate):
        raise ContractError(
            "RUN_ARTIFACT_INVALID",
            f"required artifact hash mismatch: {path.relative_to(ROOT)}",
        )
    return value


def _verify_slice5_config(config_path: Path, manifest_hash: str) -> None:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_index_path = ROOT / config["outputs"]["run_index_path"]
    run_index = _load_self_hashed(run_index_path, "run_index_hash")
    reconciliation_path = ROOT / config["outputs"]["reconciliation_path"]
    reconciliation = _load_self_hashed(reconciliation_path, "reconciliation_hash")
    if reconciliation.get("status") != "complete":
        raise ContractError(
            "RUN_RECONCILIATION_INCOMPLETE",
            f"run reconciliation is incomplete: {config['config_id']}",
        )
    if (
        reconciliation.get("config_id") != config["config_id"]
        or reconciliation.get("manifest_hash") != manifest_hash
        or reconciliation.get("run_index_hash") != run_index.get("run_index_hash")
        or run_index.get("config_id") != config["config_id"]
        or run_index.get("manifest_hash") != manifest_hash
        or run_index.get("attempt_count") != reconciliation.get("observed_attempt_count")
    ):
        raise ContractError(
            "RUN_ARTIFACT_CHAIN_MISMATCH",
            f"run index and reconciliation are not bound to the active freeze: {config['config_id']}",
        )
    replications = int(reconciliation["target_replications"])
    analysis_path = ROOT / config["outputs"]["analysis_directory"] / f"analysis_r{replications:03d}.json"
    analysis = _load_self_hashed(analysis_path, "analysis_hash")
    if (
        analysis.get("config_id") != config["config_id"]
        or analysis.get("manifest_hash") != manifest_hash
        or analysis.get("reconciliation_hash") != reconciliation.get("reconciliation_hash")
        or analysis.get("run_index_hash") != run_index.get("run_index_hash")
        or analysis.get("attempt_count") != run_index.get("attempt_count")
    ):
        raise ContractError(
            "ANALYSIS_ARTIFACT_CHAIN_MISMATCH",
            f"analysis is not bound to the reconciled active run: {config['config_id']}",
        )
    bridge = analysis.get("evaluation_bridge_summary")
    if not isinstance(bridge, dict) or bridge.get("routing_action_mismatch_count") != 0:
        raise ContractError(
            "ANALYSIS_EVALUATION_RECEIPT_INVALID",
            f"evaluation bridge summary missing or inconsistent: {config['config_id']}",
        )


def verify_repository(*, through_slice: int, release: bool) -> dict[str, object]:
    manifest = verify_freeze_manifest(ROOT, ROOT / "docs/FREEZE_MANIFEST.json")
    historical_attestations = verify_historical_freeze_attestations(ROOT)
    confirmatory_path = ROOT / "experiments/configs/confirmatory_v1.yaml"
    sensitivity_path = ROOT / "experiments/configs/sensitivity_information_latency_v1.yaml"
    confirmatory = validate_experiment_config(confirmatory_path)
    sensitivity = validate_experiment_config(sensitivity_path)
    negative_controls = verify_stored_negative_control_receipt(ROOT, confirmatory_path)
    gate_outputs = {
        "plan": _run_gate([sys.executable, "scripts/validate_plan.py"]),
        "slice0": _run_gate([sys.executable, "scripts/validate_slice0.py"]),
        "slice3": _run_gate(
            [sys.executable, "scripts/validate_slice3.py"]
            + (["--allow-confirmatory-output"] if through_slice >= 5 else [])
        ),
        "tests": _run_gate([sys.executable, "-m", "pytest", "-q"]),
    }
    if through_slice == 4:
        forbidden = sorted(
            path.relative_to(ROOT).as_posix()
            for base in (ROOT / relative for relative in ACTIVE_OUTPUT_ROOTS)
            if base.exists()
            for path in base.rglob("*")
            if path.is_file()
        )
        if forbidden:
            raise ContractError(
                "FREEZE_OUTPUT_EXISTS",
                f"confirmatory output exists during Slice 4 verification: {forbidden[:5]}",
            )
    else:
        _verify_slice5_config(confirmatory_path, str(manifest["manifest_hash"]))
        _verify_slice5_config(sensitivity_path, str(manifest["manifest_hash"]))
    if release:
        required = (
            ROOT / "docs/EVIDENCE_PACKET.md",
            ROOT / "docs/PROCEDURE_COMPREHENSIBILITY_REVIEW.md",
        )
        missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
        if missing:
            raise ContractError(
                "REPORT_RELEASE_INCOMPLETE",
                f"release artifacts missing: {missing}",
            )
    return {
        "status": "pass",
        "through_slice": through_slice,
        "release": release,
        "manifest_hash": manifest["manifest_hash"],
        "confirmatory_config_hash": confirmatory["config_hash"],
        "sensitivity_config_hash": sensitivity["config_hash"],
        "negative_control_receipt_hash": negative_controls["receipt_hash"],
        "historical_freeze_attestation_hash": historical_attestations["attestation_hash"],
        "gate_outputs": gate_outputs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through-slice", type=int, choices=(4, 5), default=4)
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    through_slice = 5 if args.release else args.through_slice
    try:
        result = verify_repository(through_slice=through_slice, release=args.release)
    except ContractError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
