"""
Does a slime mould remember a road it stopped using?

Tero's Physarum rule on a jittered triangular mesh with a round hole in it.
  A (middle left)  ---- hole ----  B (right).   C far left.
There are two equally good A-B roads: over the hole or under it.

Phase 1 (train):  flow A -> B for T1.  The mould picks a side (symmetry broken by jitter).
Phase 2 (idle):   flow A -> C for T.   C is on the other side of A, so the A-C road
                  favours neither side; the old A-B road just decays.
Phase 3 (recall): flow A -> B again for T3.  Which side does it pick?

Rule: Kirchhoff flow with conductance D/L, dD/dt = f(|Q|) - D, f = Q^mu/(1+Q^mu),
and an optional floor: D = max(D, floor) after every step (the stand-in for
'a tube cannot get thinner than this', or for pruning in Velisara's mycelium).

Usage: python3 memory.py FLOOR T [seeds]
"""
import math
import sys

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

MU = 1.8
I0 = float(__import__("os").environ.get("I0", "1.0"))
DT = 0.2


def mesh(cols=36, rows=23, jitter=0.18, seed=1, hole_r=4.2):
    rng = np.random.default_rng(seed)
    h = math.sqrt(3) / 2
    pts, index = [], {}
    for r in range(rows):
        for c in range(cols):
            pts.append((c + (0.5 if r % 2 else 0.0), r * h))
            index[(r, c)] = len(pts) - 1
    pts = np.array(pts, float)
    pts += rng.uniform(-jitter, jitter, pts.shape)
    W, H = cols - 0.5, (rows - 1) * h
    A = np.array([0.36 * W, H / 2])
    B = np.array([0.90 * W, H / 2])
    Cc = np.array([0.04 * W, H / 2])
    centre = (A + B) / 2
    inside = np.linalg.norm(pts - centre, axis=1) < hole_r
    edges = set()
    for (r, c), i in index.items():
        nbrs = [(r, c + 1)] + ([(r + 1, c - 1), (r + 1, c)] if r % 2 == 0 else [(r + 1, c), (r + 1, c + 1)])
        for nb in nbrs:
            j = index.get(nb)
            if j is not None and not inside[i] and not inside[j]:
                edges.add((min(i, j), max(i, j)))
    keep = ~inside
    newid = -np.ones(len(pts), int)
    newid[keep] = np.arange(keep.sum())
    pts = pts[keep]
    edges = np.array(sorted((newid[i], newid[j]) for i, j in edges), int)
    near = lambda q: int(np.argmin(((pts - q) ** 2).sum(1)))
    return pts, edges, near(A), near(B), near(Cc), centre


class Mould:
    def __init__(self, pts, edges, floor, seed):
        self.pts, self.edges, self.floor = pts, edges, floor
        self.N, self.E = len(pts), len(edges)
        self.a, self.b = edges[:, 0], edges[:, 1]
        self.L = np.linalg.norm(pts[self.a] - pts[self.b], axis=1)
        rng = np.random.default_rng(seed)
        self.D = 1.0 + 0.05 * rng.standard_normal(self.E)
        a, b = self.a, self.b
        self.rows = np.concatenate([a, b, a, b])
        self.cols = np.concatenate([a, b, b, a])

    def flow(self, src, snk):
        C = np.maximum(self.D, 1e-300) / self.L
        K = sp.csr_matrix((np.concatenate([C, C, -C, -C]), (self.rows, self.cols)), shape=(self.N, self.N))
        keep = np.ones(self.N, bool)
        keep[snk] = False
        idx = np.flatnonzero(keep)
        rhs = np.zeros(self.N)
        rhs[src] = I0
        p = np.zeros(self.N)
        p[idx] = spla.spsolve(K[idx][:, idx].tocsc(), rhs[idx])
        Q = C * (p[self.a] - p[self.b])
        return Q, p[src] - p[snk]

    def run(self, src, snk, T, log=None):
        steps = int(round(T / DT))
        for s in range(steps):
            Q, dp = self.flow(src, snk)
            q = np.abs(Q) ** MU
            self.D = self.D + DT * (q / (1 + q) - self.D)
            if self.floor > 0:
                self.D = np.maximum(self.D, self.floor)
            if log is not None:
                log.append(dp)
        return self.flow(src, snk)


def side_flow(pts, edges, Q, centre):
    """Flux crossing the vertical line through the hole centre, above vs below it."""
    a, b = edges[:, 0], edges[:, 1]
    xa, xb = pts[a, 0], pts[b, 0]
    cross = (xa - centre[0]) * (xb - centre[0]) < 0
    ym = (pts[a, 1] + pts[b, 1]) / 2
    up = np.abs(Q[cross & (ym > centre[1])]).sum()
    dn = np.abs(Q[cross & (ym < centre[1])]).sum()
    return up, dn


def trial(floor, T, seed, T1=60.0, T3=60.0, mesh_seed=None, want=False):
    pts, edges, A, B, C, centre = mesh(seed=seed if mesh_seed is None else mesh_seed)
    m = Mould(pts, edges, floor, seed)
    Q1, dp1 = m.run(A, B, T1)
    u1, d1 = side_flow(pts, edges, Q1, centre)
    side1 = 'up' if u1 > d1 else 'down'
    D1 = m.D.copy()
    # the old road's thickness: the thinnest tube on the trained side carrying > 90% flow
    road = np.abs(Q1) > 0.9 * I0
    if T > 0:
        m.run(A, C, T)
    D2 = m.D.copy()
    road_left = D2[road].min() if road.any() else float('nan')
    log = []
    Q3, dp3 = m.run(A, B, T3, log)
    u3, d3 = side_flow(pts, edges, Q3, centre)
    side3 = 'up' if u3 > d3 else 'down'
    # time until the pressure is within 10% of its final value
    log = np.array(log)
    within = np.abs(log - dp3) <= 0.1 * dp3
    bad = np.flatnonzero(~within)
    relearn = (bad[-1] + 1) * DT if len(bad) else 0.0
    out = dict(seed=seed, side1=side1, side3=side3, same=side1 == side3,
               share1=max(u1, d1) / (u1 + d1), share3=max(u3, d3) / (u3 + d3),
               road_left=road_left, relearn=relearn, dp1=dp1, dp3=dp3)
    if want:
        out.update(pts=pts, edges=edges, D1=D1, D2=D2, D3=m.D.copy(), A=A, B=B, C=C, centre=centre)
    return out


if __name__ == '__main__':
    floor = float(sys.argv[1])
    T = float(sys.argv[2])
    seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    for s in range(seeds):
        r = trial(floor, T, s)
        print(f"seed {s}: trained {r['side1']} ({r['share1']:.3f})  recalled {r['side3']} ({r['share3']:.3f})  "
              f"same={r['same']}  old road thinnest {r['road_left']:.2e}  relearn {r['relearn']:.1f}  dp {r['dp1']:.2f}/{r['dp3']:.2f}")
