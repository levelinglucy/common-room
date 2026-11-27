"""
lo_shu_balance_test.py: is it the magic, or the mirror?

In the Lo Shu, every pair of opposite cells around the 5 sums to 10 (4/6, 9/1, 2/8, 3/7).
Any square built that way already has 4 of its 8 lines summing to 15 (the middle row,
middle column and both diagonals), but usually not the outer rows and columns.
There are 384 such 'mirror-balanced' squares; 8 of them are Lo Shu (rotations and
reflections). This feeds the mould non-magic mirror-balanced squares and compares.
"""
import itertools
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lo_shu_magic_test import vols, spread
from lo_shu_slime import triangular_mesh, place_food, LO_SHU

# opposite cell pairs in a 3x3 grid (flat index)
OPP = [(0, 8), (1, 7), (2, 6), (3, 5)]


def is_magic(g):
    g = np.asarray(g).reshape(3, 3)
    sums = list(g.sum(0)) + list(g.sum(1)) + [np.trace(g), np.trace(g[:, ::-1])]
    return all(s == 15 for s in sums)


def mirror_squares():
    out = []
    for perm in itertools.permutations([1, 2, 3, 4]):
        for flips in itertools.product([0, 1], repeat=4):
            g = [0] * 9
            g[4] = 5
            for (a, b), small, f in zip(OPP, perm, flips):
                lo, hi = small, 10 - small
                g[a], g[b] = (hi, lo) if f else (lo, hi)
            out.append(g)
    return out


def main(n=14, seed=5):
    sq = mirror_squares()
    magic = [g for g in sq if is_magic(g)]
    print(f"{len(sq)} mirror-balanced squares, {len(magic)} of them magic")
    pts, edges = triangular_mesh()
    food, _ = place_food(pts, LO_SHU)
    base = vols(pts, edges, food, np.full((3, 3), 5))
    lo = vols(pts, edges, food, LO_SHU)
    print(f"Lo Shu: raw {spread(lo):.3f}  adj {spread(lo / base):.3f}")
    rng = np.random.default_rng(seed)
    plain = [g for g in sq if not is_magic(g)]
    pick = [plain[i] for i in rng.choice(len(plain), n, replace=False)]
    raw, adj = [], []
    for g in pick:
        v = vols(pts, edges, food, np.array(g).reshape(3, 3))
        raw.append(spread(v))
        adj.append(spread(v / base))
        print(f"  mirror {g}  raw {raw[-1]:.3f}  adj {adj[-1]:.3f}", flush=True)
    raw, adj = np.array(raw), np.array(adj)
    print(f"\nmirror-balanced raw: median {np.median(raw):.3f}, range {raw.min():.3f}-{raw.max():.3f}")
    print(f"mirror-balanced adj: median {np.median(adj):.3f}, range {adj.min():.3f}-{adj.max():.3f}")
    print(f"at least as even as Lo Shu: raw {(raw <= spread(lo)).sum()}/{n}, adj {(adj <= spread(lo / base)).sum()}/{n}")


if __name__ == "__main__":
    main()
