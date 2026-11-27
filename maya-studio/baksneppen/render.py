import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import analyse as A, os

ps = ['0', '0.000001', '0.00001', '0.00003', '0.0001', '0.0003', '0.001', '0.003', '0.01', '0.03', '0.1', '0.2', '0.3', '0.5', '0.7', '1']

# measured, both sizes, and an N -> infinity estimate assuming the bias falls like N^-1/2
meas = {}
for s in ps:
    m8 = A.fc_of('runs/N8000_p' + s)[0]
    m2 = A.fc_of('runs/N2000_p' + s)[0] if os.path.exists('runs/N2000_p%s_hist.txt' % s) else np.nan
    meas[s] = (m2, m8, m8 - (m2 - m8) if np.isfinite(m2) else np.nan)

# branching prediction from single-seed avalanches
pred = {'1': 1 / 3}
for s in ps[1:-1]:
    fn = 'runs/seed1_p%s.txt' % s
    if not os.path.exists(fn): continue
    D = np.loadtxt(fn, ndmin=2)
    f, S = D[:, 0], D[:, 1]
    g = np.log(2 * float(s) * f * S)
    k = int(np.argmax(g > 0))
    if k > 0 and g[k] > 0:
        t = -g[k - 1] / (g[k] - g[k - 1]); pred[s] = f[k - 1] + t * (f[k] - f[k - 1])

with open('results_table.txt', 'w') as o:
    o.write('p          fc N=2000  fc N=8000  fc N->inf est   branching prediction  pred - est\n')
    for s in ps:
        m2, m8, mi = meas[s]; pr = pred.get(s, np.nan)
        o.write('%-10s %.4f     %.4f     %.4f          %.4f                %+.4f\n' % (s, m2, m8, mi, pr, pr - mi))
print(open('results_table.txt').read())

# simple prediction from the plain ring's run lengths
R0 = np.load('runs/ring_s.npy'); ok = np.isfinite(R0[:, 1]) & (R0[:, 2] > 1000)
fr, Sr = R0[ok, 0], R0[ok, 1]
pgrid = np.logspace(-6, -0.6, 80)
simple = []
for p in pgrid:
    g = np.log(2 * p * fr * Sr); k = int(np.argmax(g > 0))
    simple.append(fr[k - 1] + (-g[k - 1] / (g[k] - g[k - 1])) * (fr[k] - fr[k - 1]) if k > 0 and g[k] > 0 else np.nan)

# space-time trace of where the weakest species is
def trace(N, p, steps, warm, seed):
    rng = np.random.default_rng(seed)
    f = rng.random(N); pos = np.empty(steps, int)
    for t in range(warm + steps):
        i = int(np.argmin(f))
        if t >= warm: pos[t - warm] = i
        a, c = (i - 1) % N, (i + 1) % N
        if p > 0:
            if rng.random() < p: a = int(rng.integers(N))
            if rng.random() < p: c = int(rng.integers(N))
        f[i] = rng.random(); f[a] = rng.random(); f[c] = rng.random()
    return pos

if not os.path.exists('runs/trace.npz'):
    t0 = trace(600, 0.0, 60000, 400000, 1)
    t1 = trace(600, 0.001, 60000, 400000, 2)
    t2 = trace(600, 0.03, 60000, 400000, 3)
    np.savez('runs/trace.npz', t0=t0, t1=t1, t2=t2)
T = np.load('runs/trace.npz')

plt.rcParams.update({'font.size': 10})
fig = plt.figure(figsize=(13, 9.2), facecolor='#faf7f0', dpi=130)
gs = fig.add_gridspec(2, 3, height_ratios=[1.15, 1], hspace=0.38, wspace=0.28)
ax = fig.add_subplot(gs[0, :2])
ax.set_facecolor('#faf7f0')
xp = [float(s) if s != '0' else 3e-7 for s in ps]
ax.plot(pgrid, simple, '--', color='#9a8f7a', lw=1.3, label='prediction from the plain ring alone')
kp = [s for s in ps if s in pred]
ax.plot([float(s) for s in kp], [pred[s] for s in kp], '-', color='#2b6f77', lw=2.2, label='branching prediction (no fitted numbers)')
ax.plot(xp, [meas[s][1] for s in ps], 'o', mfc='none', mec='#b5482f', ms=7, mew=1.6, label='measured, 8,000 species')
ax.plot(xp[1:], [meas[s][2] for s in ps[1:]], 'o', color='#b5482f', ms=4, label='measured, estimate for an endless ring')
ax.axhline(1 / 3, color='#cccccc', lw=0.8, zorder=0); ax.axhline(0.66702, color='#cccccc', lw=0.8, zorder=0)
ax.text(1.5e-3, 0.318, 'every neighbour random: 1/3', color='#888888', fontsize=9)
ax.text(1.3e-6, 0.672, 'plain ring: 0.667', color='#888888', fontsize=9)
ax.set_xscale('log'); ax.set_xlim(2e-7, 1.6); ax.set_ylim(0.31, 0.70)
ax.set_xticks([3e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1])
ax.set_xticklabels(['0', '1 in a\nmillion', '1 in\n100k', '1 in\n10k', '1 in\n1000', '1 in\n100', '1 in\n10', 'all'])
ax.set_xlabel('chance that a neighbour dragged along is a random species anywhere')
ax.set_ylabel('fitness threshold the ecosystem settles to')
ax.set_title('One far neighbour in a thousand drops the threshold from 0.667 to 0.629', loc='left', fontsize=12)
ax.legend(loc='lower left', frameon=False, fontsize=9)

ax2 = fig.add_subplot(gs[0, 2]); ax2.set_facecolor('#faf7f0')
cols = {'0': '#3b3b3b', '0.001': '#b5482f', '0.03': '#d08b2c', '0.3': '#2b6f77', '1': '#7a5aa6'}
names = {'0': 'ring', '0.001': '1 in 1000', '0.03': '3 in 100', '0.3': '3 in 10', '1': 'all random'}
for s, c in cols.items():
    h = np.loadtxt('runs/N8000_p%s_hist.txt' % s)[:, 1]; h = h / h[900:995].mean()
    x = (np.arange(1000) + 0.5) / 1000
    ax2.plot(x, h, color=c, lw=1.4, label=names[s])
ax2.set_xlabel('fitness'); ax2.set_ylabel('share of species (plateau = 1)')
ax2.set_ylim(0, 1.25); ax2.set_xlim(0, 1)
ax2.set_title('Where the species sit', loc='left', fontsize=11)
ax2.legend(frameon=False, fontsize=8.5, loc='upper left')

for j, (key, lab) in enumerate([('t0', 'plain ring'), ('t1', '1 far neighbour in 1000'), ('t2', '3 in 100')]):
    a = fig.add_subplot(gs[1, j]); a.set_facecolor('#faf7f0')
    pos = T[key]
    a.plot(pos, np.arange(len(pos)) / 1000, ',', color='#1f1f1f', alpha=0.5, rasterized=True)
    a.set_xlim(0, 600); a.set_ylim(60, 0)
    a.set_xlabel('place on the ring (600 species)')
    if j == 0: a.set_ylabel('time (thousands of steps)')
    a.set_title('Where the weakest one is: ' + lab, loc='left', fontsize=10)
fig.text(0.01, 0.008, 'Bak-Sneppen evolution: every step the least fit species and two neighbours get new random fitnesses.\nBranching rule: per step, an avalanche sends on average 2pf new weak species far away; the threshold is where one weak species\'s avalanche makes exactly one more.', fontsize=8, color='#555555')
fig.savefig('far_neighbour.png', dpi=130, facecolor=fig.get_facecolor())
print('saved')
# overlap check of all text items (titles, labels, ticks, legends, annotations)
fig.canvas.draw()
r = fig.canvas.get_renderer()
items = []
for a in fig.axes:
    for t in [a.title, a.xaxis.label, a.yaxis.label] + a.texts + a.get_xticklabels() + a.get_yticklabels():
        if t.get_text() and t.get_visible():
            items.append((t.get_text()[:30], t.get_window_extent(r)))
    lg = a.get_legend()
    if lg: items.append(('legend', lg.get_window_extent(r)))
for t in fig.texts: items.append((t.get_text()[:30], t.get_window_extent(r)))
bad = 0
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        if items[i][1].overlaps(items[j][1]):
            bad += 1; print("OVERLAP", items[i][0], items[i][1].bounds, "|", items[j][0], items[j][1].bounds)
W, H = fig.bbox.width, fig.bbox.height
out = [n for n, b in items if b.x0 < 0 or b.y0 < 0 or b.x1 > W or b.y1 > H]
print(len(items), 'texts,', bad, 'overlaps, outside figure:', out)
