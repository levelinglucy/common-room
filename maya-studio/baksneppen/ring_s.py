import numpy as np
a = np.loadtxt('runs/R31_N8000_p0_runs.txt'); b = np.loadtxt('runs/R32_N8000_p0_runs.txt')
f = a[:, 0]; S = (a[:, 1] + b[:, 1]) / (a[:, 2] + b[:, 2]); n = a[:, 2] + b[:, 2]
for i in range(0, 80, 4):
    print('%.3f  <s>=%10.1f  n=%d' % (f[i], S[i], n[i]))
fc = 0.66702
for lo, hi in ((0.45, 0.64), (0.55, 0.645), (0.60, 0.65)):
    m = (f > lo) & (f < hi)
    g, lA = np.polyfit(np.log(fc - f[m]), np.log(S[m]), 1)
    print('fit %.2f-%.3f: gamma %.3f A %.3f' % (lo, hi, -g, np.exp(lA)))
np.save('runs/ring_s.npy', np.c_[f, S, n])
