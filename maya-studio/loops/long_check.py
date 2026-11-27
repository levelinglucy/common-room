"""Longer runs: matched loops (s = L-2) over time, and whether a mismatched
parent's child ever lets go."""
import math
from collections import Counter
from multiprocessing import Pool
from build_loop import build, genome_of, holes, census
from langton import step, place


def sides(g):
    c = Counter()
    for a in holes(g):
        r = math.isqrt(a)
        if r * r == a and r >= 2:
            c[r + 4] += 1
        elif a > 1:
            c["odd"] += 1
    return dict(c)


def run(args):
    L, s, T, N = args
    g = place(build(L, genome_of(s, 2, L), max(L - 3, 1)), N)
    out = []
    for t in range(1, T + 1):
        g = step(g)
        if t % 500 == 0:
            n, _ = census(g)
            out.append((t, n, int((g > 0).sum()), sides(g)))
    return L, s, out


if __name__ == "__main__":
    jobs = [(L, L - 2, 3000, 520) for L in range(6, 17)]
    jobs += [(8, 5, 3000, 300), (8, 7, 3000, 300), (12, 8, 3000, 300), (10, 10, 3000, 300)]
    with Pool(6) as p:
        for L, s, out in p.map(run, jobs):
            print(f"L={L} s={s}")
            for row in out:
                print("   t=%d pieces=%d live=%d loops=%s" % row)
