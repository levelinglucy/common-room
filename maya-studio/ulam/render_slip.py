import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
b=20; lam_true=3*b+0.417031
u=np.loadtxt('u1_20_4M.txt',dtype=np.int64)
rows=600; W=3*b
def grid(lam, cols):
    g=np.zeros((rows,cols))
    for x in u:
        r=int(x//lam)
        if r>=rows: break
        c=int(((x - r*lam)/lam)*cols)
        g[r,min(c,cols-1)]+=1
    return g>0
g1=grid(W,W); g2=grid(lam_true,W)
fig,ax=plt.subplots(1,3,figsize=(15,9),gridspec_kw={'width_ratios':[1,1,1.1]})
fig.patch.set_facecolor('#111')
for a,g,t in ((ax[0],g1,'bar of 60 seats (3 x 20)'),(ax[1],g2,'bar of 60.417 seats')):
    a.imshow(g,cmap='magma',aspect='auto',interpolation='nearest')
    a.set_title(t,color='w',fontsize=13); a.set_xticks([]); a.set_yticks([0,150,300,450,599]); a.tick_params(colors='#aaa')
    a.set_ylabel('bar number',color='#aaa')
d=np.load('lattice10.npy'); m,r=d[:,0],d[:,1]; c,phi=np.polyfit(m,r,1); dv=r-c*m-phi
a=ax[2]; a.set_facecolor('#111')
a.hist(dv,bins=60,orientation='horizontal',color='#f4a259')
a.set_title('where each big block lands vs the\nperfect 3b + 0.417 grid (131,504 bars)',color='w',fontsize=12)
a.set_ylim(dv.min()-0.2,dv.max()+0.2); a.set_yticks([-1,-0.5,0,0.5,1]); a.set_ylabel('seats early / late',color='#aaa'); a.set_xlabel('blocks',color='#aaa'); a.tick_params(colors='#aaa')
for s in a.spines.values(): s.set_color('#555')
a.text(0.5,0.04,'spread %.2f seats, never wider'%(dv.max()-dv.min()),transform=a.transAxes,color='w',ha='center',fontsize=11)
fig.suptitle('Ulam sequence U(1,20): the blocks slip 0.417 of a seat per bar',color='w',fontsize=16)
plt.tight_layout(rect=[0,0,1,0.92]); plt.savefig('ulam_slip.png',dpi=110,facecolor=fig.get_facecolor())
print('saved', g1.mean(), g2.mean(), dv.max()-dv.min())
# overlap check of text
fig.canvas.draw(); rd=fig.canvas.get_renderer()
bbs=[t.get_window_extent(rd) for t in fig.findobj(matplotlib.text.Text) if t.get_text() and t.get_visible()]
ov=sum(1 for i in range(len(bbs)) for j in range(i+1,len(bbs)) if bbs[i].overlaps(bbs[j]))
print('texts',len(bbs),'overlapping pairs',ov)
# slant measure: in g1, column of block centre per row should drift ~0.417/row
