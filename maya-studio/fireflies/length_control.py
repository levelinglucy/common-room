import numpy as np, firefly as ff
from cause import graph_scores
from scipy.stats import spearmanr
for mode in ("phases","both"):
  out=[]
  for p in range(4):
    pos=ff.perches(400,100+p); lists=ff.listen_lists(pos,"count",7)
    edges=np.array([(i,j) for i,l in enumerate(lists) for j in l])
    freq=np.load(f"cause_out/freq_p{p}_{mode}.npy"); m=~np.isnan(freq)
    nb,_=graph_scores(lists,400)
    ov=np.array([len(nb[i]&nb[j]) for i,j in edges]); L=np.linalg.norm(pos[edges[:,0]]-pos[edges[:,1]],axis=1)
    # within length quartiles, spearman freq vs overlap
    q=np.quantile(L[m],[0,.25,.5,.75,1]); rs=[]
    for a,b in zip(q[:-1],q[1:]):
        s=m&(L>=a)&(L<=b); rs.append(spearmanr(freq[s],ov[s])[0])
    lo=m&(ov<=2); hi=m&(ov>=5)
    out.append((np.mean(rs), freq[lo].mean(), freq[hi].mean(), lo.mean()))
    print(mode,p,"within-length rho %.2f  freq | <=2 shared %.3f  | >=5 shared %.3f  (share of links <=2: %.2f)"%out[-1])
