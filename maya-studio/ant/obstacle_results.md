# One dot in the road (18 Nov 2026, 6:40 AM session)

Predictions: obstacle_predictions.md (written first). Code: obstacle2.c (singles + pairs), rewind.c (trace one
run, list every highway segment >= 2,080 steps, optional second dot), verify_obstacle.py (independent Python
ant), render_obstacle.py -> one_dot.png.

Clean ant, highway from step 9,976, direction (-2,2) (down-left on screen, y down). The highway touches exactly
22 new cells per 104-step period, so a single dot on its future path has 22 cases (cell classes modulo the
period shift). Dot placed on the cell first visited at T1 + phase, T1 = 30,000.

## Singles (single_T30k.txt; same on G = 8192 at T1 = 30k, 60k, 120k)

- 22/22 break the road (104-step displacement leaves (-2,2) at least once). None is absorbed.
- Heal exactly onto the clean road (last 104 positions = clean ones L steps earlier; Python check matches the
  whole last 3,000 steps): phases 34, 62, 63, 76, lag 32, 20, 120, 132 steps, after 35-310 steps of fuss.
- Same direction, road moved to its right (smaller x+y): phases 5 (-14), 6 (-52), 15 (-16), 20 (-4), 77 (-2).
- Turn right (-2,-2): 0, 1, 7, 16, 78, 81, 87. Turn left (2,2): 2, 64, 94, 95, 96.
- Goes home: phase 17. 51,044 steps of mess at the dot, then a reversed highway (2,-2) for 19,955 steps
  (the outbound one was 20,042), running ~48 cells beside the old road, straight over the start cell, ~8,000
  steps of mess at the nest, then out as (-2,-2). Its total chaos grows with the road: 78,987 / 109,043 /
  169,051 at T1 = 30k / 60k / 120k (about T1 + 49,000). The other 21 are identical at all three T1.
- Phases 2 and 95 (93 steps apart on the road) give exactly the same future: identical positions from step
  30,666 to 180,000 (Python check). 96 does not join them.
- Chaos (onset of final highway minus first touch of the dot): median 4,666 steps (incl. the home trip).

## Pairs (pairs_T30k.txt: every pair of cells first visited in [T1, T1+312), 2,145 runs = 1,199 distinct
arrangements; copies one period apart always agreed)

- None absorbed. Turn left 523, turn right 271, sideways left 150, sideways right 180, same road late 51,
  same road EARLY 2, moved along the same line 11, reversed 11.
- Early: dots at phases (0, 16) and (76, 77): back on the clean road 4 steps ahead of it (Python check:
  same road shape moved by one period at phase lag 100, i.e. lag -4). Lags are always multiples of 4.
- Reversed pairs: either the reverse road misses the nest by 27-44 cells and sails past, or it runs over the
  start cell, stops for ~9,630 steps (8,377 or 6,064 in a few) and leaves in the same reversed direction.

## Predictions scored
1. 10-30% absorbed: WRONG, 0/22 (and 0/1,199 pairs). 4 heal, but only after breaking.
2. All rebuild: right.
3. Median chaos 2,000-6,000: right (4,666).
4. Mostly turns, rarely back: half right. 12/22 turn, 9/22 keep direction, 1/22 goes back (singles).
5. Chirality: singles lean right (7 v 5 turns, all 5 side-steps to the right); pairs lean left (523 v 271).
   No consistent hand.

Not checked: the literature on Langton's ant highways meeting obstacles (it has surely been looked at; don't
claim new). one_dot.png checked programmatically (22 texts, 0 problems); not looked at by eye.
