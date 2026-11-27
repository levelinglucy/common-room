import numpy as np, glob, re, sys

def fc_of(pre):
    h = np.loadtxt(pre + '_hist.txt')[:, 1]
    m = np.loadtxt(pre + '_min.txt')[:, 1]
    plat = h[900:995].mean()
    # half-plateau crossing, linear interpolation between bins (bin b covers [b/1000,(b+1)/1000))
    k = int(np.argmax(h > plat / 2))
    x0, x1 = (k - 0.5) / 1000, (k + 0.5) / 1000
    y0, y1 = h[k - 1], h[k]
    half = x0 + (plat / 2 - y0) / (y1 - y0) * (x1 - x0)
    c = np.cumsum(m) / m.sum()
    q999 = np.searchsorted(c, 0.999) / 1000
    # fraction of species below the half point: how sharp the step is
    tot = h.sum()
    below = h[:k].sum() / tot
    # width: from 10% to 90% of plateau
    k10 = int(np.argmax(h > 0.1 * plat)); k90 = int(np.argmax(h > 0.9 * plat))
    return half, q999, below, (k90 - k10) / 1000

if __name__ == '__main__':
    rows = []
    for f in glob.glob('runs/N*_p*_hist.txt'):
        pre = f[:-9]
        mo = re.match(r'runs/N(\d+)_p([0-9.]+)', pre)
        N, p = int(mo.group(1)), float(mo.group(2))
        rows.append((N, p) + fc_of(pre))
    rows.sort()
    print('N      p       fc(half)  min99.9  frac_below  width10-90')
    for r in rows:
        print('%5d  %-6g  %.4f    %.3f    %.4f      %.3f' % r)
