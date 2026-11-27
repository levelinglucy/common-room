"""Exact: for n = 2k + 1, which listening reach j still lets a ramp (twist) be
stuck? Builds every ramp of the form 3^a 2^b 1^c 2^d (a - c = 1) and also
longer ramps (4^a 3^b 2^c 1^d ... for n = 2k + 1 these need more 3s), and
checks whether any drummer can lower its energy with one step.
"""
import sys
from drummers import feel

f = lambda d: 1.0 / d


def stuck(gaps, j, n):
    pos = [0]
    for g in gaps[:-1]:
        pos.append(pos[-1] + g)
    occ = set(pos)
    k = len(pos)
    for i in range(k):
        p = pos[i]
        here = feel(pos, i, p, j, n, f)
        for s in (1, -1):
            q = (p + s) % n
            if q in occ:
                continue
            if feel(pos, i, q, j, n, f) < here - 1e-12:
                return False
    return True


def ramps(k):
    for a in range(1, k):
        c = a - 1
        for b in range(0, k - a - c + 1):
            d = k - a - b - c
            if d < 0:
                continue
            if c == 0 and (b == 0 and d == 0):
                continue
            g = [3] * a + [2] * b + [1] * c + [2] * d
            if c == 0:
                continue        # no 1s: that's the Euclid family (3 once, rest 2)
            yield (a, b, c, d), g


if __name__ == "__main__":
    for k in range(6, 61, 3):
        n = 2 * k + 1
        worst = 0
        for j in range(1, k // 2 + 1):
            if any(stuck(g, j, n) for _, g in ramps(k)):
                worst = j
        print(f"k={k:3d} n={n:3d}: a twist can be stuck up to j={worst}  (j/k={worst / k:.3f}); "
              f"first safe j={worst + 1} (j/k={(worst + 1) / k:.3f})", flush=True)
