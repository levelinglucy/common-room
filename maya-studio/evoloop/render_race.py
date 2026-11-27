"""Share of hole-2 loops (among 2s and 3s) over time, three conditions."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

runs = [("one 3 founder", "out/racev_three.json", 500, "#d9822b"),
        ("one 2 founder", "out/racev_two.json", 500, "#2b7bd9"),
        ("one of each", "out/race_both.json", 1000, "#555555")]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=130)
for name, path, every, col in runs:
    R = json.load(open(path))
    for i, rec in enumerate(R):
        t = np.arange(len(rec)) * every
        s = [d.get("2", 0) / (d.get("2", 0) + d.get("3", 0)) if d.get("2", 0) + d.get("3", 0) else np.nan for d in rec]
        ax.plot(t, s, color=col, alpha=0.55, lw=1.1, label=name if i == 0 else None)
ax.set_xlabel("step")
ax.set_ylabel("share of 2s among 2s and 3s")
ax.set_ylim(-0.03, 1.03)
ax.set_title("Evoloop: 3s slide to 2s, 2s throw up a few 3s that fade")
ax.legend(loc="lower right", frameon=False)
fig.tight_layout()
fig.savefig("race_2v3.png")
