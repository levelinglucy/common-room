"""Fresh check for the nested-rings picture: 29 drummers on 70 slots.

Runs the band RUNS times at j = 11 and j = 12 (new seeds, not the ones in
rtrap_check.py) and counts end states: Euclid, the predicted recursive trap
(or its mirror), anything else. Writes nested_check.json.
"""
import json, random
from multiprocessing import Pool
from collections import Counter
from drummers import run, gaps_of, canon, euclid_gaps
from rtrap import predict

K, N, RUNS = 29, 70, 200
E = euclid_gaps(K, N)
PJ, TRAP, _ = predict(K, N)
MIR = canon(tuple(reversed(TRAP)))


def job(args):
    j, seed = args
    pos, sw = run(K, N, j, random.Random(seed))
    g = canon(gaps_of(pos, N))
    if g == E:
        return j, "euclid", sw
    if g in (TRAP, MIR):
        return j, "trap", sw
    return j, "other:" + "".join(map(str, g)), sw


if __name__ == "__main__":
    jobs = [(j, 100003 * j + s) for j in (11, 12) for s in range(RUNS)]
    with Pool(8) as p:
        out = p.map(job, jobs)
    res = {}
    for j in (11, 12):
        c = Counter(r[1] for r in out if r[0] == j)
        res[j] = dict(c)
        print(f"j={j}: {dict(c)}")
    print("pred jmin", PJ, "trap", "".join(map(str, TRAP)), "mirror same?", MIR == TRAP)
    json.dump({"k": K, "n": N, "runs": RUNS, "pred": PJ,
               "trap": list(TRAP), "euclid": list(E), "res": res},
              open("nested_check.json", "w"), indent=1)
