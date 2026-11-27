# Why the two odd gaps stop exactly j - 1 apart (15 Nov 2026, evening)

Setting: drummers.py model, energy 1/d to the j nearest on each side, one-slot moves.
Case: every gap is 1 or 2, exactly two gaps are 1 (e.g. 9 on 16). Write r for the
number of 2-gaps between the two 1s on one arc, and assume the other arc is long
(>= j - 1) so its far 1 is out of earshot.

Take the drummer D at the left end of a 1-gap. To its right the gaps are
1, then r twos, then the other 1. To its left, twos.

- Distances right: R_m = 2m - 1 for m <= r + 1, then 2m - 2.
- Distances left: L_m = 2m.

If D steps left, the 1 moves one place AWAY from the other 1. After the step:
left distances 1, 3, ..., 2j - 1; right distances 2, 4, ..., 2(r+1), then 2m - 1.
Using 1/(x) - 1/(x+1) = 1/(x(x+1)) the change telescopes to

  dE = sum over m = r+2 .. j of [ 1/(2m(2m-1)) - 1/((2m-1)(2m-2)) ]

Every term is negative, so dE < 0 exactly when the sum is non-empty: r + 2 <= j,
i.e. r <= j - 2. So the 1 walks away from the other 1 while r <= j - 2 and stops at
r = j - 1, the first separation where D's j-th right neighbour no longer sits past
the other 1.

The drummer at the RIGHT end of the 1-gap (the move that would bring the 1s
closer) gets

  dE = sum over m = r+1 .. j of [ 1/((2m-1)(2m-2)) - 1/(2m(2m-1)) ]  > 0 when r < j,

and 0 (a tie, no move) when r >= j. A drummer between two 2s that steps makes a
1 and a 3; not covered by this hand argument, but the exact check below includes
those moves.

So: among two-valued rhythms with two odd gaps, stuck <=> both arcs >= j - 1, for
j <= floor(k/2). Starting closer, they walk apart one step per move and stop at
exactly j - 1. That is the ladder.

## Exact checks (ladder_proof_check.py, pinned_rule.py)

- m = 2, every two-valued rhythm, simulation's own energy, all one-step moves:
  7/12, 9/16, 11/20, 13/24, 15/28 (odd gaps short) and 9/20, 11/24, 13/28 (odd
  gaps long): the arc rule agrees in every case for j <= floor(k/2). It only
  "fails" at j = floor(k/2) + 1, where drummers hear someone twice round the ring
  and Euclid is stuck regardless.
- m >= 3, the arc rule alone is wrong: Euclid itself (e.g. 14/31 = arcs 4,3,4) is
  stuck with an arc shorter than j - 1, because the short arc's odd gaps are pushed
  from both sides. Local rule: an odd gap with arcs a and b on its two sides is
  pinned if min(a, b) >= j - 1 OR |a - b| <= 1. Stuck <=> every odd gap pinned.
  - m = 3: 16 cases (10/13 ... 25/53, short and long odd gaps), 6,421 (rhythm, j)
    pairs, 0 disagreements.
  - m = 4: 9 cases, ~19,900 pairs, 3 disagreements, all at j = k/2 exactly (even k,
    the opposite drummer heard from both sides).
  - m = 5 and 7: mostly right (e.g. 21/47: 9,687 agree, 3 disagree), but fails where
    a wide ear hears the NEXT-but-one odd gap and it tilts a locally balanced one.
    The local rule is a first-neighbour approximation; m = 2 is exact (proved).
