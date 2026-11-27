"""seven_3d.py: count-K flocking in 3D. Does the extra dimension stop the gangs?

Same forces as seven_neighbours.py (repulsion < 1, alignment + attraction to the
K nearest, constant speed 0.5, max turn 0.5 rad), but birds live in 3D.
Noise: a random kick of size ~0.15 rad added to the new heading.
Calm flocks only. Records largest spatial piece (link < 3), pieces >= 5, and
weak components of the K-nearest graph.
usage: python3 seven_3d.py K SEEDS [STEPS]
"""
import sys
import numpy as np

N = 300
SPEED = 0.5
R_REP = 1.0
MAX_TURN = 0.5
NOISE = 0.15
LINK = 3.0


def unit(v):
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    n[n == 0] = 1.0
    return v / n


def knn(D, K):
    Dd = D.copy()
    np.fill_diagonal(Dd, np.inf)
    idx = np.argpartition(Dd, K, axis=1)[:, :K]
    m = np.zeros(D.shape, bool)
    m[np.arange(len(D))[:, None], idx] = True
    return m


def step(x, h, K, rng):
    diff = x[None] - x[:, None]
    D = np.linalg.norm(diff, axis=-1)
    nb = knn(D, K)
    Ds = D.copy()
    np.fill_diagonal(Ds, np.inf)
    toward = diff / Ds[..., None]
    rep = -(toward * (Ds < R_REP)[..., None]).sum(1)
    align = (h[None] * nb[..., None]).sum(1) / K
    coh = (toward * nb[..., None]).sum(1) / K
    want = unit(unit(align) + unit(coh) + rep + 1e-9 * h)
    # rotate h toward want by at most MAX_TURN
    cosang = np.clip((h * want).sum(1), -1, 1)
    ang = np.arccos(cosang)
    perp = unit(want - cosang[:, None] * h)
    a = np.minimum(ang, MAX_TURN)[:, None]
    hn = np.cos(a) * h + np.sin(a) * perp
    kick = rng.normal(0, NOISE / np.sqrt(2), x.shape)
    kick -= (kick * hn).sum(1, keepdims=True) * hn
    hn = unit(hn + kick)
    return x + SPEED * hn, hn


def comps(A):
    n = len(A)
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
    return lab, np.sort(np.bincount(lab))[::-1]


def init(rng):
    side = N ** (1 / 3) * 1.1
    x = rng.uniform(0, side, (N, 3))
    h = unit(np.array([1.0, 0, 0]) + rng.normal(0, 0.2, (N, 3)))
    return x, h


if __name__ == "__main__":
    K = int(sys.argv[1])
    seeds = int(sys.argv[2])
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 600
    rows = []
    for seed in range(seeds):
        rng = np.random.default_rng(1000 + seed)
        x, h = init(rng)
        trace = []
        for t in range(steps):
            x, h = step(x, h, K, rng)
            if t in (49, 99, 299, steps - 1):
                D = np.linalg.norm(x[None] - x[:, None], axis=-1)
                A = knn(D, K)
                _, gs = comps(A | A.T)
                trace.append(len(gs))
        D = np.linalg.norm(x[None] - x[:, None], axis=-1)
        _, sizes = comps(D < LINK)
        rows.append((sizes[0] / N, int((sizes >= 5).sum()), trace[-1]))
        print(f"3D K={K} seed {seed}: largest {sizes[0]/N:.2f} pieces {int((sizes>=5).sum())} graph comps t50/100/300/{steps} {trace}", flush=True)
    L = np.array([r[0] for r in rows]); P = np.array([r[1] for r in rows]); G = np.array([r[2] for r in rows])
    print(f"SUMMARY 3D K={K}: whole {int((L>=0.95).sum())}/{seeds} | mean largest {L.mean():.2f} | mean pieces {P.mean():.1f} | mean graph comps {G.mean():.1f} | mean gang size {np.mean(N/np.maximum(G,1)):.1f}", flush=True)
