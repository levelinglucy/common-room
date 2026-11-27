"""Pulse-coupled fireflies (Mirollo-Strogatz style) on fixed perches.

Each firefly has a phase in [0,1). Phase grows at its own rate (period ~1
with a small spread). At phase 1 it flashes and resets to 0. Every firefly
that can SEE the flasher gets nudged: phase -> phase * (1 + eps). If that
pushes it to 1 it flashes too, in the same instant (a cascade). A firefly
that just flashed sits at 0 and the multiplicative nudge can't move it, so
flashing makes you briefly deaf: a built-in refractory moment.

Who sees whom (directed: i listens to j):
  metric R   : everyone within distance R
  count K    : the K nearest
  sectors    : the nearest firefly in each of six 60-degree directions
  glance K   : K nearest plus one random firefly from anywhere, new each flash
"""
import numpy as np
from scipy.spatial import cKDTree


def perches(n, seed, kind="random"):
    rng = np.random.default_rng(seed)
    if kind == "random":
        return rng.random((n, 2))
    side = int(round(np.sqrt(n)))
    g = (np.stack(np.meshgrid(np.arange(side), np.arange(side)), -1).reshape(-1, 2) + 0.5) / side
    return g + rng.normal(0, 0.15 / side, g.shape)


def listen_lists(pos, rule, param):
    n = len(pos)
    tree = cKDTree(pos)
    if rule == "metric":
        nb = tree.query_ball_point(pos, param)
        return [np.array([j for j in nb[i] if j != i], int) for i in range(n)]
    if rule in ("count", "glance"):
        _, idx = tree.query(pos, int(param) + 1)
        return [idx[i, 1:] for i in range(n)]
    if rule == "sectors_capped":
        # six directions, but drop any link longer than the firefly's 7th-nearest distance
        dk, _ = tree.query(pos, 8)
        base = listen_lists(pos, "sectors", 0)
        return [l[np.linalg.norm(pos[l] - pos[i], axis=1) <= dk[i, 7] + 1e-12] for i, l in enumerate(base)]
    if rule == "random_near":
        # as many links as six-directions gives, same reach (within the 6-direction
        # firefly's longest link), but picked at random: no promise of every side
        rng = np.random.default_rng(int(param))
        base = listen_lists(pos, "sectors", 0)
        out = []
        for i, l in enumerate(base):
            reach = np.linalg.norm(pos[l] - pos[i], axis=1).max()
            cand = [j for j in tree.query_ball_point(pos[i], reach) if j != i]
            out.append(rng.choice(cand, size=min(len(l), len(cand)), replace=False).astype(int))
        return out
    if rule == "sectors":
        _, idx = tree.query(pos, min(n, 60))
        out = []
        for i in range(n):
            d = pos[idx[i, 1:]] - pos[i]
            sec = (np.floor((np.arctan2(d[:, 1], d[:, 0]) + np.pi) / (np.pi / 3)).astype(int)) % 6
            chosen = []
            for s in range(6):
                hit = np.nonzero(sec == s)[0]
                if len(hit):
                    chosen.append(idx[i, 1 + hit[0]])
            out.append(np.array(chosen, int))
        return out
    raise ValueError(rule)


def invert(lists, n):
    """seen_by[j] = fireflies that listen to j."""
    seen_by = [[] for _ in range(n)]
    for i, l in enumerate(lists):
        for j in l:
            seen_by[j].append(i)
    return [np.array(s, int) for s in seen_by]


def run(pos, rule, param, eps=0.08, spread=0.02, periods=60, dt=0.002, seed=0,
        record_every=0, record_from=0.0):
    rng = np.random.default_rng(seed + 7)
    n = len(pos)
    lists = listen_lists(pos, rule, param)
    seen_by = invert(lists, n)
    rate = 1.0 + rng.normal(0, spread, n)
    phase = rng.random(n)
    steps = int(periods / dt)
    flash_times = [[] for _ in range(n)]
    frames = []
    for s in range(steps):
        t = s * dt
        phase += rate * dt
        fired = np.zeros(n, bool)
        queue = list(np.nonzero(phase >= 1.0)[0])
        while queue:
            j = queue.pop()
            if fired[j]:
                continue
            fired[j] = True
            phase[j] = 0.0
            hearers = seen_by[j]
            if rule == "glance":
                # one random firefly anywhere also catches this flash
                hearers = np.append(hearers, rng.integers(n))
            if len(hearers):
                h = hearers[~fired[hearers]]
                phase[h] *= (1.0 + eps)
                queue.extend(h[phase[h] >= 1.0].tolist())
        for j in np.nonzero(fired)[0]:
            flash_times[j].append(t)
        if record_every and s % record_every == 0 and t >= record_from:
            frames.append(phase.copy())
    return flash_times, frames, lists


def beats(flash_times, last=5.0, periods=60, tol=0.03):
    """Over the last few periods: order parameter r (using each firefly's
    phase at the end, read from its last flash), and the number of distinct
    flash moments within one period (groups that flash together)."""
    end = periods
    ph = []
    ts = []
    for ft in flash_times:
        ft = np.array(ft)
        if len(ft) == 0:
            continue
        ph.append((end - ft[-1]) % 1.0)
        ts.extend(ft[ft > end - last].tolist())
    ph = np.array(ph)
    r = abs(np.mean(np.exp(2j * np.pi * ph)))
    # distinct flash moments in the final period
    win = np.sort([t for t in ts if t > end - 1.0])
    groups = 0
    if len(win):
        groups = 1 + int(np.sum(np.diff(win) > tol))
    return r, groups, ph


if __name__ == "__main__":
    import sys
    rule = sys.argv[1]
    param = float(sys.argv[2])
    seeds = range(int(sys.argv[3]) if len(sys.argv) > 3 else 4)
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 400
    for sd in seeds:
        pos = perches(n, 100 + sd)
        ft, _, lists = run(pos, rule, param, seed=sd)
        r, g, _ = beats(ft)
        deg = np.mean([len(l) for l in lists])
        print(f"{rule} {param:g} seed {sd}: r={r:.3f}  flash groups in last period={g}  mean listens={deg:.1f}", flush=True)
