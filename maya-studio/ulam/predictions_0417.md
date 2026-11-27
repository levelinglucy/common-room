# What is 0.41703? Predictions (written 19 Nov 2026, 12:45 AM, before running anything)

Setup: U(1,b) terms are u = A*b + B with A not a multiple of 3 (after the opening). The clock is lambda = 3b + c, c = 0.41703.

If lambda were exactly 3b, the phase u/lambda would be A/3 + B/(3b), so terms sit near phases 1/3 and 2/3 and never near 0. With c, the phase is about A/3 + (3B - A c)/(9b). For the beat to stay locked for ever, B must grow in step with A: B ~ beta * A, and then c = 3 * beta.

1. Writing terms of U(1,b) for a large b (b = 1000 or more) as A*b + B with |B| small, B/A tends to a constant beta = 0.13901 (= 0.41703 / 3), within 1%.
2. B is not just beta*A plus noise: the residual B - beta*A stays bounded (a few units at most) and its histogram is the folded shape.
3. The (A, B) list is identical for b = 1000 and b = 2000 over the range where both are rigid.
4. beta is irrational-looking (no small fraction within 1e-4).
5. The same trick explains U(1,2) and U(1,3) not fitting: their B is not small next to b, so the split into A and B means nothing.
