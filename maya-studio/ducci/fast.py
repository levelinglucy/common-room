"""Fast Ducci periods for odd n via Ehrlich's Lemma 1: D^(2^i) = I + H^(2^i mod n).

E(n) = n(2^h - 1) if 2^h = -1 (mod n) ("with a -1"), else 2^m - 1, m = ord_n(2).
Ehrlich (Fib. Quart. 1990): P(n) divides E(n); for odd n up to ~165 P = E except
37, 101 (with -1) and 95, 111 (without), where P = E/3. He wrote: "I do not know
whether any deeper thing is hidden behind this divisor 3."

Here: for odd n up to N, find every reduction of E by primes q < QMAX
(test D^(E/q) on the cycle state (0,...,0,1,1), repeat). Without a full
factorisation, the reported P is exact up to primes >= QMAX.
"""
import sys, json, time

def rot(A, t, n, mask):
    t %= n
    if t == 0:
        return A
    return ((A >> t) | (A << (n - t))) & mask

def Dpow(A, r, n):
    mask = (1 << n) - 1
    t = 1 % n  # 2^i mod n
    while r:
        if r & 1:
            A ^= rot(A, t, n, mask)
        r >>= 1
        t = (t * 2) % n
    return A

def ord2(n):
    e, v = 1, 2 % n
    while v != 1:
        v = v * 2 % n; e += 1
    return e

def h_minus1(n):
    v = 2 % n
    for h in range(1, n + 1):
        if v == n - 1:
            return h
        v = v * 2 % n
    return None

def small_primes(limit):
    s = bytearray([1]) * (limit + 1); s[0] = s[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(limit + 1) if s[i]]

def period(n, primes):
    m = ord2(n)
    h = h_minus1(n)
    E = n * (2 ** h - 1) if h else 2 ** m - 1
    start = 3  # bits 0,1 set: (1,1,0,...,0), a two-ones state on the cycle
    assert Dpow(start, E, n) == start, n
    P, cut = E, []
    for q in primes:
        if P % q:
            continue
        while P % q == 0 and Dpow(start, P // q, n) == start:
            P //= q
            cut.append(q)
    return dict(n=n, m=m, h=h, E=E, P=P, cut=cut)

if __name__ == "__main__":
    N = int(sys.argv[1]); QMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    primes = small_primes(QMAX)
    rows, t0 = [], time.time()
    for n in range(3, N + 1, 2):
        r = period(n, primes)
        rows.append(r)
        if r["cut"]:
            print(f"n={n:5d} m={r['m']:5d} {'with -1, h='+str(r['h']) if r['h'] else 'without -1':16s} P = E / {r['E']//r['P']}  cut by {r['cut']}", flush=True)
    json.dump([{k: (str(v) if k in ('E', 'P') else v) for k, v in r.items()} for r in rows],
              open(f"fast_N{N}.json", "w"))
    print(f"odd n to {N}: {len(rows)} sizes, {sum(1 for r in rows if r['cut'])} with P < E; {time.time()-t0:.1f}s")
