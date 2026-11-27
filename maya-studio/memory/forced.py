"""Forced training: memory vs geometry.

The first sweep showed the 'forgotten' recall is not a coin flip: each mesh has a preferred side
(jitter makes one road a little cheaper), and free training usually picks it too. So here training
is pushed onto a chosen side by a lid (the crossing edges on the other side held at 1e-12 during
phase 1 only). Even seeds are trained over the hole, odd seeds under it.

Naive control, per seed: same mesh, same floor, A->C for T then A->B, no training.
Usage: I0=1.0 python3 forced.py OUT.tsv SEEDS
"""
import sys
from multiprocessing import Pool

import numpy as np

from memory import mesh, Mould, side_flow, DT

FLOORS = [1e-3, 1e-6, 1e-9, 0.0]
TS = [0, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 24, 30, 40]
T1 = T3 = 60.0
LID = 1e-12


def crossing(pts, edges, centre, side):
    a, b = edges[:, 0], edges[:, 1]
    cross = (pts[a, 0] - centre[0]) * (pts[b, 0] - centre[0]) < 0
    ym = (pts[a, 1] + pts[b, 1]) / 2
    return cross & ((ym > centre[1]) if side == 'up' else (ym < centre[1]))


def recall(m, pts, edges, A, B, centre):
    log = []
    Q = None
    for _ in range(int(round(T3 / DT))):
        Q, dp = m.flow(A, B)
        q = np.abs(Q) ** 1.8
        m.D = m.D + DT * (q / (1 + q) - m.D)
        if m.floor > 0:
            m.D = np.maximum(m.D, m.floor)
        log.append(dp)
    Q, dp = m.flow(A, B)
    u, d = side_flow(pts, edges, Q, centre)
    log = np.array(log)
    bad = np.flatnonzero(np.abs(log - dp) > 0.1 * dp)
    return ('up' if u > d else 'down'), max(u, d) / (u + d), (bad[-1] + 1) * DT if len(bad) else 0.0


def job(args):
    floor, T, seed = args
    pts, edges, A, B, C, centre = mesh(seed=seed)
    want = 'up' if seed % 2 == 0 else 'down'
    lid = crossing(pts, edges, centre, 'down' if want == 'up' else 'up')
    # trained
    m = Mould(pts, edges, floor, seed)
    for _ in range(int(round(T1 / DT))):
        m.D[lid] = LID
        Q, dp = m.flow(A, B)
        q = np.abs(Q) ** 1.8
        m.D = m.D + DT * (q / (1 + q) - m.D)
        if floor > 0:
            m.D = np.maximum(m.D, floor)
    m.D[lid] = max(floor, LID)
    Q, _ = m.flow(A, B)
    u, d = side_flow(pts, edges, Q, centre)
    got = 'up' if u > d else 'down'
    road = np.abs(Q) > 0.9 * 1.0
    if T > 0:
        m.run(A, C, T)
    road_left = float(m.D[road].min())
    side3, share3, relearn = recall(m, pts, edges, A, B, centre)
    # naive
    n = Mould(pts, edges, floor, seed)
    if floor > 0:
        n.D[:] = floor
    else:
        n.D[:] = 1e-12
    if T > 0:
        n.run(A, C, T)
    nside, nshare, nrelearn = recall(n, pts, edges, A, B, centre)
    return (floor, T, seed, want, got, side3, nside, share3, nshare, road_left, relearn, nrelearn)


if __name__ == '__main__':
    out, seeds = sys.argv[1], int(sys.argv[2])
    jobs = [(f, T, s) for f in FLOORS for T in TS for s in range(seeds)]
    with Pool(8) as pool, open(out, 'w') as fh:
        fh.write('floor\tT\tseed\twant\tgot\tside3\tnaive\tshare3\tnshare\troad_left\trelearn\tnrelearn\n')
        for row in pool.imap_unordered(job, jobs, chunksize=2):
            fh.write('\t'.join(str(x) for x in row) + '\n')
            fh.flush()
