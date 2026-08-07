#!/usr/bin/env python3
"""Regenerate the publication Figure 13 morphospace as a self-contained SVG."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path

from compute_spd_sri import DEFAULT_DATA, load_and_compute


WIDTH, HEIGHT = 1600, 1100
MARGIN = {"top": 120, "right": 190, "bottom": 230, "left": 170}
DOMAIN_MIN, DOMAIN_MAX = -0.015, 1.015
SPD_RAW_DISPLAY_MIN, SPD_RAW_DISPLAY_MAX = 2.333, 6.750
SRI_RAW_DISPLAY_MAX = 0.222

LABEL_LAYOUT = {
    "Angarano": (16, -14, "start"),
    "Capra": (18, -14, "start"),
    "Cornaro": (18, 24, "start"),
    "Emo": (18, 24, "start"),
    "Foscari": (-18, -18, "end"),
    "Pisani": (18, -14, "start"),
    "Poiana": (-18, -18, "end"),
    "Repeta": (18, -16, "start"),
    "Saraceno": (-18, 28, "end"),
    "Serego": (-18, -16, "end"),
    "Trissino": (18, 28, "start"),
    "Valmarana": (18, 26, "start"),
    "Zeno": (18, 28, "start"),
}

CALLOUTS = {
    "Ragona": (200, 165, 390, 88, [(465, 148), (395, 165)], "SPD 3.400 · SRI 0.222", "Moderate depth, highest relative reticulation"),
    "Thiene": (1000, 245, 360, 88, [(1388, 345), (1360, 310)], "SPD 6.750 · SRI 0.150", "Maximum depth, nine surplus edges"),
    "Barbaro": (1000, 720, 360, 88, [(830, 850), (900, 808), (1000, 790)], "SPD 4.545 · SRI 0.000", "Above-median propagation, no reticulation"),
    "Capra": (220, 735, 360, 88, [(190, 515), (190, 757), (220, 757)], "SPD 2.333 · SRI 0.105", "Minimum propagation depth, near-median reticulation"),
}

CAPTION = (
    "Figure 13. SPD/SRI morphospace of sixteen Palladian villa symmetry graphs. "
    "Normalized Symmetry Propagation Depth and Symmetry Reticulation Index are plotted "
    "on the primary axes, with corresponding raw-value scales shown on the secondary axes. "
    "Dashed lines indicate corpus medians and divide the field into four descriptive regions."
)


def build_svg(rows: list[dict], medians: dict) -> str:
    plot_width = WIDTH - MARGIN["left"] - MARGIN["right"]
    plot_height = HEIGHT - MARGIN["top"] - MARGIN["bottom"]
    plot_right = MARGIN["left"] + plot_width
    plot_bottom = MARGIN["top"] + plot_height

    def fraction(value: float) -> float:
        return (value - DOMAIN_MIN) / (DOMAIN_MAX - DOMAIN_MIN)

    def map_x(value: float) -> float:
        return MARGIN["left"] + fraction(value) * plot_width

    def map_y(value: float) -> float:
        return MARGIN["top"] + (1 - fraction(value)) * plot_height

    median_x = map_x(float(medians["SPD_norm"]))
    median_y = map_y(float(medians["SRI_norm"]))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Figure 13. SPD/SRI morphospace of sixteen Palladian villa symmetry graphs</title>',
        f'<desc id="desc">{escape(CAPTION)}</desc>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>',
        '<g font-family="Arial, Helvetica, sans-serif" fill="#171717">',
        f'<rect x="{MARGIN["left"]}" y="{MARGIN["top"]}" width="{plot_width}" height="{plot_height}" fill="#ffffff" stroke="#171717" stroke-width="1.4"/>',
        f'<line x1="{median_x:.3f}" y1="{MARGIN["top"]}" x2="{median_x:.3f}" y2="{plot_bottom}" stroke="#555555" stroke-width="1.4" stroke-dasharray="9 8"/>',
        f'<line x1="{MARGIN["left"]}" y1="{median_y:.3f}" x2="{plot_right}" y2="{median_y:.3f}" stroke="#555555" stroke-width="1.4" stroke-dasharray="9 8"/>',
        f'<text x="{median_x + 10:.3f}" y="{MARGIN["top"] + 28}" font-size="14" fill="#555555">Corpus median</text>',
        f'<text x="{plot_right - 12}" y="{median_y - 10:.3f}" text-anchor="end" font-size="14" fill="#555555">Corpus median</text>',
        f'<text x="{MARGIN["left"] + 18}" y="{MARGIN["top"] + 182}" font-size="18" font-weight="600" opacity="0.24">Layered compact reticulation</text>',
        f'<text x="{plot_right - 18}" y="{MARGIN["top"] + 48}" text-anchor="end" font-size="18" font-weight="600" opacity="0.24">Distributed reticulated symmetry</text>',
        f'<text x="{MARGIN["left"] + 18}" y="{plot_bottom - 20}" font-size="18" font-weight="600" opacity="0.24">Compact low-reticulation symmetry</text>',
        f'<text x="{plot_right - 18}" y="{plot_bottom - 20}" text-anchor="end" font-size="18" font-weight="600" opacity="0.24">Sequential wing propagation</text>',
    ]

    for tick in (0, 0.25, 0.5, 0.75, 1):
        x, y = map_x(tick), map_y(tick)
        spd_raw = SPD_RAW_DISPLAY_MIN + tick * (SPD_RAW_DISPLAY_MAX - SPD_RAW_DISPLAY_MIN)
        sri_raw = tick * SRI_RAW_DISPLAY_MAX
        parts.extend(
            [
                f'<line x1="{x:.3f}" y1="{plot_bottom}" x2="{x:.3f}" y2="{plot_bottom + 8}" stroke="#171717" stroke-width="1.2"/>',
                f'<text x="{x:.3f}" y="{plot_bottom + 32}" text-anchor="middle" font-size="16">{tick:.2f}</text>',
                f'<line x1="{x:.3f}" y1="{MARGIN["top"]}" x2="{x:.3f}" y2="{MARGIN["top"] - 8}" stroke="#171717" stroke-width="1.2"/>',
                f'<text x="{x:.3f}" y="{MARGIN["top"] - 20}" text-anchor="middle" font-size="15">{spd_raw:.3f}</text>',
                f'<line x1="{MARGIN["left"]}" y1="{y:.3f}" x2="{MARGIN["left"] - 8}" y2="{y:.3f}" stroke="#171717" stroke-width="1.2"/>',
                f'<text x="{MARGIN["left"] - 18}" y="{y + 6:.3f}" text-anchor="end" font-size="16">{tick:.2f}</text>',
                f'<line x1="{plot_right}" y1="{y:.3f}" x2="{plot_right + 8}" y2="{y:.3f}" stroke="#171717" stroke-width="1.2"/>',
                f'<text x="{plot_right + 18}" y="{y + 6:.3f}" font-size="15">{sri_raw:.3f}</text>',
            ]
        )

    parts.extend(
        [
            f'<text x="{MARGIN["left"] + plot_width / 2}" y="42" text-anchor="middle" font-size="20" font-weight="700">SPD raw</text>',
            f'<text x="{MARGIN["left"] + plot_width / 2}" y="{plot_bottom + 82}" text-anchor="middle" font-size="21" font-weight="700">Normalized Symmetry Propagation Depth (SPD)</text>',
            f'<g transform="translate(48 {MARGIN["top"] + plot_height / 2}) rotate(-90)"><text text-anchor="middle" font-size="21" font-weight="700">Normalized Symmetry Reticulation Index (SRI)</text></g>',
            f'<g transform="translate(1552 {MARGIN["top"] + plot_height / 2}) rotate(90)"><text text-anchor="middle" font-size="20" font-weight="700">SRI raw</text></g>',
        ]
    )

    for row in rows:
        if row["villa"] in CALLOUTS:
            continue
        x, y = map_x(float(row["SPD_norm_exact"])), map_y(float(row["SRI_norm_exact"]))
        dx, dy, anchor = LABEL_LAYOUT[row["villa"]]
        line_end_x = x + dx + (5 if anchor == "end" else -5)
        line_end_y = y + dy - 5
        parts.append(f'<line x1="{x:.3f}" y1="{y:.3f}" x2="{line_end_x:.3f}" y2="{line_end_y:.3f}" stroke="#777777" stroke-width="0.9"/>')

    for row in rows:
        callout = CALLOUTS.get(row["villa"])
        if not callout:
            continue
        x, y = map_x(float(row["SPD_norm_exact"])), map_y(float(row["SRI_norm_exact"]))
        route = [(x, y), *callout[4]]
        points = " ".join(f"{px:.3f},{py:.3f}" for px, py in route)
        parts.append(f'<polyline points="{points}" fill="none" stroke="#555555" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>')

    for row in rows:
        x, y = map_x(float(row["SPD_norm_exact"])), map_y(float(row["SRI_norm_exact"]))
        parts.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="8" fill="#171717" stroke="#ffffff" stroke-width="1.5"/>')

    for row in rows:
        if row["villa"] in CALLOUTS:
            continue
        x, y = map_x(float(row["SPD_norm_exact"])), map_y(float(row["SRI_norm_exact"]))
        dx, dy, anchor = LABEL_LAYOUT[row["villa"]]
        parts.append(
            f'<text x="{x + dx:.3f}" y="{y + dy:.3f}" text-anchor="{anchor}" font-size="16" font-weight="700" paint-order="stroke" stroke="#ffffff" stroke-width="5" stroke-linejoin="round">{escape(row["villa"])}</text>'
        )

    for row in rows:
        callout = CALLOUTS.get(row["villa"])
        if not callout:
            continue
        x, y, width, height, _, metric, finding = callout
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="4" fill="#ffffff" fill-opacity="0.97" stroke="#888888" stroke-width="1"/>',
                f'<text x="{x + 14}" y="{y + 22}" font-size="16" font-weight="700">{escape(row["villa"])}</text>',
                f'<text x="{x + 14}" y="{y + 43}" font-size="14" fill="#444444">{escape(metric)}</text>',
                f'<text x="{x + 14}" y="{y + 65}" font-size="14" font-weight="600">{escape(finding)}</text>',
            ]
        )

    parts.append("</g></svg>")
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Path to the final metrics CSV.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("figure13_morphospace.svg"),
        help="Output SVG path (default: figure13_morphospace.svg).",
    )
    args = parser.parse_args()

    rows, medians = load_and_compute(args.data)
    args.output.write_text(build_svg(rows, medians), encoding="utf-8")
    print(f"Wrote {args.output} from {len(rows)} validated metric rows.")


if __name__ == "__main__":
    main()
