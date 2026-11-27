"""Sweep (k, n): hit rate of the Euclidean rhythm for each listening reach j."""
import json
import random
import sys
from multiprocessing import Pool

from drummers import run, gaps_of, canon, euclid_gaps, depth

RUNS = 40


def job(args):
    k, n = args
    E = euclid_gaps(k, n)
    rng = random.Random(1000 * n + k)
    rates = {}
    for j in range(1, k // 2 + 2):
        hits = 0
        for t in range(RUNS):
            pos, sw = run(k, n, j, rng)
            hits += canon(gaps_of(pos, n)) == E
        rates[j] = hits
        if hits == RUNS and j >= 2 and rates.get(j - 1) == RUNS:
            break
    jmin = min([j for j, h in rates.items() if h == RUNS], default=None)
    return dict(k=k, n=n, euclid=E, depth=depth(k, n), rates=rates, jmin=jmin)


if __name__ == "__main__":
    nmax = int(sys.argv[1])
    pairs = [(k, n) for n in range(5, nmax + 1) for k in range(2, n // 2 + 1)
             if n % k != 0]
    with Pool(8) as p:
        res = p.map(job, pairs, chunksize=1)
    with open(f"sweep_n{nmax}.json", "w") as fh:
        json.dump(res, fh)
    for r in res:
        print(r["k"], r["n"], "depth", r["depth"], "jmin", r["jmin"], r["rates"])
