"""Picture: three moments of the 600 world, and the loop-size record of all three worlds."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

COLS = np.array([[0, 0, 0], [0, 0, 255], [255, 0, 0], [0, 255, 0], [255, 255, 0],
                 [255, 0, 255], [255, 255, 255], [0, 255, 255], [255, 128, 0]]) / 255
cmap = ListedColormap(COLS)
snaps = np.load("out/snaps_600.npz")
moments = ["5000", "25000", "50000"]
labels = ["step 5,000: the ancestor's family (inner space 11)",
          "step 25,000: many sizes at once",
          "step 50,000: tiny loops (inner space 2 and 3)"]

fig = plt.figure(figsize=(15, 10.5), facecolor="black")
gs = fig.add_gridspec(2, 3, height_ratios=[1.15, 0.85], hspace=0.12, wspace=0.04)
for i, (m, lab) in enumerate(zip(moments, labels)):
    ax = fig.add_subplot(gs[0, i])
    g = snaps[m]
    # zoom to a 260x260 window so loops are visible
    ax.imshow(g[170:430, 170:430], cmap=cmap, vmin=0, vmax=8, interpolation="nearest")
    ax.set_title(lab, color="white", fontsize=11)
    ax.axis("off")

sub = gs[1, :].subgridspec(3, 1, hspace=0.35)
sizes = list(range(2, 13))
for j, N in enumerate([400, 500, 600]):
    rec = json.load(open(f"out/torus_{N}.json"))
    ts = [r["t"] for r in rec]
    M = np.zeros((len(sizes), len(rec)))
    for k, r in enumerate(rec):
        tot = sum(r["loops"].values()) or 1
        for s, c in r["loops"].items():
            if int(s) in sizes:
                M[sizes.index(int(s)), k] = c / tot
    ax = fig.add_subplot(sub[j])
    ax.imshow(M, aspect="auto", origin="lower", cmap="magma", vmin=0, vmax=1,
              extent=[0, ts[-1] / 1000, 1.5, 12.5], interpolation="nearest")
    ax.set_facecolor("black")
    ax.tick_params(colors="white", labelsize=8)
    ax.set_yticks([2, 5, 8, 11])
    ax.set_ylabel(f"{N}x{N}\ninner space", color="white", fontsize=8)
    for sp in ax.spines.values():
        sp.set_color("#555")
    if j == 0:
        ax.set_title("share of loops at each size, three worlds (bright = most loops)", color="white", fontsize=11)
    if j == 2:
        ax.set_xlabel("thousands of steps", color="white", fontsize=9)
fig.savefig("evoloop_strata.png", dpi=90, facecolor="black", bbox_inches="tight")
print("ok")
