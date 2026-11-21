"""Manifest-gated, append-only confirmatory execution and analysis."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from math import sqrt
from pathlib import Path
from statistics import mean
from typing import Mapping

from .configuration import EvaluationSpecificationSpec, compile_configuration, load_evaluation_specification
from .experiments import (
    PRIMARY_METRICS,
    _common_random_number_diagnostics,
    _paired_estimates,
    _run_metrics,
    _summarize_cells,
    _validate_metric_row,
    canonical_hash,
    load_experiment_config,
    validate_experiment_config,
)
from .freeze import FREEZE_MANIFEST_PATH, manifest_file_hash, verify_freeze_manifest
from .policies import POLICY_IDS
from .profiles import policy, stochastic_process
from .scenarios import core_factor_grid, materialize_families, overlay_from_mapping
from .schemas import ContractError
from .simulator import StochasticCohortSpec, generate_stochastic_cohort, run_engagement_stage


APPLICABLE_CELL_METRICS = {
    "U0": ("unresolved_nonprogression_rate",),
    "U1": (),
    "U2C": ("timeout_activation_rate",),
    "U2O": (),
    "U3": ("unresolved_nonprogression_rate",),
}


def _resolve_repo_path(root: Path, configured: object, diagnostic: str) -> Path:
    relative = Path(str(configured))
    if relative.is_absolute():
        raise ContractError(diagnostic, "configured output path must be repository-relative")
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ContractError(diagnostic, "configured output path escapes the repository")
    return resolved


def _self_hashed(value: Mapping[str, object], field: str) -> bool:
    candidate = dict(value)
    observed = candidate.pop(field, None)
    return observed == canonical_hash(candidate)


def _load_self_hashed(path: Path, field: str, diagnostic: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ContractError(diagnostic, f"artifact is unreadable: {path}") from exc
    if not isinstance(value, dict) or not _self_hashed(value, field):
        raise ContractError(diagnostic, f"artifact self-hash mismatch: {path}")
    return value


def _write_exclusive_json(path: Path, value: Mapping[str, object], diagnostic: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(value, indent=2, sort_keys=True) + "\n"
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(serialized)
    except FileExistsError as exc:
        raise ContractError(
            diagnostic,
            f"append-only artifact already exists and cannot be replaced: {path}",
        ) from exc


def _families(config: Mapping[str, object]):
    return materialize_families(
        core_factor_grid(),
        overlay_from_mapping(config["base_overlay"]),
        int(config["cohort_size"]),
    )


def _attempt_id(family_id: str, replication: int, policy_id: str) -> str:
    return f"{family_id}__R{replication:03d}__{policy_id}"


def _attempt_path(attempts_directory: Path, attempt_id: str) -> Path:
    return attempts_directory / f"{attempt_id}.json"


def _analysis_path(config_path: Path, config: Mapping[str, object], replications: int) -> Path:
    root = config_path.resolve().parents[2]
    directory = _resolve_repo_path(
        root,
        config["outputs"]["analysis_directory"],
        "ANALYSIS_OUTPUT_PATH_INVALID",
    )
    return directory / f"analysis_r{replications:03d}.json"


def _target_replications(config_path: Path, config: Mapping[str, object]) -> int:
    initial = int(config["replications"])
    maximum = int(config["precision"]["maximum_replications"])
    if maximum == initial:
        return initial
    initial_analysis = _analysis_path(config_path, config, initial)
    if initial_analysis.exists():
        analysis = _load_self_hashed(
            initial_analysis,
            "analysis_hash",
            "ANALYSIS_ARTIFACT_INVALID",
        )
        if analysis.get("extension_required") is True:
            return maximum
    return initial


def planned_attempt_count(config_path: Path, *, extension: bool = False) -> int:
    config = load_experiment_config(config_path)
    initial = int(config["replications"])
    maximum = int(config["precision"]["maximum_replications"])
    replication_count = maximum - initial if extension else initial
    return len(_families(config)) * replication_count * len(POLICY_IDS)


def _assert_executable_config(
    config_path: Path,
) -> tuple[dict[str, object], dict[str, object], EvaluationSpecificationSpec]:
    root = config_path.resolve().parents[2]
    manifest = verify_freeze_manifest(root, FREEZE_MANIFEST_PATH)
    validation = validate_experiment_config(config_path)
    config = load_experiment_config(config_path)
    if config["mode"] not in {"confirmatory", "sensitivity"}:
        raise ContractError("RUN_CONFIG_INVALID", "run requires a frozen study config")
    if config["freeze_readiness"] != {"status": "ready", "unresolved_items": []}:
        raise ContractError("RUN_FREEZE_REQUIRED", "config is not marked freeze-ready")
    relative = config_path.resolve().relative_to(root).as_posix()
    if manifest_file_hash(manifest, relative) != _sha256(config_path):
        raise ContractError("RUN_CONFIG_HASH_MISMATCH", "config differs from frozen manifest")
    evaluation_relative = str(config["evaluation_specification_path"])
    evaluation_path = _resolve_repo_path(
        root, evaluation_relative, "RUN_EVALUATION_SPEC_PATH_INVALID"
    )
    if manifest_file_hash(manifest, evaluation_relative) != _sha256(evaluation_path):
        raise ContractError(
            "RUN_EVALUATION_SPEC_HASH_MISMATCH",
            "evaluation specification differs from frozen manifest",
        )
    evaluation = load_evaluation_specification(evaluation_path)
    return config, manifest | {"validated_config": validation}, evaluation


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _evaluation_bridge_receipt(run: object) -> dict[str, object]:
    """Preserve a compact, inspectable receipt for runtime support evaluations."""

    receipt_fields = (
        "evaluation_spec_id",
        "evaluation_specification_hash",
        "action_comparison_schema_id",
        "action_family_id",
        "action_instance_id",
        "action_instance_hash",
        "evidence_state_id",
        "refinement_certificate_id",
        "refinement_certificate_hash",
        "implementation_id",
        "implementation_code_hash",
        "robust_action_support",
    )
    routing_receipts: dict[str, dict[str, object]] = {}
    action_receipts: dict[str, dict[str, object]] = {}
    for trace in run.traces:
        for event in trace.events:
            if event.event_type_id not in {"REPRESENTATION_APPLIED", "ACTION_COMPUTED"}:
                continue
            receipt = {field: event.details.get(field) for field in receipt_fields}
            if any(value is None for value in receipt.values()):
                raise ContractError(
                    "RUN_EVALUATION_RECEIPT_INCOMPLETE",
                    f"support receipt incomplete for {trace.case_id}:{event.event_type_id}",
                )
            target = routing_receipts if event.event_type_id == "REPRESENTATION_APPLIED" else action_receipts
            if trace.case_id in target:
                raise ContractError(
                    "RUN_EVALUATION_RECEIPT_DUPLICATE",
                    f"duplicate support receipt for {trace.case_id}:{event.event_type_id}",
                )
            target[trace.case_id] = receipt
    compared_case_ids = sorted(set(routing_receipts) & set(action_receipts))
    mismatches = [
        case_id for case_id in compared_case_ids
        if routing_receipts[case_id] != action_receipts[case_id]
    ]
    routing_values = list(routing_receipts.values())
    if not routing_values or mismatches:
        raise ContractError(
            "RUN_EVALUATION_RECEIPT_MISMATCH",
            f"routing/action support mismatch for {len(mismatches)} cases",
        )
    specification_ids = sorted({str(item["evaluation_spec_id"]) for item in routing_values})
    specification_hashes = sorted({str(item["evaluation_specification_hash"]) for item in routing_values})
    implementation_hashes = sorted({str(item["implementation_code_hash"]) for item in routing_values})
    if len(specification_ids) != 1 or len(specification_hashes) != 1 or len(implementation_hashes) != 1:
        raise ContractError(
            "RUN_EVALUATION_RECEIPT_IDENTITY_DRIFT",
            "an attempt emitted multiple evaluation or implementation identities",
        )
    value = {
        "schema_version": 1,
        "artifact_kind": "evaluation_bridge_receipt",
        "evaluation_spec_id": specification_ids[0],
        "evaluation_specification_hash": specification_hashes[0],
        "implementation_code_hash": implementation_hashes[0],
        "routing_receipt_count": len(routing_receipts),
        "action_receipt_count": len(action_receipts),
        "routing_action_compared_count": len(compared_case_ids),
        "routing_action_mismatch_count": len(mismatches),
        "action_missing_by_cutoff_count": len(set(routing_receipts) - set(action_receipts)),
        "certificate_counts": dict(sorted(Counter(
            str(item["refinement_certificate_id"]) for item in routing_values
        ).items())),
        "evidence_state_counts": dict(sorted(Counter(
            str(item["evidence_state_id"]) for item in routing_values
        ).items())),
        "support_outcome_counts": dict(sorted(Counter(
            str(bool(item["robust_action_support"])).lower() for item in routing_values
        ).items())),
        "action_instance_inventory_hash": canonical_hash(sorted(
            str(item["action_instance_hash"]) for item in routing_values
        )),
    }
    return value | {"receipt_hash": canonical_hash(value)}


def _attempt_artifact(
    *,
    config: Mapping[str, object],
    manifest: Mapping[str, object],
    family: object,
    replication: int,
    policy_id: str,
    evaluation_specification: EvaluationSpecificationSpec,
) -> dict[str, object]:
    seed_id = f"{config['seed_prefix']}-{family.family_id}-R{replication:03d}"
    cohort = generate_stochastic_cohort(StochasticCohortSpec(
        scenario_id=family.family_id,
        seed_id=seed_id,
        case_ids=tuple(
            f"{family.family_id}-R{replication:03d}-C{index:04d}"
            for index in range(1, int(config["cohort_size"]) + 1)
        ),
        overlay=family.overlay,
    ))
    compiled = compile_configuration(
        configuration_id=f"{family.family_id}-R{replication:03d}-{policy_id}",
        process=stochastic_process(),
        policy=policy(policy_id),
        overlay=family.overlay.to_compilation_overlay(),
        evaluation_spec_id=evaluation_specification.evaluation_spec_id,
        evaluation_specification=evaluation_specification,
    )
    run = run_engagement_stage(cohort, compiled)
    row = _run_metrics(family, replication, policy_id, run)
    attempt_id = _attempt_id(family.family_id, replication, policy_id)
    bridge_receipt = _evaluation_bridge_receipt(run)
    artifact = {
        "schema_version": 3,
        "artifact_kind": "confirmatory_attempt",
        "attempt_id": attempt_id,
        "config_id": config["config_id"],
        "manifest_hash": manifest["manifest_hash"],
        "family_id": family.family_id,
        "family": family.canonical_value(),
        "replication": replication,
        "policy_id": policy_id,
        "seed_id": seed_id,
        "compiled_configuration_hash": canonical_hash(compiled.model_dump(mode="json")),
        "evaluation_bridge_receipt": bridge_receipt,
        "row": row,
        "claim_limit": "confirmatory estimate within the frozen declared model and parameter space; no historical prevalence, legality, or field-effect inference",
    }
    return artifact | {"attempt_hash": canonical_hash(artifact)}


def _validate_attempt(
    path: Path,
    *,
    expected_attempt_id: str | None = None,
    manifest_hash: str | None = None,
    config_id: str | None = None,
) -> dict[str, object]:
    artifact = _load_self_hashed(path, "attempt_hash", "RUN_ATTEMPT_INVALID")
    if artifact.get("artifact_kind") != "confirmatory_attempt":
        raise ContractError("RUN_ATTEMPT_INVALID", f"unexpected attempt kind: {path}")
    if expected_attempt_id is not None and artifact.get("attempt_id") != expected_attempt_id:
        raise ContractError("RUN_ATTEMPT_IDENTITY_MISMATCH", f"attempt identity mismatch: {path}")
    if manifest_hash is not None and artifact.get("manifest_hash") != manifest_hash:
        raise ContractError("RUN_ATTEMPT_FREEZE_MISMATCH", f"attempt uses another freeze: {path}")
    if config_id is not None and artifact.get("config_id") != config_id:
        raise ContractError("RUN_ATTEMPT_CONFIG_MISMATCH", f"attempt uses another config: {path}")
    row = artifact.get("row")
    if not isinstance(row, dict):
        raise ContractError("RUN_ATTEMPT_INVALID", f"attempt metric row is missing: {path}")
    _validate_metric_row(row)
    return artifact


def run_frozen_experiment(
    root: Path,
    config_path: Path,
    *,
    extension: bool = False,
) -> dict[str, object]:
    root = root.resolve()
    config, manifest, evaluation_specification = _assert_executable_config(config_path)
    initial = int(config["replications"])
    maximum = int(config["precision"]["maximum_replications"])
    if extension:
        if config["mode"] != "confirmatory" or maximum <= initial:
            raise ContractError("RUN_EXTENSION_NOT_APPLICABLE", "config has no extension stage")
        analysis_path = _analysis_path(config_path, config, initial)
        if not analysis_path.exists():
            raise ContractError("RUN_EXTENSION_UNAUTHORIZED", "initial analysis receipt is missing")
        analysis = _load_self_hashed(
            analysis_path, "analysis_hash", "ANALYSIS_ARTIFACT_INVALID"
        )
        if analysis.get("extension_required") is not True:
            raise ContractError("RUN_EXTENSION_UNAUTHORIZED", "initial analysis did not require extension")
        replications = range(initial + 1, maximum + 1)
    else:
        replications = range(1, initial + 1)
    attempts_directory = _resolve_repo_path(
        root,
        config["outputs"]["attempts_directory"],
        "RUN_OUTPUT_PATH_INVALID",
    )
    created = 0
    retained = 0
    for family in _families(config):
        for replication in replications:
            for policy_id in POLICY_IDS:
                attempt_id = _attempt_id(family.family_id, replication, policy_id)
                path = _attempt_path(attempts_directory, attempt_id)
                if path.exists():
                    _validate_attempt(
                        path,
                        expected_attempt_id=attempt_id,
                        manifest_hash=str(manifest["manifest_hash"]),
                        config_id=str(config["config_id"]),
                    )
                    retained += 1
                    continue
                artifact = _attempt_artifact(
                    config=config,
                    manifest=manifest,
                    family=family,
                    replication=replication,
                    policy_id=policy_id,
                    evaluation_specification=evaluation_specification,
                )
                _write_exclusive_json(path, artifact, "RUN_APPEND_ONLY_VIOLATION")
                created += 1
    return {
        "status": "complete",
        "config_id": config["config_id"],
        "stage": "extension" if extension else "initial",
        "created_attempts": created,
        "retained_attempts": retained,
        "planned_attempts": created + retained,
        "manifest_hash": manifest["manifest_hash"],
    }


def _expected_attempt_ids(config_path: Path, config: Mapping[str, object]) -> set[str]:
    target = _target_replications(config_path, config)
    return {
        _attempt_id(family.family_id, replication, policy_id)
        for family in _families(config)
        for replication in range(1, target + 1)
        for policy_id in POLICY_IDS
    }


def _collect_attempts(
    root: Path,
    config_path: Path,
    config: Mapping[str, object],
    manifest: Mapping[str, object],
) -> tuple[list[dict[str, object]], set[str], set[str]]:
    attempts_directory = _resolve_repo_path(
        root,
        config["outputs"]["attempts_directory"],
        "RUN_OUTPUT_PATH_INVALID",
    )
    expected = _expected_attempt_ids(config_path, config)
    artifacts: list[dict[str, object]] = []
    observed: set[str] = set()
    if attempts_directory.exists():
        for path in sorted(attempts_directory.glob("*.json")):
            artifact = _validate_attempt(
                path,
                manifest_hash=str(manifest["manifest_hash"]),
                config_id=str(config["config_id"]),
            )
            attempt_id = str(artifact["attempt_id"])
            if path.stem != attempt_id or attempt_id in observed:
                raise ContractError(
                    "RUN_ATTEMPT_IDENTITY_MISMATCH",
                    f"duplicate or filename-mismatched attempt: {path}",
                )
            observed.add(attempt_id)
            artifacts.append(artifact)
    return artifacts, expected - observed, observed - expected


def reconcile_frozen_experiment(root: Path, config_path: Path) -> dict[str, object]:
    root = root.resolve()
    config, manifest, _ = _assert_executable_config(config_path)
    artifacts, missing, unexpected = _collect_attempts(root, config_path, config, manifest)
    target = _target_replications(config_path, config)
    run_index = {
        "schema_version": 1,
        "artifact_kind": "confirmatory_run_index",
        "config_id": config["config_id"],
        "manifest_hash": manifest["manifest_hash"],
        "target_replications": target,
        "attempt_count": len(artifacts),
        "attempts": [
            {
                "attempt_id": artifact["attempt_id"],
                "attempt_hash": artifact["attempt_hash"],
            }
            for artifact in sorted(artifacts, key=lambda item: str(item["attempt_id"]))
        ],
    }
    run_index["run_index_hash"] = canonical_hash(run_index)
    index_path = _resolve_repo_path(
        root, config["outputs"]["run_index_path"], "RUN_OUTPUT_PATH_INVALID"
    )
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(run_index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt = {
        "schema_version": 1,
        "artifact_kind": "confirmatory_reconciliation",
        "config_id": config["config_id"],
        "manifest_hash": manifest["manifest_hash"],
        "target_replications": target,
        "expected_attempt_count": len(_expected_attempt_ids(config_path, config)),
        "observed_attempt_count": len(artifacts),
        "missing_attempt_ids": sorted(missing),
        "unexpected_attempt_ids": sorted(unexpected),
        "status": "complete" if not missing and not unexpected else "incomplete",
        "run_index_hash": run_index["run_index_hash"],
    }
    receipt["reconciliation_hash"] = canonical_hash(receipt)
    reconciliation_path = _resolve_repo_path(
        root, config["outputs"]["reconciliation_path"], "RUN_OUTPUT_PATH_INVALID"
    )
    reconciliation_path.parent.mkdir(parents=True, exist_ok=True)
    reconciliation_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return receipt


def _precision_summary(
    config: Mapping[str, object],
    cells: list[dict[str, object]],
    pairs: list[dict[str, object]],
) -> dict[str, object]:
    rate_mcse = max(
        float(cell[f"{metric}_mcse"])
        for cell in cells
        for metric in APPLICABLE_CELL_METRICS[str(cell["policy_id"])]
    )
    paired_mcse = max(float(item["mcse"]) for item in pairs)
    target_rate = float(config["precision"]["target_rate_mcse"])
    target_paired = float(config["precision"]["target_paired_mcse"])
    return {
        "maximum_rate_mcse": rate_mcse,
        "maximum_paired_mcse": paired_mcse,
        "target_rate_mcse": target_rate,
        "target_paired_mcse": target_paired,
        "rate_target_met": rate_mcse <= target_rate,
        "paired_target_met": paired_mcse <= target_paired,
    }


def _designed_grid_summaries(
    cells: list[dict[str, object]],
) -> dict[str, object]:
    declarations = (
        ("u2c_timeout_by_load", "U2C", "timeout_activation_rate", "load", 36),
        ("u3_unresolved_by_access_barrier", "U3", "unresolved_nonprogression_rate", "access_barrier", 36),
        ("u3_unresolved_by_retrievability", "U3", "unresolved_nonprogression_rate", "retrievability", 54),
        ("u3_unresolved_by_staff_access", "U3", "unresolved_nonprogression_rate", "staff_access", 54),
    )
    output: dict[str, object] = {}
    for summary_id, policy_id, metric, factor, expected_count in declarations:
        grouped: dict[str, list[dict[str, object]]] = {}
        for cell in cells:
            if cell["policy_id"] != policy_id:
                continue
            grouped.setdefault(str(cell["factors"][factor]), []).append(cell)
        levels: list[dict[str, object]] = []
        for level, values in sorted(grouped.items()):
            if len(values) != expected_count:
                raise ContractError(
                    "ANALYSIS_FACTOR_BALANCE_INVALID",
                    f"{summary_id}:{level} has {len(values)} cells; expected {expected_count}",
                )
            estimate = mean(float(item[metric]) for item in values)
            simulation_mcse = sqrt(sum(
                float(item[f"{metric}_mcse"]) ** 2 for item in values
            )) / len(values)
            levels.append({
                "level": level,
                "cell_count": len(values),
                "estimate": estimate,
                "simulation_mcse": simulation_mcse,
            })
        estimates = [float(level["estimate"]) for level in levels]
        output[summary_id] = {
            "policy_id": policy_id,
            "metric": metric,
            "factor": factor,
            "weighting": "unweighted_balanced_designed_cells",
            "levels": levels,
            "range": max(estimates) - min(estimates) if estimates else None,
        }
    return output


def _evaluation_bridge_summary(
    artifacts: list[dict[str, object]],
) -> dict[str, object]:
    receipts = [dict(artifact["evaluation_bridge_receipt"]) for artifact in artifacts]
    specification_ids = sorted({str(item["evaluation_spec_id"]) for item in receipts})
    specification_hashes = sorted({str(item["evaluation_specification_hash"]) for item in receipts})
    implementation_hashes = sorted({str(item["implementation_code_hash"]) for item in receipts})
    if len(specification_ids) != 1 or len(specification_hashes) != 1 or len(implementation_hashes) != 1:
        raise ContractError(
            "ANALYSIS_EVALUATION_RECEIPT_DRIFT",
            "attempts contain multiple evaluation or implementation identities",
        )
    certificate_counts: Counter[str] = Counter()
    evidence_state_counts: Counter[str] = Counter()
    support_outcome_counts: Counter[str] = Counter()
    for receipt in receipts:
        certificate_counts.update(receipt["certificate_counts"])
        evidence_state_counts.update(receipt["evidence_state_counts"])
        support_outcome_counts.update(receipt["support_outcome_counts"])
    value = {
        "schema_version": 1,
        "artifact_kind": "evaluation_bridge_suite_summary",
        "evaluation_spec_id": specification_ids[0],
        "evaluation_specification_hash": specification_hashes[0],
        "implementation_code_hash": implementation_hashes[0],
        "attempt_receipt_count": len(receipts),
        "routing_receipt_count": sum(int(item["routing_receipt_count"]) for item in receipts),
        "action_receipt_count": sum(int(item["action_receipt_count"]) for item in receipts),
        "routing_action_compared_count": sum(int(item["routing_action_compared_count"]) for item in receipts),
        "routing_action_mismatch_count": sum(int(item["routing_action_mismatch_count"]) for item in receipts),
        "action_missing_by_cutoff_count": sum(int(item["action_missing_by_cutoff_count"]) for item in receipts),
        "certificate_counts": dict(sorted(certificate_counts.items())),
        "evidence_state_counts": dict(sorted(evidence_state_counts.items())),
        "support_outcome_counts": dict(sorted(support_outcome_counts.items())),
        "attempt_receipt_inventory_hash": canonical_hash(sorted(
            str(item["receipt_hash"]) for item in receipts
        )),
    }
    return value | {"summary_hash": canonical_hash(value)}


def _svg_document(
    title: str,
    subtitle: str,
    polylines: list[tuple[str, str, list[tuple[float, float]]]],
) -> str:
    width, height = 760, 440
    plot_left, plot_top, plot_width, plot_height = 70, 80, 640, 290
    colors = {"blue": "#276FBF", "red": "#C23B22", "green": "#2E8B57"}
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="30" y="34" font-family="sans-serif" font-size="20">{title}</text>',
        f'<text x="30" y="58" font-family="sans-serif" font-size="12" fill="#444">{subtitle}</text>',
        f'<line x1="{plot_left}" y1="{plot_top + plot_height}" x2="{plot_left + plot_width}" y2="{plot_top + plot_height}" stroke="#222"/>',
        f'<line x1="{plot_left}" y1="{plot_top}" x2="{plot_left}" y2="{plot_top + plot_height}" stroke="#222"/>',
    ]
    for index, (label, color, points) in enumerate(polylines):
        rendered = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        body.append(
            f'<polyline points="{rendered}" fill="none" stroke="{colors[color]}" stroke-width="3"/>'
        )
        for x, y in points:
            body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="{colors[color]}"/>')
        legend_y = 92 + index * 20
        body.append(
            f'<line x1="530" y1="{legend_y}" x2="550" y2="{legend_y}" stroke="{colors[color]}" stroke-width="3"/>'
        )
        body.append(
            f'<text x="558" y="{legend_y + 4}" font-family="sans-serif" font-size="11">{label}</text>'
        )
    body.extend([
        '<text x="380" y="425" text-anchor="middle" font-family="sans-serif" font-size="11">Frozen-model estimates; see analysis receipt for scope and uncertainty</text>',
        "</svg>",
    ])
    return "\n".join(body) + "\n"


def _analysis_figures(
    cells: list[dict[str, object]],
    pairs: list[dict[str, object]],
    *,
    replications: int,
) -> dict[str, str]:
    plot_left, plot_top, plot_width, plot_height = 70.0, 80.0, 640.0, 290.0
    loads = ("0.6", "0.95", "1.2")

    def x(index: int) -> float:
        return plot_left + plot_width * index / (len(loads) - 1)

    def y(rate: float) -> float:
        return plot_top + plot_height * (1 - max(0.0, min(1.0, rate)))

    lines: list[tuple[str, str, list[tuple[float, float]]]] = []
    for policy_id, metric, label, color in (
        ("U2C", "timeout_activation_rate", "U2C timeout activation", "blue"),
        ("U2O", "unsupported_progression_rate", "U2O unsupported progression", "red"),
    ):
        points = []
        for index, load in enumerate(loads):
            values = [
                float(cell[metric])
                for cell in cells
                if cell["policy_id"] == policy_id and cell["factors"]["load"] == load
            ]
            if values:
                points.append((x(index), y(mean(values))))
        lines.append((label, color, points))
    capacity = _svg_document(
        "Capacity and timeout semantics",
        f"Confirmatory analysis at {replications} paired replications per family",
        lines,
    )

    u3_pairs = [
        item for item in pairs
        if item["contrast_id"] == "U3-minus-U0"
        and item["metric"] == "unresolved_nonprogression_rate"
    ]
    ordered = sorted(u3_pairs, key=lambda item: str(item["family_id"]))
    points = [
        (
            plot_left + plot_width * index / max(1, len(ordered) - 1),
            y(float(item["estimate"])),
        )
        for index, item in enumerate(ordered)
    ]
    tradeoff = _svg_document(
        "Information-first unresolved non-progression",
        f"U3-minus-U0 paired differences at {replications} replications per family",
        [("scenario families", "green", points)],
    )
    return {
        f"capacity_timeout_r{replications:03d}.svg": capacity,
        f"information_tradeoff_r{replications:03d}.svg": tradeoff,
    }


def _verify_or_write_figure(path: Path, content: str) -> None:
    encoded = content.encode("utf-8")
    if path.exists():
        if path.read_bytes() != encoded:
            raise ContractError(
                "ANALYSIS_APPEND_ONLY_VIOLATION",
                f"stored figure differs from deterministic recomputation: {path}",
            )
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(content)
    except FileExistsError as exc:
        raise ContractError(
            "ANALYSIS_APPEND_ONLY_VIOLATION",
            f"analysis figure appeared during exclusive creation: {path}",
        ) from exc


def analyze_frozen_experiment(root: Path, config_path: Path) -> dict[str, object]:
    root = root.resolve()
    config, manifest, _ = _assert_executable_config(config_path)
    artifacts, missing, unexpected = _collect_attempts(root, config_path, config, manifest)
    if missing or unexpected:
        raise ContractError(
            "ANALYSIS_RUN_INCOMPLETE",
            f"cannot analyze incomplete run; missing={len(missing)}, unexpected={len(unexpected)}",
        )
    rows = [dict(artifact["row"]) for artifact in artifacts]
    replications = max(int(row["replication"]) for row in rows)
    cells = _summarize_cells(rows)
    pairs = _paired_estimates(rows)
    family_count = len(_families(config))
    precision = _precision_summary(config, cells, pairs)
    reconciliation_path = _resolve_repo_path(
        root, config["outputs"]["reconciliation_path"], "RUN_OUTPUT_PATH_INVALID"
    )
    reconciliation = _load_self_hashed(
        reconciliation_path, "reconciliation_hash", "RUN_RECONCILIATION_INVALID"
    )
    if reconciliation.get("status") != "complete":
        raise ContractError("RUN_RECONCILIATION_INCOMPLETE", str(config["config_id"]))
    initial = int(config["replications"])
    maximum = int(config["precision"]["maximum_replications"])
    extension_required = (
        config["mode"] == "confirmatory"
        and replications == initial
        and maximum > initial
        and (not precision["rate_target_met"] or not precision["paired_target_met"])
    )
    figure_contents = _analysis_figures(cells, pairs, replications=replications)
    analysis_directory = _analysis_path(config_path, config, replications).parent
    figures = [
        {
            "path": (analysis_directory / name).relative_to(root).as_posix(),
            "sha256": sha256(content.encode("utf-8")).hexdigest(),
        }
        for name, content in sorted(figure_contents.items())
    ]
    analysis = {
        "schema_version": 2,
        "artifact_kind": "confirmatory_analysis",
        "config_id": config["config_id"],
        "manifest_hash": manifest["manifest_hash"],
        "reconciliation_hash": reconciliation["reconciliation_hash"],
        "run_index_hash": reconciliation["run_index_hash"],
        "replications": replications,
        "family_count": family_count,
        "attempt_count": len(artifacts),
        "primary_metrics": list(PRIMARY_METRICS),
        "precision": precision,
        "extension_required": extension_required,
        "extension_rule": config["precision"]["extension_rule"],
        "cell_summaries": cells,
        "paired_estimates": pairs,
        "designed_grid_summaries": (
            _designed_grid_summaries(cells)
            if family_count == 108
            else {
                "status": "not_applicable_nonproduction_fixture",
                "family_count": family_count,
            }
        ),
        "common_random_number_diagnostics": _common_random_number_diagnostics(rows),
        "evaluation_bridge_summary": _evaluation_bridge_summary(artifacts),
        "figures": figures,
        "row_hash": canonical_hash(sorted(rows, key=lambda row: (
            str(row["family_id"]), int(row["replication"]), str(row["policy_id"])
        ))),
        "claim_limit": "estimates apply only to the frozen model and designed parameter space; no historical prevalence, legality, or unmodeled field causation",
    }
    analysis["analysis_hash"] = canonical_hash(analysis)
    path = _analysis_path(config_path, config, replications)
    if path.exists():
        observed = _load_self_hashed(path, "analysis_hash", "ANALYSIS_ARTIFACT_INVALID")
        if observed != analysis:
            raise ContractError(
                "ANALYSIS_APPEND_ONLY_VIOLATION",
                f"stored analysis differs from deterministic recomputation: {path}",
            )
        for name, content in figure_contents.items():
            _verify_or_write_figure(analysis_directory / name, content)
        return observed
    for name, content in figure_contents.items():
        _verify_or_write_figure(analysis_directory / name, content)
    _write_exclusive_json(path, analysis, "ANALYSIS_APPEND_ONLY_VIOLATION")
    return analysis
