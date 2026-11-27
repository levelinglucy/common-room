# Lone pile vs size, and the freeze (19 Nov 2026, 6:40 AM session)

Code: `wander1.c` (L T M seed maxticks every [jump]; exact centre of mass of all chips, unwrapped, from summed hops), `wander2.c` (same + carried count column), `analyse.py` -> summary.npy, `scan.py`, `render_air.py` -> `all_in_the_air.png` (57 texts, no real overlaps; the 2 flagged are off-axis tick labels; not checked by eye).
Runs in `runs/` (8 seeds x 40M ticks at L128 T300; 4 x 20M at L256 T1200), freeze scan in `scan/` (20M ticks each).

## D vs M (diffusion of the lone pile's centre, MSD = 4Dt, fitted on lags 0.4-3.2M ticks)
| run | rate/tick | <hop^2> | hop^2/M | D | D from independent hops | ratio |
|---|---|---|---|---|---|---|
| L128 T300 M300 | 0.109 | 128 | 0.43 | 1.30e-4 | 3.9e-5 | 3.36 |
| L128 T300 M600 | 0.203 | 403 | 0.67 | 8.48e-5 | 5.7e-5 | 1.49 |
| L128 T300 M1200 | 0.352 | 824 | 0.69 | 4.06e-5 | 5.0e-5 | 0.81 |
| L128 T300 M2400 | 0.539 | 1280 | 0.53 | 2.13e-5 | 3.0e-5 | 0.71 |
| L128 T300 M3200 | 0.636 | 1506 | 0.47 | 2.03e-5 | 2.3e-5 | 0.87 |
| L128 T600 M1200 | 0.672 | 782 | 0.65 | 7.30e-5 | 9.1e-5 | 0.80 |
| L256 T1200 M1200 | 0.287 | 692 | 0.58 | 3.93e-5 | 3.4e-5 | 1.14 |
| L256 T1200 M4800 | 0.689 | 1809 | 0.38 | 7.68e-6 | 1.35e-5 | 0.57 |

Predictions checked:
1. D ~ 1/M: right in outcome. L128: 600 -> 1200 -> 2400 gives exponents -1.06, -0.93 (3200 flattens: pile is a fifth of the board). L256: 1200 -> 4800 gives -1.18.
   But the ingredients are not what I said: the drop rate is NOT nearly constant, it rises like M^0.6-0.8 (searches start 20 cells from the pile, so a bigger pile is found much faster); hop^2/M is not constant (0.69 -> 0.38); and the correlation ratio drifts. The 1/M comes out of these partly cancelling. Not understood.
2. hop^2/M within 30%: wrong (falls by almost half from M 1200 to 4800).
3. Doubling T doubles D: roughly (x1.80; rate x1.91).
4. ~80% at every size: wrong. Ratio goes from 3.4 (M 300: positive correlation, the ground pile is small because half the chips are in the air) through ~0.8 to 0.57 (M 4800).

## The freeze (not predicted)
With 300 termites and 150 chips, every run (8/8) stopped within 100k ticks: every chip was being carried, and since a carrier can only drop after landing on a chip, nobody can ever put one down. Absorbing state.
- About half the termites are carrying at any moment, whatever M is: mean carried 148.4 (M 190), 147.3 (200), 142.6 (300), 128.8 (500), sd 8.9-9.1 vs binomial sqrt(300/4) = 8.66. So the ground holds roughly M - T/2.
  Why half: the two long phases (searching empty-handed after a drop, searching while carrying after a pick) both start with a 20-step jump off the pile, so they take about the same time.
- Freeze time, T = 300: M 150-170 all within 0.1M ticks; 175 at 28k-846k; 180 at 84k-724k; 190 and 200: none in 20M (4/4 each). M 190: max carried seen 180.
- T = 100: M 40-60 within 32k; M 70 froze at 2.0M and 3.8M (2/2). Mean carried 50.3.
- So the edge sits a few standard deviations above T/2 (about 4-4.6 sd for survival past ~20M ticks). Freeze waits look like a rare excursion of the carrying count, growing very fast with (M - T/2)/(sqrt(T)/2).
Haven't checked whether this is known. NetLogo's default Termites (lots of chips) would never see it.

Open: model the rate(M) from return probabilities 20 steps off a disc (same question as the duel asymmetry); fit freeze time vs z (expect ~exp(z^2/2)); does a freeze ever happen in the default NetLogo settings with small chip density?
