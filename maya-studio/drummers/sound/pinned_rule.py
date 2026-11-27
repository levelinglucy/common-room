"""Guessing the m >= 3 rule. For each odd gap with neighbouring arcs a (before) and
b (after), call it pinned if min(a, b) >= j - 1 (the m = 2 rule: can't hear a
neighbour odd gap from its edge drummers) OR |a - b| <= 1 (pushed about equally
from both sides). Prediction: stuck iff every odd gap is pinned.
Only j <= floor(k/2) (nobody hears anyone twice).
"""
import sys
from ladder_proof_check import stuck, arcs
from itertools import combinations
sys.path.insert(0, '..')
from drummers import canon


def rows_of(k, n):
    q, rem = divmod(n, k)
    if rem <= k - rem:
        odd, m, base = q + 1, rem, q
    else:
        odd, m, base = q, k - rem, q + 1
    seen = set()
    for c in combinations(range(k), m):
        g = canon(tuple(odd if i in c else base for i in range(k)))
        if g not in seen:
            seen.add(g)
    return odd, m, base, sorted(seen)


def pinned_all(g, odd, j, tol):
    A = arcs(g, odd)
    M = len(A)
    for t in range(M):
        a, b = A[t - 1], A[t]      # arc before odd gap t, arc after it
        if not (min(a, b) >= j - 1 or abs(a - b) <= tol):
            return False
    return True


if __name__ == '__main__':
    tol = int(sys.argv[1])
    cases = [tuple(map(int, a.split('/'))) for a in sys.argv[2:]]
    TA = TD = 0
    for k, n in cases:
        odd, m, base, rows = rows_of(k, n)
        A = D = 0; bad = []
        for j in range(1, k // 2 + 1):
            for g in rows:
                p = pinned_all(g, odd, j, tol)
                s = stuck(g, j)
                if p == s:
                    A += 1
                else:
                    D += 1
                    if len(bad) < 4:
                        bad.append((j, ''.join(map(str, g)), 'stuck' if s else 'moves', arcs(g, odd)))
        TA += A; TD += D
        print(f'{k}/{n} m={m} odd={odd}: agree {A} disagree {D}', bad if bad else '')
    print('TOTAL', TA, TD)
