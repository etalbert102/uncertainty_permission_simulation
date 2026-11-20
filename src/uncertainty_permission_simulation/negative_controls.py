"""Deterministic matched negative controls stored before confirmatory freeze."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping

import yaml

from .policies import ActionDecision, decide_action
from .process_model import TraceResult, TraceSpec, run_trace
from .random_streams import normalized_decimal
from .schemas import ContractError


CONFIRMATORY_NEGATIVE_CONTROL_IDS = (
    "P0-SAME-RULE-SEMANTIC-NULL",
    "P0-ROUTING-INVARIANCE",
    "VERIFIED-MATCH-PROGRESSION",
    "NO-SUPPORT-NO-PROGRESSION",
    "NO-THRESHOLD-NO-PROGRESSION",
)

SENSITIVITY_NEGATIVE_CONTROL_IDS = (
    "P0-SAME-RULE-SEMANTIC-NULL",
    "P0-ROUTING-INVARIANCE",
)

NEGATIVE_CONTROL_RECEIPT_PATH = Path(
    "data/golden_traces/slice4_negative_control_receipt_v2.json"
)


def _canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def _trace_observation(trace: TraceResult) -> dict[str, object]:
    events = [{
        "event_type_id": event.event_type_id,
        "timestamp": normalized_decimal(event.timestamp),
        "causal_event_key": event.causal_event_key,
    } for event in trace.events]
    value = {
        "trace_id": trace.trace_id,
        "route": trace.route,
        "final_action": trace.final_action,
        "functional_permission": trace.functional_permission,
        "gate_state": trace.gate_state,
        "event_types": [event.event_type_id for event in trace.events],
        "event_hash": _canonical_hash(events),
    }
    return value | {"trace_hash": _canonical_hash(value)}


def _decision_observation(
    decision: ActionDecision,
    *,
    arm_id: str,
    progression_threshold_crossed: bool | None,
) -> dict[str, object]:
    value = {
        "arm_id": arm_id,
        "policy_id": decision.policy_id,
        "progression_threshold_crossed": progression_threshold_crossed,
        "action": decision.action,
        "reason_code": decision.reason_code,
        "evidence_sufficient": decision.evidence_sufficient,
        "review_required": decision.review_required,
        "review_authorization_recorded": decision.review_authorization_recorded,
        "functional_permission": decision.functional_permission,
        "progression_supported": decision.progression_supported,
        "evidentially_supported_progression": decision.evidentially_supported_progression,
        "unauthorized_progression": decision.unauthorized_progression,
        "unsupported_reason_codes": list(decision.unsupported_reason_codes),
    }
    return value | {"observation_hash": _canonical_hash(value)}


def _p0_pair_control(
    control_id: str,
    *,
    material_uncertainty: bool,
    force_scrutiny: bool,
) -> dict[str, object]:
    preserve = run_trace(TraceSpec(
        trace_id=f"{control_id}-PRESERVE",
        policy_id="U1",
        representation="preserve",
        material_uncertainty=material_uncertainty,
        review_delay=30,
        force_scrutiny=force_scrutiny,
    ))
    fallback = run_trace(TraceSpec(
        trace_id=f"{control_id}-FALLBACK",
        policy_id="U1",
        representation="fallback",
        material_uncertainty=material_uncertainty,
        review_delay=30,
        force_scrutiny=force_scrutiny,
    ))
    preserve_observation = _trace_observation(preserve)
    fallback_observation = _trace_observation(fallback)
    fallback_adds_progression = (
        fallback.final_action == "progress" and preserve.final_action != "progress"
    )
    fallback_adds_permission = (
        fallback.functional_permission and not preserve.functional_permission
    )
    semantic_projection_equal = preserve.semantic_projection == fallback.semantic_projection
    violation_count = int(fallback_adds_progression or fallback_adds_permission)
    return {
        "control_id": control_id,
        "control_kind": "matched_representation_pair",
        "evaluation_rule": "fallback must not add progression or functional permission relative to the preserving arm",
        "action_support_scope": "omitted_by_claim_limit; this control tests representation-induced permission change",
        "expected": {
            "semantic_projection_equal": True,
            "robust_permission_violation_count": 0,
        },
        "observed": {
            "semantic_projection_equal": semantic_projection_equal,
            "fallback_adds_progression": fallback_adds_progression,
            "fallback_adds_functional_permission": fallback_adds_permission,
            "preserve": preserve_observation,
            "fallback": fallback_observation,
        },
        "robust_permission_violation_count": violation_count,
        "status": "pass" if (
            violation_count == 0
            and semantic_projection_equal
        ) else "fail",
    }


def _verified_match_control() -> dict[str, object]:
    decision = decide_action(
        policy_id="U2C",
        evidence_sufficient=True,
        review_required=True,
        review_completed_by_deadline=True,
        deadline_reached=True,
    )
    observed = _decision_observation(
        decision,
        arm_id="verified_period_specific_evidence",
        progression_threshold_crossed=True,
    )
    violation_count = int(
        decision.action == "progress"
        and (not decision.evidence_sufficient or decision.unauthorized_progression)
    )
    passed = (
        decision.action == "progress"
        and decision.progression_supported
        and violation_count == 0
    )
    return {
        "control_id": "VERIFIED-MATCH-PROGRESSION",
        "control_kind": "supported_progression",
        "evaluation_rule": "verified action-specific evidence plus timely required review may progress without a robust-permission violation",
        "expected": {
            "action": "progress",
            "progression_supported": True,
            "robust_permission_violation_count": 0,
        },
        "observed": observed,
        "robust_permission_violation_count": violation_count,
        "status": "pass" if passed else "fail",
    }


def _no_support_control() -> dict[str, object]:
    observations = [
        _decision_observation(
            decide_action(
                policy_id="U0",
                evidence_sufficient=False,
                review_required=False,
                review_completed_by_deadline=False,
                deadline_reached=True,
            ),
            arm_id=arm_id,
            progression_threshold_crossed=True,
        )
        for arm_id in ("aggregate_only", "missing_period_specific_evidence")
    ]
    violation_count = sum(
        int(item["action"] == "progress")
        for item in observations
    )
    return {
        "control_id": "NO-SUPPORT-NO-PROGRESSION",
        "control_kind": "unsupported_action_withheld",
        "evaluation_rule": "neither evidence state satisfies the action-specific support rule, so neither may progress",
        "expected": {
            "actions": ["hold", "hold"],
            "robust_permission_violation_count": 0,
        },
        "observed": {
            "actions": [item["action"] for item in observations],
            "arms": observations,
        },
        "robust_permission_violation_count": violation_count,
        "status": "pass" if violation_count == 0 else "fail",
    }


def _no_threshold_control() -> dict[str, object]:
    decision = decide_action(
        policy_id="U0",
        evidence_sufficient=False,
        review_required=False,
        review_completed_by_deadline=False,
        deadline_reached=False,
    )
    observed = _decision_observation(
        decision,
        arm_id="progression_antecedent_false",
        progression_threshold_crossed=False,
    )
    violation_count = int(decision.action == "progress")
    return {
        "control_id": "NO-THRESHOLD-NO-PROGRESSION",
        "control_kind": "false_progression_antecedent",
        "evaluation_rule": "before the declared deadline/progression threshold is reached, the pending decision must not progress",
        "expected": {
            "action": "hold",
            "reason_code": "pending",
            "robust_permission_violation_count": 0,
        },
        "observed": observed,
        "robust_permission_violation_count": violation_count,
        "status": "pass" if (
            violation_count == 0 and decision.reason_code == "pending"
        ) else "fail",
    }


def _run_control(control_id: str) -> dict[str, object]:
    if control_id == "P0-SAME-RULE-SEMANTIC-NULL":
        return _p0_pair_control(
            control_id,
            material_uncertainty=False,
            force_scrutiny=False,
        )
    if control_id == "P0-ROUTING-INVARIANCE":
        return _p0_pair_control(
            control_id,
            material_uncertainty=False,
            force_scrutiny=True,
        )
    if control_id == "VERIFIED-MATCH-PROGRESSION":
        return _verified_match_control()
    if control_id == "NO-SUPPORT-NO-PROGRESSION":
        return _no_support_control()
    if control_id == "NO-THRESHOLD-NO-PROGRESSION":
        return _no_threshold_control()
    raise ContractError(
        "NEGATIVE_CONTROL_UNKNOWN",
        f"unknown negative-control ID {control_id}",
    )


def build_negative_control_receipt(config_path: Path) -> dict[str, object]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, Mapping) or config.get("mode") != "confirmatory":
        raise ContractError(
            "NEGATIVE_CONTROL_CONFIG_INVALID",
            "negative-control receipt requires the core confirmatory config",
        )
    control_ids = tuple(config.get("negative_controls", ()))
    if control_ids != CONFIRMATORY_NEGATIVE_CONTROL_IDS:
        raise ContractError(
            "NEGATIVE_CONTROL_CONFIG_INVALID",
            "confirmatory negative-control IDs or order differ from the closed contract",
        )
    controls = [_run_control(control_id) for control_id in control_ids]
    failed = tuple(
        str(control["control_id"])
        for control in controls
        if control["status"] != "pass"
        or int(control["robust_permission_violation_count"]) != 0
    )
    if failed:
        raise ContractError(
            "NEGATIVE_CONTROL_FAILED",
            f"negative controls failed closed: {failed}",
        )
    receipt = {
        "schema_version": 1,
        "artifact_kind": "matched_negative_control_receipt",
        "receipt_id": "SLICE4-NEGATIVE-CONTROLS@2",
        "source_config_id": config["config_id"],
        "source_control_contract_hash": _canonical_hash({
            "config_id": config["config_id"],
            "policy_ids": config["policy_ids"],
            "negative_controls": config["negative_controls"],
        }),
        "execution_mode": "deterministic_pre_freeze_validation",
        "claim_limit": "implementation and falsification controls only; excluded from the 108-family confirmatory design and not evidence of historical prevalence or policy effect",
        "primary_family_count": 0,
        "control_count": len(controls),
        "control_ids": list(control_ids),
        "controls": controls,
        "robust_permission_violation_count": 0,
        "all_controls_pass": True,
    }
    return receipt | {"receipt_hash": _canonical_hash(receipt)}


def write_negative_control_receipt(root: Path, config_path: Path) -> dict[str, object]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, Mapping) or not isinstance(config.get("outputs"), Mapping):
        raise ContractError(
            "NEGATIVE_CONTROL_CONFIG_INVALID",
            "negative-control receipt requires a config outputs mapping",
        )
    configured_path = Path(str(config["outputs"].get("negative_control_receipt_path", "")))
    if configured_path != NEGATIVE_CONTROL_RECEIPT_PATH:
        raise ContractError(
            "NEGATIVE_CONTROL_CONFIG_INVALID",
            f"negative-control receipt path must be {NEGATIVE_CONTROL_RECEIPT_PATH}",
        )
    receipt = build_negative_control_receipt(config_path)
    destination = (root / configured_path).resolve()
    if not destination.is_relative_to(root.resolve()):
        raise ContractError(
            "NEGATIVE_CONTROL_CONFIG_INVALID",
            "negative-control receipt path escapes the repository",
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def verify_stored_negative_control_receipt(root: Path, config_path: Path) -> dict[str, object]:
    expected = build_negative_control_receipt(config_path)
    path = root / NEGATIVE_CONTROL_RECEIPT_PATH
    if not path.is_file():
        raise ContractError(
            "NEGATIVE_CONTROL_RECEIPT_MISSING",
            f"stored negative-control receipt missing at {NEGATIVE_CONTROL_RECEIPT_PATH}",
        )
    try:
        observed = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ContractError(
            "NEGATIVE_CONTROL_RECEIPT_INVALID",
            "stored negative-control receipt is unreadable",
        ) from exc
    stored_hash = observed.get("receipt_hash") if isinstance(observed, dict) else None
    hash_input = dict(observed) if isinstance(observed, dict) else {}
    hash_input.pop("receipt_hash", None)
    if stored_hash != _canonical_hash(hash_input):
        raise ContractError(
            "NEGATIVE_CONTROL_RECEIPT_INVALID",
            "stored negative-control receipt self-hash does not match",
        )
    if observed != expected:
        raise ContractError(
            "NEGATIVE_CONTROL_RECEIPT_DRIFT",
            "stored negative-control receipt differs from deterministic replay",
        )
    return observed
