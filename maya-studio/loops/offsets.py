"""For each L: offset of the founder's first child vs the spacing its
descendants use along the same row, for a range of founder arm lengths."""
import sys
import numpy as np
from multiprocessing import Pool
from build_loop import build, genome_of
from lone_cycle_lib import closed_loops
from langton import step

def run(args):
    L, arm = args
    N = 40 + 6 * L + 2 * arm
    N = max(N, 160)
    g = np.zeros((N, N), np.uint8)
    p = build(L, genome_of(L - 2, 2, L), arm)
    r0, c0 = N // 2, 10
    g[r0:r0 + p.shape[0], c0:c0 + p.shape[1]] = p
    row = {}
    other = []
    for t in range(1, 30 * L + 400):
        g = step(g)
        if t % 2:
            continue
        for h in closed_loops(g, L):
            dr, dc = h[0] - (r0 + 3), h[1] - (c0 + 3)
            if dr == 0 and dc not in row:
                row[dc] = t
            elif dr != 0 and (dr, dc) not in other:
                other.append((dr, dc))
        if len(row) >= 4:
            break
    xs = sorted(row)
    return L, arm, xs[:4], sorted(row.values())[:4], other[:3]

if __name__ == "__main__":
    jobs = [(L, int(a)) for L in range(8, 24) for a in sys.argv[1:]] if len(sys.argv) > 1 else [(L, L - 3) for L in range(8, 24)]
    with Pool(7) as p:
        for L, arm, xs, ts, other in p.map(run, jobs):
            gaps = np.diff(xs).tolist()
            print(f"L={L} arm={arm} row x={xs} gaps={gaps} t={ts} off-row={other}")
