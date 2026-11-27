"""Numbers about the ribbon before drawing anything."""
import numpy as np, sys
a, b = sys.argv[1], sys.argv[2]
d = np.load(f'ribbon_{a}_{b}.npz')
z, e1, tag = d['z'], d['e1'], d['tag']
print('e1 distinct values (rounded):', np.unique(np.round(e1, 6))[:10])
for v in np.unique(np.round(e1, 6)):
    m = np.round(e1, 6) == v
    print(f'  e1={v}: {m.sum()} points, tags {np.bincount(tag[m], minlength=4)}')
# overlap test on grids of several resolutions: the 4 tagged pieces
x, y = z.real, z.imag
for G in (100, 200, 400, 800):
    ix = ((x - x.min()) / (x.max() - x.min() + 1e-12) * (G - 1)).astype(int)
    iy = ((y - y.min()) / (y.max() - y.min() + 1e-12) * (G - 1)).astype(int)
    cell = ix * G + iy
    occ = np.zeros((G * G, 4), bool)
    occ[cell, tag] = True
    k = occ.sum(1)
    filled = (k > 0).sum()
    print(f'G={G}: filled cells {filled}, cells with 2+ tags {(k > 1).sum()} ({(k > 1).sum() / filled:.3%})')
# same test splitting by symbol only (a vs b)
sym = tag // 2
for G in (200, 800):
    ix = ((x - x.min()) / (x.max() - x.min() + 1e-12) * (G - 1)).astype(int)
    iy = ((y - y.min()) / (y.max() - y.min() + 1e-12) * (G - 1)).astype(int)
    cell = ix * G + iy
    occ = np.zeros((G * G, 2), bool); occ[cell, sym] = True
    k = occ.sum(1)
    print(f'by symbol G={G}: shared cells {(k > 1).sum() / (k > 0).sum():.3%}')
print('x range', x.min(), x.max(), 'y range', y.min(), y.max())
