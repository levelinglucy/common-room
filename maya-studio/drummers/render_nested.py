"""Picture: the drummers' trap is a trap inside a trap inside a trap.

29 drummers on 70 beats. Left: Euclid's even rhythm. Right: the recursive
trap (rotated to line up with Euclid; it differs by one drummer one beat
off). Each disc has four rings. Outer: drummers on the 70 beats, long gaps
(3 beats) drawn as thick arcs. Next ring in: one slot per gap of the ring
outside it (placed at that gap's middle), a bead where the gap was long.
And so on down Euclid's recursion: 29 -> 12 -> 5 -> 2.
Bottom: fresh sims from nested_check.json.
"""
import json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from seam import split

chk = json.load(open("nested_check.json"))
K, N = chk["k"], chk["n"]
E = chk["euclid"]
T = chk["trap"]
best = max(range(K), key=lambda s: sum(a == b for a, b in zip(E, T[s:] + T[:s])))
T = T[best:] + T[:best]

RADII = [1.0, 0.74, 0.50, 0.28]
INK = "#222222"
LONG = "#d08a2e"
ODD = "#c0392b"
BG = "#fbf8f2"


def levels(gaps, n):
    """Return list of levels. Each level: (angles of its beads, gaps between
    beads (in that level's slots), minor value, slot count)."""
    k = len(gaps)
    pos = np.concatenate([[0], np.cumsum(gaps)[:-1]])
    ang = 2 * math.pi * pos / n
    out = []
    cur_g, cur_ang, cur_n = list(gaps), ang, n
    while True:
        kk = len(cur_g)
        base, minor, m = split(kk, cur_n)
        out.append(dict(ang=cur_ang, gaps=cur_g, minor=minor, n=cur_n, m=m))
        if m < 2:
            break
        # midpoint angle of each gap
        a0 = cur_ang
        a1 = np.roll(cur_ang, -1)
        a1 = np.where(a1 <= a0, a1 + 2 * math.pi, a1)
        mids = (a0 + a1) / 2
        idx = [i for i in range(kk) if cur_g[i] == minor]
        new_ang = mids[idx]
        new_g = [(idx[(t + 1) % len(idx)] - idx[t]) % kk or kk for t in range(len(idx))]
        cur_g, cur_ang, cur_n = new_g, new_ang, kk
    return out


def draw_disc(ax, gaps, title, diff_gaps=None):
    L = levels(gaps, N)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    for li, lev in enumerate(L):
        r = RADII[li]
        ax.add_patch(plt.Circle((0, 0), r, fill=False, lw=0.6, color="#cccccc"))
        if li == 0:
            for s in range(N):
                a = 2 * math.pi * s / N
                ax.plot([0.97 * math.cos(a), 1.03 * math.cos(a)],
                        [0.97 * math.sin(a), 1.03 * math.sin(a)], color="#d9d4ca", lw=0.6)
        ang = lev["ang"]
        kk = len(ang)
        for i in range(kk):
            a0 = ang[i]
            a1 = ang[(i + 1) % kk]
            if a1 <= a0:
                a1 += 2 * math.pi
            if lev["gaps"][i] == lev["minor"] and lev["m"] >= 1:
                col = LONG
                ax.add_patch(Arc((0, 0), 2 * r, 2 * r, theta1=math.degrees(a0),
                                 theta2=math.degrees(a1), lw=4.0, color=col, alpha=0.85))
                # spoke to the bead one ring in
                if li + 1 < len(L):
                    am = (a0 + a1) / 2
                    r2 = RADII[li + 1]
                    ax.plot([r * math.cos(am), r2 * math.cos(am)],
                            [r * math.sin(am), r2 * math.sin(am)], color=LONG, lw=0.7, alpha=0.6)
        ax.scatter(np.cos(ang) * r, np.sin(ang) * r, s=[34, 30, 34, 60][li],
                   color=INK, zorder=5)
        if li == len(L) - 1:
            lev_last = lev
    if diff_gaps:
        lev0 = L[0]
        for i in diff_gaps:
            a = (lev0["ang"][i] + lev0["ang"][(i + 1) % K]) / 2
            ax.annotate("", xy=(1.06 * math.cos(a), 1.06 * math.sin(a)),
                        xytext=(1.2 * math.cos(a), 1.2 * math.sin(a)),
                        arrowprops=dict(arrowstyle="->", color=ODD, lw=1.4))
    # bottom ring: label its two beads' split
    last = L[-1]
    ax.text(0, -0.02, f"{'+'.join(map(str, last['gaps']))}", ha="center", va="center",
            fontsize=11, color=ODD if diff_gaps else INK, fontweight="bold")
    ax.set_title(title, fontsize=12, color=INK, pad=4)
    return L


fig = plt.figure(figsize=(11, 8.6), facecolor=BG)
axL = fig.add_axes([0.02, 0.24, 0.46, 0.66])
axR = fig.add_axes([0.52, 0.24, 0.46, 0.66])
for ax in (axL, axR):
    ax.set_facecolor(BG)
diff = [i for i in range(K) if E[i] != T[i]]
LE = draw_disc(axL, E, "Euclid: the even rhythm")
LT = draw_disc(axR, T, "The trap: one drummer one beat off", diff_gaps=diff)

fig.text(0.5, 0.955, "29 drummers on 70 beats: a mistake inside a mistake inside a mistake",
         ha="center", fontsize=15, color=INK)
fig.text(0.5, 0.918,
         "Rings from outside in: drummers on 70 beats; then one slot per gap with a dot where the gap was long; and again",
         ha="center", fontsize=9.5, color="#555555")

sizes = [f"{len(l['ang'])} on {l['n']}" for l in LE]
fig.text(0.5, 0.215, "Ring by ring (outer to inner):  " + "   ->   ".join(sizes),
         ha="center", fontsize=10.5, color=INK)
rowsE = "   ".join("".join(map(str, l["gaps"])) for l in LE)
rowsT = "   ".join("".join(map(str, l["gaps"])) for l in LT)
fig.text(0.5, 0.18, "Euclid gaps:  " + rowsE, ha="center", fontsize=9, family="monospace", color=INK)
fig.text(0.5, 0.155, "Trap gaps:    " + rowsT, ha="center", fontsize=9, family="monospace", color=ODD)

r11 = chk["res"]["11"]
r12 = chk["res"]["12"]
runs = chk["runs"]
fig.text(0.5, 0.10,
         f"Each drummer hearing 11 neighbours per side: {r11.get('trap', 0)} of {runs} bands stopped in exactly this trap, "
         f"{r11.get('euclid', 0)} found Euclid.",
         ha="center", fontsize=10.5, color=INK)
fig.text(0.5, 0.072,
         f"Hearing 12 per side: {r12.get('euclid', 0)} of {runs} found Euclid.",
         ha="center", fontsize=10.5, color=INK)
fig.text(0.5, 0.03,
         "At the bottom the trap's two beads sit 1 and 4 apart instead of 2 and 3: a squeeze, the simplest wrong rhythm there is.",
         ha="center", fontsize=9.5, color="#555555")
fig.savefig("nested_rings.png", dpi=130, facecolor=BG)
print("diff gaps", diff)
print("E levels", ["".join(map(str, l["gaps"])) for l in LE])
print("T levels", ["".join(map(str, l["gaps"])) for l in LT])
