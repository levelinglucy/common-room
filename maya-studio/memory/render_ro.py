"""ro_sweep -> reach_out_curve.png: idle organ reached vs hyphae alive, floor sweep, both_bt vs both_bt + reach_out."""
import re, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
F = ['0.15', '0.1', '0.07', '0.05', '0.03', '0.015']
def read(v, f):
    s = open(f'ro_sweep/{v}_{f}.txt').read()
    h = float(re.search(r'hyphae alive: ([\d.]+)', s).group(1))
    r = float(re.search(r'reached: ([\d.]+)%', s).group(1))
    return h, r
fig, ax = plt.subplots(figsize=(7.5, 5), dpi=140)
fig.patch.set_facecolor('#f6f1e7'); ax.set_facecolor('#f6f1e7')
for v, col, lab in [('both_bt', '#7a6a58', 'last thread + step back'), ('both_bt_ro', '#2f6b4f', '... + lone pairs reach out')]:
    pts = [read(v, f) for f in F]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], '-o', color=col, lw=2, label=lab)
    for f, (h, r) in zip(F, pts):
        if f in ('0.15', '0.1', '0.05'):
            ax.annotate(f'floor {f}', (h, r), textcoords='offset points', xytext=(6, -12 if v == 'both_bt' else 6), fontsize=8, color=col)
    print(v, pts)
ax.set_xlabel('hyphae alive (average)'); ax.set_ylabel('signal from io_channel reaches an idle organ, one try (%)')
ax.set_title('Keeping the body whole: a lower floor, or let lone pairs reach out', fontsize=11)
ax.grid(alpha=0.25); ax.legend(frameon=False, loc='lower right')
for s in ax.spines.values(): s.set_visible(False)
fig.text(0.01, 0.01, 'mycelium.py unchanged, demo life (3:1 habits), 40 runs x 3000 ticks per point', fontsize=7, color='#666')
fig.tight_layout(); fig.savefig('reach_out_curve.png')
