"""sweep.py D BMIN BMAX: census of Kaprekar attractors for one digit count."""
import sys, json
from kaprekar import attractors, to_base

d, b0, b1 = map(int, sys.argv[1:4])
out = {}
for b in range(b0, b1 + 1):
    counts, _ = attractors(b, d)
    cyc = sorted(counts.items(), key=lambda kv: -kv[1])
    desc = [([to_base(x, b, d) for x in c], cnt) for c, cnt in cyc]
    out[b] = desc
    nz = [c for c in cyc if c[0] != (0,)]
    fixed = [c for c in cyc if len(c[0]) == 1 and c[0] != (0,)]
    lens = sorted(len(c[0]) for c in cyc)
    tag = ''
    if len(cyc) == 1 and len(cyc[0][0]) == 1:
        tag = '  <== UNIQUE ' + desc[0][0][0]
    print(f'd={d} base {b:2d}: {len(cyc)} attractors, cycle lengths {lens}, fixed points {[to_base(c[0][0], b, d) for c in fixed]}{tag}', flush=True)
json.dump(out, open(f'sweep_d{d}_b{b0}-{b1}.json', 'w'))
