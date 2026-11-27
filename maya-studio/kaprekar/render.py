"""Render: base-10 landscape of steps to 6174, plus the (d1, d2) state spaces of the
6174 family in bases 5*2^m, coloured by steps to (3b/5, b/5-1, 4b/5-1, 2b/5), rivals in red."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def family_map(b):
    """Return grid[d1, d2] = steps to the family fixed point, -2 = rival basin, -1 = repdigit/invalid."""
    d = 4
    e1, e2 = np.meshgrid(np.arange(b), np.arange(b), indexing='ij')
    ok = e2 <= e1
    E1, E2 = e1[ok], e2[ok]
    n = E1 * (b ** 3 - 1) + E2 * (b ** 2 - b)
    digs = np.stack([(n // b ** j) % b for j in range(4)], 1)
    digs.sort(1)
    N1 = digs[:, 3] - digs[:, 0]
    N2 = digs[:, 2] - digs[:, 1]
    nxt = {}
    F1 = np.full((b, b), -1)
    F2 = np.full((b, b), -1)
    F1[E1, E2] = N1
    F2[E1, E2] = N2
    fx = (3 * b // 5) - (2 * b // 5) , None
    # fixed point digits (3b/5, b/5-1, 4b/5-1, 2b/5): sorted 4b/5-1, 3b/5, 2b/5, b/5-1 -> e1 = 3b/5, e2 = b/5
    t1, t2 = 3 * b // 5, b // 5
    assert F1[t1, t2] == t1 and F2[t1, t2] == t2, 'not a fixed point'
    steps = np.full((b, b), -1)
    steps[t1, t2] = 0
    # iterate: steps[x] = steps[f(x)] + 1
    a1, a2 = E1.copy(), E2.copy()
    cur1, cur2 = E1.copy(), E2.copy()
    s = np.zeros(len(E1), dtype=int)
    done = (cur1 == t1) & (cur2 == t2)
    for k in range(1, 4 * b + 50):
        live = ~done & (cur1 > 0)
        if not live.any():
            break
        c1 = F1[cur1[live], cur2[live]]
        c2 = F2[cur1[live], cur2[live]]
        cur1[live], cur2[live] = c1, c2
        s[live] = k
        done = (cur1 == t1) & (cur2 == t2)
    res = np.where(done, s, -2)
    res[(cur1 == 0)] = -3  # fell to zero
    grid = np.full((b, b), -1)
    grid[E1, E2] = res
    grid[0, :] = -1
    return grid


from kaprekar import K
steps10 = np.load('steps_6174.npy')

fig = plt.figure(figsize=(15, 8.6), facecolor='#0d0d12')
gs = fig.add_gridspec(2, 5, width_ratios=[1.0, 1.0, 0.62, 0.62, 0.62], wspace=0.08, hspace=0.18)
ax = fig.add_subplot(gs[:, :2])
pal = ['#1b1b22', '#ffffff', '#ffe08a', '#f4a261', '#e76f51', '#c2457a', '#7b3fa0', '#3d3a8c']
cm = ListedColormap(pal)
ax.imshow(steps10 + 1, cmap=cm, vmin=0, vmax=8, interpolation='nearest')
ax.set_title('every four-digit number, coloured by how many steps it takes to fall into 6174\n(row = first two digits, column = last two)', color='#ddd', fontsize=10)
ax.set_xticks([]); ax.set_yticks([])
labels = ['repdigit', '6174', '1', '2', '3', '4', '5', '6', '7']
for i, (c, l) in enumerate(zip(['#555'] + pal[1:], ['0000', '6174', '1 step', '2', '3', '4', '5', '6', '7 steps'])):
    x = 0.0 + i * 0.112
    ax.text(x, -0.035, '\u25a0', color=c, fontsize=12, va='center', transform=ax.transAxes)
    ax.text(x + 0.03, -0.035, l, color='#ccc', fontsize=8, va='center', transform=ax.transAxes)

bases = [(5, 'unique'), (10, 'unique'), (20, 'rival cycle'), (40, 'unique'), (80, 'rival cycle'), (160, 'unique')]
for i, (b, tag) in enumerate(bases):
    a = fig.add_subplot(gs[i // 3, 2 + i % 3])
    g = family_map(b).astype(float)
    img = np.zeros((b, b, 3)) + np.array([13, 13, 18]) / 255
    valid = g >= 0
    mx = g[valid].max() if valid.any() else 1
    cmap = plt.get_cmap('magma')
    img[valid] = cmap(0.25 + 0.75 * (1 - g[valid] / max(mx, 1)))[:, :3]
    img[g == -2] = np.array([0.45, 0.85, 0.95])
    img[g == -3] = np.array([0.3, 0.3, 0.3])
    a.imshow(img, origin='lower', interpolation='nearest')
    t1, t2 = 3 * b // 5, b // 5
    a.plot([t2], [t1], marker='o', ms=5, mfc='none', mec='white', mew=1)
    fp = f'({3*b//5}.{b//5-1}.{4*b//5-1}.{2*b//5})' if b != 10 else '6174'
    a.set_title(f'base {b}: {tag}\n{fp}', color='#ddd' if tag == 'unique' else '#8fd9ea', fontsize=9)
    a.set_xticks([]); a.set_yticks([])
    for sp in a.spines.values():
        sp.set_color('#333')
fig.text(0.70, 0.02, 'right: the same routine in bases 5\u00d72\u207f, drawn on (largest\u2212smallest digit) up, (middle gap) across. '
         'Bright = few steps to the cousin of 6174 (circled).\nBlue = numbers that orbit a rival cycle instead and never arrive. '
         'Unique in 5, 10, 40, 160, 640, 2560; a rival in 20, 80, 320, 1280.', color='#aaa', fontsize=8.2, ha='center')
fig.suptitle('6174 has cousins', color='white', fontsize=15, x=0.5, y=0.985)
plt.savefig('kaprekar_cousins.png', dpi=130, facecolor=fig.get_facecolor(), bbox_inches='tight')
print('saved')
