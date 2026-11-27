import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
real={}
for line in open('octaves.tsv').readlines()[1:]:
    p=line.split(); real[int(p[0])]=tuple(map(float,p[2:5]))
ks=[10,15,20,25,30]
coin={10:(79.40,45.27,1.572),15:(115.59,54.67,1.306),20:(151.64,62.55,1.132),25:(187.81,69.74,1.027),30:(224.02,76.04,0.934)}
H={}
for line in open('hist.tsv'):
    k,t,c=map(int,line.split())
    if k==10: H[t]=c
fig,ax=plt.subplots(1,3,figsize=(15,4.6))
t=np.array(sorted(H)); c=np.array([H[x] for x in t])
ax[0].bar(t,c,width=1,color='#5a7d9a')
ax[0].axvline(50,color='#c0392b',lw=1.5); ax[0].text(53,max(c)*0.92,'1995: 50 steps\n(38th percentile)',color='#c0392b',fontsize=9)
ax[0].set_title('Steps to 1 for every n from 1024 to 2047'); ax[0].set_xlabel('steps'); ax[0].set_ylabel('how many n')
kk=np.arange(8,31)
ax[1].plot(kk,[real[k][0]-10.4277*np.log(1.5*2**k) for k in kk],'o-',color='#5a7d9a',ms=4,label='Collatz')
ax[1].plot(ks,[coin[k][0]-10.4277*np.log(1.5*2**k) for k in ks],'s--',color='#e08e45',label='fair-coin model')
ax[1].set_title('Mean steps minus 10.43 x ln n'); ax[1].set_xlabel('octave (n near 2^k)'); ax[1].legend(loc='lower right',fontsize=9)
ax[2].plot(kk,[real[k][2] for k in kk],'o-',color='#5a7d9a',ms=4,label='Collatz')
ax[2].plot(ks,[coin[k][2] for k in ks],'s--',color='#e08e45',label='fair-coin model')
ax[2].set_title('Lopsidedness (skew) of the step counts'); ax[2].set_xlabel('octave (n near 2^k)'); ax[2].legend(loc='upper right',fontsize=9)
fig.tight_layout(); fig.savefig('collatz_octaves.png',dpi=110)
