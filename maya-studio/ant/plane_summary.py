import glob,collections,math,statistics as st
radii=[20,40,80,160,320,640,1280]
D=collections.defaultdict(list)
for f in glob.glob('plane_runs/*.txt'):
    for l in open(f):
        a=l.split(); D[float(a[0])].append([int(v) for v in a[2:]])
print("p n | median first-passage time to r=20..1280 | slope log2(t) per doubling (160->1280) | highway share of steps up to 1280")
for p in sorted(D):
    rs=D[p]
    meds=[st.median([r[2*i] for r in rs]) for i in range(7)]
    hw=st.median([r[13]/r[12] for r in rs])
    sl=[math.log2(meds[i+1]/meds[i]) for i in range(3,6)]
    print(p,len(rs),[int(m) for m in meds],[round(s,2) for s in sl],round(hw,3))
