import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sys
sys.path.insert(0, '.')
from wander import track

BG = '#14110f'; CHIP = '#e8b04a'; INK = '#efe6d8'; DIM = '#9a8f80'
plt.rcParams.update({'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': DIM, 'ytick.color': DIM,
                     'axes.edgecolor': DIM, 'font.family': 'DejaVu Sans'})
fig = plt.figure(figsize=(13, 9.6), facecolor=BG)
fig.text(0.5, 0.965, "The termites' rigged game", ha='center', fontsize=20, weight='bold')
fig.text(0.5, 0.935, "Resnick's rule: bump into a chip empty-handed, pick it up; bump into one while carrying, put yours down next to it.",
         ha='center', fontsize=10.5, color=DIM)

cm = ListedColormap([BG, CHIP])
snaps = [(1, 'start: 9,830 chips'), (709, '709 ticks'), (6622, '6,622 ticks'), (188278, '188,278 ticks')]
L = 256
for i, (t, lab) in enumerate(snaps):
    ax = fig.add_axes([0.035 + i * 0.24, 0.56, 0.21, 0.33])
    g = np.fromfile(f'snap256/g_{t}.bin', np.uint8).reshape(L, L)
    ax.imshow(g, cmap=cm, interpolation='nearest', vmin=0, vmax=1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(lab, fontsize=11, color=INK)
fig.text(0.035, 0.525, '1  Piles merge until one is left. 1,200 termites, 256 x 256 board that wraps round.',
         fontsize=11, color=INK)

# duel panel
ax = fig.add_axes([0.15, 0.08, 0.28, 0.36], facecolor=BG)
rows = [('1200 vs 1200', 7, 9, 53000), ('1300 vs 1100', 16, 0, 32000), ('1600 vs 800', 8, 0, 14000)]
y = np.arange(len(rows))[::-1]
for yy, (lab, a, b, med) in zip(y, rows):
    n = a + b
    ax.barh(yy, a / n, color=CHIP, height=0.55)
    ax.barh(yy, b / n, left=a / n, color='#6b5a44', height=0.55)
    ax.text(-0.03, yy, lab, ha='right', va='center', fontsize=11)
    ax.text(1.03, yy, f'{a}/{n} to the first\nmedian {med:,} ticks', ha='left', va='center', fontsize=9.5, color=DIM)
ax.set_xlim(0, 1); ax.set_ylim(-0.6, 2.6)
ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(['0', 'half', 'all'])
ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.set_xlabel('share of duels won by the first pile', fontsize=10)
fig.text(0.035, 0.475, '2  Two solid piles, 300 termites. Not a fair game: the bigger one wins every time.',
         fontsize=11, color=INK)

# wander panel
ax = fig.add_axes([0.62, 0.08, 0.34, 0.36], facecolor=BG)
cols = [CHIP, '#d77a4a', '#b9c46a', '#8fb4d9']
for s, c in zip((1, 2, 3, 4), cols):
    T, un, sz, rg = track(s)
    un = un - un[0]
    ax.plot(un[:, 0], un[:, 1], color=c, lw=1.1)
    ax.plot(un[-1, 0], un[-1, 1], 'o', color=c, ms=4)
ax.plot(0, 0, 'o', color=INK, ms=5)
ax.set_aspect('equal')
lim = 110
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_xticks([-100,-50,0,50,100]); ax.set_yticks([-100,-50,0,50,100])
ax.set_xlabel('cells moved by the last pile, 36 million ticks', fontsize=10)
fig.text(0.6, 0.475, '3  The last pile (2,400 chips) drifts like a pollen grain.', fontsize=11, color=INK)
ax.text(-lim + 6, lim - 8, 'spread grows in step with time:\n20 sq cells per 0.2M ticks, 1,488 per 12.8M', fontsize=8.8, color=DIM, va='top')

fig.savefig('termites_rigged.png', dpi=110, facecolor=BG)

# overlap check on all text
fig.canvas.draw(); r = fig.canvas.get_renderer()
texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_text().strip() and t.get_visible()]
boxes = [(t.get_text()[:30], t.get_window_extent(r)) for t in texts]
W, H = fig.canvas.get_width_height()
bad = 0
for i in range(len(boxes)):
    a = boxes[i][1]
    if a.x0 < 0 or a.y0 < 0 or a.x1 > W or a.y1 > H: print('OUT', boxes[i][0]); bad += 1
    for j in range(i + 1, len(boxes)):
        if a.overlaps(boxes[j][1]): print('OVERLAP', boxes[i][0], '|', boxes[j][0]); bad += 1
print(len(boxes), 'texts', bad, 'problems')
