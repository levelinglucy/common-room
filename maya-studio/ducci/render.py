"""ducci_dice.png: three panels.
A  binary Ducci from one lit seat: 16 seats dies, 11 seats comes back one seat over
   every 31 steps (2^5 = -1 mod 11, so 2^5 - 1 steps = one seat).
B  odd ring sizes to 3001: how much the real period falls short of the expected one.
C  the dice: observed cut rate vs (1/q)^c_eff, primes n < 30000.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from collections import defaultdict

BG, FG, DIM, ACC, ACC2 = "#0f1115", "#e8e6e3", "#8a8f98", "#f2b84b", "#5fb3d9"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": FG, "axes.labelcolor": FG,
                     "xtick.color": DIM, "ytick.color": DIM, "axes.edgecolor": DIM})

def spacetime(n, steps):
    a = np.zeros(n, dtype=np.uint8); a[0] = 1
    rows = [a.copy()]
    for _ in range(steps):
        a = a ^ np.roll(a, -1)
        rows.append(a.copy())
    return np.array(rows)

fig = plt.figure(figsize=(15, 9.6), facecolor=BG)
gs = GridSpec(2, 3, figure=fig, width_ratios=[0.55, 1.1, 1.35], height_ratios=[1, 1],
              left=0.04, right=0.98, top=0.88, bottom=0.08, wspace=0.28, hspace=0.42)
fig.text(0.04, 0.955, "Numbers on a ring, each replaced by the gap to its neighbour", fontsize=19, color=FG, weight="bold")
fig.text(0.04, 0.918, "Ducci's game. Once settled, every number is 0 or one value, so it is a pattern of lit seats. "
         "How long until it repeats?", fontsize=11.5, color=DIM)

cm = matplotlib.colors.ListedColormap([BG, ACC])
# A1: 16 seats
ax = fig.add_subplot(gs[0, 0]); ax.set_facecolor(BG)
S = spacetime(16, 20)
ax.imshow(S, cmap=cm, interpolation="nearest", aspect="auto")
ax.axhline(16, color=ACC2, lw=1)
ax.set_title("16 seats: dies at step 16", fontsize=11, color=FG, loc="left")
ax.set_xticks([]); ax.set_ylabel("step", fontsize=10)
ax.text(15.4, 17.3, "all zero", color=ACC2, fontsize=9, ha="right", va="top")
# A2: 11 seats
ax = fig.add_subplot(gs[1, 0]); ax.set_facecolor(BG)
S = spacetime(11, 125)
ax.imshow(S, cmap=cm, interpolation="nearest", aspect="auto")
for k in range(5):
    y = 1 + 31 * k
    ax.axhline(y, color=ACC2, lw=0.8, alpha=0.9)
    lit = np.nonzero(S[y])[0]
    ax.plot(lit, [y] * len(lit), "o", ms=3.2, color=ACC2)
ax.set_title("11 seats: one seat over\nevery 31 steps", fontsize=11, color=FG, loc="left")
ax.set_xticks([]); ax.set_ylabel("step", fontsize=10)

# B: shortfall
ax = fig.add_subplot(gs[:, 1]); ax.set_facecolor(BG)
rows = json.load(open("fast_N3001.json"))
ns = [r["n"] for r in rows if r["cut"]]
fac = [int(r["E"]) // int(r["P"]) for r in rows if r["cut"]]
first_q = [min(r["cut"]) for r in rows if r["cut"]]
clean = [r["n"] for r in rows if not r["cut"]]
ax.scatter(clean, [1] * len(clean), s=3, color=DIM, alpha=0.35, lw=0)
cols = {3: ACC, 5: "#e0735f", 7: ACC2}
for n, f, r in zip(ns, fac, [r for r in rows if r["cut"]]):
    c = cols.get(r["cut"][0], "#b48ce6") if len(set(r["cut"])) == 1 else "#b48ce6"
    ax.scatter([n], [f], s=16, color=c, lw=0, zorder=3)
ax.set_yscale("log"); ax.set_xlim(0, 3060); ax.set_ylim(0.7, 1500)
ax.set_xlabel("odd number of seats", fontsize=10)
ax.set_ylabel("expected period / real period", fontsize=10)
ax.set_title("Where the period falls short (odd sizes to 3001)", fontsize=12, color=FG, loc="left")
notes = {199: ("199: first 7", 230, 11.5), 605: ("605: cut by 397", 120, 1000), 841: ("841: by 233", 920, 300)}
for n, (lab, x, y) in notes.items():
    r = next(r for r in rows if r["n"] == n)
    f = int(r["E"]) // int(r["P"])
    ax.annotate(lab, (n, f), (x, y), color=FG, fontsize=8.5, arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
ax.text(1650, 1.12, "grey: no shortfall (1,376 sizes)", color=DIM, fontsize=8.5)
for i, (lab, c) in enumerate([("cut by 3", ACC), ("by 5", cols[5]), ("by 7", ACC2), ("other / several", "#b48ce6")]):
    ax.scatter([1700], [900 / 1.9 ** i], s=16, color=c, lw=0); ax.text(1760, 900 / 1.9 ** i, lab, color=FG, fontsize=8.5, va="center")
ax.text(1650, 45, "Ehrlich, 1990: up to 165 only\n37, 95, 101, 111, all by 3", color=ACC, fontsize=8.5, va="top")
ax.annotate("37, 95, 101, 111", (75, 3), (20, 1.55), color=FG, fontsize=8.5, arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))

# C: dice
ax = fig.add_subplot(gs[:, 2]); ax.set_facecolor(BG)
rec = json.load(open("dice2_N30000.json"))
st = defaultdict(lambda: [0, 0])
for n, q, ce, cut in rec:
    st[(q, ce)][0] += 1; st[(q, ce)][1] += cut
xs, ys, ss, labs = [], [], [], []
for (q, ce), (e, k) in st.items():
    if k == 0 or e < 25:
        continue
    xs.append((1 / q) ** ce); ys.append(k / e); ss.append(e); labs.append((q, ce, k, e))
line = np.array([0.0015, 0.6])
ax.plot(line, line, color=DIM, lw=1, ls="--")
ax.text(0.0016, 0.00205, "observed = predicted", color=DIM, fontsize=8.5, rotation=36)
for x, y, s, (q, ce, k, e) in zip(xs, ys, ss, labs):
    ax.scatter([x], [y], s=12 + s / 5, color=cols.get(q, "#b48ce6"), alpha=0.9, lw=0, zorder=3)
    txt = f"q={q}, {ce} {'die' if ce == 1 else 'dice'}: {k}/{e}"
    off = {(3, 1): (0.09, 1.12), (7, 1): (1.25, 0.82), (3, 2): (1.25, 0.87), (5, 2): (0.17, 0.72), (11, 1): (0.2, 1.05), (23, 1): (0.6, 1.35), (3, 4): (0.15, 0.95),
           (7, 2): (0.13, 0.95)}.get((q, ce), (1.22, 0.92))
    ax.text(x * off[0], y * off[1], txt, color=FG, fontsize=8.3)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.0015, 0.9); ax.set_ylim(0.0015, 0.9)
ax.set_xlabel("predicted chance (1/q) to the power of the number of dice", fontsize=10)
ax.set_ylabel("how often q really cuts the period", fontsize=10)
ax.set_title("Ehrlich's 3 is a die roll (prime sizes to 30,000)", fontsize=12, color=FG, loc="left")
ax.text(0.0072, 0.0072, "Each prime q dividing the expected period is a die with q faces.\n"
        "Mirror-image seats share a die, so the number of dice is\n"
        "how many separate orbits doubling and flipping make.\n"
        "All dice must land on one face for q to cut.", color=DIM, fontsize=8.6, va="top")
fig.savefig("ducci_dice.png", dpi=130, facecolor=BG)

# overlap / bounds check on all text
fig.canvas.draw()
r = fig.canvas.get_renderer()
W, H = fig.canvas.get_width_height()
boxes = []
for a in fig.axes:
    for t in a.texts + [a.title]:
        if t.get_text():
            boxes.append((t.get_text()[:22], t.get_window_extent(r), a))
for t in fig.texts:
    boxes.append((t.get_text()[:22], t.get_window_extent(r), None))
prob = 0
for i, (s, b, a) in enumerate(boxes):
    if b.x0 < 0 or b.y0 < 0 or b.x1 > W or b.y1 > H:
        print("OUT OF FIGURE:", s); prob += 1
    if a is not None and a.title.get_text()[:22] != s:
        ab = a.get_window_extent(r)
        if b.x0 < ab.x0 - 1 or b.x1 > ab.x1 + 1 or b.y0 < ab.y0 - 1 or b.y1 > ab.y1 + 1:
            print("OUTSIDE AXES:", s); prob += 1
    for s2, b2, a2 in boxes[i + 1:]:
        if b.overlaps(b2):
            print("OVERLAP:", s, "|", s2); prob += 1
print("text problems:", prob)

# text vs data points
hits = 0
for a in fig.axes:
    pts = []
    for coll in a.collections:
        off = coll.get_offsets()
        if len(off):
            pts += list(a.transData.transform(off))
    for line in a.lines:
        xy = line.get_xydata()
        if line.get_marker() not in (None, "None", "") and len(xy):
            pts += list(a.transData.transform(xy))
    for t in a.texts:
        b = t.get_window_extent(r)
        for (x, y) in pts:
            if b.x0 - 2 <= x <= b.x1 + 2 and b.y0 - 2 <= y <= b.y1 + 2:
                hits += 1; print("TEXT ON POINT:", t.get_text()[:30], round(x), round(y))
print("text-on-point hits:", hits)
