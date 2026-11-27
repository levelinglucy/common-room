"""Picture for the mycelium.py cliff: weight traces (A) and lifetime vs shortcut time (B)."""
import sys, random, json
sys.path.insert(0, '/home/sprite')
sys.path.insert(0, '/home/sprite/maya-studio/memory')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mycelium as M
from myc_cliff import ORG, A, B, AWAY, TRAIN, run


def trace(seed, cond, floor):
    M.PRUNE_BELOW = floor
    net = M.Mycelium(nodes=list(ORG), rng=random.Random(seed))
    for a, b in zip(ORG, ORG[1:] + ORG[:1]):
        net.grow(a, b)
    net.grow(A, B)
    k = M._key(A, B)
    ws = []
    for _ in range(TRAIN):
        net.route(A, B); net.tick(); ws.append(net.hyphae.get(k, 0.0))
    x, y = AWAY[cond]
    kxy = M._key(x, y)
    direct = None
    for t in range(1, 200):
        net.route(x, y)
        if direct is None and kxy in net.hyphae:
            direct = t
        res = net.tick()
        if k in res['pruned']:
            ws.append(0.0)
            break
        ws.append(net.hyphae.get(k, 0.0))
    return ws, direct


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.6))

# A: one seed, pure decay at three floors, plus a rehearsed run
cols = {0.15: '#c0392b', 0.015: '#d68910', 0.0015: '#7d3c98'}
for fl, c in cols.items():
    # find a seed with no reuse in 'elsewhere' at this floor
    for s in range(50):
        M.PRUNE_BELOW = fl
        if run(s, 'elsewhere')['uses'] == 0:
            break
    ws, _ = trace(s, 'elsewhere', fl)
    ax1.plot(range(1, len(ws) + 1), ws, color=c, lw=1.8,
             label=f'unused after training, floor {fl}: pruned {len(ws) - TRAIN} ticks later')
    ax1.axhline(fl, color=c, lw=0.6, ls=':')
M.PRUNE_BELOW = 0.15
best = None
for s in range(300):
    r = run(s, 'near')
    if r['direct'] and 35 <= r['direct'] <= 60:
        best = s; break
ws, d = trace(best, 'near', 0.15)
ax1.plot(range(1, len(ws) + 1), ws, color='#1f618d', lw=2.2,
         label=f'new job io->logger still walks the old road: lives {len(ws) - TRAIN} ticks')
ax1.axvline(TRAIN + d, color='#1f618d', lw=0.8, ls='--')
ax1.text(TRAIN + d + 2, 8.6, 'new job grows\nits own hypha', color='#1f618d', fontsize=9, va='top')
ax1.axvline(TRAIN, color='0.5', lw=0.8)
ax1.text(TRAIN - 2, 8.6, 'training ends', color='0.4', fontsize=9, ha='right', va='top')
ax1.set_yscale('symlog', linthresh=0.001)
ax1.set_ylim(0, 12)
ax1.set_xlabel('tick')
ax1.set_ylabel('weight of io_channel <-> memory_store')
ax1.set_title('A. The old road in mycelium.py: flat while used, then a fixed fall to the floor', fontsize=10.5)
ax1.legend(fontsize=8, loc='lower left')

# B: lifetime vs time until the new job has a shortcut
M.PRUNE_BELOW = 0.15
for cond, c, mk in (('near', '#1f618d', 'o'), ('far', '#148f77', 's')):
    pts = [run(s, cond) for s in range(300)]
    xs = [p['direct'] for p in pts if p['direct'] is not None]
    ys = [p['death'] for p in pts if p['direct'] is not None]
    ax2.scatter(xs, ys, s=12, alpha=0.55, color=c, marker=mk,
                label=f'new job io->{AWAY[cond][1]} ({len(xs)} runs)')
xx = [0, 300]
ax2.plot(xx, [46, 46], color='#c0392b', lw=1, ls=':')
ax2.plot(xx, [x + 46 for x in xx], color='0.3', lw=1, ls='--')
ax2.text(150, 205, 'shortcut tick + 46', rotation=0, fontsize=9, color='0.3')
ax2.text(200, 50, 'never used again: 46', fontsize=9, color='#c0392b')
ax2.set_xlim(0, 300); ax2.set_ylim(0, 400)
ax2.set_xlabel('tick (after training) when the new job gets its own direct hypha')
ax2.set_ylabel('tick the old road is pruned')
ax2.set_title('B. The old road lives as long as the new job needs it, then 46 ticks', fontsize=10.5)
ax2.legend(fontsize=8, loc='upper left')
fig.suptitle("Forgetting in Velisara's mycelium.py (unchanged code, PRUNE_BELOW 0.15 unless shown, 300 seeds)", fontsize=12)
fig.tight_layout()
fig.savefig('/home/sprite/maya-studio/memory/myc_cliff.png', dpi=130)

# text check: overlaps and bounds
fig.canvas.draw()
r = fig.canvas.get_renderer()
W, H = fig.canvas.get_width_height()
texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_text().strip() and t.get_visible()]
boxes = []
for t in texts:
    if getattr(t, 'axes', None) is None and t not in fig.texts and t.get_text() not in (fig._suptitle.get_text() if fig._suptitle else '',):
        pass
    bb = t.get_window_extent(r)
    boxes.append((t.get_text()[:30], bb))
bad = 0
for name, bb in boxes:
    if bb.x0 < 0 or bb.y0 < 0 or bb.x1 > W or bb.y1 > H:
        print('OUT', name); bad += 1
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        a, b = boxes[i][1], boxes[j][1]
        if a.width and b.width and a.overlaps(b):
            print('OVERLAP', boxes[i][0], '|', boxes[j][0]); bad += 1
print('texts', len(boxes), 'problems', bad)
