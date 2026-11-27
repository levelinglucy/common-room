"""one_far_friend.py: can one long link per bird stop the count-seven gangs?

The count-7 flock in seven_neighbours.py closes into gangs of ~2K birds that
only hear each other. Here each bird keeps 6 nearest and spends its seventh
slot on one bird chosen another way:
  near7   -> 7 nearest (the original, for comparison)
  friend  -> 6 nearest + one fixed 'friend' picked at random at the start, kept all run
  glance  -> 6 nearest + one random bird, re-picked every step
  glanceP -> same, but each bird only glances with probability P per step (e.g. glance0.05)
  far     -> 6 nearest + the bird furthest away
Calm 2D flocks, same forces and starts as seven_neighbours.py.
usage: python3 one_far_friend.py MODE SEEDS [STEPS]
"""
import sys
import numpy as np
import seven_neighbours as s

MODE = sys.argv[1]
P_GLANCE = float(MODE[6:]) if MODE.startswith("glance") and len(MODE) > 6 else 1.0
seeds = int(sys.argv[2])
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 600
state = {}


def mask(D, mode, R):
    n = D.shape[0]
    Dd = D.copy()
    np.fill_diagonal(Dd, np.inf)
    k = 7 if MODE == "near7" else 6
    idx = np.argpartition(Dd, k, axis=1)[:, :k]
    m = np.zeros_like(D, dtype=bool)
    m[np.arange(n)[:, None], idx] = True
    rows = np.arange(n)
    if MODE == "friend":
        m[rows, state["friend"]] = True
    elif MODE.startswith("glance"):
        g = (rows + state["rng"].integers(1, n, n)) % n
        who = state["rng"].random(n) < P_GLANCE
        m[rows[who], g[who]] = True
    elif MODE == "far":
        Df = D.copy()
        np.fill_diagonal(Df, -1)
        m[rows, Df.argmax(1)] = True
    return m


s.neighbour_mask = mask
rows_out = []
for seed in range(seeds):
    rng = np.random.default_rng(1000 + seed)
    x, h = s.init(rng)
    state["rng"] = np.random.default_rng(5000 + seed)
    state["friend"] = (np.arange(s.N) + state["rng"].integers(1, s.N, s.N)) % s.N
    for t in range(steps):
        x, h, cnt = s.step(x, h, "topological", 0.0, rng)
    lab, sizes = s.components(x, s.LINK)
    spread = np.linalg.norm(x - x.mean(0), axis=1).mean()
    pol = np.linalg.norm(h.mean(0))
    D = np.linalg.norm(x[None] - x[:, None], axis=-1); np.fill_diagonal(D, np.inf)
    nn = D.min(1).mean()
    rows_out.append((sizes[0] / s.N, int((sizes >= 5).sum()), spread, pol, nn))
    print(f"{MODE} seed {seed}: largest {sizes[0]/s.N:.2f} pieces {int((sizes>=5).sum())} mean dist from centre {spread:.1f} polarisation {pol:.2f} nn dist {nn:.2f}", flush=True)
L = np.array([r[0] for r in rows_out]); P = np.array([r[1] for r in rows_out]); S = np.array([r[2] for r in rows_out]); Po = np.array([r[3] for r in rows_out]); NN = np.array([r[4] for r in rows_out])
print(f"SUMMARY {MODE}: whole {int((L>=0.95).sum())}/{seeds} | mean largest {L.mean():.2f} | mean pieces {P.mean():.1f} | mean dist from centre {S.mean():.1f} | polarisation {Po.mean():.2f} | nn dist {NN.mean():.2f}", flush=True)
