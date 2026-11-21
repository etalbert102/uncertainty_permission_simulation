#!/usr/bin/env python3
"""Build Figure 3 from a stored pilot or frozen analysis artifact."""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from html import escape
import json
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "outputs/confirmatory_v3/analysis/analysis_r030.json"
DEFAULT_OUTPUT = ROOT / "docs/figures/figure3_simulation_results.svg"
COLORS = {
    "blue": "#2563A6",
    "orange": "#C56A11",
    "red": "#B3382C",
    "green": "#2E7D5B",
    "purple": "#7252A3",
    "gray": "#59636E",
    "grid": "#D8DEE6",
    "ink": "#17212B",
    "panel": "#F8FAFC",
}
FONT = "Arial, Helvetica, sans-serif"


def _canonical_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def _verify_receipt(receipt: dict[str, object]) -> None:
    field = "analysis_hash" if "analysis_hash" in receipt else "receipt_hash"
    observed = receipt.get(field)
    candidate = dict(receipt)
    candidate.pop(field, None)
    if observed != _canonical_hash(candidate):
        raise RuntimeError(f"source artifact {field} does not verify")
    if receipt.get("artifact_kind") not in {
        "confirmatory_analysis", "development_pilot_receipt"
    }:
        raise RuntimeError("unsupported Figure 3 source artifact")


def build_payload(receipt: dict[str, object]) -> dict[str, object]:
    _verify_receipt(receipt)
    cells = [dict(cell) for cell in receipt["cell_summaries"]]
    family_count = len({str(cell["family_id"]) for cell in cells})

    load_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for cell in cells:
        if cell["policy_id"] == "U2C":
            load_groups[str(cell["factors"]["load"])].append(cell)
    panel_a = []
    for load, values in sorted(load_groups.items(), key=lambda item: float(item[0])):
        timely = sum(int(value["conditional_timely_review"]["numerator_count"]) for value in values)
        requests = sum(int(value["conditional_timely_review"]["denominator_count"]) for value in values)
        panel_a.append({
            "load": load,
            "cell_count": len(values),
            "timeout_activation_rate": mean(float(value["timeout_activation_rate"]) for value in values),
            "conditional_timely_review_rate": timely / requests if requests else None,
            "timely_review_count": timely,
            "review_request_count": requests,
        })

    state_metrics = (
        "supported_progression_rate",
        "unsupported_progression_rate",
        "evidence_requested_rate",
        "held_rate",
        "pre_action_open_rate",
    )
    panel_b = []
    for policy_id in ("U0", "U3"):
        values = [cell for cell in cells if cell["policy_id"] == policy_id]
        states = {
            metric: mean(float(value[metric]) for value in values)
            for metric in state_metrics
        }
        if abs(sum(states.values()) - 1.0) > 1e-12:
            raise RuntimeError(f"decision-state decomposition does not conserve {policy_id}")
        panel_b.append({"policy_id": policy_id, "cell_count": len(values), "states": states})

    panel_c = []
    u3 = [cell for cell in cells if cell["policy_id"] == "U3"]
    for factor in ("access_barrier", "retrievability", "staff_access"):
        groups: dict[str, list[dict[str, object]]] = defaultdict(list)
        for cell in u3:
            groups[str(cell["factors"][factor])].append(cell)
        for level, values in sorted(groups.items()):
            panel_c.append({
                "factor": factor,
                "level": level,
                "cell_count": len(values),
                "unresolved_nonprogression_rate": mean(
                    float(value["unresolved_nonprogression_rate"]) for value in values
                ),
            })
    return {
        "schema_version": 1,
        "family_count": family_count,
        "source_hash": receipt.get("analysis_hash", receipt.get("receipt_hash")),
        "panel_a": panel_a,
        "panel_b": panel_b,
        "panel_c": panel_c,
    }


def _text(x: float, y: float, value: str, *, size: int = 16, weight: int = 400,
          anchor: str = "start", fill: str | None = None) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill or COLORS["ink"]}">'
        f"{escape(value)}</text>"
    )


def _line(x1: float, y1: float, x2: float, y2: float, *, color: str, width: float = 1) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width:.1f}"/>'
    )


def _panel(parts: list[str], y: float, title: str, subtitle: str, height: float) -> None:
    parts.append(
        f'<rect x="45" y="{y:.1f}" width="910" height="{height:.1f}" rx="10" '
        f'fill="{COLORS["panel"]}" stroke="{COLORS["grid"]}"/>'
    )
    parts.append(_text(70, y + 36, title, size=22, weight=700))
    parts.append(_text(70, y + 62, subtitle, size=15, fill=COLORS["gray"]))


def _axis(parts: list[str], *, left: float, right: float, top: float, bottom: float) -> None:
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom - tick * (bottom - top)
        parts.append(_line(left, y, right, y, color=COLORS["grid"]))
        parts.append(_text(left - 12, y + 5, f"{tick:.2f}", size=13, anchor="end", fill=COLORS["gray"]))
    parts.append(_line(left, top, left, bottom, color=COLORS["ink"], width=1.5))
    parts.append(_line(left, bottom, right, bottom, color=COLORS["ink"], width=1.5))


def build_svg(receipt: dict[str, object], *, development: bool = False) -> str:
    payload = build_payload(receipt)
    boundary = "Development-only reporting rehearsal" if development else "Frozen core simulation"
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1320" viewBox="0 0 1000 1320" role="img">',
        '<rect width="1000" height="1320" fill="white"/>',
        _text(45, 43, "Figure 3. Timeout activation and unresolved case location", size=27, weight=700),
        _text(45, 72, f"{boundary}; {payload['family_count']} designed families", size=17, fill=COLORS["gray"]),
    ]

    _panel(parts, 95, "A  Review timing by load", "U2C; timeout per initiated case and timely completion per review request", 340)
    left, right, top, bottom = 135.0, 920.0, 205.0, 365.0
    _axis(parts, left=left, right=right, top=top, bottom=bottom)
    loads = list(payload["panel_a"])
    for index, item in enumerate(loads):
        x = left + index * (right - left) / max(1, len(loads) - 1)
        parts.append(_text(x, bottom + 25, str(item["load"]), size=14, anchor="middle"))
    for label, field, color in (
        ("Timeout activation", "timeout_activation_rate", COLORS["orange"]),
        ("Timely review | request", "conditional_timely_review_rate", COLORS["blue"]),
    ):
        points = []
        for index, item in enumerate(loads):
            value = item[field]
            if value is None:
                continue
            x = left + index * (right - left) / max(1, len(loads) - 1)
            y = bottom - float(value) * (bottom - top)
            points.append((x, y))
        parts.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="3"/>')
        for x, y in points:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}"/>')
        legend_y = 175 if field == "timeout_activation_rate" else 195
        parts.append(_text(650, legend_y, label, size=14, fill=color))

    _panel(parts, 460, "B  Decision state at cutoff", "Unweighted designed-family means; each policy bar sums to 1", 330)
    state_order = (
        ("supported_progression_rate", COLORS["green"], "Supported progression"),
        ("unsupported_progression_rate", COLORS["red"], "Unsupported progression"),
        ("evidence_requested_rate", COLORS["purple"], "Evidence requested"),
        ("held_rate", COLORS["orange"], "Held"),
        ("pre_action_open_rate", COLORS["gray"], "Pre-action open"),
    )
    bar_left, bar_width = 190.0, 700.0
    for row_index, item in enumerate(payload["panel_b"]):
        y = 585 + row_index * 80
        parts.append(_text(90, y + 22, str(item["policy_id"]), size=18, weight=700))
        cursor = bar_left
        for metric, color, _ in state_order:
            width = float(item["states"][metric]) * bar_width
            parts.append(f'<rect x="{cursor:.1f}" y="{y:.1f}" width="{width:.1f}" height="32" fill="{color}"/>')
            cursor += width
    for index, (_, color, label) in enumerate(state_order):
        x = 95 + (index % 3) * 290
        y = 735 + (index // 3) * 24
        parts.append(f'<rect x="{x:.1f}" y="{y-12:.1f}" width="14" height="14" fill="{color}"/>')
        parts.append(_text(x + 21, y, label, size=13))

    _panel(parts, 815, "C  Where U3 unresolved cases accumulate", "Unweighted U3 means across each declared organizational factor", 390)
    c_left, c_right, c_top, c_bottom = 255.0, 920.0, 925.0, 1145.0
    _axis(parts, left=c_left, right=c_right, top=c_top, bottom=c_bottom)
    entries = list(payload["panel_c"])
    for index, item in enumerate(entries):
        x = c_left + index * (c_right - c_left) / max(1, len(entries) - 1)
        value = float(item["unresolved_nonprogression_rate"])
        y = c_bottom - value * (c_bottom - c_top)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{COLORS["purple"]}"/>')
        parts.append(_text(x, c_bottom + 24, str(item["level"]), size=12, anchor="middle"))
        parts.append(_text(x, c_bottom + 42, str(item["factor"]).replace("_", " "), size=10, anchor="middle", fill=COLORS["gray"]))

    parts.extend([
        _text(45, 1240, "Rates describe the declared model and designed grid, not historical Robodebt frequencies.", size=15, weight=700),
        _text(45, 1267, "Conditional review excludes cells with no review requests; decision states and recovery paths remain distinct.", size=15, fill=COLORS["gray"]),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, default=DEFAULT_RECEIPT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--development", action="store_true")
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    svg = build_svg(receipt, development=args.development)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    print(args.output.relative_to(ROOT) if args.output.is_relative_to(ROOT) else args.output)


if __name__ == "__main__":
    main()
