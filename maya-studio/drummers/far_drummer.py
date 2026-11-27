"""Nearest-only listeners plus one far drummer (the firefly/starling trick).

mode 'friend': each drummer also hears one fixed, randomly chosen other drummer.
mode 'glance': each time a drummer considers a move it also hears one random
               other drummer, redrawn every time.
mode 'none'  : plain j nearest per side (control).

Glance never has to settle, so every mode runs a fixed number of sweeps and we
record whether the final state is the Euclidean rhythm and the share of the
last 100 sweeps spent in it.
"""
import json
import random
import sys
from multiprocessing import Pool

from drummers import gaps_of, canon, euclid_gaps, feel

f = lambda d: 1.0 / d


def feel_extra(pos, i, p, j, n, other):
    e = feel(pos, i, p, j, n, f)
    if other is not None:
        a = pos[other]
        d = (a - p) % n
        e += f(d) + f(n - d)       # hear it both ways round
    return e


def run_mode(k, n, j, mode, rng, sweeps=600, tail=100):
    pos = sorted(rng.sample(range(n), k))
    occ = set(pos)
    E = euclid_gaps(k, n)
    friend = [rng.choice([x for x in range(k) if x != i]) for i in range(k)]
    in_e = 0
    for s in range(sweeps):
        order = list(range(k))
        rng.shuffle(order)
        for i in order:
            if mode == "friend":
                other = friend[i]
            elif mode == "glance":
                other = rng.choice([x for x in range(k) if x != i])
            else:
                other = None
            p = pos[i]
            best, bp = feel_extra(pos, i, p, j, n, other), p
            for st in rng.sample([1, -1], 2):
                q = (p + st) % n
                if q in occ:
                    continue
                e = feel_extra(pos, i, q, j, n, other)
                if e < best - 1e-12:
                    best, bp = e, q
            if bp != p:
                occ.discard(p); occ.add(bp); pos[i] = bp
        if s >= sweeps - tail:
            in_e += canon(gaps_of(pos, n)) == E
    return canon(gaps_of(pos, n)) == E, in_e / tail


CASES = [(7, 16), (8, 21), (9, 20), (10, 22), (11, 24), (12, 26), (12, 29), (13, 28), (14, 30),
         (8, 17), (10, 23), (11, 26)]


def job(args):
    k, n, j, mode = args
    rng = random.Random(k * 100000 + n * 100 + j * 10 + ["none", "friend", "glance"].index(mode))
    finals, shares = 0, 0.0
    R = 24
    for t in range(R):
        fin, sh = run_mode(k, n, j, mode, rng)
        finals += fin
        shares += sh
    return dict(k=k, n=n, j=j, mode=mode, final=finals, runs=R, share=round(shares / R, 3))


if __name__ == "__main__":
    jobs = [(k, n, j, m) for (k, n) in CASES for j in (1, 2) for m in ("none", "friend", "glance")]
    with Pool(8) as p:
        res = p.map(job, jobs, chunksize=1)
    json.dump(res, open("far_drummer.json", "w"))
    for r in res:
        print(r)
