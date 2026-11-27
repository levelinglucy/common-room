"""Lone founder (arm 5), big grid (no wrap). Find the first step at which a
lasting small odd hole (size 2) appears, and print the scene around it a few
frames before. usage: python3 first_hole.py L [pad]"""
import sys
import numpy as np
from scipy import ndimage
from build_loop import build, genome_of
from langton import step

L = int(sys.argv[1])
N = 400
g = np.zeros((N, N), np.uint8)
f = build(L, genome_of(L - 2, 2, L), 5)
r0 = c0 = N // 2
g[r0:r0 + f.shape[0], c0:c0 + f.shape[1]] = f
hist = []
seen = {}
for t in range(1, 1500):
    g = step(g)
    hist.append(g.copy())
    hist = hist[-80:]
    lab, n = ndimage.label(g == 0)
    cnt = np.bincount(lab.ravel())
    for i in np.where(cnt == 2)[0]:
        rr, cc = np.where(lab == i)
        key = (int(rr.min()), int(cc.min()))
        seen.setdefault(key, t)
    # lasting: present now and since 30 steps ago
    old = [k for k, t0 in seen.items() if t - t0 >= 30]
    alive = []
    for k in old:
        r, c = k
        if g[r, c] == 0 and lab[r, c] > 0 and cnt[lab[r, c]] == 2:
            alive.append(k)
    if alive:
        r, c = alive[0]
        t0 = seen[(r, c)]
        print(f"L={L}: lasting 2-hole at {(r - r0, c - c0)} (rel. founder corner), formed t={t0}; founder lattice spacing {L+3}")
        for back in (60, 40, 20, 0):
            idx = len(hist) - 1 - (t - t0) - 1 + 1 - back + 0
            idx = max(0, min(len(hist) - 1, len(hist) - 1 - (t - t0) - back + 20))
            fr = hist[idx]
            tt = t - (len(hist) - 1 - idx)
            print(f"--- t={tt}")
            for rr in range(r - 12, r + 13):
                print("".join("." if v == 0 else str(v) for v in fr[rr, c - 22:c + 23]))
        break
