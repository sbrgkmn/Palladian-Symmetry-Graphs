#!/usr/bin/env python3
"""Recompute the published Table 1 SPD and SRI values from final tree data."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = REPOSITORY_ROOT / "data" / "palladio_spd_sri_metrics.csv"
THREE_PLACES = Decimal("0.001")
PUBLISHED_FIELDS = ("SPD_raw", "SPD_norm", "SRI_raw", "SRI_norm")


def round_published(value: Decimal) -> Decimal:
    """Round exactly as the manuscript table does (three decimals, half up)."""

    return value.quantize(THREE_PLACES, rounding=ROUND_HALF_UP)


def median(values: Iterable[Decimal]) -> Decimal:
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / Decimal(2)


def load_and_compute(path: Path = DEFAULT_DATA) -> tuple[list[dict], dict[str, Decimal]]:
    """Load final base counts, recompute the four reported metrics, and validate them."""

    with path.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))

    if len(source_rows) != 16:
        raise ValueError(f"Expected the fixed 16-villa corpus; found {len(source_rows)} rows.")

    rows: list[dict] = []
    for source in source_rows:
        q = int(source["Q"])
        e_q = int(source["E_Q"])
        c_q = int(source["C_Q"])
        leaves = int(source["leaves"])
        leaf_depth_sum = int(source["leaf_depth_sum"])
        surplus = e_q - (q - c_q)

        if surplus != int(source["surplus_edges"]):
            raise ValueError(
                f"{source['villa']}: surplus mismatch; {e_q} - ({q} - {c_q}) = {surplus}."
            )
        if leaves <= 0 or e_q <= 0:
            raise ValueError(f"{source['villa']}: leaves and E_Q must be positive.")

        row = dict(source)
        row.update(
            Q=q,
            E_Q=e_q,
            C_Q=c_q,
            surplus_edges=surplus,
            leaves=leaves,
            branches=int(source["branches"]),
            max_depth=int(source["max_depth"]),
            leaf_depth_sum=leaf_depth_sum,
            SPD_raw_exact=Decimal(leaf_depth_sum) / Decimal(leaves),
            SRI_raw_exact=Decimal(surplus) / Decimal(e_q),
        )
        rows.append(row)

    spd_values = [row["SPD_raw_exact"] for row in rows]
    sri_values = [row["SRI_raw_exact"] for row in rows]
    spd_min, spd_max = min(spd_values), max(spd_values)
    sri_min, sri_max = min(sri_values), max(sri_values)

    for row in rows:
        row["SPD_norm_exact"] = (row["SPD_raw_exact"] - spd_min) / (spd_max - spd_min)
        row["SRI_norm_exact"] = (row["SRI_raw_exact"] - sri_min) / (sri_max - sri_min)
        calculated = {
            "SPD_raw": row["SPD_raw_exact"],
            "SPD_norm": row["SPD_norm_exact"],
            "SRI_raw": row["SRI_raw_exact"],
            "SRI_norm": row["SRI_norm_exact"],
        }
        for field in PUBLISHED_FIELDS:
            expected = Decimal(row[field])
            actual = round_published(calculated[field])
            if actual != expected:
                raise ValueError(
                    f"{row['villa']} {field}: computed {actual}, published {expected}."
                )

    medians = {
        "SPD_raw": median(spd_values),
        "SPD_norm": median(row["SPD_norm_exact"] for row in rows),
        "SRI_raw": median(sri_values),
        "SRI_norm": median(row["SRI_norm_exact"] for row in rows),
    }
    return rows, medians


def table_rows(rows: list[dict]) -> list[list[str]]:
    output = []
    for row in rows:
        output.append(
            [
                row["villa"],
                str(row["Q"]),
                str(row["E_Q"]),
                str(row["surplus_edges"]),
                str(row["leaves"]),
                str(row["branches"]),
                str(row["max_depth"]),
                f"{round_published(row['SPD_raw_exact']):.3f}",
                f"{round_published(row['SPD_norm_exact']):.3f}",
                f"{round_published(row['SRI_raw_exact']):.3f}",
                f"{round_published(row['SRI_norm_exact']):.3f}",
            ]
        )
    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    header = [
        "Villa",
        "Q",
        "E_Q",
        "Surplus",
        "Leaves",
        "Branches",
        "Max depth",
        "SPD raw",
        "SPD norm",
        "SRI raw",
        "SRI norm",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(table_rows(rows))


def print_markdown(rows: list[dict], medians: dict[str, Decimal]) -> None:
    print("| Villa | Q | E_Q | Surplus | Leaves | Branches | Max depth | SPD raw | SPD norm | SRI raw | SRI norm |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for values in table_rows(rows):
        print("| " + " | ".join(values) + " |")
    print()
    print(
        "Corpus medians: "
        f"SPD raw={round_published(medians['SPD_raw']):.3f}, "
        f"SPD norm={round_published(medians['SPD_norm']):.3f}, "
        f"SRI raw={round_published(medians['SRI_raw']):.3f}, "
        f"SRI norm={round_published(medians['SRI_norm']):.3f}."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help="Path to the final metrics CSV.")
    parser.add_argument("--output", type=Path, help="Optional path for a regenerated Table 1 CSV.")
    args = parser.parse_args()

    rows, medians = load_and_compute(args.data)
    print_markdown(rows, medians)
    if args.output:
        write_csv(args.output, rows)
        print(f"Wrote {args.output}")
    print("Validated all 16 published metric rows.")


if __name__ == "__main__":
    main()
