import sys
sys.path.insert(0,'/home/sprite/maya-studio/solitaire')
from vernier import *
from collections import Counter
for n in [12,17,18,24,31,32]:
    k,r=tri_k(n); d,nxt,oc=depth_all(n)
    fin=Counter(); runs=Counter()
    for p in d:
        if p in oc: continue
        x=p; run=[]
        while x not in oc:
            v=vernier_state(x,k)
            run = [] if v is None else run+[(v, tuple(diag_cells(x,k)))]
            x=nxt[x]
        if run:
            fin[(run[-1][0], run[-1][1])]+=1
    print(n,k,r)
    for key,c in sorted(fin.items()): print('   final (hole,card)',key[0],'d_k cards',key[1],'count',c)
