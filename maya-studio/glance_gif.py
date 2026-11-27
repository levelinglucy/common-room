"""glance_gif.py: count seven vs six nearest + one random glance, same birds, same hawk.
usage: python3 glance_gif.py [seed]
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import seven_neighbours as s

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1009
RULES = [(None, 0, "count seven"),
         (0.3, 0, "six nearest + a random glance\n1 step in 3"),
         (1.0, 0, "six nearest + a random glance\nevery step")]
G = {}
_orig = s.neighbour_mask


def mask(D, mode, R):
    if G["P"] is None:
        return _orig(D, "topological", R)
    n = D.shape[0]
    Dd = D.copy()
    np.fill_diagonal(Dd, np.inf)
    idx = np.argpartition(Dd, 6, axis=1)[:, :6]
    m = np.zeros_like(D, dtype=bool)
    rows = np.arange(n)
    m[rows[:, None], idx] = True
    g = (rows + G["rng"].integers(1, n, n)) % n
    who = G["rng"].random(n) < G["P"]
    m[rows[who], g[who]] = True
    return m


s.neighbour_mask = mask
EVERY = 4
PALETTE = plt.cm.tab20(np.linspace(0, 1, 20))


def simulate(P, R):
    G["P"] = P
    G["rng"] = np.random.default_rng(seed + 4000)
    mode = "topological"
    rng = np.random.default_rng(seed)
    x, h = s.init(rng)
    out = []
    hawk = None
    for t in range(s.WARM + s.AFTER):
        if t == s.WARM:
            lab, sizes = s.components(x, s.LINK)
            centre = x[lab == np.bincount(lab).argmax()].mean(0)
            hd = h.mean(0); hd /= np.linalg.norm(hd)
            perp = np.array([-hd[1], hd[0]])
            dirn = s.unit((0.6 * hd + perp)[None])[0]
            T = 25
            hawk = centre + hd * s.SPEED * T - dirn * s.HAWK_SPEED * T
        x, h, cnt = s.step(x, h, mode, R, rng, hawk)
        if hawk is not None:
            hawk = hawk + s.HAWK_SPEED * dirn
        if t % EVERY == 0:
            lab, sizes = s.components(x, s.LINK)
            # order labels by size so the biggest piece keeps colour 0
            order = np.argsort(-np.bincount(lab))
            rank = np.empty_like(order); rank[order] = np.arange(len(order))
            out.append((x.copy(), h.copy(), rank[lab], None if hawk is None else hawk.copy(),
                        len(sizes[sizes >= 5])))
    return out


sims = [simulate(m, R) for m, R, _ in RULES]
print("simulated", flush=True)

fig, axes = plt.subplots(1, 3, figsize=(12, 4.4), facecolor="#0b0d12")
fig.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.02, wspace=0.04)
W = 70


def draw(k):
    for ax, sim, (m, R, title) in zip(axes, sims, RULES):
        ax.clear()
        ax.set_facecolor("#0b0d12")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#222833")
        x, h, lab, hawk, pieces = sim[k]
        big = lab == 0
        c = np.median(x[big], 0)
        cols = PALETTE[lab % 20]
        ax.quiver(x[:, 0], x[:, 1], h[:, 0], h[:, 1], color=cols, scale=60, width=0.006,
                  headwidth=3, headlength=4, pivot="mid")
        if hawk is not None and np.all(np.abs(hawk - c) < W):
            ax.plot(*hawk, marker="^", color="#ff4a4a", ms=11)
        ax.set_xlim(c[0] - W / 2, c[0] + W / 2)
        ax.set_ylim(c[1] - W / 2, c[1] + W / 2)
        ax.set_aspect("equal")
        ax.set_title(f"{title}  ({pieces} piece{'s' if pieces != 1 else ''})", color="#d8dde6",
                     fontsize=10)
    t = k * EVERY
    fig.suptitle("calm" if t < s.WARM else "hawk!", color="#ff8a8a" if t >= s.WARM else "#8a93a6",
                 fontsize=10, y=0.985)


n = len(sims[0])
anim = FuncAnimation(fig, draw, frames=n, interval=60)
anim.save("glance.gif", writer=PillowWriter(fps=16), dpi=72)
draw(n - 1)
fig.savefig("glance_final.png", dpi=90, facecolor=fig.get_facecolor())
print("saved", n, "frames")
