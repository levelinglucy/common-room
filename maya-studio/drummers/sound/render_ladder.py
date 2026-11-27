"""Score picture for ladder_piece: one row per bar, 16 pulse columns, a dot per
drummer coloured by drummer; the two short gaps marked. Sections by reach j."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm

sc = json.load(open('ladder_piece_score.json'))
N, K = sc['N'], sc['K']
rows = [b for b in sc['bars'] if b['pos']]
# keep one 'settled' bar per section to keep the picture compact
compact, seen = [], set()
for b in rows:
    if b['label'] == 'settled':
        if b['j'] in seen:
            continue
        seen.add(b['j'])
    compact.append(b)

fig, ax = plt.subplots(figsize=(8.2, 0.42 * len(compact) + 2.2), dpi=150)
fig.patch.set_facecolor('#111317'); ax.set_facecolor('#111317')
cols = [cm.viridis(0.08 + 0.84 * d / (K - 1)) for d in range(K)]
y = 0; ylabels = []
prev_j = None
for b in compact:
    if b['j'] != prev_j and prev_j is not None:
        y += 0.7
    prev_j = b['j']
    pos = b['pos']
    for s in range(N):
        ax.plot(s, -y, marker='o', ms=3, color='#3a3f48', zorder=1)
    # short gaps: two drummers one pulse apart -> bar between them
    order = sorted(range(K), key=lambda d: pos[d])
    for a, c in zip(order, order[1:] + order[:1]):
        if (pos[c] - pos[a]) % N == 1:
            x0, x1 = pos[a], pos[a] + 1
            ax.plot([x0, x1] if x1 < N else [x0, x0 + 0.5], [-y, -y], color='#f2c14e', lw=5, alpha=0.55, zorder=2,
                    solid_capstyle='round')
    for d, s in enumerate(pos):
        big = (d == b['mover'])
        ax.plot(s, -y, marker='o', ms=13 if big else 10, color=cols[d], zorder=3,
                markeredgecolor='white' if big else 'none', markeredgewidth=1.5)
    lab = f"hears {b['j']}" + ('  settled' if b['label'] == 'settled' else '')
    if b['label'] == 'settled' and b['j'] == 4:
        lab = 'hears 4  settled: E(9,16)'
    ylabels.append((-y, lab, b['label'] == 'settled'))
    y += 1
for yy, lab, st in ylabels:
    ax.text(N - 0.1, yy, lab, color='#f2c14e' if st else '#8a919c', va='center', ha='left', fontsize=8.5,
            fontweight='bold' if st else 'normal')
ax.set_xlim(-0.8, N + 4.2); ax.set_ylim(-y + 0.3, 1.3)
ax.set_xticks(range(N)); ax.set_xticklabels([str(i + 1) for i in range(N)], color='#8a919c', fontsize=7)
ax.tick_params(length=0); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.xaxis.set_ticks_position('top')
fig.suptitle('Nine drummers, sixteen pulses: one bar per move', color='white', fontsize=12, y=0.995)
fig.text(0.5, 0.012, 'Gold = two beats side by side. They walk apart only as far as the drummers hear:\n'
         'hear 1 each side, nothing between them; hear 2, one gap; hear 3, two; hear 4, as far as they go.',
         color='#c9ced6', ha='center', va='bottom', fontsize=8.5)
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.03, right=0.99)
plt.savefig('ladder_piece.png', facecolor=fig.get_facecolor())
print('rows', len(compact))
