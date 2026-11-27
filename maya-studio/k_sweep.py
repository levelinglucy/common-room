"""k_sweep.py: does a count-K flock stop breaking into gangs at some K?

Calm flocks only (no hawk). For each K, run WARM+extra steps from the same
starts as seven_neighbours.py and record:
  - largest spatial piece (link < 3) as a fraction of the flock
  - number of spatial pieces of size >= 5
  - number of weakly connected components of the K-nearest 'who listens to whom' graph
usage: python3 k_sweep.py K SEEDS [STEPS]
"""
import sys
import numpy as np
import seven_neighbours as s


def graph_components(x, K):
    D = np.linalg.norm(x[None] - x[:, None], axis=-1)
    np.fill_diagonal(D, np.inf)
    idx = np.argpartition(D, K, axis=1)[:, :K]
    n = len(x)
    A = np.zeros((n, n), bool)
    A[np.arange(n)[:, None], idx] = True
    A = A | A.T
    lab = -np.ones(n, int)
    c = 0
    for st in range(n):
        if lab[st] >= 0:
            continue
        stack = [st]
        lab[st] = c
        while stack:
            i = stack.pop()
            for j in np.nonzero(A[i] & (lab < 0))[0]:
                lab[j] = c
                stack.append(j)
        c += 1
    return c


K = int(sys.argv[1])
seeds = int(sys.argv[2])
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 600
s.K = K
rows = []
for seed in range(seeds):
    rng = np.random.default_rng(1000 + seed)
    x, h = s.init(rng)
    gc_trace = []
    for t in range(steps):
        x, h, cnt = s.step(x, h, "topological", 0.0, rng)
        if t in (49, 99, 299, steps - 1):
            gc_trace.append(graph_components(x, K))
    lab, sizes = s.components(x, s.LINK)
    rows.append((sizes[0] / s.N, int((sizes >= 5).sum()), gc_trace))
    print(f"K={K} seed {seed}: largest {sizes[0]/s.N:.2f} pieces {int((sizes>=5).sum())} graph comps at t50/100/300/{steps} {gc_trace}", flush=True)
L = np.array([r[0] for r in rows])
P = np.array([r[1] for r in rows])
G = np.array([r[2][-1] for r in rows])
print(f"SUMMARY K={K}: whole {int((L>=0.95).sum())}/{seeds} | mean largest {L.mean():.2f} | mean pieces {P.mean():.1f} | mean graph comps at end {G.mean():.1f} (graph connected {int((G==1).sum())}/{seeds})", flush=True)
