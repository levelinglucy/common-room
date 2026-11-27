import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D={}
for line in open('results_raw.tsv').readlines()[1:]:
    p=line.split(); D[(int(p[0]),float(p[1]))]=list(map(float,p[2:]))
ks=sorted({k for k,a in D})
fig,ax=plt.subplots(1,3,figsize=(16,4.9))
cols={0.75:'#9bb7d4',0.5:'#5a7d9a',0.25:'#2c4a63',0.0:'#c0392b'}
lab={0.75:'drop below n^0.75',0.5:'drop below n^0.5',0.25:'drop below n^0.25',0.0:'reach 1'}
for a in [0.75,0.5,0.25,0.0]:
    ax[0].plot(ks,[D[(k,a)][2] for k in ks],'o-',color=cols[a],ms=4,label=lab[a])
ax[0].axhline(0,color='grey',lw=0.8)
ax[0].set_title('Collatz minus coin: mean steps'); ax[0].set_xlabel('start size (n near 2^k)'); ax[0].set_ylabel('steps')
ax[0].legend(fontsize=8.5,loc='upper right')
ax[1].plot(ks,[D[(k,0.5)][5] for k in ks],'o-',color='#5a7d9a',ms=4,label='drop below sqrt(n): Collatz')
ax[1].plot(ks,[D[(k,0.5)][6] for k in ks],'s--',color='#e08e45',ms=4,label='drop below sqrt(n): coin')
ax[1].plot(ks,[D[(k,0.0)][5] for k in ks],'o-',color='#c0392b',ms=4,label='reach 1: Collatz')
ax[1].plot(ks,[D[(k,0.0)][6] for k in ks],'s--',color='#f0b27a',ms=4,label='reach 1: coin')
ax[1].set_title('Lopsidedness (skew) of the step counts'); ax[1].set_xlabel('start size (n near 2^k)')
ax[1].legend(fontsize=8.5,loc='upper right')
t,r,c=np.loadtxt('floor_hist_64.tsv',unpack=True); N=r.sum()
m=t<=80
ax[2].bar(t[m]-0.2,r[m]/N,width=0.4,color='#5a7d9a',label='Collatz (longest 22)')
ax[2].bar(t[m]+0.2,c[m]/N,width=0.4,color='#e08e45',label='coin (longest 328)')
ax[2].set_title('Steps spent below 64 (n near 2^40)'); ax[2].set_xlabel('steps'); ax[2].set_ylabel('share of starts')
ax[2].legend(fontsize=8.5,loc='upper right')
ax[2].text(0.97,0.62,'Collatz goes home through\none of 6 doors: 40, 44, 56,\n32, 34, 52 (40 alone: 46%)',transform=ax[2].transAxes,ha='right',va='top',fontsize=8.5)
fig.tight_layout(); fig.savefig('six_doors.png',dpi=110)
