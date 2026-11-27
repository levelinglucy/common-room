import sys, numpy as np
from firefly import perches, run, beats
n=int(sys.argv[1]); 
for eps in [0.005,0.01,0.02,0.04]:
    for rule,param in [("count",7),("sectors",0),("metric",np.sqrt(7/(np.pi*n)))]:
        res=[]
        for sd in range(3):
            ft,_,_=run(perches(n,100+sd),rule,param,eps=eps,seed=sd,periods=60)
            r,g,_=beats(ft); res.append((round(r,2),g))
        print(n,eps,rule,res,flush=True)
