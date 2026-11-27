# Quenched far links (19 Nov 2026, 6:40 PM session)

Model: as in results.md, but each species' left and right slot is fixed at the start: with chance p it is rewired for good to a uniformly random species. The weakest species always drags the same two. Code: `bs_q.c` (adds a fitness histogram split into clean sites vs sites touched by rewiring), `bs_q2.c` (mode 0 random rewiring, mode 1 every in-degree exactly 2 via two random permutations, mode 2 half the species never dragged; histograms by in-degree), `tree.c` (single-seed f-avalanche on an endless out-tree where every species has the same two children forever; order 0 min, 1 random, 2 annealed check), `tree_stats.c` (counts drags that land on an already-weak child), `treering.c` (single seed on an endless tree of rings: each species on a line, each slot with chance p a permanent link to a fresh species on a fresh line), `render_quenched.py` -> `fixed_or_fresh.png`.

## Thresholds (half-plateau of the fitness histogram, analyse.py)

p       quenched N2000 (wirings 7/21/22)   mean    N8000   annealed N8000   tree of rings (single seed)
0.001   0.6624 0.6638 0.6601               0.6621  0.6642  0.6292           -
0.003   0.6606 0.6585 0.6581               0.6591  0.6575  0.6100           -
0.01    0.6429 0.6476 0.6434               0.6446  0.6399  0.5781           0.635-0.640 (P_inf extrapolation ~0.6385)
0.03    0.6221 0.6125 0.6099               0.6148  0.6134  0.5349           0.605-0.610 (~0.606)
0.1     0.5622 0.5570 0.5587               0.5593  0.5534  0.4688           0.545-0.550 (~0.548)
0.2     0.5049 0.5075 0.5081               0.5068  0.5074  0.4229           -
0.3     0.4796 0.4777 0.4803               0.4792  0.4770  0.3951           0.470-0.475 (~0.471)
0.5     0.4442 0.4443 0.4433               0.4439  0.4392  0.3621           -
0.7     0.4232 0.4263 0.4252               0.4249  0.4185  0.3443           -
1       0.4117 0.4130 0.4128               0.4125  0.4070  0.3350           0.401-0.402 (pure tree)

Quenched minus annealed at N 8000: +0.035 at p = 0.001, peaking at +0.085 around p = 0.1-0.2, +0.072 at p = 1. Fixed links are much worse at spreading trouble than fresh ones.

## p = 1: the endless tree pins it

- Size scan, random fixed links: 0.4235 (N 500), 0.4117 (2000), 0.4070 (8000), 0.4043 (32000). Differences shrink by about half per factor 4 (N^-1/2), so N -> inf ~ 0.4016.
- Every species dragged by exactly two (no in-degree spread): 0.4072, 0.4045, 0.4031, 0.4024 -> ~0.4017. So the in-degree spread is NOT the cause (my first guess).
- Half the species never dragged (mode 2, N 8000): 0.4234, so heavy in-degree spread does push it up, but that is a separate, smaller effect.
- Endless out-tree, single seed, min order: survival to 3M steps is 0 at f = 0.401 (8000 seeds) and a plateau of 0.0036 at 0.402, 0.012 at 0.403, 0.024 at 0.404. Threshold 0.4015 +- 0.0005. Random order instead of min order: ~0.404-0.405 (order matters a little).
- Annealed check of tree.c: mean single-seed size at f = 0.25 is 4.02 (exact 1/(1-3f) = 4).

Why: per step, the weak count changes by -1 + f (the minimum itself) + sum over its two drags of (f - [already weak]). With fresh links, drags never land on a weak species, so 3f = 1. With fixed links the weakest species often comes back (47% of avalanche steps at f = 0.401 are a species that has been the minimum before) and drags the same two it just made weak. Measured on the tree at f = 0.401: 10.19% of drags land on an already-weak child; the balance condition (3f - 1)/2 at f = 0.4015 is 10.15%. On the tree every such hit comes from a repeat minimum (true by construction: only the parent can have made the child weak).

## Small p

The tree of rings (ring segments joined by permanent far links, no loops at large scale) matches the graph's thresholds within the seed spread and the finite-size drift: 0.548 vs graph ~0.548 (N^-1/2 extrapolation of the 3-wiring mean) at p = 0.1; 0.471 vs 0.475 at p = 0.3; 0.606 vs ~0.612 at p = 0.03 (wiring spread is large there: sd 0.0064 at N 2000); 0.6385 vs ~0.635 at p = 0.01. So the quenched small world is, locally, an endless tree of rings, just as the annealed one was a branching process of single-seed ring avalanches.

The quenched drop from the ring is slow: 0.666 (ring, N 8000) -> 0.664 at p = 0.001 (annealed: 0.629). A fixed far link mostly re-stirs the same distant spot, which recovers in between.

## Predictions scored (predictions_quenched.md)

1. p = 1 still about 1/3, maybe 0.34: wrong, 0.4015. Best result of the session.
2. Quenched higher than annealed, ~0.60 at p = 0.01: right in direction, wrong in size (0.64 at N 8000; the gap is 0.06-0.085 for p >= 0.01).
3. The annealed branching rule fails for quenched: right, but the fix is clean: run the single seed on a tree of rings instead.
4. Bigger wiring spread, +- 0.003 at p = 0.01, N 2000: right (sd 0.0026 at 0.01, 0.0064 at 0.03; annealed seeds agreed within 0.0005).
5. Clean species sit in a sharper threshold: wrong. Same half point; widths 0.010 vs 0.018 at p = 0.01 but no consistent pattern.

Not checked: whether 0.4015 for Bak-Sneppen on a random directed graph of out-degree 2 is known (I believe random-neighbour vs fixed-random-graph BS has been compared in the literature, from memory only).
