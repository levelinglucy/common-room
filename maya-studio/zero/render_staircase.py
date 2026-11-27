"""Picture: a corridor standing on a foot, its zero, and the staircase in the
zero's potential that carries the change up the corridor."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from depth import shapes
from odometer import zero_odo

w, fh, H = 24, 24, 420
strip, tee, x0 = shapes(w, H, 3 * w, fh)
es, u1s, u2s = zero_odo(strip)
et, u1t, u2t = zero_odo(tee)
dv = (u2t - u1t) - (u2s - u1s)
base = H + 2 - fh

# crop: 130 rows of corridor above the foot, the foot, a margin each side
top, bot = base - 130, H + 3
left, right = x0 - 40, x0 + w + 40
crop = (slice(top, bot), slice(left, right))

pal = ListedColormap(["#0b0b14", "#3b2a6b", "#c2477a", "#f6c453", "#000000"])


def show_zero(ax, e, mask, title):
    img = np.where(mask, e, 4)[crop]
    ax.imshow(img, cmap=pal, vmin=0, vmax=4, interpolation="nearest")
    ax.set_title(title, color="w", fontsize=10)
    ax.axis("off")


fig = plt.figure(figsize=(12, 7.5), facecolor="black")
ax1 = fig.add_axes([0.02, 0.06, 0.22, 0.86])
ax2 = fig.add_axes([0.26, 0.06, 0.22, 0.86])
ax3 = fig.add_axes([0.50, 0.06, 0.22, 0.86])
ax4 = fig.add_axes([0.79, 0.12, 0.19, 0.76], facecolor="#0b0b14")

show_zero(ax1, es, strip, "zero of the corridor alone")
show_zero(ax2, et, tee, "zero with a foot")

d = np.where(tee, -dv, np.nan)[crop].astype(float)
d[~tee[crop]] = np.nan
im = ax3.imshow(np.where(d > 0, d, np.nan), cmap="magma", interpolation="nearest",
                vmin=0, vmax=130)
ch = ((es != et) & strip)[crop]
yy, xx = np.nonzero(ch)
ax3.scatter(xx, yy, s=0.6, c="#7fd1ff", marker="s", linewidths=0)
ax3.imshow(np.where(tee[crop], np.nan, 1.0), cmap=ListedColormap(["#000000"]))
ax3.set_title("how much deeper the potential sits\n(blue: cells that changed)", color="w", fontsize=10)
ax3.axis("off")

c = x0 + w // 2
k = np.arange(1, 131)
prof = -dv[base - k, c]
ax4.plot(prof, k, color="#f6c453", lw=1.5, label="centre line")
ax4.plot(np.maximum(83 - k, 0), k, color="#7fd1ff", lw=0.8, ls="--", label="one step per row")
ax4.set_xlabel("steps deeper", color="w")
ax4.set_ylabel("rows above the foot", color="w")
ax4.tick_params(colors="w")
for s in ax4.spines.values():
    s.set_color("#555")
ax4.set_xlim(0, 100)
ax4.set_ylim(0, 130)
ax4.legend(facecolor="#0b0b14", labelcolor="w", fontsize=8, loc="upper right")
ax4.set_title("the staircase", color="w", fontsize=10)

fig.savefig("staircase.png", dpi=110, facecolor="black")
print("saved; changed cells:", int(ch.sum()), "top changed height:", base - (top + yy.min()))
print("profile at 1,10,20,40,60,80,83,90:", [int(prof[i - 1]) for i in (1, 10, 20, 40, 60, 80, 83, 90)])
