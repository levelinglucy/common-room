import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, figsize=(13, 5.6), facecolor='#101418')
cols = {1000000: '#7fb3d5', 10000000: '#76d7c4', 100000000: '#f7dc6f', 1000000000: '#f1948a'}
lab = {1000000: 'first million', 10000000: '10 million', 100000000: '100 million', 1000000000: '1 billion'}
for a in ax:
    a.set_facecolor('#101418'); a.tick_params(colors='#cccccc')
    for s in a.spines.values(): s.set_color('#555555')

for N, c in cols.items():
    d = np.loadtxt(f'zipf_{N}.txt')
    m = (d[:, 2] > 20) & (d[:, 1] < 0.8 * N / 2)
    flat = np.median(d[m & (d[:, 2] > 100), 3])
    ax[0].plot(d[m, 2], d[m, 3], color=c, lw=1.6, label=f'{lab[N]} terms: {flat:.3f} (x ln N = {flat*np.log(N):.2f})')
ax[0].set_xscale('log'); ax[0].set_ylim(0.0, 0.075)
ax[0].set_xlabel('value v', color='#dddddd'); ax[0].set_ylabel('v x (how often v turns up)', color='#dddddd')
ax[0].set_title('Every value is used in proportion to 1/v\n(flat line = Zipf; height shrinks like 0.82 / ln N)', color='#eeeeee', fontsize=11)
ax[0].legend(facecolor='#101418', edgecolor='#555555', labelcolor='#dddddd', fontsize=9, loc='lower left')

a = np.fromfile('a_1e8.bin', dtype=np.uint32).astype(np.float64)
zi = np.flatnonzero(a == 0)
rng = np.random.default_rng(3)
pick = rng.choice(len(zi) - 1, 60, replace=False)
for p in pick:
    seg = a[zi[p] + 1: zi[p + 1]]
    ax[1].plot(range(1, len(seg) + 1), seg, color='#f7dc6f', alpha=0.25, lw=0.9, marker='o', ms=2)
means = []
for k in range(1, 12):
    idx = zi[:-1] + k; ok = idx < zi[1:]
    means.append(np.exp(np.log(a[idx[ok]]).mean()))
ax[1].plot(range(1, 12), means, color='#f1948a', lw=2.5, label='typical climb (geometric mean)')
ax[1].axhline(1.05e8, color='#888888', ls=':', lw=1)
ax[1].text(1.1, 1.3e8, 'terms written so far (~100 million)', color='#aaaaaa', fontsize=9)
ax[1].set_yscale('log'); ax[1].set_ylim(1, 1e9)
ax[1].set_xlabel('steps after a zero', color='#dddddd'); ax[1].set_ylabel('value', color='#dddddd')
ax[1].set_title('Between zeros, each term climbs about x13 to a rarer number\nuntil it reaches one never seen, and the next term is 0', color='#eeeeee', fontsize=11)
ax[1].legend(facecolor='#101418', edgecolor='#555555', labelcolor='#dddddd', fontsize=9, loc='lower right')
fig.suptitle("Van Eck's sequence: each term says how long ago the last one was seen", color='white', fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig('zipf_ladder.png', dpi=110, facecolor=fig.get_facecolor())
