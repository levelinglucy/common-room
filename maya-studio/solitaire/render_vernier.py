"""Picture of the vernier plateau: n = 24, start (5,5,4,3,3,2,1,1), k = 6, r = 3.
Three rings (d5: 6 seats, d6: 7, d7: 8), seat 0 at the top, clockwise, each seat at angle
seat/seats of a turn, so a move turns each ring by one seat (1/6, 1/7, 1/8 of a turn).
"""
import sys
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, '/home/sprite/maya-studio/solitaire')
from bulgarian import move
from vernier import diag_cells

BG = '#14161f'
FG = '#e6e8f5'
BLUE = '#5aa9e6'
GOLD = '#ffc43d'
RED = '#ff5d5d'
DIM = '#3a3f55'

k = 6
p = (5, 5, 4, 3, 3, 2, 1, 1)
traj = [p]
for _ in range(18):
    p = move(p)
    traj.append(p)

show = [0, 3, 6, 9, 12, 15, 17, 18]
radii = {k - 1: 1.0, k: 1.55, k + 1: 2.1}

fig = plt.figure(figsize=(14, 8.6), facecolor=BG)
fig.text(0.5, 0.955, 'The vernier', ha='center', color=FG, fontsize=24, weight='bold')
fig.text(0.5, 0.915, 'Bulgarian solitaire with 24 cards. Each move, three rings of 6, 7 and 8 seats turn one seat each, so they slide against each other.',
         ha='center', color='#b9bdd6', fontsize=11.5)
fig.text(0.5, 0.885, 'The gold card has to rest on two blue cards. The red hole has to sit under two empty seats. The blue block slips one seat against both every lap.',
         ha='center', color='#b9bdd6', fontsize=11.5)

for idx, s in enumerate(show):
    row, col = divmod(idx, 4)
    ax = fig.add_axes([0.03 + col * 0.24, 0.50 - row * 0.38, 0.22, 0.34])
    ax.set_facecolor(BG)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-3.0, 2.3)
    ax.set_aspect('equal')
    ax.axis('off')
    q = traj[s]
    for t, R in radii.items():
        m = t + 1
        ax.add_patch(plt.Circle((0, 0), R, fill=False, ec=DIM, lw=0.8))
        filled = set(diag_cells(q, t))
        for i in range(m):
            ang = math.pi / 2 - 2 * math.pi * i / m
            x, y = R * math.cos(ang), R * math.sin(ang)
            if t == k + 1:
                fc, ec = (GOLD, GOLD) if i in filled else (BG, DIM)
            elif t == k - 1:
                fc, ec = (BLUE, BLUE) if i in filled else (BG, RED)
                if i in filled:
                    fc, ec = ('#7d8399', '#7d8399')
            else:
                fc, ec = (BLUE, BLUE) if i in filled else (BG, DIM)
            lw = 2.2 if (t == k - 1 and i not in filled) else 1.0
            ax.add_patch(plt.Circle((x, y), 0.17, fc=fc, ec=ec, lw=lw))
    label = f'move {s}'
    if s == 0:
        label += ': plateau starts'
    elif s == 17:
        label += ': last plateau move'
    elif s == 18:
        label += ': card and hole gone'
    ax.text(0, -2.45, label, ha='center', va='top', color=FG, fontsize=11)

fig.text(0.5, 0.045, 'Plateau length = the first clock to run out: min(k(k - r), (k + 2)(r - 1) + 2). Here k = 6, r = 3, so 18 and 18 tie, the same as the all-ones start.',
         ha='center', color=GOLD, fontsize=11)
fig.text(0.5, 0.018, 'Checked for every such plateau with 7 to 46 cards: rigid turning throughout, length = shorter clock, 0 exceptions. Probably known maths.',
         ha='center', color='#8c90a8', fontsize=9.5)

fig.savefig('/home/sprite/maya-studio/solitaire/vernier_rings.png', dpi=110, facecolor=BG)

# programmatic check: texts inside the figure and not overlapping
fig.canvas.draw()
rend = fig.canvas.get_renderer()
boxes = []
for t_ in fig.findobj(matplotlib.text.Text):
    if not t_.get_text().strip() or not t_.get_visible():
        continue
    boxes.append((t_.get_text()[:30], t_.get_window_extent(rend)))
W_, H_ = fig.canvas.get_width_height()
prob = 0
for name, bb in boxes:
    if bb.x0 < 0 or bb.y0 < 0 or bb.x1 > W_ or bb.y1 > H_:
        print('OUT', name)
        prob += 1
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        a, b = boxes[i][1], boxes[j][1]
        if a.overlaps(b) and a.width > 0 and b.width > 0:
            print('OVERLAP', boxes[i][0], '|', boxes[j][0])
            prob += 1
print(len(boxes), 'texts,', prob, 'problems')
# state check: plateau states have 5 on d5 (one hole), 3 on d6, 1 on d7; move 18 has 6, 3, 0
for s in show:
    print(s, traj[s], [len(diag_cells(traj[s], t)) for t in (k - 1, k, k + 1)])
