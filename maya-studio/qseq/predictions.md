# Hofstadter's Q, predictions written before running (19 Nov 2026, 9:45 PM)

Q(1)=Q(2)=1, Q(n) = Q(n - Q(n-1)) + Q(n - Q(n-2)).

1. Q(n)/n settles near 1/2. Spread of Q(n) - n/2 grows like a power of n; Pinn (1999) said about n^0.88. I guess I'll measure 0.85-0.92 to 1e9.
2. 'Generations': the wild patches start and end near powers of 2 (Pinn). I guess the boundaries keep doubling cleanly to 2^30.
3. The two 'look-back' distances n - Q(n-1) and n - Q(n-2): I guess they stay within a few percent of n/2, so the sequence reads from about halfway back. Fraction of steps where the two parents are the same cell: small, under 1%.
4. Parity: I guess Q(n) is even about half the time, no lasting bias.
5. Never undefined (no look-back below 1) up to 1e9.
