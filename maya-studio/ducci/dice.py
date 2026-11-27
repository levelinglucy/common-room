"""Is Ehrlich's divisor a dice roll?

For prime n, the ring splits into c = (n-1)/m copies of GF(2^m), and P(n) is the
lcm of the orders of 1 + zeta^a over one a per coset of <2> in (Z/n)*.
Heuristic: a prime q dividing E cuts P only if every one of the c elements
lands in the index-q subgroup, so if they behave like independent dice the
rate is about (1/q)^c. Measure cut rates per (q, c) over primes n < N.
"""
import sys, json, time
from collections import defaultdict
from fast import Dpow, ord2, h_minus1, small_primes

N = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
QS = [3, 5, 7, 11, 13]
primes_n = [p for p in small_primes(N) if p > 2]
stat = defaultdict(lambda: [0, 0])  # (q, c) -> [eligible, cut]
t0 = time.time()
for n in primes_n:
    m = ord2(n); h = h_minus1(n); c = (n - 1) // m
    E = n * (2 ** h - 1) if h else 2 ** m - 1
    for q in QS:
        if q == n or E % q:
            continue
        # q divides E; is the cycle still closed after E/q steps?
        cut = Dpow(3, E // q, n) == 3
        key = (q, min(c, 4))
        stat[key][0] += 1; stat[key][1] += cut
print(f"primes 3 < n < {N}: {len(primes_n)}  ({time.time()-t0:.0f}s)")
print("q  cosets  eligible  cut   rate    (1/q)^c")
out = []
for (q, c) in sorted(stat):
    e, k = stat[(q, c)]
    lab = f"{c}" if c < 4 else "4+"
    print(f"{q:<3d}{lab:>6s} {e:9d} {k:5d}  {k/e:6.3f}   {(1/q)**c:6.3f}")
    out.append(dict(q=q, cosets=lab, eligible=e, cut=k))
json.dump(out, open(f"dice_N{N}.json", "w"), indent=1)
