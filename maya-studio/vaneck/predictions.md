# Van Eck's sequence: predictions before running (27 Nov 2026, 12:40 AM)

Rule: a(0)=0. If a(n) appeared before, a(n+1) = n - (last earlier index of a(n)); else a(n+1) = 0.
Known (OEIS A181391): infinitely many zeros, unbounded (Van Eck 2010 / Sloane). Open: does every number appear? Is the count of zeros ~ n/ln n?

My guesses:
1. Zeros up to N: Z(N) ~ c * N / ln N with c close to 1 (each zero = a new value; new values arrive at rate ~1/ln n if values up to ~n are used, each needing about ln n tries).
2. First appearance of value v: around v * ln v / something, and every v < 10^6 appears by N = 10^9.
3. The largest value up to N is within a small factor of N (a value reappearing after a long gap).
4. Small values are common: count of 1s grows like Z(N) (a 1 follows any immediate repeat).
