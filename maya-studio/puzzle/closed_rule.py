"""Closed rule for whether a visible slip of E(k, n) is pinned on one drummer.

Descend: at each level the points are a ring of m points on N slots with gaps in
{a, a+1}. If the slip shows up as a value outside {a, a+1} at this level, decide:
  - two outliers side by side (a-1 next to a+2): pinned iff m >= 3
  - one outlier a-1 (beside a created a+1): ambiguous iff m == 2, or the level has
    exactly ONE long gap (N mod m == 1) and it sits on the outlier's far side
  - one outlier a+2 (beside a created a): ambiguous iff m == 2, or exactly ONE
    short gap (N mod m == m-1) and it sits on the outlier's far side
Otherwise (balance-only at this level) go down: the rarer gap letter becomes the
points, the m gaps the slots.
Returns (pinned, level, kind)."""
import sys
from every_slip import euclid, rots, brute_fixes

def closed(points, n, level=0):
    p = sorted(points); m = len(p)
    g = [(p[(i+1) % m] - p[i]) % n for i in range(m)]
    a, r = n // m, n % m
    out = [i for i in range(m) if not (a <= g[i] <= a+1)]
    if out:
        if len(out) == 2:
            return (m >= 3, level, 'pair')
        i = out[0]
        if m == 2:
            return (False, level, 'two points')
        lo = g[i] < a
        # which neighbour was created by the slip? it is the one holding the
        # opposite extreme value (a+1 for a-1, a for a+2) next to i and adjacent
        # through the slipped drummer; the far side is the other neighbour.
        L, R = g[(i-1) % m], g[(i+1) % m]
        partner = a+1 if lo else a
        # both neighbours may hold the partner value; the slip is ambiguous iff
        # the lone letter sits on the far side. Count lone letters in the ring:
        if lo:
            lone = (r == 1)
        else:
            lone = (r == m-1)
        if not lone:
            return (True, level, 'single')
        # with a lone letter: is the far neighbour that lone letter?  The slip
        # consumed one copy of 'partner'... decide by direct count around i
        far_ok = (L == partner) + (R == partner)
        return (far_ok < 2, level, 'single-lone')
    rare = a+1 if r <= m - r else a
    slots = [i for i in range(m) if g[i] == rare]
    return closed(set(slots), m, level+1)

def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    ag = dis = 0; bad = []
    from collections import Counter
    lv = Counter()
    for n in range(5, NMAX+1):
        for k in range(2, n-1):
            rs = rots(k, n); base = euclid(k, n); s = set(base)
            for b in base:
                for d in (-1, 1):
                    t = (b+d) % n
                    if t in s: continue
                    beats = sorted((s-{b}) | {t})
                    if frozenset(beats) in rs: continue
                    f = brute_fixes(beats, n, rs)
                    truth = len({x for x, _ in f}) == 1
                    pin, level, kind = closed(set(beats), n)
                    lv[(level, kind, pin)] += 1
                    if pin == truth: ag += 1
                    else:
                        dis += 1
                        if len(bad) < 8: bad.append((n, k, beats, sorted(f), level, kind))
    print('slips', ag+dis, 'closed rule agrees', ag, 'disagrees', dis)
    for b in bad: print('BAD', b)
    for key in sorted(lv): print(key, lv[key])

if __name__ == '__main__':
    main()
