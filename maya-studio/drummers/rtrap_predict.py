"""Pre-register recursive predictions of jmin past the sim table (k > 20)."""
import sys, json, time
from rtrap import predict
from seam import split

if __name__ == "__main__":
    k0, k1 = int(sys.argv[1]), int(sys.argv[2])
    out = []
    for k in range(k0, k1 + 1):
        for m in range(1, k // 2 + 1):
            n = 2 * k + m
            pj, arg, nc = predict(k, n)
            out.append(dict(k=k, n=n, m=m, pred=pj, trap=arg, ncand=nc))
            print(f"k={k:2d} n={n:2d} m={m:2d}: predicted jmin {pj:2d}  ({nc} cand)  trap {''.join(map(str, arg)) if arg else '-'}", flush=True)
    json.dump(dict(made=time.strftime("%Y-%m-%d %H:%M:%S"), rows=out), open(f"rtrap_predictions_k{k0}_{k1}.json", "w"))
