"""Bulgarian solitaire, 18 Nov 3:40 PM: why does a staircase family tie the all-ones pile
at n = T_k + k/2 (k even)?
usage: python3 tie_trace.py N K
Prints the deepest starts, which cycle each lands in, and the 'excess energy' profile
(diagonal energy above the cycle minimum) along each trip.
Energy: card in row i (pile index, piles sorted big first), column j sits on diagonal i+j.
A move keeps every card's diagonal if the new pile goes on top; only re-sorting lowers it.
"""
import sys
from collections import Counter
sys.path.insert(0, '/home/sprite/maya-studio/solitaire')
from bulgarian import partitions, move


def depth_all(n):
    P = list(partitions(n))
    nxt = {p: move(p) for p in P}
    oncyc = set()
    done = set()
    for s in P:
        if s in done:
            continue
        path = []
        pos = {}
        x = s
        while x not in pos and x not in done:
            pos[x] = len(path)
            path.append(x)
            x = nxt[x]
        if x in pos:
            oncyc.update(path[pos[x]:])
        done.update(path)
    d = {c: 0 for c in oncyc}
    for s in P:
        stack = []
        x = s
        while x not in d:
            stack.append(x)
            x = nxt[x]
        base = d[x]
        for y in reversed(stack):
            base += 1
            d[y] = base
    return d, nxt, oncyc


def energy(p):
    return sum(i * x + x * (x - 1) // 2 for i, x in enumerate(p))


def unsorted_move(p):
    """new pile on top, no sorting (keeps diagonals)."""
    return [len(p)] + [x - 1 for x in p]


def cyc_of(x, nxt, oc):
    while x not in oc:
        x = nxt[x]
    c = [x]
    y = nxt[x]
    while y != x:
        c.append(y)
        y = nxt[y]
    return min(c), len(c)


def main():
    n, k = int(sys.argv[1]), int(sys.argv[2])
    r = n - k * (k + 1) // 2
    d, nxt, oc = depth_all(n)
    M = max(d.values())
    Emin = sum(t * (t + 1) for t in range(k)) + r * k
    ones = tuple([1] * n)
    deep = sorted(p for p in d if d[p] == M and p != ones)
    print(f'n={n} k={k} r={r} maxT={M} n-k={n-k} Emin={Emin} ties(excl. ones)={len(deep)}')
    print('all-ones lands in', cyc_of(ones, nxt, oc))
    print('tie family lands in', dict(Counter(cyc_of(p, nxt, oc) for p in deep)))
    print('basins', dict(Counter(cyc_of(p, nxt, oc) for p in d)))
    shown = [ones] + deep[:3]
    for p in shown:
        x = p
        prof = []
        while True:
            prof.append(energy(x) - Emin)
            if x in oc:
                break
            x = nxt[x]
        print('start', p if len(p) < 16 else '1^%d' % n)
        print('   excess energy', prof)


if __name__ == '__main__':
    main()
