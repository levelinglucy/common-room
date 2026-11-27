import numpy as np, glob, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
L=400; r=np.arange(L); d=np.minimum.outer(np.minimum(r,L-1-r),np.minimum(r,L-1-r))
names={'A':'absent (no one there)','D':'ring of permanent defectors','M':'mirror','V':'absent, average payoff','P':'no wall (wrap-around)'}
cols={'A':'#d62728','D':'#ff9896','M':'#1f77b4','V':'#2ca02c','P':'#555555'}
fig,ax=plt.subplots(1,2,figsize=(12,5))
for m in 'ADMVP':
    A=np.mean([np.fromfile(f).reshape(L,L) for f in glob.glob(f'walls/{m}_L{L}_s*.bin')],axis=0)
    inner=A[d>=40].mean(); prof=np.array([A[d==k].mean() for k in range(20)])
    exc=(A[d<40]-inner).sum()/(4*L)
    ls='--' if m=='D' else '-'
    ax[0].plot(range(20),prof,ls,marker='o',ms=3,color=cols[m],label=f'{names[m]}: {exc:+.2f} per wall cell')
ax[0].axhline(12*np.log(2)-8,color='k',lw=0.6,ls=':'); ax[0].text(19,0.3195,'12 ln 2 - 8',ha='right',fontsize=8)
ax[0].set_xlabel('rows in from the wall'); ax[0].set_ylabel('long-run share of cooperators')
ax[0].set_title('Four kinds of wall, 400 x 400, 6 runs each'); ax[0].legend(fontsize=8,loc='upper right')
ax[0].set_ylim(-0.02,0.62)
s=np.load('walls/summary.npy',allow_pickle=True)
for i,m in enumerate('ADMVP'):
    for L2,mk in ((200,'s'),(400,'o')):
        row=[x for x in s if x[0]==L2 and x[1]==m][0]
        ax[1].errorbar(i+(-0.12 if L2==200 else 0.12),row[4],yerr=row[5],fmt=mk,color=cols[m],label=f'L {L2}' if i==0 else None)
ax[1].axhline(0.31559,color='#555',lw=0.6); ax[1].axhline(12*np.log(2)-8,color='k',lw=0.6,ls=':')
ax[1].set_xticks(range(5)); ax[1].set_xticklabels(['absent','defector\nring','mirror','average\npayoff','no wall'])
ax[1].set_ylabel('whole-grid share (steps 500-4000)'); ax[1].set_title('Whole-grid share: the wall decides the third decimal')
ax[1].legend(fontsize=8,loc='upper right')
fig.suptitle('In this game a defector next door is the same as nobody: so a defector wall is no wall at all',fontsize=11)
fig.tight_layout(); fig.savefig('walls/four_walls.png',dpi=130)
# overlap check
fig.canvas.draw(); rr=fig.canvas.get_renderer()
ts=[t for a in ax for t in a.texts+[a.title,a.xaxis.label,a.yaxis.label]]+[a.get_legend() for a in ax]
bb=[t.get_window_extent(rr) for t in ts]
ov=sum(1 for i in range(len(bb)) for j in range(i+1,len(bb)) if bb[i].overlaps(bb[j]))
print('items',len(bb),'overlaps',ov)
