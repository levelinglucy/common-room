# build board by reverse play, then win it forwards; also check no other board of n seeds wins (small n, brute force)
import itertools
def build(n):
    b=[0]*200
    for _ in range(n):
        i=b.index(0)
        for j in range(i): b[j]-=1
        b[i]=i+1
    while b and b[-1]==0: b.pop()
    return b
def wins(b):
    b=list(b)
    from functools import lru_cache
    @lru_cache(None)
    def w(t):
        if sum(t)==0: return True
        for i,c in enumerate(t):
            if c==i+1:
                u=list(t); u[i]=0
                for j in range(i): u[j]+=1
                if w(tuple(u)): return True
        return False
    return w(tuple(b))
def greedy(b):
    b=list(b)
    while sum(b):
        for i,c in enumerate(b):
            if c==i+1: break
        else: return False
        b[i]=0
        for j in range(i): b[j]+=1
    return True
ok=all(greedy(build(n)) for n in range(1,3001)); print('built boards all win, n<=3000 (greedy forward play):',ok)
# uniqueness brute force n<=12
def comps(n,maxlen):
    # all boards (pits len<=maxlen) summing to n with b[i]<=i+1
    def rec(i,left):
        if left==0: yield (); return
        if i>=maxlen: return
        for c in range(0,min(i+1,left)+1):
            for r in rec(i+1,left-c): yield (c,)+r
    return rec(0,n)
for n in range(1,11):
    W=[c for c in comps(n,n) if c and c[-1]!=0 and wins(c)]
    assert len(W)==1 and list(W[0])==build(n),(n,W)
print('unique winning board for n=1..10: yes')
print(build(20), build(100))
