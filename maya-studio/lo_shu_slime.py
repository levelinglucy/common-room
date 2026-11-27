"""
lo_shu_slime.py: a slime mould network fed on a magic square.

The model is the flow-adaptation rule from Tero et al. (Science, 2010), the one
used to compare Physarum with the Tokyo rail map:

  - The plate is a mesh of tubes. Each tube has a conductivity D and a length L.
  - Food sources inject and withdraw fluid. Flow through a tube is Q = (D/L) * (p_a - p_b),
    with pressures p solved from Kirchhoff's law (flow in = flow out at every node).
  - Tubes that carry flow thicken, idle tubes wither:  dD/dt = f(|Q|) - D,
    with f(Q) = Q^g / (1 + Q^g).

Here the nine food sources sit on a 3 x 3 grid and carry the digits of the Lo Shu
square:

      4 9 2
      3 5 7
      8 1 6

Every row, column and diagonal sums to 15. A source with digit w sends out fluid in
proportion to w and pulls it in in proportion to w (a 'gravity' demand). The
question: does the magic balance show up in the tubes the mould keeps?

Run:  python3 lo_shu_slime.py            (gallery + gif + numbers)
      python3 lo_shu_slime.py --quick    (numbers only)
numpy + Pillow only.
"""
from __future__ import annotations

import argparse
import heapq
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

LO_SHU = [[4, 9, 2],
          [3, 5, 7],
          [8, 1, 6]]


# ---------------------------------------------------------------- the plate

def triangular_mesh(cols=27, rows=31, jitter=0.18, seed=1):
    """A slightly jittered triangular lattice, so no tube direction is privileged."""
    rng = np.random.default_rng(seed)
    h = math.sqrt(3) / 2
    pts, index = [], {}
    for r in range(rows):
        for c in range(cols):
            x = c + (0.5 if r % 2 else 0.0)
            y = r * h
            index[(r, c)] = len(pts)
            pts.append((x, y))
    pts = np.array(pts, float)
    pts += rng.uniform(-jitter, jitter, pts.shape)
    edges = set()
    for (r, c), i in index.items():
        nbrs = [(r, c + 1)]
        if r % 2 == 0:
            nbrs += [(r + 1, c - 1), (r + 1, c)]
        else:
            nbrs += [(r + 1, c), (r + 1, c + 1)]
        for nb in nbrs:
            j = index.get(nb)
            if j is not None:
                edges.add((min(i, j), max(i, j)))
    edges = np.array(sorted(edges), int)
    return pts, edges


def place_food(pts, digits):
    """Nine food sources on a 3x3 grid inside the plate, snapped to the nearest node."""
    lo, hi = pts.min(0), pts.max(0)
    food, w = [], []
    for r in range(3):
        for c in range(3):
            fx = lo[0] + (hi[0] - lo[0]) * (0.18 + 0.32 * c)
            fy = lo[1] + (hi[1] - lo[1]) * (0.18 + 0.32 * r)
            food.append(int(np.argmin(((pts - (fx, fy)) ** 2).sum(1))))
            w.append(digits[r][c])
    return np.array(food), np.array(w, float)


# ---------------------------------------------------------------- the rule

def demand_matrix(w, I0):
    """Column i: injections when source i is 'pumping'. Source gets +I0*w_i,
    each other food j gets -I0*w_i*w_j/sum_{k!=i} w_k."""
    n = len(w)
    B = np.zeros((n, n))
    for i in range(n):
        others = w.copy()
        others[i] = 0
        B[:, i] = -I0 * w[i] * others / others.sum()
        B[i, i] = I0 * w[i]
    return B


def simulate(pts, edges, food, w, gamma=1.8, I0=2.0, dt=0.25, steps=900,
             snap_every=0, seed=3):
    rng = np.random.default_rng(seed)
    N, E = len(pts), len(edges)
    a, b = edges[:, 0], edges[:, 1]
    L = np.linalg.norm(pts[a] - pts[b], axis=1)
    D = 1.0 + 0.05 * rng.standard_normal(E)
    Bf = demand_matrix(w, I0)
    rhs = np.zeros((N, len(food)))
    rhs[food, :] = Bf
    weights = w / w.sum()          # how often each source is the one pumping
    ground = int(food[0])
    keep = np.ones(N, bool)
    keep[ground] = False
    snaps = []
    for t in range(steps + 1):
        C = np.maximum(D, 1e-9) / L
        K = np.zeros((N, N))
        np.add.at(K, (a, a), C)
        np.add.at(K, (b, b), C)
        np.add.at(K, (a, b), -C)
        np.add.at(K, (b, a), -C)
        p = np.zeros((N, len(food)))
        p[keep] = np.linalg.solve(K[np.ix_(keep, keep)], rhs[keep])
        Q = C[:, None] * (p[a] - p[b])            # E x 9 fluxes
        Qg = np.abs(Q) ** gamma
        f = (Qg / (1 + Qg)) @ weights              # expected stimulus
        if snap_every and t % snap_every == 0:
            snaps.append((t, D.copy()))
        D = D + dt * (f - D)
    return D, L, snaps


# ---------------------------------------------------------------- measuring

def surviving(D, thresh=0.05):
    return D > thresh


def components_ok(n_nodes, edges, alive, food):
    parent = list(range(n_nodes))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (i, j), ok in zip(edges, alive):
        if ok:
            parent[find(i)] = find(j)
    roots = {find(int(f)) for f in food}
    return len(roots) == 1


def shortest(n_nodes, edges, L, alive, src):
    adj = [[] for _ in range(n_nodes)]
    for (i, j), l, ok in zip(edges, L, alive):
        if ok:
            adj[i].append((j, l))
            adj[j].append((i, l))
    dist = [math.inf] * n_nodes
    dist[src] = 0.0
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, l in adj[u]:
            nd = d + l
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def mst_length(points):
    n = len(points)
    inT = [False] * n
    best = [math.inf] * n
    best[0] = 0
    total = 0.0
    for _ in range(n):
        u = min((d, i) for i, d in enumerate(best) if not inT[i])[1]
        inT[u] = True
        total += best[u]
        for v in range(n):
            if not inT[v]:
                best[v] = min(best[v], float(np.linalg.norm(points[u] - points[v])))
    return total


def measure(pts, edges, food, D, L):
    alive = surviving(D)
    total = float(L[alive].sum())
    mst = mst_length(pts[food])
    connected = components_ok(len(pts), edges, alive, food)
    # fault tolerance: share of surviving tubes you can cut without splitting the food
    idx = np.flatnonzero(alive)
    safe = 0
    for e in idx:
        test = alive.copy()
        test[e] = False
        safe += components_ok(len(pts), edges, test, food)
    ft = safe / max(1, len(idx))
    # detour: network path / straight line, averaged over food pairs
    ratios = []
    for i, s in enumerate(food):
        dist = shortest(len(pts), edges, L, alive, int(s))
        for t in food[i + 1:]:
            ratios.append(dist[int(t)] / float(np.linalg.norm(pts[s] - pts[t])))
    return dict(tubes=int(alive.sum()), length=total, length_vs_mst=total / mst,
                fault_tolerance=ft, detour=float(np.mean(ratios)), connected=connected)


def line_volumes(pts, edges, food, D, L):
    """Tube volume (D*L) in a disc around each food source, then summed along the
    eight magic lines. If the magic shows, the eight sums should match."""
    mid = (pts[edges[:, 0]] + pts[edges[:, 1]]) / 2
    vol = []
    for s in food:
        near = np.linalg.norm(mid - pts[s], axis=1) < 2.2
        vol.append(float((D * L)[near].sum()))
    v = np.array(vol).reshape(3, 3)
    lines = {f"row {r+1}": v[r].sum() for r in range(3)}
    lines.update({f"col {c+1}": v[:, c].sum() for c in range(3)})
    lines["diag \\"] = np.trace(v)
    lines["diag /"] = np.trace(v[:, ::-1])
    return v, lines


# ---------------------------------------------------------------- drawing

BG = (14, 12, 10)
TUBE = (246, 196, 52)
OAT = (236, 226, 200)


def font(size):
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw(pts, edges, food, w, D, size=520, caption="", dmax=None):
    img = Image.new("RGB", (size, size + (34 if caption else 0)), BG)
    dr = ImageDraw.Draw(img)
    lo, hi = pts.min(0), pts.max(0)
    pad = 26
    s = (size - 2 * pad) / max(hi - lo)

    def xy(p):
        return (pad + (p[0] - lo[0]) * s, pad + (p[1] - lo[1]) * s)
    dmax = dmax or max(1e-9, float(D.max()))
    order = np.argsort(D)
    for e in order:
        d = D[e] / dmax
        if d < 0.02:
            continue
        i, j = edges[e]
        width = max(1, int(round(1 + 7 * math.sqrt(d))))
        glow = min(1.0, 0.25 + 0.9 * math.sqrt(d))
        col = tuple(int(BG[k] + (TUBE[k] - BG[k]) * glow) for k in range(3))
        dr.line([xy(pts[i]), xy(pts[j])], fill=col, width=width)
    f = font(15)
    for s_, digit in zip(food, w):
        x, y = xy(pts[s_])
        r = 9 + 1.2 * digit
        dr.ellipse([x - r, y - r, x + r, y + r], fill=OAT, outline=(120, 100, 60), width=2)
        txt = str(int(digit))
        tw = dr.textlength(txt, font=f)
        dr.text((x - tw / 2, y - 9), txt, fill=(40, 30, 20), font=f)
    if caption:
        cf = font(16)
        tw = dr.textlength(caption, font=cf)
        dr.text(((size - tw) / 2, size + 6), caption, fill=(220, 210, 190), font=cf)
    return img


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--steps", type=int, default=900)
    args = ap.parse_args()

    pts, edges = triangular_mesh()
    food, w = place_food(pts, LO_SHU)
    print(f"plate: {len(pts)} nodes, {len(edges)} tubes; food at {list(food)}")

    runs = [
        ("equal oats, all 5", np.full(9, 5.0), 2.0),
        ("Lo Shu, thin feed", w, 1.0),
        ("Lo Shu", w, 2.0),
        ("Lo Shu, rich feed", w, 4.0),
    ]
    results = {}
    for name, ww, I0 in runs:
        D, L, _ = simulate(pts, edges, food, ww, I0=I0, steps=args.steps)
        m = measure(pts, edges, food, D, L)
        v, lines = line_volumes(pts, edges, food, D, L)
        results[name] = (ww, D, m, v, lines)
        print(f"\n[{name}, I0={I0}]", {k: (round(x, 3) if isinstance(x, float) else x) for k, x in m.items()})
        print("  tube volume near each oat:\n", np.round(v, 2))
        print("  line sums:", {k: round(float(x), 2) for k, x in lines.items()})
        spread = (max(lines.values()) - min(lines.values())) / np.mean(list(lines.values()))
        print(f"  spread of the 8 line sums: {spread:.1%}")

    if args.quick:
        return

    # gallery
    tiles = [draw(pts, edges, food, ww, D, caption=name) for name, (ww, D, *_ ) in results.items()]
    W, H = tiles[0].size
    gal = Image.new("RGB", (2 * W, 2 * H), BG)
    for k, t in enumerate(tiles):
        gal.paste(t, ((k % 2) * W, (k // 2) * H))
    gal.save(HERE / "lo_shu_slime_gallery.png")

    # growth gif for the main Lo Shu run
    D, L, snaps = simulate(pts, edges, food, w, I0=2.0, steps=args.steps, snap_every=15)
    frames = []
    for t, Ds in snaps:
        frames.append(draw(pts, edges, food, w, Ds, size=560,
                           caption=f"Lo Shu slime  -  step {t}"))
    frames += [frames[-1]] * 20
    frames[0].save(HERE / "lo_shu_slime_growth.gif", save_all=True,
                   append_images=frames[1:], duration=90, loop=0, optimize=True)
    print("\nsaved gallery + gif")


if __name__ == "__main__":
    main()
