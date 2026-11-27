"""Same colony census as long_check.py, but every founder gets arm 5, the arm
its own descendants use, so the founder sits on the colony's lattice."""
import sys
from multiprocessing import Pool
from build_loop import build, genome_of, census
from long_check import sides
from langton import step, place


def run(args):
    L, T, N, arm = args
    g = place(build(L, genome_of(L - 2, 2, L), arm), N)
    out = []
    for t in range(1, T + 1):
        g = step(g)
        if t % 500 == 0:
            n, _ = census(g)
            out.append((t, n, int((g > 0).sum()), sides(g)))
    return L, arm, out


if __name__ == "__main__":
    jobs = [(L, 5000, 640, 5) for L in range(17, 24)] + [(L, 3000, 520, 5) for L in range(8, 17)]
    with Pool(8) as p:
        for L, arm, out in p.map(run, jobs):
            t, n, live, s = out[-1]
            allh = sum(s.values())
            same = s.get(L, 0)
            print(f"L={L} arm={arm} t={t} pieces={n} live={live} clean={same}/{allh}={same/max(allh,1):.2f} loops={s}", flush=True)
