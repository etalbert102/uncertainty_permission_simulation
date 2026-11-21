from pathlib import Path

from uncertainty_permission_simulation.experiments import (
    dummy_analysis_receipt,
    validate_experiment_config,
)
from uncertainty_permission_simulation.worked_trace import build_worked_trace


ROOT = Path(__file__).resolve().parents[2]
PILOT = ROOT / "experiments/configs/pilot_v1.yaml"
CONFIRMATORY = ROOT / "experiments/configs/confirmatory_v1.yaml"
SENSITIVITY = ROOT / "experiments/configs/sensitivity_information_latency_v1.yaml"


def test_pilot_config_closes_development_grid_without_running_confirmatory() -> None:
    result = validate_experiment_config(PILOT)
    assert result["status"] == "valid"
    assert result["mode"] == "development_pilot"
    assert result["family_count"] == 15
    assert result["policy_count"] == 5


def test_dummy_analysis_pipeline_exercises_cells_and_paired_estimates() -> None:
    result = dummy_analysis_receipt()
    assert result["artifact_kind"] == "dummy_analysis_receipt"
    assert result["cell_count"] == 5
    assert result["paired_estimate_count"] == 15
    assert len(result["receipt_hash"]) == 64


def test_slice4_confirmatory_freeze_ready_config_closes_grid_seeds_and_pilot_decisions() -> None:
    result = validate_experiment_config(CONFIRMATORY)
    assert result["status"] == "valid_candidate"
    assert result["mode"] == "confirmatory"
    assert result["family_count"] == 108
    assert result["policy_count"] == 5
    assert result["replications"] == 30
    assert result["cohort_size"] == 80
    assert result["seed_count"] == 108 * 30
    assert len(result["seed_inventory_hash"]) == 64
    assert result["negative_control_receipt_hash"] == "a90f810032f3b0af9acde802401fd07294ceb42d69575df32226f35a9014b45b"
    assert result["freeze_readiness"] == {"status": "ready", "unresolved_items": []}


def test_slice4_information_latency_sensitivity_is_separate_and_prespecified() -> None:
    result = validate_experiment_config(SENSITIVITY)
    assert result["status"] == "valid_candidate"
    assert result["mode"] == "sensitivity"
    assert result["family_count"] == 108
    assert result["seed_count"] == 108 * 30


def test_prespecified_worked_trace_is_compiled_and_oracle_separated() -> None:
    result = build_worked_trace(ROOT, PILOT)
    assert result["specification_id"] == "RB-WORKED-TRACE-001"
    assert result["randomness"] == {"mode": "deterministic", "keyed_draws": []}
    assert result["compilation"]["baseline"]["unresolved_parameter_slot_ids"] == []
    assert result["compilation"]["repair"]["unresolved_parameter_slot_ids"] == []
    assert result["arms"]["baseline"]["policy_id"] == "U1"
    assert result["arms"]["repair"]["policy_id"] == "U3"
    assert result["held_input_hash"]
    assert len(result["assessments"]["baseline"]) == 6
    assert len(result["assessments"]["repair"]) == 6
