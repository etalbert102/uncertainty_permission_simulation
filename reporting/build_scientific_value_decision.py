#!/usr/bin/env python3
"""Apply the recorded Slice 7 scientific-value gate to Freeze 4 analyses."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "outputs/confirmatory_v3/analysis/analysis_r030.json"
SENSITIVITY = ROOT / "outputs/sensitivity_information_latency_v3/analysis/analysis_r030.json"
JSON_OUTPUT = ROOT / "docs/FREEZE4_SCIENTIFIC_VALUE_DECISION.json"
MARKDOWN_OUTPUT = ROOT / "docs/FREEZE4_SCIENTIFIC_VALUE_DECISION.md"
FACTOR_RANGE_THRESHOLD = 0.05
SIMULATION_ERROR_MULTIPLE = 2.0


def canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def load_analysis(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    observed = value.get("analysis_hash")
    candidate = dict(value)
    candidate.pop("analysis_hash", None)
    if observed != canonical_hash(candidate):
        raise RuntimeError(f"analysis self-hash mismatch: {path}")
    return value


def factor_evidence(analysis: dict[str, object]) -> list[dict[str, object]]:
    output = []
    for summary_id, summary in sorted(analysis["designed_grid_summaries"].items()):
        if not summary_id.startswith("u3_unresolved_by_"):
            continue
        levels = summary["levels"]
        error_scale = max(float(level["simulation_mcse"]) for level in levels)
        observed_range = float(summary["range"])
        output.append({
            "summary_id": summary_id,
            "factor": summary["factor"],
            "range": observed_range,
            "range_threshold": FACTOR_RANGE_THRESHOLD,
            "maximum_level_simulation_mcse": error_scale,
            "required_error_multiple": SIMULATION_ERROR_MULTIPLE,
            "error_multiple": observed_range / error_scale if error_scale else None,
            "range_gate_pass": observed_range >= FACTOR_RANGE_THRESHOLD,
            "simulation_error_gate_pass": observed_range > SIMULATION_ERROR_MULTIPLE * error_scale,
            "levels": levels,
        })
    return output


def review_evidence(analysis: dict[str, object]) -> dict[str, object]:
    cells = [cell for cell in analysis["cell_summaries"] if cell["policy_id"] == "U3"]
    requests = sum(int(cell["conditional_timely_review"]["denominator_count"]) for cell in cells)
    timely = sum(int(cell["conditional_timely_review"]["numerator_count"]) for cell in cells)
    zero_replications = sum(
        int(cell["conditional_timely_review"]["zero_denominator_replications"])
        for cell in cells
    )
    positive_families = sum(
        int(cell["conditional_timely_review"]["denominator_count"]) > 0
        for cell in cells
    )
    total_replications = sum(int(cell["conditional_timely_review"]["cluster_count"]) for cell in cells)
    return {
        "review_request_count": requests,
        "timely_review_count": timely,
        "conditional_timely_review_rate": timely / requests if requests else None,
        "zero_request_replications": zero_replications,
        "total_family_replications": total_replications,
        "family_count": len(cells),
        "families_with_positive_total_requests": positive_families,
        "interpretability_rule": "positive total denominator and positive request coverage in every designed family; report zero-request replications",
        "interpretability_gate_pass": requests > 0 and positive_families == len(cells),
    }


def main() -> None:
    core = load_analysis(CORE)
    sensitivity = load_analysis(SENSITIVITY)
    core_factors = factor_evidence(core)
    sensitivity_factors = factor_evidence(sensitivity)
    core_review = review_evidence(core)
    sensitivity_review = review_evidence(sensitivity)
    qualifying = [
        item for item in core_factors
        if item["range_gate_pass"] and item["simulation_error_gate_pass"]
    ]
    gate_pass = bool(qualifying) and bool(core_review["interpretability_gate_pass"])
    value = {
        "schema_version": 1,
        "artifact_kind": "scientific_value_decision",
        "decision": "retain_full_simulation_section" if gate_pass else "demote_to_short_illustration",
        "gate_pass": gate_pass,
        "decision_timing": "recorded after differential audit and before manuscript reconstruction",
        "core_analysis_hash": core["analysis_hash"],
        "sensitivity_analysis_hash": sensitivity["analysis_hash"],
        "factor_range_threshold": FACTOR_RANGE_THRESHOLD,
        "simulation_error_multiple": SIMULATION_ERROR_MULTIPLE,
        "core_factor_evidence": core_factors,
        "core_review_denominator": core_review,
        "qualifying_core_factors": [item["factor"] for item in qualifying],
        "sensitivity_factor_evidence": sensitivity_factors,
        "sensitivity_review_denominator": sensitivity_review,
        "full_disclosure_rule": "retain both complete analyses and report all three declared factor margins regardless of which factor qualifies",
        "post_decision_prohibition": "do not add a parameter, sensitivity, interaction, or outcome after this decision",
        "claim_boundary": "the gate determines article prominence only; it is not evidence of historical prevalence, calibration, causality outside the model, welfare, or overall policy value",
    }
    receipt = value | {"decision_hash": canonical_hash(value)}
    JSON_OUTPUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    factor_rows = "\n".join(
        f"| {item['factor']} | {item['range']:.6f} | {item['maximum_level_simulation_mcse']:.6f} | {item['error_multiple']:.1f} | {'pass' if item['range_gate_pass'] and item['simulation_error_gate_pass'] else 'fail'} |"
        for item in core_factors
    )
    retrievability_core = next(
        item for item in core_factors if item["factor"] == "retrievability"
    )
    markdown = f"""# Freeze 4 Scientific-Value Decision

Decision: **{receipt['decision']}**

The decision was recorded after the Freeze 3/4 differential audit and before manuscript reconstruction. A full simulation section is retained only when at least one prespecified U3 organizational-factor range is at least {FACTOR_RANGE_THRESHOLD:.2f}, exceeds {SIMULATION_ERROR_MULTIPLE:.0f} times its largest level-specific simulation MCSE, and the conditional-review denominator is interpretable and reported.

| U3 factor | Range | Maximum level MCSE | Range/MCSE | Gate |
| --- | ---: | ---: | ---: | --- |
{factor_rows}

Retrievability {'qualifies' if retrievability_core['range_gate_pass'] and retrievability_core['simulation_error_gate_pass'] else 'does not qualify'}. Its core range is {retrievability_core['range']:.6f}; the access-barrier and staff-access margins remain disclosed rather than promoted.

The core U3 conditional-review denominator contains {core_review['review_request_count']:,} requests, {core_review['timely_review_count']:,} timely completions, and {core_review['zero_request_replications']:,} zero-request family-replications out of {core_review['total_family_replications']:,}. Every one of the {core_review['family_count']} designed families has a positive total request denominator. The resulting request-weighted timely-review rate is {core_review['conditional_timely_review_rate']:.6f}.

The latency sensitivity remains in the evidence packet. Its retrievability range is {next(item for item in sensitivity_factors if item['factor'] == 'retrievability')['range']:.6f}; this is supporting robustness information, not a second value-gate search.

This gate controls prominence only. It does not validate the simulation against historical Robodebt or establish welfare, legality, population prevalence, or overall policy value.
"""
    MARKDOWN_OUTPUT.write_text(markdown, encoding="utf-8")
    print(json.dumps({
        "decision": receipt["decision"],
        "decision_hash": receipt["decision_hash"],
        "qualifying_factors": receipt["qualifying_core_factors"],
        "review_requests": core_review["review_request_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
