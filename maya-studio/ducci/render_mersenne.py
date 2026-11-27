"""Picture for the Mersenne rule: cut by q = 2^d - 1 <=> units of the degree-d field are 1 mod 2
OR Frobenius at 2 acts on Cl/q by 2. Panel A: every one-die case for q = 3, 7, 31 sorted by
category, with how many were cut. Panel B: the 29 cubic fields with 7 | h3, by eigenvalue."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, CUT, NOT = "#222222", "#c0392b", "#bdc3c7"
data = {3: json.load(open("mersenne_q3_N30000.json")),
        7: json.load(open("cubic7b_N30000.json")),
        31: json.load(open("mersenne_q31_N30000.json"))}
for o in data[7]:
    o["h"] = o["h3"]

cats = [("units all 1 mod 2", lambda o, q: o["units_one"] == 1),
        ("class group, eigenvalue 2", lambda o, q: o["units_one"] != 1 and o["eig2"] == 1),
        ("class group, other eigenvalue", lambda o, q: o["units_one"] != 1 and o["h"] % q == 0 and o["eig2"] != 1),
        ("neither", lambda o, q: o["units_one"] != 1 and o["h"] % q != 0)]

fig = plt.figure(figsize=(13, 6.2), dpi=130)
axA = fig.add_axes([0.25, 0.20, 0.33, 0.62])
axB = fig.add_axes([0.66, 0.20, 0.31, 0.62])

rows, labels = [], []
y = 0
yt = []
for q in (3, 7, 31):
    for name, f in cats:
        sel = [o for o in data[q] if f(o, q)]
        n, c = len(sel), sum(o["cut"] for o in sel)
        rows.append((y, n, c))
        labels.append(f"q = {q}: {name}")
        y += 1
    y += 0.8
for (yy, n, c), lab in zip(rows, labels):
    if n:
        axA.barh(yy, c, color=CUT, height=0.7, log=False)
        axA.barh(yy, n - c, left=c, color=NOT, height=0.7)
    axA.text(max(n, 1) * 1.15 if n else 1.15, yy, f"{c} of {n} cut", va="center", fontsize=8.5, color=INK)
axA.set_xscale("symlog", linthresh=1)
axA.set_xlim(0, 3000)
axA.set_yticks([r[0] for r in rows])
axA.set_yticklabels(labels, fontsize=8.5)
axA.invert_yaxis()
axA.set_xlabel("prime ring sizes below 30,000 (log scale)", fontsize=9)
axA.set_title("A. Every one-die case for q = 3, 7, 31\nred = period cut by q, grey = not cut", fontsize=10, loc="left")
for s in ("top", "right"):
    axA.spines[s].set_visible(False)

c7 = [o for o in data[7] if o["h3"] % 7 == 0]
lane = {(1, 0): 0, (0, 1): 1, (1, 1): 2}
lane_names = ["eigenvalue 2", "eigenvalue 4", "both (Cl = 7 x 7)"]
for o in c7:
    yy = lane[(o["eig2"], o["eig4"])]
    filled = o["cut"] == 1
    mk = "s" if o["units_one"] == 1 else "o"
    axB.scatter(o["p"], yy, s=70, marker=mk, facecolor=CUT if filled else "white",
                edgecolor=CUT if filled else "#7f8c8d", linewidth=1.3, zorder=3)
axB.set_yticks([0, 1, 2])
axB.set_yticklabels(lane_names, fontsize=8.5)
axB.set_ylim(2.6, -0.6)
axB.set_xlim(0, 30000)
axB.set_xlabel("ring size p", fontsize=9)
axB.set_title("B. The 29 cubic fields with 7 | class number\nhow Frobenius at 2 acts on the class group mod 7", fontsize=10, loc="left")
axB.grid(axis="x", color="#eeeeee", zorder=0)
for s in ("top", "right"):
    axB.spines[s].set_visible(False)
h1 = axB.scatter([], [], s=60, marker="o", facecolor=CUT, edgecolor=CUT, label="cut by 7")
h2 = axB.scatter([], [], s=60, marker="o", facecolor="white", edgecolor="#7f8c8d", label="not cut")
h3 = axB.scatter([], [], s=60, marker="s", facecolor=CUT, edgecolor=CUT, label="units already 1 mod 2")
axB.legend(handles=[h1, h2, h3], fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, frameon=False)

fig.text(0.02, 0.955, "The Ducci ring is cut by q = 2^d - 1 exactly when the degree-d field inside it has units that are all 1 mod 2, "
         "or a class group that Frobenius at 2 turns by 2.", fontsize=10.5, color=INK)
fig.text(0.02, 0.925, "1,704 of 1,704 prime ring sizes below 30,000 follow it (q = 3: 604, q = 7: 723, q = 31: 377). "
         "For q = 7, seven dividing the class number is not enough: the eigenvalue decides.", fontsize=9, color="#555555")
fig.savefig("mersenne_rule.png")

# programmatic checks: text overlap and bounds
fig.canvas.draw()
r = fig.canvas.get_renderer()
W, H = fig.bbox.width, fig.bbox.height
texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_text().strip() and t.get_visible()]
boxes = [(t.get_text()[:30], t.get_window_extent(r)) for t in texts]
prob = 0
for i in range(len(boxes)):
    a = boxes[i][1]
    if a.x0 < -1 or a.y0 < -1 or a.x1 > W + 1 or a.y1 > H + 1:
        print("out of bounds:", boxes[i][0]); prob += 1
    for j in range(i + 1, len(boxes)):
        b = boxes[j][1]
        if a.overlaps(b) and a.width > 0 and b.width > 0:
            print("overlap:", boxes[i][0], "|", boxes[j][0]); prob += 1
print("problems:", prob)
