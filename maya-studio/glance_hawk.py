"""glance_hawk.py: the hawk test from seven_experiment.py, for the glance rules.
usage: python3 glance_hawk.py P SEEDS   (P = chance per step that a bird glances at one random bird)
"""
import sys
import numpy as np
import seven_neighbours as s

P = float(sys.argv[1])
seeds = int(sys.argv[2])
G = {}


def mask(D, mode, R):
    n = D.shape[0]
    Dd = D.copy()
    np.fill_diagonal(Dd, np.inf)
    idx = np.argpartition(Dd, 6, axis=1)[:, :6]
    m = np.zeros_like(D, dtype=bool)
    rows = np.arange(n)
    m[rows[:, None], idx] = True
    g = (rows + G["rng"].integers(1, n, n)) % n
    who = G["rng"].random(n) < P
    m[rows[who], g[who]] = True
    return m


s.neighbour_mask = mask
rows_out = []
for seed in range(seeds):
    G["rng"] = np.random.default_rng(5000 + seed)
    r = s.run("topological", 0.0, 1000 + seed, hawk_on=True)
    rows_out.append(r)
    print(f"glance P={P} seed {seed}: calm largest {r['calm_largest']:.2f} -> after hawk largest {r['largest']:.2f}, pieces {r['pieces']}, strays {r['strays']}", flush=True)
f = lambda k: np.array([r[k] for r in rows_out], float)
wb = f('calm_largest') >= 0.95
wa = f('largest') >= 0.95
print(f"SUMMARY glance P={P}: whole before hawk {wb.sum()}/{seeds} | whole after {wa.sum()}/{seeds} | broken by hawk {(wb & ~wa).sum()} | mean largest after {f('largest').mean():.2f} | mean pieces {f('pieces').mean():.1f} | scared bird-steps {f('scared').mean():.0f}", flush=True)
