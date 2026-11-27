"""Causal test. Run a lone founder (arm 5) until shortly before its east child's
westward arm reaches the founder's top-right corner, then roll the founder's
ring contents by k cells (k = 0, 1, 2: shifts which part of the 7-0-1 triplet
sits at the corner when the arm lands). Then see whether the founder is
flooded with 7s and whether the lasting 2-cell hole forms at (2, L).

usage: python3 phase_shift.py
"""
import numpy as np
from multiprocessing import Pool
from scipy import ndimage
from build_loop import build, genome_of, ring_upstream
from langton import step

N = 400
r0 = c0 = N // 2


def contact_time(L):
    g = np.zeros((N, N), np.uint8)
    f = build(L, genome_of(L - 2, 2, L), 5)
    g[r0:r0 + f.shape[0], c0:c0 + f.shape[1]] = f
    for t in range(1, 3000):
        g = step(g)
        if t > 50 and g[r0 + 1, c0 + L + 2] != 0:
            return t


def corner_state(g, L):
    return int(g[r0 + 1, c0 + L])  # founder's top-right core cell


def run(args):
    L, k, lead = args
    tc = contact_time(L)
    g = np.zeros((N, N), np.uint8)
    f = build(L, genome_of(L - 2, 2, L), 5)
    g[r0:r0 + f.shape[0], c0:c0 + f.shape[1]] = f
    t = 0
    while t < tc - lead:
        g = step(g); t += 1
    ring = [(r0 + r, c0 + c) for r, c in ring_upstream(L)]
    vals = [g[p] for p in ring]
    if k:
        vals = vals[k:] + vals[:k]  # advance the stream by k cells
        for p, v in zip(ring, vals):
            g[p] = v
    corner_at_contact = None
    flood = 0
    hole = None
    for _ in range(lead + 300):
        g = step(g); t += 1
        if corner_at_contact is None and g[r0 + 1, c0 + L + 2] != 0:
            corner_at_contact = corner_state(g, L)
        if t == tc + 40:
            flood = sum(1 for p in ring if g[p] == 7)
    lab, n = ndimage.label(g == 0)
    cnt = np.bincount(lab.ravel())
    i = lab[r0 + 2, c0 + L]
    hole = int(cnt[i]) if g[r0 + 2, c0 + L] == 0 and i > 0 else 0
    st56 = int(((g[r0 - 2:r0 + L + 4, c0 - 2:c0 + 2 * L + 8] == 5) |
                (g[r0 - 2:r0 + L + 4, c0 - 2:c0 + 2 * L + 8] == 6)).sum())
    return L, k, tc, corner_at_contact, flood, hole, st56, 4 * (L - 1)


if __name__ == "__main__":
    jobs = [(L, k, 12) for L in range(8, 22) for k in (0, 1, 2, 3, 4, 5)]
    with Pool(8) as p:
        for L, k, tc, cs, flood, hole, st56, P in p.map(run, jobs):
            print(f"L={L:2d} mod3={L%3} shift={k} contact t={tc} corner_state_at_contact={cs} "
                  f"7s_in_founder_ring@+40={flood:3d}/{P} hole_at(2,L)={hole} 5/6_nearby@+300={st56}", flush=True)
