# Render kaleidoscope_wall.png: the single-defector kaleidoscope, and why 0.318 is a wall effect.
import numpy as np, glob, re, math, collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

TARGET = 12*math.log(2) - 8

def load(f):
    return np.array([[float(a) for a in l.split()] for l in open(f) if len(l.split()) == 2])

# --- data: f by grid size and boundary ---
groups = collections.defaultdict(list)
for f in glob.glob('runs2/*_L*_s*.txt') + glob.glob('runs/L*_s*.txt'):
    name = f.split('/')[-1]
    m = re.match(r'(per|fix)?_?L(\d+)_s\d+', name)
    kind = m.group(1) or 'per'; L = int(m.group(2))
    groups[(kind, L)].append(load(f)[500:, 1].mean())
per = sorted((L, np.mean(v), np.std(v, ddof=1)/math.sqrt(len(v))) for (k, L), v in groups.items() if k == 'per')
fix = sorted((L, np.mean(v), np.std(v, ddof=1)/math.sqrt(len(v))) for (k, L), v in groups.items() if k == 'fix')
finf = np.mean([m for L, m, s in per if L >= 400])
# fit walled excess = a/L + c/L^2
Ls = np.array([L for L, m, s in fix], float); ex = np.array([m for L, m, s in fix]) - finf
A = np.vstack([1/Ls, 1/Ls**2]).T
a, c = np.linalg.lstsq(A, ex, rcond=None)[0]
Lcross = None
for L in np.arange(100, 3000, 0.5):
    if finf + a/L + c/L**2 < TARGET:
        Lcross = L; break
print('f_inf %.5f  a %.3f  c %.2f  crossing L %.0f' % (finf, a, c, Lcross))

# --- kaleidoscope frames ---
L = 199; N = L*L
raw = open('single199.bin', 'rb').read(); rec = 8 + N
frames = {}
for i in range(len(raw)//rec):
    t = int(np.frombuffer(raw[i*rec:i*rec+8], dtype=np.int64)[0])
    frames[t] = np.frombuffer(raw[i*rec+8:(i+1)*rec], dtype=np.uint8).reshape(L, L)
show = [30, 60, 100, 3000]
cmap = ListedColormap(['#2b59c3', '#d1342f', '#3fae49', '#f2c12e'])  # C stays, D stays, D->C, C->D

prof = np.load('acc/profile400.npy')

fig = plt.figure(figsize=(14, 9.2), facecolor='white')
fig.suptitle('One defector, then a kaleidoscope. And the famous 0.318 is the walls talking.', fontsize=15, y=0.985)
axs = [fig.add_axes([0.03 + 0.235*i, 0.55, 0.22, 0.36]) for i in range(4)]
for ax, t in zip(axs, show):
    ax.imshow(frames[t], cmap=cmap, vmin=0, vmax=3, interpolation='nearest')
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title('step %d' % t, fontsize=11)
fig.text(0.03, 0.515, 'Nowak-May dilemma, 199 x 199 walled grid, b = 1.9, one defector in the middle of a cooperating world.   '
         'blue: stays a cooperator   red: stays a defector   green: defector turns cooperator   yellow: cooperator turns defector.   '
         'Every frame keeps all 8 symmetries of the square.', fontsize=8.5, wrap=True)

# panel: f vs L
ax1 = fig.add_axes([0.07, 0.08, 0.40, 0.36])
LL = np.linspace(90, 3200, 400)
ax1.plot(LL, finf + a/LL + c/LL**2, color='#d1342f', lw=1, alpha=0.6)
ax1.errorbar([p[0] for p in fix], [p[1] for p in fix], yerr=[p[2] for p in fix], fmt='o', color='#d1342f', label='walled grid')
ax1.errorbar([p[0] for p in per], [p[1] for p in per], yerr=[p[2] for p in per], fmt='s', color='#2b59c3', label='wrap-around grid (no walls)')
ax1.axhline(finf, color='#2b59c3', lw=1, ls=':')
ax1.axhline(TARGET, color='k', lw=1, ls='--')
ax1.text(110, TARGET + 0.0004, '12 ln 2 - 8 = 0.31777', fontsize=9)
ax1.text(560, finf - 0.0011, 'no walls: %.4f at every size' % finf, fontsize=9, color='#2b59c3')
ax1.text(1050, finf + a/1000 + c/1e6 + 0.0009, 'walls: %.4f + %.2f / L' % (finf, a), fontsize=9, color='#d1342f')
ax1.axvline(Lcross, color='grey', lw=0.8)
ax1.text(Lcross*1.04, 0.3235, 'equal at L = %d' % round(Lcross), fontsize=9, color='grey')
ax1.set_xscale('log'); ax1.set_xlabel('grid side L'); ax1.set_ylabel('long-run share of cooperators')
ax1.set_ylim(0.3135, 0.327); ax1.set_xlim(85, 3600); ax1.set_xticks([100, 200, 400, 1000, 3000]); ax1.set_xticklabels(['100','200','400','1000','3000']); ax1.minorticks_off()
ax1.legend(loc='upper right', fontsize=9, frameon=False)
ax1.set_title('Long-run cooperator share (mean of steps 500 to the end)', fontsize=11)

# panel: wall halo
ax2 = fig.add_axes([0.57, 0.08, 0.40, 0.36])
ax2.plot(np.arange(len(prof)), prof, 'o-', color='#d1342f', ms=4)
ax2.axhline(finf, color='#2b59c3', ls=':', lw=1)
ax2.set_xlabel('cells from the nearest wall'); ax2.set_ylabel('time-averaged share of cooperators')
ax2.set_title('The halo: walls grow cooperators (400 x 400, 6 runs x 3500 steps)', fontsize=11)
ax2.set_xlim(-1, 40)
ax2.text(12, 0.405, 'cells on the wall play 6 games, not 9\n(corners 4), and cooperators gather there.\nAbout 0.23 extra cooperators per wall cell.', fontsize=9, va='top')
fig.savefig('kaleidoscope_wall.png', dpi=110)

# overlap check on all text artists
fig.canvas.draw(); r = fig.canvas.get_renderer()
texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_text().strip() and t.get_visible()]
boxes = [(t.get_text()[:30], t.get_window_extent(r)) for t in texts]
bad = 0
for i in range(len(boxes)):
    for j in range(i+1, len(boxes)):
        if boxes[i][1].overlaps(boxes[j][1]):
            bad += 1; print('OVERLAP:', boxes[i][0], '|', boxes[j][0])
print(len(boxes), 'texts,', bad, 'overlaps')
for ax in [ax1, ax2]:
    bb = ax.get_window_extent(r)
    for t in ax.texts:
        e = t.get_window_extent(r)
        inside = e.x0 >= bb.x0 and e.x1 <= bb.x1 and e.y0 >= bb.y0 and e.y1 <= bb.y1
        print('inside' if inside else 'OUTSIDE', repr(t.get_text()[:25]))
fb = fig.bbox
for t in fig.texts:
    e = t.get_window_extent(r); print('fig text', 'ok' if e.x1 <= fb.x1 and e.x0 >= 0 else 'CLIPPED', repr(t.get_text()[:25]))
