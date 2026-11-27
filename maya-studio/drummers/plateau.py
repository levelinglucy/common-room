"""Why the seam is stuck: the two ends of a shifted block don't feel each other.

Start from Euclid, take the minority gaps (the 'beads'), and slide a block of
b consecutive beads one gap forward. That leaves one bead spacing short by 1
and one long by 1: a pair of defects, b beads apart. Measure the band's total
local energy (each drummer, its j nearest per side, 1/d) as b varies.

If the bead pattern is periodic (m divides k), sliding a lone defect along is
a symmetry, so the energy should be flat in b once the two ends are out of
reach of each other: nothing pulls them together. If the pattern isn't
periodic, the energy should wobble, which pins or pushes defects.
"""
import sys, json
from seam import split
from twist_exact import stuck


def total_energy(g, j, n):
    k = len(g)
    e = 0.0
    for i in range(k):
        span = 0
        for w in range(1, j + 1):
            span += g[(i + w - 1) % k]
            e += 1.0 / span      # pair (i, i+w), counted once per ordered side
    return 2 * e


def block_state(k, n, b):
    base, minor, m = split(k, n)
    P = [(i * k) // m for i in range(m)]
    Q = P[:m - b] + [(p + 1) % k for p in P[m - b:]]
    if len(set(Q)) < m:
        return None
    g = [base] * k
    for p in Q:
        g[p] = minor
    return g


if __name__ == "__main__":
    out = {}
    for (k, n, j) in [(16, 36, 7), (16, 36, 5), (20, 50, 9), (20, 47, 5), (20, 45, 7)]:
        base, minor, m = split(k, n)
        g0 = block_state(k, n, 0)
        e0 = total_energy(g0, j, n)
        rows = []
        for b in range(1, m):
            g = block_state(k, n, b)
            if g is None:
                continue
            de = total_energy(g, j, n) - e0
            rows.append((b, round(de, 6), stuck(g, j, n)))
        out[f"{k},{n},{j}"] = dict(m=m, rows=rows)
        print(f"k={k} n={n} m={m} j={j}:")
        for b, de, st in rows:
            print(f"   block of {b} beads slid: energy above Euclid {de:+.6f}  stuck={st}")
    json.dump(out, open("plateau.json", "w"))
