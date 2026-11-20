"""Create and verify the immutable Slice 4 freeze manifest."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from importlib import metadata
import json
import platform
from pathlib import Path
import subprocess
import sys
from typing import Mapping

import yaml

from .experiments import canonical_hash, validate_experiment_config
from .negative_controls import verify_stored_negative_control_receipt
from .schemas import ContractError


FREEZE_MANIFEST_PATH = Path("docs/FREEZE_MANIFEST.json")
FREEZE_ATTESTATION_PATH = Path("docs/FREEZE_COMMIT_ATTESTATIONS.json")
FREEZE_ID = "UPS-CONFIRMATORY-FREEZE@3"

FROZEN_DOCUMENT_PATHS = (
    "pyproject.toml",
    "requirements-lock.txt",
    "docs/CASE_APPLICATION_SUFFICIENCY.md",
    "docs/CONFIGURATION_COMPILATION.md",
    "docs/CONTINUITY_AND_CLAIM_BOUNDARY.md",
    "docs/FORMAL_MODEL.md",
    "docs/P0_PROCEDURE_REVIEW_PACKET.md",
    "docs/P0_USABILITY_WALKTHROUGH.md",
    "docs/PREREGISTRATION.md",
    "docs/PRECURSOR_FIDELITY_FIXTURE.md",
    "docs/PROCESS_RED_TEAM_PROTOCOL.md",
    "docs/ROBODEBT_CASE_STUDY.md",
    "docs/ROBODEBT_WORKED_TRACE_EXPECTED_PROFILE.md",
    "docs/ROBODEBT_WORKED_TRACE_REVIEW_PACKET.md",
    "docs/SOURCE_IDENTITY_RULE.md",
    "docs/TRANSFER_CANARY.md",
    "docs/TRANSFER_CANARY_EXPECTED_PROFILE.md",
    "docs/WORKED_TRACE_SELECTION.md",
    "experiments/configs/confirmatory_v1.yaml",
    "experiments/configs/sensitivity_information_latency_v1.yaml",
    "experiments/evaluation_specs/period_evidence_v2.json",
)

FROZEN_TREE_RULES = (
    ("src/uncertainty_permission_simulation", "*.py", "executable_code"),
    ("scripts", "*.py", "verification_code"),
    ("tests", "*.py", "verification_tests"),
    ("data/model", "*", "formal_data"),
    ("data/sources/robodebt", "*", "source_identity"),
    ("data/scenarios", "*", "scenario_inputs"),
    ("data/golden_traces", "*", "validation_receipts"),
    ("data/pilot", "*", "pilot_receipts"),
)

DEPENDENCY_DISTRIBUTIONS = (
    "annotated-types",
    "iniconfig",
    "numpy",
    "orjson",
    "packaging",
    "pluggy",
    "pydantic",
    "pydantic_core",
    "Pygments",
    "pytest",
    "PyYAML",
    "typing-inspection",
    "typing_extensions",
)


def _sha256_path(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _category_for_explicit(path: str) -> str:
    if path.startswith("experiments/configs/"):
        return "experiment_config"
    if path == "requirements-lock.txt" or path == "pyproject.toml":
        return "environment_contract"
    return "frozen_document"


def frozen_inventory(root: Path) -> dict[str, str]:
    """Return the closed frozen path-to-category inventory."""

    root = root.resolve()
    inventory = {path: _category_for_explicit(path) for path in FROZEN_DOCUMENT_PATHS}
    for tree, pattern, category in FROZEN_TREE_RULES:
        base = root / tree
        if not base.is_dir():
            raise ContractError(
                "FREEZE_INPUT_MISSING",
                f"frozen tree missing: {tree}",
            )
        for path in base.rglob(pattern):
            if not path.is_file() or path.name == ".gitkeep" or "__pycache__" in path.parts:
                continue
            relative = path.relative_to(root).as_posix()
            inventory[relative] = category
    missing = [path for path in inventory if not (root / path).is_file()]
    if missing:
        raise ContractError(
            "FREEZE_INPUT_MISSING",
            f"frozen files missing: {missing}",
        )
    return dict(sorted(inventory.items()))


def _file_entries(root: Path, inventory: Mapping[str, str]) -> list[dict[str, object]]:
    return [
        {
            "path": relative,
            "category": category,
            "sha256": _sha256_path(root / relative),
            "size_bytes": (root / relative).stat().st_size,
        }
        for relative, category in sorted(inventory.items())
    ]


def _dependency_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for distribution in DEPENDENCY_DISTRIBUTIONS:
        try:
            versions[distribution] = metadata.version(distribution)
        except metadata.PackageNotFoundError as exc:
            raise ContractError(
                "FREEZE_ENVIRONMENT_INVALID",
                f"required distribution is not installed: {distribution}",
            ) from exc
    return versions


def environment_identity() -> dict[str, object]:
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "dependency_versions": _dependency_versions(),
    }


def _git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _assert_clean_worktree(root: Path) -> None:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        raise ContractError(
            "FREEZE_WORKTREE_DIRTY",
            "commit the reviewed frozen inputs before creating the manifest",
        )


def _git_blob_hash(root: Path, commit: str, relative: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=root,
        capture_output=True,
    )
    if result.returncode:
        raise ContractError(
            "FREEZE_COMMIT_ATTESTATION_INVALID",
            f"frozen file absent from attested commit: {relative}",
        )
    return sha256(result.stdout).hexdigest()


def verify_manifest_commit_binding(root: Path, manifest: Mapping[str, object]) -> None:
    commit = manifest.get("repository_head_at_creation")
    entries = manifest.get("files")
    if not isinstance(commit, str) or not commit or not isinstance(entries, list):
        raise ContractError(
            "FREEZE_COMMIT_ATTESTATION_INVALID",
            "manifest lacks a repository commit or file inventory",
        )
    for entry in entries:
        if not isinstance(entry, dict):
            raise ContractError("FREEZE_COMMIT_ATTESTATION_INVALID", "invalid file entry")
        relative = str(entry.get("path"))
        if _git_blob_hash(root, commit, relative) != entry.get("sha256"):
            raise ContractError(
                "FREEZE_COMMIT_ATTESTATION_INVALID",
                f"attested commit does not contain the frozen bytes: {relative}",
            )


def verify_historical_freeze_attestations(
    root: Path,
    attestation_path: Path = FREEZE_ATTESTATION_PATH,
) -> dict[str, object]:
    path = attestation_path if attestation_path.is_absolute() else root / attestation_path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError("FREEZE_ATTESTATION_INVALID", str(path)) from exc
    if not isinstance(value, dict):
        raise ContractError("FREEZE_ATTESTATION_INVALID", "attestation must be a mapping")
    observed_hash = value.get("attestation_hash")
    hash_input = dict(value)
    hash_input.pop("attestation_hash", None)
    if observed_hash != canonical_hash(hash_input):
        raise ContractError("FREEZE_ATTESTATION_INVALID", "attestation hash mismatch")
    records = value.get("records")
    if not isinstance(records, list) or not records:
        raise ContractError("FREEZE_ATTESTATION_INVALID", "attestation records are missing")
    for record in records:
        if not isinstance(record, dict):
            raise ContractError("FREEZE_ATTESTATION_INVALID", "invalid attestation record")
        manifest_path = root / str(record.get("manifest_path"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if (
            manifest.get("freeze_id") != record.get("freeze_id")
            or manifest.get("manifest_hash") != record.get("manifest_hash")
            or manifest.get("repository_head_at_creation")
            != record.get("working_tree_head_at_freeze_creation")
            or len(manifest.get("files", ())) != record.get("verified_file_count")
        ):
            raise ContractError("FREEZE_ATTESTATION_INVALID", "manifest identity mismatch")
        attested = dict(manifest)
        attested["repository_head_at_creation"] = record.get(
            "first_commit_containing_exact_frozen_inventory"
        )
        verify_manifest_commit_binding(root, attested)
    return value


def _source_identity(root: Path) -> dict[str, object]:
    path = root / "data/sources/robodebt/source_manifest.yaml"
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    sources = manifest.get("sources") if isinstance(manifest, dict) else None
    if not isinstance(sources, list) or not sources:
        raise ContractError(
            "FREEZE_SOURCE_IDENTITY_INVALID",
            "source manifest must contain selected sources",
        )
    entries = []
    for source in sources:
        if not isinstance(source, dict):
            raise ContractError(
                "FREEZE_SOURCE_IDENTITY_INVALID",
                "each selected source must be a mapping",
            )
        entries.append({
            "source_id": source.get("source_id"),
            "authoritative_url": source.get("url"),
            "publisher": source.get("publisher"),
            "title": source.get("title"),
            "publication_date": str(source.get("publication_date")),
            "corrected_edition_date": (
                str(source["corrected_edition_date"])
                if source.get("corrected_edition_date") is not None else None
            ),
            "local_copy": source.get("local_copy"),
            "remote_byte_hash": source.get("content_hash"),
            "http_outcome_at_freeze": "not_rechecked",
            "content_type_at_freeze": "not_recorded",
            "local_record_hash": canonical_hash(
                json.loads(json.dumps(source, default=str))
            ),
        })
    return {
        "identity_rule": "docs/SOURCE_IDENTITY_RULE.md",
        "retrieved_through": str(manifest.get("retrieved_through")),
        "manifest_hash": _sha256_path(path),
        "selected_source_count": len(entries),
        "sources": entries,
    }


def _assert_freeze_ready(root: Path) -> tuple[dict[str, object], dict[str, object]]:
    confirmatory_path = root / "experiments/configs/confirmatory_v1.yaml"
    sensitivity_path = root / "experiments/configs/sensitivity_information_latency_v1.yaml"
    confirmatory = yaml.safe_load(confirmatory_path.read_text(encoding="utf-8"))
    sensitivity = yaml.safe_load(sensitivity_path.read_text(encoding="utf-8"))
    for name, config in (("confirmatory", confirmatory), ("sensitivity", sensitivity)):
        readiness = config.get("freeze_readiness") if isinstance(config, dict) else None
        if readiness != {"status": "ready", "unresolved_items": []}:
            raise ContractError(
                "FREEZE_NOT_READY",
                f"{name} config has not been promoted to ready",
            )
    protocol = (root / "docs/PROCESS_RED_TEAM_PROTOCOL.md").read_text(encoding="utf-8")
    preregistration = (root / "docs/PREREGISTRATION.md").read_text(encoding="utf-8")
    formal = (root / "docs/FORMAL_MODEL.md").read_text(encoding="utf-8")
    if "version `1.0`" not in protocol or "Protocol version: `1.0`" not in preregistration:
        raise ContractError(
            "FREEZE_VERSION_INVALID",
            "protocol and preregistration must declare version 1.0",
        )
    if "Formal-model version: `1.0`" not in formal:
        raise ContractError(
            "FREEZE_VERSION_INVALID",
            "formal model must declare version 1.0",
        )
    return (
        validate_experiment_config(confirmatory_path),
        validate_experiment_config(sensitivity_path),
    )


def _confirmatory_output_paths(root: Path) -> list[str]:
    output_roots = (
        root / "outputs/confirmatory_v2",
        root / "outputs/sensitivity_information_latency_v2",
    )
    return sorted(
        path.relative_to(root).as_posix()
        for output_root in output_roots
        if output_root.exists()
        for path in output_root.rglob("*")
        if path.is_file()
    )


def build_freeze_manifest(root: Path) -> dict[str, object]:
    root = root.resolve()
    if _confirmatory_output_paths(root):
        raise ContractError(
            "FREEZE_OUTPUT_EXISTS",
            "confirmatory or sensitivity output exists before freeze",
        )
    confirmatory, sensitivity = _assert_freeze_ready(root)
    _assert_clean_worktree(root)
    negative_controls = verify_stored_negative_control_receipt(
        root,
        root / "experiments/configs/confirmatory_v1.yaml",
    )
    inventory = frozen_inventory(root)
    manifest = {
        "schema_version": 1,
        "artifact_kind": "confirmatory_freeze_manifest",
        "freeze_id": FREEZE_ID,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository_head_at_creation": _git_head(root),
        "claim_boundary": "formal counterfactual simulation over the declared parameter space; no historical prevalence, monetary correctness, legality, or attackability inference",
        "files": _file_entries(root, inventory),
        "inventory_path_hash": canonical_hash(sorted(inventory)),
        "environment": environment_identity(),
        "source_identity": _source_identity(root),
        "design": {
            "confirmatory_validation": confirmatory,
            "sensitivity_validation": sensitivity,
            "negative_control_receipt_hash": negative_controls["receipt_hash"],
            "primary_family_count": confirmatory["family_count"],
            "initial_replications": confirmatory["replications"],
            "seed_count": confirmatory["seed_count"],
            "seed_inventory_hash": confirmatory["seed_inventory_hash"],
        },
    }
    return manifest | {"manifest_hash": canonical_hash(manifest)}


def write_freeze_manifest(root: Path, destination: Path = FREEZE_MANIFEST_PATH) -> dict[str, object]:
    root = root.resolve()
    if destination != FREEZE_MANIFEST_PATH:
        raise ContractError(
            "FREEZE_DESTINATION_INVALID",
            f"freeze manifest destination must be {FREEZE_MANIFEST_PATH}",
        )
    path = root / destination
    if path.exists():
        raise ContractError(
            "FREEZE_MANIFEST_EXISTS",
            "freeze manifest already exists and is immutable",
        )
    manifest = build_freeze_manifest(root)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def verify_freeze_manifest(
    root: Path,
    manifest_path: Path = FREEZE_MANIFEST_PATH,
    *,
    verify_environment: bool = True,
) -> dict[str, object]:
    root = root.resolve()
    path = manifest_path if manifest_path.is_absolute() else root / manifest_path
    if not path.is_file():
        raise ContractError(
            "FREEZE_MANIFEST_MISSING",
            f"freeze manifest missing: {path}",
        )
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ContractError(
            "FREEZE_MANIFEST_INVALID",
            "freeze manifest is unreadable",
        ) from exc
    if not isinstance(manifest, dict) or manifest.get("freeze_id") != FREEZE_ID:
        raise ContractError(
            "FREEZE_MANIFEST_INVALID",
            "freeze manifest identity is invalid",
        )
    observed_hash = manifest.get("manifest_hash")
    hash_input = dict(manifest)
    hash_input.pop("manifest_hash", None)
    if observed_hash != canonical_hash(hash_input):
        raise ContractError(
            "FREEZE_MANIFEST_HASH_MISMATCH",
            "freeze manifest self-hash does not match",
        )
    expected_inventory = frozen_inventory(root)
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise ContractError("FREEZE_MANIFEST_INVALID", "freeze file inventory is missing")
    recorded_paths = [entry.get("path") for entry in entries if isinstance(entry, dict)]
    if recorded_paths != sorted(expected_inventory):
        missing = sorted(set(expected_inventory) - set(recorded_paths))
        extra = sorted(set(recorded_paths) - set(expected_inventory))
        raise ContractError(
            "FREEZE_INVENTORY_DRIFT",
            f"frozen inventory drift; missing={missing}, extra={extra}",
        )
    for entry in entries:
        relative = entry["path"]
        file_path = root / relative
        if entry.get("category") != expected_inventory[relative]:
            raise ContractError(
                "FREEZE_INVENTORY_DRIFT",
                f"frozen category drift: {relative}",
            )
        if _sha256_path(file_path) != entry.get("sha256"):
            raise ContractError(
                "FREEZE_FILE_HASH_MISMATCH",
                f"frozen file hash mismatch: {relative}",
            )
        if file_path.stat().st_size != entry.get("size_bytes"):
            raise ContractError(
                "FREEZE_FILE_SIZE_MISMATCH",
                f"frozen file size mismatch: {relative}",
            )
    if manifest.get("inventory_path_hash") != canonical_hash(sorted(expected_inventory)):
        raise ContractError(
            "FREEZE_INVENTORY_DRIFT",
            "freeze inventory path hash mismatch",
        )
    if verify_environment and manifest.get("environment") != environment_identity():
        raise ContractError(
            "FREEZE_ENVIRONMENT_DRIFT",
            "current interpreter, platform, or dependency versions differ from freeze",
        )
    if manifest.get("repository_head_at_creation") is not None:
        verify_manifest_commit_binding(root, manifest)
    return manifest


def manifest_file_hash(manifest: Mapping[str, object], relative_path: str) -> str:
    for entry in manifest.get("files", []):
        if isinstance(entry, dict) and entry.get("path") == relative_path:
            return str(entry["sha256"])
    raise ContractError(
        "FREEZE_INPUT_NOT_HASHED",
        f"frozen input absent from manifest: {relative_path}",
    )
