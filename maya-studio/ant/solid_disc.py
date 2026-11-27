# What happens when the mirrored highway built inside a solid black disc reaches the disc's edge?
import sys
R=int(sys.argv[1]); T=int(sys.argv[2])
black=set((x,y) for x in range(-R,R+1) for y in range(-R,R+1) if x*x+y*y<=R*R)
dx=[0,1,0,-1]; dy=[-1,0,1,0]
x=y=d=0; hist=[]; segs=[]; cur=None; start=0
for t in range(1,T+1):
    hist.append((x,y))
    if (x,y) in black: d=(d+3)%4; black.discard((x,y))
    else: d=(d+1)%4; black.add((x,y))
    x+=dx[d]; y+=dy[d]
    if t>=104:
        ex=x-hist[t-104][0]; ey=y-hist[t-104][1]
        hw=(ex,ey) if abs(ex)==2 and abs(ey)==2 else None
    else: hw=None
    if hw!=cur:
        if cur is not None and t-start>500: segs.append((start-104,t,cur,round((hist[start-1][0]**2+hist[start-1][1]**2)**.5),round((x*x+y*y)**.5)))
        cur=hw; start=t
if cur is not None: segs.append((start-104,T,cur,round((hist[start-1][0]**2+hist[start-1][1]**2)**.5),round((x*x+y*y)**.5)))
print("R",R,"highway stretches >500 steps: (start, end, direction, r at start, r at end)")
for s in segs: print(s)
