"""Recursive traps: build the drummers' trap by Euclid's recursion.

candidates(k, n): gap sequences (k gaps summing to n) built like this.
  m = 0 (all gaps equal): squeeze, one gap one short and one gap one long,
        every placement.
  m = 1: three defects. One short + two long if the odd gap is long, or two
        short + one long if it is short; every placement.
  m >= 2: the m odd gaps sit at m of the k positions, a rhythm of m beads on
        k slots. Put them in each candidate trap of the bead problem (m, k).
The largest reach at which any candidate is stuck, plus one, is the
recursive prediction for jmin. Compare with the sims (k <= 20) and the
exhaustive two-valued search, then predict past k = 20.
"""
import sys
import json
from functools import lru_cache
from drummers import canon, euclid_gaps
from seam import split
from twist_exact import stuck


def place(k, beads, base, minor):
    g = [base] * k
    p = 0
    for b in beads:
        g[p] = minor
        p += b
    assert p == k
    return canon(tuple(g))


@lru_cache(maxsize=None)
def candidates(k, n):
    q, r = divmod(n, k)
    out = set()
    if k <= 3:
        # tiny bead problems: every rhythm is a candidate
        import itertools
        for c in itertools.product(range(1, n), repeat=k - 1):
            if sum(c) < n:
                out.add(canon(tuple(c) + (n - sum(c),)))
        return frozenset(out)
    if r == 0:
        for p in range(1, k):
            g = [q] * k
            g[0], g[p] = q - 1, q + 1
            if min(g) > 0:
                out.add(canon(tuple(g)))
        return frozenset(out)
    base, minor, m = split(k, n)
    if m == 1:
        lo, hi = (base - 1, minor) if minor > base else (minor, base + 1)
        # long odd gap: one lo + two hi ; short odd gap: two lo + one hi
        for x in range(1, k):
            for y in range(x + 1, k):
                g = [base] * k
                if minor > base:
                    g[0], g[x], g[y] = lo, hi, hi
                else:
                    g[0], g[x], g[y] = hi, lo, lo
                if min(g) > 0:
                    out.add(canon(tuple(g)))
        # and a squeeze on Euclid: one gap one shorter, another one longer
        E = list(euclid_gaps(k, n))
        for i in range(k):
            for p in range(k):
                if p != i:
                    g = E[:]
                    g[i] -= 1
                    g[p] += 1
                    if min(g) > 0:
                        out.add(canon(tuple(g)))
        return frozenset(out)
    E = euclid_gaps(m, k)
    for beads in candidates(m, k):
        if beads == E:
            continue
        out.add(place(k, beads, base, minor))
    return frozenset(out)


def largest_stuck(g, n):
    k = len(g)
    for j in range(k // 2, 0, -1):
        if stuck(list(g), j, n):
            return j
    return 0


def predict(k, n):
    E = euclid_gaps(k, n)
    worst, arg = 0, None
    for g in candidates(k, n):
        if g == E:
            continue
        w = largest_stuck(g, n)
        if w > worst:
            worst, arg = w, g
    return worst + 1, arg, len(candidates(k, n))


if __name__ == "__main__":
    sim = {(r["k"], r["n"]): r["jmin"] for r in json.load(open("sweep_km20.json"))}
    match = below = above = 0
    lines = []
    for (k, n), jm in sorted(sim.items()):
        base, minor, m = split(k, n)
        pj, arg, nc = predict(k, n)
        tag = "MATCH" if pj == jm else ("below" if pj < jm else "ABOVE")
        match += tag == "MATCH"; below += tag == "below"; above += tag == "ABOVE"
        line = f"k={k:2d} n={n:2d} m={m}: recursive {pj}, sim {jm} {tag}  ({nc} cand) {''.join(map(str, arg)) if arg else '-'}"
        print(line, flush=True)
    print(f"MATCH {match}  below {below}  ABOVE {above}")
