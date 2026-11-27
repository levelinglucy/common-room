"""Picture: the choirs of the 7-nearest forest (seed 0), and the listening
links that cross a choir border, drawn under two rules on the same split.
Left: the 7-nearest links the forest actually used. Right: the six-direction
links it would have had."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import firefly as ff
from borders import choir_labels, crossing

sd = 0
pos = ff.perches(400, 100 + sd)
ft, _, l7 = ff.run(pos, "count", 7, eps=0.03, periods=200, seed=sd)
lab = choir_labels(ft)
l6 = ff.listen_lists(pos, "sectors", 0)

palette = ["#f2c14e", "#5fb3d6", "#e07a9a", "#8fd17c", "#b39ddb", "#f28c4e", "#7fd1c7"]
sizes = np.bincount(lab[lab >= 0])
rank = {c: k for k, c in enumerate(np.argsort(-sizes))}
cols = [palette[rank[c] % len(palette)] if c >= 0 else "#555555" for c in lab]

fig, axes = plt.subplots(1, 2, figsize=(12, 6.4), facecolor="#0b0d14")
stats = {}
for ax, lists, name in [(axes[0], l7, "7 nearest (what they used)"), (axes[1], l6, "nearest in each of 6 directions")]:
    ax.set_facecolor("#0b0d14")
    inside, across = [], []
    for i, l in enumerate(lists):
        for j in l:
            seg = [pos[i], pos[j]]
            if lab[i] >= 0 and lab[j] >= 0 and lab[i] != lab[j]:
                across.append(seg)
            else:
                inside.append(seg)
    ax.add_collection(LineCollection(inside, colors="#3a4055", linewidths=0.5, alpha=0.7))
    ax.add_collection(LineCollection(across, colors="#ff3b3b", linewidths=1.6, alpha=0.95))
    ax.scatter(pos[:, 0], pos[:, 1], s=60, c=cols, alpha=0.18, linewidths=0)
    ax.scatter(pos[:, 0], pos[:, 1], s=12, c=cols, linewidths=0)
    frac = crossing(lists, lab)
    stats[name] = (len(across), frac)
    ax.set_title(f"{name}\n{len(across)} links cross a choir border ({100*frac:.1f}% of links)",
                 color="#e8e8f0", fontsize=12)
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02); ax.set_aspect("equal"); ax.axis("off")
fig.suptitle("Same fireflies, same choirs. The choirs sit on the seams of the 7-nearest web.",
             color="#e8e8f0", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("choir_seams.png", dpi=110, facecolor=fig.get_facecolor())
print(stats, "choir sizes", sorted(sizes.tolist(), reverse=True))
