import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpmath import gamma, mpf
def traj(a,d,L):
    P=1; ks=[L]; Ps=[1]; js=[1]
    for k in range(L-1,0,-1):
        c=a*k+d; j=-(-P//c); P+=j; ks.append(k); Ps.append(P); js.append(j)
    return np.array(ks),np.array(Ps),np.array(js)
fig,(ax,bx)=plt.subplots(1,2,figsize=(11,5),dpi=150)
L=400; a=1
k,P,j=traj(a,0,L)
m=j<=14
sc=ax.scatter(k[m],P[m],c=j[m],cmap='viridis',s=7,zorder=3)
for jj in range(1,15):
    x=np.linspace(1,L,200); ax.plot(x,jj*a*x,color='grey',lw=0.5,alpha=0.5)
ax.set_ylim(0,P[m].max()*1.08); ax.set_xlim(k[m].min()-5,L+5)
ax.set_xlabel('pit k (walking back from pit 400 towards the store)')
ax.set_ylabel('which move it is, among the moves that reach pit k')
ax.set_title('Ordinary game, tracing back the first move to reach pit 400:\nstraight runs of slope 1, 2, 3 ..., each ending on a grey line (move = slope × pit)',fontsize=9)
plt.colorbar(sc,ax=ax,label='slope of the current run')
aa=list(range(1,7))
pred=[float(gamma(mpf(1)/(x+1))**(mpf(x+1)/x)*gamma(mpf(1)/x)/x**2) for x in aa]
meas=[3.141592267,1.942938391,1.657912735,1.522743142,1.440900244,1.384831464]
bx.plot(aa,pred,'o-',color='C1',label='formula')
bx.plot(aa,meas,'x',color='k',ms=9,label='measured at 10 million pits')
for x,p,m in zip(aa,pred,meas): bx.text(x+0.1,p+0.05,f'{m:.6f}\n{p:.6f}',fontsize=7)
bx.set_xlabel('a  (pit k is sown when it holds a×k seeds)')
bx.set_ylabel('C  in  moves ≈ pits^((a+1)/a) / C')
bx.set_title('Fatter pits: pi becomes Γ(1/(a+1))^((a+1)/a) · Γ(1/a) / a²\n(a = 1 gives Γ(1/2)² = π)',fontsize=9)
bx.legend(fontsize=8); bx.set_xlim(0.5,7.2); bx.set_ylim(1,3.6)
plt.tight_layout(); plt.savefig('fat_pits.png')
