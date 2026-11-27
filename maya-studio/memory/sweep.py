"""Sweep idle time T for several floors; record whether the recalled road is on the trained side.
Usage: I0=1.0 python3 sweep.py OUT.tsv SEEDS
"""
import sys
from multiprocessing import Pool

from memory import trial

FLOORS = [1e-3, 1e-6, 1e-9]
TS = [0, 4, 8, 10, 12, 14, 16, 18, 20, 22, 24, 28]
CONTROL = [(0.0, T) for T in (0, 20, 40)]


def job(args):
    floor, T, seed = args
    r = trial(floor, T, seed)
    return (floor, T, seed, r['side1'], r['side3'], int(r['same']), r['share1'], r['share3'], r['road_left'], r['relearn'])


if __name__ == '__main__':
    out, seeds = sys.argv[1], int(sys.argv[2])
    jobs = [(f, T, s) for f in FLOORS for T in TS for s in range(seeds)]
    jobs += [(f, T, s) for f, T in CONTROL for s in range(seeds)]
    with Pool(8) as pool, open(out, 'w') as fh:
        fh.write('floor\tT\tseed\tside1\tside3\tsame\tshare1\tshare3\troad_left\trelearn\n')
        for row in pool.imap_unordered(job, jobs, chunksize=2):
            fh.write('\t'.join(str(x) for x in row) + '\n')
            fh.flush()
