#!/usr/bin/env python3
"""Build the Table 3 data receipt from a stored pilot or frozen analysis artifact."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import sqrt
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "outputs/confirmatory_v4/analysis/analysis_r030.json"
DEFAULT_OUTPUT = ROOT / "docs/tables/table3_simulation_results.json"


def _canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def _verify_receipt(receipt: dict[str, object]) -> None:
    field = "analysis_hash" if "analysis_hash" in receipt else "receipt_hash"
    candidate = dict(receipt)
    observed = candidate.pop(field, None)
    if observed != _canonical_hash(candidate):
        raise RuntimeError(f"source artifact {field} does not verify")


def _family_summary(items: list[dict[str, object]]) -> dict[str, float | int]:
    estimates = [float(item["estimate"]) for item in items]
    return {
        "family_count": len(items),
        "estimate": mean(estimates),
        "family_minimum": min(estimates),
        "family_maximum": max(estimates),
        "simulation_mcse": sqrt(sum(float(item["mcse"]) ** 2 for item in items)) / len(items),
    }


def _cell_metric_summary(
    cells: list[dict[str, object]],
    *,
    policy_id: str,
    metric: str,
) -> dict[str, float | int]:
    selected = [cell for cell in cells if cell["policy_id"] == policy_id]
    estimates = [float(cell[metric]) for cell in selected]
    return {
        "family_count": len(selected),
        "estimate": mean(estimates),
        "family_minimum": min(estimates),
        "family_maximum": max(estimates),
        "simulation_mcse": sqrt(sum(
            float(cell[f"{metric}_mcse"]) ** 2 for cell in selected
        )) / len(selected),
    }


def build_table(receipt: dict[str, object], *, development: bool = False) -> dict[str, object]:
    _verify_receipt(receipt)
    cells = [dict(cell) for cell in receipt["cell_summaries"]]
    pairs = [dict(item) for item in receipt["paired_estimates"]]
    process = [dict(item) for item in receipt.get("process_contrasts", [])]
    u2c = [cell for cell in cells if cell["policy_id"] == "U2C"]
    timeout = {
        "family_count": len(u2c),
        "estimate": mean(float(cell["timeout_activation_rate"]) for cell in u2c),
        "family_minimum": min(float(cell["timeout_activation_rate"]) for cell in u2c),
        "family_maximum": max(float(cell["timeout_activation_rate"]) for cell in u2c),
        "simulation_mcse": sqrt(sum(
            float(cell["timeout_activation_rate_mcse"]) ** 2 for cell in u2c
        )) / len(u2c),
    }
    failure_components = {
        metric: _cell_metric_summary(cells, policy_id="U2O", metric=metric)
        for metric in (
            "evidence_only_failure_rate",
            "authorization_only_failure_rate",
            "joint_evidence_authorization_failure_rate",
        )
    }
    if abs(
        sum(float(item["estimate"]) for item in failure_components.values())
        - float(timeout["estimate"])
    ) > 1e-12:
        raise RuntimeError("fail-open failure components do not conserve timeout activation")
    timely = sum(int(cell["conditional_timely_review"]["numerator_count"]) for cell in u2c)
    requests = sum(int(cell["conditional_timely_review"]["denominator_count"]) for cell in u2c)
    zero_request_replications = sum(
        int(cell["conditional_timely_review"]["zero_denominator_replications"])
        for cell in u2c
    )
    unresolved = [
        item for item in pairs
        if item["contrast_id"] == "U3-minus-U0"
        and item["metric"] == "unresolved_nonprogression_rate"
    ]
    burden = [item for item in process if item["metric"] == "recipient_burden_rate"]
    workload = [item for item in process if item["metric"] == "agency_workload_rate"]
    rows = [
        {
            "quantity_id": "U2C_TIMEOUT_ACTIVATION",
            "label": "Fail-closed timeout activation per initiated case",
            **timeout,
            "claim_boundary": "queue deadline misses in the designed grid; fail-open progression and fail-closed holding are rule-defined consequences, not separate findings",
        },
    ]
    if not development:
        rows.extend((
        {
            "quantity_id": "U2O_EVIDENCE_ONLY_FAILURE",
            "label": "Fail-open evidence-only progression failure",
            **failure_components["evidence_only_failure_rate"],
            "claim_boundary": "exclusive component of the timeout-activated progression union; not a separate policy effect",
        },
        {
            "quantity_id": "U2O_AUTHORIZATION_ONLY_FAILURE",
            "label": "Fail-open authorization-only progression failure",
            **failure_components["authorization_only_failure_rate"],
            "claim_boundary": "sufficient evidence with required timely review authorization missing; exclusive union component",
        },
        {
            "quantity_id": "U2O_JOINT_EVIDENCE_AUTHORIZATION_FAILURE",
            "label": "Fail-open joint evidence-and-authorization failure",
            **failure_components["joint_evidence_authorization_failure_rate"],
            "claim_boundary": "evidence and required timely review authorization both missing; exclusive union component",
        },
        ))
    rows.extend((
        {
            "quantity_id": "U3_MINUS_U0_UNRESOLVED_NONPROGRESSION",
            "label": "Information-first change in unresolved non-progression",
            **_family_summary(unresolved),
            "claim_boundary": "sole aggregate U3-minus-U0 decision-state contrast",
        },
        {
            "quantity_id": "U2C_CONDITIONAL_TIMELY_REVIEW",
            "label": "Timely review conditional on a review request",
            "numerator_count": timely,
            "denominator_count": requests,
            "zero_request_replications": zero_request_replications,
            "estimate": timely / requests if requests else None,
            "simulation_mcse": None,
            "claim_boundary": "request-weighted diagnostic; null when no request exists and not a supported-disposition measure",
        },
        {
            "quantity_id": "U3_MINUS_U0_INTERACTION_EVENTS",
            "label": "Additional modeled interaction events per initiated case",
            **_family_summary(burden),
            "claim_boundary": "event count, not effort, subjective burden, welfare, or cost",
        },
        {
            "quantity_id": "U3_MINUS_U0_WORKLOAD_EVENTS",
            "label": "Additional modeled agency-work events per initiated case",
            **_family_summary(workload),
            "claim_boundary": "event count, not staffing cost, efficiency, or overall policy value",
        },
    ))
    quantity_ids = [str(row["quantity_id"]) for row in rows]
    if len(quantity_ids) != len(set(quantity_ids)):
        raise RuntimeError("Table 3 contains duplicate quantity identities")
    if len(unresolved) != len({str(item["family_id"]) for item in unresolved}):
        raise RuntimeError("Table 3 repeats the U3 decision contrast")
    value = {
        "schema_version": 2,
        "artifact_kind": "simulation_table3_data",
        "status": "development_only_rehearsal" if development else "frozen_result",
        "source_hash": receipt.get("analysis_hash", receipt.get("receipt_hash")),
        "row_count": len(rows),
        "rows": rows,
        "accounting_identity_policy": "one reported quantity per decision-state accounting identity",
    }
    return value | {"table_hash": _canonical_hash(value)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--development", action="store_true")
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    result = build_table(receipt, development=args.development)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output.relative_to(ROOT) if args.output.is_relative_to(ROOT) else args.output)


if __name__ == "__main__":
    main()
