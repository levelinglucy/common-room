"""Kaprekar's routine in any base and digit count.

K(n): sort the d digits (leading zeros kept) descending -> a, ascending -> b, return a - b.
K depends only on the multiset of digits, so we iterate over multisets.
"""
from itertools import combinations_with_replacement
import sys, json


def digits_of(n, base, d):
    out = []
    for _ in range(d):
        out.append(n % base)
        n //= base
    return out


def K(n, base, d):
    ds = sorted(digits_of(n, base, d))
    lo = 0
    for x in ds:
        lo = lo * base + x
    hi = 0
    for x in reversed(ds):
        hi = hi * base + x
    return hi - lo


def K_ms(ms, base):
    """ms: sorted ascending tuple of digits."""
    lo = 0
    for x in ms:
        lo = lo * base + x
    hi = 0
    for x in reversed(ms):
        hi = hi * base + x
    return hi - lo


def attractors(base, d):
    """Return list of cycles (as tuples of numbers, rotated to start at min) reached
    from non-repdigit inputs, with the number of multisets falling into each, and the
    max steps to reach a cycle."""
    key = lambda n: tuple(sorted(digits_of(n, base, d)))
    memo = {}  # multiset -> cycle id
    cycles = {}
    counts = {}
    maxsteps = 0
    for ms in combinations_with_replacement(range(base), d):
        if ms[0] == ms[-1]:
            continue  # repdigit -> 0
        path = []
        seen = {}
        n = K_ms(ms, base)
        steps = 1
        cyc = None
        while True:
            k = key(n)
            if k in memo:
                cyc = memo[k]
                break
            if n in seen:
                # found cycle starting at seen[n]
                c = path[seen[n]:]
                m = c.index(min(c))
                c = tuple(c[m:] + c[:m])
                cyc = cycles.setdefault(c, c)
                break
            seen[n] = len(path)
            path.append(n)
            n = K(n, base, d)
            steps += 1
        memo[ms] = cyc
        counts[cyc] = counts.get(cyc, 0) + 1
        maxsteps = max(maxsteps, steps)
    return counts, maxsteps


def to_base(n, base, d):
    al = '0123456789abcdefghijklmnopqrstuvwxyz'
    ds = list(reversed(digits_of(n, base, d)))
    if base <= 36:
        return ''.join(al[x] for x in ds)
    return '(' + '.'.join(str(x) for x in ds) + ')'


if __name__ == '__main__':
    maxb = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    maxd = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    res = {}
    for d in range(2, maxd + 1):
        for b in range(2, maxb + 1):
            counts, ms = attractors(b, d)
            cyc = sorted(counts.items(), key=lambda kv: -kv[1])
            desc = [([to_base(x, b, d) for x in c], cnt) for c, cnt in cyc]
            res[f'{b},{d}'] = {'cycles': desc, 'maxsteps': ms}
            single = len(cyc) == 1 and len(cyc[0][0]) == 1
            tag = 'SINGLE FIXED POINT ' + desc[0][0][0] if single else f'{len(cyc)} attractors'
            print(f'base {b:2d} d={d}: {tag}', flush=True)
    json.dump(res, open(f'/home/sprite/maya-studio/kaprekar/census_b{maxb}_d{maxd}.json', 'w'), indent=1)
