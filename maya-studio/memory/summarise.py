import csv, sys
from collections import defaultdict
rows = list(csv.DictReader(open(sys.argv[1]), delimiter='\t'))
g = defaultdict(list)
for r in rows: g[(float(r['floor']), float(r['T']))].append(r)
print('min share1', min(float(r['share1']) for r in rows), 'min share3', min(float(r['share3']) for r in rows))
s1 = defaultdict(int)
for r in rows:
    if float(r['T'])==0: s1[r['side1']]+=1
print('trained sides (T=0 rows)', dict(s1))
for k in sorted(g):
    v = g[k]; same = sum(int(r['same']) for r in v)
    rl = sum(float(r['relearn']) for r in v)/len(v)
    up3 = sum(r['side3']=='up' for r in v)
    print(f"floor {k[0]:g}  T {k[1]:4g}  same {same:2d}/{len(v)}  recalled-up {up3:2d}  relearn {rl:5.2f}  road {sorted(float(r['road_left']) for r in v)[len(v)//2]:.2e}")
