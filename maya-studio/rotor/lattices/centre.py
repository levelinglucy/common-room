import numpy as np,glob
from edge import load
def stats(f,lat):
    g,px,py=load(f,lat); occ=g>0
    cx,cy=px[occ].mean(),py[occ].mean()
    r0=np.hypot(px,py); r1=np.hypot(px-cx,py-cy)
    return cx,cy,r0[occ].max()-r0[~occ].min(), r1[occ].max()-r1[~occ].min()
if __name__=='__main__':
    for f in sorted(glob.glob('out/L*_m*.bin')):
        lat=int(f.split('L')[1][0]); cx,cy,g0,g1=stats(f,lat)
        print(f"{f:20s} centre ({cx:+.3f},{cy:+.3f}) |c|={np.hypot(cx,cy):.3f} gap origin {g0:.3f} gap centroid {g1:.3f}")
