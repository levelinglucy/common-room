"""Fast Kaprekar census using the difference reduction.

For sorted digits a1>=...>=ad, K = sum_i e_i (b^(d-i) - b^(i-1)), e_i = a_i - a_(d+1-i), i<=d//2.
So the state is (e_1 >= e_2 >= ... >= e_h >= 0), h = d//2, e_1 <= b-1. e_1 = 0 is a repdigit.
The middle digit (odd d) cancels.

usage: kfast.py D BMIN BMAX [STEP]
"""
import sys
import numpy as np
from itertools import combinations_with_replacement


def states(b, h):
    # non-increasing sequences e1>=...>=eh, 0<=e<=b-1
    if h == 2:
        e1, e2 = np.triu_indices(b)  # e1<=e2 pairs -> swap
        return np.stack([e2, e1], 1).astype(np.int64)
    return np.array([tuple(reversed(c)) for c in combinations_with_replacement(range(b), h)], dtype=np.int64)


def census(b, d):
    h = d // 2
    S = states(b, h)
    w = np.array([b ** (d - i) - b ** (i - 1) for i in range(1, h + 1)], dtype=object)
    n = (S.astype(object) * w).sum(1) if b ** d > 2 ** 62 else S @ np.array(w, dtype=np.int64)
    n = np.asarray(n, dtype=np.int64)
    # digits
    digs = np.empty((len(S), d), dtype=np.int64)
    m = n.copy()
    for j in range(d):
        digs[:, j] = m % b
        m //= b
    digs.sort(1)  # ascending
    E = np.stack([digs[:, d - i] - digs[:, i - 1] for i in range(1, h + 1)], 1)
    # index states
    mult = b ** np.arange(h - 1, -1, -1, dtype=np.int64)
    keyS = S @ mult
    keyE = E @ mult
    order = np.argsort(keyS)
    pos = np.searchsorted(keyS[order], keyE)
    f = order[pos]
    assert (keyS[f] == keyE).all()
    g = f.copy()
    for _ in range(22):
        g = g[g]
    C = np.unique(g)
    seen = set()
    cycles = []
    for c in C:
        if c in seen:
            continue
        cyc = [c]
        seen.add(c)
        x = f[c]
        while x != c:
            cyc.append(x)
            seen.add(x)
            x = f[x]
        cycles.append(cyc)
    # basin sizes over states with e1>0 (non-repdigit)
    cid = {}
    for k, cyc in enumerate(cycles):
        for x in cyc:
            cid[x] = k
    lab = np.array([cid[x] for x in g])
    valid = S[:, 0] > 0
    basins = np.bincount(lab[valid], minlength=len(cycles))
    out = []
    for k, cyc in enumerate(cycles):
        if basins[k] == 0:
            continue
        out.append((len(cyc), [int(n[x]) for x in cyc], int(basins[k]), tuple(S[cyc[0]])))
    return out


def show(n, b, d):
    ds = []
    for _ in range(d):
        ds.append(n % b)
        n //= b
    return '(' + '.'.join(map(str, reversed(ds))) + ')'


if __name__ == '__main__':
    d, b0, b1 = map(int, sys.argv[1:4])
    step = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    for b in range(b0, b1 + 1, step):
        out = census(b, d)
        lens = sorted(o[0] for o in out)
        tag = ''
        if len(out) == 1 and out[0][0] == 1:
            tag = '  <== UNIQUE ' + show(out[0][1][0], b, d) + (' (zero)' if out[0][1][0] == 0 else '')
        print(f'd={d} base {b}: {len(out)} attractors, lengths {lens[:12]}{"..." if len(lens) > 12 else ""}{tag}', flush=True)
