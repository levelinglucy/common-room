import numpy as np, sys, collections
b=int(sys.argv[1]); f=sys.argv[2] if len(sys.argv)>2 else f'u1_{b}.txt'
u=np.loadtxt(f,dtype=np.int64)
# maximal runs of consecutive integers
brk=np.where(np.diff(u)!=1)[0]
st=np.r_[u[0],u[brk+1]]; en=np.r_[u[brk],u[-1]]
ln=en-st+1
big=ln>=b//3
S=st[big]; E=en[big]; L=ln[big]
print('runs',len(st),'big',big.sum(),'lengths of big (min,max)',L.min(),L.max())
# spacing of big run ends and starts
for name,X in (('start',S),('end',E)):
    d=np.diff(X)-3*b
    c=collections.Counter(d.tolist())
    print(name,'spacing-3b counts',sorted(c.items())[:15],'mean',d.mean(), 'mean (2nd half)', d[len(d)//2:].mean())
# fit slope of end positions
k=np.arange(len(E)); p=np.polyfit(k[len(k)//4:],E[len(k)//4:],1); print('fit end slope -3b',p[0]-3*b)
# small runs between
