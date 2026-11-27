# Collatz octaves: predictions (20 Nov 2026, 9:40 AM, written before running)

Standard steps: n even -> n/2, n odd -> 3n+1, count steps to reach 1.
Coin model: each shortcut step (odd -> (3n+1)/2, even -> n/2) is a fair coin, log drift ln(3/4)/2 per shortcut step; standard steps = 1.5 x shortcut steps.

1. Mean standard steps per octave / ln n tends to 3/ln(4/3) = 10.43 from below (finite-size offset makes small octaves look low). Guess at 2^30: ratio 9.5-10.4.
2. SD of steps grows like sqrt(ln n): coin model gives var = N * (ln 3 / 2)^2 / drift^2 per shortcut step... predict SD/sqrt(ln n) roughly constant, ~ 4-6 standard steps.
3. Distribution per octave looks normal (skew small, < 0.3).
4. 1995 (50 steps) is unusually quick for its octave: below the 10th percentile.
5. Record holders (more steps than every smaller n) number about c * ln n: maybe ~150 up to 2^30.
