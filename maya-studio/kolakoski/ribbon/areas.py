import numpy as np
d=np.load('ribbon_1_3.npz'); z,tag=d['z'],d['tag']; x,y=z.real,z.imag
for G in (400,800):
    ix=((x-x.min())/(x.max()-x.min()+1e-12)*(G-1)).astype(int); iy=((y-y.min())/(y.max()-y.min()+1e-12)*(G-1)).astype(int)
    cell=ix*G+iy; occ=np.zeros((G*G,4),bool); occ[cell,tag]=True; a=occ.sum(0)
    print(G,'cells per tag',a,'even 1-share',a[0]/(a[0]+a[2]),'odd 1-share',a[1]/(a[1]+a[3]),'even/odd area',(a[0]+a[2])/(a[1]+a[3]))
print('point freqs', np.bincount(tag)/len(tag))
