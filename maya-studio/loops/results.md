# Langton's loops: body vs genome (13 Nov 2026, 12:40 AM session)

Rule table and seed: Golly's Langtons-Loops.rule / Langtons-Loops.rle (fetched from the AlephAlpha/golly mirror). `langton.py` runs it with numpy; rebuilt canonical loop matches Golly's seed cell for cell, and it doubles every ~150 steps (1, 2, 4, 8, 15, 25, 39, 58, 84 pieces by step 1200).

Genome read upstream from the junction: (7 0 1)^s (4 0 1)^2, padded with 1s, on a core ring of side L. Canonical: L=8, s=6.

## 1. The genome sets the child's size, not the body (`size_sweep.py`, `sweep_1500.txt`)

All L 5..16, every s that fits, arm L-3, 1500 steps. Whenever s+2 != L the parent builds exactly one child of side s+2, which never detaches; the pair then freezes (live cells constant to t=3000, `long_check.txt`):
- body 8, genome 5 -> one 7-loop, stuck
- body 8, genome 7 -> one 9-loop, stuck
- body 12, genome 8 -> one 10-loop, stuck
- body 10, genome 10 -> one 12-loop, stuck
Only s = L-2 breeds on. L=6 and L=7 fail even when matched.

## 2. Matched colonies are tidy at every third size (`long_check*.txt`)

Share of enclosed holes that are proper same-size loops (rest = debris, mangled or odd-sized loops), at t=3000 (L 8-16) or t=5000 (L 17-23):

| L | s | clean share |
|---|---|---|
| 8 | 6 | 655/655 = 1.00 |
| 9 | 7 | 47/580 = 0.08 |
| 10 | 8 | 1/99 = 0.01 |
| 11 | 9 | 164/200 = 0.82 |
| 12 | 10 | 16/148 = 0.11 |
| 13 | 11 | 28/134 = 0.21 |
| 14 | 12 | 58/109 = 0.53 |
| 15 | 13 | 22/179 = 0.12 |
| 16 | 14 | 22/82 = 0.27 |
| 17 | 15 | 134/212 = 0.63 |
| 18 | 16 | 17/295 = 0.06 |
| 19 | 17 | 24/183 = 0.13 |
| 20 | 18 | 82/172 = 0.48 |
| 21 | 19 | 52/266 = 0.20 |
| 22 | 20 | 7/69 = 0.10 |
| 23 | 21 | 55/115 = 0.48 |

L = 8, 11, 14, 17, 20, 23 (straight genes 6, 9, 12, 15, 18, 21: multiples of three) are the six cleanest; the best of the rest is 0.27. ASCII look at L=9 vs L=11 at t=1500: both form a lattice; L=11 has a few 5/6 debris spots, L=9 has runaway arms (long 7-0 trails shooting off) and 4/5 junk patches. Cause not tested yet.

`colony_gallery.png`: top row L = 8, 11, 14; bottom row L = 9, 10, 12; all at step 2500.

## 3. Correction (13 Nov, 3:40 AM session): section 2 was mostly my founder's fault

`offsets.py` (lone founder, closed holes along its row). Descendants always sit on a square lattice of spacing L+3, and their arm is always 5 cells, whatever L is. My `build()` founders had arm L-3, so the founder's first child landed at 2L-5, i.e. L-8 cells off the lattice, and for L >= 9 the founder never made a second child within the run (`offsets_armLminus3.txt`). With arm 5 every founder is on-lattice and breeds normally (`offsets_arm5.txt`). The founder's offset L-8 is a multiple of 3 exactly for L = 8, 11, 14, 17, 20, 23: the old "tidy" set.

`colony_arm5.py` -> `colony_arm5.txt`: same census, founder arm 5 (t=3000 for L 8-16, t=5000 for L 17-23, same grids as before):

| L | clean share | | L | clean share |
|---|---|---|---|---|
| 8 | 655/655 = 1.00 | | 16 | 105/105 = 1.00 |
| 9 | 56/943 = 0.06 | | 17 | 295/295 = 1.00 |
| 10 | 345/345 = 1.00 | | 18 | 55/606 = 0.09 |
| 11 | 295/295 = 1.00 | | 19 | 249/249 = 1.00 |
| 12 | 34/538 = 0.06 | | 20 | 207/207 = 1.00 |
| 13 | 169/169 = 1.00 | | 21 | 49/328 = 0.15 |
| 14 | 158/168 = 0.94 | | 22 | 169/169 = 1.00 |
| 15 | 29/295 = 0.10 | | 23 | 135/135 = 1.00 |

So there is still a period-3 rule, but the other way round: two sizes in three are spotless, and the messy third is L divisible by 3 (9, 12, 15, 18, 21; straight genes 7, 10, 13, 16, 19). Those sizes were messy with the old founder too, so they are messy on their own; the old founder additionally spoiled L = 10, 13, 16, 19, 22 (offset not a multiple of 3) and only dented 11, 14, 17, 20, 23 (offset a multiple of 3).

For L = 3k the padding of 1s after the genome is L-4, which is 2 mod 3, and the ring perimeter 4(L-1) is 2 mod 3. Mechanism not found yet. `first_debris.py` (lasting odd holes) is crude: it flags transient founder holes (L=12 at t=196) and edge wrap (L=10 at t=2860), and crashes printing far-back frames. For L=9 it did catch a real one by t=504: two neighbours' arms meet in the 1-cell gap between loops and leave a 6 with a run of 7s (`first_debris_9.txt`).

`colony_gallery_v2.png` (founder arm 5, step 2500): top row L = 9, 10, 11, bottom row 12, 13, 14. Left column is the divisible-by-3 sizes. Checked numerically: share of debris states 5 and 6 per tile is 0.45% / 0.41% (L=9) and 0.35% / 0.28% (L=12), versus 0.00-0.01% for the other four.

## 4. Why L = 3k breaks: the child's arm lands on a 0 (14 Nov, 12:40 PM session)

- From a single founder (arm 5, 400x400, no wrap), L = 3k makes a lasting 2-cell hole at (2, L) from the founder's corner: L=9 t=504, L=12 t=690, L=15 t=876 (`first_hole.py`). Other L don't.
- Cause (`hit_parent.py`, frames in hp9.txt..hp12.txt): the founder's east child sends an arm back west along the shared top row. It reaches the 1-cell gap at t = 62L - 60. If the founder's top-right core cell holds 0 at that step, the arm's 7s pour into the founder's ring (more than half the ring is 7s 40 steps later) and the mess leaves the hole. If it holds 1 or 7, the two rings join and the founder keeps cycling.
- Undisturbed colonies land on 7 (L = 2 mod 3), 0 (L = 0 mod 3), 1 (L = 1 mod 3).
- Causal test (`freeze_shift.py` -> `freeze_shift.txt`): freeze everything left of the gap for k = 0..5 steps before the landing (gap column empty throughout, all 84 runs), L = 8..21. Landing on 0: flooded 28/28, hole 28/28. Landing on 1 or 7: flooded 0/56, hole 0/56. So any size can be broken or rescued by a 1- or 2-step delay.
- `phase_shift.py` (rolling the founder's ring) is confounded by the founder's outgoing arm; ignore except as a warning.
- Picture: `landing_on_zero.png` (`render_landing.py`).
