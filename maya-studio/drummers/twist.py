"""m = 1 at bigger k: where does the threshold sit, and are the misses twists?

A 'twist' here: the drummers' offsets from the even lattice wind once (or more)
around the ring, which shows up as a ramp in the gaps. Winding number is
computed from the gaps: q = round(sum of (gap - n/k) along the ramp...) is
awkward, so instead we count ramps directly: max gap - min gap >= 2 with
neighbouring gaps within 1.
"""
import random
import sys
from collections import Counter
from multiprocessing import Pool

from drummers import run, gaps_of, canon, euclid_gaps
from checks import kind

RUNS = 40


def job(args):
    k, n, j = args
    rng = random.Random(k * 1000 + j)
    E = euclid_gaps(k, n)
    c = Counter()
    for t in range(RUNS):
        pos, _ = run(k, n, j, rng)
        c[kind(gaps_of(pos, n), E)] += 1
    return k, n, j, dict(c)


if __name__ == "__main__":
    jobs = []
    for k in (24, 30, 36, 42):
        n = 2 * k + 1
        for j in range(int(0.22 * k), int(0.42 * k) + 1):
            jobs.append((k, n, j))
    with Pool(8) as p:
        for k, n, j, c in p.imap(job, jobs):
            print(k, n, "j", j, "j/k %.3f" % (j / k), c, flush=True)
