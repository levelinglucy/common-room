"""
lo_shu_magic_test.py: does the mould feel the magic?

Feeds the same plate with the Lo Shu square and with random arrangements of 1..9,
then asks how evenly the tube volume falls along the eight lines (3 rows, 3 columns,
2 diagonals). Two readings:

  raw       tube volume near each oat, summed along each line
  adjusted  the same, but each oat's volume divided by what that spot gets when
            all nine oats are equal (5s), which takes out the plain geometry:
            the centre is a hub whatever number sits there

spread = (largest line - smallest line) / mean line.  Lower = more 'magic'.
"""
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lo_shu_slime import triangular_mesh, place_food, simulate, line_volumes, LO_SHU

STEPS = 400          # the network is settled by ~300 steps (checked to 1500)


def spread(v):
    lines = list(v.sum(1)) + list(v.sum(0)) + [np.trace(v), np.trace(v[:, ::-1])]
    lines = np.array(lines)
    return (lines.max() - lines.min()) / lines.mean()


def vols(pts, edges, food, grid):
    w = np.array(grid, float).ravel()
    D, L, _ = simulate(pts, edges, food, w, I0=2.0, steps=STEPS)
    v, _ = line_volumes(pts, edges, food, D, L)
    return v


def main(n_random=40, seed=11):
    pts, edges = triangular_mesh()
    food, _ = place_food(pts, LO_SHU)
    base = vols(pts, edges, food, np.full((3, 3), 5))
    lo = vols(pts, edges, food, LO_SHU)
    print("equal-5 volumes:\n", np.round(base, 2))
    print("Lo Shu volumes:\n", np.round(lo, 2))
    print(f"Lo Shu: raw spread {spread(lo):.3f}, adjusted spread {spread(lo / base):.3f}")
    rng = np.random.default_rng(seed)
    raw, adj = [], []
    for k in range(n_random):
        g = rng.permutation(np.arange(1, 10)).reshape(3, 3)
        v = vols(pts, edges, food, g)
        raw.append(spread(v))
        adj.append(spread(v / base))
        print(f"  random {k+1:2d} {g.ravel().tolist()}  raw {raw[-1]:.3f}  adj {adj[-1]:.3f}", flush=True)
    raw, adj = np.array(raw), np.array(adj)
    print(f"\nrandom raw spread: median {np.median(raw):.3f}, range {raw.min():.3f}-{raw.max():.3f}")
    print(f"random adjusted spread: median {np.median(adj):.3f}, range {adj.min():.3f}-{adj.max():.3f}")
    print(f"randoms at least as even as Lo Shu: raw {(raw <= spread(lo)).sum()}/{n_random}, "
          f"adjusted {(adj <= spread(lo / base)).sum()}/{n_random}")


if __name__ == "__main__":
    main()
