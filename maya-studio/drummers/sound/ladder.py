"""The two-short-gaps ladder: with m = 2 odd gaps, how far apart do the two short
(or long) gaps end up, as a function of reach j?
For each final state, measure the separation r = number of gaps strictly between
the two odd gaps, the short way round. Euclid has the largest possible r.
"""
import random, sys
from collections import Counter
sys.path.insert(0, '..')
from drummers import run, gaps_of, canon, euclid_gaps

RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 400
cases = [(7, 12), (9, 16), (11, 20), (13, 24), (15, 28), (9, 20), (11, 24), (13, 28)]
for k, n in cases:
    q, rem = divmod(n, k)
    e = euclid_gaps(k, n)
    odd = q + 1 if rem == 2 else q       # the two gaps that differ from the rest
    print(f'== {k} on {n}: gaps mostly {q if rem == 2 else q + 1}, two odd gaps of {odd}; Euclid {"".join(map(str, e))}')
    for j in range(1, k // 2 + 2):
        c = Counter(); other = 0
        for s in range(RUNS):
            pos, _ = run(k, n, j, random.Random(s * 104729 + j))
            g = gaps_of(sorted(pos), n)
            idx = [i for i, x in enumerate(g) if x == odd]
            if len(idx) != 2 or any(x not in (q, q + 1) for x in g):
                other += 1; continue
            d = (idx[1] - idx[0]) % k
            r = min(d, k - d) - 1
            c[r] += 1
        top = ', '.join(f'r={r}:{m}' for r, m in sorted(c.items()))
        print(f'  j={j}: {top}' + (f', other states {other}' if other else ''))
