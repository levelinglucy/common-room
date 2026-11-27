"""Exact check of the ladder rule, and its extension to m odd gaps.

Claim (proved by hand for m = 2, see ladder_proof.md): among two-valued rhythms
(every gap q or q+1), a rhythm is stuck for reach j exactly when every arc of
ordinary gaps between two consecutive odd gaps holds at least j - 1 gaps.

Here: enumerate EVERY two-valued rhythm of k drummers on n slots (up to
rotation), test stuckness directly with the simulation's own energy (feel), and
compare with the arc rule. Moves that leave the two-valued set (making a gap
q-1 or q+2) are tested too, since the sim allows them.
"""
import sys
from itertools import combinations
sys.path.insert(0, '..')
from drummers import feel, canon

f = lambda d: 1.0 / d


def stuck(gaps, j):
    n = sum(gaps); k = len(gaps)
    pos = [0]
    for g in gaps[:-1]:
        pos.append(pos[-1] + g)
    occ = set(pos)
    for i, p in enumerate(pos):
        here = feel(pos, i, p, j, n, f)
        for s in (1, -1):
            q = (p + s) % n
            if q in occ:
                continue
            if feel(pos, i, q, j, n, f) < here - 1e-12:
                return False
    return True


def arcs(gaps, odd):
    idx = [i for i, g in enumerate(gaps) if g == odd]
    k = len(gaps)
    return [((idx[(t + 1) % len(idx)] - idx[t]) % k or k) - 1 for t in range(len(idx))]


def check(k, n):
    q, rem = divmod(n, k)
    if rem == 0:
        return None
    # minority value and its count
    if rem <= k - rem:
        odd, m, base = q + 1, rem, q
    else:
        odd, m, base = q, k - rem, q + 1
    seen = set(); rows = []
    for c in combinations(range(k), m):
        g = tuple(odd if i in c else base for i in range(k))
        cg = canon(g)
        if cg in seen:
            continue
        seen.add(cg)
        rows.append(cg)
    out = []
    for j in range(1, k // 2 + 2):
        agree = disagree = 0; bad = []
        for g in rows:
            pred = min(arcs(g, odd)) >= j - 1
            real = stuck(g, j)
            if pred == real:
                agree += 1
            else:
                disagree += 1
                if len(bad) < 3:
                    bad.append((''.join(map(str, g)), 'pred' if pred else 'real', arcs(g, odd)))
        out.append((j, agree, disagree, bad))
    return m, odd, base, len(rows), out


if __name__ == '__main__':
    cases = [tuple(map(int, a.split('/'))) for a in sys.argv[1:]]
    tot_a = tot_d = 0
    for k, n in cases:
        r = check(k, n)
        if r is None:
            continue
        m, odd, base, nr, out = r
        print(f'== {k} on {n}: m = {m} odd gaps of {odd} among {base}s, {nr} rhythms')
        for j, a, d, bad in out:
            tot_a += a; tot_d += d
            print(f'  j={j}: agree {a}, disagree {d}' + (f'  e.g. {bad}' if bad else ''))
    print('TOTAL agree', tot_a, 'disagree', tot_d)
