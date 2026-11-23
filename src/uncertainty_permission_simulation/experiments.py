"""Development-pilot and frozen-run orchestration with aggregate-only analysis."""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal
from hashlib import sha256
import json
from math import sqrt
from pathlib import Path
from statistics import mean, stdev
from time import monotonic
from typing import Iterable, Mapping

import yaml

from .configuration import (
    compile_configuration,
    load_evaluation_specification,
    period_evidence_evaluation_specification,
)
from .negative_controls import (
    CONFIRMATORY_NEGATIVE_CONTROL_IDS,
    NEGATIVE_CONTROL_RECEIPT_PATH,
    SENSITIVITY_NEGATIVE_CONTROL_IDS,
    verify_stored_negative_control_receipt,
)
from .policies import POLICY_IDS
from .profiles import policy, stochastic_process
from .scenarios import (
    ScenarioFamily,
    core_factor_grid,
    development_factor_subset,
    materialize_families,
    overlay_from_mapping,
)
from .schemas import ContractError
from .simulator import StochasticCohortSpec, generate_stochastic_cohort, run_engagement_stage


PRIMARY_METRICS = (
    "timeout_activation_rate",
    "unresolved_nonprogression_rate",
)

CELL_RATE_METRICS = (
    "review_request_rate",
    "timeout_activation_rate",
    "supported_progression_rate",
    "unsupported_progression_rate",
    "evidence_only_failure_rate",
    "authorization_only_failure_rate",
    "joint_evidence_authorization_failure_rate",
    "evidentially_unsupported_progression_rate",
    "unauthorized_progression_rate",
    "adequate_response_evidence_rate",
    "retrieval_request_rate",
    "retrieved_evidence_rate",
    "unresolved_after_acquisition_rate",
    "evidence_requested_rate",
    "held_rate",
    "pre_action_open_rate",
    "unresolved_nonprogression_rate",
    "supported_recovery_entry_rate",
    "unsupported_recovery_entry_rate",
    "no_recovery_entry_rate",
    "recipient_burden_rate",
    "agency_workload_rate",
)

CORE_CONFIG_ID = "CONFIRMATORY-V4"
SENSITIVITY_CONFIG_ID = "SENSITIVITY-INFORMATION-LATENCY-V4"
EXPECTED_OUTPUTS = {
    "confirmatory": {
        "attempts_directory": "outputs/confirmatory_v4/attempts",
        "run_index_path": "outputs/confirmatory_v4/run_index.json",
        "reconciliation_path": "outputs/confirmatory_v4/reconciliation.json",
        "analysis_directory": "outputs/confirmatory_v4/analysis",
        "negative_control_receipt_path": str(NEGATIVE_CONTROL_RECEIPT_PATH),
    },
    "sensitivity": {
        "attempts_directory": "outputs/sensitivity_information_latency_v4/attempts",
        "run_index_path": "outputs/sensitivity_information_latency_v4/run_index.json",
        "reconciliation_path": "outputs/sensitivity_information_latency_v4/reconciliation.json",
        "analysis_directory": "outputs/sensitivity_information_latency_v4/analysis",
        "negative_control_receipt_path": str(NEGATIVE_CONTROL_RECEIPT_PATH),
    },
}


def canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def load_experiment_config(path: Path) -> dict[str, object]:
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ContractError("EXPERIMENT_CONFIG_INVALID", "experiment config must be a mapping")
    common_required = {
        "config_id", "mode", "policy_ids", "cohort_size", "replications", "seed_prefix",
        "base_overlay", "runtime", "precision", "outputs",
    }
    missing = common_required - set(config)
    if missing:
        raise ContractError("EXPERIMENT_CONFIG_INVALID", f"missing config fields {sorted(missing)}")
    if config["mode"] not in {"development_pilot", "confirmatory", "sensitivity"}:
        raise ContractError(
            "EXPERIMENT_CONFIG_INVALID",
            "mode must be development_pilot, confirmatory, or sensitivity",
        )
    for field_name in ("config_id", "seed_prefix"):
        if not isinstance(config[field_name], str) or not config[field_name]:
            raise ContractError("EXPERIMENT_CONFIG_INVALID", f"{field_name} must be nonempty")
    policy_ids = tuple(config["policy_ids"])
    if len(policy_ids) != len(POLICY_IDS) or set(policy_ids) != set(POLICY_IDS):
        raise ContractError("EXPERIMENT_CONFIG_INVALID", f"policy_ids must equal {POLICY_IDS}")
    for name in ("cohort_size", "replications"):
        value = config[name]
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ContractError("EXPERIMENT_CONFIG_INVALID", f"{name} must be a positive integer")
    if config["mode"] == "development_pilot":
        count = config.get("development_family_count")
        if not isinstance(count, int) or isinstance(count, bool) or not 12 <= count <= 18:
            raise ContractError("EXPERIMENT_CONFIG_INVALID", "pilot requires 12-18 development families")
    else:
        design_role = config.get("design_role")
        expected_role = "core_confirmatory" if config["mode"] == "confirmatory" else "prespecified_sensitivity"
        if design_role != expected_role:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                f"{config['mode']} config requires design_role={expected_role}",
            )
        analysis = config.get("analysis")
        if not isinstance(analysis, dict):
            raise ContractError("EXPERIMENT_CONFIG_INVALID", "frozen config requires an analysis mapping")
        if tuple(analysis.get("primary_metrics", ())) != PRIMARY_METRICS:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "analysis.primary_metrics must match the closed implemented metric order",
            )
        expected_config_id = (
            CORE_CONFIG_ID if config["mode"] == "confirmatory" else SENSITIVITY_CONFIG_ID
        )
        if config["config_id"] != expected_config_id:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                f"{config['mode']} config_id must be {expected_config_id}",
            )
        evaluation_path = config.get("evaluation_specification_path")
        if not isinstance(evaluation_path, str) or not evaluation_path:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "frozen config requires evaluation_specification_path",
            )
        relative_evaluation_path = Path(evaluation_path)
        root = path.resolve().parents[2]
        resolved_evaluation_path = (root / relative_evaluation_path).resolve()
        if relative_evaluation_path.is_absolute() or not resolved_evaluation_path.is_relative_to(root):
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "evaluation specification path must remain repository-relative",
            )
        if analysis.get("confidence_interval") != "normal_95_from_replication_mcse":
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "frozen analysis requires the declared 95% MCSE interval rule",
            )
        controls = config.get("negative_controls")
        if not isinstance(controls, list) or len(controls) != len(set(controls)) or not controls:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "frozen config requires unique negative-control IDs",
            )
        expected_controls = (
            CONFIRMATORY_NEGATIVE_CONTROL_IDS
            if config["mode"] == "confirmatory"
            else SENSITIVITY_NEGATIVE_CONTROL_IDS
        )
        if tuple(controls) != expected_controls:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                f"{config['mode']} negative-control IDs or order differ from the closed contract",
            )
        outputs = config["outputs"]
        if not isinstance(outputs, dict) or outputs != EXPECTED_OUTPUTS[config["mode"]]:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                f"{config['mode']} outputs must match the closed Freeze 5 paths",
            )
        readiness = config.get("freeze_readiness")
        if not isinstance(readiness, dict) or readiness.get("status") not in {"blocked", "ready"}:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "frozen config requires explicit freeze_readiness status",
            )
        unresolved = readiness.get("unresolved_items")
        if not isinstance(unresolved, list) or len(unresolved) != len(set(unresolved)):
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "freeze_readiness.unresolved_items must be a unique list",
            )
        if readiness["status"] == "ready" and unresolved:
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "ready config cannot retain unresolved freeze items",
            )
        if config["mode"] == "sensitivity":
            if config.get("parent_config_id") != CORE_CONFIG_ID:
                raise ContractError(
                    "EXPERIMENT_CONFIG_INVALID",
                    f"sensitivity config must name {CORE_CONFIG_ID} as parent",
                )
            if not isinstance(config.get("sensitivity_id"), str) or not config["sensitivity_id"]:
                raise ContractError(
                    "EXPERIMENT_CONFIG_INVALID",
                    "sensitivity config requires a nonempty sensitivity_id",
                )
    precision = config["precision"]
    if not isinstance(precision, dict):
        raise ContractError("EXPERIMENT_CONFIG_INVALID", "precision must be a mapping")
    minimum = int(precision["minimum_replications"])
    maximum = int(precision["maximum_replications"])
    replication_count = int(config["replications"])
    valid_replication_rule = (
        1 <= replication_count <= minimum <= maximum <= 100
        if config["mode"] == "development_pilot"
        else 1 <= minimum <= replication_count <= maximum <= 100
    )
    if not valid_replication_rule:
        raise ContractError(
            "EXPERIMENT_CONFIG_INVALID",
            "replication counts conflict with the pilot/frozen precision bounds or exceed 100",
        )
    overlay = overlay_from_mapping(config["base_overlay"])
    expected_provenance = "sensitivity" if config["mode"] == "sensitivity" else "stylized"
    if overlay.provenance != expected_provenance:
        raise ContractError(
            "EXPERIMENT_CONFIG_INVALID",
            f"{config['mode']} overlay provenance must be {expected_provenance}",
        )
    if config["mode"] == "confirmatory":
        if (config["cohort_size"], config["replications"], minimum, maximum) != (80, 30, 30, 60):
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "core confirmatory config must preserve the Slice 3 80/30/30/60 decision",
            )
        if overlay.administrative_cutoff != Decimal("650"):
            raise ContractError(
                "EXPERIMENT_CONFIG_INVALID",
                "core confirmatory administrative cutoff must remain day 650",
            )
    return config


def validate_experiment_config(path: Path) -> dict[str, object]:
    config = load_experiment_config(path)
    if config["mode"] != "development_pilot":
        root = path.resolve().parents[2]
        load_evaluation_specification(
            (root / str(config["evaluation_specification_path"])).resolve()
        )
    negative_control_receipt: dict[str, object] | None = None
    if (
        config["mode"] != "development_pilot"
        and "NEGATIVE_CONTROL_EXECUTION_RECEIPT"
        not in config["freeze_readiness"]["unresolved_items"]
    ):
        root = path.resolve().parents[2]
        confirmatory_path = (
            path.resolve()
            if config["mode"] == "confirmatory"
            else path.resolve().parent / "confirmatory_v1.yaml"
        )
        negative_control_receipt = verify_stored_negative_control_receipt(
            root,
            confirmatory_path,
        )
    factors = (
        development_factor_subset(int(config["development_family_count"]))
        if config["mode"] == "development_pilot"
        else core_factor_grid()
    )
    families = materialize_families(
        factors,
        overlay_from_mapping(config["base_overlay"]),
        int(config["cohort_size"]),
    )
    invalid = [family for family in families if family.validity_status != "valid"]
    if invalid:
        detail = ", ".join(f"{item.family_id}:{item.invalid_reason}" for item in invalid)
        raise ContractError("SCENARIO_GRID_INVALID", detail)
    result = {
        "status": "valid" if config["mode"] == "development_pilot" else "valid_candidate",
        "config_id": config["config_id"],
        "mode": config["mode"],
        "family_count": len(families),
        "policy_count": len(POLICY_IDS),
        "replications": config["replications"],
        "cohort_size": config["cohort_size"],
        "config_hash": canonical_hash(config),
        "scenario_hash": canonical_hash([family.canonical_value() for family in families]),
    }
    if config["mode"] != "development_pilot":
        seed_ids = tuple(
            f"{config['seed_prefix']}-{family.family_id}-R{replication:03d}"
            for family in families
            for replication in range(1, int(config["replications"]) + 1)
        )
        result.update({
            "seed_count": len(seed_ids),
            "seed_inventory_hash": canonical_hash(seed_ids),
            "freeze_readiness": config["freeze_readiness"],
            "negative_control_receipt_hash": (
                negative_control_receipt["receipt_hash"]
                if negative_control_receipt is not None else None
            ),
        })
    return result


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _nullable_rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _validate_metric_row(row: Mapping[str, object]) -> None:
    """Fail closed when raw counts do not implement the active metric contract."""

    integer_fields = (
        "case_count",
        "review_request_count",
        "timely_review_count",
        "timeout_activation_count",
        "gate_applicable_count",
        "gate_safe_count",
        "supported_progression_count",
        "unsupported_progression_count",
        "evidence_only_failure_count",
        "authorization_only_failure_count",
        "joint_evidence_authorization_failure_count",
        "evidentially_unsupported_progression_count",
        "unauthorized_progression_count",
        "adequate_response_evidence_count",
        "retrieval_request_count",
        "retrieved_evidence_count",
        "unresolved_after_acquisition_count",
        "evidence_requested_count",
        "held_count",
        "pre_action_open_count",
        "unresolved_nonprogression_count",
        "supported_recovery_entry_count",
        "unsupported_recovery_entry_count",
        "no_recovery_entry_count",
    )
    for field in integer_fields:
        value = row.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ContractError(
                "METRIC_COUNT_INVALID",
                f"metric count must be a nonnegative integer: {field}",
            )
    cases = int(row["case_count"])
    state_total = sum(int(row[field]) for field in (
        "supported_progression_count",
        "unsupported_progression_count",
        "evidence_requested_count",
        "held_count",
        "pre_action_open_count",
    ))
    if state_total != cases:
        raise ContractError(
            "METRIC_DECISION_PARTITION_INVALID",
            f"decision states sum to {state_total}, expected {cases}",
        )
    progression_failure_total = sum(int(row[field]) for field in (
        "evidence_only_failure_count",
        "authorization_only_failure_count",
        "joint_evidence_authorization_failure_count",
    ))
    if progression_failure_total != int(row["unsupported_progression_count"]):
        raise ContractError(
            "METRIC_PROGRESSION_FAILURE_PARTITION_INVALID",
            "exclusive evidence, authorization, and joint failures do not equal unsupported progression",
        )
    if (
        int(row["evidentially_unsupported_progression_count"])
        != int(row["evidence_only_failure_count"])
        + int(row["joint_evidence_authorization_failure_count"])
    ):
        raise ContractError(
            "METRIC_EVIDENCE_FAILURE_UNION_INVALID",
            "evidentially unsupported progression does not equal evidence-only plus joint failures",
        )
    if (
        int(row["unauthorized_progression_count"])
        != int(row["authorization_only_failure_count"])
        + int(row["joint_evidence_authorization_failure_count"])
    ):
        raise ContractError(
            "METRIC_AUTHORIZATION_FAILURE_UNION_INVALID",
            "unauthorized progression does not equal authorization-only plus joint failures",
        )
    if int(row["retrieved_evidence_count"]) > int(row["retrieval_request_count"]):
        raise ContractError(
            "METRIC_RETRIEVAL_NUMERATOR_INVALID",
            "retrieved evidence exceeds retrieval requests",
        )
    acquisition_total = (
        int(row["adequate_response_evidence_count"])
        + int(row["retrieved_evidence_count"])
        + int(row["unresolved_after_acquisition_count"])
    )
    if acquisition_total != cases:
        raise ContractError(
            "METRIC_ACQUISITION_PARTITION_INVALID",
            f"evidence-acquisition stages sum to {acquisition_total}, expected {cases}",
        )
    if row.get("policy_id") == "U3":
        if (
            int(row["adequate_response_evidence_count"])
            + int(row["retrieved_evidence_count"])
            != int(row["supported_progression_count"])
        ):
            raise ContractError(
                "METRIC_U3_SUPPORTED_STAGE_INVALID",
                "U3 pre-retrieval and retrieved evidence do not equal supported progression",
            )
        if int(row["unresolved_after_acquisition_count"]) != int(row["review_request_count"]):
            raise ContractError(
                "METRIC_U3_REVIEW_STAGE_INVALID",
                "U3 unresolved acquisition cases do not equal review requests",
            )
    unresolved = sum(int(row[field]) for field in (
        "evidence_requested_count", "held_count", "pre_action_open_count"
    ))
    if unresolved != int(row["unresolved_nonprogression_count"]):
        raise ContractError(
            "METRIC_UNRESOLVED_COUNT_INVALID",
            "unresolved non-progression does not equal evidence-requested, held, and pre-action-open counts",
        )
    recovery_total = sum(int(row[field]) for field in (
        "supported_recovery_entry_count",
        "unsupported_recovery_entry_count",
        "no_recovery_entry_count",
    ))
    if recovery_total != cases:
        raise ContractError(
            "METRIC_RECOVERY_PARTITION_INVALID",
            f"recovery-entry states sum to {recovery_total}, expected {cases}",
        )
    if (
        int(row["supported_recovery_entry_count"])
        > int(row["supported_progression_count"])
        or int(row["unsupported_recovery_entry_count"])
        > int(row["unsupported_progression_count"])
    ):
        raise ContractError(
            "METRIC_RECOVERY_ENTRY_ORPHANED",
            "recovery-path entry exists without a progression in the same support state",
        )
    bounded_pairs = (
        ("timely_review_count", "review_request_count"),
        ("timeout_activation_count", "review_request_count"),
        ("gate_safe_count", "gate_applicable_count"),
    )
    for numerator, denominator in bounded_pairs:
        if int(row[numerator]) > int(row[denominator]):
            raise ContractError(
                "METRIC_NUMERATOR_EXCEEDS_DENOMINATOR",
                f"{numerator} exceeds {denominator}",
            )
    if int(row["timely_review_count"]) + int(row["timeout_activation_count"]) != int(row["review_request_count"]):
        raise ContractError(
            "METRIC_TIMEOUT_PARTITION_INVALID",
            "timely review and timeout activation do not partition required reviews",
        )
    for rate_name, numerator, denominator in (
        ("conditional_timely_review_rate", "timely_review_count", "review_request_count"),
        ("conditional_gate_safety_rate", "gate_safe_count", "gate_applicable_count"),
    ):
        expected = _nullable_rate(int(row[numerator]), int(row[denominator]))
        if row.get(rate_name) != expected:
            raise ContractError(
                "METRIC_NULLABILITY_INVALID",
                f"{rate_name} must be null exactly when {denominator} is zero",
            )
    for rate_name, count_name in (
        ("review_request_rate", "review_request_count"),
        ("timeout_activation_rate", "timeout_activation_count"),
        ("supported_progression_rate", "supported_progression_count"),
        ("unsupported_progression_rate", "unsupported_progression_count"),
        ("evidence_only_failure_rate", "evidence_only_failure_count"),
        ("authorization_only_failure_rate", "authorization_only_failure_count"),
        ("joint_evidence_authorization_failure_rate", "joint_evidence_authorization_failure_count"),
        ("evidentially_unsupported_progression_rate", "evidentially_unsupported_progression_count"),
        ("unauthorized_progression_rate", "unauthorized_progression_count"),
        ("adequate_response_evidence_rate", "adequate_response_evidence_count"),
        ("retrieval_request_rate", "retrieval_request_count"),
        ("retrieved_evidence_rate", "retrieved_evidence_count"),
        ("unresolved_after_acquisition_rate", "unresolved_after_acquisition_count"),
        ("evidence_requested_rate", "evidence_requested_count"),
        ("held_rate", "held_count"),
        ("pre_action_open_rate", "pre_action_open_count"),
        ("unresolved_nonprogression_rate", "unresolved_nonprogression_count"),
        ("supported_recovery_entry_rate", "supported_recovery_entry_count"),
        ("unsupported_recovery_entry_rate", "unsupported_recovery_entry_count"),
        ("no_recovery_entry_rate", "no_recovery_entry_count"),
    ):
        expected = _rate(int(row[count_name]), cases)
        if row.get(rate_name) != expected:
            raise ContractError(
                "METRIC_RATE_COUNT_MISMATCH",
                f"{rate_name} does not equal {count_name}/case_count",
            )


def _run_metrics(family: ScenarioFamily, replication: int, policy_id: str, run: object) -> dict[str, object]:
    telemetry = run.telemetry
    cases = telemetry.case_count
    review_requests = telemetry.review_queue_count
    censoring_reasons: dict[str, int] = defaultdict(int)
    for trace in run.traces:
        for event in trace.events:
            if event.event_type_id == "CASE_CLOSED" and event.details.get("right_censored"):
                censoring_reasons[str(event.details.get("censoring_reason", "unspecified"))] += 1
    timeout_activation_count = review_requests - telemetry.timely_review_count
    supported_progression_count = telemetry.supported_progression_count
    unsupported_progression_count = telemetry.unsupported_progression_count
    evidence_only_failure_count = sum(
        trace.action_decision is not None
        and trace.action_decision.action == "progress"
        and not trace.action_decision.evidence_sufficient
        and not trace.action_decision.unauthorized_progression
        for trace in run.traces
    )
    authorization_only_failure_count = sum(
        trace.action_decision is not None
        and trace.action_decision.action == "progress"
        and trace.action_decision.evidence_sufficient
        and trace.action_decision.unauthorized_progression
        for trace in run.traces
    )
    joint_evidence_authorization_failure_count = sum(
        trace.action_decision is not None
        and trace.action_decision.action == "progress"
        and not trace.action_decision.evidence_sufficient
        and trace.action_decision.unauthorized_progression
        for trace in run.traces
    )
    adequate_response_evidence_count = telemetry.adequate_response_evidence_count
    retrieval_request_count = telemetry.retrieval_request_count
    retrieved_evidence_count = telemetry.retrieved_evidence_count
    unresolved_after_acquisition_count = (
        cases - adequate_response_evidence_count - retrieved_evidence_count
    )
    evidence_requested_count = telemetry.request_evidence_action_count
    held_count = telemetry.hold_count
    pre_action_open_count = cases - telemetry.action_count
    unresolved_nonprogression_count = (
        evidence_requested_count + held_count + pre_action_open_count
    )
    supported_recovery_entry_count = telemetry.supported_exposure_count
    unsupported_recovery_entry_count = telemetry.unsupported_exposure_count
    no_recovery_entry_count = cases - telemetry.external_exposure_count
    row = {
        "family_id": family.family_id,
        **family.factors.canonical_value(),
        "replication": replication,
        "policy_id": policy_id,
        "case_count": cases,
        "event_count": telemetry.event_count,
        "cohort_hash": run.cohort_hash,
        "event_hash": telemetry.event_hash,
        "review_request_count": review_requests,
        "timely_review_count": telemetry.timely_review_count,
        "timeout_activation_count": timeout_activation_count,
        "gate_applicable_count": telemetry.gate_applicable_count,
        "gate_safe_count": telemetry.gate_safe_count,
        "supported_progression_count": supported_progression_count,
        "unsupported_progression_count": unsupported_progression_count,
        "evidence_only_failure_count": evidence_only_failure_count,
        "authorization_only_failure_count": authorization_only_failure_count,
        "joint_evidence_authorization_failure_count": joint_evidence_authorization_failure_count,
        "evidentially_unsupported_progression_count": telemetry.evidentially_unsupported_progression_count,
        "unauthorized_progression_count": telemetry.unauthorized_progression_count,
        "adequate_response_evidence_count": adequate_response_evidence_count,
        "retrieval_request_count": retrieval_request_count,
        "retrieved_evidence_count": retrieved_evidence_count,
        "unresolved_after_acquisition_count": unresolved_after_acquisition_count,
        "evidence_requested_count": evidence_requested_count,
        "held_count": held_count,
        "pre_action_open_count": pre_action_open_count,
        "unresolved_nonprogression_count": unresolved_nonprogression_count,
        "supported_recovery_entry_count": supported_recovery_entry_count,
        "unsupported_recovery_entry_count": unsupported_recovery_entry_count,
        "no_recovery_entry_count": no_recovery_entry_count,
        "review_request_rate": _rate(review_requests, cases),
        "timeout_activation_rate": _rate(timeout_activation_count, cases),
        "conditional_timely_review_rate": _nullable_rate(
            telemetry.timely_review_count, review_requests
        ),
        "conditional_gate_safety_rate": _nullable_rate(
            telemetry.gate_safe_count, telemetry.gate_applicable_count
        ),
        "supported_progression_rate": _rate(supported_progression_count, cases),
        "unsupported_progression_rate": _rate(unsupported_progression_count, cases),
        "evidence_only_failure_rate": _rate(evidence_only_failure_count, cases),
        "authorization_only_failure_rate": _rate(authorization_only_failure_count, cases),
        "joint_evidence_authorization_failure_rate": _rate(joint_evidence_authorization_failure_count, cases),
        "evidentially_unsupported_progression_rate": _rate(
            telemetry.evidentially_unsupported_progression_count, cases
        ),
        "unauthorized_progression_rate": _rate(telemetry.unauthorized_progression_count, cases),
        "adequate_response_evidence_rate": _rate(adequate_response_evidence_count, cases),
        "retrieval_request_rate": _rate(retrieval_request_count, cases),
        "retrieved_evidence_rate": _rate(retrieved_evidence_count, cases),
        "unresolved_after_acquisition_rate": _rate(unresolved_after_acquisition_count, cases),
        "evidence_requested_rate": _rate(evidence_requested_count, cases),
        "held_rate": _rate(held_count, cases),
        "pre_action_open_rate": _rate(pre_action_open_count, cases),
        "unresolved_nonprogression_rate": _rate(unresolved_nonprogression_count, cases),
        "supported_recovery_entry_rate": _rate(supported_recovery_entry_count, cases),
        "unsupported_recovery_entry_rate": _rate(unsupported_recovery_entry_count, cases),
        "no_recovery_entry_rate": _rate(no_recovery_entry_count, cases),
        "recipient_burden_rate": _rate(
            telemetry.response_count + telemetry.assistance_request_count,
            cases,
        ),
        "agency_workload_rate": _rate(
            telemetry.assistance_completed_count
            + telemetry.retrieval_request_count
            + telemetry.review_completed_count
            + telemetry.reassessment_completed_count,
            cases,
        ),
        "censoring_reason_counts": dict(sorted(censoring_reasons.items())),
        "review_mean_wait_time": float(
            telemetry.review_total_wait_time / Decimal(review_requests)
        ) if review_requests else 0.0,
        "correction_mean_exposure_time": float(
            telemetry.correction_total_exposure_time / Decimal(telemetry.correction_executed_count)
        ) if telemetry.correction_executed_count else 0.0,
    }
    _validate_metric_row(row)
    return row


def _cluster_jackknife_ratio(
    values: list[Mapping[str, object]],
    numerator: str,
    denominator: str,
) -> dict[str, object]:
    total_numerator = sum(int(item[numerator]) for item in values)
    total_denominator = sum(int(item[denominator]) for item in values)
    zero_denominator_replications = sum(int(item[denominator]) == 0 for item in values)
    estimate = _nullable_rate(total_numerator, total_denominator)
    mcse: float | None = None
    if estimate is not None and len(values) > 1:
        leave_one_out: list[float] = []
        for item in values:
            remaining_denominator = total_denominator - int(item[denominator])
            if remaining_denominator == 0:
                leave_one_out = []
                break
            leave_one_out.append(
                (total_numerator - int(item[numerator])) / remaining_denominator
            )
        if len(leave_one_out) == len(values):
            jackknife_mean = mean(leave_one_out)
            mcse = sqrt(
                (len(values) - 1)
                / len(values)
                * sum((value - jackknife_mean) ** 2 for value in leave_one_out)
            )
    return {
        "numerator_count": total_numerator,
        "denominator_count": total_denominator,
        "zero_denominator_replications": zero_denominator_replications,
        "rate": estimate,
        "cluster_jackknife_mcse": mcse,
        "cluster_count": len(values),
    }


def _summarize_cells(rows: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["family_id"]), str(row["policy_id"]))].append(row)
    output: list[dict[str, object]] = []
    for (family_id, policy_id), values in sorted(grouped.items()):
        for value in values:
            _validate_metric_row(value)
        entry: dict[str, object] = {
            "family_id": family_id,
            "policy_id": policy_id,
            "replications": len(values),
            "factors": {
                key: values[0][key]
                for key in ("load", "missing_evidence", "access_barrier", "retrievability", "staff_access")
            },
        }
        for metric in CELL_RATE_METRICS:
            samples = [float(item[metric]) for item in values]
            entry[metric] = mean(samples)
            entry[f"{metric}_mcse"] = stdev(samples) / sqrt(len(samples)) if len(samples) > 1 else 0.0
        entry["conditional_timely_review"] = _cluster_jackknife_ratio(
            values, "timely_review_count", "review_request_count"
        )
        entry["conditional_gate_safety"] = _cluster_jackknife_ratio(
            values, "gate_safe_count", "gate_applicable_count"
        )
        output.append(entry)
    return output


def _paired_estimates(rows: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    keyed = {
        (str(row["family_id"]), int(row["replication"]), str(row["policy_id"])): row
        for row in rows
    }
    contrasts = ((
        "U3-minus-U0",
        "U3",
        "U0",
        ("unresolved_nonprogression_rate",),
    ),)
    families = sorted({key[0] for key in keyed})
    replications = sorted({key[1] for key in keyed})
    output: list[dict[str, object]] = []
    for family_id in families:
        for contrast_id, left, right, metrics in contrasts:
            for metric in metrics:
                differences = [
                    float(keyed[(family_id, replication, left)][metric])
                    - float(keyed[(family_id, replication, right)][metric])
                    for replication in replications
                ]
                estimate = mean(differences)
                mcse = stdev(differences) / sqrt(len(differences)) if len(differences) > 1 else 0.0
                output.append({
                    "family_id": family_id,
                    "contrast_id": contrast_id,
                    "metric": metric,
                    "estimate": estimate,
                    "mcse": mcse,
                    "ci95_low": estimate - 1.96 * mcse,
                    "ci95_high": estimate + 1.96 * mcse,
                    "replications": len(differences),
                })
    return output


def _process_contrasts(rows: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    """Keep process-event contrasts separate from the sole decision-state contrast."""

    keyed = {
        (str(row["family_id"]), int(row["replication"]), str(row["policy_id"])): row
        for row in rows
    }
    output: list[dict[str, object]] = []
    families = sorted({key[0] for key in keyed})
    replications = sorted({key[1] for key in keyed})
    for family_id in families:
        for metric in ("recipient_burden_rate", "agency_workload_rate"):
            differences = [
                float(keyed[(family_id, replication, "U3")][metric])
                - float(keyed[(family_id, replication, "U0")][metric])
                for replication in replications
            ]
            estimate = mean(differences)
            mcse = stdev(differences) / sqrt(len(differences)) if len(differences) > 1 else 0.0
            output.append({
                "family_id": family_id,
                "contrast_id": "U3-minus-U0-process-events",
                "metric": metric,
                "estimate": estimate,
                "mcse": mcse,
                "ci95_low": estimate - 1.96 * mcse,
                "ci95_high": estimate + 1.96 * mcse,
                "replications": len(differences),
                "claim_boundary": "event counts per initiated case; not effort, welfare, cost, or overall policy value",
            })
    return output


def _common_random_number_diagnostics(rows: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    keyed = {
        (str(row["family_id"]), int(row["replication"]), str(row["policy_id"])): row
        for row in rows
    }
    diagnostics: list[dict[str, object]] = []
    for family_id in sorted({key[0] for key in keyed}):
        replications = sorted({key[1] for key in keyed if key[0] == family_id})
        for metric, left_policy, right_policy in (
            ("timeout_activation_rate", "U2O", "U2C"),
            ("unresolved_nonprogression_rate", "U3", "U0"),
        ):
            left = [float(keyed[(family_id, rep, left_policy)][metric]) for rep in replications]
            right = [float(keyed[(family_id, rep, right_policy)][metric]) for rep in replications]
            differences = [a - b for a, b in zip(left, right, strict=True)]
            paired_variance = stdev(differences) ** 2 if len(differences) > 1 else 0.0
            unpaired_variance = (
                (stdev(left) ** 2 + stdev(right) ** 2) if len(left) > 1 else 0.0
            )
            diagnostics.append({
                "family_id": family_id,
                "metric": metric,
                "paired_variance": paired_variance,
                "unpaired_variance_proxy": unpaired_variance,
                "variance_ratio": paired_variance / unpaired_variance if unpaired_variance else 0.0,
            })
    return diagnostics


def _audit(rows: list[dict[str, object]], cells: list[dict[str, object]]) -> dict[str, object]:
    u2c = [cell for cell in cells if cell["policy_id"] == "U2C"]
    by_load: dict[str, list[dict[str, object]]] = defaultdict(list)
    for cell in u2c:
        by_load[str(cell["factors"]["load"])].append(cell)
    load_review = {
        load: mean(float(cell["timeout_activation_rate"]) for cell in values)
        for load, values in sorted(by_load.items())
    }
    u2o = [row for row in rows if row["policy_id"] == "U2O"]
    u2c_rows = [row for row in rows if row["policy_id"] == "U2C"]
    censoring_reasons: dict[str, int] = defaultdict(int)
    for row in rows:
        for reason, count in row["censoring_reason_counts"].items():
            censoring_reasons[reason] += int(count)
    return {
        "queue_dynamics_change_timeout_activation": len(set(round(value, 8) for value in load_review.values())) > 1,
        "u2c_timeout_activation_by_load": load_review,
        "timeout_semantics_change_progression": (
            mean(float(row["unsupported_progression_rate"]) for row in u2o)
            != mean(float(row["unsupported_progression_rate"]) for row in u2c_rows)
        ),
        "paired_case_membership_preserved": all(
            len({
                row["cohort_hash"]
                for row in rows
                if row["family_id"] == family and row["replication"] == replication
            }) == 1
            for family in {str(row["family_id"]) for row in rows}
            for replication in {int(row["replication"]) for row in rows}
        ),
        "stage_aware_censoring_reason_counts": dict(sorted(censoring_reasons.items())),
        "censoring_interpretation": "ongoing recovery exposure and unresolved post-action paths remain stage-coded supplementary diagnostics; they are not relabeled as decision resolution",
        "claim_limit": "development-only pilot diagnostics; not confirmatory evidence",
    }


def _adapter_swap_rehearsal(family: ScenarioFamily) -> dict[str, object]:
    cohort = generate_stochastic_cohort(StochasticCohortSpec(
        scenario_id="SLICE3-ADAPTER-SWAP",
        seed_id="SLICE3-ADAPTER-SWAP-SEED-001",
        case_ids=tuple(f"SWAP-C{index:03d}" for index in range(1, 9)),
        overlay=family.overlay,
    ))
    original = compile_configuration(
        configuration_id="SLICE3-ADAPTER-SWAP-ORIGINAL",
        process=stochastic_process("SYNTHETIC-STOCHASTIC@1"),
        policy=policy("U2C"),
        overlay=family.overlay.to_compilation_overlay(),
        evaluation_spec_id="PILOT-EVALUATION@1",
        evaluation_specification=period_evidence_evaluation_specification("PILOT-EVALUATION@1"),
    )
    alternate = compile_configuration(
        configuration_id="SLICE3-ADAPTER-SWAP-ALTERNATE",
        process=stochastic_process("TRANSFER-SYNTHETIC-STOCHASTIC@1"),
        policy=policy("U2C"),
        overlay=family.overlay.to_compilation_overlay(),
        evaluation_spec_id="PILOT-EVALUATION@1",
        evaluation_specification=period_evidence_evaluation_specification("PILOT-EVALUATION@1"),
    )
    original_run = run_engagement_stage(cohort, original)
    alternate_run = run_engagement_stage(cohort, alternate)
    return {
        "original_profile_id": original.process_profile.profile_id,
        "alternate_profile_id": alternate.process_profile.profile_id,
        "configuration_artifacts_differ": canonical_hash(original.model_dump(mode="json")) != canonical_hash(alternate.model_dump(mode="json")),
        "compiler_hash_equal": original.compiler_code_hash == alternate.compiler_code_hash,
        "cohort_hash_equal": original_run.cohort_hash == alternate_run.cohort_hash,
        "event_hash_equal": original_run.telemetry.event_hash == alternate_run.telemetry.event_hash,
        "telemetry_equal": original_run.telemetry == alternate_run.telemetry,
        "engine_change_required": False,
        "status": "pass" if original_run == alternate_run else "fail",
    }


def run_experiment(config_path: Path) -> dict[str, object]:
    config = load_experiment_config(config_path)
    validation = validate_experiment_config(config_path)
    if config["mode"] != "development_pilot":
        raise ContractError(
            "FREEZE_REQUIRED",
            "confirmatory execution is available only through a verified freeze manifest",
        )
    factors = development_factor_subset(int(config["development_family_count"]))
    families = materialize_families(
        factors,
        overlay_from_mapping(config["base_overlay"]),
        int(config["cohort_size"]),
    )
    rows: list[dict[str, object]] = []
    started = monotonic()
    for family in families:
        for replication in range(1, int(config["replications"]) + 1):
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
            for policy_id in POLICY_IDS:
                compiled = compile_configuration(
                    configuration_id=f"{family.family_id}-R{replication:03d}-{policy_id}",
                    process=stochastic_process(),
                    policy=policy(policy_id),
                    overlay=family.overlay.to_compilation_overlay(),
                    evaluation_spec_id="PILOT-EVALUATION@1",
                    evaluation_specification=period_evidence_evaluation_specification("PILOT-EVALUATION@1"),
                )
                run = run_engagement_stage(cohort, compiled)
                rows.append(_run_metrics(family, replication, policy_id, run))
    elapsed = monotonic() - started
    cells = _summarize_cells(rows)
    pairs = _paired_estimates(rows)
    process_contrasts = _process_contrasts(rows)
    crn = _common_random_number_diagnostics(rows)
    total_case_policy_runs = sum(int(row["case_count"]) for row in rows)
    throughput = total_case_policy_runs / elapsed if elapsed else 0.0
    runtime_config = config["runtime"]
    confirmatory_runs = (
        108
        * int(runtime_config["confirmatory_replications"])
        * len(POLICY_IDS)
        * int(runtime_config["confirmatory_cohort_size"])
    )
    predicted_seconds = confirmatory_runs / throughput if throughput else float("inf")
    precision = config["precision"]
    applicable_cell_metrics = {
        "U0": ("unresolved_nonprogression_rate",),
        "U1": (),
        "U2C": ("timeout_activation_rate",),
        "U2O": (),
        "U3": ("unresolved_nonprogression_rate",),
    }
    max_rate_mcse = max(
        float(cell[f"{metric}_mcse"])
        for cell in cells
        for metric in applicable_cell_metrics[str(cell["policy_id"])]
    )
    max_paired_mcse = max(float(item["mcse"]) for item in pairs)
    minimum_replications = int(precision["minimum_replications"])
    projection_multiplier = sqrt(int(config["replications"]) / minimum_replications)
    projected_rate_mcse = max_rate_mcse * projection_multiplier
    projected_paired_mcse = max_paired_mcse * projection_multiplier
    dummy_receipt = dummy_analysis_receipt()
    result = {
        "schema_version": 1,
        "artifact_kind": "development_pilot_receipt",
        "claim_limit": "development-only design calibration; not confirmatory evidence",
        "validation": validation,
        "families": [family.canonical_value() for family in families],
        "runtime": {
            "elapsed_seconds": elapsed,
            "case_policy_runs": total_case_policy_runs,
            "case_policy_runs_per_second": throughput,
            "predicted_confirmatory_seconds": predicted_seconds,
            "predicted_confirmatory_ceiling_seconds": runtime_config["confirmatory_ceiling_seconds"],
            "within_ceiling": predicted_seconds <= float(runtime_config["confirmatory_ceiling_seconds"]),
        },
        "precision": {
            "maximum_observed_rate_mcse": max_rate_mcse,
            "maximum_observed_paired_mcse": max_paired_mcse,
            "projected_rate_mcse_at_minimum_replications": projected_rate_mcse,
            "projected_paired_mcse_at_minimum_replications": projected_paired_mcse,
            "projection_rule": "pilot MCSE multiplied by sqrt(pilot_replications/minimum_replications)",
            "target_rate_mcse": precision["target_rate_mcse"],
            "target_paired_mcse": precision["target_paired_mcse"],
            "pilot_rate_target_met": max_rate_mcse <= float(precision["target_rate_mcse"]),
            "pilot_paired_target_met": max_paired_mcse <= float(precision["target_paired_mcse"]),
            "projected_rate_target_met_at_minimum_replications": projected_rate_mcse <= float(precision["target_rate_mcse"]),
            "projected_paired_target_met_at_minimum_replications": projected_paired_mcse <= float(precision["target_paired_mcse"]),
            "extension_rule": precision["extension_rule"],
        },
        "audit": _audit(rows, cells),
        "adapter_swap_rehearsal": _adapter_swap_rehearsal(families[0]),
        "cell_summaries": cells,
        "paired_estimates": pairs,
        "process_contrasts": process_contrasts,
        "common_random_number_diagnostics": crn,
        "dummy_analysis_receipt": dummy_receipt,
        "row_hash": canonical_hash(rows),
    }
    result["receipt_hash"] = canonical_hash(result)
    outputs = config["outputs"]
    detailed_path = Path(str(outputs["development_output_path"]))
    if not detailed_path.is_absolute():
        detailed_path = config_path.resolve().parents[2] / detailed_path
    detailed_path.parent.mkdir(parents=True, exist_ok=True)
    detailed = {"receipt": result, "replicate_rows": rows}
    detailed_path.write_text(json.dumps(detailed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt_path = Path(str(outputs["stored_receipt_path"]))
    if not receipt_path.is_absolute():
        receipt_path = config_path.resolve().parents[2] / receipt_path
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    dummy_path = receipt_path.parent / "dummy_analysis_receipt_v1.json"
    dummy_path.write_text(json.dumps(dummy_receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_figure_prototypes(result, receipt_path.parent)
    return result


def _svg_document(title: str, subtitle: str, polylines: list[tuple[str, str, list[tuple[float, float]]]]) -> str:
    width, height = 760, 440
    plot_left, plot_top, plot_width, plot_height = 70, 80, 640, 290
    body = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="30" y="34" font-family="sans-serif" font-size="20">{title}</text>',
        f'<text x="30" y="58" font-family="sans-serif" font-size="12" fill="#444">{subtitle}</text>',
        f'<line x1="{plot_left}" y1="{plot_top + plot_height}" x2="{plot_left + plot_width}" y2="{plot_top + plot_height}" stroke="#222"/>',
        f'<line x1="{plot_left}" y1="{plot_top}" x2="{plot_left}" y2="{plot_top + plot_height}" stroke="#222"/>',
    ]
    colors = {"blue": "#276FBF", "red": "#C23B22", "green": "#2E8B57", "gold": "#B7791F"}
    for index, (label, color, points) in enumerate(polylines):
        rendered = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        body.append(f'<polyline points="{rendered}" fill="none" stroke="{colors[color]}" stroke-width="3"/>')
        for x, y in points:
            body.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="{colors[color]}"/>')
        legend_y = 92 + index * 20
        body.append(f'<line x1="530" y1="{legend_y}" x2="550" y2="{legend_y}" stroke="{colors[color]}" stroke-width="3"/>')
        body.append(f'<text x="558" y="{legend_y + 4}" font-family="sans-serif" font-size="11">{label}</text>')
    body.extend([
        '<text x="380" y="425" text-anchor="middle" font-family="sans-serif" font-size="11">Prototype only — axes and labels freeze before confirmatory execution</text>',
        '</svg>',
    ])
    return "\n".join(body) + "\n"


def _write_figure_prototypes(receipt: Mapping[str, object], directory: Path) -> None:
    cells = list(receipt["cell_summaries"])
    loads = ["0.6", "0.95", "1.2"]
    plot_left, plot_top, plot_width, plot_height = 70.0, 80.0, 640.0, 290.0

    def y(rate: float) -> float:
        return plot_top + plot_height * (1.0 - max(0.0, min(1.0, rate)))

    def x(index: int) -> float:
        return plot_left + (plot_width * index / (len(loads) - 1))

    capacity_lines: list[tuple[str, str, list[tuple[float, float]]]] = []
    for policy_id, metric, label, color in (
        ("U2C", "timeout_activation_rate", "U2C timeout activation", "blue"),
        ("U2O", "unsupported_progression_rate", "U2O unsupported progression", "red"),
    ):
        points = []
        for index, load in enumerate(loads):
            values = [
                float(cell[metric]) for cell in cells
                if cell["policy_id"] == policy_id and cell["factors"]["load"] == load
            ]
            points.append((x(index), y(mean(values) if values else 0.0)))
        capacity_lines.append((label, color, points))
    (directory / "figure_capacity_timeout_prototype_v1.svg").write_text(
        _svg_document(
            "Capacity and timeout semantics",
            "Development-only pilot means across the coverage subset; confirmatory data not used",
            capacity_lines,
        ),
        encoding="utf-8",
    )

    pairs = [item for item in receipt["paired_estimates"] if item["contrast_id"] == "U3-minus-U0"]
    unresolved = {
        item["family_id"]: float(item["estimate"])
        for item in pairs
        if item["metric"] == "unresolved_nonprogression_rate"
    }
    families = sorted(unresolved)
    points = [
        (
            plot_left + plot_width * index / max(1, len(families) - 1),
            y(unresolved[family]),
        )
        for index, family in enumerate(families)
    ]
    (directory / "figure_information_tradeoff_prototype_v1.svg").write_text(
        _svg_document(
            "Information-first unresolved non-progression",
            "U3-minus-U0 paired development estimates; family order is provisional",
            [("scenario families", "green", points)],
        ),
        encoding="utf-8",
    )


def dummy_analysis_receipt() -> dict[str, object]:
    """Rehearse the aggregate analysis contract without reading study output."""

    rows: list[dict[str, object]] = []
    for replication in range(1, 5):
        for policy_index, policy_id in enumerate(POLICY_IDS):
            base = Decimal(replication + policy_index) / Decimal(20)
            review_requests = 5 if policy_id == "U3" else (4 if policy_id in {"U2C", "U2O"} else 0)
            timely_reviews = min(replication, review_requests)
            unresolved = 5 if policy_id == "U3" else 4
            unsupported = 0 if policy_id == "U3" else 1
            supported = 10 - unresolved - unsupported
            rows.append({
                "family_id": "DUMMY-FAMILY",
                "load": "0.95",
                "missing_evidence": "0.30",
                "access_barrier": "0.30",
                "retrievability": "high",
                "staff_access": "complete",
                "replication": replication,
                "policy_id": policy_id,
                "case_count": 10,
                "event_count": 100,
                "cohort_hash": f"DUMMY-{replication}",
                "event_hash": f"DUMMY-{policy_id}-{replication}",
                "review_request_count": review_requests,
                "review_request_rate": review_requests / 10,
                "timely_review_count": timely_reviews,
                "timeout_activation_count": review_requests - timely_reviews,
                "gate_applicable_count": review_requests,
                "gate_safe_count": timely_reviews,
                "supported_progression_count": supported,
                "unsupported_progression_count": unsupported,
                "evidence_only_failure_count": 0,
                "authorization_only_failure_count": 0,
                "joint_evidence_authorization_failure_count": unsupported,
                "evidentially_unsupported_progression_count": unsupported,
                "unauthorized_progression_count": unsupported,
                "adequate_response_evidence_count": supported,
                "retrieval_request_count": unresolved + unsupported,
                "retrieved_evidence_count": unsupported,
                "unresolved_after_acquisition_count": unresolved,
                "evidence_requested_count": unresolved - 3,
                "held_count": 1,
                "pre_action_open_count": 2,
                "unresolved_nonprogression_count": unresolved,
                "supported_recovery_entry_count": 3,
                "unsupported_recovery_entry_count": unsupported,
                "no_recovery_entry_count": 7 - unsupported,
                "timeout_activation_rate": (review_requests - timely_reviews) / 10,
                "conditional_timely_review_rate": (
                    timely_reviews / review_requests if review_requests else None
                ),
                "conditional_gate_safety_rate": (
                    timely_reviews / review_requests if review_requests else None
                ),
                "supported_progression_rate": supported / 10,
                "unsupported_progression_rate": unsupported / 10,
                "evidence_only_failure_rate": 0.0,
                "authorization_only_failure_rate": 0.0,
                "joint_evidence_authorization_failure_rate": unsupported / 10,
                "evidentially_unsupported_progression_rate": unsupported / 10,
                "unauthorized_progression_rate": unsupported / 10,
                "adequate_response_evidence_rate": supported / 10,
                "retrieval_request_rate": (unresolved + unsupported) / 10,
                "retrieved_evidence_rate": unsupported / 10,
                "unresolved_after_acquisition_rate": unresolved / 10,
                "evidence_requested_rate": (unresolved - 3) / 10,
                "held_rate": 0.1,
                "pre_action_open_rate": 0.2,
                "unresolved_nonprogression_rate": unresolved / 10,
                "supported_recovery_entry_rate": 0.3,
                "unsupported_recovery_entry_rate": unsupported / 10,
                "no_recovery_entry_rate": (7 - unsupported) / 10,
                "recipient_burden_rate": float(base),
                "agency_workload_rate": float(base),
                "censoring_reason_counts": {},
                "review_mean_wait_time": float(replication),
                "correction_mean_exposure_time": float(policy_index),
            })
    cells = _summarize_cells(rows)
    pairs = _paired_estimates(rows)
    receipt = {
        "schema_version": 1,
        "artifact_kind": "dummy_analysis_receipt",
        "source": "synthetic dummy rows generated independently of pilot and confirmatory output",
        "cell_count": len(cells),
        "paired_estimate_count": len(pairs),
        "primary_metrics": PRIMARY_METRICS,
        "cell_hash": canonical_hash(cells),
        "paired_hash": canonical_hash(pairs),
    }
    return receipt | {"receipt_hash": canonical_hash(receipt)}
