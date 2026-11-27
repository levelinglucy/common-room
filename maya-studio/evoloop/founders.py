"""Collect fertile founders of hole 2 and hole 3 from the same world moment.

Takes the 600 world at step 35,000 (2s and 3s side by side), cuts each loop
with 3 cells of margin, runs it alone on a 200 torus for 1,500 steps, and
keeps the ones that grow a colony (>= 4 loops of their own size at the end).
Also records each founder's tape and its births over time.
usage: founders.py COUNT_PER_SIZE
"""
import sys
import pickle
import numpy as np
from scipy import ndimage
import evoloop as ev
from census import holes


def ring(g, r, c, H):
    a, b = r - 2, r + H + 1
    l, rr = c - 2, c + H + 1
    top = [g[a, j] for j in range(l, rr + 1)]
    right = [g[i, rr] for i in range(a + 1, b + 1)]
    bot = [g[b, j] for j in range(rr - 1, l - 1, -1)]
    left = [g[i, l] for i in range(b - 1, a, -1)]
    return [int(x) for x in top + right + bot + left]


def canon(seq):
    s = "".join(map(str, seq))
    return min(s[i:] + s[:i] for i in range(len(s)))

COUNT = int(sys.argv[1])
w = np.load("out/snaps_600.npz")["35000"]
lab, n = ndimage.label(w == 0)
areas = np.bincount(lab.ravel())
sites = {2: [], 3: []}
for i, s in enumerate(ndimage.find_objects(lab), 1):
    h = s[0].stop - s[0].start
    if h in sites and s[1].stop - s[1].start == h and areas[i] == h * h:
        r, c = s[0].start, s[1].start
        if r >= 6 and c >= 6 and r + h + 6 <= 600 and c + h + 6 <= 600:
            sites[h].append((r, c))
rng = np.random.default_rng(7)
out = {}
for H in (2, 3):
    rng.shuffle(sites[H])
    keep = []
    tapes = {}
    for r, c in sites[H][:COUNT]:
        piece = w[r - 3:r + H + 3, c - 3:c + H + 3].copy()
        tape = canon(ring(w, r, c, H))
        tapes[tape] = tapes.get(tape, 0) + 1
        M = 200
        g = np.zeros((M, M), np.uint8)
        g[M // 2:M // 2 + piece.shape[0], M // 2:M // 2 + piece.shape[1]] = piece
        curve = []
        for t in range(1501):
            if t % 50 == 0:
                curve.append(sum(1 for x in holes(g) if x == H))
            g = ev.step(g)
        if curve[-1] >= 4:
            keep.append({"piece": piece, "tape": tape, "curve": curve})
    print(f"hole {H}: {len(sites[H])} in world, tested {min(COUNT, len(sites[H]))}, fertile {len(keep)}")
    for tp, k in sorted(tapes.items(), key=lambda kv: -kv[1]):
        print("   tape", tp, "x", k)
    for f in keep[:5]:
        print("   fertile", f["tape"], "curve", f["curve"])
    out[H] = keep
pickle.dump(out, open("out/founders_35k.pkl", "wb"))
