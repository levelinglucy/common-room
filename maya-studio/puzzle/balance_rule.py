"""For which (k, n) can a 'balance only' one-seat slip be pinned on a
single drummer? Guess: iff the rarer gap occurs at least 3 times."""
import sys
def euclid(k, n): return sorted({(i*n)//k for i in range(k)})
def rots(k, n):
    b = euclid(k, n); return {frozenset((x+r) % n for x in b) for r in range(n)}
def restorers(beats, k, n, rset):
    s = set(beats); out = []
    for b in beats:
        for d in (-1, 1):
            t = (b+d) % n
            if t in s: continue
            if frozenset((s-{b})|{t}) in rset: out.append(b)
    return out
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
agree = dis = 0; rows = []
for n in range(6, NMAX+1):
    for k in range(3, n-1):
        r = n % k
        if r == 0: continue
        lo = n // k
        rs = rots(k, n); seat0 = 0
        ok = False
        # by rotation symmetry, enough to test the stray on seat 0
        for rot in rs:
            for d in (-1, 1):
                home = (-d) % n
                if home not in rot or 0 in rot: continue
                beats = sorted((set(rot)-{home})|{0})
                if frozenset(beats) in rs: continue
                g = [(beats[(i+1)%k]-beats[i]) % n for i in range(k)]
                if any(x < lo or x > lo+1 for x in g): continue
                f = restorers(beats, k, n, rs)
                if f == [0]: ok = True; break
            if ok: break
        guess = min(r, k-r) >= 3
        if ok == guess: agree += 1
        else:
            dis += 1; rows.append((n, k, r, k-r, ok))
print('pairs', agree+dis, 'agree', agree, 'disagree', dis)
for row in rows[:40]: print('n k rare-counts possible', row)
