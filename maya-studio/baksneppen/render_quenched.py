import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import analyse

ps = [0.001, 0.003, 0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 0.7, 1]
pstr = ['0.001', '0.003', '0.01', '0.03', '0.1', '0.2', '0.3', '0.5', '0.7', '1']
ann = {}
for line in open('results_table.txt').read().splitlines()[1:]:
    t = line.split(); ann[float(t[0])] = (float(t[2]), float(t[4]))
q2 = [np.mean([analyse.fc_of(f'qruns/N2000_p{p}_s{s}')[0] for s in (7, 21, 22)]) for p in pstr]
q8 = [analyse.fc_of(f'qruns/N8000_p{p}_s7')[0] for p in pstr]
# tree-of-rings threshold brackets (survival to 1e6 / 3e6 steps), from tr_runs and tree_runs
tr = {0.01: (0.635, 0.640), 0.03: (0.605, 0.610), 0.1: (0.545, 0.550), 0.3: (0.470, 0.475), 1: (0.401, 0.402)}

fig = plt.figure(figsize=(12.5, 5.6), dpi=130, facecolor='white')
ax = fig.add_axes([0.06, 0.2, 0.52, 0.7])
ax.semilogx(ps, [ann[p][0] for p in ps], 'o', color='#3a7bd5', label='annealed: a fresh random far species each time (N 8000)')
ax.semilogx(ps, [ann[p][1] for p in ps], '-', color='#3a7bd5', lw=1, alpha=0.6, label='annealed: branching rule, no fitted numbers')
ax.semilogx(ps, q2, 's', mfc='none', color='#d5573a', label='quenched: the same far species every time (N 2000, 3 wirings)')
ax.semilogx(ps, q8, 's', color='#d5573a', label='quenched, N 8000')
for p, (lo, hi) in tr.items():
    ax.plot([p, p], [lo, hi], color='black', lw=4, solid_capstyle='butt')
ax.plot([], [], color='black', lw=4, label='quenched: threshold of one seed on an endless tree of rings')
ax.axhline(1/3, color='#999999', ls=':', lw=1)
ax.text(0.00075, 1/3 + 0.004, '1/3', color='#777777', fontsize=9)
ax.axhline(0.4015, color='#999999', ls=':', lw=1)
ax.text(0.00075, 0.4015 + 0.004, '0.4015', color='#777777', fontsize=9)
ax.set_xlabel('chance p that a dragged neighbour is a far species')
ax.set_ylabel('fitness threshold')
ax.set_ylim(0.2, 0.69)
ax.set_xlim(7e-4, 1.4)
ax.set_xticks([0.001, 0.01, 0.1, 1]); ax.set_xticklabels(['0.001', '0.01', '0.1', '1'])
ax.legend(loc='lower left', fontsize=8, frameon=False)
ax.set_title('Same number of far links, fixed or fresh', loc='left', fontsize=11)

b = fig.add_axes([0.68, 0.2, 0.29, 0.7])
Ns = np.array([500, 2000, 8000, 32000])
P1 = [analyse.fc_of(f'qruns/P1_N{N}')[0] for N in Ns]
RG = [analyse.fc_of(f'qruns/REG_N{N}')[0] for N in Ns]
x = Ns ** -0.5
b.plot(x, P1, 'o-', color='#d5573a', label='random fixed links')
b.plot(x, RG, 's-', color='#8a3ad5', label='every species dragged by exactly 2')
b.axhline(0.4015, color='black', lw=1.2, label='endless tree: 0.4015')
b.axhline(1/3, color='#3a7bd5', lw=1, ls='--', label='fresh links: 1/3')
for N, xx, y, off in zip(Ns, x, P1, [(6, 4), (6, 4), (4, 8), (-4, 14)]):
    b.annotate(f'N {N}', (xx, y), textcoords='offset points', xytext=off, fontsize=8, color='#555555')
b.set_xlim(-0.003, 0.05)
b.set_ylim(0.32, 0.435)
b.set_xlabel('1 / sqrt(N)')
b.set_title('Every link far (p = 1)', loc='left', fontsize=11)
b.legend(loc='center right', fontsize=8, frameon=False)

fig.text(0.01, 0.015, 'Bak-Sneppen evolution: each step the least fit species and two neighbours get new random fitnesses. Fixed links let the weakest species come back\nand stir the same two it just stirred: on the endless tree, 10.2% of drags at the threshold land on a species that is already weak, exactly the (3f - 1)/2 that lifts 1/3 to 0.4015.', fontsize=8, color='#555555')
fig.savefig('fixed_or_fresh.png', dpi=130, facecolor='white')
print('saved')
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
            bad += 1; print('OVERLAP', items[i][0], '|', items[j][0])
W, H = fig.bbox.width, fig.bbox.height
out = [n for n, bb in items if bb.x0 < 0 or bb.y0 < 0 or bb.x1 > W or bb.y1 > H]
print(len(items), 'texts,', bad, 'overlaps, outside figure:', out)
# legend vs plotted data check
for a in fig.axes:
    lg = a.get_legend(); lb = lg.get_window_extent(r)
    hits = 0
    for ln in a.get_lines():
        xy = ln.get_xydata()
        if len(xy) == 0: continue
        if len(xy) == 2 and ln.get_transform() != a.transData:  # axhline in axes coords
            pts = a.get_xaxis_transform().transform(np.c_[np.linspace(0, 1, 200), np.full(200, xy[0, 1])]) if False else None
        d = ln.get_transform().transform(xy)
        # densify segments
        if ln.get_linestyle() not in ('None', ''):
            d = np.vstack([np.linspace(d[i], d[i + 1], 50) for i in range(len(d) - 1)]) if len(d) > 1 else d
        inside = (d[:, 0] > lb.x0) & (d[:, 0] < lb.x1) & (d[:, 1] > lb.y0) & (d[:, 1] < lb.y1)
        if inside.any(): hits += 1; print('legend covers', ln.get_label())
    print(a.get_title()[:20], 'legend-data hits:', hits)
