import random, json
from multiprocessing import Pool
from drummers import run, gaps_of, canon, euclid_gaps
from collections import Counter
k,n,j=28,70,13
E=euclid_gaps(k,n)
def w(s):
    r=random.Random(s);c=Counter()
    for t in range(500):
        pos,_=run(k,n,j,r);g=canon(gaps_of(pos,n))
        if g!=E: c[''.join(map(str,g))]+=1
    return c
with Pool(8) as p: cs=p.map(w,range(8))
tot=sum(cs,Counter()); print('misses in 4000:',sum(tot.values()), tot.most_common(5))
print('E', ''.join(map(str,E)))
d=json.load(open('rtrap_predictions_k21_32.json'))
print([''.join(map(str,r['trap'])) for r in d['rows'] if r['k']==k and r['n']==n])
