# The ant on scribbled ground (18 Nov 2026, 3:40 AM session)

Langton's ant (white: right, black: left, flip, step), facing up. Ground scribbled at random
(each cell black with probability p) before it starts. Highway = 104-step displacement a fixed
(+-2, +-2). Predictions in predictions.md were written before any run.

## 1. Scribbled disc of radius R, clean beyond (ant.c, runs/, summarise.py)

400 seeds per (R, p), R = 10..160, p = 0.02..0.98. Clean ant onset 9,976 (matches the known ~10,000).
- Every one of 22,010 runs found a highway (prediction 2 right).
- Highway starts just outside the disc (mean radius at onset ~ R + 17 for R = 160).
- Directions uniform over the four diagonals (prediction 5 right, ~100 each of 400).
- Prediction 4 WRONG, backwards: onset is shortest at p = 0.3-0.5 and longest at the extremes.
  R = 160 medians: p 0.02: 416,225; 0.05: 337,975; 0.3: 69,993; 0.5: 78,486; 0.95: 265,783; 0.98: 340,620.
- Prediction 3 half right: x4 per doubling holds only at the extremes (0.02: 79k -> 416k from R 80 to 160);
  at p = 0.5 it is x2.3 (33k -> 78k).

## 2. Endless scribbled plane (plane.c, plane_runs/, plane_summary.txt; plane2.c, diag/)

Fill radius 1900 on a 4096 grid; first time the ant gets r = 20..1280 out. 200 seeds per p
(50 at 0.01, 40 at 0.005 from diag/).
Median steps to r = 1280: 0.005: 4.4M; 0.01: 37.8M; 0.02: 139.8M; 0.05: 77.7M; 0.1: 11.9M;
0.2: 2.5M; 0.3: 1.36M; 0.5: 0.87M. 0.98 (mirror of 0.02): 141.8M, same as 0.02 (check passed:
inside the scribble, p and 1-p are mirror images).
Growth per doubling of r (160 -> 1280): p >= 0.3: time x4 (exponent ~2.0, diffusive);
p = 0.02-0.05: x7-8.6 (exponent 2.7-3.1).

Why (diag/, 40 seeds each):
- p = 0.005: longest highway median 5,277 steps (~100 cells); touches 6.6% of the disc of
  radius 1280. It flies: short highways between dots.
- p = 0.02: longest highway median 1,632 steps (~31 cells), only 15% of runs ever hold one
  2,000 steps; touches 42% of the disc. It fills: highways die on dots and it paints a solid blob,
  and a solid blob has to be repainted to grow (time ~ r^3).
- p = 0.3-0.5: longest 'highway' 22-24 steps (none at all); touches ~5% of the disc. It wanders: a
  thin random-walk trail, time ~ r^2.
- Inside everything the ant touched, the ground ends up 50% black at every p (0.500-0.512).

## 3. Solid black disc (solid_disc.py)

Inside, the ant is the mirror of the clean ant: highway at exactly step 9,976, direction (2,2)
instead of the clean (-2,2). It runs to the disc's edge and crashes (prediction 6 right). Then a
new highway turned a right angle, (2,-2), and leaves: after 2,041 steps of chaos at R = 80, after
3,356 at R = 160. Only these two sizes tried.

## Picture

three_ways_out.png (render.py): footprints at first reaching r = 200 for p = 0.005, 0.02, 0.5
(median-time seed of 9: seeds 5, 1, 6; 85,444 / 479,715 / 27,762 steps), plus the escape-time
chart. Checked programmatically: 32 texts, 0 overlaps or out of bounds; visited-cell counts in the
raw windows match the totals (10,799 / 34,989 / 9,797). Not looked at by eye.

Not checked: whether this is in the literature (Langton's ant on random backgrounds has been
studied; I didn't look). Don't claim it's new.
