"""Record every move of a drummers-on-a-ring run, so it can be played bar by bar.

Same model as ../drummers.py (1/d repulsion, j nearest per side, one-slot steps
into empty neighbours, random order), but logs the positions after each move.
"""
import random, sys, json
sys.path.insert(0, '..')
from drummers import feel, gaps_of, canon, euclid_gaps


def run_log(start, n, j, rng, max_sweeps=2000):
    pos = list(start)
    k = len(pos)
    occupied = set(pos)
    log = [tuple(pos)]
    movers = [None]
    f = lambda d: 1.0 / d
    for sweep in range(max_sweeps):
        moved = False
        order = list(range(k))
        rng.shuffle(order)
        for i in order:
            p = pos[i]
            here = feel(pos, i, p, j, n, f)
            best, bestp = here, p
            steps = [1, -1]
            rng.shuffle(steps)
            for s in steps:
                q = (p + s) % n
                if q in occupied:
                    continue
                e = feel(pos, i, q, j, n, f)
                if e < best - 1e-12:
                    best, bestp = e, q
            if bestp != p:
                occupied.discard(p); occupied.add(bestp)
                pos[i] = bestp
                moved = True
                log.append(tuple(pos)); movers.append(i)
        if not moved:
            return log, movers
    return log, movers


def is_euclid(pos, n):
    k = len(pos)
    return canon(gaps_of(sorted(pos), n)) == euclid_gaps(k, n)


if __name__ == '__main__':
    k, n, jlo, jhi, tries = map(int, sys.argv[1:6])
    found = []
    for seed in range(tries):
        rng = random.Random(seed)
        start = sorted(rng.sample(range(n), k))
        lo, _ = run_log(start, n, jlo, random.Random(1000 + seed))
        hi, _ = run_log(start, n, jhi, random.Random(2000 + seed))
        if (not is_euclid(lo[-1], n)) and is_euclid(hi[-1], n):
            found.append((seed, len(lo) - 1, len(hi) - 1, gaps_of(sorted(lo[-1]), n)))
    print(f'k={k} n={n} j={jlo} stuck & j={jhi} euclid: {len(found)}/{tries}; euclid gaps {euclid_gaps(k, n)}')
    for s in found[:8]:
        print('  seed', s[0], 'moves lo', s[1], 'hi', s[2], 'stuck gaps', s[3])
