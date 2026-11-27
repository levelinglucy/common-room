# 'All the chips in the air': carried count traces, freeze times, and D vs M.
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 3, figsize=(16, 5.2), dpi=110)
fig.patch.set_facecolor('#f6f1e7')
for a in ax: a.set_facecolor('#fbf8f2')

# A: carried count vs time, T = 300
cols = {170: '#b5523b', 180: '#d39b2a', 200: '#3d6b8c'}
for M, c in cols.items():
    a = np.loadtxt(f'scan/M{M}_s1.txt' if M != 180 else 'scan/M180_s3.txt', comments='#')
    t = a[:, 0] / 1e6; car = a[:, 5]
    keep = t <= 1.0
    ax[0].plot(t[keep], car[keep], color=c, lw=0.9, label=f'{M} chips')
    ax[0].axhline(M, color=c, ls=':', lw=1)
ax[0].axhline(150, color='#555', lw=0.8, ls='--')
ax[0].text(0.99, 151.5, 'half the termites', ha='right', va='bottom', fontsize=9, color='#555')
ax[0].set_xlabel('time (million ticks)'); ax[0].set_ylabel('termites carrying a chip')
ax[0].set_title('300 termites: about half are always carrying.\nWhen they hold every chip (dotted line), the world stops.', fontsize=10)
ax[0].legend(loc='lower right', fontsize=9, frameon=False)
ax[0].set_ylim(100, 205)

# B: time to freeze vs how far M sits above T/2, in units of sqrt(T)/2
for T, Ms, mk, col in ((300, (155, 160, 165, 170, 175, 180, 190, 200), 'o', '#3d6b8c'), (100, (50, 60, 70), 's', '#b5523b')):
    for M in Ms:
        for s in (1, 2, 3, 4):
            fn = f'scan/M{M}_s{s}.txt' if T == 300 else f'scan/T100_M{M}_s{s}.txt'
            try: a = np.loadtxt(fn, comments='#')
            except Exception: continue
            fz = np.nonzero(a[:, 5] == M)[0]
            z = (M - T / 2) / (np.sqrt(T) / 2)
            if len(fz):
                ax[1].scatter(z, a[fz[0], 0], marker=mk, color=col, s=26, alpha=0.8)
            else:
                ax[1].scatter(z, 2e7, marker='^', facecolor='none', edgecolor=col, s=40)
ax[1].scatter([], [], marker='o', color='#3d6b8c', label='300 termites')
ax[1].scatter([], [], marker='s', color='#b5523b', label='100 termites')
ax[1].scatter([], [], marker='^', facecolor='none', edgecolor='#555', label='still alive at 20M ticks')
ax[1].set_yscale('log'); ax[1].set_xlabel('chips above half the termites, in standard deviations of the carrying count')
ax[1].set_ylabel('ticks until every chip is in the air')
ax[1].set_title('The freeze gets rare fast once there are a few\nstandard deviations more chips than half the termites', fontsize=10)
ax[1].legend(fontsize=9, frameon=False, loc='upper left')

# C: diffusion constant of a lone pile vs its size
rows = np.load('summary.npy', allow_pickle=True)
for tag, M, rate, h2, D, Dh in rows:
    if tag.startswith('L128_T300') and M >= 600:
        ax[2].scatter(M, D, color='#3d6b8c', s=40)
    elif tag.startswith('L256'):
        ax[2].scatter(M, D, color='#d39b2a', marker='D', s=40)
Ms = np.array([500, 5000.])
ax[2].plot(Ms, 4.06e-5 * 1200 / Ms, color='#555', ls='--', lw=1)
ax[2].text(560, 4.06e-5 * 1200 / 560 * 1.12, 'D ~ 1/M', fontsize=9, color='#555')
ax[2].scatter([], [], color='#3d6b8c', label='128 board, 300 termites')
ax[2].scatter([], [], color='#d39b2a', marker='D', label='256 board, 1200 termites')
ax[2].set_xscale('log'); ax[2].set_yscale('log')
ax[2].set_xlabel('chips in the pile (M)'); ax[2].set_ylabel('wander rate D (cells$^2$ per tick)')
ax[2].set_title('A lone pile wanders at a rate close to 1/M', fontsize=10)
ax[2].legend(fontsize=9, frameon=False, loc='lower left')

fig.suptitle('Termites and wood chips: when there are too few chips, the termites lift them all and nobody can put one down', fontsize=12, y=1.0)
from matplotlib.ticker import NullFormatter
ax[2].yaxis.set_minor_formatter(NullFormatter()); ax[2].xaxis.set_minor_formatter(NullFormatter())
fig.tight_layout(w_pad=3)
fig.savefig('all_in_the_air.png', facecolor=fig.get_facecolor(), bbox_inches='tight')
print('saved')
