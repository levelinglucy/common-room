"""Overlap of a vs b inside each parity layer, and of the two layers."""
import numpy as np, sys
a, b = sys.argv[1], sys.argv[2]
d = np.load(f'ribbon_{a}_{b}.npz')
z, tag = d['z'], d['tag']
x, y = z.real, z.imag
for N in (250000, 1000000, len(z)):
    print(f'--- first {N} points')
    for G in (200, 400, 800, 1600):
        ix = ((x[:N] - x.min()) / (x.max() - x.min() + 1e-12) * (G - 1)).astype(int)
        iy = ((y[:N] - y.min()) / (y.max() - y.min() + 1e-12) * (G - 1)).astype(int)
        cell = ix * G + iy
        occ = np.zeros((G * G, 4), bool); occ[cell, tag[:N]] = True
        ev = occ[:, [0, 2]]; od = occ[:, [1, 3]]
        def share(o):
            k = o.sum(1); return (k > 1).sum() / max((k > 0).sum(), 1)
        layer = np.stack([ev.any(1), od.any(1)], 1)
        print(f'G={G}: even layer a/b shared {share(ev):.3%}, odd layer a/b shared {share(od):.3%}, even vs odd layer shared {share(layer):.3%}')
