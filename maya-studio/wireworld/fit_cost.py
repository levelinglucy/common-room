"""Which work model explains how long the WireWorld computer takes between primes?"""
import numpy as np, math
d = np.loadtxt('primes_times.txt', skiprows=1, dtype=np.int64)
P, T = d[:, 0], d[:, 1]
def spf(n):
    for k in range(2, int(math.isqrt(n)) + 1):
        if n % k == 0: return k
    return n
models = {
 'n per candidate (odd)':        lambda n: [1, n],
 'trial divs to sqrt, stop at factor (odd d)': lambda n: [1, len([k for k in range(3, min(spf(n), math.isqrt(n)) + 1, 2)]) + 1],
 'repeated subtraction, odd d to sqrt, stop at factor': lambda n: [1, sum(n / k for k in range(3, min(spf(n), math.isqrt(n)) + 1, 2)) + 1],
 'trial divs to sqrt, no early stop': lambda n: [1, math.isqrt(n)],
 'trial divs up to n, stop at factor': lambda n: [1, spf(n)],
 'n^2 per candidate': lambda n: [1, n * n],
}
for cand_step in (2,):
  for name, f in models.items():
    X, y = [], []
    for i in range(1, len(P)):
        rows = [f(n) for n in range(P[i-1] + cand_step, P[i] + 1, cand_step)]
        X.append(np.sum(rows, 0)); y.append(T[i] - T[i-1])
    X, y = np.array(X, float), np.array(y, float)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    rel = np.abs(pred - y) / y
    print(f'{name:55s} coef={np.round(coef,1)}  median err {np.median(rel)*100:5.2f}%  max {rel.max()*100:5.1f}%')
# show intervals
for i in range(1, len(P)):
    print(P[i-1], '->', P[i], T[i]-T[i-1])
