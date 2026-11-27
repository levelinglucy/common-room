"""Does the forest edge make the choirs? Same model as firefly.py, but the
perches live on a torus (wrap-around square), so nobody sits on an edge.

usage: python torus.py RULE PARAM SEEDS EPS [torus|square]
"""
import sys
import numpy as np
from scipy.spatial import cKDTree
import firefly as ff


def listen_lists_torus(pos, rule, param):
    n = len(pos)
    tree = cKDTree(pos, boxsize=1.0)
    if rule == "count":
        _, idx = tree.query(pos, int(param) + 1)
        return [idx[i, 1:] for i in range(n)]
    if rule == "metric":
        nb = tree.query_ball_point(pos, param)
        return [np.array([j for j in nb[i] if j != i], int) for i in range(n)]
    if rule == "sectors":
        _, idx = tree.query(pos, min(n, 60))
        out = []
        for i in range(n):
            d = pos[idx[i, 1:]] - pos[i]
            d -= np.round(d)  # minimum image
            sec = (np.floor((np.arctan2(d[:, 1], d[:, 0]) + np.pi) / (np.pi / 3)).astype(int)) % 6
            chosen = []
            for s in range(6):
                hit = np.nonzero(sec == s)[0]
                if len(hit):
                    chosen.append(idx[i, 1 + hit[0]])
            out.append(np.array(chosen, int))
        return out
    raise ValueError(rule)


def choir_sizes(flash_times, periods, tol=0.01):
    """Group fireflies by the time of their last flash (same instant = same choir)."""
    last = np.array([ft[-1] if ft else -1 for ft in flash_times])
    order = np.argsort(last)
    sizes, cur = [], 1
    for a, b in zip(order[:-1], order[1:]):
        if last[b] - last[a] < tol:
            cur += 1
        else:
            sizes.append(cur)
            cur = 1
    sizes.append(cur)
    # wrap: a choir straddling the period boundary is not an issue since we use last flash
    return sorted(sizes, reverse=True)


if __name__ == "__main__":
    rule, param, nseeds, eps = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
    geom = sys.argv[5] if len(sys.argv) > 5 else "torus"
    periods = 200
    if geom == "torus":
        ff.listen_lists = listen_lists_torus
    synced = 0
    for sd in range(nseeds):
        pos = ff.perches(400, 100 + sd)
        ft, _, lists = ff.run(pos, rule, param, eps=eps, periods=periods, seed=sd)
        r, g, _ = ff.beats(ft, periods=periods)
        cs = choir_sizes(ft, periods)
        big = [c for c in cs if c >= 5]
        synced += r > 0.95
        deg = np.mean([len(l) for l in lists])
        print(f"{geom} {rule} {param:g} eps {eps} seed {sd}: r={r:.3f} links={deg:.2f} choirs>=5: {len(big)} biggest {big[:4]}", flush=True)
    print(f"{geom} {rule} {param:g} eps {eps}: synced {synced}/{nseeds}")
