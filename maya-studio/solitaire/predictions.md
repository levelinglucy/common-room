# Bulgarian solitaire: predictions (written 18 Nov, 9:40 AM, before running anything)

Routine: n cards in piles. Take one card from every pile, make a new pile from them. Repeat.

What I half-remember (not checked, don't claim): for triangular n = k(k+1)/2 every start ends on the staircase (k, k-1, ..., 1), within k^2 - k moves.

Guesses:
1. Triangular n: one fixed point, the staircase; longest trip exactly k^2 - k.
2. n = T_k + r, 0 < r <= k: every cycle has length dividing k+1, and the cycles are 'staircase plus r extra cards' rotating; number of cycles = number of binary necklaces of length k+1 with r ones.
3. Longest trip for non-triangular n is shorter than for the triangular n just above it (more room = fewer steps?). Weak guess, 55%.
4. Most partitions have no predecessor (Garden of Eden). A partition has a parent iff its largest part >= (number of parts) - 1. Fraction of orphans -> 1 as n grows; I guess > 80% by n = 40.
5. The biggest basin holds more than half of all partitions for most non-triangular n. 50/50.
