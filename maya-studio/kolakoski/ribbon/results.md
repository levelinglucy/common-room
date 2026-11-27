# The K(1,3) window (16 Nov, 6:40 PM)

`ribbon.py 1 3 2000000` -> ribbon_1_3.npz; `check.py`, `check2.py`, `areas.py` (numbers); `render.py` -> kolakoski_window.png.

- Substitution matrix (tags ae, ao, be, bo): eigenvalues 2.205569, 1, and -0.102785 +- 0.665457i (modulus 0.673348 = 1/sqrt(2.205569)). Correction: the "modulus ~0.10" in ../results.md was the real part.
- Self-check: the tagged sequence equals its own run expansion (True, 2M letters).
- Coordinates of prefix count vectors: Perron grows (1.1e6), complex pair bounded (|z| <= 0.9367), eigenvalue-1 coordinate takes exactly two values 0 / 1 = parity of the position. So the window is two flat sheets.
- Letter frequencies: ae 0.3120, ao 0.0853, be 0.1880, bo 0.4147. A 1 stands on 62.4% of even places and 17.0% of odd ones (every run of 1s starts on an even place, because run i starts on parity i when all lengths are odd).
- Inside one sheet, the 1-piece and 3-piece do not overlap: shared grid cells 1.8% / 0.89% / 0.36% / 0.06% at G = 200/400/800/1600 (2M points), roughly halving or better per doubling = boundary only. The two sheets overlap for real: 45.3-46.1% shared at every resolution.
- Areas match frequencies (unique ergodicity, as expected): 1-share of even sheet 0.623 by area vs 0.624 by count; odd 0.172 vs 0.170; even/odd sheet area ratio 0.99999.
- Picture checked by text extents (all inside 1650 px) and colour counts, not by eye.

Open: are the two sheets congruent (one a rotated/scaled copy of the other via the set equations)? Boundary dimension of the 1/3 split? Write the graph-directed IFS and draw from it instead of from the orbit.
