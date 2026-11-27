# Final branching prediction: single-seed avalanche in the dropout ring, s1(f; p) from seed1.c.
# Critical when each seed's avalanche makes on average one new seed far away:
#     2 p f s1(f; p) = 1
# No fitted parameter. Compare with measured f_c(p) (half-plateau, N = 8000).
import numpy as np, analyse as A, os
rows = []
print('p        measured  pred(single seed)  diff')
for ps in ['0.0001', '0.001', '0.003', '0.01', '0.03', '0.1', '0.2', '0.3', '0.5', '0.7', '1']:
    p = float(ps)
    meas = A.fc_of('runs/N8000_p' + ps)[0]
    if ps == '1':
        pred = 1 / 3
    else:
        fn = 'runs/seed1_p%s.txt' % ps
        if not os.path.exists(fn) or os.path.getsize(fn) == 0:
            continue
        D = np.loadtxt(fn, ndmin=2)
        f, S = D[:, 0], D[:, 1]
        g = np.log(2 * p * f * S)
        k = int(np.argmax(g > 0))
        if k == 0 or not g[k] > 0:
            pred = np.nan
        else:
            t = -g[k - 1] / (g[k] - g[k - 1]); pred = f[k - 1] + t * (f[k] - f[k - 1])
    rows.append((p, meas, pred))
    print('%-8g %.4f    %.4f             %+.4f' % (p, meas, pred, pred - meas))
np.save('runs/predict_seed.npy', np.array(rows))
