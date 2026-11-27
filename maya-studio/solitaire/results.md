# Bulgarian solitaire: results (18 Nov, 9:40 AM session)

Code: `bulgarian.py NMAX` (whole state graph per n: cycles, longest trip, basins, orphans), `vshape.py NMAX [NMIN]` (longest trip vs three branches), `orphans.py NMAX` (orphan share by counting, no listing). Outputs: run45.txt, run62.txt, vshape56.txt, vshape57_64.txt, orphans.txt (the last run was cut off by a VM hiccup after n = 160).

Write n = T_k + r with T_k = k(k+1)/2 and 0 <= r <= k.

## Checked against predictions
1. Triangular n: one fixed point, longest trip exactly k^2 - k, every k up to 10 (n <= 55). Right (and known: Igusa / Etienne, Knuth's conjecture).
2. Number of cycles = binary necklaces of length k+1 with r ones, every n <= 62; cycle lengths all divide k+1. Right (known: Brandt 1982; a survey summary confirms the staircase + 0/1 form).
3. Longest trip for non-triangular n is below the triangular n just above it: right for every n <= 64. But it is NOT always below the triangular n just below: at r = k it is k^2 - 2 > k^2 - k. (A survey summary says Griggs & Ho 1998 proved D <= m^2 - 2 with equality at m' = m; my numbers agree for k = 2..9.)
4. Parent rule right (has a parent iff largest part >= parts - 1, all n <= 62). Orphan share wrong: 42.7% at n = 45, 46.2% at n = 160, not > 80%. It must tend to 1/2: conjugation swaps 'largest > parts' and 'largest < parts', so the orphans are half of everything minus a thin near-diagonal band (21% of partitions at n = 10, 5.1% at n = 160).
5. Biggest basin over half for most non-triangular n: mostly yes (55-73%), but 49.3% at n = 24, 44.5% at n = 40, 43.4% at n = 60 (all r = k/2 with k even: the most cycles).

## The V (the session's find)
Longest trip over all starts, for n = T_k + r, every n from 3 to 64 (62 values, 0 misses):

    maxT = max( k(k-1-r),  k(k+1) - (k+1-r)(k+2),  n - k )

- 'down' branch k(k-1-r): drops by k for each extra card above the staircase T_k.
- 'up' branch: climbs by k+2 per card towards T_{k+1} - 1, where it equals k^2 - 2 (Griggs-Ho's bound).
- floor n - k: the all-ones start. Starting from n single cards takes exactly n - k moves to reach the cycle for every non-triangular n up to 399 (n - k + 1 for triangular n). The big pile loses one card a move while a staircase builds beside it.
- So the longest trip draws a V between consecutive staircases: k=10 row reads 90 80 70 60 50 50 51 62 74 86 (r = 0..9). The bottom of the V sits near r = k/2, where the worst start is just n single cards.
- Deepest starts: near the bottom the all-ones pile alone; on the branches big families (thousands of partitions) shaped like a staircase with one step doubled, e.g. (9,9,8,7,6,5,5,4,3,2,1) at n = 59.

Unknown: whether the three-branch formula is in the literature (Griggs & Ho may have it; I only saw a summary). Don't claim it as new. Not proved; checked to n = 64 only.


## 18 Nov, 12:40 PM: the V to n = 122, and who is deepest

Code: `vtree.c` (walks the trees backwards from the cycle states, one visit per partition, no visited set; predecessor rule: pick a part m >= L-1, drop it, +1 to the rest, add m-(L-1) ones). `vsmall.c`, `vrest.c` (also the deepest start off the all-ones chain), `vhist.c` (depth histogram + sample deepest starts for one n). Outputs: vtree_3_64.txt, vtree_65_135.txt (stopped after n = 122), vrest_3_98.txt, hist84.txt.

- Completeness check every n: partitions visited = p(n) exactly (largest p(122) = 2,291,320,912). maxT agrees with the old Python for all 62 overlapping n.
- The three-branch formula max(k(k-1-r), k(k+1)-(k+1-r)(k+2), n-k) holds for every n = 3..122 (120 values, 0 misses).
- How many starts take the longest trip: on the branches a few percent (triangular n: 9.1% at n = 15, 5.7% at 55, 3.3% at 105), millions of partitions. At the bottom of the V the all-ones pile is the ONLY deepest start: for odd k at r = (k-1)/2 and (k+1)/2, for even k at r = k/2 + 1 (every k from 5 to 14).
- At even k, r = k/2, a staircase family ties the all-ones pile exactly at k^2/2 moves (k = 4..14: n = 12, 24, 40, 60, 84, 112), though the down formula gives only k^2/2 - k there. E.g. n = 84: 317,078 starts tie, like (11,11,10,9,8,7,6,6,5,4,3,2,1,1). So the down branch flattens before it meets the floor; the formula still holds because n - k covers it.
- At odd-k bottoms the runner-up is (2,1,...,1), one move behind, and alone (count 1 excluding the chain).
- Deepest-family shape: staircase with two doubled steps, e.g. (11,11,10,9,8,7,6,6,...) at n = 84; on the down branch the top is doubled, (k-1,k-1,k-2,...).
- Literature: one more search, summary unreliable (gave a bound my data breaks). Still unknown whether the formula is published; don't claim new.


## 18 Nov, 3:40 PM: why the tie at k^2/2 (the vernier)

Code: `tie_trace.py N K` (deepest starts, their cycles, excess-energy profile), `plateau.py N K p` (diagonals k-1..k+2 move by move), `vernier.py NMIN NMAX` (every start whose last phase is one-card-one-hole), `final_seats.py` (seat pattern at the drop). Outputs: vernier_6_36.txt, vernier_37_46.txt.

Energy view: card in pile i (sorted), position j sits on diagonal i+j (diagonal t has t+1 seats). With the new pile placed on top, a move just turns every diagonal one seat; only re-sorting lowers energy. Cycle = diagonals 0..k-1 full, r cards on diagonal k.

- The tie family never joins the all-ones trip: it lands in a different cycle (n = 24: all 30 go to the cycle of (6,5,4,4,2,2,1); the all-ones pile goes to (6,5,4,3,3,2,1); n = 12 likewise; n = 40: none of the 820 merge with the all-ones chain).
- Its trip: a short fall, then a long plateau at excess energy exactly 2, then a drop to 0. The plateau is always one card too high (diagonal k+1, k+2 seats) and one empty seat too low (diagonal k-1, k seats), with r cards on diagonal k (k+1 seats). Three rings turning one seat per move.
- Each time the empty seat comes round to the bottom (every k moves), the card is exactly 2 seats nearer the top (0 exceptions, n = 6..46). The drop happens when the empty seat is at the bottom and the card is at the top seat (0, or 1 when it rests on d_k seats 0 and 1): checked for n = 12, 17, 18, 24, 31, 32.
- Longest such plateau, every non-triangular n = 7..46 (28 values, 0 misses):
      L = min( k(k-r), (k+2)(r-1)+2 )
  My reading of the two clocks (from traces, not proved): the card must rest on two neighbouring d_k cards and slips back one seat per lap of its ring, so it can ride the r cards for r-1 laps of k+2 (+2 at the edge seat). The empty seat needs two neighbouring empty d_k seats beside it; it lives in the k+1-r empty seats, slipping one per lap of k, so k-r laps of k.
- The two clocks are equal only when r = k/2 (k^2+k = 2r(k+1)), so only for even k, and then both equal k^2/2 = n - k, the all-ones trip. Three different mechanisms give the same number at exactly that n: that is the tie. For odd k the clocks never match and the plateau family falls short of the floor (e.g. n = 31: 20 vs 24; n = 32: 21 vs 25).
- All 1, 30 and 820 tie starts at n = 12, 24, 40 end in this plateau.
- Not proved; don't claim new.


## 18 Nov, 6:40 PM: the two clocks, checked directly

Code: `clocks.py NMIN NMAX` (outputs clocks_7_30.txt, clocks_31_46.txt), `render_vernier.py` -> `vernier_rings.png`.

For every start whose trip ends in a one-card-one-hole plateau (all n = 7..46, k >= 3, r >= 1; e.g. 12,019 starts at n = 40):
- The whole plateau is rigid turning: hole seat +1 mod k, card seat +1 mod k+2, d_k pattern turned +1 mod k+1, every move. 0 exceptions.
- Clocks from the plateau's first state, under rigid turning: card clock = moves until the card's support fails (seat c needs d_k seats c-1 and c; seat 0 needs only d_k seat 0, seat k+1 only d_k seat k); hole clock = moves until a d_k card sits over the hole (seat h needs d_k seats h, h+1 empty).
- Plateau length = min(card clock, hole clock), 0 exceptions.
- No plateau that runs straight into the cycle ever ends on the card clock alone: it ends on the hole clock, or both on the same move (n = 40: both 10,081, hole 1,938, card 0). (A card-only failure drops the card to d_k, E+1, and the trip goes on; those runs aren't counted here.)
- Largest card clock seen = (k+2)(r-1)+2 whenever r <= k/2 (or k odd and r = (k+1)/2); largest hole clock = k(k-r) whenever r >= k/2; longest plateau = min of the two formulas, every n.
- Geometry: with seat i at angle i/(seats) of a turn, the card's two supports straddle it and the hole's two empty seats straddle it, so the picture is literally three concentric gear rings; the only seam is seat 0 at the top.
- Still not proved by hand; the rigid-turning part is easy (a move only turns diagonals; sorting acts only when a clock fails), the clock lengths are counting.
