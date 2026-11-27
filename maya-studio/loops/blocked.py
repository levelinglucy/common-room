"""Why do colonies break when L divides by 3?  Controlled test: one founder
(arm 5) plus a dead neighbour (same size, genome all 1s, sealed) sitting on
lattice spots.  Does the founder's blocked arm leave debris?

usage: python3 blocked.py  -> prints a table over L and neighbour layouts
"""
import sys
import numpy as np
from multiprocessing import Pool
from scipy import ndimage
from build_loop import build, genome_of, holes
from langton import step

SPOTS = {"E": (0, 1), "N": (-1, 0), "W": (0, -1), "S": (1, 0)}


def dead(L):
    return build(L, [1] * (4 * (L - 1)), 0)


def setup(L, spots, N=None):
    sp = L + 3
    N = N or 8 * sp + 40
    g = np.zeros((N, N), np.uint8)
    r0 = c0 = N // 2 - sp // 2
    f = build(L, genome_of(L - 2, 2, L), 5)
    g[r0:r0 + f.shape[0], c0:c0 + f.shape[1]] = f
    d = dead(L)
    for k in spots:
        dr, dc = SPOTS[k]
        r, c = r0 + dr * sp, c0 + dc * sp
        g[r:r + d.shape[0], c:c + d.shape[1]] |= d
    return g, (r0, c0)


def verdict(g, L):
    st56 = int(((g == 5) | (g == 6)).sum())
    hs = holes(g)
    want = (L - 4) ** 2
    odd = [h for h in hs if h != want and h > 1]
    return st56, odd


def run(args):
    L, spots, T = args
    g, _ = setup(L, spots)
    trace = []
    for t in range(1, T + 1):
        g = step(g)
        if t % 100 == 0:
            trace.append(verdict(g, L))
    st56, odd = trace[-1]
    lasting56 = sum(1 for s, _ in trace[-5:] if s > 0)
    return L, spots, st56, odd, lasting56, int((g > 0).sum())


if __name__ == "__main__":
    layouts = sys.argv[1:] or ["", "E", "N", "W", "S", "EN"]
    jobs = [(L, s, 40 * L + 600) for L in range(8, 22) for s in layouts]
    with Pool(8) as p:
        for L, s, st56, odd, last, live in p.map(run, jobs):
            print(f"L={L:2d} mod3={L%3} nb={s or '-':3s} 5/6 now={st56:3d} in_last5={last} odd_holes={odd[:6]} live={live}", flush=True)
