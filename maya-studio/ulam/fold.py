"""fold.py: fold U(1,b) by its own hidden period and compare the shapes.
Prints, for each b, the period, mean cos, and the occupied phase range (terms > 50b),
plus the L1 distance between each folded histogram and b = 30's.
"""
import re
import numpy as np

BS = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 25, 30]
BINS = 120

def alpha_of(b):
    txt = open(f"spec_u1_{b}.txt").read()
    return float(re.search(r"refined: alpha ([0-9.]+)", txt).group(1))

def folded(b):
    u = np.loadtxt(f"u1_{b}.txt", dtype=np.int64)
    a = alpha_of(b)
    ph = (a * u.astype(float)) % (2 * np.pi) / (2 * np.pi)
    return u, a, ph

if __name__ == "__main__":
    hists = {}
    for b in BS:
        u, a, ph = folded(b)
        late = ph[u > 50 * b]
        h, _ = np.histogram(ph, bins=BINS, range=(0, 1), density=True)
        hists[b] = h
        occ = np.sort(late)
        # widest empty arc on the circle for late terms
        gaps = np.diff(np.concatenate([occ, [occ[0] + 1]]))
        g = gaps.max()
        print(f"b={b:2d} P={2*np.pi/a:.6f} P-3b={2*np.pi/a-3*b:.6f} n={len(u)} meancos={np.cos(2*np.pi*ph).mean():+.4f} empty arc (terms>50b)={g:.3f}")
    ref = hists[30]
    for b in BS:
        print(f"  L1 distance of b={b} histogram to b=30: {np.abs(hists[b]-ref).sum()/BINS:.3f}")
    np.save("fold_hists.npy", np.array([hists[b] for b in BS]))
