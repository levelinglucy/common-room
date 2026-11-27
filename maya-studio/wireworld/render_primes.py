"""Picture: the WireWorld computer showing 23, beside where its time goes."""
import sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.argv = ['x']
src = open('fit_program.py').read().split("if __name__ == '__main__':\n    pr")[0]
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(src)

log2 = sys.argv  # placeholder
verify = {}
try:
    from decode_log import decode, events
    g2, s2 = decode('seglog2.txt')
    verify = {n: t for n, t in events(g2, s2)}
except Exception as e:
    print('no verification log', e)

BG = '#0d0f14'
fig = plt.figure(figsize=(15, 9.2), facecolor=BG)

# left: the machine
ax0 = fig.add_axes([0.01, 0.04, 0.36, 0.86])
grid = np.fromfile('snaps/full_2060000.raw', np.uint8).reshape(905, 570)
pal = np.array([[13, 15, 20], [120, 220, 255], [255, 255, 255], [150, 80, 30]], np.uint8)
ax0.imshow(pal[grid], interpolation='nearest')
ax0.set_axis_off()
ax0.set_title('the copper computer at generation 2,060,000, showing 23', color='w', fontsize=11)

# right top: cost of testing each odd number (model fitted to the measured gaps)
ax1 = fig.add_axes([0.44, 0.56, 0.54, 0.34], facecolor=BG)
ns = np.arange(7, 90, 2)
cost = np.array([np.dot(coef_c, feats(int(n), RND['ceil'])) for n in ns]) / 1e6
isp = np.array([all(n % q for q in range(3, int(n ** .5) + 1, 2)) for n in ns])
ax1.bar(ns[isp], cost[isp], width=1.6, color='#ffb347', label='prime: every odd divisor up to itself')
ax1.bar(ns[~isp], cost[~isp], width=1.6, color='#5a6a80', label='not prime: stops at its first factor')
for n, c in zip(ns, cost):
    if n in (9, 15, 25, 49, 77, 91 - 2):
        pass
ax1.set_xlim(5, 91)
ax1.set_ylabel('millions of generations', color='w')
ax1.set_xlabel('the odd number being tested', color='w')
ax1.legend(facecolor=BG, edgecolor='#333', labelcolor='w', fontsize=9, loc='upper left')
share = cost[isp].sum() / cost.sum()
ax1.set_title(f'how long it spends on each number ({share*100:.0f}% of the time from 7 to 89 goes on primes)', color='w', fontsize=11)

# right bottom: when each prime appears, measured, fitted, predicted
ax2 = fig.add_axes([0.44, 0.08, 0.54, 0.36], facecolor=BG)
ax2.plot(P, T / 1e6, 'o', color='#ffb347', ms=5, label='seen on the display')
for n, t in zip(P, T):
    if n < 20: continue
    ax2.annotate(str(n), (n, t / 1e6), textcoords='offset points', xytext=(-4, 6), color='#bbb', fontsize=7)
pr = predict_after(int(P[-1]), int(T[-1]), 104)
ax2.plot([n for n, _ in pr], [t / 1e6 for _, t in pr], 'x', color='#78dcff', ms=9, mew=2,
         label='predicted before running')
vx = [n for n, _ in pr if n in verify]
if vx:
    ax2.plot(vx, [verify[n] / 1e6 for n in vx], 'o', mfc='none', mec='w', ms=12, mew=1.2,
             label='then seen')
ax2.set_xlabel('prime', color='w')
ax2.set_ylabel('generation it appears (millions)', color='w')
ax2.legend(facecolor=BG, edgecolor='#333', labelcolor='w', fontsize=9, loc='upper left')
ax2.set_title('when each prime reaches the display', color='w', fontsize=11)
for ax in (ax1, ax2):
    ax.tick_params(colors='#ccc')
    for s in ax.spines.values():
        s.set_color('#444')

fig.suptitle('Primes in copper: the Moore/Owen WireWorld computer running Michael Fryers\' program',
             color='w', fontsize=14, y=0.985)
fig.savefig('primes_in_copper.png', dpi=110, facecolor=BG)
print('share on primes', share, 'verify', {n: verify.get(n) for n, _ in pr})
print('pred', [(n, int(t)) for n, t in pr])

# layout check: overlapping text boxes, and legends covering data
fig.canvas.draw(); r = fig.canvas.get_renderer()
texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip()]
bbs = [(t.get_text()[:30], t.get_window_extent(r)) for t in texts]
bad = [(a, b) for i, (a, ba) in enumerate(bbs) for (b, bb) in bbs[i+1:] if ba.overlaps(bb)]
print('text overlaps:', bad)
for ax in (ax1, ax2):
    lb = ax.get_legend().get_window_extent(r)
    pts = []
    for ln in ax.lines:
        xy = ax.transData.transform(np.c_[ln.get_xdata(), ln.get_ydata()])
        pts += [p for p in xy if lb.contains(*p)]
    for c in ax.containers:
        for b in c:
            if b.get_window_extent(r).overlaps(lb): pts.append('bar')
    print('legend covers', len(pts), 'data items')
