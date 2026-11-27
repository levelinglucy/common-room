"""Build a Langton loop of any size with any genome, and test whether it breeds.

The canonical loop, read upstream from the junction J (bottom-right corner,
where the arm leaves), is (7 0 1)x6 (4 0 1)x2 1x4 on a core ring of side 8.
7-0 = 'grow straight', 4-0 = 'turn left'. Signals flow anticlockwise.
"""
import numpy as np
from scipy import ndimage
from langton import step, parse_rle, place


def ring_upstream(L):
    """Core-ring cells of a side-L loop (local frame, core at 1..L), in upstream
    order starting from J=(L,L): bottom row leftwards, left column upwards,
    top row rightwards, right column downwards."""
    cells = [(L, c) for c in range(L, 0, -1)]          # J ... (L,1)
    cells += [(r, 1) for r in range(L - 1, 0, -1)]      # (L-1,1) ... (1,1)
    cells += [(1, c) for c in range(2, L + 1)]          # (1,2) ... (1,L)
    cells += [(r, L) for r in range(2, L)]              # (2,L) ... (L-1,L)
    return cells


def build(L, genome, arm):
    """genome: list of states, upstream from J, length must be 4(L-1)."""
    P = 4 * (L - 1)
    assert len(genome) == P, (len(genome), P)
    H, W = L + 2, L + arm + 2
    g = np.zeros((H, W), dtype=np.uint8)
    # outer sheath
    g[0, 1:L + 1] = 2
    g[1:L + 1, 0] = 2
    g[1:L, L + 1] = 2
    g[L + 1, 1:L + arm + 1] = 2
    # inner sheath
    g[2, 2:L] = 2
    g[L - 1, 2:L] = 2
    g[2:L, 2] = 2
    g[2:L, L - 1] = 2
    # core ring
    for (r, c), v in zip(ring_upstream(L), genome):
        g[r, c] = v
    # arm
    if arm > 0:
        g[L, L + 1:L + arm + 1] = 1
        g[L - 1, L + 1:L + arm + 1] = 2
    g[L, L + arm + 1] = 2
    return g


def genome_of(s, t=2, L=None):
    """(7 0 1)^s (4 0 1)^t then 1s to fill the ring."""
    core = [7, 0, 1] * s + [4, 0, 1] * t
    P = 4 * (L - 1)
    if len(core) > P:
        return None
    return core + [1] * (P - len(core))


def census(g):
    lab, n = ndimage.label(g > 0)
    sizes = []
    for sl in ndimage.find_objects(lab):
        sizes.append((sl[0].stop - sl[0].start, sl[1].stop - sl[1].start))
    return n, sizes


def has_closed_loop(g, L):
    """True if some component contains an empty hole of (L-4)x(L-4) cells
    enclosed by sheath: the signature of a finished loop of side L."""
    empty = g == 0
    lab, n = ndimage.label(empty)
    want = (L - 4) ** 2
    counts = np.bincount(lab.ravel())
    return bool(np.any(counts[1:] == want))


def holes(g):
    """Sizes of enclosed empty regions (not the outside)."""
    lab, n = ndimage.label(g == 0)
    counts = np.bincount(lab.ravel())[1:]
    if len(counts) == 0:
        return []
    big = counts.argmax()
    return sorted(int(c) for i, c in enumerate(counts) if i != big)


if __name__ == "__main__":
    # sanity: rebuilt canonical loop equals Golly's seed
    seed = parse_rle("Langtons-Loops.rle")
    mine = build(8, genome_of(6, 2, 8), 5)
    print("canonical rebuilt matches seed:", mine.shape == seed.shape and bool((mine == seed).all()))
    if not (mine.shape == seed.shape and (mine == seed).all()):
        print(seed)
        print(mine)
