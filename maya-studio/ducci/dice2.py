"""Dice, refined. 1 + zeta^(-1) = zeta^(-1) (1 + zeta), and zeta (order n, prime to q)
is always a q-th power, so the cosets a and -a are the SAME die.
Independent dice = cosets of <2, -1> in (Z/n)*:
  c_eff = (n-1)/m with a -1, (n-1)/(2m) without.
Prediction: cut rate (1/q)^c_eff. Also split q=3, c_eff=1 by range of n.
"""
import sys, json, time
from collections import defaultdict
from fast import Dpow, ord2, h_minus1, small_primes

N = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
QS = [3, 5, 7, 11, 13, 17, 19, 23, 31]
stat = defaultdict(lambda: [0, 0])
rng = defaultdict(lambda: [0, 0])
records = []
t0 = time.time()
for n in (p for p in small_primes(N) if p > 2):
    m = ord2(n); h = h_minus1(n)
    ce = (n - 1) // m if h else (n - 1) // (2 * m)
    E = n * (2 ** h - 1) if h else 2 ** m - 1
    for q in QS:
        if q == n or E % q:
            continue
        cut = Dpow(3, E // q, n) == 3
        stat[(q, min(ce, 3))][0] += 1; stat[(q, min(ce, 3))][1] += cut
        records.append((n, q, ce, int(cut)))
        if q == 3 and ce == 1:
            b = n * 4 // N
            rng[b][0] += 1; rng[b][1] += cut
print(f"primes 3 < n < {N} ({time.time()-t0:.0f}s)")
print("q   c_eff  eligible  cut   rate   predicted (1/q)^c_eff")
for (q, c) in sorted(stat):
    e, k = stat[(q, c)]
    print(f"{q:<4d}{(str(c) if c < 3 else '3+'):>5s} {e:9d} {k:5d}  {k/e:6.3f}   {(1/q)**c:6.3f}")
print("q=3, c_eff=1 by quarter of the range:")
for b in sorted(rng):
    e, k = rng[b]
    print(f"  n in [{b*N//4}, {(b+1)*N//4}): {k}/{e} = {k/e:.3f}")
json.dump(records, open(f"dice2_N{N}.json", "w"))
