import numpy as np
from firefly import perches, run
sd=0; P=200; pos=perches(400,100+sd)
for rule,param in [("count",7),("sectors",0)]:
    ft,_,_=run(pos,rule,param,eps=0.03,seed=sd,periods=P)
    rates=[]
    # flash time in the final window [P-1.5, P-0.5): first flash of each firefly
    t=np.array([ [x for x in f if x>=P-1.5][0] for f in ft])
    span=np.ptp(t)
    print(rule,"spread of flash times over one cycle: %.3f period"%span)
    # periods: mean interval
    iv=np.array([np.mean(np.diff(f[-20:])) for f in ft]); print("  mean period %.4f  sd %.5f"%(iv.mean(),iv.std()))
    if span>0.05:
        src=np.argmin(t); dist=np.linalg.norm(pos-pos[src],axis=1)
        print("  corr(flash time, distance from first flasher)=%.2f, first flasher at (%.2f,%.2f)"%(np.corrcoef(t,dist)[0,1],*pos[src]))
        # histogram over time in 10 bins
        h,_=np.histogram(t,bins=10); print("  flashes per tenth of the spread:",h.tolist())
        # where is source over the last 10 cycles
        srcs=[]
        for c in range(10):
            w0=P-1.5-c
            tt=np.array([[x for x in f if x>=w0][0] for f in ft]); srcs.append(tuple(np.round(pos[np.argmin(tt)],2)))
        print("  first flasher, last 10 cycles:",srcs)
