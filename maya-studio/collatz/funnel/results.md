# Is it the funnel? Results (26 Nov 2026, 12:40 PM session)

Code: `funnel.c` (steps to first drop below n^a, a = 0.75/0.5/0.25/0, real vs fair coin, identical stopping rule: coin stops when its log first falls below a ln n, or below ln 2 for a = 0). 4M starts per octave, k = 12..44 step 4, 128-bit arithmetic. Table in `results_raw.tsv`.
`endgame.c`: split at the first value below an absolute B. `floor.c`: steps spent below V (histogram `floor_hist_64.tsv`). `doors.py`: last entry into the zone below 64, 100k starts near 2^40.

## Findings

- **The drop is a fair coin.** Once the target is above about 2^14, Collatz and coin agree on the mean (within 0.06 steps), SD (within 0.2) and skew (within 0.01) for the drop below n^0.75 and n^0.5. At k = 44, drop below sqrt(n): 164.13 vs 164.10 steps, skew 1.093 vs 1.099. Same split at absolute B: drop phase matches; phase 1 and endgame uncorrelated (|corr| < 0.016).
- **Correction to 20 Nov:** the flat '5.5 steps quicker than the coin' was mostly where I put the coin's finish line. With the coin stopping at log <= 0 it's -5.5; stopping below 2 (the same rule as Collatz reaching 1) it's +1.7, flat from k 16 to 44 (1.66-1.86). The constant is a convention; the robust difference is shape.
- **The shape difference lives at the floor.** Endgame below B = 2^16 (k 40): mean 110.2 vs 108.4, SD 50.7 vs 53.0, skew 0.55 vs 1.35, longest 321 vs 832. Steps spent below 64: Collatz 16.1 +- 4.6, skew -0.61, longest 22; coin 27.8 +- 19.8, skew +1.82, longest 328. A coin can hover near the floor for hundreds of steps; Collatz never repeats a number and there are only 63 seats below 64.
- **Six doors home.** Near 2^40, the last entry below 64 is always a halving from 64-126 onto a number whose path then stays below 64: 40 (46.1%), 44 (25.6%), 56 (19.0%), 32 (6.2%), 34 (1.5%), 52 (1.5%). Multiples of 3 (48, 42 ...) are never doors: a multiple of 3 has no odd predecessor, so only its own doublings reach it.
- **Total skew turned:** Collatz reach-1 skew peaks at 0.669 (k 28) and falls to 0.626 (k 44). On 20 Nov I said it flattened; it was the top of a hump. Both should sink toward 0 as the drop dominates.

## Predictions scored
1. Offset near 0 for a >= 0.25, only the reach-1 one big: half right. a = 0.75 and 0.5 go to 0; a = 0.25 swings (+14 at k 16, -3.5 at k 28) and settles near -1.35 by k 36 (target only 2^9-2^11, still floor territory); the reach-1 offset is +1.7, not -5.5 (finish-line artefact).
2. Skew of the drop to sqrt(n) matches within 0.1: right from k 24 on (0.18 off at k 20, 0.77 at k 12).
3. Offsets don't grow with k: right.

## Open
- Door shares: can 40/44/56/32/34/52 be predicted from the 2-adic tree (the share of starts whose path passes 80, 88, 112, 64, 68, 104 last)? Do they converge as k grows?
- Why the a = 0.25 offset settles negative (-1.35) while reach-1 is positive.
- A 'self-avoiding coin' (no value visited twice, integer values) as a better model of the floor.
