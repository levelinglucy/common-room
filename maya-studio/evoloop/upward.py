"""Where do the 3s in a 2-only world come from? Re-run one 2-only torus
(same placement as race.py trial TR with vary), stop at step STEPS, read the
tapes of 2s and 3s, and cut each 3 out to see if it breeds 3s alone.
usage: upward.py TR STEPS
"""
import sys
import pickle
from collections import Counter
import numpy as np
from scipy import ndimage
import evoloop as ev
from census import holes
from tapes import ring, canon

TR, STEPS = int(sys.argv[1]), int(sys.argv[2])
F = pickle.load(open("out/founders_35k.pkl", "rb"))
f2 = F[2][0]["piece"]
rng = np.random.default_rng(1000 + TR)
N = 250 + 10 * TR
g = np.zeros((N, N), np.uint8)
p = np.rot90(f2, rng.integers(4))
r, c = rng.integers(0, N - p.shape[0], 2)
g[r:r + p.shape[0], c:c + p.shape[1]] = p
for t in range(STEPS):
    g = ev.step(g)
np.save(f"out/two_only_N{N}_t{STEPS}.npy", g)
lab, n = ndimage.label(g == 0)
areas = np.bincount(lab.ravel())
found = {2: [], 3: []}
for i, s in enumerate(ndimage.find_objects(lab), 1):
    h = s[0].stop - s[0].start
    if h in found and s[1].stop - s[1].start == h and areas[i] == h * h:
        r0, c0 = s[0].start, s[1].start
        if r0 >= 6 and c0 >= 6 and r0 + h + 6 <= N and c0 + h + 6 <= N:
            found[h].append((r0, c0))
print(f"N {N} step {STEPS}: {len(found[2])} twos, {len(found[3])} threes (away from edge)")
for H in (2, 3):
    tc = Counter(canon(ring(g, r0, c0, H)) for r0, c0 in found[H])
    for tp, k in tc.most_common(6):
        print(f"  hole {H} tape {tp} x{k}  (straight 7s: {tp.count('7')}, turns 4s: {tp.count('4')})")
fert = []
for r0, c0 in found[3]:
    piece = g[r0 - 3:r0 + 6, c0 - 3:c0 + 6].copy()
    M = 200
    h = np.zeros((M, M), np.uint8)
    h[M // 2:M // 2 + 9, M // 2:M // 2 + 9] = piece
    for t in range(1500):
        h = ev.step(h)
    fert.append(Counter(holes(h)).get(3, 0))
print("threes cut out, hole-3 loops after 1,500 steps alone:", sorted(fert))
