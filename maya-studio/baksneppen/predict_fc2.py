# Refined branching prediction: the ring part of an avalanche in the p-model is a ring
# process whose neighbours are refreshed only with prob 1-p (the rest went far). Measure its
# <s>_drop(f) directly (bs_drop), then solve 2 p f <s>_drop(f) = 1. No fitted parameter.
# At p = 1 this is exact: <s> = 1/(1-f) -> 2f/(1-f) = 1 -> f = 1/3.
import numpy as np, analyse as A

def solve(p, f, S):
    g = np.log(2 * p * f) + np.log(S)
    k = int(np.argmax(g > 0))
    if k == 0 or not g[k] > 0: return np.nan
    t = -g[k - 1] / (g[k] - g[k - 1])
    return f[k - 1] + t * (f[k] - f[k - 1])

R0 = np.load('runs/ring_s.npy')
print('p        measured  simple(ring <s>)  refined(dropout <s>)  refined-measured')
rows = []
for ps in ['0.00001', '0.00003', '0.0001', '0.0003', '0.001', '0.003', '0.01', '0.03', '0.1', '0.2', '0.3', '0.5', '0.7', '1']:
    p = float(ps)
    meas = A.fc_of('runs/N8000_p' + ps)[0]
    ok = np.isfinite(R0[:, 1]) & (R0[:, 2] > 1000)
    simple = solve(p, R0[ok, 0], R0[ok, 1])
    if ps == '1':
        ref = 1 / 3
    else:
        try:
            D = np.loadtxt('runs/D_N8000_p%s_runs.txt' % ps)
            ok = D[:, 2] > 1000
            ref = solve(p, D[ok, 0], D[ok, 1] / D[ok, 2])
        except OSError:
            ref = np.nan
    rows.append((p, meas, simple, ref))
    print('%-8g %.4f    %.4f            %.4f                %+.4f' % (p, meas, simple, ref, ref - meas))
np.save('runs/predict_all.npy', np.array(rows))
