# Ulam's hidden beat: results (18 Nov 2026, 9:40 PM session)

Tools: `ulam.c` (./ulam a b VMAX, sums counted with a capped byte array, O(terms^2); U(1,2) to 2e6 in 5 s), `spectrum.py` (FFT of the indicator, 4x zero pad, then 3 rounds of fine direct scan), `fold.py` (fold U(1,b) by its own period), `render_beat.py` -> `ulam_beat.png` (40 text items, 0 overlaps checked in code).

U(1,2) check: first 41 terms match the known start 1 2 3 4 6 8 11 13 16 18 26 28 36 38 47 48 53 57 62 69 ...

## U(1,2), 147,960 terms up to 2,000,000
- One frequency: alpha = 2.5714475771, mean cos(alpha u) = -0.7976, clock length 2pi/alpha = 2.44344289.
- The other FFT peaks are all its folded harmonics: 0.2909 (5 alpha), 2.2806 (4 alpha), 2.8623 (6 alpha), 1.1403 (2 alpha), 1.4312 (3 alpha). So guess 1 ('nothing else') was wrong in wording, right in substance.
- Folded: terms > 1000 all land in phases 0.296..0.694 (phase 0 = cos +1). Within 0.296 of phase 0 (59% of the clock): only 9 terms ever, 2 3 8 36 47 69 102 273 339. They cluster: 36/102/273/339 near one edge, 3/8/47/69 near the other, 2 alone.

## Other starts (to 5e5 or 6e5)
- (1,3): alpha 2.8334975, mean cos -0.796, clock 2.21746633.
- (2,3): alpha 1.1650129, mean cos -0.829, clock 5.39323239.
- (3,4): clock 2.84430630, mean cos -0.860. (3,5): clock 3.13399447, mean cos -0.864.
- (2,5) and (2,7): regular. Differences eventually periodic with period 32 and 26, both summing to 126. Spectrum is a comb of equal lines (0.125 and 0.2326), no single spike. (4,7): only a weak line at pi; not examined further.

## The (1,b) family: clock = 3b + 0.41703
| b | clock | clock - 3b | mean cos |
|---|---|---|---|
| 4 | 12.417033 | 0.417033 | -0.8592 |
| 5 | 15.417033 | 0.417033 | -0.8538 |
| 6 | 18.417033 | 0.417033 | -0.8498 |
| 10 | 30.417035 | 0.417035 | -0.8413 |
| 16 | 48.417035 | 0.417035 | -0.8361 |
| 20 | 60.417037 | 0.417037 | -0.8343 |
| 30 | 90.417041 | 0.417041 | -0.8321 |
(all 16 values b = 4..16, 20, 25, 30 in fold.py output; drift in the 6th decimal at big b is fit resolution: fewer clock turns in 6e5.)
- Rigidity seen directly: U(1,b) terms written as A*b + B have the same (A, B) list for b = 10, 11, 12, 20 at the start (0b+1, 1b+0..., 2b-k..., 2b+2, 4b+0, 4b+2, ..., 7b+3, 7b+4, 8b..., 10b+2, 11b+2, 13b+4, 14b..., 16b+2, 17b+2, 19b+3). The A values skip multiples of 3 (except the opening 1).
- Folded shapes converge as b grows: L1 distance to the b = 30 histogram falls 0.169 (b=4) -> 0.043 (b=16) -> 0.025 (b=25). The empty arc for terms > 50b widens 0.615 (b=4) -> 0.660 (b=30); maybe heading to 2/3 (untested guess).

## Known?
Yes, mostly. A search summary (arXiv 2511.13066, Gilson) says Hinman, Kuca, Schlesinger and Sheydvasser showed large initial segments of U(1,n) are described uniformly by finite data depending on n mod some L, which is the rigidity above. Steinerberger 2017 is the hidden signal at 2.5714 (in the same summary). Whether the 3b + 0.41703 clock is written down there: not checked. Treat it as probably known.

## Predictions scorecard
1. single spike at ~2.57, mean cos ~-0.8: right (-0.798); 'nothing else' only true up to harmonics.
2. each (1,b) has one dominant frequency: right, and more: the clock is 3b + 0.41703.
3. (2, odd) regular, comb spectrum: right.
4. folded U(1,2) avoids a big arc: right, 59% of the clock with 9 strays.
5. strays are early: right (largest is 339).

## Open
- What is 0.41703? Does it come out of the A*b + B structure (the B drift per three blocks)?
- Does the empty arc for (1,b) tend to 2/3, and the mean cos to some limit (-0.832 at b = 30, still rising slowly)?
- (1,2) and (1,3) are outside the rigid family: is there a relation between their clocks (2.4434, 2.2175) and the rest?
- A sound version: play U(1,2) as clicks and the hidden clock as a drone? The beat would be audible as a phase lock.

# 19 Nov 2026, 12:40 AM: what 0.41703 is (predictions in predictions_0417.md)

Tools: `blocks.py`, `lattice.py` (big blocks = runs of consecutive terms at least b/3 long; gaps between them as j bars of 3b plus a slip delta), `render_slip.py` -> `ulam_slip.png` (32 texts, 0 overlaps, checked in code; not by eye). New data: u1_10_4M.txt (687,120 terms), u1_20_4M.txt (701,285 terms), ~2 min each in the background.

- My A*b + B picture was too thin: U(1,b) is mostly runs of consecutive numbers. Big runs are b-3 to b+1 long, sit on a grid of bars 3b long, and some bars are empty (54% of bars hold a block).
- Gap between consecutive big blocks = j*3b + delta. delta ~ round(0.417*j): j=1 gives 0 (5404) or 1 (2609); j=3 mostly 2; j=6 mostly 3; j=13 mostly 6 (b=10, 6e5).
- So 0.41703 = total slip / total bars: the blocks fall 0.417 of a seat behind the 3b grid per bar. b=10 to 4e6: 131,504 bars, c = 0.4170291 (sum) / 0.417031 (fit). b=20: 66,194 bars, 0.4170318.
- Rigid: the (j, delta) word is identical for b = 10, 20, 30 to 6e5 (all 3,645 gaps for b=30) and for b = 10 vs 20 to 4e6 (all 35,680 gaps). For b <= 8 the b/3 block test misfires, so not compared.
- Not a pure rotation: block ends wobble around the perfect (3b + c) grid with a spread of 2.229 seats, and the spread is the same 2.229 at 13k, 33k, 66k and 131k bars. Bounded, bell-shaped histogram.
- No closed form found (83/199 nearest small fraction; mpmath identify gives junk). Only ~6 digits known.
- Known? A search summary of Sheydvasser's 'The Ulam Sequence of the Integer Polynomial Ring' (arXiv 1910.00109) describes U(1,X) as a disjoint union of intervals computed uniformly for large n, which is this block word. Treat 3b + 0.417 as probably known.

Scorecard: 1 (B/A -> 0.139) wrong framing (blocks, not points), right idea (c is a drift per bar). 2 bounded residual: right (2.229 seats). 3 same list across b: right. 4 no small fraction: right. 5 untested.
