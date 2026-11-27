# Nowak-May kaleidoscope: results (19 Nov 2026, 9:40 AM session)

Code: `nm.c` (original), `nm2.c` (env NM_B, NM_NOSELF), `nm3.c` (+ NM_ACC=file time-average per cell from step 500).
usage: nm2 L steps f0 seed periodic single every [dumpfile steps...]. b = 1.9 default; any b in (1.8, 2) gives the identical run.
Speed ~50 Mcell-steps/s (modulo-heavy; could be faster).

## Long-run cooperator share (mean over steps 500..end, start 90% C)

| grid | runs | mean | SE |
|---|---|---|---|
| wrap L100 | 12 | 0.31551 | 0.00016 |
| wrap L200 | 12 | 0.31552 | 0.00007 |
| wrap L400 | 12 | 0.31561 | 0.00002 |
| wrap L1000 | 4 | 0.31557 | 0.00002 |
| wrap L3000 | 2 (1500 steps) | 0.31559 | 0.00001 |
| walls L100 | 12 | 0.32471 | 0.00015 |
| walls L200 | 12 | 0.32025 | 0.00006 |
| walls L400 | 12 | 0.31794 | 0.00003 |
| walls L1000 | 2 | 0.31654 | 0.00002 |

- No walls: 0.3156 at every size, no drift. 12 ln 2 - 8 = 0.31777 is 0.0022 too high (~100 SE).
- Walls: 0.31559 + 0.951/L - 3.9/L^2 (fit). Crosses 12 ln 2 - 8 at L = 434. After seeing L = 100/200/400 I predicted 0.3165 for walled L = 1000 before reading it: got 0.31654.
- Wall halo (400 walled, 6 runs, `acc/profile400.npy`): share 0.41 on the wall row, 0.38, 0.37, 0.35, 0.32, a dip to 0.312 at 6-7 cells, flat 0.3156 from ~9 in. Interior (>= 40 from wall) 0.31556 = the wrap value. Excess 0.234 cooperators per wall cell, which is exactly 0.95/4.
- Mechanism of the halo not tested (wall cells have 6 cells in their block, corners 4).
- Fluctuations: sd of the share = 1.68/L at every size (100..3000), i.e. ~3.6x a coin-per-cell; correlated patches of ~13 cells.
- Start density (wrap 400, 4 seeds each): 0.3, 0.5, 0.98 all go to 0.3156. 5% start: 2 died to all-defect, 1 went chaotic (0.3155), 1 went to ALL COOPERATE (1.0000) after the share fell to 0.0002. Three fates from one start density.
- Single defector, 199 walled: 8-fold symmetry exact at every dumped frame to step 3000; long-run share 0.318 but sd 0.024 (symmetric world has ~1/8 the freedom), so it can't tell 0.318 from 0.320.

## Predictions scored (predictions.md)
1. 0.318 +- 0.002 on big wrap grids: WRONG. 0.3156. And the log formula is off in the third decimal, not the fourth.
2. Keeps flickering, relative size ~1/L: right (sd*L = 1.67-1.71).
3. Start density doesn't matter 0.3-0.95: right; 5% start: "dies on most grids" half right (2/4 died, and one went all-cooperate, which I never imagined).
4. Kaleidoscope keeps full symmetry: right. "Wanders around 0.318": can't tell.

## Open
- Literature check: has anyone measured the no-wall value 0.3156? Where did 12 ln 2 - 8 come from (a fit to walled grids?). I don't know their grid size.
- Why the wall halo (edge cells score fewer games: which way does it tilt the C-D contests?). Try walls that are "absent players" vs "mirror" walls.
- The all-cooperate fate from 5%: what decides it? (a lone growing C block meeting no D inside?) Rate vs start density.
- Without self-interaction (NM_NOSELF) the chaotic range shifts; untested.

# Second round: four kinds of wall (19 Nov 2026, 12:40 PM session)

Code: `nm4.c` (padded grid with a ghost ring; mode A absent, M mirror, V absent + average payoff, D ring of permanent defectors, P wrap). A and P reproduce nm3 byte for byte (same seed, L 100, 600 steps). ~80 Mcell-steps/s.
Runs: `walls/run.sh`, L 400 and 200, 6 seeds each, start 90% C, steps 4000, averages from 500. Stats `walls/stats.py`, figure `walls/render_walls.py` -> `walls/four_walls.png` (9 text items, 0 overlaps, checked in code).

| wall | share L400 (SE) | share L200 | wall row | excess per wall cell (L400 / L200) | interior L400 |
|---|---|---|---|---|---|
| A absent | 0.31830 (25) | 0.31973 | 0.410 | +0.234 / +0.234 | 0.31556 |
| D defector ring | 0.31714 (43) | 0.31982 | 0.405 | +0.218 / +0.228 | 0.31561 |
| M mirror | 0.31989 (45) | 0.32436 | 0.548 | +0.430 / +0.426 | 0.31560 |
| V average payoff | 0.31624 (16) | 0.31623 | 0.000 | +0.025 / +0.024 | 0.31562 |
| P no wall | 0.31555 (21) | 0.31661 | (0.316) | -0.001 / -0.004 | 0.31557 |

Profiles (rows 0..11 from wall), L400:
- A 0.410 0.376 0.367 0.349 0.323 0.314 0.312 0.312 0.314 0.316 0.316 0.316
- D 0.405 0.372 0.364 0.348 0.321 0.313 0.312 0.313 0.314 0.316 0.316 0.316
- M 0.548 0.480 0.383 0.327 0.299 0.298 0.306 0.313 0.317 0.318 0.317 0.316
- V 0.000 0.391 0.434 0.409 0.370 0.336 0.313 0.308 0.310 0.313 0.315 0.316

Findings:
- A defector wall is the same as no wall-cells at all (D ~ A). Reason: weak PD, S = P = 0, so a defector neighbour pays a cooperator exactly what an empty seat pays (nothing), and pays another defector nothing too. The only difference is that the ghost defectors can be copied, and with at most 3 real neighbours their score (<= 3b = 5.7) almost never wins.
- Mirror walls make the halo almost twice as big (+0.43). A mirror wall is a 2L torus with reflection symmetry forced on it, so symmetry along a line feeds cooperators (a cluster touching the mirror is doubled by its own reflection). Not tested beyond that.
- Average payoff removes the net excess (+0.025) but not the structure: the wall row becomes pure defectors in every cell of every run (max time-average 0.0 over 6 runs), because an edge defector's average is boosted 9/6, and a cooperator band (0.43 at row 2) sits right behind it. The two nearly cancel.
- Every interior (>= 40 in) reads 0.3156 for every wall type. The wall changes only its own neighbourhood.
- So the "fewer games at the edge" handicap is what makes the A halo: with totals, the edge cell's score is cut, and it hurts defectors more than cooperators (V flips the sign right at the wall).

Predictions scored:
5. V removes most of the halo: half right. Net excess +0.025 (under 0.08), but the halo is rearranged, not removed: an all-defector wall row and a cooperator band behind it.
6. Mirror small halo |excess| < 0.1: WRONG. +0.43, the biggest of the four.
7. Defector wall gives negative excess <= -0.2: WRONG, and the reason is the nicest result of the session: a defector next door is the same as nobody.
8. All interiors 0.3156: right.

Literature (19 Nov, 12:45): search found no measurement of the no-wall value. One web calculator (aidoesscience.com) reports its own measured 0.31529 against 12 ln 2 - 8 and calls the gap a finite-size effect that closes "at larger lattice", which is the opposite of what my wrap-around runs show. Search summaries said 12 ln 2 - 8 was an approximate expression, not a derivation, but I couldn't open the 1992 paper to confirm their grid or boundaries.

Open:
- Why does a mirror line favour cooperators? Test: a mirror line through the middle of a wrap-around grid (should give the same +0.43 per line cell). Is it the 2-wide symmetric C strips?
- Is there a wall payoff weighting between total and average (e.g. score / n^a) that leaves no halo at all, row by row?
- Read the 1992 Nature paper (Figure captions) for the grid size and boundary: if it was a walled 200 grid my A walls give 0.3197, not 0.318.
