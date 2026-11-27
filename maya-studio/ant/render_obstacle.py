# One dot in the road: where Langton's ant goes when a single black cell sits on its highway.
# Data: single_T30k.txt (obstacle2.c), checked by verify_obstacle.py and rewind.c.
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)
T1 = 30000
BG = '#0d1020'
COL = {'heal': '#7ee081', 'side': '#2fb7c4', 'right': '#ffb347', 'left': '#8fa8ff', 'home': '#ff5d73'}
CAT = {}
for p in (34, 62, 63, 76): CAT[p] = 'heal'
for p in (5, 6, 15, 20, 77): CAT[p] = 'side'
for p in (0, 1, 7, 16, 78, 81, 87): CAT[p] = 'right'
for p in (2, 64, 94, 95, 96): CAT[p] = 'left'
CAT[17] = 'home'


def run(T, dots=(), keep_ground_at=None, every=8):
    g = set(dots)
    x = y = d = 0
    path = []
    first = {}
    ground = None
    for t in range(T + 1):
        if t % every == 0:
            path.append((x, y))
        if (x, y) not in first:
            first[(x, y)] = t
        if keep_ground_at is not None and t == keep_ground_at:
            ground = set(g)
        if (x, y) in g:
            d = (d + 3) & 3; g.discard((x, y))
        else:
            d = (d + 1) & 3; g.add((x, y))
        x += DX[d]; y += DY[d]
    return np.array(path), first, ground


T = 150000
clean, first, ground = run(T, keep_ground_at=T1)
cells = sorted((t, c) for c, t in first.items() if T1 <= t < T1 + 104)
assert len(cells) == 22
ph = {t - T1: c for t, c in cells}
assert sorted(ph) == sorted(CAT)
ant_at_T1 = tuple(clean[T1 // 8]) if T1 % 8 == 0 else None

examples = [(62, 'heal', 'back on the same road, 20 steps late'),
            (6, 'side', 'same direction, moved over to its right'),
            (0, 'right', 'turns right'),
            (2, 'left', 'turns left'),
            (17, 'home', 'turns round and goes home')]
paths = {p: run(T, [ph[p]])[0] for p, _, _ in examples}

fig = plt.figure(figsize=(13, 12), facecolor=BG)
fig.text(0.5, 0.962, 'One dot in the road', ha='center', color='white', fontsize=24, weight='bold')
fig.text(0.5, 0.933, "Langton's ant has built its highway. Put one black dot on a cell it is about to step on. What happens?",
         ha='center', color='#c8cbe0', fontsize=11.5)

# --- panel A: the road's 22 kinds of cell, coloured by what a dot there does ---
axA = fig.add_axes([0.04, 0.40, 0.42, 0.48], facecolor=BG)
cx, cy = np.mean([c for _, c in cells], axis=0)
R = 13
for (x, y) in ground:
    if abs(x - cx) <= R and abs(y - cy) <= R:
        axA.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='#5a6078', lw=0))
for t, (x, y) in cells:
    c = COL[CAT[t - T1]]
    axA.add_patch(plt.Rectangle((x - 0.45, y - 0.45), 0.9, 0.9, fill=False, ec=c, lw=2.2))
    axA.plot(x, y, 'o', color=c, ms=7)
ax_, ay_ = ant_at_T1
axA.plot(ax_, ay_, marker='*', color='white', ms=16, mec=BG)
axA.annotate('', xy=(ax_ - 7, ay_ + 7), xytext=(ax_ - 1, ay_ + 1),
             arrowprops=dict(arrowstyle='->', color='white', lw=1.5))
axA.set_xlim(cx - R, cx + R); axA.set_ylim(cy + R, cy - R)
axA.set_aspect('equal'); axA.set_xticks([]); axA.set_yticks([])
for s in axA.spines.values(): s.set_color('#30344a')
axA.set_title('Every cell the road will step on, one period of it', color='white', fontsize=13.5, pad=8)
fig.text(0.25, 0.375, 'Grey: the road built so far. Star: the ant, heading down-left.\nThe road repeats every 104 steps, so these 22 cells are all the cases there are.',
         ha='center', color='#c8cbe0', fontsize=10, va='top')

# --- panel B: where the ant goes afterwards ---
axB = fig.add_axes([0.52, 0.40, 0.44, 0.48], facecolor='#11152a')
L = 1500
axB.plot(clean[:, 0], clean[:, 1], color='#ffffff', lw=1, alpha=0.35, ls='--')
for p, cat, _ in examples:
    P = paths[p]
    k = T1 // 8 - 5
    axB.plot(P[k:, 0], P[k:, 1], color=COL[cat], lw=2.2 if cat != 'home' else 2.6)
axB.plot(0, 0, 'o', color='white', ms=6)
axB.text(30, -40, 'start', color='white', fontsize=10)
axB.plot(*ph[0], marker='o', color='white', ms=5)
axB.text(ph[0][0] + 50, ph[0][1] + 10, 'the dot', color='white', fontsize=10)
axB.set_xlim(-L, L * 0.6); axB.set_ylim(L, -L * 0.9)
axB.set_aspect('equal'); axB.set_xticks([]); axB.set_yticks([])
for s in axB.spines.values(): s.set_color('#30344a')
axB.set_title('Where it goes next (first 150,000 steps)', color='white', fontsize=13.5, pad=8)
axB.text(-L + 40, -L * 0.9 + 60, 'dashed: the road with no dot', color='#c8cbe0', fontsize=9.5, va='top')

# --- legend / tally ---
tally = [('heal', 4, 'Heals: back on exactly the same road, 20 to 132 steps late'),
         ('side', 5, 'Same direction, road moved over to its right'),
         ('right', 7, 'Turns right'),
         ('left', 5, 'Turns left'),
         ('home', 1, 'Turns round, walks home beside its old road, then turns right')]
y = 0.27
fig.text(0.06, y + 0.035, 'What one dot does, all 22 cases', color='white', fontsize=14, weight='bold')
for cat, n, label in tally:
    fig.patches.append(matplotlib.patches.Circle((0.075, y + 0.005), 0.008, color=COL[cat], transform=fig.transFigure))
    fig.text(0.095, y, f'{n}', color=COL[cat], fontsize=13, weight='bold', va='center')
    fig.text(0.125, y, label, color='#e6e8f5', fontsize=11.5, va='center')
    y -= 0.04
fig.text(0.06, y - 0.01, 'No dot is ever shrugged off: all 22 break the road, even the 4 that heal.', color='#ffb347', fontsize=11.5)

notes = ('Going home takes as long as getting there: 20,042 steps out,\n'
         'then 51,000 steps of mess at the dot, then 19,955 steps back.\n'
         'The longer the road, the longer the walk home.\n\n'
         'Two dots can do more: 11 of 1,199 pairs send it straight back,\n'
         'and 2 pairs put it on the same road 4 steps ahead of itself.')
fig.text(0.56, 0.335, notes, color='#c8cbe0', fontsize=11, va='top', linespacing=1.5)
fig.text(0.5, 0.025, 'Dot placed 20,000 steps into the highway. Same results 50,000 and 110,000 steps in, except the walk home, which grows with the road.',
         ha='center', color='#8c90a8', fontsize=9.5)

fig.savefig('one_dot.png', dpi=110, facecolor=BG)

# programmatic check: texts inside the figure and not overlapping each other
fig.canvas.draw()
r = fig.canvas.get_renderer()
boxes = []
for t_ in fig.findobj(matplotlib.text.Text):
    if not t_.get_text().strip() or not t_.get_visible():
        continue
    if t_.axes is not None and t_.axes.get_xticks().size == 0 and t_ in t_.axes.xaxis.get_ticklabels() + t_.axes.yaxis.get_ticklabels():
        continue
    bb = t_.get_window_extent(r)
    if bb.width == 0:
        continue
    boxes.append((t_.get_text()[:30], bb))
W_, H_ = fig.canvas.get_width_height()
prob = 0
for name, bb in boxes:
    if bb.x0 < 0 or bb.y0 < 0 or bb.x1 > W_ or bb.y1 > H_:
        print('OUT', name); prob += 1
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        a, b = boxes[i][1], boxes[j][1]
        if a.overlaps(b):
            print('OVERLAP', boxes[i][0], '|', boxes[j][0]); prob += 1
print(len(boxes), 'texts,', prob, 'problems')
# where the example paths end up inside panel B
for p, cat, _ in examples:
    P = paths[p]
    inside = np.mean((P[:, 0] > -L) & (P[:, 0] < L * 0.6) & (P[:, 1] < L) & (P[:, 1] > -L * 0.9))
    print(p, cat, 'end', tuple(P[-1]), 'share of points inside panel B: %.2f' % inside)
print('ant at T1', ant_at_T1, 'dot cells centre', (cx, cy))
