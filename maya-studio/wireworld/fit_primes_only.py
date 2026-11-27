"""Twin-prime intervals test exactly one candidate (a prime). Fit cost(p) to work models."""
import numpy as np, math
d = np.loadtxt('primes_times.txt', skiprows=1, dtype=np.int64)
P, T = list(d[:, 0]), list(d[:, 1])
pts = [(P[i], T[i] - T[i-1]) for i in range(1, len(P)) if P[i] - P[i-1] == 2 and P[i] > 5]
p = np.array([a for a, _ in pts], float); c = np.array([b for _, b in pts], float)
fl = math.floor
S = {
 'sum floor(p/d), d=2..p-1': lambda n: sum(n // k for k in range(2, n)),
 'sum floor(p/d), odd d=3..p-2': lambda n: sum(n // k for k in range(3, n - 1, 2)),
 'sum floor(p/d), d=2..sqrt': lambda n: sum(n // k for k in range(2, math.isqrt(n) + 1)),
 'sum floor(p/d), odd d=3..sqrt': lambda n: sum(n // k for k in range(3, math.isqrt(n) + 1, 2)),
 'sum floor(p/d), d while d*d<=p (d=2..)': lambda n: sum(n // k for k in range(2, math.isqrt(n) + 1)),
 'p*ln p': lambda n: n * math.log(n),
 'p': lambda n: n,
 'p^2': lambda n: n * n,
}
for name, f in S.items():
    x = np.array([f(int(n)) for n in p], float)
    for intercept in (True, False):
        X = np.c_[np.ones_like(x), x] if intercept else x[:, None]
        coef, *_ = np.linalg.lstsq(X, c, rcond=None)
        rel = np.abs(X @ coef - c) / c
        print(f'{name:42s} {"a+b*S" if intercept else "  b*S"} coef={np.round(coef,1)} max err {rel.max()*100:5.2f}%')
print(list(zip(p.astype(int), c.astype(int))))
