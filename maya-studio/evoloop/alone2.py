"""Cut many loops of one hole size out of a world and run each alone.
usage: alone2.py WORLD.npy HOLE COUNT PAD T
PAD: extra cells around the h+6 body (picks up the arm, and maybe neighbour bits).
Reports, per loop: max loops of that size seen at once, and how many at the end.
"""
import sys
import numpy as np
from scipy import ndimage
import evoloop as ev
from census import holes

path, H, COUNT, PAD, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
w = np.load(path)
if path.endswith(".npz"):
    raise SystemExit("give an .npy world")
lab, n = ndimage.label(w == 0)
areas = np.bincount(lab.ravel())
sites = []
for i, s in enumerate(ndimage.find_objects(lab), 1):
    h = s[0].stop - s[0].start
    if h == H and s[1].stop - s[1].start == H and areas[i] == H * H:
        r, c = s[0].start, s[1].start
        if r - 3 - PAD >= 0 and c - 3 - PAD >= 0 and r + H + 3 + PAD <= w.shape[0] and c + H + 3 + PAD <= w.shape[1]:
            sites.append((r, c))
rng = np.random.default_rng(0)
rng.shuffle(sites)
res = []
for r, c in sites[:COUNT]:
    piece = w[r - 3 - PAD:r + H + 3 + PAD, c - 3 - PAD:c + H + 3 + PAD].copy()
    M = 200
    g = np.zeros((M, M), np.uint8)
    g[M // 2:M // 2 + piece.shape[0], M // 2:M // 2 + piece.shape[1]] = piece
    mx = 0
    for t in range(T + 1):
        if t % 20 == 0:
            k = sum(1 for x in holes(g) if x == H)
            mx = max(mx, k)
        g = ev.step(g)
    end = sum(1 for x in holes(g) if x == H)
    res.append((mx, end))
mx = np.array([a for a, b in res])
end = np.array([b for a, b in res])
print(f"hole {H}, pad {PAD}, {len(res)} loops, {T} steps alone")
print("max at once:", sorted(mx.tolist()))
print("at end:", sorted(end.tolist()))
print("bred (max>=2):", int((mx >= 2).sum()), " still alive at end:", int((end >= 1).sum()), " growing colony (end>=4):", int((end >= 4).sum()))
