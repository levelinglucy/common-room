"""Orphan share (no predecessor) for large n, without listing partitions.
Orphan <=> largest part < (number of parts) - 1  (checked against the full graph to n = 62).
Count partitions of n by (largest a, length l): = partitions of n-a-l+1 inside an (a-1) x (l-1) box.
usage: python3 orphans.py NMAX
"""
import sys
from functools import lru_cache
sys.setrecursionlimit(10000)

@lru_cache(maxsize=None)
def box(m, w, h):
    # partitions of m with at most h parts, each part <= w
    if m == 0:
        return 1
    if w == 0 or h == 0 or m > w * h:
        return 0
    # largest part < w, or largest part == w
    return box(m, w - 1, h) + box(m - w, w, h - 1)

NMAX = int(sys.argv[1])
for n in list(range(10, 61, 10)) + list(range(80, NMAX + 1, 40)):
    tot = orph = diag = 0
    for a in range(1, n + 1):
        for l in range(1, n - a + 2):
            m = n - a - l + 1
            if m < 0:
                continue
            c = box(m, a - 1, l - 1)
            tot += c
            if a < l - 1:
                orph += c
            if a in (l, l - 1):
                diag += c
    print(n, tot, f"orphans {orph/tot:.4f}", f"near-diagonal {diag/tot:.4f}", flush=True)
