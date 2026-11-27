# Drummers on a ring (14 Nov 2026, 3:40 PM session)

Question: k drummers on n beat slots of a cycle, each hearing only its j nearest drummers on each side (repulsion 1/d, d = distance round the ring in that direction). One at a time they step one slot into an empty neighbour slot if it lowers what they feel; order round the ring is fixed. Do they find the Euclidean (maximally even) rhythm E(k, n), and how far does each have to listen?

Files: `drummers.py` (model; `python3 drummers.py k n j`), `sweep.py N` -> `sweep_n30.json/.txt` (40 runs per (k, n, j)), `checks.py` -> `checks_output.txt`, `sweep_km.py 20` -> `sweep_km20.json/.txt`, `far_drummer.py` -> `far_drummer.json/.txt`, `twist.py` -> `twist_output.txt`, `twist_exact.py` (dud, see below), `three_defects.py` -> `three_defects_output.txt`.

## Findings
- Target is right: for every (k, n) with n <= 22 (100 pairs), the all-pairs 1/d energy has the Euclidean rhythm as its unique minimum up to rotation (exhaustive).
- Nearest-only (j = 1) rarely finds it once k >= 5: most misses are defect states, some are clumps (gaps all within 1 but the long ones bunched).
- jmin (smallest j with 40/40 hits) depends only on k and m = min(n mod k, k - n mod k), the number of odd gaps: 42 classes for n <= 30, no clashes; 3k + m agrees with 2k + m up to k = 14.
- Table to k = 20: m = 1 and m = 3 -> floor((k+1)/3). m = 2 -> floor(k/2). Even k with even m -> k/2 (everyone hears everyone). m = 5 -> floor((2k+1)/5) for k = 10..20. Odd k, m = 4 -> floor((k+3)/4). m = 6, 7 irregular-looking.
- m = 1 explained exactly: the trap is one squeezed gap (1) and two stretched gaps (3) a third of the ring apart, e.g. k = 29 spacing (10, 9, 10). `three_defects.py` finds the largest j at which such a state is stuck; jmin = that + 1 = floor((k+1)/3) for every k = 6..30 and 36, 42, 48. Sims at k = 24, 30, 36, 42 (n = 2k+1) switch to 40/40 at exactly j/k = 1/3.
- First guess was the Wiley-Strogatz-Girvan twisted states (ring of oscillators, k nearest each side: sync is global only above k/n ~ 0.34, per two search summaries of Chaos 16, 015103, 2006; paper not read). Wrong mechanism here: a plain staircase twist (3s, 2s, 1s, 2s) is only stuck at j = 1 (`twist_exact.py`). The 1/3 is three defects, not a twist. Nice coincidence of numbers, not the same thing.
- One far drummer (the trick that saved the starlings and the fireflies) helps only a little. 12 hard cases x 24 runs, 600 sweeps: j = 1 plain 12/288 end in Euclid, + fixed random friend 25/288, + random glance redrawn every move 70/288 (mean time share in Euclid 0.22). j = 2: 25, 48, 80 /288. Sync is agreeing on one thing; an even rhythm is a pattern at several scales, so it needs a wide ear, not one long link.

Gotcha: `checks.py` labels spread >= 2 with neighbour gaps within 1 as "ramp"; in practice those are the defect states, not staircases.

## 14 Nov, 6:40 PM session: every class explained
- `two_valued.py K` -> `two_valued_k14.txt`, `two_valued_k20.txt/.json`: exhaustive over every rhythm that uses only the two Euclid gap sizes (exactly m minority gaps), up to rotation; largest j at which each non-Euclid one is stuck. For every sim class with m >= 2, k <= 20: worst + 1 = simulated jmin, **117 of 117**. With three_defects (m = 1), every class in the sim table now has its trap. For m >= 2 the worst trap is always just a wrong arrangement of the long gaps; no third gap size needed.
- Even k, even m: Euclid is one half-rhythm played twice. Trap = 'two right halves, out of step': rotate the second half by r within itself. `halves.py 40` -> `halves_output.txt`: some r is non-Euclid and stuck at j = k/2 - 1 in **380 of 380** even-even cases up to k = 40. So jmin >= k/2 there (sims + exhaustive show = k/2 up to k = 20).
- `seam.py` (slide half the minority gaps by one) only reaches k/2 - 1 when m divides k; the halves construction is the right general one. Kept the output (`seam_output.txt`).
- `plateau.py` -> `plateau_output.txt`: total energy vs size of a slid block. Messy, didn't give a clean 'defects don't feel each other' story (energies equal across b in 16/36 but only b = 2 stuck). Not used for claims.
- `render_seam.py` -> `drummers_seam.png`: k = 16, n = 36 (m = 4). Euclid ring, trap ring (joins marked), one band from seed 2 at j = 7 (25 moves, ends in the exact trap 2223222322322232 up to rotation) vs j = 8 (29 moves, Euclid); bottom jmin table. Text overlap / out-of-figure checked programmatically (0), not by eye.

## Open
- ~~Why even k with even m needs everyone~~ (done: halves out of step).
- Closed form for odd-m classes from the two-valued traps (the trap's bead spacings look like a trap one level down the Euclid recursion: e.g. 20/48 trap spacings 3232 2323 = halves out of step at the bead level).
- General formula for jmin(k, m): m = 5 looks like floor((2k+1)/5); is jmin = the defect spacing of the worst trap for each m, related to E(m, k)?
- Sound: render the drummers settling (or getting stuck) as a WAV.
- A picture: the ring over time, j = 1 vs j = k/3, plus the jmin table.

## 14 Nov, 9:40 PM session: the trap is recursive
- `recursion.py`: the worst two-valued trap's odd gaps, read as m beads on k slots, are themselves the bead problem's trap (e.g. 20/48 trap -> beads 22323323 = the (8, 20) trap; whose beads 1232 = a squeeze on (4, 8)). So the trap follows Euclid's recursion (k, n) -> (m, k) -> (m', m) -> ...
- `rtrap.py`: builds candidate traps by that recursion only. Bottom levels: m = 0 squeeze (one gap -1, one +1, any placement); m = 1 three defects (any placement) plus a squeeze on Euclid; 2-3 beads: every placement. Upper levels: place the odd gaps on each bead-level candidate. 1 to 497 candidates per case (mean 45 for k 21-32) instead of exhaustive.
- vs sims k <= 20 (`rtrap_vs_sim.txt`): recursive prediction = simulated jmin in **145 of 145** classes (before adding the 2-3 bead and squeeze-on-Euclid bottoms: 118/145, the misses were all bottoms with no candidates).
- Pre-registered (`rtrap_predictions_k21_32.json/.txt`, made before any sim), all n = 2k + m, k = 21..32, 156 cases. `rtrap_check.py` (60 runs each at pred-1, pred, pred+1) -> `rtrap_check_k21_32.txt`, `rtrap_check.json`: 155/156 held. The one 'fail', k=28 n=70 (m=14, pred 14 = k/2), had 0 misses in 60 runs at j=13; `rare_trap_k28.py` with 4,000 runs at j=13: 314 misses (7.9%), every one exactly the predicted trap 2232323232323233232323232323. So **156/156**. In 146 of the 155 cases with misses at pred-1, the exact stored trap was among them; the rest showed a sibling trap (other placement).
- Sims are fast (k=26 run ~1.6 ms), so the whole check took 11 s on 8 cores.

## Open
- A closed form for jmin from the recursion: roughly J(m, m') bead gaps' worth of drummers (J(k,m) ~ J(m,m') k/m) but the rounding isn't a simple floor/ceil (k=15, m=7: 4.29 -> 5; k=7, m=3: 2.33 -> 2). Maybe the max drummer-span of J(m,m') consecutive bead gaps in the trap itself?
- Picture: the recursion as nested rings (drummers -> beads -> beads of beads), and a WAV of trap vs Euclid.

## 15 Nov, 12:40 AM session: nested rings picture
- `nested_check.py` (k=29, n=70, 200 fresh runs each): j=11 -> 187 trap (exact predicted, mirror-symmetric), 13 Euclid; j=12 -> 200 Euclid.
- Trap vs Euclid aligned: differ only at gaps 16-17 (one drummer one beat off). Levels E: 23232..., 232322323223, 23232, 23; trap: ..., 232323223223, 22332, 14.
- `render_nested.py` -> `nested_rings.png`.
