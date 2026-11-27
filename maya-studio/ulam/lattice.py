import numpy as np, sys
def seq(b):
    u=np.loadtxt(f'u1_{b}.txt',dtype=np.int64)
    brk=np.where(np.diff(u)!=1)[0]
    st=np.r_[u[0],u[brk+1]]; en=np.r_[u[brk],u[-1]]
    E=en[(en-st+1)>=b//3]
    d=np.diff(E); j=np.rint(d/(3*b)).astype(int); dl=d-3*b*j
    return E,j,dl
bs=[int(x) for x in sys.argv[1:]]
R={b:seq(b) for b in bs}
for b in bs:
    E,j,dl=R[b]
    print(b,'steps',j.sum(),'blocks',len(j),'c=sum delta/sum j',dl.sum()/j.sum(), 'E-3b*steps offset at end', E[-1]-3*b*j.sum()-E[0])
b0=bs[0]
for b in bs[1:]:
    n=min(len(R[b0][1]),len(R[b][1]))
    same=(R[b0][1][:n]==R[b][1][:n])&(R[b0][2][:n]==R[b][2][:n])
    first=np.where(~same)[0]
    print(b0,'vs',b,'compared',n,'agree',same.sum(),'first disagreement',first[:5])
