"""Draw the K(1,3) window: two sheets (even / odd positions), each cut into
the places a 1 can stand and the places a 3 can stand. Raster, not scatter."""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

d = np.load('ribbon_1_3.npz')
z, tag = d['z'], d['tag']
x, y = z.real, z.imag
G = 900
pad = 0.04
x0, x1 = x.min() - pad, x.max() + pad
y0, y1 = y.min() - pad, y.max() + pad
ix = ((x - x0) / (x1 - x0) * (G - 1)).astype(int)
iy = ((y1 - y) / (y1 - y0) * (G - 1)).astype(int)  # row 0 at top

BG = np.array([0.06, 0.06, 0.09])
ONE = np.array([0.98, 0.72, 0.25])    # amber: a 1 stands here
THREE = np.array([0.30, 0.62, 0.95])  # blue: a 3 stands here

def sheet(mask_tags):
    img = np.tile(BG, (G, G, 1))
    for t, col in mask_tags:
        m = tag == t
        img[iy[m], ix[m]] = col
    return img

even = sheet([(0, ONE), (2, THREE)])
odd = sheet([(1, ONE), (3, THREE)])
# overlay: where both sheets are filled, a pale colour
fe = np.zeros((G, G), bool); fe[iy[tag % 2 == 0], ix[tag % 2 == 0]] = True
fo = np.zeros((G, G), bool); fo[iy[tag % 2 == 1], ix[tag % 2 == 1]] = True
over = np.tile(BG, (G, G, 1))
over[fe & ~fo] = np.array([0.85, 0.35, 0.45])
over[fo & ~fe] = np.array([0.35, 0.80, 0.60])
over[fe & fo] = np.array([0.93, 0.91, 0.85])

fig, axs = plt.subplots(1, 3, figsize=(16.5, 6.4), facecolor=BG)
titles = ['even places', 'odd places', 'both sheets laid on top']
notes = ['amber: a 1 can stand here   blue: a 3', 'amber: a 1   blue: a 3',
         'pink: even only   green: odd only   pale: both']
for ax, im, t, n in zip(axs, [even, odd, over], titles, notes):
    ax.imshow(im, interpolation='nearest')
    ax.set_axis_off()
    ax.set_title(t, color='white', fontsize=15, pad=8)
    ax.text(0.5, -0.04, n, color='0.8', fontsize=11, ha='center', va='top', transform=ax.transAxes)
fig.suptitle('Where each letter of the Kolakoski sequence (1, 3) lives: 2,000,000 letters',
             color='white', fontsize=17, y=0.98)
fig.text(0.5, 0.025, 'Each letter is placed by how far the counts before it are from their average (the two shrinking directions). '
         'Inside each sheet the 1s and 3s never share ground.', color='0.75', fontsize=11, ha='center')
plt.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.1, wspace=0.03)
plt.savefig('kolakoski_window.png', dpi=110, facecolor=BG)
print('saved')
