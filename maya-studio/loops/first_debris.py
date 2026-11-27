"""Run a matched colony (founder arm 5) and stop at the first odd-shaped hole
or stray piece; print where it formed and the cells around it."""
import sys, math
import numpy as np
from scipy import ndimage
from build_loop import build, genome_of
from langton import step, place

L = int(sys.argv[1]); N = 400
g = place(build(L, genome_of(L - 2, 2, L), 5), N)
want = (L - 4) ** 2
seen = {}
hist = []
for t in range(1, 3001):
    g = step(g)
    hist.append(g.copy()); hist = hist[-200:]
    if t % 2:
        continue
    lab, n = ndimage.label(g == 0)
    cnt = np.bincount(lab.ravel())
    big = cnt[1:].argmax() + 1
    bad = [i for i in range(1, n + 1) if i != big and cnt[i] != want and cnt[i] > 1]
    keys = set()
    for b in bad:
        rr, cc = np.where(lab == b)
        keys.add((int(cnt[b]), int(rr.mean()), int(cc.mean())))
    for k in keys:
        seen.setdefault(k, t)
    stuck = [k for k in keys if t - seen[k] >= 80]
    if stuck:
        size, r, c = stuck[0]
        t0 = seen[stuck[0]]
        bad = [None]
        print(f"L={L} first lasting odd hole formed by t={t0}, size {size}, centre ({r-N//2},{c-N//2}) from grid centre")
        w = L + 4
        for back in (t - t0 + 60, t - t0 + 20, t - t0):
            h = hist[-1 - back]
            print(f"--- t={t-back}")
            sub = h[max(r - w, 0):r + w, max(c - w, 0):c + w]
            for row in sub:
                print("".join("." if v == 0 else str(v) for v in row))
        break
