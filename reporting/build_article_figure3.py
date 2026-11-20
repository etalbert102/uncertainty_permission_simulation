#!/usr/bin/env python3
"""Build article Figure 3 from the frozen core analysis receipt.

This is a post-freeze reporting utility, not part of the frozen simulation or
verification-code inventory.
"""

from __future__ import annotations

from collections import defaultdict
from html import escape
import json
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "outputs/confirmatory_v1/analysis/analysis_r030.json"
OUTPUT = ROOT / "docs/figures/figure3_simulation_results.svg"
EXPECTED_ANALYSIS_HASH = "4d549f5e1fed84f294052749d9987d807e9fe2199843b44d7eb7aece867b36bd"

WIDTH = 1000
HEIGHT = 1390
FONT = "Arial, Helvetica, sans-serif"

COLORS = {
    "blue": "#2563A6",
    "orange": "#C56A11",
    "red": "#B3382C",
    "green": "#2E7D5B",
    "purple": "#7252A3",
    "gray": "#59636E",
    "grid": "#D8DEE6",
    "ink": "#17212B",
    "muted": "#52606D",
    "panel": "#F8FAFC",
}


def text(x: float, y: float, value: str, *, size: int = 16, weight: int = 400,
         anchor: str = "start", fill: str | None = None) -> str:
    color = fill or COLORS["ink"]
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{color}">'
        f"{escape(value)}</text>"
    )


def line(x1: float, y1: float, x2: float, y2: float, *, stroke: str,
         width: float = 1.0, dash: str | None = None) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width:.1f}"{dashed}/>'
    )


def circle(x: float, y: float, color: str, radius: float = 6.0) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{color}"/>'


def square(x: float, y: float, color: str, side: float = 12.0) -> str:
    half = side / 2
    return (
        f'<rect x="{x-half:.1f}" y="{y-half:.1f}" width="{side:.1f}" height="{side:.1f}" '
        f'fill="{color}"/>'
    )


def triangle(x: float, y: float, color: str, radius: float = 7.0) -> str:
    points = f"{x:.1f},{y-radius:.1f} {x-radius:.1f},{y+radius:.1f} {x+radius:.1f},{y+radius:.1f}"
    return f'<polygon points="{points}" fill="{color}"/>'


def load_summaries(cells: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    metrics = ("gate_safe_rate", "review_effective_rate", "unresolved_hold_rate")
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for cell in cells:
        if cell["policy_id"] != "U2C":
            continue
        load = str(cell["factors"]["load"])
        for metric in metrics:
            grouped[load][metric].append(float(cell[metric]))
    return {
        load: {metric: mean(values) for metric, values in metric_values.items()}
        for load, metric_values in grouped.items()
    }


def paired_summary(pairs: list[dict[str, object]], contrast: str, metric: str) -> tuple[float, float, float]:
    values = [
        float(item["estimate"])
        for item in pairs
        if item["contrast_id"] == contrast and item["metric"] == metric
    ]
    if len(values) != 108:
        raise RuntimeError(f"expected 108 paired estimates for {contrast}/{metric}, found {len(values)}")
    return mean(values), min(values), max(values)


def panel_frame(
    parts: list[str],
    y: float,
    title_value: str,
    subtitle: str,
    *,
    height: float,
) -> None:
    parts.append(
        f'<rect x="45" y="{y:.1f}" width="910" height="{height:.1f}" rx="10" '
        f'fill="{COLORS["panel"]}" stroke="{COLORS["grid"]}"/>'
    )
    parts.append(text(70, y + 38, title_value, size=23, weight=700))
    parts.append(text(70, y + 68, subtitle, size=17, fill=COLORS["muted"]))


def build_svg(receipt: dict[str, object]) -> str:
    cells = list(receipt["cell_summaries"])
    pairs = list(receipt["paired_estimates"])
    loads = load_summaries(cells)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Figure 3. Capacity, timeout, and information-first results</title>',
        '<desc id="desc">Three panels show the U2C load response, U2O minus U2C paired differences, and U3 minus U0 paired differences over 108 designed scenario families.</desc>',
        f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
        text(45, 45, "Figure 3. Capacity, timeout, and information-first tradeoffs", size=28, weight=700),
        text(45, 76, "Frozen core simulation; 108 designed families, 30 paired replications per family", size=18, fill=COLORS["muted"]),
    ]

    # Panel A: load-stratified U2C summaries.
    panel_frame(
        parts,
        100,
        "A  Fail-closed load response",
        "U2C; unweighted means over other designed factors",
        height=380,
    )
    left, right, top, bottom = 130.0, 930.0, 245.0, 400.0
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom - tick * (bottom - top)
        parts.append(line(left, y, right, y, stroke=COLORS["grid"]))
        parts.append(text(left - 15, y + 6, f"{tick:.2f}", size=16, anchor="end", fill=COLORS["muted"]))
    parts.append(line(left, top, left, bottom, stroke=COLORS["ink"], width=1.5))
    parts.append(line(left, bottom, right, bottom, stroke=COLORS["ink"], width=1.5))
    load_order = ("0.6", "0.95", "1.2")
    x_positions = (left, (left + right) / 2, right)
    for load, x in zip(load_order, x_positions):
        parts.append(text(x, bottom + 27, load, size=16, anchor="middle"))
    parts.append(text((left + right) / 2, bottom + 57, "Nominal initiation load", size=17, anchor="middle"))
    parts.append(
        f'<text x="67" y="{(top + bottom) / 2:.1f}" font-family="{FONT}" font-size="17" '
        f'text-anchor="middle" fill="{COLORS["ink"]}" transform="rotate(-90 67 {(top + bottom) / 2:.1f})">Rate</text>'
    )

    series = (
        ("Gate safety", "gate_safe_rate", COLORS["green"], circle),
        ("Timely review completion", "review_effective_rate", COLORS["blue"], square),
        ("Unresolved hold", "unresolved_hold_rate", COLORS["orange"], triangle),
    )
    for index, (label, metric, color, marker) in enumerate(series):
        points: list[tuple[float, float]] = []
        for load, x in zip(load_order, x_positions):
            value = loads[load][metric]
            y = bottom - value * (bottom - top)
            points.append((x, y))
        rendered = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        parts.append(f'<polyline points="{rendered}" fill="none" stroke="{color}" stroke-width="3"/>')
        for x, y in points:
            parts.append(marker(x, y, color))
        legend_x = (110, 390, 725)[index]
        legend_y = 210
        parts.append(line(legend_x, legend_y, legend_x + 30, legend_y, stroke=color, width=3))
        parts.append(
            marker(legend_x + 15, legend_y, color, 6)
            if marker is circle
            else marker(legend_x + 15, legend_y, color, 12)
        )
        parts.append(text(legend_x + 42, legend_y + 6, label, size=16))

    # Panel B: U2O-U2C paired differences.
    panel_frame(
        parts,
        505,
        "B  Timeout semantics",
        "U2O − U2C; point = unweighted mean, line = family min–max range",
        height=330,
    )
    b_left, b_right = 430.0, 930.0
    b_top, b_bottom = 600.0, 755.0
    for tick in (-1.0, -0.5, 0.0, 0.5, 1.0):
        x = b_left + (tick + 1) / 2 * (b_right - b_left)
        parts.append(line(x, b_top, x, b_bottom, stroke=COLORS["ink"] if tick == 0 else COLORS["grid"], width=1.5 if tick == 0 else 1))
        parts.append(text(x, b_bottom + 27, f"{tick:+.1f}", size=16, anchor="middle"))
    parts.append(text((b_left + b_right) / 2, b_bottom + 55, "Paired rate difference", size=17, anchor="middle"))
    b_rows = (
        ("Unsupported progression", "unsupported_progression_rate", COLORS["red"]),
        ("Exposure", "recovery_exposure_rate", COLORS["orange"]),
        ("Gate safety", "gate_safe_rate", COLORS["green"]),
        ("Unresolved hold", "unresolved_hold_rate", COLORS["blue"]),
        ("Timely review completion", "review_effective_rate", COLORS["purple"]),
    )
    for index, (label, metric, color) in enumerate(b_rows):
        y = 615 + index * 30
        avg, minimum, maximum = paired_summary(pairs, "U2O-minus-U2C", metric)
        scale = lambda value: b_left + (value + 1) / 2 * (b_right - b_left)
        parts.append(text(70, y + 6, label, size=16))
        parts.append(line(scale(minimum), y, scale(maximum), y, stroke=color, width=4))
        parts.append(line(scale(minimum), y - 8, scale(minimum), y + 8, stroke=color, width=2))
        parts.append(line(scale(maximum), y - 8, scale(maximum), y + 8, stroke=color, width=2))
        parts.append(circle(scale(avg), y, color, 7.5))

    # Panel C: U3-U0 paired differences. Metrics carry their own units.
    panel_frame(
        parts,
        860,
        "C  Information-first tradeoff",
        "U3 − U0; outcome rows have different units",
        height=330,
    )
    c_left, c_right = 430.0, 930.0
    c_top, c_bottom = 950.0, 1110.0
    for tick in (0.0, 0.6, 1.2, 1.8):
        x = c_left + tick / 1.8 * (c_right - c_left)
        parts.append(line(x, c_top, x, c_bottom, stroke=COLORS["ink"] if tick == 0 else COLORS["grid"], width=1.5 if tick == 0 else 1))
        parts.append(text(x, c_bottom + 27, f"{tick:.1f}", size=16, anchor="middle"))
    parts.append(text((c_left + c_right) / 2, c_bottom + 57, "Paired difference per initiated case", size=17, anchor="middle"))
    c_rows = (
        ("Unsupported progression", "rate", "unsupported_progression_rate", COLORS["red"]),
        ("Exposure", "rate", "recovery_exposure_rate", COLORS["orange"]),
        ("Interaction events", "events/case", "recipient_burden_rate", COLORS["purple"]),
        ("Agency workload", "events/case", "agency_workload_rate", COLORS["blue"]),
    )
    for index, (label, unit, metric, color) in enumerate(c_rows):
        y = 970 + index * 40
        avg, minimum, maximum = paired_summary(pairs, "U3-minus-U0", metric)
        scale = lambda value: c_left + value / 1.8 * (c_right - c_left)
        parts.append(text(70, y, label, size=16))
        parts.append(text(70, y + 19, unit, size=16, fill=COLORS["muted"]))
        parts.append(line(scale(minimum), y, scale(maximum), y, stroke=color, width=4))
        parts.append(line(scale(minimum), y - 8, scale(minimum), y + 8, stroke=color, width=2))
        parts.append(line(scale(maximum), y - 8, scale(maximum), y + 8, stroke=color, width=2))
        parts.append(circle(scale(avg), y, color, 7.5))

    parts.extend([
        text(45, 1225, "Reading the figure", size=20, weight=700),
        text(45, 1258, "Panel A shows unweighted means over other designed factors; Panels B and C show means and family min–max ranges.", size=16, fill=COLORS["muted"]),
        text(45, 1288, "Family ranges show scenario variation, not uncertainty. Panel C rows use different units and are not a common scale.", size=16, fill=COLORS["muted"]),
        text(45, 1318, "MCSE intervals appear in Table 3. Timely review completion is timing only; exposure is downstream and not proof of harm.", size=16, fill=COLORS["muted"]),
        text(45, 1358, "Scope: frozen stylized parameter space; no historical, legal, population, or complete-restoration estimate.", size=16, weight=700),
        "</svg>",
    ])
    return "\n".join(parts) + "\n"


def main() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if receipt.get("analysis_hash") != EXPECTED_ANALYSIS_HASH:
        raise RuntimeError("core analysis receipt hash differs from the frozen article source")
    svg = build_svg(receipt)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
