import sys,numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from firefly import perches, run
P=200; eps=float(sys.argv[1]); rule=sys.argv[2]; param=float(sys.argv[3]); seeds=int(sys.argv[4])
for sd in range(seeds):
    pos=perches(400,100+sd)
    ft,_,_=run(pos,rule,param,eps=eps,seed=sd,periods=P)
    w0=P-1.2
    t=np.array([[x for x in f if x>=w0][0] for f in ft])
    order=np.argsort(t); lab=np.zeros(400,int); g=0
    for a,b in zip(order[:-1],order[1:]):
        if t[b]-t[a]>0.02: g+=1
        lab[b]=g
    sizes=np.bincount(lab); big=np.nonzero(sizes>=5)[0]
    # spatial: patches = connected comps of geometric 6-NN graph restricted to same-choir links
    _,idx=cKDTree(pos).query(pos,7)
    rows=np.repeat(np.arange(400),6); cols=idx[:,1:].ravel(); m=lab[rows]==lab[cols]
    A=coo_matrix((np.ones(m.sum()),(rows[m],cols[m])),shape=(400,400))
    nc,cl=connected_components(A,directed=False)
    patch_sizes=np.bincount(cl); 
    print(f"seed {sd}: choirs(>=5) {len(big)} sizes {sorted(sizes[big].tolist(),reverse=True)}  stragglers {int(sizes[sizes<5].sum())}  spatial patches(>=5) {int(np.sum(patch_sizes>=5))}",flush=True)
