"""Even k, even m: 'two perfect halves, out of step'.

Euclid for even k and even m is one half-rhythm played twice. Build the
trap candidate: first half as it is, second half rotated by r gaps within
itself (r = 1 .. k/2 - 1). Each half is still the right rhythm; only the two
joins are wrong, and they sit half a ring apart. Is some r non-Euclid and
stuck at j = k/2 - 1? And is everything unstuck at j = k/2?
Runs well past the sims (k up to 40).
"""
import sys
from drummers import canon, euclid_gaps
from twist_exact import stuck
from seam import split

if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    tested = trapped = 0
    for k in range(4, K + 1, 2):
        for n in range(k + 2, 3 * k):
            base, minor, m = split(k, n)
            if m < 2 or m % 2:
                continue
            E = euclid_gaps(k, n)
            h = k // 2
            # a Euclid rotation that is exactly half-periodic
            g = None
            for s in range(k):
                c = list(E[s:] + E[:s])
                if c[:h] == c[h:]:
                    g = c
                    break
            assert g is not None
            found = None
            for r in range(1, h):
                second = g[h:]
                cand = g[:h] + second[r:] + second[:r]
                if canon(tuple(cand)) == E:
                    continue
                if stuck(cand, h - 1, n):
                    found = (r, ''.join(map(str, cand)))
                    break
            tested += 1
            trapped += found is not None
            print(f"k={k:2d} n={n:2d} m={m:2d}: halves-out-of-step stuck at j=k/2-1: {found}", flush=True)
    print(f"trapped {trapped} of {tested} even-even cases")
