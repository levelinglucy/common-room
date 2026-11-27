import numpy as np
from scipy import ndimage

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
