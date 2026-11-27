"""Why the 3 shows up: a guess from the quadratic field, tested.

The q = 3 one-die cases are exactly primes n = 5 (mod 8) with 2 a primitive root
(checked: every one in dice2_N30000.json is 5 mod 8). Then:
  cut by 3  <=>  1 + zeta is a cube in F_{2^(n-1)}
            <=>  its norm down to F_4 is 1
  norm to F_4 = prod over quadratic residues a of (1 + zeta^a)
              = A mod 2,   A = prod_{a in QR} (1 - zeta^a) = sqrt(n) * eps^(-h)  (Dirichlet)
  2 is inert in Q(sqrt n) for n = 5 mod 8, residue field F_4, sqrt(n) = 1 + 2*eta = 1 mod 2.
So the guess:  cut by 3  <=>  eps^h = 1 (mod 2)
            <=>  eps in Z[sqrt n]   or   3 | h,
where eps = fundamental unit and h = class number of Q(sqrt n).
(If eps = (a + b sqrt n)/2 with a, b odd, eps mod 2 is a cube root of 1 in F_4.)

This script computes eps (Pell via continued fraction of sqrt n, then a cube-root test),
h (analytic class number formula, rounded and checked), and the cut (Dpow), and compares.
"""
import sys, json, time, math
import numpy as np
from fast import Dpow, ord2, h_minus1, small_primes

def pell(n):
    """Smallest x + y sqrt n > 1 with x^2 - n y^2 = +-1 (continued fraction of sqrt n)."""
    a0 = math.isqrt(n)
    m, d, a = 0, 1, a0
    p0, p1 = 1, a0
    q0, q1 = 0, 1
    while p1 * p1 - n * q1 * q1 not in (1, -1):
        m = d * a - m
        d = (n - m * m) // d
        a = (a0 + m) // d
        p0, p1 = p1, a * p1 + p0
        q0, q1 = q1, a * q1 + q0
    return p1, q1

def icbrt_solve(x2):
    """Integer a > 0 with a^3 + 3a = x2, or None."""
    lo, hi = 0, 1
    while hi ** 3 + 3 * hi < x2:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** 3 + 3 * mid < x2:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo ** 3 + 3 * lo == x2 else None

def unit(n):
    """Return (in_Z_sqrt_n, log eps)."""
    x, y = pell(n)
    assert x * x - n * y * y == -1, n  # prime n = 1 mod 4: norm -1
    logeps0 = math.log(x) + math.log1p(y * math.sqrt(n) / x) if x < 10 ** 300 else \
        (len(str(x)) - 20) * math.log(10) + math.log(int(str(x)[:20]) + 0.5) + math.log(2)
    # eps0 = eps^3 with eps half-integral  <=>  trace a of eps solves a^3 + 3a = 2x (norm -1)
    a = icbrt_solve(2 * x)
    if a is not None:
        assert a % 2 == 1, n
        return False, logeps0 / 3
    return True, logeps0

def classno(n, logeps):
    a = np.arange(1, (n - 1) // 2 + 1)
    chi = -np.ones(n, dtype=np.int8)
    chi[(np.arange(1, n, dtype=np.int64) ** 2) % n] = 1
    s = -(chi[a].astype(float) * np.log(np.sin(np.pi * a / n))).sum()
    hf = s / logeps
    h = round(hf)
    return h, abs(hf - h)

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    t0 = time.time()
    rows, agree, worst = [], 0, 0.0
    for n in small_primes(N):
        if n % 8 != 5 or ord2(n) != n - 1:
            continue
        h2 = h_minus1(n)
        E = n * (2 ** h2 - 1)
        assert E % 3 == 0
        cut = Dpow(3, E // 3, n) == 3
        inZ, le = unit(n)
        h, err = classno(n, le)
        worst = max(worst, err)
        guess = inZ or h % 3 == 0
        agree += (guess == cut)
        rows.append(dict(n=n, cut=int(cut), eps_in_Z=int(inZ), h=h, guess=int(guess)))
        if guess != cut:
            print("MISMATCH", rows[-1], flush=True)
    k = len(rows)
    c = sum(r["cut"] for r in rows)
    z = sum(r["eps_in_Z"] for r in rows)
    h3 = sum(1 for r in rows if r["h"] % 3 == 0)
    both = sum(1 for r in rows if r["h"] % 3 == 0 and r["eps_in_Z"])
    h3_notZ = sum(1 for r in rows if r["h"] % 3 == 0 and not r["eps_in_Z"])
    out = [
        f"primes n = 5 mod 8, 2 primitive, n < {N}: {k}  ({time.time()-t0:.0f}s)",
        f"guess (eps in Z[sqrt n] or 3 | h) agrees with the cut in {agree}/{k}",
        f"worst class-number rounding error {worst:.2e}",
        f"cut by 3: {c}/{k} = {c/k:.3f}",
        f"  eps in Z[sqrt n]: {z}/{k} = {z/k:.3f}",
        f"  3 | h: {h3}/{k} = {h3/k:.3f}  (of these, eps in Z: {both}; eps half-integral: {h3_notZ})",
        f"  cuts coming only from 3 | h: {h3_notZ}",
        "first rows: " + ", ".join(f"{r['n']}{'*' if r['cut'] else ''}(h={r['h']},{'Z' if r['eps_in_Z'] else 'half'})" for r in rows[:16]),
    ]
    print("\n".join(out))
    open(f"units_N{N}_output.txt", "w").write("\n".join(out) + "\n")
    json.dump(rows, open(f"units_N{N}.json", "w"))
