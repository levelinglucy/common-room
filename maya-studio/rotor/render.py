import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
def load(f):
    b=open(f,'rb').read(); R=np.frombuffer(b[:4],np.int32)[0]
    return np.frombuffer(b[4:],np.uint8).reshape(2*R+1,2*R+1)[::-1]
cm=ListedColormap(['#0b0b12','#f2c14e','#e4572e','#4e8098','#7fb069'])
fig=plt.figure(figsize=(15,10.5),dpi=110)
titles=[('north','All arrows start north'),('rand1','Arrows start random'),('idla1','No arrows: random steps (IDLA)')]
for i,(k,t) in enumerate(titles):
    ax=fig.add_axes([0.02+i*0.33,0.40,0.30,0.55]); g=load('out/%s.bin'%k)
    if k.startswith('idla'): ax.imshow(g>0,cmap=ListedColormap(['#0b0b12','#c9c9d6']),interpolation='nearest')
    else: ax.imshow(g,cmap=cm,vmin=0,vmax=4,interpolation='nearest')
    ax.set_title(t,fontsize=13); ax.axis('off')
fig.text(0.5,0.365,'300,000 walkers each. Colours = the arrow each site holds at the end (yellow N, red E, blue S, green W).',ha='center',fontsize=11)
ax=fig.add_axes([0.07,0.06,0.40,0.26])
for k,c,l in [('north','#f2c14e','all north'),('check','#e4572e','checkerboard'),('rand1','#4e8098','random 1'),('rand2','#4e8098',None),('rand3','#4e8098',None),('idla1','#999999','IDLA'),('idla2','#999999',None),('idla3','#999999',None)]:
    a=np.loadtxt('out/%s.txt'%k); m=a[:,0]>=100
    ax.plot(a[m,1],a[m,4],color=c,label=l,lw=1.3)
ax.set_xscale('log'); ax.set_ylim(0,12); ax.set_xlabel('disc radius'); ax.set_ylabel('outer minus inner radius'); ax.legend(fontsize=9,loc='upper left',ncol=4); ax.set_title('How ragged the edge is',fontsize=12)
ax2=fig.add_axes([0.56,0.06,0.40,0.26]); ax2.axis('off')
txt=("Edge raggedness, biggest seen from 1,000 walkers on:\n"
"  all north 1.67, checkerboard 1.88, random arrows 1.76 to 2.32\n"
"  random steps 6.7 to 7.3\n\n"
"Total steps vs the sum of squared distances where walkers settled:\n"
"  arrows: equal to within 0.01%\n"
"  random steps: 0.15% to 0.31% over")
ax2.text(0,0.95,txt,va='top',fontsize=11.5,family='monospace')
fig.savefig('rotor_discs.png'); print('saved')
fig.canvas.draw(); r=fig.canvas.get_renderer()
bbs=[]
for a in fig.axes:
    for t in [a.title,a.xaxis.label,a.yaxis.label]+a.texts+a.get_xticklabels()+a.get_yticklabels():
        if t.get_visible() and t.get_text(): bbs.append((t.get_text()[:20],t.get_window_extent(r)))
    L=a.get_legend()
    if L: bbs.append(('legend',L.get_window_extent(r)))
for t in fig.texts: bbs.append((t.get_text()[:20],t.get_window_extent(r)))
ov=[(a[0],b[0]) for i,a in enumerate(bbs) for b in bbs[i+1:] if a[1].overlaps(b[1])]
print(len(bbs),'texts, overlaps:',ov)
L=fig.axes[3].get_legend().get_window_extent(r); inv=fig.axes[3].transData
hits=0
for ln in fig.axes[3].lines:
    xy=inv.transform(ln.get_xydata()); hits+=sum(L.contains(x,y) for x,y in xy)
print('legend-data hits',hits)
