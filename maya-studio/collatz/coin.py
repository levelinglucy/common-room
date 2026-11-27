import numpy as np
rng=np.random.default_rng(1)
def coin(k,M=1_000_000):
    L=np.log(2.0**k*(1+rng.random(M)))   # n uniform in octave
    S=np.zeros(M); alive=np.ones(M,bool)
    while alive.any():
        idx=np.nonzero(alive)[0]
        odd=rng.random(idx.size)<0.5
        L[idx]+=np.where(odd,np.log(1.5),-np.log(2)); S[idx]+=np.where(odd,2,1)
        alive[idx[L[idx]<=0]]=False   # reached 1
    m=S.mean(); sd=S.std(); sk=((S-m)**3).mean()/sd**3
    return m,sd,sk
real={}
for line in open('octaves.tsv').readlines()[1:]:
    p=line.split(); real[int(p[0])]=(float(p[2]),float(p[3]),float(p[4]))
print("k  real_mean coin_mean  real_sd coin_sd  real_skew coin_skew")
for k in [10,15,20,25,30]:
    m,sd,sk=coin(k)
    r=real[k]; print(k, "%.2f %.2f   %.2f %.2f   %.3f %.3f"%(r[0],m,r[1],sd,r[2],sk))
