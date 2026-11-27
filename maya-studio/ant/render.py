# Three ways out: the ant's footprint on lightly, barely and half scribbled ground, plus escape times.
import glob, collections, statistics as st
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

W = 440
BG = '#0d1020'
cmap = ListedColormap([BG, '#5a6078', '#2f8f8a', '#ffb347'])
# median-time seed of 9 for each density (times to r = 200 printed by footprint)
panels = [
    (0.005, 5, 85444, 10799, 'Half a percent scribbled: it flies',
     'Short highways carry it\nbetween the dots'),
    (0.02, 1, 479715, 34989, 'Two percent scribbled: it fills',
     'Highways break on the dots;\nit paints a solid blob'),
    (0.5, 6, 27762, 9797, 'Half scribbled: it wanders',
     'No highways at all;\na thin random-walk trail'),
]

fig = plt.figure(figsize=(13, 11.6), facecolor=BG)
fig.text(0.5, 0.965, 'Three ways out', ha='center', color='white', fontsize=24, weight='bold')
fig.text(0.5, 0.935, "Langton's ant starts on ground already scribbled at random. Each picture is the moment it first gets 200 cells from where it began.",
         ha='center', color='#c8cbe0', fontsize=11.5)

pos = [(0.04, 0.50), (0.52, 0.50), (0.04, 0.04)]
for (p, seed, t, vis, title, sub), (x0, y0) in zip(panels, pos):
    a = np.fromfile(f'fp/p{p}_s{seed}.raw', dtype=np.uint8).reshape(W, W)
    ax = fig.add_axes([x0, y0, 0.42, 0.38])
    ax.imshow(a, cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(W / 2 + 200 * np.cos(th), W / 2 + 200 * np.sin(th), color='#ffffff', lw=0.6, alpha=0.35)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color('#30344a')
    ax.set_title(title, color='white', fontsize=14, pad=8)
    fig.text(x0 + 0.21, y0 - 0.025, f'{t:,} steps, {vis:,} cells touched', ha='center', color='#ffb347', fontsize=11)
    ax.text(6, 18, sub, color='#e6e8f5', fontsize=10.5, va='top',
            bbox=dict(facecolor=BG, edgecolor='none', alpha=0.75, pad=3))

# escape-time chart from the endless-plane runs
D = collections.defaultdict(list)
for f in glob.glob('plane_runs/*.txt'):
    for l in open(f):
        a = l.split(); D[float(a[0])].append([int(v) for v in a[2:]])
for f in glob.glob('diag/*.txt'):
    for l in open(f):
        a = l.split()
        if float(a[0]) == 0.005: D[0.005].append([int(v) for v in a[2:]])
ps = sorted(p for p in D if p <= 0.5)
ax = fig.add_axes([0.60, 0.10, 0.36, 0.30], facecolor='#151a30')
for idx, (r, col) in enumerate([(160, '#2f8f8a'), (1280, '#ffb347')]):
    i = [20, 40, 80, 160, 320, 640, 1280].index(r)
    med = [st.median(x[2 * i] for x in D[p]) for p in ps]
    ax.plot(ps, med, 'o-', color=col, lw=2, ms=5, label=f'to get {r} cells out')
    m98 = st.median(x[2 * i] for x in D[0.98])
    ax.plot([0.02], [m98], marker='x', color='white', ms=9, mew=1.5, ls='none',
            label='98% scribbled (mirror of 2%)' if idx == 0 else None)
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('share of ground scribbled', color='#c8cbe0', fontsize=11)
ax.set_ylabel('median steps', color='#c8cbe0', fontsize=11)
ax.tick_params(colors='#c8cbe0', labelsize=9)
for s in ax.spines.values(): s.set_color('#30344a')
ax.set_xticks([0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5])
ax.set_xticklabels(['0.5%', '1%', '2%', '5%', '10%', '20%', '50%'])
ax.minorticks_off()
ax.legend(facecolor='#151a30', edgecolor='#30344a', labelcolor='#e6e8f5', fontsize=9.5, loc='upper right')
ax.set_title('Slowest at about 2%, not at 50%', color='white', fontsize=14, pad=8)
fig.text(0.78, 0.035, 'Medians over 200 runs each (40 at 0.5%, 50 at 1%)', ha='center', color='#8c90a8', fontsize=9.5)

fig.savefig('three_ways_out.png', dpi=110, facecolor=BG)

# programmatic check: texts inside the figure and not overlapping each other
fig.canvas.draw()
r = fig.canvas.get_renderer()
boxes = []
for t_ in fig.findobj(matplotlib.text.Text):
    if not t_.get_text().strip() or not t_.get_visible():
        continue
    if t_.axes is not None and t_ in (t_.axes.xaxis.get_ticklabels(minor=False) + t_.axes.yaxis.get_ticklabels(minor=False)):
        bb = t_.get_window_extent(r)
        if bb.width == 0: continue
    bb = t_.get_window_extent(r)
    boxes.append((t_.get_text()[:30], bb))
W_, H_ = fig.canvas.get_width_height()
prob = 0
for name, bb in boxes:
    if bb.x0 < 0 or bb.y0 < 0 or bb.x1 > W_ or bb.y1 > H_:
        print('OUT', name); prob += 1
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        a, b = boxes[i][1], boxes[j][1]
        if a.overlaps(b) and a.width > 0 and b.width > 0:
            print('OVERLAP', boxes[i][0], '|', boxes[j][0]); prob += 1
print(len(boxes), 'texts,', prob, 'problems')
for p in ps + [0.98]:
    print(p, len(D[p]), int(st.median(x[6] for x in D[p])), int(st.median(x[12] for x in D[p])))
