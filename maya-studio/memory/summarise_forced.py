import csv
import sys
from collections import defaultdict

rows = list(csv.DictReader(open(sys.argv[1]), delimiter='\t'))
g = defaultdict(list)
for r in rows:
    g[(float(r['floor']), float(r['T']))].append(r)
print('rows', len(rows), ' training landed on the wanted side:', sum(r['want'] == r['got'] for r in rows), '/', len(rows))
print('min share3', min(float(r['share3']) for r in rows), ' min naive share', min(float(r['nshare']) for r in rows))
for k in sorted(g):
    v = g[k]
    tr = sum(r['side3'] == r['want'] for r in v)
    nv = sum(r['side3'] == r['naive'] for r in v)
    differ = [r for r in v if r['want'] != r['naive']]
    trd = sum(r['side3'] == r['want'] for r in differ)
    rl = sum(float(r['relearn']) for r in v) / len(v)
    nrl = sum(float(r['nrelearn']) for r in v) / len(v)
    road = sorted(float(r['road_left']) for r in v)[len(v) // 2]
    print(f"floor {k[0]:g}\tT {k[1]:4g}\trecall=trained {tr:2d}/{len(v)}\trecall=naive {nv:2d}/{len(v)}"
          f"\t(against-geometry seeds kept {trd}/{len(differ)})\trelearn {rl:5.2f} vs naive {nrl:5.2f}\troad {road:.2e}")
