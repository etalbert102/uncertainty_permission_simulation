from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from uncertainty_permission_simulation.applications.robodebt import (
    load_early_stochastic_adapter,
    load_enhanced_adapter,
)
from uncertainty_permission_simulation.configuration import CompilationError, compile_configuration
from uncertainty_permission_simulation.profiles import policy, stochastic_process
from uncertainty_permission_simulation.simulator import (
    StochasticCohortSpec,
    StochasticInputOverlay,
    generate_stochastic_cohort,
    run_engagement_stage,
)


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "experiments/configs/application_validation_v1.yaml"


def _fixture() -> dict[str, object]:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def _runtime_overlay(
    config: dict[str, object],
    application_id: str,
) -> StochasticInputOverlay:
    stylized = dict(config["stylized_overlay"])
    documented = config["applications"][application_id]["documented_runtime_parameters"]
    values = stylized | documented
    return StochasticInputOverlay(**{
        key: value if key in {"overlay_id", "provenance"} else Decimal(str(value))
        for key, value in values.items()
    })


@pytest.mark.parametrize(
    ("application_id", "loader", "expected_owner"),
    (
        ("early", load_early_stochastic_adapter, "R-OCI-Early@1"),
        ("enhanced", load_enhanced_adapter, "R-OCI-Enhanced@1"),
    ),
)
def test_application_adapter_matches_semantically_equivalent_synthetic_profile(
    application_id: str,
    loader,
    expected_owner: str,
) -> None:
    config = _fixture()
    application = config["applications"][application_id]
    input_overlay = _runtime_overlay(config, application_id)
    cohort = generate_stochastic_cohort(StochasticCohortSpec(
        scenario_id=f"APPLICATION-EQUIVALENCE-{application_id.upper()}",
        seed_id=config["seed_id"],
        case_ids=tuple(config["case_ids"]),
        overlay=input_overlay,
    ))
    process, historical_profile = loader(ROOT / application["source_fixture"])
    active_policy = policy(config["active_policy_id"])
    application_compiled = compile_configuration(
        configuration_id=f"APPLICATION-{application_id.upper()}",
        process=process,
        policy=active_policy,
        overlay=input_overlay.to_compilation_overlay(
            exclude_slot_ids=frozenset({"response_deadline"}),
        ),
        evaluation_spec_id=config["evaluation_spec_id"],
        application_mapping_id=application["application_mapping_id"],
    )
    synthetic_compiled = compile_configuration(
        configuration_id=f"SYNTHETIC-{application_id.upper()}",
        process=stochastic_process(),
        policy=active_policy,
        overlay=input_overlay.to_compilation_overlay(),
        evaluation_spec_id=config["evaluation_spec_id"],
    )

    application_run = run_engagement_stage(cohort, application_compiled)
    synthetic_run = run_engagement_stage(cohort, synthetic_compiled)
    assert application_run == synthetic_run
    assert historical_profile.profile_id.startswith(
        "R-OCI-Early" if application_id == "early" else "R-OCI-Enhanced"
    )
    receipt_by_slot = {
        receipt.slot_id: receipt for receipt in application_compiled.receipts
    }
    assert receipt_by_slot["response_deadline"].provenance == "documented"
    assert receipt_by_slot["response_deadline"].owner_id == expected_owner
    assert all(
        receipt.provenance == "stylized"
        and receipt.owner_id == config["stylized_overlay"]["overlay_id"]
        for slot_id, receipt in receipt_by_slot.items()
        if slot_id != "response_deadline"
    )
    assert set(receipt_by_slot) == set(input_overlay.canonical_value()) - {
        "overlay_id", "provenance",
    }


@pytest.mark.parametrize(
    ("application_id", "loader"),
    (
        ("early", load_early_stochastic_adapter),
        ("enhanced", load_enhanced_adapter),
    ),
)
def test_documented_adapter_value_cannot_be_overridden(
    application_id: str,
    loader,
) -> None:
    config = _fixture()
    application = config["applications"][application_id]
    input_overlay = _runtime_overlay(config, application_id)
    process, _ = loader(ROOT / application["source_fixture"])
    with pytest.raises(CompilationError, match="PROFILE_PARAMETER_CONFLICT"):
        compile_configuration(
            configuration_id=f"INVALID-{application_id.upper()}",
            process=process,
            policy=policy(config["active_policy_id"]),
            overlay=input_overlay.to_compilation_overlay(),
            evaluation_spec_id=config["evaluation_spec_id"],
            application_mapping_id=application["application_mapping_id"],
        )


def test_application_validation_overlay_is_complete_and_separate_from_sources() -> None:
    config = _fixture()
    early = _runtime_overlay(config, "early")
    expected_stylized_slots = set(early.canonical_value()) - {
        "overlay_id", "provenance", "response_deadline",
    }
    assert set(config["stylized_overlay"]) - {"overlay_id", "provenance"} == expected_stylized_slots
    assert config["stylized_overlay"]["provenance"] == "stylized"
    assert all(
        set(application["documented_runtime_parameters"]) == {"response_deadline"}
        for application in config["applications"].values()
    )
