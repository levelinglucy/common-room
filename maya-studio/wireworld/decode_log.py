"""Decode seglog.txt (gen + 35 head counts: 5 digits x segments a f b g e c d) into the
sequence of numbers the WireWorld computer shows, with the first generation each appears."""
import numpy as np, sys

ORDER = 'afbgecd'
DIG = {frozenset('abcdef'): '0', frozenset('bc'): '1', frozenset('abged'): '2', frozenset('abgcd'): '3',
       frozenset('fgbc'): '4', frozenset('afgcd'): '5', frozenset('afgedc'): '6', frozenset('abc'): '7',
       frozenset('abcdefg'): '8', frozenset('abcdfg'): '9', frozenset('fgedc'): '6', frozenset('abcfg'): '9'}


def decode(path='seglog.txt', thr=30):
    rows = np.loadtxt(path, dtype=np.int64, ndmin=2)
    gens, c = rows[:, 0], rows[:, 1:].reshape(-1, 5, 7)
    shown = []
    for i in range(len(gens)):
        s = ''
        for d in range(5):
            on = frozenset(ORDER[k] for k in range(7) if c[i, d, k] > thr)
            s += DIG.get(on, '?')
        shown.append(s)
    return gens, shown


def events(gens, shown, hold=4):
    """A number counts when it's read the same for `hold` samples in a row (skips write transients).
    Returns list of (number, first gen of the stable run)."""
    out = []
    i = 0
    while i < len(shown):
        j = i
        while j < len(shown) and shown[j] == shown[i]:
            j += 1
        s = shown[i]
        if j - i >= hold and '?' not in s and s != '00000':
            n = int(s)
            if not out or out[-1][0] != n:
                out.append((n, int(gens[i])))
        i = j
    return out


if __name__ == '__main__':
    g, s = decode(sys.argv[1] if len(sys.argv) > 1 else 'seglog.txt')
    ev = events(g, s)
    print('last gen', g[-1])
    for n, t in ev:
        print(n, t)
