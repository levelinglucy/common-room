# Nowak-May spatial dilemma: predictions (written before any run, 19 Nov 2026, 9:45 AM)

Model (Nowak & May 1992): square grid, each cell plays the prisoner's dilemma with its 8 neighbours and itself.
Cooperator meeting cooperator gets 1, defector meeting cooperator gets b, everything else 0.
Each step, every cell copies the strategy of the best scorer in its 3x3 block (itself included). Synchronous.
For 1.8 < b < 2 every comparison comes out the same (no fraction m/n with m <= 9, n <= 8 lies in that gap), so the whole run is identical for any b there.

The folklore: from random starts the cooperator share settles near 0.318, and Nowak & May noted 12 ln 2 - 8 = 0.317766.

Predictions:
1. Big periodic grids (L >= 1000) from random 90% cooperators settle at 0.318 +- 0.002. I expect the mean to sit within 0.001 of 0.3178 but I don't believe the log formula is exact; I'd bet the true value differs from 12 ln 2 - 8 in the fourth decimal.
2. The share does not settle to a fixed point: it keeps flickering, with relative fluctuations falling like 1/L.
3. The starting density doesn't matter between 0.3 and 0.95 (same limit), but a very low start (5% cooperators) dies out to all-defect on most grids.
4. One defector in the middle of a cooperator world (odd L, fixed walls) makes a kaleidoscope that keeps the square's full 8-fold symmetry forever (it's deterministic and symmetric), and its cooperator share wanders around the same 0.318 rather than settling somewhere else.

## Second round: why do walls grow cooperators? (written before any run, 19 Nov 2026, 12:50 PM)

Today's walls are "absent players": an edge cell has 6 cells in its block (corner 4), plays fewer games, and has fewer cells to copy from.
Four wall types, all on L = 400, 6 seeds, start 90% C, average steps 500..4000:
- A absent (today's): halo 0.41 on the wall row, +0.234 cooperators per wall cell.
- M mirror: the row beyond the wall is a reflection of the edge row (edge cell's outside neighbours are its own reflected neighbours, scores included).
- V average: absent walls, but each cell scores its AVERAGE payoff per game instead of the total (so edge cells aren't handicapped by playing fewer games; still fewer cells to copy).
- D dead wall: a ring of permanent defectors outside the grid that play and can be copied (score computed as normal from what they see).

Predictions:
5. V removes most of the halo (excess per wall cell under 0.08). My guess at the mechanism: defectors live off the number of cooperators they touch, and an edge defector touches fewer, so it loses contests it would win inside; the edge handicap hurts D more than C.
6. M has a small halo, either sign, |excess| < 0.1 per wall cell: a mirror is the closest thing to no wall.
7. D wall makes a cooperator-poor band: negative excess, at least -0.2 per wall cell, because permanent defectors next to the edge feed on edge cooperators.
8. All four interiors (>= 40 cells in) still read 0.3156: the wall only changes its own neighbourhood.
