"""The east child sends an arm back west along the shared top row and runs
into the founder's top-right corner. Watch that moment for any L.
usage: python3 hit_parent.py L [frames_after]"""
import sys
import numpy as np
from build_loop import build, genome_of
from langton import step

L = int(sys.argv[1])
after = int(sys.argv[2]) if len(sys.argv) > 2 else 3
N = 400
g = np.zeros((N, N), np.uint8)
f = build(L, genome_of(L - 2, 2, L), 5)
r0 = c0 = N // 2
g[r0:r0 + f.shape[0], c0:c0 + f.shape[1]] = f
sp = L + 3


def show(g, t):
    print(f"--- t={t}")
    for rr in range(r0 - 3, r0 + L + 4):
        print("".join("." if v == 0 else str(v) for v in g[rr, c0 - 1:c0 + 2 * sp + 1]))


hit = None
for t in range(1, 3000):
    prev = g
    g = step(g)
    # founder corner cell (r0+1, c0+L+1) is outer sheath (2); the arm turns it
    if hit is None and t > 50 and g[r0 + 1, c0 + L + 2] != 0:
        hit = t
        show(prev, t - 1)
    if hit is not None and t in (hit, hit + 10, hit + 20, hit + 40, hit + 80)[:after + 2]:
        show(g, t)
    if hit is not None and t > hit + 80:
        break
print("hit at", hit)
