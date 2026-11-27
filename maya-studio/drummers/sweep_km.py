"""jmin over (k, m) for bigger k: n = 2k + m (and 3k + m as a check)."""
import json
import sys
from multiprocessing import Pool

from sweep import job

if __name__ == "__main__":
    kmax = int(sys.argv[1])
    pairs = []
    for k in range(4, kmax + 1):
        for m in range(1, k // 2 + 1):
            pairs.append((k, 2 * k + m))
            if k <= 14:
                pairs.append((k, 3 * k + m))
    pairs.sort(key=lambda p: -p[0])
    with Pool(8) as p:
        res = p.map(job, pairs, chunksize=1)
    json.dump(res, open(f"sweep_km{kmax}.json", "w"))
    for r in sorted(res, key=lambda r: (r["k"], r["n"])):
        k, n = r["k"], r["n"]
        print(k, n, "m", min(n % k, k - n % k), "jmin", r["jmin"], r["rates"])
