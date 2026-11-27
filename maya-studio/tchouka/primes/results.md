# Seidov's prime queue (OEIS A104737): how fast it grows

_Maya, studio session, 27 November 2026. Numerical result plus a heuristic, not a proof._

## The question
A104737 lists the records of Seidov's prime queue (A104705). Run backwards, it is a Tchoukaillon-style sieve:
start r = 1 and for x = k-1 down to 1 set r <- r + ceil(r / s(x)) with s(x) = p_x - x + 1.
Leonov's "queue sieves" note (Zenodo record 23915663, 3 November 2026) proves the growth for sieves with
linear moduli and leaves A104737, whose moduli grow like x log x, as an open question. The OEIS entry has
no formula. I found no growth result for it anywhere I looked (OEIS, Leonov's two Zenodo notes, Li's arXiv
2608.17517, web search).

## What I found
1. **Stage one is exact.** While p_x >= k, r = k - x + 1 <= s(x), so each step adds exactly 1. So from
   x = k-1 down to pi(k) the count is k - x + 1 with no error.
2. **Stage two is nearly a product.** Below pi(k), r is much larger than s(x) and each step multiplies by
   about (1 + 1/s(x)). Guess: T(k) ~ (k - pi(k) + 1) * prod_{x < pi(k)} (1 + 1/s(x)).
3. **The guess is right to leading order, and the leftover is about 0.60/ln k.** Exact T(k) to k = 10^8
   (code `q.c`, output `run_1e8.txt`): T/guess = 1.0891 at 10^3, 1.0441 at 10^6, 1.0327 at 10^8, and
   (T/guess - 1) ln k sits between 0.60 and 0.63 throughout, drifting down to 0.6016 at 10^8.
4. **The product grows like B ln x with B = 2.6077.** Summing ln(1 + 1/s(x)) to x = 10^8 and adding a tail
   from Cipolla's expansion of p_x gives B = 2.60813, 2.60757, 2.60759, 2.60766, 2.60772 at x = 10^4 ... 10^8
   (`bconst.c`, `bconst.txt`). The limit itself is an extrapolation.
5. **So A104737(k) ~ B k ln k with B about 2.6077**, approached very slowly: T/(k ln k) is 2.000 at 10^3,
   2.320 at 10^6 and 2.396 at 10^8.

The idea is the same staircase-then-percentage split that Erdős and Jabotinsky (1958) saw for the plain
sieve. Only its use for this prime-modulus queue is mine, and I haven't checked every possible source.

First terms from the code match OEIS: 1, 2, 3, 5, 8, 9, 14, 17, 23, 26, 27, 32.

Picture: `prime_queue.png`.

## Earlier fatter-pits formula: already published
My Gamma-function formula for the sowing game with fatter pits (pit k needs a*k seeds) is not new.
Leonov's note proves it for every linear modulus a*k + d, with d included. I've marked it in
`../variants/results.md`.
