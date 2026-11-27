"""Solve One beat off from the PNG alone: find yellow dots, fit each ring's circle, read seats."""
import sys, math
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.cluster.hierarchy import fcluster, linkage
import one_beat_off as o

for src in sys.argv[1:]:
    a = np.asarray(Image.open(src + '.png').convert('RGB')).astype(int)
    m = (abs(a[..., 0] - 242) < 40) & (abs(a[..., 1] - 193) < 40) & (abs(a[..., 2] - 78) < 50)
    lab, n = ndimage.label(m)
    cents = np.array(ndimage.center_of_mass(m, lab, range(1, n + 1)))
    sizes = np.array(ndimage.sum(m, lab, range(1, n + 1)))
    cents = cents[sizes > 30]
    # find the rings: k-means for each plausible ring count, keep the count whose
    # clusters all fit one circle best (no layout knowledge used)
    from scipy.cluster.vq import kmeans2
    def fit(p):
        y, x = p[:, 0], p[:, 1]
        sol = np.linalg.lstsq(np.c_[x, y, np.ones(len(x))], x ** 2 + y ** 2, rcond=None)[0]
        cx, cy = sol[0] / 2, sol[1] / 2
        r = np.hypot(x - cx, y - cy)
        return cx, cy, r.mean(), r.std()
    best = None
    for K in range(4, 14):
        for seed in range(20):
            _, cl = kmeans2(cents, K, seed=seed, minit='++')
            if len(set(cl)) < K or min(np.bincount(cl)) < 4: continue
            for _ in range(10):  # refine: move each dot to the circle it sits on best
                fits = [fit(cents[cl == c]) for c in range(K)]
                d = np.array([abs(np.hypot(cents[:, 1] - f[0], cents[:, 0] - f[1]) - f[2]) for f in fits])
                new = d.argmin(0)
                if (new == cl).all() or len(set(new)) < K or min(np.bincount(new, minlength=K)) < 4: break
                cl = new
            fits = [fit(cents[cl == c]) for c in range(K)]
            radii = [f[2] for f in fits]
            score = max(f[3] for f in fits) + (max(radii) - min(radii))
            if best is None or score < best[0]: best = (score, K, cl)
    cl = best[2] + 1
    print('  ring count chosen', best[1], 'score', round(best[0], 2))
    rings = []
    for c in sorted(set(cl)):
        p = cents[cl == c]
        y, x = p[:, 0], p[:, 1]
        sol = np.linalg.lstsq(np.c_[x, y, np.ones(len(x))], x ** 2 + y ** 2, rcond=None)[0]
        cx, cy = sol[0] / 2, sol[1] / 2
        raw = [((math.atan2(xx - cx, -(yy - cy))) % (2 * math.pi)) / (2 * math.pi) * 26 for yy, xx in p]
        err = max(abs(r - round(r)) for r in raw)
        seats = sorted({round(r) % 26 for r in raw})
        rings.append((round(cy / 200), cx, seats, len(p), err))
    rings.sort(key=lambda r: (r[0], r[1]))
    print(src, 'dots', len(cents), 'rings', len(rings), 'k', [r[3] for r in rings],
          'max angle error (seats)', round(max(r[4] for r in rings), 3))
    print('  solved from pixels:', o.solve([{'beats': r[2]} for r in rings]))
