"""Exact uniqueness check for 4-digit Kaprekar at B = 5*2^m, in O(B) starts instead of O(B^2).

Off the 'correction' states, the gap map is exactly z -> |2z - B| on each gap, then sorted
(checked below). With w = B - z that is doubling mod 2B up to sign. For 2B = 5*2^(m+1) the
only periodic residues are multiples of 2^(m+1), i.e. gaps in {B/5, 3B/5} (or B, impossible).
So any cycle other than the fixed point (3B/5, B/5) must pass through a correction state:
  y == 0, or the two digit-pairs interleave: | |2x-B| - |2y-B| | < 2.
Iterate every correction state forward; if all reach the fixed point, it is unique.
"""
import sys
import numpy as np
from ladder import K


def Kvec(x, y, B):
    a = np.where(y >= 1, x, x - 1)
    b = np.where(y >= 1, B - x, B - 1)
    c = np.where(y >= 1, y - 1, B - 1)
    d = np.where(y >= 1, B - 1 - y, B - x)
    D = np.sort(np.stack([a, b, c, d]), axis=0)
    return D[3] - D[0], D[2] - D[1]


def correction_states(B):
    xs, ys = [], []
    x = np.arange(1, B)
    xs.append(x); ys.append(np.zeros_like(x))
    for y in range(1, B):
        s2 = abs(2 * y - B)
        for s1 in range(max(0, s2 - 1), s2 + 2):
            for x in {(B + s1) // 2, (B - s1 + 1) // 2} if False else set():
                pass
            # x with |2x - B| == s1
            for x in ((B + s1), (B - s1)):
                if x % 2 == 0:
                    xv = x // 2
                    if y <= xv <= B - 1:
                        xs.append(np.array([xv])); ys.append(np.array([y]))
    return np.concatenate(xs).astype(np.int64), np.concatenate(ys).astype(np.int64)


def check(m, steps=None):
    B = 5 * 2 ** m
    x, y = correction_states(B)
    n0 = len(x)
    steps = steps or (8 * m + 60)
    fx, fy = 3 * B // 5, B // 5
    for _ in range(steps):
        x, y = Kvec(x, y, B)
    bad = ~((x == fx) & (y == fy))
    return B, n0, int(bad.sum()), (list(zip(x[bad][:3].tolist(), y[bad][:3].tolist())))


if __name__ == '__main__':
    # 1) the tent claim, exactly, on random non-correction states
    rng = np.random.default_rng(1)
    for B in [20, 37, 160, 1000, 1280]:
        for _ in range(20000):
            x = int(rng.integers(1, B)); y = int(rng.integers(1, x + 1))
            if abs(abs(2 * x - B) - abs(2 * y - B)) >= 2:
                t = sorted([abs(2 * x - B), abs(2 * y - B)], reverse=True)
                assert K(x, y, B) == tuple(t), (B, x, y)
    print('tent claim holds off the correction states')
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    for m in range(0, M + 1):
        B, n0, nbad, ex = check(m)
        verdict = 'UNIQUE' if nbad == 0 else f'rival ({nbad} correction states stay off the fixed point, e.g. {ex})'
        print(f'm={m:2d} B={B:>8d}  correction states {n0:>8d}  {verdict}', flush=True)
