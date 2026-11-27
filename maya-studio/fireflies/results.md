# Fireflies: choirs vs unison (2026-11-13, 12:40 PM session)

Model (`firefly.py`): 400 fireflies on fixed random perches in the unit square. Phase grows at rate 1 + N(0, 0.02); at phase 1 a firefly flashes and resets to 0. Each firefly that listens to the flasher gets phase *= (1 + eps); reaching 1 makes it flash in the same instant (cascade). Multiplicative nudge = just-flashed fireflies are deaf. dt = 0.002, 200 periods. "Synced" = order parameter r > 0.95 from each firefly's last flash.

## Coupling sweep (`sweep2.py`, 3 seeds, 200 periods)
- eps 0.01: nobody syncs (r 0.04-0.27), local coherence ~0.6-0.7.
- eps 0.02: r 0.06-0.80, local ~0.85-0.9.
- eps 0.04: sectors 3/3 synced, count 1/3, metric 0/3.
- eps 0.08: all synced.

## 12 seeds (`sweep_12seeds.txt`, `sweep3.py`), eps 0.03 unless noted
| rule | links/ff | synced |
|---|---|---|
| count 7 | 7 | 0/12 (eps 0.04: 2/12) |
| metric R=sqrt(7/(pi n)) | ~6.8 | 0/12 (eps 0.04: 0/12) |
| sectors (nearest in each of 6 directions) | 5.7 | 9/12 (eps 0.04: 12/12) |
| random_near (same number as sectors, random within sectors' longest link) | 5.6 | 1/12 |
| sectors_capped (drop links longer than 7th-nearest distance) | 4.2 | 0/12 |
| count 5 / 8 / 9 / 10 / 12 | | 0 / 4 / 9 / 12 / 12 of 12 |
| glance (7 nearest + one random hearer per flash) | 7+1 | 12/12 |

Random_near links are LONGER on average (0.070 vs 0.060) yet it fails: the every-side promise matters, not reach. Count-K needs about 9 neighbours to match six-directions with 5.7. One random long-range hearer per flash beats one more near neighbour (glance 12/12 vs count 8 4/12).

## The unsynced state is choirs (`choirs.py`)
Count 7, eps 0.03: the forest splits into 3-11 choirs (>= 5 fireflies flashing in the same instant), each mostly one spatial patch; biggest choir 89-217 of 400. Choirs keep their offsets; snapshot r in 1000-period runs (`longrun.py`) keeps wandering (0.1-0.96), never settles.
Sectors, eps 0.03: one main choir of 365-400 in 10 of 12 seeds (seed 2: 241 + 94 + smaller).

## Session 2 (2026-11-13, 3:40 PM): edges and seams
Outputs in `torus_out/`.
- Torus (`torus.py`, cKDTree boxsize, minimum-image sectors), eps 0.03, 12 seeds: count-7 still 0/12 synced, 5-12 choirs; six-directions 11/12 (square 9/12); count 9 12/12 (square 9/12); count 10 12/12 both. The edge costs a little, but it doesn't make the choirs.
- Topology (`twist.py`, 20x20 nearest-firefly phase grid; vortices from plaquette circulation, windings on the torus): many choir states have no vortex and no winding (square seeds 0, 1, 7; torus 0, 4, 7, 8). So choirs are not held by twists in general.
- Seams (`borders.py`, `borders_baseline.py`): keep count-7's choir split and count links that cross a choir border. Count-7 links: 7.8% cross (mean of 12). Six-direction links on the same perches and same split: 15.2%. Count-12: 13.3%. Fair baseline: random Voronoi patches with the same number of choirs give count-7/six-dir ratio 0.87 (0.84-0.89); the real choir borders give 0.50 (0.35-0.59), every seed below 0.6. Six-dir crossing at real borders 0.152 vs random patches 0.158 = ordinary lines for six-dir; count-7 crossing 0.078 vs 0.136 random = seams. The choirs settle along the thin places of the 7-nearest web (mutual links: count-7 0.82 vs six-dir 0.65, i.e. cliquey).
- Picture `choir_seams.png` (seed 0): choirs coloured, border-crossing links red. Left count-7: 91 crossing links (3.3%); right six-dir on the same split: 155 (6.8%). Checked by pixel count, not by eye.

## Session 3 (2026-11-13, 6:40 PM): fault lines, cause not effect
`cause.py`, `length_control.py`, outputs `cause_out/`. 4 perch sets x 8 runs, count-7, eps 0.03.
- New phases only: lift P(border in b | border in a)/P(border) = 9.36, 5.51, 8.94, 12.85 (random Voronoi patches 1.20, 1.30, 1.26, 1.23).
- New phases and rates: lift 3.61, 3.26, 3.37, 5.16 (patches 1.25, 1.43, 1.19, 1.28).
- Links sharing <= 2 neighbours (symmetrised 7-NN): border freq 0.18-0.32; sharing >= 5: 0.01-0.04. Within-length-quartile rho -0.17 to -0.41.
- Top 10% by few-shared carry 0.34-0.44 of crossings; by spectral distance 0.26-0.43; by length 0.19-0.25.
- Whole partition: spectral k-means ARI 0.20-0.37, random patches 0.11-0.28, run vs run 0.19-0.65.
- `fault_map_p2.png` (perch 2, both): 125/2800 links border in >= 50% of runs.

## Picture
`forest_waves_vs_unison_s0.gif` (seed 0, eps 0.03, last 4 periods, 200 frames): left count-7 (r 0.62; two big choirs of 217 and 154 that flash about three quarters of a period apart, plus three small ones), right six-directions (r 0.99; 397 of 400 in one instant). Checked numerically (`check_wave.py`), not by eye.
