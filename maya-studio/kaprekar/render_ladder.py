import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ladder import orbit

fig, axes = plt.subplots(2, 2, figsize=(12, 7.6), gridspec_kw={'height_ratios': [1.25, 1]})
fig.patch.set_facecolor('#0f1117')
cases = [(7, 640, 'base 640  (m = 7, odd): falls home to the fixed point'),
         (8, 1280, 'base 1280  (m = 8, even): the ladder lands on 0 and loops')]
for col, (m, B, title) in enumerate(cases):
    tail, cyc = orbit((B // 5, 0), B)
    path = tail + cyc + ([cyc[0]] if len(cyc) > 1 else [])
    X = np.array([p[0] for p in path]) / B
    Y = np.array([p[1] for p in path]) / B
    k = np.arange(len(path))
    ax = axes[0, col]
    ax.set_facecolor('#0f1117')
    for r, c in [(1/5, '#f2c14e'), (3/5, '#f2c14e'), (2/5, '#555b6e'), (4/5, '#555b6e')]:
        ax.axhline(r, color=c, lw=0.8, ls='--', alpha=0.7)
    ax.plot(k, X, '-o', color='#7fd1ae', ms=4, lw=1.4, label='first gap')
    ax.plot(k, Y, '-o', color='#e07a9a', ms=4, lw=1.4, label='second gap')
    ax.set_ylim(-0.04, 1.14)
    ax.set_yticks([0, 1/5, 2/5, 3/5, 4/5, 1]); ax.set_yticklabels(['0', 'B/5', '2B/5', '3B/5', '4B/5', 'B'])
    ax.set_title(title, color='white', fontsize=11)
    if len(cyc) > 1:
        ax.axvspan(len(tail), len(path) - 1, color='#e07a9a', alpha=0.08)
        ax.text(len(path) - 1, 0.02, 'back to the start', color='#e07a9a', ha='right', fontsize=9)
    else:
        ax.text(len(path) - 1, 0.66, 'fixed point', color='#f2c14e', ha='right', fontsize=9)
    ax.legend(loc='upper center', ncol=2, fontsize=8, facecolor='#0f1117', labelcolor='white', edgecolor='#333')
    # bottom: log2 distance from the nearest rail (B/5 or 3B/5), for each gap
    ax2 = axes[1, col]
    ax2.set_facecolor('#0f1117')
    P = np.array(path)
    rails = np.array([B // 5, 3 * B // 5])
    for j, c in [(0, '#7fd1ae'), (1, '#e07a9a')]:
        dist = np.min(np.abs(P[:, j:j+1] - rails[None, :]), axis=1)
        lv = np.where(dist > 0, np.log2(np.maximum(dist, 1)), -1)
        ax2.plot(k, lv, '-o', color=c, ms=4, lw=1.4)
    ax2.axhline(m, color='#f2c14e', lw=0.8, ls=':')
    ax2.text(0.2, m + 0.3, f'2^{m} = B/5: a gap this far off the rail sits on 0, 2B/5 or 4B/5', color='#f2c14e', fontsize=8)
    ax2.set_ylim(-1.6, m + 1.6)
    ax2.set_yticks([-1] + list(range(0, m + 1)))
    ax2.set_yticklabels(['on rail'] + [str(2 ** i) for i in range(0, m + 1)])
    ax2.set_xlabel('step', color='#bbb')
    ax2.set_ylabel('distance from B/5 or 3B/5', color='#bbb', fontsize=9)
    for a in (ax, ax2):
        a.tick_params(colors='#bbb', labelsize=8)
        for s in a.spines.values():
            s.set_color('#333')
fig.suptitle('Kaprekar, 4 digits: why only odd powers of 2 give one single answer', color='white', fontsize=13)
fig.text(0.5, 0.012, 'Both runs start at the edge state (B/5, 0). The small error doubles every step while the gaps hop between the rails B/5 and 3B/5.',
         color='#999', ha='center', fontsize=9)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('kaprekar_ladder.png', dpi=130, facecolor=fig.get_facecolor())
print('saved')
