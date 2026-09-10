# Reconstructing Palladian Symmetry

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21842439.svg)](https://doi.org/10.5281/zenodo.21842439)

Minimal public reproducibility repository for the article **“Reconstructing Palladian Symmetry: Quotient Trees and House-and-Wing Morphospace.”**

This repository preserves the final 16-villa metric table, the final quotient-tree diagrams, the supplementary workflow diagrams, and the two small scripts needed to validate Table 1 and regenerate Figure 13. It is a publication support archive, not the development repository for the analysis software.

## Version v1.1 — September 10, 2026

Updated from analysis source [`9afbb43`](https://github.com/sbrgkmn/260224_PalladioGraph/commit/9afbb43). All sixteen quotient-tree and workflow images reflect the current directed connections, compact branch arrangements, and numbered-node alignment. Distinct dashed connections remain visible; self-loops and redundant reverse arrows are suppressed in the presentation. Display layout changes do not alter the analytical metrics.

Compared with v1.0, the corrected Zeno graph changes Q and E_Q from 21 to 22, leaves from 9 to 10, and leaf-depth sum from 40 to 47. Zeno now has SPD raw **4.700**, SPD norm **0.536**, SRI raw **0.045**, and SRI norm **0.205**. All other metric rows, the corpus medians, and all morphospace category assignments remain unchanged. Zeno remains in **Sequential wing propagation**. The previously corrected Repeta values remain unchanged.

The DOI badge links to all versions; the original v1.0 remains available at [its version DOI](https://doi.org/10.5281/zenodo.21842440).

## Corpus

The fixed corpus contains sixteen Palladian villas: Angarano, Barbaro, Capra, Cornaro, Emo, Foscari, Pisani, Poiana, Ragona, Repeta, Saraceno, Serego, Thiene, Trissino, Valmarana, and Zeno. The analysis treats the central house and attached or extended wings as one compositional system.

No Palladio scans or other copyrighted source images are included. The diagrams in this repository are final analytical outputs.

## Inside-out symmetry-graph method

Each plan is encoded as a room-centroid graph and ordered from the compositional center outward. Bilaterally corresponding nodes are collapsed into quotient nodes; on-axis and unmatched residual nodes remain explicit. A rooted quotient tree records the principal inside-out propagation hierarchy, while additional quotient-graph edges are retained as surplus connections rather than discarded.

The archived diagrams are the final manuscript versions. This repository does not rerun plan extraction, symmetry matching, or tolerance experiments.

## SPD and SRI

**Symmetry Propagation Depth (SPD)** is the mean depth of quotient-tree leaves:

```text
SPD_raw = sum of leaf depths / number of leaves
```

**Symmetry Reticulation Index (SRI)** measures surplus quotient-graph connectivity relative to all quotient edges:

```text
tree_min_edges = Q - C_Q
surplus_edges = E_Q - tree_min_edges
SRI_raw = surplus_edges / E_Q
```

Here `Q` is the quotient-node count, `E_Q` is the quotient-edge count, and `C_Q` is the quotient-graph component count. SPD and SRI are independently min-max normalized across the fixed sixteen-villa corpus for Figure 13.

The corrected final Repeta values are:

```text
Q = 26                 E_Q = 29
Surplus = 4            Leaves = 11
Branches = 6           Max depth = 8
SPD raw = 3.909        SPD norm = 0.357
SRI raw = 0.138        SRI norm = 0.621
```

## Repository contents

```text
data/
  palladio_spd_sri_metrics.csv   Final Table 1 values and sufficient leaf-depth counts for recomputation
code/
  compute_spd_sri.py             Recomputes, validates, and exports the final Table 1 metrics
  plot_morphospace.py            Regenerates Figure 13 as a self-contained SVG
figures/
  figure13_morphospace.svg      Morphospace regenerated from the updated CSV
quotient_trees/
  *_quotient_tree.png            Final quotient-tree diagram for each of the sixteen villas
supplementary/
  fig_workflow_*.png             Final supplementary workflow diagram for each villa
```

## Reproduce Table 1

Python 3.9 or newer is sufficient; the scripts use only the Python standard library.

From the repository root, run:

```bash
python code/compute_spd_sri.py
```

The script recomputes SPD and SRI from the archived integer counts, applies corpus min-max normalization, verifies every displayed value against the final manuscript values, and prints Table 1. To save the regenerated table:

```bash
python code/compute_spd_sri.py --output table1_recomputed.csv
```

The expected corpus medians are SPD raw `4.026`, SPD norm `0.383`, SRI raw `0.108`, and SRI norm `0.487`.

## Regenerate Figure 13

Run:

```bash
python code/plot_morphospace.py
```

This creates `figure13_morphospace.svg` from the same validated CSV. The primary axes show normalized SPD and SRI, the secondary axes show the corresponding raw ranges, and dashed lines mark the corpus medians used in the published morphospace.

## Publication support

This repository supports the data and figure claims reported in **“Reconstructing Palladian Symmetry: Quotient Trees and House-and-Wing Morphospace.”** It intentionally excludes obsolete graph versions, debugging files, discarded analyses, intermediate tolerance experiments, copyrighted Palladio scans, and manuscript drafts.
