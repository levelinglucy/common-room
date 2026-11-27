import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

N = 26
import sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'one_beat_off'
rings = json.load(open(f'/home/sprite/maya-studio/puzzle/{SRC}.json'))

BG = '#14161c'
SEAT = '#3a3f4b'
BEAT = '#f2c14e'
INK = '#d8d8d8'
DPI = 150
W, H = 12.0, 6.6

fig = plt.figure(figsize=(W, H), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect('equal')
ax.axis('off')

R = 0.92
centres = []
for i in range(len(rings)):
    row, col = divmod(i, 5)
    in_row = min(5, len(rings) - row * 5)
    cx = W / 2 + (col - (in_row - 1) / 2) * 2.33
    cy = 4.55 - row * 2.35
    centres.append((cx, cy))

seat_xy = []
for (cx, cy), r in zip(centres, rings):
    ax.add_patch(plt.Circle((cx, cy), R, fill=False, ec=SEAT, lw=1.0))
    # notch at seat 1 (top)
    ax.plot([cx, cx], [cy + R + 0.10, cy + R + 0.24], color=INK, lw=1.6,
            solid_capstyle='round')
    beats = set(r['beats'])
    pts = []
    for s in range(N):
        a = math.pi / 2 - 2 * math.pi * s / N  # clockwise from top
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        pts.append((x, y, s in beats))
        if s in beats:
            ax.add_patch(plt.Circle((x, y), 0.085, color=BEAT, zorder=3))
        else:
            ax.add_patch(plt.Circle((x, y), 0.03, color=SEAT, zorder=3))
    seat_xy.append(pts)

TITLE = 'One beat off' + (' (hard)' if SRC.endswith('hard') else '')
ax.text(W / 2, H - 0.35, TITLE, ha='center', va='center',
        color=INK, fontsize=17)
ax.text(W / 2, 0.55,
        'Each ring has 26 seats. Seat 1 is under the notch; count clockwise.\n'
        'The drummers on a ring sit as evenly as they can, except one who has slipped one seat.\n'
        'The seat that drummer sits on now is a letter: 1 = A, 26 = Z. Read the rings like a page.'
        + ('\nHard: every gap here is already the right size. The slip only spoils how the long gaps are spread.' if SRC.endswith('hard') else ''),
        ha='center', va='center', color=INK, fontsize=10.5, linespacing=1.6)

out = f'/home/sprite/maya-studio/puzzle/{SRC}.png'
fig.savefig(out, dpi=DPI, facecolor=BG)

# pixel coordinates of every seat, for the checker
pix = []
for pts in seat_xy:
    pix.append([[x / W * W * DPI, (H - y) / H * H * DPI, b] for x, y, b in pts])
json.dump(pix, open(f'/home/sprite/maya-studio/puzzle/seat_pixels_{SRC}.json', 'w'))
print('saved', out)

# layout check: caption box vs lowest dot
fig.canvas.draw()
rend = fig.canvas.get_renderer()
for t in ax.texts:
    bb = t.get_window_extent(rend)
    print('text', repr(t.get_text()[:20]), 'y px from bottom', round(bb.y0), round(bb.y1), 'x', round(bb.x0), round(bb.x1))
low = min(cy for cx, cy in centres) - R - 0.085
high = max(cy for cx, cy in centres) + R + 0.24
print('lowest ring px', round(low * DPI), 'highest notch px', round(high * DPI))
