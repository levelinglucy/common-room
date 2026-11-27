"""Fit the gaps between primes to Fryers' program as documented on quinapalus.com:
odd candidates n; trial divisors q = 3,5,... until q divides n (q = n means prime);
each division by repeated subtraction, so about n/q passes round the inner loop.
cost(n) = alpha + beta * (#divisors tried) + gamma * (total subtraction passes)."""
import numpy as np, math
d = np.loadtxt('primes_times.txt', skiprows=1, dtype=np.int64)
P, T = d[:, 0], d[:, 1]
def qs(n):
    q = 3
    while True:
        yield q
        if n % q == 0: return
        q += 2
def feats(n, rnd):
    Q = list(qs(n))
    return [1, len(Q), sum(rnd(n, q) for q in Q)]
RND = {'floor': lambda n, q: n // q, 'ceil': lambda n, q: -(-n // q)}
for rname, rnd in RND.items():
    X, y, lab = [], [], []
    for i in range(1, len(P)):
        if P[i-1] < 5: continue   # first gap: pattern was saved part-way through testing 5
        X.append(np.sum([feats(n, rnd) for n in range(P[i-1] + 2, P[i] + 1, 2)], 0))
        y.append(T[i] - T[i-1]); lab.append((P[i-1], P[i]))
    X, y = np.array(X, float), np.array(y, float)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ coef
    print(rname, 'alpha,beta,gamma =', np.round(coef, 2), ' max |resid| =', np.abs(res).max().round(0), 'gens')
    if rname == 'ceil':
        for (a, b), yy, r in zip(lab, y, res): print(f'  {a:3d}->{b:3d}  {int(yy):8d}  resid {r:8.0f}')

# predictions beyond the data, from the ceil fit
coef_c = None
X, y = [], []
for i in range(1, len(P)):
    if P[i-1] < 5: continue
    X.append(np.sum([feats(n, RND['ceil']) for n in range(P[i-1] + 2, P[i] + 1, 2)], 0)); y.append(T[i] - T[i-1])
coef_c, *_ = np.linalg.lstsq(np.array(X, float), np.array(y, float), rcond=None)
def predict_after(p0, t0, upto):
    t, out = float(t0), []
    for n in range(p0 + 2, upto + 1, 2):
        t += np.dot(coef_c, feats(n, RND['ceil']))
        if all(n % q for q in range(3, int(n**.5) + 1, 2)): out.append((n, t))
    return out
if __name__ == '__main__':
    pr = predict_after(int(P[-1]), int(T[-1]), 110)
    print('predicted:', [(n, int(t)) for n, t in pr])
