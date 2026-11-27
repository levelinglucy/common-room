"""Re-run a torus and save snapshots every EVERY steps. usage: snapshots.py N STEPS EVERY"""
import sys
import numpy as np
import evoloop as ev

N, steps, every = map(int, sys.argv[1:4])
g = np.zeros((N, N), dtype=np.uint8)
s = ev.parse_rle("../loops/Evoloop.rle")
g[N // 2:N // 2 + s.shape[0], N // 2:N // 2 + s.shape[1]] = s
snaps = {}
for t in range(steps + 1):
    if t % every == 0:
        snaps[str(t)] = g.copy()
    g = ev.step(g)
np.savez_compressed(f"out/snaps_{N}.npz", **snaps)
print("saved", len(snaps))
