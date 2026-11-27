"""What holds the choirs? Look for topology in the final phase field.

Torus: winding number of phase along each row and column of a grid
(nearest-firefly interpolation, torus distance). Both geometries: vortices,
the net phase turn around each little grid square (+1/-1 = a spiral core).

usage: python twist.py RULE PARAM SEEDS EPS GEOM [GRID]
"""
import sys
import numpy as np
from scipy.spatial import cKDTree
import firefly as ff
import torus as tor


def wrap(x):
    return (x + 0.5) % 1.0 - 0.5


def field(pos, ph, G, geom):
    g = (np.arange(G) + 0.5) / G
    X, Y = np.meshgrid(g, g, indexing="xy")
    pts = np.stack([X.ravel(), Y.ravel()], 1)
    tree = cKDTree(pos, boxsize=1.0) if geom == "torus" else cKDTree(pos)
    _, idx = tree.query(pts)
    return ph[idx].reshape(G, G)  # [row=y, col=x]


def analyse(F, geom):
    dx = wrap(np.roll(F, -1, 1) - F)  # step in x
    dy = wrap(np.roll(F, -1, 0) - F)  # step in y
    # plaquette circulation: around square (i,j)->(i,j+1)->(i+1,j+1)->(i+1,j)
    circ = dx + np.roll(dy, -1, 1) - np.roll(dx, -1, 0) - dy
    if geom == "square":
        circ = circ[:-1, :-1]
    v = np.rint(circ).astype(int)
    out = {"vort+": int((v > 0).sum()), "vort-": int((v < 0).sum())}
    if geom == "torus":
        wx = np.rint(dx.sum(1)).astype(int)  # winding along each row
        wy = np.rint(dy.sum(0)).astype(int)
        out["wind_x"] = sorted(set(wx.tolist()))
        out["wind_y"] = sorted(set(wy.tolist()))
    return out


if __name__ == "__main__":
    rule, param, nseeds, eps, geom = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    G = int(sys.argv[6]) if len(sys.argv) > 6 else 20
    periods = 200
    if geom == "torus":
        ff.listen_lists = tor.listen_lists_torus
    for sd in range(nseeds):
        pos = ff.perches(400, 100 + sd)
        ft, _, _ = ff.run(pos, rule, param, eps=eps, periods=periods, seed=sd)
        r, _, ph = ff.beats(ft, periods=periods)
        cs = [c for c in tor.choir_sizes(ft, periods) if c >= 5]
        F = field(pos, ph, G, geom)
        a = analyse(F, geom)
        print(f"{geom} {rule} {param:g} seed {sd}: r={r:.3f} choirs {len(cs)} biggest {cs[:3]}  {a}", flush=True)
