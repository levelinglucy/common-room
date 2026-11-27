"""The real m = 1 trap: three defects a third of the ring apart.

n = 2k + 1. Euclid = all gaps 2 except one 3. The stuck misses in the sims
were all 2s except one 1 and two 3s, spaced roughly a third of the way round
from each other. Build that state for every placement of the 1 and the two
3s, and find the largest reach j at which some placement is still stuck.
Compare with the simulated jmin = floor((k + 1) / 3).
"""
from twist_exact import stuck

if __name__ == "__main__":
    for k in list(range(6, 31)) + [36, 42, 48]:
        n = 2 * k + 1
        worst, where = 0, None
        for j in range(1, k // 2 + 1):
            found = None
            for x in range(1, k):
                for y in range(x + 1, k):
                    g = [2] * k
                    g[0], g[x], g[y] = 1, 3, 3
                    if stuck(g, j, n):
                        found = (x, y - x, k - y)
                        break
                if found:
                    break
            if found:
                worst, where = j, found
        print(f"k={k:2d}: three defects stuck up to j={worst}, spacing {where};"
              f" predicts jmin={worst + 1}, sims floor((k+1)/3)={(k + 1) // 3}", flush=True)
