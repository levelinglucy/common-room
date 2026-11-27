"""pull_or_news.py: is the random glance a pull to the centre, or news about heading?

Last session: 6 nearest + one random bird per step holds the flock (12/12),
but those flocks were also much denser, so maybe the glance only works as a
hidden pull toward the middle. A glance feeds two things into a bird's choice:
  coh   -> a unit vector toward the glanced bird (on average: toward the centre)
  align -> the glanced bird's heading (on average: the flock's mean heading)
This splits them.
  near7        7 nearest, nothing else (the gangs)
  glance       6 nearest + random bird in both align and coh (last session's fix)
  glance_coh   6 nearest + random bird in coh only (pull, no heading news)
  glance_align 6 nearest + random bird in align only (heading news, no pull)
  centroid     6 nearest + a 7th 'neighbour' that is the flock centroid, coh only
  meanhead     6 nearest + a 7th heading that is the flock's mean heading, align only
Each extra counts as one neighbour out of seven, the same weight a glance had.
Same forces, starts and hawk as seven_neighbours.py.
usage: python3 pull_or_news.py MODE SEEDS [hawk]
"""
import sys
import numpy as np
import seven_neighbours as s

MODE = sys.argv[1] if __name__ == "__main__" else "near7"
SEEDS = int(sys.argv[2]) if __name__ == "__main__" else 0
HAWK = __name__ == "__main__" and len(sys.argv) > 3 and sys.argv[3] == "hawk"
G = {}


def step(x, h, mode, R, rng, hawk=None):
    n = len(x)
    diff = x[None, :, :] - x[:, None, :]
    D = np.linalg.norm(diff, axis=-1)
    Dd = D.copy()
    np.fill_diagonal(Dd, np.inf)
    k = 7 if MODE == "near7" else 6
    idx = np.argpartition(Dd, k, axis=1)[:, :k]
    nb = np.zeros((n, n), bool)
    rows = np.arange(n)
    nb[rows[:, None], idx] = True
    toward = diff / Dd[..., None]
    close = Dd < s.R_REP
    rep = -(toward * close[..., None]).sum(1)
    align = (h[None] * nb[..., None]).sum(1)
    coh = (toward * nb[..., None]).sum(1)
    # the 7th input
    if MODE.startswith("glance"):
        g = (rows + G["rng"].integers(1, n, n)) % n
        if MODE in ("glance", "glance_align"):
            align = align + h[g]
        if MODE in ("glance", "glance_coh"):
            coh = coh + toward[rows, g]
    elif MODE == "centroid":
        coh = coh + s.unit(x.mean(0)[None] - x)
    elif MODE == "meanhead":
        align = align + s.unit(h.mean(0)[None])[0]
    desire = s.W_ALIGN * s.unit(align / 7) + s.W_COH * s.unit(coh / 7) + s.W_REP * rep
    desire = desire + 1e-9 * h
    if hawk is not None:
        away = x - hawk
        scared = np.linalg.norm(away, axis=1) < s.HAWK_R
        desire[scared] = s.unit(desire[scared]) + s.W_HAWK * s.unit(away[scared])
    a0 = np.arctan2(h[:, 1], h[:, 0])
    aw = np.arctan2(desire[:, 1], desire[:, 0])
    turn = (aw - a0 + np.pi) % (2 * np.pi) - np.pi
    turn = np.clip(turn, -s.MAX_TURN, s.MAX_TURN) + rng.uniform(-s.NOISE, s.NOISE, n)
    a = a0 + turn
    h = np.stack([np.cos(a), np.sin(a)], 1)
    return x + s.SPEED * h, h, np.full(n, 7)


def shape(x, h):
    D = np.linalg.norm(x[None] - x[:, None], axis=-1)
    np.fill_diagonal(D, np.inf)
    return (np.linalg.norm(x - x.mean(0), axis=1).mean(), np.linalg.norm(h.mean(0)), D.min(1).mean())


if __name__ == "__main__":
    s.step = step
    out = []

    for seed in range(SEEDS):
        G["rng"] = np.random.default_rng(5000 + seed)
        if HAWK:
            r = s.run("topological", 0.0, 1000 + seed, hawk_on=True)
            out.append((r["calm_largest"], r["largest"], r["pieces"]))
            print(f"{MODE} hawk seed {seed}: before {r['calm_largest']:.2f} after {r['largest']:.2f} pieces {r['pieces']}", flush=True)
        else:
            rng = np.random.default_rng(1000 + seed)
            x, h = s.init(rng)
            for _ in range(600):
                x, h, _c = step(x, h, None, 0, rng)
            lab, sizes = s.components(x, s.LINK)
            sp, pol, nn = shape(x, h)
            out.append((sizes[0] / s.N, int((sizes >= 5).sum()), sp, pol, nn))
            print(f"{MODE} seed {seed}: largest {sizes[0]/s.N:.2f} pieces {int((sizes>=5).sum())} spread {sp:.1f} pol {pol:.2f} nn {nn:.2f}", flush=True)
    A = np.array(out, float)
    if HAWK:
        wb, wa = A[:, 0] >= 0.95, A[:, 1] >= 0.95
        print(f"SUMMARY {MODE} hawk: whole before {wb.sum()}/{SEEDS} | whole after {wa.sum()}/{SEEDS} | mean largest after {A[:,1].mean():.2f} | mean pieces {A[:,2].mean():.1f}")
    else:
        print(f"SUMMARY {MODE} calm: whole {(A[:,0]>=0.95).sum()}/{SEEDS} | mean largest {A[:,0].mean():.2f} | pieces {A[:,1].mean():.1f} | spread {A[:,2].mean():.1f} | pol {A[:,3].mean():.2f} | nn {A[:,4].mean():.2f}")
