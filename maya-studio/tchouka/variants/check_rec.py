# check: recursion P_k = P_{k+1} + ceil(P_{k+1}/c(k)) gives the first move that reaches pit L
def sim(a,d,Lmax):
    b=[0]*(Lmax+5); first={}; m=0
    while len(first)<Lmax:
        m+=1; i=b.index(0)
        for j in range(i): b[j]-=1
        b[i]=a*(i+1)+d
        if i+1 not in first: first[i+1]=m
    return first
def rec(a,d,L):
    P=1
    for k in range(L-1,0,-1):
        c=a*k+d; P+= -(-P//c)
    return P
bad=0;tot=0
for a,d in [(1,0),(1,1),(1,3),(2,0),(2,-1),(3,0),(3,2)]:
    f=sim(a,d,60 if a==1 else 40)
    for L,m in f.items():
        tot+=1; bad+= rec(a,d,L)!=m
print('checked',tot,'mismatches',bad)
