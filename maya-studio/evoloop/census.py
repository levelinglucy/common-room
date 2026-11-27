"""Run Evoloop on a torus from the Golly seed and census loop sizes over time.

A loop = a square hole of 0s fully enclosed (component of 0 not touching the
background), recorded by its side. usage: census.py N STEPS EVERY SEED OUT
"""
import sys
import time
import json
import numpy as np
from scipy import ndimage
import evoloop as ev


def holes(g, max_area=900):
    zero = g == 0
    lab, n = ndimage.label(zero)  # 4-connectivity
    # torus wrap: merge labels across edges
    parent = np.arange(n + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for a, b in list(zip(lab[0], lab[-1])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
    roots = np.array([find(i) for i in range(n + 1)])
    lab = roots[lab]
    areas = np.bincount(lab.ravel())
    out = []
    sl = ndimage.find_objects(lab)
    for i, s in enumerate(sl, start=1):
        if s is None or areas[i] == 0 or areas[i] > max_area:
            continue
        h = s[0].stop - s[0].start
        w = s[1].stop - s[1].start
        if h == w and h >= 2 and areas[i] == h * w:
            out.append(h)
    return out


def main():
    N, steps, every = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    seed_rot = int(sys.argv[4])
    out = sys.argv[5]
    g = np.zeros((N, N), dtype=np.uint8)
    s = ev.parse_rle("../loops/Evoloop.rle")
    s = np.rot90(s, seed_rot % 4)
    g[N // 2:N // 2 + s.shape[0], N // 2:N // 2 + s.shape[1]] = s
    rec = []
    t0 = time.time()
    for t in range(steps + 1):
        if t % every == 0:
            hs = holes(g)
            cnt = {int(k): int(v) for k, v in zip(*np.unique(hs, return_counts=True))} if hs else {}
            live = int((g != 0).sum())
            rec.append({"t": t, "loops": cnt, "live": live})
            print(t, f"{time.time()-t0:.0f}s", live, cnt, flush=True)
        g = ev.step(g)
    json.dump(rec, open(out, "w"))
    np.save(out.replace(".json", "_final.npy"), g)


if __name__ == "__main__":
    main()
