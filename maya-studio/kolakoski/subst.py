import numpy as np, sys
def rho(a,b):
    L=['ae','ao','be','bo']; idx={x:i for i,x in enumerate(L)}
    img={}
    for x,v in (('a',a),('b',b)):
        img[x+'e']=[('a'+('e' if j%2==0 else 'o')) for j in range(v)]
        img[x+'o']=[('b'+('o' if j%2==0 else 'e')) for j in range(v)]
    Mx=np.zeros((4,4))
    for x in L:
        for y in img[x]: Mx[idx[y],idx[x]]+=1
    w,V=np.linalg.eig(Mx); k=np.argmax(abs(w)); v=abs(np.real(V[:,k])); v/=v.sum()
    return np.sort(abs(w))[::-1], v[0]+v[1], np.round(np.real(w),6)
for a,b in [(1,3),(1,5),(3,5),(3,1)]:
    ev,r,w=rho(a,b); print((a,b),'eigs',w,'density of a',r)
