import math,sys
# reverse play: from empty board, unplay one move per step
N=int(sys.argv[1])
b=[0]*10
L=[];
for n in range(1,N+1):
    i=0
    while b[i]!=0: i+=1
    if i+1>=len(b): b+= [0]*len(b)
    for j in range(i): b[j]-=1
    b[i]=i+1
    # length = last nonzero
    l=max(k for k in range(len(b)) if b[k])+1
    L.append(l)
for n in [10,100,1000,10000,100000,N]:
    if n<=N:
        l=L[n-1]; print(n,l,l*l/n, l*l/n/math.pi)
