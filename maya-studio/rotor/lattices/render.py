import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from edge import load

S3 = 3**0.5

def edge_profile(f, lat, c, nb=180):
    g, px, py = load(f, lat); occ = g > 0
    qx, qy = px - c[0], py - c[1]
    th = np.arctan2(qy, qx); r = np.hypot(qx, qy)
    b = ((th + np.pi) / (2*np.pi) * nb).astype(int) % nb
    out = np.array([r[(b == k) & occ].max() for k in range(nb)])
    ang = (np.arange(nb) + 0.5) / nb * 360 - 180
    return ang, out - out.mean()

fig = plt.figure(figsize=(15, 10.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], hspace=0.38, wspace=0.22)

# panel 1: the sine
ax = fig.add_subplot(gs[0, 0])
a0, e0 = edge_profile('out/L0_m0.bin', 0, (0, 0))
a1, e1 = edge_profile('out/L0_m0.bin', 0, (0.5, -0.5))
ax.plot(a0, e0, color='#c0504d', lw=1.6, label='measured from where walkers start')
ax.plot(a1, e1, color='#1f4e79', lw=1.6, label='measured from (+1/2, -1/2), the predicted centre')
ax.set_xlabel('direction (degrees)'); ax.set_ylabel('edge radius minus its mean (cells)')
ax.set_xlim(-180, 180); ax.set_ylim(-1.3, 1.3)
ax.set_title('Square grid, all arrows north, 200,000 walkers:\nthe "roughness" was a disc sitting half a cell off', fontsize=11)
ax.legend(loc='lower left', fontsize=9, frameon=False)

# panel 2: gap vs radius, about the centroid
ax = fig.add_subplot(gs[0, 1])
names = {0: 'square', 1: 'square N,S,E,W', 2: 'triangle', 3: 'honeycomb'}
cols = {0: '#1f4e79', 1: '#7f7f7f', 2: '#c0504d', 3: '#4f8a3a'}
for l in [0, 2, 3]:
    d = np.loadtxt(f'out2/L{l}_m0.txt'); d = d[d[:, 0] >= 300]
    ax.plot(d[:, 1], d[:, 9], color=cols[l], lw=1.8, label=f'{names[l]}, arrows all alike')
    d = np.loadtxt(f'out2/L{l}_m1.txt'); d = d[d[:, 0] >= 300]
    ax.plot(d[:, 1], d[:, 9], color=cols[l], lw=1.2, ls='--', label=f'{names[l]}, random arrows')
for l in [0, 2, 3]:
    d = np.loadtxt(f'out/L{l}_m2.txt'); d = d[d[:, 0] >= 300]
    ax.plot(d[:, 1], d[:, 4], color=cols[l], lw=0.9, ls=':', alpha=0.9)
ax.text(170, 3.55, 'dotted: random steps (IDLA)', fontsize=9, color='#444444')
ax.set_xlabel('disc radius (bond lengths)'); ax.set_ylabel('edge gap about the centre of mass')
ax.set_ylim(0, 9.6); ax.set_xlim(8, 300)
ax.set_title('Measured from the true centre, arrows that start alike make\nnear-perfect discs; random arrows are 3 to 10 times rougher', fontsize=11)
ax.legend(loc='upper left', fontsize=8.2, frameon=False, ncol=2)

# panel 3: predicted vs measured centres
ax = fig.add_subplot(gs[1, :]); ax.axis('off')
rows = [
 ('square, arrows N, turn N-E-S-W', '(+0.500, -0.500)', '(+0.495, -0.492)', 'a corner between four cells'),
 ('square, checkerboard N/E', '(0, -0.500)', '(+0.003, -0.496)', 'middle of the edge below'),
 ('square, arrows N, turn N-S-E-W', '(+0.250, -0.750)', '(+0.276, -0.717)', 'off by 0.04 (order is uneven)'),
 ('triangle, all alike', '(-0.500, -0.866)', '(-0.495, -0.862)', 'a neighbouring site'),
 ('honeycomb, all along own vertical bond', '(0, 0)', '(+0.002, -0.000)', 'exactly where walkers start'),
 ('honeycomb, B sites one turn on', '(+0.433, -0.250)', '(+0.434, -0.247)', 'middle of a bond'),
 ('honeycomb, B sites two turns on', '(0, -0.500)', '(+0.003, -0.497)', 'halfway to a hexagon centre'),
 ('any grid, random arrows', '(0, 0)', 'within 0.003', 'where walkers start'),
]
cell = [[r[0], r[1], r[2], r[3]] for r in rows]
tab = ax.table(cellText=cell, colLabels=['grid and starting arrows', 'predicted centre', 'measured centre (200,000)', 'where that is'],
               loc='upper center', cellLoc='left', colWidths=[0.30, 0.17, 0.2, 0.27])
tab.auto_set_font_size(False); tab.set_fontsize(10); tab.scale(1, 1.55)
for (r, c), t in tab.get_celld().items():
    t.set_edgecolor('#bbbbbb')
    if r == 0: t.set_text_props(weight='bold')
ax.set_title('Where the disc is centred, predicted with no simulation: every site leaves a part-turn of arrows behind,\n'
             'and a part-turn of k arrows pushes walkers by the sum of those k directions. Average over k = 0 .. (number of directions - 1).',
             fontsize=11, loc='center', pad=4)

fig.suptitle('Rotor discs, re-measured: round, but not centred where the walkers start', fontsize=14, y=0.985)
fig.savefig('off_centre.png', dpi=130)

# overlap check at save dpi
fig.canvas.draw(); r = fig.canvas.get_renderer()
texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip() and t.axes is not None and t.axes.axison or (t.get_visible() and t.get_text().strip() and t.figure is fig and t.axes is None)]
bb = [(t, t.get_window_extent(r)) for t in texts]
ov = 0
for i in range(len(bb)):
    for j in range(i+1, len(bb)):
        if bb[i][1].overlaps(bb[j][1]):
            ov += 1; print('OVERLAP', repr(bb[i][0].get_text()[:30]), repr(bb[j][0].get_text()[:30]))
print(len(bb), 'texts', ov, 'overlaps')
