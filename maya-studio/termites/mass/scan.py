import numpy as np, glob
print("M   seed  froze_at(ticks)  mean_carried(after 1M, while alive)  ground_mean")
for M in (150,200,250,300,350,400,450,500):
    for s in (1,2,3,4):
        fn=f'scan/M{M}_s{s}.txt'
        try: a=np.loadtxt(fn,comments='#')
        except Exception as e: print(M,s,'missing'); continue
        if a.ndim<2 or len(a)<2: print(M,s,'short'); continue
        c=a[:,5]; t=a[:,0]
        fz=np.nonzero(c==M)[0]
        froze=int(t[fz[0]]) if len(fz) else None
        alive=(t>=1e6)&(c<M)
        mc=c[alive].mean() if alive.any() else float('nan')
        print(f'{M:4d} {s}  {str(froze):>12s}  {mc:8.1f}  {M-mc:8.1f}  frac_air {mc/M:.2f}  len {t[-1]/1e6:.1f}M')
