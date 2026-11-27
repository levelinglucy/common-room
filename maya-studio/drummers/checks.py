"""Checks on the drummers.

1. Exhaustive: for small n, is the all-pairs 1/d energy minimum exactly the
   Euclidean rhythm (up to rotation)?
2. What the stuck states look like when they miss: 'ramp' (gap spread >= 2,
   neighbouring gaps differ by <= 1) vs 'clump' (gaps within 1 of each
   other, but the long gaps bunched in the wrong order) vs other.
3. Does jmin depend only on k and r = n mod k?
"""
import itertools
import json
import random
from collections import Counter, defaultdict

from drummers import run, gaps_of, canon, euclid_gaps


def energy_all(pos, n):
    e = 0.0
    for a, b in itertools.combinations(pos, 2):
        d = (b - a) % n
        e += 1.0 / d + 1.0 / (n - d)   # both ways round the ring
    return e


def check_global(nmax):
    bad = 0
    total = 0
    for n in range(4, nmax + 1):
        for k in range(2, n // 2 + 1):
            best = None
            winners = set()
            for pos in itertools.combinations(range(n), k):
                if pos[0] != 0:
                    continue
                e = energy_all(pos, n)
                g = canon(gaps_of(list(pos), n))
                if best is None or e < best - 1e-9:
                    best, winners = e, {g}
                elif abs(e - best) < 1e-9:
                    winners.add(g)
            total += 1
            if winners != {euclid_gaps(k, n)}:
                bad += 1
                print("  global min not Euclid:", k, n, winners)
    print(f"global check n<= {nmax}: {total - bad}/{total} (k,n) pairs have the Euclidean rhythm as the unique all-pairs minimum")


def kind(g, E):
    if canon(g) == E:
        return "euclid"
    if max(g) - min(g) >= 2:
        return "ramp" if all(abs(g[i] - g[i - 1]) <= 1 for i in range(len(g))) else "spread"
    return "clump"


def failure_kinds():
    rng = random.Random(7)
    tally = defaultdict(Counter)
    for n in range(10, 31):
        for k in range(4, n // 2 + 1):
            if n % k == 0:
                continue
            E = euclid_gaps(k, n)
            for j in (1, 2, 3):
                for t in range(20):
                    pos, _ = run(k, n, j, rng)
                    tally[j][kind(gaps_of(pos, n), E)] += 1
    for j in (1, 2, 3):
        print("j =", j, dict(tally[j]))


def jmin_by_kr():
    R = json.load(open("sweep_n30.json"))
    d = defaultdict(set)
    for r in R:
        k, n = r["k"], r["n"]
        m = min(n % k, k - n % k)
        d[(k, m)].add(r["jmin"])
    clash = {key: v for key, v in d.items() if len(v) > 1}
    print("(k, minority) classes:", len(d), "with more than one jmin:", clash)
    return d


if __name__ == "__main__":
    check_global(22)
    failure_kinds()
    d = jmin_by_kr()
    for key in sorted(d):
        print(key, sorted(d[key]))
