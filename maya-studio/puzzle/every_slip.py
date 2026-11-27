"""Every slip, not just one.

balance_rule.py asked: does SOME balance-only slip of E(k, n) have exactly
one restoring drummer? This asks it of EVERY visible slip, and tests a
recursive explanation:

  gap word of the slipped ring over {a, a+1}
  - if a value outside {a, a+1} appears (a 'new-value' slip), the defect is
    local and the fix count follows from closed rules;
  - otherwise (balance-only) the slip is a rare letter moved one slot, so the
    question is the SAME question one level down, for the rare letters as
    points (c of them in k slots). Recurse.

Usage: python3 every_slip.py NMAX
"""
import sys
from collections import Counter


def euclid(k, n):
    return sorted({(i * n) // k for i in range(k)})


def rots(k, n):
    b = euclid(k, n)
    return {frozenset((x + r) % n for x in b) for r in range(n)}


def brute_fixes(beats, n, rset):
    """Set of (seat, dir) one-seat moves giving a maximally even ring."""
    s = set(beats)
    out = set()
    for b in beats:
        for d in (-1, 1):
            t = (b + d) % n
            if t in s:
                continue
            if frozenset((s - {b}) | {t}) in rset:
                out.add((b, d))
    return out


def is_me(points, n):
    k = len(points)
    if k <= 1:
        return True
    p = sorted(points)
    g = [(p[(i + 1) % k] - p[i]) % n for i in range(k)]
    # balanced circular word: every window of every length has sums within 1
    for L in range(1, k):
        sums = [sum(g[(i + j) % k] for j in range(L)) for i in range(k)]
        if max(sums) - min(sums) > 1:
            return False
    return True


def predict(points, n):
    """Recursive prediction of the restoring moves, as (point, dir).

    points: slipped configuration of k points on a ring of n slots.
    Rules used, no search over moves at this level except through recursion:
    """
    p = sorted(points)
    k = len(p)
    if k == 1:
        return {(p[0], -1), (p[0], 1)}
    g = [(p[(i + 1) % k] - p[i]) % n for i in range(k)]  # g[i]: p[i] -> p[i+1]
    a = n // k
    r = n % k
    out_vals = [i for i in range(k) if g[i] < a or g[i] > a + 1]
    if out_vals:
        # new-value slip: only drummers touching an outlier can help.
        # drummer p[i] sits between gap g[i-1] (left) and g[i] (right).
        # moving p[i] by +1: g[i-1]+1, g[i]-1. by -1: g[i-1]-1, g[i]+1.
        cands = set()
        for i in range(k):
            for d in (-1, 1):
                left, right = (i - 1) % k, i
                if left not in out_vals and right not in out_vals:
                    continue
                cands.add((p[i], d))
        return {(x, d) for (x, d) in cands
                if ((x + d) % n) not in points
                and is_me((set(points) - {x}) | {(x + d) % n}, n)}
    # balance-only: reduce to rare letters. Long gaps (a+1) number r,
    # short gaps number k - r. Take the rarer letter as points on k slots.
    rare_val = a + 1 if r <= k - r else a
    slots = [i for i in range(k) if g[i] == rare_val]
    sub = predict(set(slots), k)
    # a rare gap at slot i moving to slot i+1 swaps gaps i, i+1: that is
    # drummer p[i+1] moving. Gap i long -> drummer p[i+1] moves... work it
    # out by the gap change: drummer p[j] moving +1 makes g[j-1]+1, g[j]-1.
    res = set()
    for (i, d) in sub:
        j = (i + d) % k  # destination slot of the rare letter
        if d == 1:
            drum = (i + 1) % k  # between slots i and i+1
            # rare letter moves from slot i to i+1: g[i] changes by -(rare-common)
        else:
            drum = i  # between slots i-1 and i
        lo_slot, hi_slot = (drum - 1) % k, drum
        # after the swap gap lo_slot takes g[hi_slot] and vice versa
        delta = g[hi_slot] - g[lo_slot]  # g[lo] increases by delta
        res.add((p[drum], 1 if delta > 0 else -1))
    return res


def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    agree = dis = 0
    kinds = Counter()
    per_pair = {}
    bad = []
    for n in range(5, NMAX + 1):
        for k in range(2, n - 1):
            rs = rots(k, n)
            base = euclid(k, n)
            s = set(base)
            stats = Counter()
            for b in base:
                for d in (-1, 1):
                    t = (b + d) % n
                    if t in s:
                        continue
                    beats = sorted((s - {b}) | {t})
                    if frozenset(beats) in rs:
                        continue
                    a = n // k
                    gaps = [(beats[(i + 1) % k] - beats[i]) % n for i in range(k)]
                    bal = all(a <= x <= a + 1 for x in gaps)
                    f = brute_fixes(beats, n, rs)
                    pr = predict(set(beats), n)
                    if f == pr:
                        agree += 1
                    else:
                        dis += 1
                        if len(bad) < 10:
                            bad.append((n, k, beats, sorted(f), sorted(pr)))
                    nd = len({x for x, _ in f})
                    stats[(bal, nd == 1)] += 1
            per_pair[(k, n)] = stats
    print('slips', agree + dis, 'prediction agrees', agree, 'disagrees', dis)
    for row in bad:
        print('BAD', row)
    return per_pair


if __name__ == '__main__':
    main()
