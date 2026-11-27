from multiprocessing import Pool
from long_check import run
if __name__ == "__main__":
    jobs = [(L, L - 2, 5000, 640) for L in range(17, 24)] + [(5, 3, 3000, 400)]
    with Pool(8) as p:
        for L, s, out in p.map(run, jobs):
            print(f"L={L} s={s}")
            for row in out[1::2]:
                print("   t=%d pieces=%d live=%d loops=%s" % row)
