# Evoloop: the loops that evolved small (13 Nov 2026, 9:40 PM session)

Rule: Golly's Evoloop.rule (Sayama 1999), fetched from the AlephAlpha/golly mirror into ../loops/. `evoloop.py` expands the @TABLE (variables bound per line, rotate4, first match wins, unmatched cells keep their state) into a 9^5 lookup. Check: it agrees with the file's own @TREE on all 59,049 entries (Golly tree order for von Neumann: N W E S C). Seed: Golly's Evoloop.rle (inner space 11x11, core ring side 15).

Size here = side of the square empty hole inside the loop ("inner space"). Ancestor = 11.

## 1. Three tori, same story (`census.py`, out/torus_*.json/.log)

One ancestor, empty torus, 150,000 steps, census every 1,000.

- 400x400: 11s fill the world (49 at 10k), then 8-10s and 5s (20k), then 3s (223 at 30k), then 2s take over: 372 at 100k, 355 at 150k, 3s nearly gone.
- 500x500: 11s (75 at 10k), 7s dominate at 20k (79), then 3-5s at 30k, then 2s: 516 at 150k (+11 threes).
- 600x600: 11s (132 at 10k), 8-11s at 20k, 3s at 30k (296), 2s from 40k on: 761 at 150k (+22 threes).
- No loop with a 1x1 inner space anywhere in the final worlds (no 0 cell fully ringed by sheath). 2 is the floor.

## 2. Small breeds faster (alone.py, out/alone_600.txt, founder runs)

Loops cut out of the 600 world and run alone on an empty torus:
- inner 8: 7 loops at step 1,000, 19 at 1,500 (240 torus)
- inner 10: 4 at 1,000, 12 at 1,500
- inner 11 (ancestor): 4 at 1,000, 9 at 1,500
- inner 12: 4 at 1,000, 7 at 1,500
- inner 2 (founder from the 400 world, 200 torus): counts every 100 steps 1,1,2,4,8,6,10,11,19,38,23,29,37. So 19 by step 800; doubling about every 100 steps once going; the colony crowds and crashes/recovers on a 200 torus.

## 3. Most tiny loops can't start a colony alone, and it isn't their genes (`alone2.py`, `genomes.py`)

- 40 inner-2 loops cut from the 400 world: 14 made a child, only 5 had a growing colony after 1,500 steps (pad 0); with 3 cells of margin, 7/40.
- Genome tape (states round the core ring): 76 of 80 sampled carry the same tape, 4 straight genes (7) and 2 turns (4), cyclic `01170117017014014017`. Of those 76 identical tapes, 15 grow alone, 61 don't. All 15 fertile ones end at exactly 37 loops (same outcome).
- A colony grown from one fertile founder (37 loops at step 1,200, all one family): cut out at that moment, 0 of 37 can start a colony alone.
- Reading: fertility alone depends on the moment in the loop's cycle when it's cut (a whole family is in step, so they're all fertile or all not). Failed case watched cell by cell: the child is built flush against the parent with no gap, then a dissolving signal (state 8) appears at the join and both go within ~30 steps. Fertile case: arm reaches out, child forms one cell away, separates.

## Picture

`render_strata.py` -> `evoloop_strata.png`: top, 600 world at steps 5,000 / 25,000 / 50,000 (260x260 zoom, Golly colours); bottom, share of loops at each inner size vs time for all three worlds. Not checked by eye.

## Open

- Why does 2 win over 3 (both fast)? Head-to-head: one 2 and one 3 on the same torus, many phases.
- Why do newborn tiny loops get built flush (no gap) at some phases? Arm length vs genome for inner 2.
- Sayama-style: do the 2s keep mutating (tape variants) or is it a frozen end state? The 4 odd tapes in the sample were all sterile.
- Words as genomes (straight/turn genes from numerology), the old loops idea, now on Evoloop where bad genomes get cleaned up by dissolution.

# 2 vs 3 (14 Nov 2026, 12:40 AM session)

Founders (`founders.py 40`, out/founders_35k.pkl): from the 600 world at step 35,000 (134 twos, 417 threes), each cut with 3 cells margin and run alone 1,500 steps on a 200 torus. Fertile: 1 of 40 twos, 6 of 40 threes. Main 3 tape 011117017014014017017017 (5 straight, 2 turn); main 2 tape 01117017014014017017 (4 straight, 2 turn). Alone, both double about every 150 steps early and saturate near 41-47 loops on a 200 torus: no obvious speed gap.

`race.py` (one founder, or one of each, on an empty torus; single-founder runs vary the torus side 250..340 with `vary`, since rotations alone give identical runs):
- one 3 founder (10 runs, 40k steps): the first 2 appears at step 4,000 in every run (inside the colony, before it wraps, so independent of torus size). 2s pass half the 2+3 population between steps 12,000 and 24,000. End: 2s 88-100%.
- one 2 founder (10 runs, 40k): 3s appear in all 10 runs (first at steps 6,000-21,500), but never exceed 17% of 2s+3s; 7 of 10 end with no 3s at all.
- one of each (10 runs, 300 torus, 30k): 2s win all 10; 3s at 0-12% at the end (4 runs with none).
So it's not a one-way ratchet. Mutation goes both ways, and selection favours 2 in a crowd.

`upward.py`: the 3s born in a 2-only world gain a straight gene: tape 011170170140140170117017 (5 straight, 2 turn, the extra 1-spacer sits elsewhere from the 35k 3s). In the N=300 run at 30k: 19 of 20 threes carry it; 8 of 20 breed alone (all to 42 loops). N=310 at 20k: all 13 threes carry it; 0 of 13 breed alone (the phase effect again). Also in 2-only worlds: 2-tape variants (rearranged gene orders; a few with 3 straight genes or a lost turn gene).

Picture: `race_2v3.png` (share of 2s over time, all runs). Not checked by eye. Not shared.

Open: why does 2 win in a crowd if it doesn't breed faster alone? Candidates: smaller footprint (more loops per area), fewer collisions per birth, or 3s losing a gene in collisions more often than 2s gain one. Next test: count births and deaths per loop by size in a mixed world.
