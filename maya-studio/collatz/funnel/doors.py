# Which number is each trajectory's LAST entry into the zone below 64 (the door it takes home), n uniform near 2^40.
import random, collections
random.seed(4)
last=collections.Counter(); first=collections.Counter()
N=100000
for _ in range(N):
    n=(1<<40)|random.getrandbits(40); m=n; prev=n; f=None; door=None
    while m!=1:
        if m<64 and prev>=64:
            door=m
            if f is None: f=m
        prev=m; m= 3*m+1 if m&1 else m>>1
    last[door]+=1; first[f]+=1
print("last door:",[(d,round(c/N,4)) for d,c in last.most_common(8)])
print("first door:",[(d,round(c/N,4)) for d,c in first.most_common(8)])
print("distinct last doors:",len(last))
