"""memory_cliff.png: one mould remembering, then forgetting all at once; plus the sweep."""
import csv
import math
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

from memory import mesh, Mould, DT
from forced import crossing, recall, T1, LID

SEED, FLOOR = 1, 1e-6
BG, INK, TUBE, DIM = '#0e0c0a', '#ece2c8', '#f6c434', '#7d7564'
COLS = {1e-3: '#e07a5f', 1e-6: '#f6c434', 1e-9: '#81b29a', 0.0: '#a9a9d9'}


def states():
    pts, edges, A, B, C, centre = mesh(seed=SEED)
    lid = crossing(pts, edges, centre, 'up')     # seed 1 is trained under the hole
    out = {}
    for T in (11, 13):
        m = Mould(pts, edges, FLOOR, SEED)
        for _ in range(int(round(T1 / DT))):
            m.D[lid] = LID
            Q, _ = m.flow(A, B)
            q = np.abs(Q) ** 1.8
            m.D = np.maximum(m.D + DT * (q / (1 + q) - m.D), FLOOR)
        m.D[lid] = FLOOR
        out['trained'] = m.D.copy()
        m.run(A, C, T)
        out[f'idle{T}'] = m.D.copy()
        side, share, rl = recall(m, pts, edges, A, B, centre)
        out[f'recall{T}'] = (m.D.copy(), side, rl)
    return pts, edges, A, B, C, centre, out


def tubes(ax, pts, edges, D, A, B, C, centre, title, sub):
    ax.set_facecolor(BG)
    seg = pts[edges]
    lw = 0.25 + 4.5 * np.clip(D / 0.5, 0, 1)
    alive = np.clip((np.log10(np.maximum(D, 1e-12)) + 9) / 9, 0.0, 1.0)
    cols = np.zeros((len(D), 4))
    cols[:, :3] = np.array(matplotlib.colors.to_rgb(TUBE))
    cols[:, 3] = 0.08 + 0.92 * alive
    ax.add_collection(LineCollection(seg, linewidths=lw, colors=cols, capstyle='round'))
    ax.add_patch(plt.Circle(centre, 3.7, color='#1c1915', zorder=3))
    for node, name in ((A, 'A'), (B, 'B'), (C, 'C')):
        ax.plot(*pts[node], 'o', ms=9, color=INK, zorder=4)
        ax.text(pts[node][0], pts[node][1] + 1.4, name, color=INK, ha='center', va='bottom', fontsize=10, zorder=5)
    ax.set_xlim(pts[:, 0].min() - 0.8, pts[:, 0].max() + 0.8)
    ax.set_ylim(pts[:, 1].min() - 0.8, pts[:, 1].max() + 2.6)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, color=INK, fontsize=12, loc='left', pad=18)
    ax.text(0.0, 1.015, sub, transform=ax.transAxes, color=DIM, fontsize=9, ha='left', va='bottom')


def sweep():
    rows = list(csv.DictReader(open('forced_24.tsv'), delimiter='\t'))
    g = defaultdict(list)
    for r in rows:
        g[(float(r['floor']), float(r['T']))].append(r)
    kept, rl = defaultdict(list), defaultdict(list)
    for (f, T), v in sorted(g.items()):
        differ = [r for r in v if r['want'] != r['naive']]
        kept[f].append((T, sum(r['side3'] == r['want'] for r in differ) / len(differ)))
        rl[f].append((T, np.mean([float(r['relearn']) for r in v]), np.mean([float(r['nrelearn']) for r in v])))
    return kept, rl


def main():
    pts, edges, A, B, C, centre, st = states()
    kept, rl = sweep()
    fig = plt.figure(figsize=(13, 8.6), facecolor=BG)
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.05], hspace=0.42, wspace=0.12,
                          left=0.075, right=0.97, top=0.86, bottom=0.08)
    fig.text(0.05, 0.955, 'A road the slime mould stopped using', color=INK, fontsize=17, ha='left')
    fig.text(0.05, 0.92, 'Taught to go A to B under the hole, then sent to C for a while, then asked for B again. '
             'Tubes can never be thinner than one millionth.', color=DIM, fontsize=10, ha='left')
    D11, s11, _ = st['recall11']
    D13, s13, _ = st['recall13']
    tubes(fig.add_subplot(gs[0, 0]), pts, edges, st['trained'], A, B, C, centre,
          'Taught: under the hole', 'the over road was blocked while it learned')
    tubes(fig.add_subplot(gs[0, 1]), pts, edges, D11, A, B, C, centre,
          f'Away for 11, then back: {"under" if s11 == "down" else "over"}', 'the old road was still above the floor')
    tubes(fig.add_subplot(gs[0, 2]), pts, edges, D13, A, B, C, centre,
          f'Away for 13, then back: {"under" if s13 == "down" else "over"}', 'old road at the floor: same as never taught')

    ax = fig.add_subplot(gs[1, 0:2])
    ax.set_facecolor(BG)
    for f in (1e-3, 1e-6, 1e-9, 0.0):
        T, k = zip(*kept[f])
        lab = 'no floor' if f == 0 else f'floor 1e{int(round(math.log10(f)))}'
        ax.plot(T, k, '-o', color=COLS[f], ms=4, lw=2, label=lab)
        if f > 0:
            ts = math.log(0.5 / f) / (-math.log(1 - DT) / DT)
            ax.axvline(ts, color=COLS[f], ls=':', lw=1.2)
    ax.set_xlabel('time away (sent to C)', color=INK)
    ax.set_ylabel('still takes the taught road', color=INK)
    ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(['never', 'half', 'always'])
    ax.set_ylim(-0.08, 1.12)
    ax.text(0.01, 0.5, 'dotted: where I predicted each cliff, ln(0.5 / floor) / 1.116', transform=ax.transAxes,
            color=DIM, fontsize=9, va='center')
    ax.legend(loc='upper right', facecolor=BG, edgecolor=DIM, labelcolor=INK, fontsize=9, ncol=4)
    ax.set_title('Only the meshes where the taught road is the slightly worse one (11 to 16 of 24)', color=INK,
                 fontsize=11, loc='left')

    bx = fig.add_subplot(gs[1, 2])
    bx.set_facecolor(BG)
    T, r, n = zip(*rl[1e-6])
    bx.plot(T, r, '-o', color=COLS[1e-6], ms=4, lw=2, label='taught before')
    bx.plot(T, n, '--', color=DIM, lw=1.6, label='never taught')
    bx.set_xlabel('time away', color=INK)
    bx.set_ylabel('time to settle again', color=INK)
    bx.set_ylim(0, 7.5)
    bx.legend(loc='lower right', facecolor=BG, edgecolor=DIM, labelcolor=INK, fontsize=9)
    bx.set_title('Floor 1e-6: no fading, just a drop', color=INK, fontsize=11, loc='left')
    for a in (ax, bx):
        a.tick_params(colors=INK)
        for s in a.spines.values():
            s.set_color(DIM)
    fig.savefig('memory_cliff.png', dpi=110, facecolor=BG)

    # programmatic text checks
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    W, H = fig.bbox.width, fig.bbox.height
    texts = list(fig.texts)
    for a in fig.axes:
        texts += [a.title, a._left_title, a.xaxis.label, a.yaxis.label] + list(a.texts)
        if a.get_legend():
            texts += list(a.get_legend().get_texts())
        lo, hi = sorted(a.get_xlim())
        texts += [t.label1 for t in a.xaxis.get_major_ticks() if lo <= t.get_loc() <= hi]
        lo, hi = sorted(a.get_ylim())
        texts += [t.label1 for t in a.yaxis.get_major_ticks() if lo <= t.get_loc() <= hi]
    boxes = [(t.get_text()[:40], t.get_window_extent(rend)) for t in texts if t.get_visible() and t.get_text().strip()]
    problems = 0
    for name, bb in boxes:
        if bb.x0 < 0 or bb.y0 < 0 or bb.x1 > W or bb.y1 > H:
            print('OUT OF BOUNDS', name); problems += 1
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes[i][1].overlaps(boxes[j][1]):
                print('OVERLAP', repr(boxes[i][0]), '|', repr(boxes[j][0])); problems += 1
    print('sides: recall11', s11, 'recall13', s13, ' problems', problems, ' texts', len(boxes))


if __name__ == '__main__':
    main()
