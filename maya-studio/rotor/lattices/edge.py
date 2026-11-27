import numpy as np,sys
S3=3**0.5
def load(f,lat):
    d=open(f,'rb').read(); R=int(np.frombuffer(d[:4],np.int32)[0]); g=np.frombuffer(d[4:],np.uint8).reshape(2*R+1,2*R+1)
    b,a=np.mgrid[-R:R+1,-R:R+1]
    if lat<=1: px,py=a,b
    elif lat==2: px,py=a+0.5*b,b*S3/2
    else: px=a*S3/2; py=1.5*b+np.where((a+b)%2==0,0,-0.5)
    return g,px,py
def profile(f,lat,nb=72):
    g,px,py=load(f,lat); occ=g>0
    th=np.arctan2(py,px); r=np.hypot(px,py)
    bins=((th+np.pi)/(2*np.pi)*nb).astype(int)%nb
    out=np.zeros(nb); inn=np.zeros(nb)
    for k in range(nb):
        m=bins==k
        out[k]=r[m&occ].max(); inn[k]=r[m&~occ].min()
    return out,inn
if __name__=='__main__':
    for f,l in [('out/L3_m0.bin',3),('out/L3_m1.bin',3),('out/L2_m0.bin',2),('out/L0_m0.bin',0)]:
        o,i=profile(f,l,24); print(f,np.round(o-o.mean(),2)); print('  in',np.round(i-i.mean(),2))
