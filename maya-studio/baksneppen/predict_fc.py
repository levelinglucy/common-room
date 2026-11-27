# Branching prediction: the far links turn each ring avalanche into a branching process.
# A ring f-avalanche lasting s steps sends ~2 p s refreshes to random far species; each lands
# below f with probability f and starts its own ring avalanche. Critical when 2 p f <s>(f) = 1.
# <s>(f) comes from the pure ring run (no fitting); compare with the measured f_c(p).
import numpy as np, analyse as A
R = np.load('runs/ring_s.npy'); f, S = R[:, 0], R[:, 1]
ok = np.isfinite(S) & (R[:, 2] > 1000)
f, S = f[ok], S[ok]
logS = np.log(S)

def solve(target_fn):
    # find f where target_fn(f) * <s>(f) = 1, by log-linear interpolation on the grid
    g = np.log(target_fn(f)) + logS
    k = int(np.argmax(g > 0))
    if k == 0: return np.nan
    t = -g[k - 1] / (g[k] - g[k - 1])
    return f[k - 1] + t * (f[k] - f[k - 1])

ps = ['0.00001', '0.00003', '0.0001', '0.0003', '0.001', '0.003', '0.01', '0.03', '0.1', '0.2', '0.3', '0.5', '0.7', '1']
print('p        measured(N8000)  predicted 2pf<s>=1   diff     predicted 2p<s>=1')
out = []
for ps_ in ps:
    p = float(ps_)
    meas = A.fc_of('runs/N8000_p' + ps_)[0]
    pr = solve(lambda x: 2 * p * x)
    pr2 = solve(lambda x: 2 * p + 0 * x)
    out.append((p, meas, pr, pr2))
    print('%-8g %.4f           %.4f               %+.4f   %.4f' % (p, meas, pr, pr - meas, pr2))
np.save('runs/predict_fc.npy', np.array(out))
