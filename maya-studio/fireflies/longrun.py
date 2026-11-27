import sys, numpy as np
from firefly import perches, run
n=400; rule=sys.argv[1]; eps=float(sys.argv[2]); sd=int(sys.argv[3]); P=int(sys.argv[4])
param={"count":7,"sectors":0,"metric":np.sqrt(7/(np.pi*n))}[rule]
dt=0.002
ft,frames,_=run(perches(n,100+sd),rule,param,eps=eps,seed=sd,periods=P,dt=dt,record_every=int(50/dt))
rs=[abs(np.mean(np.exp(2j*np.pi*f))) for f in frames]
print(rule,eps,sd,"r every 50 periods:"," ".join(f"{r:.2f}" for r in rs),flush=True)
