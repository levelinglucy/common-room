"""Exhaustive two-valued traps.

For each (k, n), list every rhythm that uses only the two Euclid gap sizes
(base and minority, with exactly m minority gaps), up to rotation. For each
non-Euclid one, find the largest reach j at which it is stuck. The worst one
gives a lower bound jmin >= worst + 1. Compare with the simulated jmin from
sweep_km20.json. m = 1 traps need a third gap size (the 1-and-two-3s defect),
so this bound is expected to miss there.
"""
import sys, json, itertools
from drummers import canon, euclid_gaps
from twist_exact import stuck
from seam import split


def rhythms(k, m, base, minor):
    seen = set()
    for P in itertools.combinations(range(1, k), m - 1):
        g = [base] * k
        g[0] = minor
        for p in P:
            g[p] = minor
        c = canon(tuple(g))
        if c not in seen:
            seen.add(c)
            yield c


def largest_stuck(g, k, n):
    for j in range(k // 2, 0, -1):
        if stuck(list(g), j, n):
            return j
    return 0


if __name__ == "__main__":
    K = int(sys.argv[1])
    sim = {}
    for row in json.load(open("sweep_km20.json")):
        sim[(row["k"], row["n"])] = row["jmin"]
    out = []
    for (k, n), jm in sorted(sim.items()):
        if k > K:
            continue
        base, minor, m = split(k, n)
        if m < 2:
            continue
        E = euclid_gaps(k, n)
        worst, arg = 0, None
        for g in rhythms(k, m, base, minor):
            if g == E:
                continue
            w = largest_stuck(g, k, n)
            if w > worst:
                worst, arg = w, g
        ok = "MATCH" if worst + 1 == jm else ("below" if worst + 1 < jm else "ABOVE?")
        line = f"k={k:2d} n={n:2d} m={m}: two-valued worst stuck j={worst} -> bound {worst + 1}, sim jmin {jm}  {ok}  trap {''.join(map(str, arg)) if arg else '-'}"
        print(line, flush=True)
        out.append(dict(k=k, n=n, m=m, worst=worst, sim=jm, trap=arg))
    json.dump(out, open(f"two_valued_k{K}.json", "w"))
