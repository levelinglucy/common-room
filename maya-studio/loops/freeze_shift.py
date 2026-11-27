"""Cleaner causal test than phase_shift.py (which rolled the founder's ring and
broke its outgoing arm). Here everything left of the 1-cell gap between the
founder and its east child is frozen for k steps, so the founder's whole side
of the colony is delayed by k, consistently, and the east child's arm lands on
a different part of the founder's 7-0-1 stream. Checks the gap column stays
empty during the freeze (otherwise the freeze would cut something).

usage: python3 freeze_shift.py
"""
import numpy as np
from multiprocessing import Pool
from scipy import ndimage
from build_loop import build, genome_of, ring_upstream
from langton import step

N = 400
r0 = c0 = N // 2


def fresh(L):
    g = np.zeros((N, N), np.uint8)
    f = build(L, genome_of(L - 2, 2, L), 5)
    g[r0:r0 + f.shape[0], c0:c0 + f.shape[1]] = f
    return g


def contact_time(L):
    g = fresh(L)
    for t in range(1, 3000):
        g = step(g)
        if t > 50 and g[r0 + 1, c0 + L + 2] != 0:
            return t


def run(args):
    L, k, lead = args
    tc = contact_time(L)
    g = fresh(L)
    t = 0
    while t < tc - lead:
        g = step(g); t += 1
    gapc = c0 + L + 2
    clean_cut = True
    for _ in range(k):
        new = step(g)
        new[:, :gapc] = g[:, :gapc]          # left side holds still
        if new[:, gapc].any() or g[:, gapc].any():
            clean_cut = False
        g = new
    ring = [(r0 + r, c0 + c) for r, c in ring_upstream(L)]
    cs = None
    flood = 0
    for _ in range(lead + 400):
        g = step(g); t += 1
        if cs is None and g[r0 + 1, gapc] != 0:
            cs = int(g[r0 + 1, c0 + L])
            tcont = t
        if cs is not None and t == tcont + 40:
            flood = sum(1 for p in ring if g[p] == 7)
    lab, n = ndimage.label(g == 0)
    cnt = np.bincount(lab.ravel())
    i = lab[r0 + 2, c0 + L]
    hole = int(cnt[i]) if g[r0 + 2, c0 + L] == 0 and i > 0 else 0
    box = g[r0 - 2:r0 + L + 4, c0 - 2:c0 + 2 * L + 8]
    st56 = int(((box == 5) | (box == 6)).sum())
    return L, k, clean_cut, cs, flood, 4 * (L - 1), hole, st56


if __name__ == "__main__":
    jobs = [(L, k, 30) for L in range(8, 22) for k in range(0, 6)]
    with Pool(8) as p:
        for L, k, cut, cs, flood, P, hole, st56 in p.map(run, jobs):
            print(f"L={L:2d} mod3={L%3} delay={k} cut_ok={cut} corner_at_contact={cs} "
                  f"7s@+40={flood:3d}/{P} hole_at(2,L)={hole} 5/6_nearby@+400={st56}", flush=True)
