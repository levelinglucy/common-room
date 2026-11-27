"""Check the rotating-ring law for Ducci periods, n = 3..80.

Odd n, h = smallest h with 2^h = -1 (mod n): predict P = n (2^h - 1).
Odd n with no such h, e = ord_n(2): predict P | 2^e - 1 (report exact P).
n = 2^k m (m odd): predict P(n) = 2^k P(m), with P(1) = 1.
Also check directly: on the cycle, 2^h - 1 steps = rotate by one seat.
Random integer starts confirm the binary period for n <= 40 (periods <= 3e4).
"""
import random, json
from ducci import binary_period_from, mulmod, run

def ordm(n):
    e, v = 1, 2 % n
    while v != 1:
        v = v * 2 % n; e += 1
    return e

def minus_one_h(n):
    h, v = 1, 2 % n
    for _ in range(n):
        if v == n - 1:
            return h
        v = v * 2 % n; h += 1
    return None

def odd_part(n):
    k = 0
    while n % 2 == 0:
        n //= 2; k += 1
    return k, n

rows, bad = [], 0
random.seed(7)
Pcache = {1: 1}
for n in range(3, 81):
    tail, P = binary_period_from(1, n)
    k, m = odd_part(n)
    if m == 1:
        pred, law = 1, "power of 2: dies"
    elif k > 0:
        pred, law = 2**k * Pcache[m], f"2^{k} x P({m})"
    else:
        h = minus_one_h(n)
        if h:
            pred, law = n * (2**h - 1), f"n(2^{h}-1)"
            # direct rotation check on the cycle
            mask = (1 << n) - 1
            a = 1
            for _ in range(tail): a = mulmod(a, 3, n)
            b = a
            for _ in range(2**h - 1): b = mulmod(b, 3, n)
            rot = ((a >> 1) | (a << (n - 1))) & mask  # x^{-1} a
            assert b == rot, n
        else:
            e = ordm(n)
            pred, law = (P if (2**e - 1) % P == 0 else -1), f"divides 2^{e}-1"
    Pcache[n] = P
    ok = (pred == P)
    rnd = None
    if n <= 40 and P <= 30000:
        ps = set(run(tuple(random.randint(0, 10**5) for _ in range(n)))[1] for _ in range(8))
        rnd = max(ps)
        ok = ok and rnd == P
    bad += (not ok)
    rows.append(dict(n=n, P=P, tail=tail, law=law, pred=pred, random_max=rnd, ok=ok))
    print(f"{n:3d} P={P:<14d} tail={tail:<3d} law={law:<18s} pred={pred:<14d} rand={rnd} {'OK' if ok else 'MISMATCH'}")
print("mismatches:", bad)
json.dump(rows, open("verify_table.json", "w"), indent=1)
