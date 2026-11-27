"""render_beat.py -> ulam_beat.png: the hidden beat in Ulam sequences."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fold import BS, folded

INK, PAPER, DIM = "#1d1b2f", "#f6f1e7", "#9a93a8"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})

fig = plt.figure(figsize=(13, 8.6), facecolor=PAPER)
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], hspace=0.42, wspace=0.22)

# Panel 1: U(1,2) folded by 2pi/2.5714476
ax = fig.add_subplot(gs[0, :]); ax.set_facecolor(PAPER)
u = np.loadtxt("u12.txt", dtype=np.int64)
a = 2.5714475771
ph = (a * u.astype(float)) % (2 * np.pi) / (2 * np.pi)
sh = (ph + 0.5) % 1.0   # put phase 0 at the centre so the empty zone sits in the middle
h, e = np.histogram(sh, bins=200, range=(0, 1))
ax.bar(e[:-1], h, width=e[1] - e[0], align="edge", color=INK)
lo, hi = 0.5 - 0.296, 0.5 + 0.296
ax.axvspan(lo, hi, color="#e3d9c6", zorder=0)
for t in [2, 3, 8, 36, 47, 69, 102, 273, 339]:
    s = ((a * t) % (2 * np.pi) / (2 * np.pi) + 0.5) % 1.0
    ax.plot([s, s], [0, max(h) * 0.06], color="#c0392b", lw=1.5)
for label, s in [("36, 102, 273, 339", 0.236), ("2", 0.319), ("3, 8, 47, 69", 0.75)]:
    ax.text(s, max(h) * 0.10, label, ha="center", fontsize=10, color="#c0392b")
ax.text(0.5, max(h) * 0.72, "shaded: 59% of the clock. Only 9 of the 147,960 terms ever land here,\nall of them 339 or smaller (marked in red)",
        ha="center", fontsize=11)
ax.set_xlim(0, 1); ax.set_yticks([])
ax.set_xticks([0, 0.25, 0.5, 0.75, 1]); ax.set_xticklabels(["1/2", "3/4", "0", "1/4", "1/2"])
for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
ax.set_title("Ulam's sequence 1, 2, 3, 4, 6, 8, 11, 13, 16, 18, 26, ...  wrapped round a clock of 2.4434 steps\n"
             f"all {len(u):,} terms up to 2,000,000", fontsize=12, loc="left")
ax.set_xlabel("where each term lands on the clock")

# Panel 2: period minus 3b
ax2 = fig.add_subplot(gs[1, 0]); ax2.set_facecolor(PAPER)
rows = []
for b in BS:
    ub, ab, phb = folded(b)
    rows.append((b, 2 * np.pi / ab, phb))
bs = np.array([r[0] for r in rows]); P = np.array([r[1] for r in rows])
ax2.plot(bs, P - 3 * bs, "o", color=INK)
ax2.set_ylim(0.4165, 0.4175); ax2.set_yticks([0.4166, 0.4168, 0.4170, 0.4172, 0.4174])
ax2.axhline(0.417034, color=DIM, lw=1, ls="--")
ax2.set_xlabel("second starting number b, in 1, b, ...")
ax2.set_ylabel("hidden clock length  minus  3b")
ax2.set_title("start 1, b instead: the clock is always 3b + 0.41703", fontsize=12, loc="left")
for s in ["top", "right"]: ax2.spines[s].set_visible(False)

# Panel 3: folded shapes
ax3 = fig.add_subplot(gs[1, 1]); ax3.set_facecolor(PAPER)
cmap = plt.get_cmap("plasma")
for i, (b, Pb, phb) in enumerate(rows):
    if b not in (4, 6, 10, 16, 30):
        continue
    hh, ee = np.histogram(phb, bins=120, range=(0, 1), density=True)
    ax3.plot((ee[:-1] + ee[1:]) / 2, hh, color=cmap(i / len(rows)), lw=1.4, label=f"b = {b}")
ax3.set_xlim(0.25, 0.75); ax3.set_yticks([])
ax3.set_xticks([0.25, 1/3, 0.5, 2/3, 0.75]); ax3.set_xticklabels(["1/4", "1/3", "1/2", "2/3", "3/4"])
ax3.legend(frameon=False, fontsize=9)
ax3.set_xlabel("where each term lands on its own clock")
ax3.set_title("and every b draws the same fingerprint, sharper as b grows", fontsize=12, loc="left")
for s in ["top", "right", "left"]: ax3.spines[s].set_visible(False)

fig.text(0.01, 0.005, "Each term is the smallest number that is a sum of two earlier terms in exactly one way. "
         "Hidden beat: Steinerberger 2017; the 1, b family's rigidity: Hinman, Kuca, Schlesinger, Sheydvasser. Drawn my way, probably known.",
         fontsize=8.5, color=DIM)
fig.savefig("ulam_beat.png", dpi=130, facecolor=PAPER, bbox_inches="tight")
print("saved; panel-3 rows:", [r[0] for r in rows if r[0] in (4, 6, 10, 16, 30)])
print("panel-1 counts inside shaded zone:", int(((sh > lo) & (sh < hi)).sum()))
