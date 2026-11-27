"""Rauzy-style picture of K(1,3) (and other both-odd Kolakoski sequences).

Tag letter j with (symbol, parity of j). That 4-letter sequence is the fixed
point of a substitution (see ../subst.py). Project each prefix's letter-count
vector onto the left eigenvectors of the substitution matrix:
  - the complex pair gives a point in the plane (the 'ribbon'),
  - eigenvalue 1 gives a scalar that should stay bounded,
  - the Perron one gives (density-scaled) length.
Usage: python3 ribbon.py a b N   -> writes ribbon_a_b.npz and prints checks.
"""
import sys, numpy as np
sys.path.insert(0, '..')
from ref import direct

def matrix(a, b):
    L = ['ae', 'ao', 'be', 'bo']; idx = {x: i for i, x in enumerate(L)}
    M = np.zeros((4, 4))
    for x, v in (('a', a), ('b', b)):
        for par in 'eo':
            src = x + par
            sym = 'a' if par == 'e' else 'b'
            first = par  # run starts on the parity of its index (all lengths odd)
            for j in range(v):
                p = first if j % 2 == 0 else ('o' if first == 'e' else 'e')
                M[idx[sym + p], idx[src]] += 1
    return M

def main():
    a, b, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    s, _ = direct(a, b, N)
    s = np.array(s)
    tag = 2 * (s == b) + (np.arange(N) % 2)
    M = matrix(a, b)
    w, V = np.linalg.eig(M)
    Linv = np.linalg.inv(V)          # rows = left eigenvectors
    print('eigenvalues', np.round(w, 6), 'moduli', np.round(abs(w), 6))
    # prefix count vectors (prefix of length n, n = 0..N-1)
    C = np.zeros((N, 4))
    onehot = np.eye(4)[tag]
    C[1:] = np.cumsum(onehot, axis=0)[:-1]
    proj = C @ Linv.T                # coordinate along each eigen-direction
    order = np.argsort(-abs(w))
    for k in order:
        col = proj[:, k]
        print(f'eig {w[k]:.5f}: |coord| max {abs(col).max():.4f}  (n={N})')
    cplx = [k for k in range(4) if abs(w[k].imag) > 1e-9]
    one = [k for k in range(4) if abs(w[k] - 1) < 1e-9]
    z = proj[:, cplx[0]]
    e1 = proj[:, one[0]].real if one else np.zeros(N)
    # self-check: the tagged sequence really is the substitution's fixed point
    img = {}
    for i in range(4):
        img[i] = [r for r in range(4) for _ in range(int(M[r, i]))]
    # rebuild by expanding run i from tag i (order within run alternates parity)
    rebuilt = []
    for i in range(N):
        sym = 0 if i % 2 == 0 else 1
        for j in range(s[i]):
            rebuilt.append(2 * sym + ((i + j) % 2))
        if len(rebuilt) >= N: break
    ok = np.array_equal(np.array(rebuilt[:N]), tag)
    print('tagged sequence = expansion of itself:', ok)
    np.savez_compressed(f'ribbon_{a}_{b}.npz', z=z, e1=e1, tag=tag, s=s, w=w)

if __name__ == '__main__':
    main()
