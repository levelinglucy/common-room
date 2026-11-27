import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A = 0.8847
e = np.loadtxt('r30/envelope.tsv')
n = e[:, 0]
d = np.genfromtxt('r30/bins.tsv', names=True)
fig, ax = plt.subplots(2, 1, figsize=(11, 8), gridspec_kw={'height_ratios': [2, 1]})
m = n >= 2**12
x = np.log2(n[m])
ax[0].fill_between(x, e[m, 1] / n[m]**A, e[m, 2] / n[m]**A, color='#2b6f8f', lw=0)
for k in range(13, 31):
    ax[0].axvline(k, color='#999', lw=0.4)
    ax[0].axvline(k + np.log2(1.40), color='#d2691e', lw=0.6, ls=':')
ax[0].set_xlim(12, 30)
ax[0].set_xlabel('log2 n')
ax[0].set_ylabel('(Q(n) - n/2) / n^0.885')
ax[0].set_title("Hofstadter's Q to 2^30: the same breath every octave, quiet seam near 1.40 x 2^k (dotted)")
x2 = d['log2n']; c = d['count']; r = d['rms_d']
oc = np.floor(x2 + 1e-9)
ks, ex = [], []
prev = None
for o in range(10, 30):
    s = oc == o
    R = np.sqrt((c[s] * r[s]**2).sum() / c[s].sum())
    if prev is not None:
        ks.append(o); ex.append(np.log2(R / prev))
    prev = R
ax[1].plot(ks, ex, 'o-', color='#2b6f8f')
ax[1].set_xlabel('octave k (n from 2^k to 2^(k+1))')
ax[1].set_ylabel('growth exponent')
ax[1].set_title('spread grows like n^a; a per octave still creeping up: 0.880 at k=20, 0.8847 at k=29')
ax[1].grid(alpha=0.3)
fig.tight_layout()
fig.savefig('q_breath.png', dpi=110)
print('saved')
