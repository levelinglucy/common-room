"""Picture: the divisor 3 is the quadratic field's unit and class number."""
import json, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

N = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
rows = json.load(open(f"units_N{N}.json"))
n = np.array([r["n"] for r in rows])
cut = np.array([r["cut"] for r in rows])
z = np.array([r["eps_in_Z"] for r in rows])
h3 = np.array([r["h"] % 3 == 0 for r in rows]).astype(int)
k = len(rows)

BG, INK, MUTED = "#fbf8f2", "#222222", "#6b6b6b"
C_Z, C_H, C_NO = "#d1495b", "#edae49", "#c9c9c9"

fig = plt.figure(figsize=(13, 7.2), facecolor=BG)
fig.text(0.04, 0.95, "Ehrlich's divisor 3, explained", fontsize=20, color=INK, weight="bold")
fig.text(0.04, 0.865,
         f"Ring sizes n: primes with n = 5 (mod 8) where 2 is a primitive root, n < {N:,} ({k} sizes).\n"
         "The period falls short by 3 exactly when the field Q(√n) says so: in all {k} of them.".format(k=k),
         fontsize=11.5, color=MUTED)

# Panel A: the 2x2 table
axA = fig.add_axes([0.04, 0.12, 0.40, 0.70]); axA.set_facecolor(BG)
axA.set_xlim(0, 2.3); axA.set_ylim(0, 2.75); axA.axis("off")
axA.text(0.0, 2.62, "A   Every size, sorted two ways", fontsize=13, color=INK, weight="bold")
cells = [  # (col, row, eps_in_Z, h3)
    (0, 1, 1, 1), (1, 1, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0)]
x0, y0, w, hgt = 0.35, 0.25, 0.95, 0.95
for col, row, zz, hh in cells:
    sel = (z == zz) & (h3 == hh)
    tot, c = int(sel.sum()), int(cut[sel].sum())
    colr = C_Z if zz else (C_H if hh else C_NO)
    X, Y = x0 + col * w, y0 + row * hgt
    axA.add_patch(FancyBboxPatch((X + 0.03, Y + 0.03), w - 0.06, hgt - 0.06,
                                 boxstyle="round,pad=0,rounding_size=0.05", fc=colr, ec="none", alpha=0.9))
    axA.text(X + w / 2, Y + hgt * 0.60, f"{tot}", ha="center", va="center", fontsize=24, color=INK, weight="bold")
    axA.text(X + w / 2, Y + hgt * 0.30, f"{c} cut by 3", ha="center", va="center", fontsize=11.5, color=INK)
axA.text(x0 + w / 2, y0 + 2 * hgt + 0.06, "3 divides h", ha="center", fontsize=11.5, color=INK)
axA.text(x0 + 1.5 * w, y0 + 2 * hgt + 0.06, "3 does not divide h", ha="center", fontsize=11.5, color=INK)
axA.text(x0 - 0.05, y0 + 1.5 * hgt, "unit\nwhole", ha="right", va="center", fontsize=11.5, color=INK)
axA.text(x0 - 0.05, y0 + 0.5 * hgt, "unit\nhalves", ha="right", va="center", fontsize=11.5, color=INK)
axA.text(0.0, -0.22,
         "unit whole: ε = x + y√n\nunit halves: ε = (x + y√n)/2 with x, y odd\nε = fundamental unit of Q(√n),  h = its class number",
         fontsize=9.5, color=MUTED)

# Panel B: running proportions
axB = fig.add_axes([0.53, 0.17, 0.43, 0.62]); axB.set_facecolor(BG)
idx = np.arange(1, k + 1)
run_cut = np.cumsum(cut) / idx
run_z = np.cumsum(z) / idx
run_h_only = np.cumsum((1 - z) * h3) / idx
m = idx >= 30
axB.fill_between(n[m], 0, run_z[m], color=C_Z, alpha=0.85, lw=0, label="unit whole (Breuer's rule)")
axB.fill_between(n[m], run_z[m], run_z[m] + run_h_only[m], color=C_H, alpha=0.9, lw=0,
                 label="unit halves, but 3 divides h")
axB.plot(n[m], run_cut[m], color=INK, lw=1.6, label="measured: period cut by 3")
axB.axhline(1 / 3, color=MUTED, lw=1, ls="--")
axB.text(n[-1], 1 / 3 + 0.008, "1/3, a fair die", ha="right", va="bottom", fontsize=10, color=MUTED)
axB.set_xscale("log"); axB.set_ylim(0, 0.5); axB.set_xlim(n[m][0], n[-1])
axB.set_xlabel("ring size n (log scale)", color=INK); axB.set_ylabel("share of sizes so far", color=INK)
for s in ("top", "right"):
    axB.spines[s].set_visible(False)
axB.tick_params(colors=INK)
axB.legend(loc="lower left", frameon=False, fontsize=10)
fig.text(0.53, 0.83, "B   Where the extra cuts come from", fontsize=13, color=INK, weight="bold")

fig.savefig("divisor_three.png", dpi=150, facecolor=BG)

# programmatic checks: text overlap and bounds
fig.canvas.draw()
r = fig.canvas.get_renderer()
texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_text().strip() and t.get_visible()]
boxes = [(t.get_text()[:30], t.get_window_extent(r)) for t in texts]
W, H = fig.canvas.get_width_height()
prob = 0
for i in range(len(boxes)):
    a = boxes[i][1]
    if a.x0 < 0 or a.y0 < 0 or a.x1 > W or a.y1 > H:
        print("OUT", boxes[i][0]); prob += 1
    for j in range(i + 1, len(boxes)):
        b = boxes[j][1]
        if a.overlaps(b) and a.width > 0 and b.width > 0:
            print("OVERLAP", boxes[i][0], "|", boxes[j][0]); prob += 1
print("problems:", prob)
