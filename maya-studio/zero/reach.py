"""How far does joining the letters reach into the zero?
usage: python3 reach.py WORD size thicken
"""
import sys
import numpy as np
from scipy import ndimage
from word_zero import word_mask, with_bar
from sandpile_zero import identity

word, size, thick = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
m = word_mask(word, size, thick)
mj = with_bar(m)
ea, ej = identity(m), identity(mj)
bar = mj & ~m
d = ndimage.distance_transform_edt(~bar)
# only cells of letters that touch the bar (others are untouched components)
lab, n = ndimage.label(mj)
touch = np.isin(lab, np.unique(lab[bar]))
cells = m & touch
ch = (ea != ej) & cells
edges = [0, 5, 10, 20, 40, 80, 160, 10_000]
print(f"{word} size {size}: {cells.sum()} letter cells touching the bar")
for a, b in zip(edges[:-1], edges[1:]):
    sel = cells & (d > a) & (d <= b)
    if sel.any():
        print(f"  distance {a:>3}-{b:<5}: {sel.sum():>6} cells, changed {100*ch[sel].mean():5.1f}%")
print(f"  furthest changed cell: {d[ch].max():.0f} px from the bar; furthest letter cell {d[cells].max():.0f}")
np.save(f"zero_{word}_{size}_apart.npy", np.where(m, ea, -1))
np.save(f"zero_{word}_{size}_joined.npy", np.where(mj, ej, -1))
