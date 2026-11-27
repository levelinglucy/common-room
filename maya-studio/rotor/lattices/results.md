# Rotors on other grids: results (20 Nov 2026, 6:40 AM session)

`rl.c` / `rl2` (rl2 adds running centre of mass and gap about it, cols 8-10). Lattices: 0 square N-E-S-W, 1 square N-S-E-W, 2 triangular (6 dirs, axial), 3 honeycomb (brick wall, bond length 1). Modes: 0 all arrows at direction 0, 1 random, 2 IDLA, 3/4 honeycomb with B sites starting 1/2 turns on. 200,000 walkers, 8 in parallel ~75 s.

## Gap measured from the start site (what rotor_discs.png used)
max/mean for n >= 1000: square 1.63/1.49, square NSEW 1.86/1.71, triangle 2.24/2.09, honeycomb 0.86/0.67 (ordered); random 2.10/1.45, 1.74/1.31, 2.72/2.12, 1.80/1.30; IDLA 6.67, 5.75, 6.07, 7.21 max.

## The catch: ordered discs are off-centre
Edge radius vs angle for square-north is a clean sine of amplitude ~0.7 about the start site. Centre of mass at 200k:
- square N-E-S-W: (+0.495, -0.492); predicted (+1/2, -1/2), a cell corner
- square checkerboard N/E (old 300k run): (+0.003, -0.496); predicted (0, -1/2)
- square N-S-E-W: (+0.276, -0.717); predicted (+1/4, -3/4) (off 0.04; k mod 4 not uniform for this order?)
- triangle: (-0.495, -0.862); predicted (-1/2, -sqrt3/2) = the neighbour site (0,-1)
- honeycomb A up/B down: (+0.002, 0.000); predicted (0,0)
- honeycomb B +1: (+0.434, -0.247); predicted (0.433, -0.25), mid-bond
- honeycomb B +2: (+0.003, -0.497); predicted (0, -0.5)
- every random start: within 0.003 of (0,0)

Prediction rule: sum of settled positions = sum of all steps = sum over sites of the part-turn left over (full cycles of directions sum to zero). A site with k leftover departures adds e_1 + ... + e_k (the k directions after its start arrow). If k is uniform mod d, the centre is (1/d) sum_{k=0}^{d-1} (e_1+...+e_k), averaged over sublattices. Random arrows average this to zero.

## Gap about the centre of mass (n >= 1000, max / mean / final)
- ordered: square 0.41/0.27/0.13, square NSEW 0.55/0.33/0.34, triangle 0.51/0.37/0.40, honeycomb 0.86/0.67/0.75
- random: square 2.09/1.46/1.63, NSEW 1.74/1.32/1.32, triangle 2.70/2.11/2.38, honeycomb 1.80/1.30/1.54
- checkerboard (old run, final): 1.00
So arrows that start alike give discs 3-10x smoother than random arrows. rotor_discs.png (shared earlier today) said random was as round as ordered: WRONG, an artefact of measuring from the start site.

## Steps vs sum |x|^2
All rotor runs within ~1e-4 (e.g. square 6.36573e9 vs 6.36629e9); IDLA 0.2% over. Holds on all three grids.

## Scored
1. wrong: triangle is the roughest grid from the start site, and about the same as square from the centre.
2. wrong the other way: honeycomb ordered is the roundest from the start site (because its centre is the start site).
3. right-ish: NSEW is a disc, similar gap.
4. right: IDLA 5.3-7.2 on all.
5. right.
Best result: the off-centre shift, predicted exactly by part-turn bookkeeping, and the correction it forces.

Picture: off_centre.png (sine, gaps about centre vs radius, centre table). 51 texts, 1 overlap flagged = out-of-limits tick label false positive.

## 500,000 walkers (ordered starts)
Gap from start site: square 1.62, triangle 2.26, honeycomb 0.90. Triangle centre (-0.495, -0.867), gap about centre 0.374. Honeycomb centre (-0.001, -0.002), gap 0.897 (honeycomb's floor seems higher; why?). Square run had no dump.
