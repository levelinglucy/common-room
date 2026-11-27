"""Fault map: same perches, 8 runs with new phases and rates. Left: each
7-nearest link coloured by how often it ended up on a choir border. Right:
the same links coloured by a graph-only score (few shared neighbours =
bright), computed before any firefly flashed."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import firefly as ff
from cause import graph_scores

p = int(sys.argv[1]) if len(sys.argv) > 1 else 2
mode = sys.argv[2] if len(sys.argv) > 2 else "both"
pos = ff.perches(400, 100 + p)
lists = ff.listen_lists(pos, "count", 7)
edges = np.array([(i, j) for i, l in enumerate(lists) for j in l])
freq = np.nan_to_num(np.load(f"cause_out/freq_p{p}_{mode}.npy"))
nb, _ = graph_scores(lists, 400)
ov = np.array([len(nb[i] & nb[j]) for i, j in edges])
seg = pos[edges]
fig, ax = plt.subplots(1, 2, figsize=(12, 6.2), facecolor="#0b0b14")
for a, val, title in ((ax[0], freq, "how often each link was a choir border (8 runs)"),
                      (ax[1], np.clip((6 - ov) / 6, 0, 1), "few shared neighbours (graph only, before any flash)")):
    o = np.argsort(val)
    lc = LineCollection(seg[o], colors=plt.cm.inferno(0.08 + 0.92 * val[o]), linewidths=0.6 + 2.2 * val[o])
    a.add_collection(lc)
    a.scatter(pos[:, 0], pos[:, 1], s=3, c="#9fb4ff", zorder=3)
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.set_aspect("equal"); a.axis("off")
    a.set_title(title, color="#ddd", fontsize=10)
plt.tight_layout()
plt.savefig(f"fault_map_p{p}.png", dpi=110, facecolor=fig.get_facecolor())
print("saved", f"fault_map_p{p}.png", "links freq>=0.5:", int((freq >= .5).sum()), "of", len(freq))
