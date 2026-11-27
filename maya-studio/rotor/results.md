# Rotor-router discs: results (20 Nov 2026, 3:40 AM session)

> **CORRECTION (20 Nov 2026, 6:40 AM, see `lattices/results.md`):** the claim below that random starting arrows give a disc "about as round as all-north" is WRONG. Discs from same-direction arrows are centred off the start site (on the square grid, on a cell corner half a cell over), and the gap here was measured from the start site, so it mostly measured that offset. Measured from the true centre, same-direction arrows give discs 3-10x smoother than random arrows. rotor_discs.png carries the old, wrong comparison.

`rotor.c` (modes: 0 all north, 1 random arrows, 2 checkerboard N/E, 3 IDLA). 300,000 walkers each, radius ~309. Each run ~4 to 5 min, 8 runs in parallel. Raw: out/*.txt (n, disc radius, out-excess, in-deficit, gap, cumulative steps at checkpoints x1.25), out/*.bin (final grid: 0 empty, 1+arrow).

Gap = farthest occupied minus nearest empty site.

| start | max gap (n >= 1000) | mean gap | final gap |
|---|---|---|---|
| all north | 1.667 | 1.505 | 1.584 |
| checkerboard | 1.878 | 1.589 | 1.878 |
| random 1/2/3 | 2.045 / 2.321 / 1.762 | 1.46 / 1.51 / 1.38 | 1.75 / 1.69 / 1.64 |
| IDLA 1/2/3 | 6.668 / 7.275 / 7.016 | 4.90 / 4.84 / 4.77 | 6.35 / 5.52 / 7.02 |

Steps vs sum of |x|^2 over settled sites (each step changes |x|^2 by 2 v.d + 1; arrows cycling N,E,S,W cancel the 2 v.d over each full turn, so only part-turns are left):
- arrows: diff -1.43e6 (north), -1.03e6 (check), -5.9e5, -2.3e5, -1.8e4 (random) out of 1.4324e10: within 1.0e-4.
- IDLA: +2.2e7, +4.5e7, +2.2e7: 0.15% to 0.31% over (random-walk noise).
- n^2/(2 pi) = 1.43239e10 for comparison; sum|x|^2 itself is 1.43240-1.43247e10.

Scored predictions:
1. right (north gap < 2 throughout: max 1.667).
2. WRONG, best result: random starting arrows are about as round as all-north (max 1.76-2.32, mean ~1.45). The disorder of the start barely shows at the edge. The memory in the arrows makes the roundness, not the starting order.
3. half right: IDLA gap 5.5-7.3 at r ~ 309, a bit under my 6-10 guess; growth with log r is plausible on the plot but not fitted.
4. right (checkerboard max 1.878).
5. not tested properly; the north picture shows the known curved-region patterns. Random start picture: see rotor_discs.png (interior arrows reorganised, not noise? look again next time with a zoom).

Picture: rotor_discs.png (three discs, gap vs radius, summary). 86 texts checked in code: only false positives from hidden axes; legend-data hits 0.

Follow-up: share of left-right neighbours holding the same arrow, inner 70% of the disc: north 0.289, random 0.298, checkerboard 0.293 (pure noise would be 0.25). After 300,000 walkers the three interiors look statistically alike; the start is forgotten inside too.
