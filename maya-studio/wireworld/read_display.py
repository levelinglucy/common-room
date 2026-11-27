"""Read the 7-segment display of the Moore/Owen WireWorld computer from window snapshots.
Window: rows 0..140, cols 120..569 of the parsed grid. Segment on = electrons present in its band."""
import numpy as np, glob, re, sys
pre = sys.argv[1] if len(sys.argv) > 1 else 'snaps/d'
files = sorted(glob.glob(pre + '_*.raw'), key=lambda f: int(re.findall(r'_(\d+)\.raw', f)[0]))
gens = np.array([int(re.findall(r'_(\d+)\.raw', f)[0]) for f in files])
S = np.array([np.fromfile(f, np.uint8).reshape(141, 450) for f in files])
heads = (S == 1)
act = heads[:, :86].sum(0)
col = act.sum(0) > 0
# digit bounding boxes = runs of active columns (merge gaps < 8)
runs = []; x = 0
while x < 450:
    if col[x]:
        a = x
        while x < 450 and (col[x] or col[x:x+8].any()): x += 1
        runs.append((a, x - 1))
    x += 1
runs = [r for r in runs if r[1] - r[0] > 30]
SEG = {  # (y0,y1, xfrac0, xfrac1)
    'a': (0, 10, .3, .7), 'f': (12, 34, 0, .22), 'b': (12, 34, .78, 1), 'g': (35, 45, .3, .7),
    'e': (47, 71, 0, .22), 'c': (47, 71, .78, 1), 'd': (73, 85, .3, .7)}
DIG = {frozenset('abcdef'): 0, frozenset('bc'): 1, frozenset('abged'): 2, frozenset('abgcd'): 3,
       frozenset('fgbc'): 4, frozenset('afgcd'): 5, frozenset('afgedc'): 6, frozenset('abc'): 7,
       frozenset('abcdefg'): 8, frozenset('abcdfg'): 9, frozenset('fgedc'): 6, frozenset('abcfg'): 9,
       frozenset(): ' '}
def read(i):
    out = []
    for (a, b) in runs:
        w = b - a + 1; on = set()
        for s, (y0, y1, f0, f1) in SEG.items():
            box = heads[i, y0:y1, int(a + f0 * w):int(a + f1 * w) + 1]
            if box.sum() > 30: on.add(s)
        out.append(DIG.get(frozenset(on), '?' + ''.join(sorted(on))))
    return out
if __name__ == '__main__':
    print('digit boxes:', runs)
    last = None
    for i in range(len(files)):
        r = read(i)
        if r != last:
            print(gens[i], ''.join(str(c) if len(str(c)) == 1 else '[' + c + ']' for c in r))
            last = r
