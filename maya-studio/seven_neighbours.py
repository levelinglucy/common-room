"""
seven_neighbours.py: do starlings hold together because they count, not measure?

Ballerini et al. (2008) tracked real starling flocks in 3D and found each bird
responds to its ~6.5 nearest neighbours whatever the distance (a topological
rule), not to every bird inside a fixed radius (a metric rule). Their argument:
a topological flock survives being stretched, because a bird flung outward
still has its seven.

This is a small 2D test of that claim. Same birds, same forces, one difference:
  metric      -> a bird listens to every bird within radius R
  topological -> a bird listens to its K = 7 nearest birds
R is tuned so that, in a calm flock, the metric birds also average ~7
neighbours, so the only thing that differs is what happens when spacing changes.

A hawk then dives straight through the middle. Afterwards we count how many
pieces the flock is in, and how many birds are left with nobody at all.

Forces (Couzin / Vicsek style, constant speed):
  repulsion from anyone closer than R_REP
  alignment with the neighbours' headings
  attraction toward the neighbours
  fleeing from the hawk inside HAWK_R
  angular noise

numpy only. Run:  python3 seven_neighbours.py [--seeds 20] [--gif]
"""
import argparse
import numpy as np

N = 300
SPEED = 0.5
R_REP = 1.0
K = 7
W_ALIGN = 1.0
W_COH = 1.0
W_REP = 1.0
NOISE = 0.15          # radians, uniform +-
MAX_TURN = 0.5        # radians per step
HAWK_SPEED = 1.6
HAWK_R = 6.0
W_HAWK = 4.0
WARM = 300
AFTER = 500


def unit(v):
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    n[n == 0] = 1.0
    return v / n


def neighbour_mask(D, mode, R):
    n = D.shape[0]
    if mode == "metric":
        m = D < R
        np.fill_diagonal(m, False)
        return m
    Dd = D.copy()
    np.fill_diagonal(Dd, np.inf)
    if mode == "sectors":
        return SECTOR_MASK(Dd)
    idx = np.argpartition(Dd, K, axis=1)[:, :K]
    m = np.zeros_like(D, dtype=bool)
    m[np.arange(n)[:, None], idx] = True
    return m


_ANG = None


def SECTOR_MASK(Dd):
    """Nearest bird in each of 6 directions (60 degree slices), at any range."""
    n = Dd.shape[0]
    sec = np.floor((_ANG + np.pi) / (2 * np.pi / 6)).astype(int) % 6
    m = np.zeros((n, n), dtype=bool)
    rows = np.arange(n)
    for s in range(6):
        Ds = np.where(sec == s, Dd, np.inf)
        j = Ds.argmin(1)
        ok = np.isfinite(Ds[rows, j])
        m[rows[ok], j[ok]] = True
    return m


def step(x, h, mode, R, rng, hawk=None):
    global _ANG
    diff = x[None, :, :] - x[:, None, :]        # i -> j
    D = np.linalg.norm(diff, axis=-1)
    if mode == "sectors":
        _ANG = np.arctan2(diff[..., 1], diff[..., 0])
    nb = neighbour_mask(D, mode, R)
    cnt = nb.sum(1)

    Dsafe = D.copy()
    np.fill_diagonal(Dsafe, np.inf)
    toward = diff / Dsafe[..., None]

    close = Dsafe < R_REP
    rep = -(toward * close[..., None]).sum(1)

    align = (h[None, :, :] * nb[..., None]).sum(1)
    coh = (toward * nb[..., None]).sum(1)
    c = np.maximum(cnt, 1)[:, None]
    desire = W_ALIGN * unit(align / c) + W_COH * unit(coh / c) + W_REP * rep
    has = cnt > 0
    desire[~has] = h[~has]                       # alone: keep flying straight
    desire = desire + 1e-9 * h

    if hawk is not None:
        away = x - hawk
        dh = np.linalg.norm(away, axis=1)
        scared = dh < HAWK_R
        desire[scared] = unit(desire[scared]) + W_HAWK * unit(away[scared])

    ang_now = np.arctan2(h[:, 1], h[:, 0])
    ang_want = np.arctan2(desire[:, 1], desire[:, 0])
    turn = (ang_want - ang_now + np.pi) % (2 * np.pi) - np.pi
    turn = np.clip(turn, -MAX_TURN, MAX_TURN) + rng.uniform(-NOISE, NOISE, len(x))
    a = ang_now + turn
    h = np.stack([np.cos(a), np.sin(a)], 1)
    return x + SPEED * h, h, cnt


def components(x, link):
    D = np.linalg.norm(x[None] - x[:, None], axis=-1) < link
    n = len(x)
    lab = -np.ones(n, int)
    c = 0
    for s in range(n):
        if lab[s] >= 0:
            continue
        stack = [s]
        lab[s] = c
        while stack:
            i = stack.pop()
            for j in np.nonzero(D[i] & (lab < 0))[0]:
                lab[j] = c
                stack.append(j)
        c += 1
    sizes = np.bincount(lab)
    return lab, np.sort(sizes)[::-1]


def init(rng):
    side = np.sqrt(N) * 1.1
    x = rng.uniform(0, side, (N, 2))
    a = rng.uniform(-0.3, 0.3, N)
    h = np.stack([np.cos(a), np.sin(a)], 1)
    return x, h


def run(mode, R, seed, hawk_on=True, record=False):
    rng = np.random.default_rng(seed)
    x, h = init(rng)
    frames = []
    for _ in range(WARM):
        x, h, cnt = step(x, h, mode, R, rng)
    calm_cnt = cnt.mean()
    lab, sizes = components(x, LINK)
    calm_largest = sizes[0] / N

    # hawk starts behind the flock's centre, flies through it at an angle
    centre = x[lab == np.bincount(lab).argmax()].mean(0)
    hd = np.mean(h, 0)
    hd = hd / np.linalg.norm(hd)
    perp = np.array([-hd[1], hd[0]])
    dirn = unit((0.6 * hd + perp)[None])[0]
    T = 25   # aim so the hawk reaches the flock's centre after T steps
    hawk = centre + hd * SPEED * T - dirn * HAWK_SPEED * T
    alone = []
    scared_total = 0
    for t in range(AFTER):
        hk = hawk if hawk_on else None
        x, h, cnt = step(x, h, mode, R, rng, hk)
        hawk = hawk + HAWK_SPEED * dirn
        alone.append((cnt == 0).mean())
        scared_total += int((np.linalg.norm(x - hawk, axis=1) < HAWK_R).sum())
        if record and t % 2 == 0:
            frames.append((x.copy(), hawk.copy()))
    lab, sizes = components(x, LINK)
    return dict(calm_cnt=calm_cnt, calm_largest=calm_largest,
                largest=sizes[0] / N, pieces=int((sizes >= 5).sum()),
                strays=int(sizes[sizes < 5].sum()),
                alone_peak=max(alone), alone_end=alone[-1],
                frames=frames, lab=lab, scared=scared_total)


LINK = 3.0   # birds closer than this count as one piece


def tune_R(seeds=(101, 102, 103)):
    """Find metric R whose calm flock averages ~K neighbours."""
    best = None
    for R in np.arange(1.6, 3.61, 0.2):
        cs = []
        for s in seeds:
            rng = np.random.default_rng(s)
            x, h = init(rng)
            for _ in range(WARM):
                x, h, cnt = step(x, h, "metric", R, rng)
            cs.append(cnt.mean())
        m = float(np.mean(cs))
        print(f"  R={R:.1f}: calm neighbours {m:.2f}")
        if best is None or abs(m - K) < abs(best[1] - K):
            best = (R, m)
    return best


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--R", type=float, default=None)
    ap.add_argument("--gif", action="store_true")
    a = ap.parse_args()
    R = a.R
    if R is None:
        print("tuning metric radius:")
        R, m = tune_R()
        print(f"chosen R = {R:.1f} (calm neighbours {m:.2f})")
    for hawk_on in (False, True):
        print(f"\n=== hawk {'ON' if hawk_on else 'OFF'} ===")
        for mode in ("metric", "topological"):
            rs = [run(mode, R, 1000 + s, hawk_on) for s in range(a.seeds)]
            f = lambda k: np.array([r[k] for r in rs], float)
            print(f"{mode:12s} calm nb {f('calm_cnt').mean():5.2f} | "
                  f"calm largest {f('calm_largest').mean():.3f} | "
                  f"end largest {f('largest').mean():.3f} (min {f('largest').min():.3f}) | "
                  f"pieces>=5 {f('pieces').mean():.2f} | strays {f('strays').mean():5.1f} | "
                  f"alone peak {f('alone_peak').mean():.3f} end {f('alone_end').mean():.3f} | "
                  f"intact(>=95%) {int((f('largest') >= 0.95).sum())}/{a.seeds}")
