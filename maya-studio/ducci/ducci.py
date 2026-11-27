"""Ducci sequences: numbers on a ring, each replaced by |a_i - a_{i+1}|.

For each ring size n: steps to enter the cycle and cycle length, over random
integer starts and (small n) every binary start. Then an algebraic prediction:
once in the cycle every entry is 0 or c, so the binary map x -> (1+x) a over
GF(2)[x]/(x^n - 1) governs it. Period = order of (1+x) acting on the
reachable part. Compare.
"""
import random, json, sys

def step(a):
    n = len(a)
    return tuple(abs(a[i] - a[(i + 1) % n]) for i in range(n))

def run(a, cap=10**6):
    seen = {}
    t = 0
    while a not in seen:
        seen[a] = t
        a = step(a)
        t += 1
        if t > cap:
            return None
    return seen[a], t - seen[a], a  # tail, period, a state on the cycle

# --- GF(2) polynomials as ints (bit i = coeff of x^i), mod x^n - 1 ---
def mulmod(p, q, n):
    r = 0
    mask = (1 << n) - 1
    while q:
        if q & 1:
            r ^= p
        q >>= 1
        p = ((p << 1) | (p >> (n - 1))) & mask  # times x, cyclic
    return r

def binary_period_from(a_bits, n, cap=10**7):
    """Iterate a -> (1+x)a on bit-ring until it repeats; return tail, period."""
    seen = {}
    t = 0
    a = a_bits
    while a not in seen:
        seen[a] = t
        a = mulmod(a, 0b11, n)
        t += 1
        if t > cap:
            return None
    return seen[a], t - seen[a]

def predicted_max_period(n):
    # worst start in binary: a = 1 (single 1). Its orbit visits the most.
    # (Every binary orbit is (1+x)^t a; period of a divides period of 1's orbit.)
    return binary_period_from(1, n)

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    random.seed(1)
    out = {}
    for n in range(3, N + 1):
        periods, tails = set(), []
        for _ in range(300):
            a = tuple(random.randint(0, 10**6) for _ in range(n))
            r = run(a)
            tails.append(r[0]); periods.add(r[1])
        exh = None
        if n <= 18:
            bp = set()
            for s in range(1 << n):
                a = tuple((s >> i) & 1 for i in range(n))
                bp.add(run(a)[1])
            exh = max(bp)
        pt, pp = predicted_max_period(n)
        out[n] = dict(max_period_random=max(periods), periods=sorted(periods),
                      max_tail_random=max(tails), max_period_binary_exhaustive=exh,
                      pred_tail=pt, pred_period=pp)
        print(n, "rand max P", max(periods), "all P", sorted(periods)[:8],
              "| bin exh", exh, "| (1+x) orbit of 1: tail", pt, "P", pp,
              "| max tail", max(tails), flush=True)
    json.dump(out, open("ducci_table.json", "w"), indent=1)
