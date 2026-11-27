import sys; sys.argv=['x','60']
from every_slip import *
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()): pp=main()
def chain(k,n):
    out=[]
    while k>1:
        r=n%k; c=min(r,k-r); out.append(c); n,k=k,c
        if c==0: break
    return out
# balance-only slips: all pinned?
amb=[];allp=[]
for (k,n),st in pp.items():
    b_tot=st[(True,True)]+st[(True,False)]
    if b_tot==0: continue
    c=min(n%k,k-n%k)
    if c>=3 and st[(True,False)]>0: amb.append((k,n,chain(k,n),st[(True,True)],st[(True,False)]))
print(len(amb)); print(amb[:15])
print([ (k,n) for (k,n) in [(10,23),(10,26),(11,26)]], [pp[(10,23)],pp[(10,26)],pp[(11,26)]])
