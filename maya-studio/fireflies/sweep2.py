import sys, numpy as np
from firefly import perches, run, beats, listen_lists
from scipy.spatial import cKDTree
n=int(sys.argv[1]); P=int(sys.argv[2]); eps_list=[float(x) for x in sys.argv[3].split(",")]
rules=[("count",7),("sectors",0),("metric",np.sqrt(7/(np.pi*n)))]
for eps in eps_list:
    for rule,param in rules:
        out=[]
        for sd in range(int(sys.argv[4]) if len(sys.argv)>4 else 3):
            pos=perches(n,100+sd)
            ft,_,lists=run(pos,rule,param,eps=eps,seed=sd,periods=P)
            r,_,ph=beats(ft,periods=P)
            z=np.exp(2j*np.pi*ph)
            # local coherence with 6 geometric nearest (same for all rules)
            _,idx=cKDTree(pos).query(pos,7)
            loc=np.mean(np.abs(np.mean(z[idx[:,1:]]*np.conj(z)[:,None],axis=1)))
            out.append(f"r={r:.2f} loc={loc:.2f}")
        print(n,P,eps,rule," | ".join(out),flush=True)
