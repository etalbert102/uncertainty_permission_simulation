from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from uncertainty_permission_simulation.experiments import load_experiment_config
from uncertainty_permission_simulation.schemas import ContractError


ROOT = Path(__file__).resolve().parents[2]
CONFIRMATORY = ROOT / "experiments/configs/confirmatory_v1.yaml"


def _write_config(tmp_path: Path, updates: dict[str, object]) -> Path:
    value = yaml.safe_load(CONFIRMATORY.read_text(encoding="utf-8"))
    for path, replacement in updates.items():
        target = value
        tokens = path.split(".")
        for token in tokens[:-1]:
            target = target[token]
        target[tokens[-1]] = replacement
    output = tmp_path / "candidate.yaml"
    output.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
    return output


@pytest.mark.parametrize(
    ("path", "replacement", "message"),
    (
        ("cohort_size", 79, "80/30/30/60"),
        ("replications", 31, "80/30/30/60"),
        ("precision.maximum_replications", 61, "80/30/30/60"),
        ("base_overlay.administrative_cutoff", "649", "day 650"),
        ("base_overlay.provenance", "sensitivity", "must be stylized"),
        ("analysis.confidence_interval", "bootstrap", "95% MCSE"),
        (
            "freeze_readiness.unresolved_items",
            ["FREEZE_MANIFEST_IMPLEMENTATION"],
            "cannot retain unresolved",
        ),
    ),
)
def test_confirmatory_config_rejects_post_pilot_drift(
    tmp_path: Path,
    path: str,
    replacement: object,
    message: str,
) -> None:
    candidate = _write_config(tmp_path, {path: replacement})
    with pytest.raises(ContractError, match=message):
        load_experiment_config(candidate)


def test_confirmatory_candidate_rejects_metric_reordering(tmp_path: Path) -> None:
    value = yaml.safe_load(CONFIRMATORY.read_text(encoding="utf-8"))
    metrics = deepcopy(value["analysis"]["primary_metrics"])
    metrics.reverse()
    candidate = _write_config(tmp_path, {"analysis.primary_metrics": metrics})
    with pytest.raises(ContractError, match="closed implemented metric order"):
        load_experiment_config(candidate)


def test_confirmatory_candidate_rejects_negative_control_drift(tmp_path: Path) -> None:
    value = yaml.safe_load(CONFIRMATORY.read_text(encoding="utf-8"))
    controls = deepcopy(value["negative_controls"])
    controls.reverse()
    candidate = _write_config(tmp_path, {"negative_controls": controls})
    with pytest.raises(ContractError, match="negative-control IDs or order"):
        load_experiment_config(candidate)


def test_confirmatory_candidate_requires_stored_control_receipt_path(tmp_path: Path) -> None:
    candidate = _write_config(
        tmp_path,
        {"outputs.negative_control_receipt_path": "data/golden_traces/other.json"},
    )
    with pytest.raises(ContractError, match="closed stored negative-control receipt path"):
        load_experiment_config(candidate)
