"""Harvest one isolated-looking loop of each hole size from snapshots and run it
alone on an empty torus: does it breed, how fast, and do children keep its size?

usage: alone.py N(snap torus) T(steps alone)
"""
import sys
import numpy as np
from scipy import ndimage
import evoloop as ev
from census import holes

N, T = int(sys.argv[1]), int(sys.argv[2])
snaps = np.load(f"out/snaps_{N}.npz")
keys = sorted(snaps.files, key=int)


def candidates(g):
    lab, n = ndimage.label(g == 0)
    areas = np.bincount(lab.ravel())
    for i, s in enumerate(ndimage.find_objects(lab), 1):
        h = s[0].stop - s[0].start
        w = s[1].stop - s[1].start
        if h == w and h >= 2 and areas[i] == h * w:
            yield h, s[0].start, s[1].start


def cut(g, h, r, c):
    # loop body: hole h, inner sheath, core, outer sheath => h+6 square
    r0, c0 = r - 3, c - 3
    size = h + 6
    if r0 < 0 or c0 < 0 or r0 + size > g.shape[0] or c0 + size > g.shape[1]:
        return None
    return g[r0:r0 + size, c0:c0 + size].copy()


def trial(piece, h, M=240, T=3000):
    g = np.zeros((M, M), dtype=np.uint8)
    g[M // 2:M // 2 + piece.shape[0], M // 2:M // 2 + piece.shape[1]] = piece
    first_two = None
    hist = []
    for t in range(T + 1):
        if t % 25 == 0:
            hs = holes(g)
            same = sum(1 for x in hs if x == h)
            if first_two is None and same >= 2:
                first_two = t
            if t % 500 == 0:
                vals, cts = np.unique(hs, return_counts=True) if hs else ([], [])
                hist.append((t, dict(zip(map(int, vals), map(int, cts)))))
        g = ev.step(g)
    return first_two, hist


done = set()
tries = {}
for k in keys:
    g = snaps[k]
    for h, r, c in candidates(g):
        if h in done or tries.get(h, 0) >= 8:
            continue
        piece = cut(g, h, r, c)
        if piece is None:
            continue
        # the piece must be a whole loop: its border rows mostly sheath/empty,
        # and the piece alone must still show the hole
        if holes(np.pad(piece, 5)) != [h]:
            continue
        tries[h] = tries.get(h, 0) + 1
        first_two, hist = trial(piece, h, T=T)
        if hist[-1][1].get(h, 0) >= 3:  # it bred true at least twice
            done.add(h)
            np.save(f"out/loop_hole{h}.npy", piece)
            print(f"hole {h} (from t={k}): first child of same size by t={first_two}; census {hist}", flush=True)
print("sizes that bred alone:", sorted(done))
print("tries per size:", dict(sorted(tries.items())))
