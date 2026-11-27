"""Screening in a corridor: a strip of width w, height H. Add a foot (an inverted T)
and see how far up the strip the zero changes."""
import numpy as np
from sandpile_zero import identity

H = 400
print("w   foot  reach(rows above foot)  reach/w")
for w in [8, 12, 16, 24, 32, 48]:
    for foot in [w, 3 * w]:
        W = 2 * foot + w + 4
        strip = np.zeros((H + foot + 4, W), bool)
        x0 = foot + 2
        strip[2:H + 2, x0:x0 + w] = True
        tee = strip.copy()
        tee[H + 2 - w:H + 2, 2:W - 2] = True  # foot of height w at the bottom
        ea, et = identity(strip), identity(tee)
        diff = (ea != et) & strip
        diff[H + 2 - w:, :] = False  # ignore the overlap with the foot
        rows = np.where(diff.any(1))[0]
        reach = (H + 2 - w) - rows.min() if rows.size else 0
        print(f"{w:<3} {foot:<5} {reach:<23} {reach / w:.2f}")
