"""Final calm positions (600 steps, seed 1009) for three rules, coloured by piece."""
import subprocess, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seven_neighbours as s
import importlib

PANELS = [("near7", "+ its seventh nearest bird"),
          ("glance_align", "+ one random bird's heading"),
          ("centroid", "+ a pull to the flock's middle")]


def final(mode):
    mod = importlib.import_module("pull_or_news")
    mod.MODE = mode
    mod.G["rng"] = np.random.default_rng(5009)
    rng = np.random.default_rng(1009)
    x, h = s.init(rng)
    for _ in range(600):
        x, h, _c = mod.step(x, h, None, 0, rng)
    return x, h


fig, axs = plt.subplots(1, 3, figsize=(15, 5.4), facecolor="#0b0d14")
cmap = plt.get_cmap("tab20")
for ax, (mode, title) in zip(axs, PANELS):
    x, h = final(mode)
    lab, sizes = s.components(x, s.LINK)
    order = np.argsort(-np.bincount(lab))
    rank = np.empty_like(order); rank[order] = np.arange(len(order))
    col = cmap(rank[lab] % 20)
    ax.set_facecolor("#0b0d14")
    ax.scatter(x[:, 0], x[:, 1], s=6, c=col)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#333")
    n = int((sizes >= 5).sum())
    ax.set_title(f"{title}\n{n} piece{'s' if n != 1 else ''}, largest {sizes[0]*100//s.N}%",
                 color="#ddd", fontsize=12)
fig.suptitle("Six nearest birds, plus one more input. Same birds, same start, 600 steps.",
             color="#eee", fontsize=13)
fig.tight_layout()
fig.savefig("pull_or_news.png", dpi=110, facecolor=fig.get_facecolor())
print("saved")
