import sys, numpy as np
from firefly import perches, run, beats, listen_lists
n=400; P=200; eps=float(sys.argv[1]); seeds=int(sys.argv[2])
for rule,param in [(a.split(':')[0], float(a.split(':')[1])) for a in sys.argv[3:]]:
    rs=[]; deg=[]
    for sd in range(seeds):
        pos=perches(n,100+sd)
        ft,_,L=run(pos,rule,param if rule!="random_near" else sd,eps=eps,seed=sd,periods=P)
        r,_,_=beats(ft,periods=P); rs.append(r); deg.append(np.mean([len(l) for l in L]))
    print(eps,rule,param,f"synced {sum(r>0.95 for r in rs)}/{seeds}  mean r {np.mean(rs):.2f}  links/ff {np.mean(deg):.1f}",flush=True)
