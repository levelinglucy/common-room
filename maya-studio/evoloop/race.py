"""2 vs 3: three conditions on a torus, census every EVERY steps.

founders from out/founders_35k.pkl (fertile alone). condition:
  two   - one hole-2 founder
  three - one hole-3 founder (tape 011117017014014017017017)
  both  - one of each, at random places and rotations
usage: race.py COND TRIALS N STEPS EVERY OUT.json [vary]
  vary: torus side N + 10*trial (single-founder runs are otherwise identical up to rotation)
"""
import sys
import json
import pickle
import numpy as np
import evoloop as ev
from census import holes

cond, trials, N0, steps, every, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
vary = len(sys.argv) > 7 and sys.argv[7] == "vary"
F = pickle.load(open("out/founders_35k.pkl", "rb"))
f2 = F[2][0]["piece"]
f3 = [f for f in F[3] if f["tape"] == "011117017014014017017017"][0]["piece"]
pieces = {"two": [f2], "three": [f3], "both": [f2, f3]}[cond]
res = []
for tr in range(trials):
    rng = np.random.default_rng(1000 + tr)
    N = N0 + 10 * tr if vary else N0
    g = np.zeros((N, N), np.uint8)
    spots = []
    for p in pieces:
        p = np.rot90(p, rng.integers(4))
        while True:
            r, c = rng.integers(0, N - p.shape[0], 2)
            if all(abs(r - a) > 40 and abs(c - b) > 40 for a, b in spots) or not spots:
                break
        spots.append((r, c))
        g[r:r + p.shape[0], c:c + p.shape[1]] = np.maximum(g[r:r + p.shape[0], c:c + p.shape[1]], p)
    rec = []
    for t in range(steps + 1):
        if t % every == 0:
            hs = holes(g)
            rec.append({int(k): int(v) for k, v in zip(*np.unique(hs, return_counts=True))} if hs else {})
        g = ev.step(g)
    res.append(rec)
    last = rec[-1]
    print(cond, tr, "N", N, "end", last, " mid", rec[len(rec) // 2], flush=True)
json.dump(res, open(outp, "w"))
