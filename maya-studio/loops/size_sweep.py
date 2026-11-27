"""Which (loop side L, straight genes s) pairs breed true?

For each pair, build the loop with arm L-3 (as in the canonical seed), run it,
and record the enclosed holes: a finished loop of side L' leaves an empty
(L'-4)^2 hole, so hole sizes tell us the sizes of the loops that exist.
"""
import sys
import json
import math
from collections import Counter
from multiprocessing import Pool
import numpy as np
from build_loop import build, genome_of, holes, census
from langton import step, place

T = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
N = 320


def run(args):
    L, s, arm = args
    gen = genome_of(s, 2, L)
    if gen is None:
        return None
    g = place(build(L, gen, arm), N)
    first_split = None
    for t in range(1, T + 1):
        g = step(g)
        if first_split is None and t % 5 == 0:
            n, _ = census(g)
            if n >= 2:
                first_split = t
    h = holes(g)
    sides = Counter()
    for a in h:
        r = math.isqrt(a)
        if r * r == a:
            sides[r + 4] += 1
        else:
            sides["odd"] += 1
    n, _ = census(g)
    return dict(L=L, s=s, arm=arm, pieces=n, live=int((g > 0).sum()),
                first_split=first_split, loops_by_side={str(k): v for k, v in sides.items()})


if __name__ == "__main__":
    jobs = []
    for L in range(5, 17):
        P = 4 * (L - 1)
        for s in range(0, P // 3):
            if 3 * (s + 2) <= P:
                jobs.append((L, s, max(L - 3, 1)))
    with Pool(4) as pool:
        res = [r for r in pool.map(run, jobs) if r]
    json.dump(res, open(f"size_sweep_T{T}.json", "w"), indent=1)
    for r in res:
        same = r["loops_by_side"].get(str(r["L"]), 0)
        print(r["L"], r["s"], "split", r["first_split"], "pieces", r["pieces"],
              "same-size loops", same, "all", r["loops_by_side"])
