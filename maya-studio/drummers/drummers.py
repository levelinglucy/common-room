"""Drummers on a ring: do local listeners find the Euclidean rhythm?

k drummers sit on n beat slots of a cycle (order around the ring is fixed:
nobody passes anyone). Each drummer only hears its j nearest drummers on each
side, and feels a repulsion f(d) = 1/d from each, d = distance around the ring
in that direction. One at a time, in random order, a drummer steps one slot
forward or back into an empty slot if that lowers what it feels. Stop when no
drummer can improve.

Question: when does the stuck state equal the maximally even (Euclidean)
rhythm E(k, n), and how far does each drummer need to listen?
"""
import random


def gaps_of(pos, n):
    k = len(pos)
    return tuple((pos[(i + 1) % k] - pos[i]) % n for i in range(k))


def canon(g):
    """Smallest rotation of a gap sequence (rhythm up to rotation)."""
    return min(g[i:] + g[:i] for i in range(len(g)))


def euclid_gaps(k, n):
    pos = [(i * n) // k for i in range(k)]
    return canon(gaps_of(pos, n))


def feel(pos, i, p, j, n, f):
    """Energy drummer i would feel at slot p, hearing j drummers per side."""
    k = len(pos)
    e = 0.0
    for m in range(1, j + 1):
        a = pos[(i + m) % k]
        b = pos[(i - m) % k]
        da = (a - p) % n
        db = (p - b) % n
        if m % k == 0:          # wrapped onto itself (j >= k)
            da = db = n
        e += f(da) + f(db)
    return e


def run(k, n, j, rng, f=lambda d: 1.0 / d, max_sweeps=10000):
    pos = sorted(rng.sample(range(n), k))
    occupied = set(pos)
    for sweep in range(max_sweeps):
        moved = False
        order = list(range(k))
        rng.shuffle(order)
        for i in order:
            p = pos[i]
            here = feel(pos, i, p, j, n, f)
            best, bestp = here, p
            steps = [1, -1]
            rng.shuffle(steps)
            for s in steps:
                q = (p + s) % n
                if q in occupied:
                    continue
                e = feel(pos, i, q, j, n, f)
                if e < best - 1e-12:
                    best, bestp = e, q
            if bestp != p:
                occupied.discard(p)
                occupied.add(bestp)
                pos[i] = bestp
                moved = True
        if not moved:
            return pos, sweep
    return pos, max_sweeps


def depth(k, n):
    """Length of the continued fraction of k/n (Euclid's algorithm steps)."""
    a, b, d = n, k, 0
    while b:
        a, b = b, a % b
        d += 1
    return d


if __name__ == "__main__":
    import sys
    rng = random.Random(1)
    k, n, j = map(int, sys.argv[1:4])
    E = euclid_gaps(k, n)
    hits = 0
    for t in range(50):
        pos, sw = run(k, n, j, rng)
        hits += canon(gaps_of(pos, n)) == E
    print(k, n, j, "euclid", E, "hits", hits, "/50")
