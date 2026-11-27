import re,sys,math
import numpy as np
for f in sys.argv[1:]:
    J=[];M=[]
    for line in open(f):
        m=re.search(r'max\|D\| in \[2\^(\d+),2\^\d+\)=(\d+)',line)
        if m and int(m.group(1))>=12 and int(m.group(2))>0: J.append(int(m.group(1))); M.append(math.log2(int(m.group(2))))
    if len(J)>3:
        s,c=np.polyfit(J,M,1); print(f'{f}: max|D| ~ n^{s:.3f} over 2^{J[0]}..2^{J[-1]+1} ({len(J)} windows)')
