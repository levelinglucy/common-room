import numpy as np, glob, math
out=[]
for L in (400,200):
  r=np.arange(L); d=np.minimum.outer(np.minimum(r,L-1-r),np.minimum(r,L-1-r))
  for m in 'AMVDP':
    accs=[np.fromfile(f).reshape(L,L) for f in sorted(glob.glob(f'walls/{m}_L{L}_s*.bin'))]
    means=[]; dead=0
    for f in sorted(glob.glob(f'walls/{m}_L{L}_s*.txt')):
        x=np.loadtxt(f); y=x[x[:,0]>=500,1]; means.append(y.mean()); dead+= x[-1,1]<0.01 or x[-1,1]>0.99
    means=np.array(means); se=means.std(ddof=1)/math.sqrt(len(means))
    A=np.mean(accs,axis=0)
    prof=[A[d==k].mean() for k in range(12)]
    inner=A[d>=40].mean()
    # excess cooperators per wall cell: sum over (A - inner) for d<40, divided by perimeter 4L
    exc=(A[d<40]-inner).sum()/(4*L)
    out.append((L,m,len(means),dead,means.mean(),se,inner,exc,prof))
    print(f"L{L} {m} runs {len(means)} stuck {dead} share {means.mean():.5f} se {se:.5f} interior {inner:.5f} excess/wallcell {exc:+.3f}")
    print('   rows from wall:',' '.join(f'{v:.3f}' for v in prof))
np.save('walls/summary.npy',np.array(out,dtype=object),allow_pickle=True)
