# Collatz octaves: results (20 Nov 2026, 9:40 AM session)

> **CORRECTION (26 Nov 2026, see `funnel/results.md`):** the "~5.5 steps quicker than the coin" below is an artefact of where I put the coin's finish line (log <= 0). With the same finish rule as Collatz (below 2), Collatz is about 1.7 steps SLOWER, flat across sizes. The descent itself matches a fair coin; the real difference is at the floor (below 64). The "skew flattens at 0.665" was also the top of a hump (it peaks at 0.669, k 28, then falls).

`oct.c`: standard step count (3n+1 / halve, to 1) for every n < 2^31, memo below 2^28, 54 s on one core. Outputs: octaves.tsv (mean, sd, skew per octave), hist.tsv (full step histogram per octave), records.tsv (69 step records to 2^31; top: 1,674,652,263 at 1008 steps).
`coin.py`: fair-coin model (each shortcut step is (3n+1)/2 or n/2 with chance 1/2, counting 2 or 1 standard steps; stop when the log falls to 0), 1M samples per octave, n uniform in the octave.

Coin-model theory (renewal): mean = 3 ln n / ln(4/3) = 10.4277 ln n; per-step cost-minus-drift fluctuation is exactly +-6.229, so var = 6.229^2 / 0.1438 = 270 per unit ln n, SD / sqrt(ln n) -> 16.4.

| k | real mean | coin mean | real sd | coin sd | real skew | coin skew |
|---|---|---|---|---|---|---|
| 10 | 74.99 | 79.40 | 43.42 | 45.27 | 0.528 | 1.572 |
| 15 | 110.09 | 115.59 | 50.96 | 54.67 | 0.548 | 1.306 |
| 20 | 146.24 | 151.64 | 58.97 | 62.55 | 0.616 | 1.132 |
| 25 | 182.28 | 187.81 | 66.36 | 69.74 | 0.658 | 1.027 |
| 30 | 218.42 | 224.02 | 73.08 | 76.04 | 0.665 | 0.934 |

- Mean / ln n: 10.10 (k 9) -> 10.303 (k 30), creeping up toward 10.43. Prediction 1 right.
- Mean minus 10.43 ln(1.5 x 2^k): coin sits at a flat +2.9; Collatz at about -2.5 to -2.65, drifting down very slowly. So real Collatz runs a near-constant ~5.5 steps quicker than the coin, at every size from 2^10 to 2^30.
- SD / sqrt(ln n): 15.5-15.9, rising slowly toward the coin's 16.4. Prediction 2 (4-6) WRONG: I botched the variance by not counting that odd steps cost 2; the renewal sum gets it.
- Skew: coin falls like 1/sqrt(ln n) (1.57 -> 0.93), as an inverse-Gaussian first passage should. Real Collatz RISES from 0.46 (k 11) and flattens at 0.665 (k 27-30). They'd meet around k 40+ if the coin keeps falling. Prediction 3 (< 0.3) wrong in both directions. Best bit.
- 1995: 50 steps; octave 1024-2047 mean 75.0; 38% of that octave is quicker; 34 numbers in the octave share exactly 50. Prediction 4 (below 10th percentile) wrong: ordinary-quick, not rare.
- Records: 69 to 2^31, not ~150. Prediction 5 wrong.

Scored: 1 right, 2-5 wrong.

Guess (not tested): the real map funnels: trajectories merge onto shared highways (e.g. through 9232, 160, 16), so the endgame is shared and deterministic rather than an independent random tail. That would explain the constant mean offset and the low skew at small n. Test: skew of the steps to first fall below sqrt(n) (no endgame) vs the coin.

`render.py` -> collatz_octaves.png (histogram 1024-2047 with 1995 marked; mean offset vs coin; skew vs coin). Viewed: readable, no overlaps.
