import numpy as np
from firefly import perches, listen_lists, invert
n=400
for sd in range(3):
    pos=perches(n,100+sd)
    for rule,param in [("count",7),("sectors",0),("metric",np.sqrt(7/(np.pi*n)))]:
        L=listen_lists(pos,rule,param)
        lens=np.concatenate([np.linalg.norm(pos[l]-pos[i],axis=1) for i,l in enumerate(L) if len(l)])
        indeg=np.array([len(s) for s in invert(L,n)])
        outd=np.array([len(l) for l in L])
        recip=np.mean([ (i in L[j]) for i,l in enumerate(L) for j in l])
        print(sd,rule,f"links/ff {outd.mean():.1f}  mean len {lens.mean():.3f}  95%len {np.percentile(lens,95):.3f} max {lens.max():.3f}  heard-by min/max {indeg.min()}/{indeg.max()}  reciprocal {recip:.2f}")
