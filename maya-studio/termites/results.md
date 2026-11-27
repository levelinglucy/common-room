# Termites and wood chips (19 Nov 2026, 3:40 AM session)

Code: `termites.c` (L p T maxticks seed every [snapprefix|-] [tstart for drop stats]), `duel.c` (L T MA MB seed maxticks [fluxend] [jump]), `wander.py`, `render_termites.py` -> `termites_rigged.png`.
Rule: 8 headings, wiggle -1/0/+1, step 1; empty + chip -> pick up, jump 20; carrying + chip -> walk until empty cell, drop, jump 20. Pile = 8-connected cluster on the torus.

## Coarsening (L = 256, p = 0.15, T = 1200, 8 seeds)
- Pile count is not a power law: local exponent climbs 0.4 -> 0.7 -> 1.1 -> 1.7 between t = 200 and 10k (the initial singletons evaporating), then a floor of 6-20 'piles' that are mostly 1-4 chip fragments next to the big pile.
- Piles >= 500 chips: 8.6 (20k) -> 5.9 (39k) -> 3.4 (150k) -> 1.5 (575k) -> 1.1 (1.1M).
- 8-connected count does go up sometimes (pickups split piles): prediction 2 right.
- Time until the largest pile holds 80% of chips, geo mean of 8: L=64 9.6k, L=128 42k, L=256 708k. Faster than L^2 per doubling at the top end (prediction 3 roughly right). L=32 too small: 19 termites keep tearing a 154-chip pile into 2-3 pieces.

## The last pile wanders (L = 128, p = 0.15, T = 300, 4 seeds, 4M-40M ticks)
- Solid disc: Rg 19.6, so area ~2,410 for ~2,390 chips (essentially packed).
- MSD of its centre: 19.6, 39.0, 82.2, 167.7, 335.8, 708.9, 1488 at lags 0.2..12.8M ticks. Linear: plain diffusion, D ~ 2.45e-5 cells^2/tick.
- Prediction from independent chip hops: drop rate 0.543/tick x mean hop^2 1,291 / M^2 (2,390^2) = 24.5 per 0.2M ticks vs 19.6 seen: hops explain ~80%; the rest is presumably anti-correlation (a bump that loses a chip is less likely to lose the next). Prediction 4 right.

## Duels: two solid discs, L = 128, T = 300, jump 20
- 1200 vs 1200 (16 runs): A 7, B 9. Median 53k ticks (38k-76k for 12 runs; tail 394k, 1.2M, 18M, 20M; the long ones not inspected, maybe a pile drifted onto the midline).
- 1300 vs 1100: bigger wins 16/16, 30k-36k ticks.
- 1600 vs 800: 8/8, 12-14k. Reversed (800 vs 1600): 8/8 for the 1600.
- So equal piles are an unstable balance (rich get richer), not a fair game. Under a fair (martingale) game 1300 would win ~54%.
- Flux, first 4,000 ticks, 1600 vs 800: chips taken from the big pile land on the small one 7% of the time; chips from the small pile land on the big one 25%. Picks are in ratio ~1.46 (about sqrt 2, perimeter). The escape asymmetry (3.5x) is what makes it rigged.
- Jump length, 1300 vs 1100: jump 5 -> big wins 15/16 but median ~305k ticks; jump 20 -> 16/16 at ~32k; jump 60 -> 9/7, 1.3M-20M ticks (but on a 128 board a 60-step jump carries chips straight across the 64-cell gap: cross fractions 61%/66%, so geometry confounds it); jump 200 -> nothing settled in 20M.

Open: why is jump ~ pile radius the most rigged (escape probability vs R/jump)? Exact return-probability model for a random walker released 20 steps off a disc. Fix the jump-60 geometry (diagonal placement, bigger board). Long equal-duel tails. Probably known in spirit (StarLogo literature talks about piles only dying); the duel numbers are mine.
