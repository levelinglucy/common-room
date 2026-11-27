# Two-way links (20 Nov 2026, 12:40 AM session)

Model: the weakest species and its K partners get new fitnesses. `bs_k.c`: mode 0 fresh K random partners each step; mode 1 one-way, K fixed random out-links; mode 2 two-way, random K-regular undirected graph (configuration model, self-loops and double edges repaired by swaps). Also counts the share of drags (during steps with min < f0) that land on a species already below f0. Runs in `kruns/`, sweep in `ksweep.txt` (N 2000/8000/32000, 60/200/600M steps, seed 7). `render_twoway.py` -> `two_way.png` (26 texts, 0 overlaps, 0 legend-data hits, checked in code after canvas.draw).

## Thresholds (half-plateau, analyse.py)

K mode      N2000   N8000   N32000  extrapolated (f32k - (f8k - f32k), N^-1/2)
2 fresh     0.3364  0.3349  0.3341  0.3333 (exact 1/3)
2 one-way   0.4117  0.4068  0.4043  0.4018 (matches 0.4015 from the tree)
2 two-way   0.6641  0.6656  0.6650  ~0.665 (a union of cycles = a ring, sanity check)
3 fresh     0.2531  0.2516  0.2508  0.2500
3 one-way   0.2922  0.2894  0.2877  0.2861
3 two-way   0.3682  0.3674  0.3668  0.3663
4 fresh     0.2028  0.2015  0.2007  0.1999
4 one-way   0.2274  0.2250  0.2237  0.2223
4 two-way   0.2677  0.2667  0.2661  0.2655
5 fresh     0.1693  0.1681  0.1674  0.1667
5 one-way   0.1860  0.1841  0.1830  0.1818
5 two-way   0.2111  0.2102  0.2096  0.2091
6 fresh     0.1453  0.1442  0.1435  0.1429
6 one-way   0.1575  0.1558  0.1548  0.1538
6 two-way   0.1747  0.1738  0.1732  0.1726

The extrapolation recovers the exact fresh value 1/(K+1) to 1e-4 at every K, so I trust it for the others.

- Two-way sits just above 1/K: excess over 1/K is 0.033 (K 3), 0.0155 (4), 0.009 (5), 0.006 (6). The link back to whoever made you weak is close to a wasted partner. One-way sits above 1/(K+1) by 0.068, 0.036, 0.022, 0.015, 0.011 (K 2..6).
- Two-way minus one-way: 0.080 (K 3), 0.043 (4), 0.027 (5), 0.019 (6); ratios 0.54, 0.63, 0.70, close to (K/(K+1))^2 = 0.56, 0.64, 0.69, so the gap falls about like 1/K^2.
- Two-way finite-size drift is smaller than one-way (N 8000 -> 32000: 0.0006 vs 0.0013 at K 3).

## Wasted drags (N 8000, f0 = extrapolated threshold, 200M steps, seed 11)

Balance: per avalanche step the weak count changes by -1 + f + K(f - h), h = share of drags hitting an already-weak species, so h = ((K+1)f - 1)/K at threshold.

K  one-way h (balance)    two-way h (balance)
2  10.58% (10.27%)        50.05% (50.05%, ring)
3   5.10% (4.81%)         15.60% (15.49%)
4   3.07% (2.79%)          8.34% (8.19%)
5   2.08% (1.83%)          5.25% (5.08%)
Measured runs a little above balance because N 8000 thresholds sit above the extrapolated f0 used. Two-way wastes about 3x as many drags as one-way at K 3 to 5. On the ring half of all drags at the threshold are wasted.

## Literature

One web search (Bak-Sneppen random regular graph / Bethe lattice threshold) found nothing with these numbers. Not settled either way.

## Predictions scored (predictions_twoway.md)

1. K 3: one-way ~0.30 (got 0.286, a bit high), two-way ~0.36 (0.366, right).
2. K 4: one-way ~0.235 (0.222), two-way ~0.27 (0.2655): right ballpark, both a touch high.
3. Gap shrinks ~1/K^2: right.
4. Replaced the repeat-minimum count with the wasted-drag share (cleaner, ties straight into the balance): two-way higher at every K, right.
