"""Check pre-registered recursive predictions with fresh sims (k > 20).

For each chosen (k, n): run the band at j = pred - 1, pred, pred + 1.
Prediction holds if j = pred - 1 misses Euclid at least once in RUNS runs
and j = pred, pred + 1 hit it every time. Also records which non-Euclid
end states turned up at pred - 1, and whether the predicted trap is among them.
"""
import sys, json, random, time
from multiprocessing import Pool
from collections import Counter
from drummers import run, gaps_of, canon, euclid_gaps

RUNS = 60


def mirror(g):
    return canon(tuple(reversed(g)))


def job(row):
    k, n, pj = row["k"], row["n"], row["pred"]
    trap = tuple(row["trap"]) if row["trap"] else None
    E = euclid_gaps(k, n)
    rng = random.Random(7919 * n + k)
    res = {}
    misses = Counter()
    for j in (pj - 1, pj, pj + 1):
        if j < 1:
            continue
        hits = 0
        for t in range(RUNS):
            pos, sw = run(k, n, j, rng)
            g = canon(gaps_of(pos, n))
            if g == E:
                hits += 1
            elif j == pj - 1:
                misses[min(g, mirror(g))] += 1
        res[j] = hits
    ok = res.get(pj - 1, 0) < RUNS and res[pj] == RUNS and res[pj + 1] == RUNS
    seen_trap = trap is not None and min(trap, mirror(trap)) in misses
    top = [("".join(map(str, g)), c) for g, c in misses.most_common(3)]
    return dict(k=k, n=n, m=row["m"], pred=pj, hits=res, ok=ok, trap_seen=seen_trap, top_misses=top)


if __name__ == "__main__":
    pred = json.load(open(sys.argv[1]))
    chosen = [tuple(map(int, s.split(","))) for s in sys.argv[2:]]
    rows = [r for r in pred["rows"] if (r["k"], r["n"]) in chosen]
    rows.sort(key=lambda r: -r["k"] * r["pred"])
    t0 = time.time()
    with Pool(8) as p:
        out = p.map(job, rows, chunksize=1)
    out.sort(key=lambda r: (r["k"], r["n"]))
    for r in out:
        print(f"k={r['k']:2d} n={r['n']:2d} m={r['m']:2d} pred {r['pred']:2d}  hits {r['hits']}  {'HOLDS' if r['ok'] else 'FAILS'}  trap seen {r['trap_seen']}  misses {r['top_misses']}")
    print(f"{sum(r['ok'] for r in out)}/{len(out)} hold; {time.time() - t0:.0f}s")
    json.dump(out, open("rtrap_check.json", "w"))
