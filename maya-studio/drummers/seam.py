"""Even k, even m: is the trap a seam?

When k and m are both even, the Euclidean rhythm is two copies of the same
half-rhythm, E(m/2, k/2) twice. Build the 'seam' state: keep one half of the
minority gaps where Euclid puts them and slide the other half by one gap.
Each half is locally perfect; the mistake is only visible to a drummer who
can hear across half the ring. Test: is the seam stuck for every j < k/2?
Also test odd m with the same slide (half = first floor(m/2) minority gaps).
"""
import sys
from drummers import canon, euclid_gaps
from twist_exact import stuck


def split(k, n):
    q, r = divmod(n, k)
    if r <= k - r:
        return q, q + 1, r          # base gap, minority gap, m
    return q + 1, q, k - r


def seam_state(k, n, shift=1):
    base, minor, m = split(k, n)
    P = [(i * k) // m for i in range(m)]
    Q = P[: m // 2] + [(p + shift) % k for p in P[m // 2:]]
    if len(set(Q)) < m:
        return None
    g = [base] * k
    for p in Q:
        g[p] = minor
    return g


def max_stuck_j(g, k, n):
    worst = 0
    for j in range(1, k // 2 + 1):
        if stuck(g, j, n):
            worst = j
    return worst


if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    for k in range(4, K + 1):
        for n in range(k + 2, 3 * k):
            base, minor, m = split(k, n)
            if m < 2:
                continue
            g = seam_state(k, n)
            if g is None or canon(tuple(g)) == euclid_gaps(k, n):
                print(f"k={k} n={n} m={m}: seam is Euclid or invalid")
                continue
            w = max_stuck_j(g, k, n)
            tag = "even-even" if k % 2 == 0 and m % 2 == 0 else ""
            print(f"k={k:2d} n={n:2d} m={m}: seam stuck up to j={w}, predicts jmin>={w + 1}; k/2={k // 2} {tag}", flush=True)
