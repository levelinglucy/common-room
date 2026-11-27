"""Bulgarian solitaire: full state graph for each n.
usage: python3 bulgarian.py NMAX
For each n prints: #partitions, cycles (lengths), max transient (moves to reach a cycle),
largest basin share, orphan share (no predecessor), and checks guesses 1, 2, 4.
"""
import sys
from math import gcd

def partitions(n, maxp=None):
    if maxp is None:
        maxp = n
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxp), 0, -1):
        for rest in partitions(n - p, p):
            yield (p,) + rest

def move(lam):
    new = [x - 1 for x in lam if x > 1]
    new.append(len(lam))
    new.sort(reverse=True)
    return tuple(new)

def necklaces(L, r):
    # number of binary necklaces of length L with r ones (Burnside)
    from math import comb
    tot = 0
    for d in range(1, L + 1):
        if L % d == 0 and r % (L // d) == 0:
            # rotation by L/d positions... use standard formula over divisors of gcd
            pass
    g = gcd(L, r)
    def phi(m):
        res, x, p = m, m, 2
        while p * p <= x:
            if x % p == 0:
                while x % p == 0:
                    x //= p
                res -= res // p
            p += 1
        if x > 1:
            res -= res // x
        return res
    for d in range(1, g + 1):
        if g % d == 0:
            tot += phi(d) * comb(L // d, r // d)
    return tot // L

def analyse(n):
    P = list(partitions(n))
    nxt = {lam: move(lam) for lam in P}
    # find cycles
    state = {}
    cyc_id = {}
    cycles = []
    for s in P:
        path = []
        x = s
        while x not in state:
            state[x] = 1
            path.append(x)
            x = nxt[x]
        if state[x] == 1 and x not in cyc_id:
            # new cycle found starting at x
            c = [x]
            y = nxt[x]
            while y != x:
                c.append(y)
                y = nxt[y]
            for z in c:
                cyc_id[z] = len(cycles)
            cycles.append(c)
        for z in path:
            state[z] = 2
    # transient depth and basin
    depth = {}
    basin_of = {}
    for z in cyc_id:
        depth[z] = 0
        basin_of[z] = cyc_id[z]
    def get(s):
        stack = []
        x = s
        while x not in depth:
            stack.append(x)
            x = nxt[x]
        d, b = depth[x], basin_of[x]
        for z in reversed(stack):
            d += 1
            depth[z] = d
            basin_of[z] = b
    for s in P:
        get(s)
    maxd = max(depth.values())
    deepest = [s for s in P if depth[s] == maxd]
    sizes = [0] * len(cycles)
    for s in P:
        sizes[basin_of[s]] += 1
    has_parent = set(nxt.values())
    orphans = sum(1 for s in P if s not in has_parent)
    # rule check for orphans: parent iff max part >= len - 1
    rule_ok = all((s in has_parent) == (s[0] >= len(s) - 1) for s in P)
    return dict(n=n, P=len(P), cycles=cycles, maxd=maxd, deepest=deepest,
                sizes=sizes, orphans=orphans, rule_ok=rule_ok)

def tri_k(n):
    k = 0
    while (k + 1) * (k + 2) // 2 <= n:
        k += 1
    return k, n - k * (k + 1) // 2

if __name__ == '__main__':
    NMAX = int(sys.argv[1])
    print('n p(n) k r #cyc cyclens(set) necklace maxT k^2-k bigbasin% orphan% rule deepest_example')
    for n in range(1, NMAX + 1):
        a = analyse(n)
        k, r = tri_k(n)
        lens = sorted(set(len(c) for c in a['cycles']))
        neck = necklaces(k + 1, r) if r > 0 else 1
        big = 100 * max(a['sizes']) / a['P']
        print(n, a['P'], k, r, len(a['cycles']), lens, neck, a['maxd'], k * k - k,
              f"{big:.1f}", f"{100*a['orphans']/a['P']:.1f}", a['rule_ok'],
              a['deepest'][0], len(a['deepest']), flush=True)
