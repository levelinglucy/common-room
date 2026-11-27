import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyse import fc_of

Ks = [2, 3, 4, 5, 6]
def ext(K, mo):
    a = fc_of('kruns/N8000_K%d_m%d' % (K, mo))[0]
    try:
        b = fc_of('kruns/N32000_K%d_m%d' % (K, mo))[0]
        return b - (a - b)  # N^-1/2 extrapolation (recovers 1/(K+1) for fresh to 1e-4)
    except OSError:
        return a
vals = {mo: [ext(K, mo) for K in Ks] for mo in range(3)}
hit = {1: [0.10575, 0.05099, 0.03067, 0.02076], 2: [0.50049, 0.15602, 0.08336, 0.05247]}

fig, ax = plt.subplots(1, 2, figsize=(13, 5.2), dpi=130)
col = {0: '#4a7fb5', 1: '#e08a2c', 2: '#b23a48'}
lab = {0: 'fresh partners each time', 1: 'fixed, one-way', 2: 'fixed, two-way'}
k = np.linspace(2, 6, 100)
ax[0].plot(k, 1 / (k + 1), color='#999', lw=1, ls='--', label='1/(K+1)')
ax[0].plot(k, 1 / k, color='#999', lw=1, ls=':', label='1/K')
for mo in range(3):
    ax[0].plot(Ks, vals[mo], 'o-', color=col[mo], label=lab[mo])
ax[0].set_xlabel('K, partners dragged along with the weakest')
ax[0].set_ylabel('threshold (fitness below which no species lasts)')
ax[0].set_xticks(Ks)
ax[0].set_ylim(0.1, 0.72)
ax[0].annotate('two-way, K = 2:\njust a ring again (0.665)', xy=(2, vals[2][0]), xytext=(2.6, 0.62), fontsize=9,
               arrowprops=dict(arrowstyle='->', color='#555'))
ax[0].legend(loc='center right', fontsize=9, frameon=False)
ax[0].set_title('Same number of partners, three kinds of link', fontsize=11)

x = np.arange(4); w = 0.38
ax[1].bar(x - w/2, np.array(hit[1]) * 100, w, color=col[1], label=lab[1])
ax[1].bar(x + w/2, np.array(hit[2]) * 100, w, color=col[2], label=lab[2])
ax[1].set_xticks(x); ax[1].set_xticklabels(['K = %d' % K for K in [2, 3, 4, 5]])
ax[1].set_ylabel('% of drags that land on a species already weak')
ax[1].set_title('Wasted drags at the threshold (fresh: none)', fontsize=11)
ax[1].legend(loc='upper right', fontsize=9, frameon=False)
for i in range(4):
    for s, mo in ((-1, 1), (1, 2)):
        v = hit[mo][i] * 100
        ax[1].text(i + s * w/2, v + 0.8, '%.1f' % v, ha='center', fontsize=8)
ax[1].set_ylim(0, 58)
fig.tight_layout()
fig.canvas.draw()
r = fig.canvas.get_renderer()
boxes = [t.get_window_extent(r) for a in ax for t in a.texts + [a.title, a.xaxis.label, a.yaxis.label] + a.get_xticklabels()]
boxes += [a.get_legend().get_window_extent(r) for a in ax]
ov = sum(1 for i in range(len(boxes)) for j in range(i+1, len(boxes)) if boxes[i].overlaps(boxes[j]))
print('texts', len(boxes), 'overlaps', ov)
fig.savefig('two_way.png')
for mo in range(3): print(lab[mo], ['%.4f' % v for v in vals[mo]])
# legend vs data check
bad=0
for a in ax:
    lb=a.get_legend().get_window_extent(r)
    for ln in a.get_lines():
        for xy in a.transData.transform(np.c_[ln.get_xdata(), ln.get_ydata()]):
            if lb.contains(*xy): bad+=1
    for p in a.patches:
        if lb.overlaps(p.get_window_extent(r)): bad+=1
print('legend-data hits', bad)
