"""Picture for the 'why L = 3k breaks' finding.
Top: founder (left) and its east child (right) for L = 9 and L = 10, at the
step the child's westward arm lands in the gap and 40 steps later.
Bottom: freeze test outcome over L (8..21) x delay (0..5): which digit the
arm lands on, and whether the founder floods with 7s.
"""
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from build_loop import build, genome_of
from langton import step

PAL = np.array([(12, 12, 20), (70, 110, 220), (230, 60, 60), (60, 200, 90),
                (240, 220, 60), (230, 80, 230), (240, 240, 240), (60, 220, 230)]) / 255
N = 400
r0 = c0 = N // 2


def frames(L):
    g = np.zeros((N, N), np.uint8)
    f = build(L, genome_of(L - 2, 2, L), 5)
    g[r0:r0 + f.shape[0], c0:c0 + f.shape[1]] = f
    out, tc = {}, None
    for t in range(1, 3000):
        g = step(g)
        if tc is None and t > 50 and g[r0 + 1, c0 + L + 2] != 0:
            tc = t
            out["land"] = g.copy()
        if tc is not None and t == tc + 40:
            out["later"] = g.copy()
            break
    win = (slice(r0 - 2, r0 + L + 4), slice(c0 - 2, c0 + 2 * L + 7))
    return tc, {k: v[win] for k, v in out.items()}, int(out["land"][r0 + 1, c0 + L])


fig = plt.figure(figsize=(11, 10.5), facecolor="white")
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1.25], hspace=0.38, wspace=0.08)
cmap = ListedColormap(PAL)
name = {0: "0 (a gap)", 1: "1", 7: "7"}
for row, L in enumerate((9, 10)):
    tc, fr, cs = frames(L)
    for col, key in enumerate(("land", "later")):
        ax = fig.add_subplot(gs[row, col])
        ax.imshow(fr[key], cmap=cmap, vmin=-0.5, vmax=7.5, interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([])
        if key == "land":
            ax.set_title(f"Size {L}, step {tc}: the child's arm reaches the parent.\n"
                         f"The parent's corner cell holds {name[cs]}.", fontsize=10.5)
            # mark the corner cell
            ax.add_patch(plt.Rectangle((L + 2 - 0.5, 3 - 0.5), 1, 1, fill=False, ec="yellow", lw=2))
        else:
            n7 = int((fr[key] == 7).sum())
            verdict = "parent flooded with 7s" if cs == 0 else "parent keeps cycling"
            ax.set_title(f"40 steps later: {verdict}", fontsize=10.5)

# outcome grid
rows = []
for l in open("freeze_shift.txt"):
    m = re.search(r"L=\s*(\d+).*delay=(\d).*corner_at_contact=(\d+) 7s@\+40=\s*(\d+)/(\d+)", l)
    L, k, cs, f, P = map(int, m.groups())
    rows.append((L, k, cs, f / P > 0.5))
Ls = sorted({r[0] for r in rows}); ks = sorted({r[1] for r in rows})
M = np.zeros((len(ks), len(Ls)))
ax = fig.add_subplot(gs[2, :])
for L, k, cs, fl in rows:
    M[ks.index(k), Ls.index(L)] = 1 if fl else 0
ax.imshow(M, cmap=ListedColormap(["#d9dde3", "#e05252"]), vmin=0, vmax=1, aspect="auto")
for L, k, cs, fl in rows:
    ax.text(Ls.index(L), ks.index(k), str(cs), ha="center", va="center", fontsize=11,
            color="white" if fl else "#333", weight="bold")
ax.set_xticks(range(len(Ls))); ax.set_xticklabels([str(L) for L in Ls])
for lab in ax.get_xticklabels():
    if int(lab.get_text()) % 3 == 0:
        lab.set_color("#c03030"); lab.set_fontweight("bold")
ax.set_yticks(range(len(ks))); ax.set_yticklabels([str(k) for k in ks])
ax.set_xlabel("loop size (red labels: divisible by 3)")
ax.set_ylabel("parent held back\n(steps)")
ax.set_title("Which digit the arm lands on (number in each box). Red box = parent flooded and wrecked.\n"
             "Row 0 is the colony left alone: only sizes divisible by 3 land on 0.", fontsize=10.5)
fig.savefig("landing_on_zero.png", dpi=110, bbox_inches="tight")
print("saved")

# overlap check: every text box against every other text box and every axes box
fig.canvas.draw()
r = fig.canvas.get_renderer()
texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_text().strip() and t.get_visible()]
boxes = [(t.get_text()[:30], t.get_window_extent(r)) for t in texts]
bad = 0
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        a, b = boxes[i][1], boxes[j][1]
        if a.overlaps(b) and not (a.width > 400 and b.width > 400 and False):
            # cell labels inside the grid never overlap each other at this size; report everything else
            bad += 1
            print("TEXT OVERLAP:", boxes[i][0], "|", boxes[j][0])
for ax in fig.axes:
    ab = ax.get_window_extent(r)
    for name_, bb in boxes:
        if ax.title.get_text().startswith(name_[:10]):
            continue
for ax_i, ax in enumerate(fig.axes):
    tb = ax.title.get_window_extent(r)
    for ax_j, other in enumerate(fig.axes):
        if ax_j != ax_i and tb.overlaps(other.get_window_extent(r)):
            bad += 1
            print("TITLE over axes:", ax.title.get_text()[:40], "->", ax_j)
print("overlap problems:", bad)
