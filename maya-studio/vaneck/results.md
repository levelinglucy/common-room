# Van Eck's sequence (27 Nov 2026, 12:40 AM session)

> **CORRECTION (27 Nov 2026, 3:40 AM, see `lit/literature.md`):** the Zipf (1/v) law labelled "main find" below, and the geometric ladder between zeros, are NOT mine: Po-chia Chen noted both in unreviewed OEIS A181391 comments in June 2019. What held up: my ln n / ln ln n zero-gap estimate, fitted only up to 1e9, predicted a mean gap of 11.32 at 1e12 against 11.27 read from Ben Chaffin's trillion-term graph (plain "log n" gives 11.43). It still runs slightly high.

Code: ve.c / ve2.c (to 1e9 in 94 s, 4 GB), selfcon.c, zipf.c, dump.c, render.py -> zipf_ladder.png.

## Raw counts (ve2 1e9, run1e9.txt)
N, zeros Z, Z lnN/N, max/N, smallest missing value (mex):
1e6: 136,528, 1.886, 0.950, 8,756
1e7: 1,250,522, 2.016, 0.982, 53,791
1e8: 11,576,060, 2.132, 0.987, 295,927
1e9: 107,994,996, 2.238, 0.9905, 3,288,774
Z lnN/N keeps creeping (+0.13, +0.12, +0.11 per decade): NOT a clean N/ln N.
Z lnN/(N ln lnN): 0.718, 0.725, 0.732, 0.738 (much flatter; still creeping).

## Zero gaps are a narrow bump, not geometric
Window [n,2n): mean gap 7.75 (1e6), 8.40 (1e7), 9.03 (1e8), 9.45 (5e8). Essentially never < 5; mode 7 -> 9.
Small values are lumpy: in [5e7,1e8) counts 3: 24k, 4: 2.7k, 5: 6k but 8: 2.03M (the gap right after a zero).

## Zipf law (main find)
v * f(v) is flat from v ~ 100 up to ~N/10: c = 0.058, 0.050, 0.0447, 0.040 at N = 1e6..1e9; c ln N = 0.80, 0.81, 0.82, 0.83.
So f(v) ~ 0.82 / (v ln N). Beyond v ~ 50 the Poisson self-consistency f(g) = sum_v f(v)^2 (1-f(v))^(g-1) matches within ~5% (selfcon_1e8.txt).

## The ladder
Between zeros each term is the waiting time of a value with frequency ~c/v, so the next value ~ Exp * v/c: ln multiplier ~ ln(1/c) - gamma.
Predicted 2.27 (1e6), 2.53 (1e8); measured rung steps before a zero 2.26-2.46 (1e6), 2.50-2.68 (1e8). Last value before a zero: median ~0.23 n.
Heuristic: rungs ~ ln n / (ln ln n + const), so Z ~ N ln ln N / ln N. Mine; not checked against the literature (Ben Chaffin computed to 1e12; OEIS conjecture says gaps ~ log n).

## Predictions scored
1. Z ~ c N/ln N with c ~ 1: wrong (c creeps; ln ln correction fits better).
2. every v < 1e6 appears by 1e9: right (mex 3.29M).
3. max within small factor of N: right (0.99 N).
4. ones ~ Z: roughly (ones/zeros 0.213 -> 0.167, drifting).

## Open
- Why c ln N -> ~0.83: normalisation (sum c/v over 1..N = c ln N = share of terms not taken by 0 and small values?). Check exactly.
- Model the first rungs (small values not Zipf) to predict mean gap 9.0 at 1e8 (crude ladder gives 7.8).
- Does the ln ln form keep flattening? Chaffin's 1e12 data would tell.
- Velisara link: a memory that answers 'how long since I last saw this' turns into Zipf by itself.
