import numpy as np, glob, math, re, collections
target=12*math.log(2)-8
groups=collections.defaultdict(list)
for f in glob.glob('runs2/*_L*_s*.txt')+glob.glob('runs/L*_s*.txt'):
    rows=[l.split() for l in open(f)]
    d=np.array([[float(a) for a in r] for r in rows if len(r)==2])
    if d.ndim<2 or len(d)<1000: continue
    x=d[500:,1]
    name=f.split('/')[-1]
    m=re.match(r'(per|fix)?_?L(\d+)_s\d+',name)
    kind=m.group(1) or 'per'; L=int(m.group(2))
    groups[(kind,L)].append((x.mean(), x.min(), len(x), x[-1]))
for k in sorted(groups):
    v=groups[k]; ms=np.array([a[0] for a in v])
    dead=sum(1 for a in v if a[3]<0.01)
    se=ms.std(ddof=1)/math.sqrt(len(ms)) if len(ms)>1 else float('nan')
    print(k, 'runs',len(v),'dead',dead,'mean %.5f se %.5f diff %+.5f'%(ms.mean(),se,ms.mean()-target), 'range %.4f-%.4f'%(ms.min(),ms.max()))
