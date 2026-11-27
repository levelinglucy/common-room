# Track the largest pile's centre on the torus across snapshots; unwrap; MSD.
import numpy as np, glob, re, sys
from scipy import ndimage
L = 128
st8 = np.ones((3, 3), int)

def largest_centre(g):
    # label on torus: tile 3x3 not needed if we use circular mean of the largest label after wrap-merge
    lab, n = ndimage.label(g, structure=st8)
    # merge labels across the wrap edges
    parent = list(range(n + 1))
    def f(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def u(a, b):
        if a and b:
            ra, rb = f(a), f(b)
            if ra != rb: parent[ra] = rb
    for i in range(L):
        for d in (-1, 0, 1):
            u(lab[i, 0], lab[(i + d) % L, L - 1])
            u(lab[0, i], lab[L - 1, (i + d) % L])
    roots = np.array([f(a) for a in range(n + 1)])
    lab2 = roots[lab] * (lab > 0)
    sizes = np.bincount(lab2.ravel()); sizes[0] = 0
    big = sizes.argmax()
    ys, xs = np.nonzero(lab2 == big)
    ang = 2 * np.pi / L
    cx = (np.angle(np.mean(np.exp(1j * ang * xs))) / ang) % L
    cy = (np.angle(np.mean(np.exp(1j * ang * ys))) / ang) % L
    # radius of gyration on torus
    dx = (xs - cx + L / 2) % L - L / 2; dy = (ys - cy + L / 2) % L - L / 2
    rg = np.sqrt(np.mean(dx ** 2 + dy ** 2))
    return cx, cy, sizes[big], rg

def track(seed, tmin=4_000_000):
    fs = glob.glob(f'snaps/s{seed}/g_*.bin')
    fs = sorted(fs, key=lambda s: int(re.findall(r'_(\d+)\.bin', s)[0]))
    T, P = [], []
    for fn in fs:
        t = int(re.findall(r'_(\d+)\.bin', fn)[0])
        if t < tmin: continue
        g = np.fromfile(fn, np.uint8).reshape(L, L)
        cx, cy, sz, rg = largest_centre(g)
        T.append(t); P.append((cx, cy, sz, rg))
    P = np.array(P); T = np.array(T)
    xy = P[:, :2].copy()
    d = np.diff(xy, axis=0); d = (d + L / 2) % L - L / 2
    un = np.vstack([xy[:1], xy[:1] + np.cumsum(d, 0)])
    return T, un, P[:, 2], P[:, 3]

if __name__ == '__main__':
    out = {}
    for s in (1, 2, 3, 4):
        T, un, sz, rg = track(s)
        out[s] = (T, un, sz, rg)
        disp = np.hypot(*(un[-1] - un[0]))
        print(f'seed {s}: snaps {len(T)}, size {sz.mean():.0f}, Rg {rg.mean():.1f}, net move {disp:.1f} cells over {(T[-1]-T[0])/1e6:.1f}M ticks, path {np.sum(np.hypot(*np.diff(un,axis=0).T)):.1f}')
    # MSD over lags (pooled)
    lags = [1, 2, 4, 8, 16, 32, 64]
    for lag in lags:
        m = []
        for s in out:
            un = out[s][1]
            if len(un) > lag:
                dd = un[lag:] - un[:-lag]; m.extend((dd ** 2).sum(1))
        print(f'lag {lag*0.2:.1f}M ticks: MSD {np.mean(m):.1f}  (n={len(m)})')
    np.save('wander_tracks.npy', np.array([np.column_stack([out[s][0], out[s][1], out[s][2], out[s][3]]) for s in out], dtype=object), allow_pickle=True)
