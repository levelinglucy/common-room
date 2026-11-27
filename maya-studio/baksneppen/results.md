# Bak-Sneppen with far neighbours (19 Nov 2026, 3:40 PM session)

Model: N species on a ring, fitness in [0,1]. Each step the least fit species and two neighbours get new uniform fitnesses; each of the two neighbours is, with probability p, swapped for a uniformly random species anywhere. Threshold f_c = half-plateau point of the stationary fitness histogram (`analyse.py`). Code: `bs.c` (segment-tree minimum, ~9M steps/s), `bs_runs.c` (adds mean run length of min < f on a grid of f), `bs_drop.c` (ring where each neighbour is refreshed only w.p. 1-p, no far refresh), `seed1.c` (single-seed f-avalanche on an infinite line in the dropout ring), `render.py` -> `far_neighbour.png`.

## Thresholds and the branching prediction

Branching rule: an avalanche that starts from one weak species (below f) runs on the ring, with each dragged neighbour going far w.p. p. Each step it makes 2p far refreshes, each below f w.p. f, and each such one starts a fresh single-seed avalanche somewhere else. So the far links make a branching process with mean offspring 2 p f s1(f; p), where s1 is the mean single-seed avalanche size in the dropout ring. The threshold is where that equals 1. At p = 1, s1 = 1/(1-f) and the rule gives f = 1/3 exactly.

(results_table.txt; N -> inf estimate = f8000 - (f2000 - f8000), i.e. bias ~ N^-1/2, which is exact-looking at p = 1 and does NOT work at p = 0, where the ring scales differently.)

p          fc N=2000  fc N=8000  fc N->inf est   branching prediction  pred - est
0.0001     -          0.6508     -               0.6506                (vs N=8000: -0.0002)
0.001      0.6295     0.6292     0.6289          0.6286                -0.0003
0.003      0.6107     0.6100     0.6094          0.6093                -0.0001
0.01       0.5790     0.5781     0.5772          0.5772                -0.0000
0.03       0.5358     0.5349     0.5340          0.5339                -0.0001
0.1        0.4701     0.4688     0.4676          0.4673                -0.0002
0.2        0.4242     0.4229     0.4216          0.4214                -0.0002
0.3        0.3966     0.3951     0.3936          0.3935                -0.0001
0.5        0.3637     0.3621     0.3604          0.3604                -0.0000
0.7        0.3460     0.3443     0.3427          0.3427                +0.0001
1          0.3367     0.3350     0.3333          0.3333 (exact)        +0.0000

Ring p = 0: 0.6641 (N 2000), 0.6662 (N 8000); literature value 0.66702 (from memory). Small p at N 8000: 1e-6 0.6639, 1e-5 0.6603, 3e-5 0.6566, 3e-4 0.6427. Seeds 7/21/22 at N 2000 agree within 0.0005.

Two cruder versions, for the record: using the plain ring's mean run length instead of s1 works only for p <= 1e-4 (error -0.0005 there, -0.025 at p = 0.1, because far links also shrink the ring part). Using the dropout ring's run lengths (which start from 1-3 weak sites, not one) halves that error but is still 0.01-0.018 low at p 0.1-0.7. The single seed is the right object.

## Other numbers

- Ring mean f-avalanche (run of min < f, N 8000, 2 x 400M steps): 22.1 at f 0.50, 203 at 0.60, 2,121 at 0.64. Fitted gamma 2.46 (0.45-0.64), 2.54 (0.55-0.645), 2.60 (0.60-0.65): creeping towards the literature 2.70.
- Drop f_c(0) - f_c(p) ~ p^0.39 for p 1e-5 to 1e-2, close to 1/gamma: the far links cap the ring avalanches at size ~1/(2pf).
- Jumps of the minimum, ring: tail exponent 3.21 (prediction 3.2). Far jumps (> 100 sites) are ~10x more common than 2p/3 at small p (p 1e-4: 0.00108 vs 0.00007; p 1e-3: 0.0075 vs 0.00067), because once a far weak species is seeded, the minimum hops back and forth between two or more active regions. Trace N 600, p 0.001: 340 far jumps (> 50 sites) in 60k steps vs 120 far refreshes.
- Threshold step width (10-90%) widens from 0.004 (ring) to 0.014 (p = 1) at N 8000.

## Predictions scored (predictions.md)

1. Ring 0.667 +- 0.002 at N 2000: wrong-ish, 0.664 (finite size; 0.666 at 8000).
2. p = 1 gives 1/3: right (0.3350 at N 8000, -> 0.3333). "Softer step": right (width 0.004 -> 0.014).
3. Falls fast, half the drop by p = 0.1: right and faster than guessed: 0.47 at p = 0.1, the half point is near p = 0.06, and one in a thousand already moves it 0.037.
4. Avalanche exponent crossover to 3/2: not tested.
5. Ring jump tail 3.2: right (3.21). Far jumps ~2p/3: wrong by ~10x, for an interesting reason (hopping between coexisting fronts).

Probably known in part: Bak-Sneppen on small-world networks has been studied (Kulkarni, Almaas & Stroud 1999, from memory, not checked). Not checked whether the single-seed branching criterion that pins the whole curve is in the literature.
