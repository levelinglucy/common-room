"""Parse a Golly macrocell (.mc) file for a multistate rule (WireWorld) into a numpy grid.

Node lines: level-1 leaves are '1 nw ne sw se' (cell states); higher levels
'L nw ne sw se' with child node indices (1-based, 0 = empty). The last node is the root.
"""
import sys
import numpy as np


def parse_mc(path):
    nodes = [None]  # 1-based
    for line in open(path):
        line = line.strip()
        if not line or line[0] in '[#':
            continue
        parts = line.split()
        if not parts[0].isdigit():
            continue
        lev = int(parts[0])
        kids = list(map(int, parts[1:5]))
        nodes.append((lev, kids))
    root = len(nodes) - 1
    rlev = nodes[root][0]
    size = 1 << rlev
    cells = []  # (y, x, state)
    memo = {}

    def walk(idx, y, x):
        if idx == 0:
            return
        lev, kids = nodes[idx]
        if lev == 1:
            for k, (dy, dx) in zip(kids, [(0, 0), (0, 1), (1, 0), (1, 1)]):
                if k:
                    cells.append((y + dy, x + dx, k))
            return
        h = 1 << (lev - 1)
        for k, (dy, dx) in zip(kids, [(0, 0), (0, h), (h, 0), (h, h)]):
            walk(k, y + dy, x + dx)

    sys.setrecursionlimit(10000)
    walk(root, 0, 0)
    arr = np.array(cells)
    y0, x0 = arr[:, 0].min(), arr[:, 1].min()
    y1, x1 = arr[:, 0].max(), arr[:, 1].max()
    g = np.zeros((y1 - y0 + 3, x1 - x0 + 3), np.uint8)
    g[arr[:, 0] - y0 + 1, arr[:, 1] - x0 + 1] = arr[:, 2]
    return g


if __name__ == '__main__':
    g = parse_mc(sys.argv[1])
    print(g.shape, {s: int((g == s).sum()) for s in range(4)})
    np.save(sys.argv[2], g)
