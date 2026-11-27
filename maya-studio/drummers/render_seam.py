"""Picture: the drummers' trap for even k, even m, and the reach table.

Top left/middle: k = 16 drummers on n = 36 slots (m = 4). Euclid ring vs the
'halves out of step' trap (stuck at j = 7, needs j = 8 = k/2).
Top right: one band from the same start, j = 7 vs j = 8, ring unrolled over
sweeps (rows = sweeps, dots = drummers, long gaps marked).
Bottom: jmin / k for every (k, m) in the sims, k <= 20.
"""
import json, math, random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from drummers import feel, gaps_of, canon, euclid_gaps
from seam import split

k, n = 16, 36
base, minor, m = split(k, n)
E = list(euclid_gaps(k, n))
h = k // 2
for s in range(k):
    c = E[s:] + E[:s]
    if c[:h] == c[h:]:
        g = c
        break
second = g[h:]
trap = g[:h] + second[1:] + second[:1]


def history(k, n, j, seed, max_sweeps=400):
    rng = random.Random(seed)
    pos = sorted(rng.sample(range(n), k))
    occ = set(pos)
    hist = [list(pos)]
    f = lambda d: 1.0 / d
    for sw in range(max_sweeps):
        moved = False
        order = list(range(k)); rng.shuffle(order)
        for i in order:
            p = pos[i]
            here = feel(pos, i, p, j, n, f)
            best, bp = here, p
            steps = [1, -1]; rng.shuffle(steps)
            for st in steps:
                q = (p + st) % n
                if q in occ:
                    continue
                e = feel(pos, i, q, j, n, f)
                if e < best - 1e-12:
                    best, bp = e, q
            if bp != p:
                occ.discard(p); occ.add(bp); pos[i] = bp; moved = True
                hist.append(list(pos))
        if not moved:
            break
    return hist


# find a seed where j = 7 ends stuck off Euclid and j = 8 (same seed) ends in Euclid
Ec = tuple(canon(tuple(E)))
pick = None
for seed in range(200):
    a = history(k, n, 7, seed)
    if canon(gaps_of(a[-1], n)) == Ec:
        continue
    b = history(k, n, 8, seed)
    if canon(gaps_of(b[-1], n)) == Ec:
        pick = (seed, a, b)
        break
seed, A, B = pick
endA = canon(gaps_of(A[-1], n))

fig = plt.figure(figsize=(15, 10.5), facecolor="#0e0f14")
txt = "#e8e6df"; gold = "#f2b84b"; teal = "#5fd0c6"; dim = "#4a4d5a"; red = "#ff6b6b"


def ring(ax, gaps, title, mark_joins=None):
    ax.set_facecolor("#0e0f14"); ax.set_aspect("equal"); ax.axis("off")
    th = lambda p: math.pi / 2 - 2 * math.pi * p / n
    for p in range(n):
        ax.plot(math.cos(th(p)), math.sin(th(p)), ".", color=dim, ms=4)
    pos = [0]
    for x in gaps[:-1]:
        pos.append(pos[-1] + x)
    for i, p in enumerate(pos):
        q = pos[(i + 1) % k] if i + 1 < k else n
        if gaps[i] == minor:
            ts = np.linspace(th(p), th(q), 30)
            ax.plot(1.0 * np.cos(ts), 1.0 * np.sin(ts), color=gold, lw=4, solid_capstyle="round")
    for p in pos:
        ax.plot(math.cos(th(p)), math.sin(th(p)), "o", color=teal, ms=11, mec="#0e0f14")
    if mark_joins:
        for p in mark_joins:
            ax.plot(1.22 * math.cos(th(p)), 1.22 * math.sin(th(p)), marker="v", color=red, ms=12)
    ax.plot([0, 0], [-0.92, 0.92], color=dim, lw=0.8, ls=":")
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.set_title(title, color=txt, fontsize=12, pad=6)


ax1 = fig.add_axes([0.02, 0.45, 0.28, 0.5])
ring(ax1, g, f"The even rhythm: {k} drummers, {n} beats\n(gold = the {m} long gaps, one half repeats the other)")
# joins: start of each half in the trap
pos_t = [0]
for x in trap[:-1]:
    pos_t.append(pos_t[-1] + x)
ax2 = fig.add_axes([0.32, 0.45, 0.28, 0.5])
ring(ax2, trap, "The trap: each half is still right,\nbut the halves are out of step", mark_joins=[pos_t[0], pos_t[h]])

ax3 = fig.add_axes([0.66, 0.47, 0.32, 0.46]); ax3.set_facecolor("#0e0f14")
for col, (H, lab, xoff) in enumerate([(A, "hearing 7 each side", 0), (B, "hearing 8 each side", n + 6)]):
    for t, pos in enumerate(H):
        gs = gaps_of(sorted(pos), n)
        sp = sorted(pos)
        for i, p in enumerate(sp):
            if gs[i] == minor:
                ax3.plot([xoff + p, xoff + p + gs[i]], [t, t], color=gold, lw=1.6, alpha=0.8)
        ax3.plot([xoff + p for p in pos], [t] * k, "o", color=teal, ms=2.2)
    ax3.text(xoff + n / 2, -3.5, lab, color=txt, ha="center", fontsize=11)
    ok = canon(gaps_of(H[-1], n)) == Ec
    ax3.text(xoff + n / 2, len(H) + 1.5, "settles on the even rhythm" if ok else "stuck in the trap", color=teal if ok else red, ha="center", fontsize=11)
ax3.set_ylim(max(len(A), len(B)) + 4, -6)
ax3.set_xlim(-2, 2 * n + 8); ax3.axis("off")
ax3.set_title(f"Same start (seed {seed}), one band, each row = one step", color=txt, fontsize=12)

# bottom: jmin/k table
sim = json.load(open("sweep_km20.json"))
mm = {}
for r in sim:
    b_, mi, mmm = split(r["k"], r["n"])
    mm[(r["k"], mmm)] = r["jmin"]
ks = list(range(4, 21)); ms = list(range(1, 11))
M = np.full((len(ms), len(ks)), np.nan)
for (kk, mv), jm in mm.items():
    if kk in ks and mv in ms:
        M[ms.index(mv), ks.index(kk)] = jm / kk
ax4 = fig.add_axes([0.07, 0.05, 0.62, 0.34]); ax4.set_facecolor("#0e0f14")
im = ax4.imshow(M, origin="lower", cmap="magma", vmin=0.2, vmax=0.55, aspect="auto")
for (kk, mv), jm in mm.items():
    if kk in ks and mv in ms:
        ax4.text(ks.index(kk), ms.index(mv), str(jm), ha="center", va="center", fontsize=8,
                 color="#0e0f14" if jm / kk > 0.42 else txt)
ax4.set_xticks(range(len(ks))); ax4.set_xticklabels(ks, color=txt)
ax4.set_yticks(range(len(ms))); ax4.set_yticklabels(ms, color=txt)
ax4.set_xlabel("drummers k", color=txt); ax4.set_ylabel("long gaps m", color=txt)
for sp_ in ax4.spines.values():
    sp_.set_color(dim)
ax4.tick_params(colors=txt)
ax4.set_title("How far each drummer must listen (number = drummers per side; colour = share of the band)", color=txt, fontsize=11)
ax5 = fig.add_axes([0.72, 0.05, 0.26, 0.34]); ax5.axis("off")
notes = ("m = 1: a third of the band.\nTrap: one squeezed gap and two\nstretched ones, a third apart.\n\n"
         "k and m both even: half the band,\nso everyone hears everyone.\nTrap: two right halves, out of step.\n\n"
         "Every other row: the worst wrong\narrangement of the long gaps\nsets the reach exactly\n(117 of 117 cases, k up to 20).")
ax5.text(0.0, 0.95, notes, color=txt, fontsize=11, va="top", family="DejaVu Sans")
fig.savefig("drummers_seam.png", dpi=110, facecolor=fig.get_facecolor())
print("seed", seed, "moves", len(A) - 1, len(B) - 1, "j=7 end", ''.join(map(str, endA)))
print("trap", ''.join(map(str, trap)), "euclid half-periodic", ''.join(map(str, g)))
