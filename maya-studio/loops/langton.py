"""Langton's self-reproducing loop (1984), run from Golly's rule table.

States: 0 empty, 1 core, 2 sheath, 3-7 signals. von Neumann neighbourhood,
rotate4 symmetry. A cell with no matching rule keeps its state (Golly's default).
"""
import numpy as np
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_table(path=os.path.join(HERE, "Langtons-Loops.rule")):
    lut = np.full(8 ** 5, -1, dtype=np.int16)  # index C,N,E,S,W
    in_table = False
    for line in open(path):
        line = line.strip()
        if line.startswith("@TABLE"):
            in_table = True
            continue
        if line.startswith("@") and in_table:
            break
        if not in_table or not line or line[0] in "#" or ":" in line:
            continue
        if len(line) != 6 or not line.isdigit():
            continue
        c, n, e, s, w, out = (int(ch) for ch in line)
        nb = [n, e, s, w]
        for r in range(4):
            rn = nb[r:] + nb[:r]
            idx = (((c * 8 + rn[0]) * 8 + rn[1]) * 8 + rn[2]) * 8 + rn[3]
            lut[idx] = out
    # unmatched: keep own state
    for idx in range(8 ** 5):
        if lut[idx] < 0:
            lut[idx] = idx // 8 ** 4
    return lut.astype(np.uint8)


LUT = load_table()


def step(g):
    n = np.roll(g, 1, 0)
    s = np.roll(g, -1, 0)
    w = np.roll(g, 1, 1)
    e = np.roll(g, -1, 1)
    idx = (((g.astype(np.int32) * 8 + n) * 8 + e) * 8 + s) * 8 + w
    return LUT[idx]


def parse_rle(path):
    txt = open(path).read()
    lines = [l for l in txt.splitlines() if not l.startswith("#")]
    header = lines[0]
    body = "".join(lines[1:])
    x = int(header.split("x =")[1].split(",")[0])
    y = int(header.split("y =")[1].split(",")[0])
    g = np.zeros((y, x), dtype=np.uint8)
    r = c = 0
    num = ""
    for ch in body:
        if ch.isdigit():
            num += ch
            continue
        k = int(num) if num else 1
        num = ""
        if ch == "!":
            break
        if ch == "$":
            r += k
            c = 0
        elif ch in ".b":
            c += k
        else:
            v = ord(ch) - ord("A") + 1
            g[r, c:c + k] = v
            c += k
    return g


def place(pattern, size=200, at=None):
    g = np.zeros((size, size), dtype=np.uint8)
    h, w = pattern.shape
    r0, c0 = at if at else ((size - h) // 2, (size - w) // 2)
    g[r0:r0 + h, c0:c0 + w] = pattern
    return g


def count_loops(g):
    """Count 4-connected components of non-empty cells."""
    from scipy import ndimage
    lab, n = ndimage.label(g > 0)
    return n


if __name__ == "__main__":
    seed = parse_rle(os.path.join(HERE, "Langtons-Loops.rle"))
    print(seed)
    g = place(seed, 160)
    for t in range(1, 1201):
        g = step(g)
        if t % 50 == 0:
            print(t, "live", int((g > 0).sum()), "pieces", count_loops(g))
