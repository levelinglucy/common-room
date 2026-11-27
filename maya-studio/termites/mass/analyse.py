# Pool the centre-of-mass tracks; MSD vs lag, D, hop prediction, scaling fit.
import numpy as np, glob, re, sys

def load(fn, tmin=1_000_000):
    a = np.loadtxt(fn, comments='#')
    a = a[a[:, 0] >= tmin]
    return a

def group(tag):
    fs = sorted(glob.glob(f'runs/{tag}_s*.txt'))
    return [load(f) for f in fs if load(f).shape[0] > 10]

def stats(runs, every=100_000, lags=(1, 2, 4, 8, 16, 32, 64)):
    out = {}
    for lag in lags:
        m = []
        per = []
        for a in runs:
            xy = a[:, 1:3]
            if len(xy) > lag:
                d = ((xy[lag:] - xy[:-lag]) ** 2).sum(1)
                m.extend(d); per.append(d.mean())
        out[lag] = (np.mean(m), np.std(per) / np.sqrt(len(per)) if len(per) > 1 else np.nan)
    # rate and hop^2 from cumulative counters
    rates, h2 = [], []
    for a in runs:
        dt = a[-1, 0] - a[0, 0]
        nd = a[-1, 3] - a[0, 3]
        rates.append(nd / dt); h2.append((a[-1, 4] - a[0, 4]) / nd)
    return out, np.mean(rates), np.mean(h2)

if __name__ == '__main__':
    rows = []
    tags = sys.argv[1:] or sorted({re.sub(r'_s\d+\.txt$', '', f.split('/')[-1]) for f in glob.glob('runs/*.txt')})
    for tag in tags:
        runs = group(tag)
        if not runs: continue
        M = int(re.findall(r'_M(\d+)', tag)[0])
        out, rate, h2 = stats(runs)
        every = 100_000
        # D from lags 4..32 (slope through origin)
        lg = np.array([4, 8, 16, 32]); ms = np.array([out[l][0] for l in lg])
        D = (ms @ lg) / (lg @ lg) / (4 * every)
        Dhop = rate * h2 / (4 * M * M)
        nlen = np.mean([len(a) for a in runs])
        print(f'{tag:22s} runs {len(runs):2d} len {nlen*0.1:.1f}M  rate {rate:.4f}/tick  hop2 {h2:7.1f}  hop2/M {h2/M:.3f}  D {D:.3e}  Dhop {Dhop:.3e}  ratio {D/Dhop:.2f}')
        print('    MSD:', '  '.join(f'{l*0.1:.1f}M {out[l][0]:.1f}+-{out[l][1]:.1f}' for l in out))
        rows.append((tag, M, rate, h2, D, Dhop))
    np.save('summary.npy', np.array(rows, dtype=object), allow_pickle=True)
