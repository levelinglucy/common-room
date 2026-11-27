"""Where do bands get stuck on the way to the 7-on-12 bell (and a few other timelines)?
Census of final states, up to rotation, for each listening reach j.
"""
import random, sys
from collections import Counter
sys.path.insert(0, '..')
from drummers import run, gaps_of, canon, euclid_gaps

cases = [(7, 12), (5, 8), (5, 16), (5, 12), (7, 16), (9, 16)]
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
for k, n in cases:
    e = euclid_gaps(k, n)
    print(f'== {k} on {n}: Euclid gaps {e}')
    for j in range(1, k // 2 + 1):
        c = Counter()
        for s in range(RUNS):
            pos, _ = run(k, n, j, random.Random(s * 7919 + j))
            c[canon(gaps_of(sorted(pos), n))] += 1
        top = c.most_common(4)
        print(f'  j={j}: euclid {c[e]}/{RUNS}; distinct finals {len(c)}; top ' +
              ', '.join(f'{"".join(map(str, g))} x{m}' for g, m in top))
