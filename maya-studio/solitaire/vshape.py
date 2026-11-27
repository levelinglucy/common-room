"""The V of the longest trip. usage: python3 vshape.py NMAX
For each n = T_k + r: maxT, depth of all-ones, three candidate branches:
  down = k(k-1-r)                    (from the staircase below)
  up   = (k+1)k - (k+1-r)(k+2)        (from the staircase above)
  ones = depth of (1,1,...,1)
and which partitions reach maxT.
"""
import sys
from bulgarian import analyse, tri_k, move

def depth_of(lam, cyc):
    d = 0
    while lam not in cyc:
        lam = move(lam)
        d += 1
    return d

NMIN = int(sys.argv[2]) if len(sys.argv) > 2 else 3
NMAX = int(sys.argv[1])
print('n k r maxT down up ones max(down,up,ones) match second_best_nonones')
for n in range(NMIN, NMAX + 1):
    a = analyse(n)
    k, r = tri_k(n)
    cyc = set(z for c in a['cycles'] for z in c)
    ones = depth_of((1,) * n, cyc)
    down = k * (k - 1 - r)
    up = (k + 1) * k - (k + 1 - r) * (k + 2)
    best = max(down, up, ones)
    print(n, k, r, a['maxd'], down, up, ones, best, 'OK' if best == a['maxd'] else 'MISS', flush=True)
