import numpy as np, glob, math, sys
burn=int(sys.argv[1]) if len(sys.argv)>1 else 500
target=12*math.log(2)-8
for f in sorted(glob.glob('runs/L*.txt')):
    d=np.loadtxt(f)
    if len(d)<burn+50: print(f,'short',len(d)); continue
    x=d[burn:,1]
    # block means for error bar
    nb=10; bl=np.array_split(x,nb); bm=np.array([b.mean() for b in bl])
    print(f"{f}: n={len(x)} mean={x.mean():.5f} sd={x.std():.5f} blockSE={bm.std(ddof=1)/math.sqrt(nb):.5f}  diff={x.mean()-target:+.5f}")
