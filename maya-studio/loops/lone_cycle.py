"""Lone matched loop: where does each child appear and when (bounding boxes of
closed loops, relative to the parent's core ring)."""
import sys
import numpy as np
from scipy import ndimage
from build_loop import build, genome_of
from langton import step

def closed_loops(g, L):
    lab, n = ndimage.label(g == 0)
    counts = np.bincount(lab.ravel())
    want = (L - 4) ** 2
    out = []
    for i in range(1, n + 1):
        if counts[i] == want:
            rr, cc = np.where(lab == i)
            out.append((int(rr.min()), int(cc.min())))
    return out

L = int(sys.argv[1]); T = int(sys.argv[2]) if len(sys.argv) > 2 else 600
N = 200
g = np.zeros((N, N), np.uint8)
p = build(L, genome_of(L - 2, 2, L), L - 3)
r0, c0 = 90, 90
g[r0:r0 + p.shape[0], c0:c0 + p.shape[1]] = p
seen = {}
for t in range(1, T + 1):
    g = step(g)
    for h in closed_loops(g, L):
        if h not in seen:
            seen[h] = t
for h, t in sorted(seen.items(), key=lambda x: x[1]):
    print("t=%d hole at dr=%d dc=%d" % (t, h[0] - (r0 + 3), h[1] - (c0 + 3)))
