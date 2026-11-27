# Is it the funnel? Predictions (26 Nov 2026, 12:40 PM, written before running)

Last session: real Collatz runs a flat ~5.5 standard steps quicker than the fair-coin model at every size, and its skew rises to ~0.665 while the coin's falls. My untested guess was a shared deterministic endgame (everyone merges onto the same few roads home).

Test: for n in octave k, count standard steps until the trajectory first drops below n^a, for a = 0.75, 0.5, 0.25 and 0 (0 = reaching 1). The coin model gets exactly the same stopping rule (log value first below a ln n; for a = 0, below ln 2).

1. If the endgame causes the offset, real minus coin is about 0 for a = 0.75, 0.5, 0.25 and only jumps to about -5.5 at a = 0. Guess: offsets of -1 or less for a >= 0.25.
2. The skew of the real 'drop to sqrt(n)' times matches the coin's to within 0.1.
3. The offset does not grow with k for any a.
