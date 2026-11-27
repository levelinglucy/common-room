"""Read each loop's core ring (the genome tape) and test it alone.
usage: genomes.py WORLD.npy HOLE COUNT T
Groups loops by the multiset of signal states on the ring (cyclic order kept
as a canonical rotation too), and reports fertility per group.
"""
import sys
from collections import defaultdict, Counter
import numpy as np
from scipy import ndimage
import evoloop as ev
from census import holes

path, H, COUNT, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
w = np.load(path)
lab, n = ndimage.label(w == 0)
areas = np.bincount(lab.ravel())


def ring(g, r, c, H):
    a, b = r - 2, r + H + 1
    l, rr = c - 2, c + H + 1
    top = [g[a, j] for j in range(l, rr + 1)]
    right = [g[i, rr] for i in range(a + 1, b + 1)]
    bot = [g[b, j] for j in range(rr - 1, l - 1, -1)]
    left = [g[i, l] for i in range(b - 1, a, -1)]
    return [int(x) for x in top + right + bot + left]


def canon(seq):
    s = "".join(map(str, seq))
    return min(s[i:] + s[:i] for i in range(len(s)))


def fertile(piece, H, T):
    M = 200
    g = np.zeros((M, M), np.uint8)
    g[M // 2:M // 2 + piece.shape[0], M // 2:M // 2 + piece.shape[1]] = piece
    for t in range(T):
        g = ev.step(g)
    return sum(1 for x in holes(g) if x == H)


sites = []
for i, s in enumerate(ndimage.find_objects(lab), 1):
    h = s[0].stop - s[0].start
    if h == H and s[1].stop - s[1].start == H and areas[i] == H * H:
        r, c = s[0].start, s[1].start
        if r >= 6 and c >= 6 and r + H + 6 <= w.shape[0] and c + H + 6 <= w.shape[1]:
            sites.append((r, c))
print(f"{len(sites)} loops with hole {H} in world")
rng = np.random.default_rng(1)
rng.shuffle(sites)
bags = defaultdict(list)
for r, c in sites[:COUNT]:
    seq = ring(w, r, c, H)
    cnt = Counter(seq)
    key = " ".join(f"{k}x{cnt[k]}" for k in sorted(cnt))
    piece = w[r - 3:r + H + 3, c - 3:c + H + 3].copy()
    end = fertile(piece, H, T)
    bags[key].append((end, canon(seq)))
for key, v in sorted(bags.items(), key=lambda kv: -len(kv[1])):
    ends = [e for e, _ in v]
    print(f"ring states {key}: {len(v)} loops, colony alive after {T} steps in {sum(e >= 1 for e in ends)} (ends {sorted(ends)})")
    for e, s in v[:3]:
        print("    ", s, "->", e)
