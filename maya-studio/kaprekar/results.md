# Kaprekar in other bases (14 Nov 2026, 3:40 AM session)

K(n) = digits sorted high-to-low minus low-to-high, d digits, leading zeros kept. "Unique" = every non-repdigit d-digit string ends on one fixed point.

Tools: `kaprekar.py` (slow, over digit multisets, census for b<=16, d<=6), `sweep.py` (slow sweeps), `kfast.py D BMIN BMAX` (fast: K depends only on the gaps e_i = a_i - a_(d+1-i), so d=4,5 are 2-variable maps; checked identical to the slow census on 60 (base, d) pairs), `landscape.py` -> `steps_6174.npy`, `render.py` -> `kaprekar_cousins.png`.

Base 10 checks: 4 digits step counts 0..7 = 1, 383, 576, 2400, 1272, 1518, 1656, 2184 (+10 repdigits), matches the known table. 6 digits: 631764, 549945 + a 7-cycle; 7 digits: one 8-cycle; 8 digits: 97508421, 63317664 + 3- and 7-cycles (matches OEIS A099009).

## Unique constants found
- d=2: only base 2 (01). Bases 2^k - 1 (3, 7, 15, ..., 1023) send everything to 0 (checked to 1100).
- d=3: every even base (2..400), constant (b/2-1)(b-1)(b/2) (known family). No odd base.
- d=4: bases 5, 10, 40, 160, 640 (sweep 2..700) and 2560 (checked alone). Constant (3b/5)(b/5-1)(4b/5-1)(2b/5): 3032, 6174, (24.7.31.16), (96.31.127.64), (384.127.511.256), (1536.511.2047.1024). Same fixed point exists in 20, 80, 320, 1280 but a rival cycle steals part of the space (lengths 6, 5, 14, 9). Base 20 rival 6-cycle takes 52 of 209 gap-states. So: unique at 5*2^m for m = 0 and odd m.
- d=5: base 3 and every base 6k+3 from 15 to 699 (not 9). Constant (2b/3)(b/3-1)(b-1)(2b/3-1)(b/3), e.g. a4e95 in base 15.
- d=6: bases 13 and 17 only (2..120): 951a74, d91e74.
- d=7: base 4 only (2..120): 3203211.
- d=8: base 3 (21022111) in the slow sweep 2..12.

Literature: Chen, Ono, Schwartz, Thakur, "Four-digit Kaprekar dynamics in odd bases" (arXiv 2606.20439, 2026): in odd bases the 4-digit map is conjugate to doubling on unordered pairs of (Z/B)*/{+-1}. Even bases not covered there. I don't know whether the 5*2^odd pattern is already known.

Open: why odd powers of 2 (maybe the 2-part acts like a doubling with a parity flip)? d=5 6k+3 family: why 9 fails. d=6 beyond 120 with a faster 3-variable enumerator.

## Why odd powers of 2 (14 Nov 2026, 6:40 AM session)

Tools: `ladder.py [M]` (closed-form gap map + escape orbits from the edge states), `prove_unique.py [M]` (exact uniqueness check over correction states only), `render_ladder.py` -> `kaprekar_ladder.png`. Output tail in `prove_unique_output.txt`.

Closed form (checked against the literal routine): state (x, y) = (e1, e2).
- y >= 1: K's digits are {x, B-x, y-1, B-1-y}. y = 0: {x-1, B-1, B-1, B-x}.
- Two digit pairs, centred at B/2 and B/2 - 1, with spreads |2x-B| and |2y-B|. When the spreads differ by 2 or more the pairs nest and the map is exactly the tent map z -> |2z-B| on each gap, sorted (checked on 100k random states). Corrections only at y = 0 (edge) or when the spreads are within 1 (collision).
- With w = B - z the tent is doubling mod 2B up to sign. For B = 5*2^m its only periodic values are B/5 and 3B/5 (the tent 2-cycle), so every cycle except the fixed point (3B/5, B/5) must pass a correction state. So checking ~2.5B correction states is an exact uniqueness test.

The ladder: from the edge (B/5, 0) the next state is (4B/5, B/5 - 1). One gap rides the rails B/5 <-> 3B/5 exactly; the other carries a deviation -1, +2, +4, -8, -16, ... (doubles; sign flips on each B/5 step because the tent slopes down there). |dev| = 2^k on a B/5 step when k is even, a 3B/5 step when k is odd. Deviation 2^m = B/5:
- m = 0 mod 4: reached at a B/5 step with sign minus -> gap = 0 exactly -> back to the edge: rival cycle of length m+1 (80: 5, 1280: 9, ... 327680: 17).
- m = 2 mod 4: reached at B/5 with sign plus -> 2B/5 -> next step both gaps hit B/5 (collision) -> split +-1 -> a second ladder lands on (2B/5, 0) -> rival cycle of length 2m+2 (20: 6, 320: 14, 5120: 22 ... 54 at m=26). Started from (2B/5, 0).
- m odd: reached at a 3B/5 step -> 2B/5 or 4B/5, no edge -> a second ladder ends on the fixed point.
`ladder.py 26` confirms this pattern for every m from 0 to 26. `prove_unique.py 19`: UNIQUE for every odd m up to 19 (B = 2,621,440) and m = 0; rival for every even m >= 2. Matches the slow census where they overlap (m <= 9).
Not a written proof for all odd m (the second-ladder landing and the other correction states were checked by computer, not by hand), but the mechanism is clear: the error has to land on an edge, and the rails have period 2, so only the parity of m decides it.

Open: write the odd-m case by hand; other q*2^m (q = 3 collides with itself: B/3 is a tent fixed point with equal spreads; q = 7, 9, 11 have longer rail cycles -> landing depends on m mod period?); d=5 6k+3 family looks like the same story with rails 1/3, 2/3.
