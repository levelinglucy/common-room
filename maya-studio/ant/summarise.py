import glob,collections,statistics as st
rows=[l.split() for f in sorted(glob.glob('runs/*.txt')) for l in open(f)]
D=collections.defaultdict(list)
for r in rows: D[(int(r[0]),float(r[1]))].append(r)
print("R p n hw% median q10 q90 max  dirs(++,+-,-+,--)  mean_maxr_at_onset")
for k in sorted(D):
    rs=D[k]; on=[int(r[3]) for r in rs if r[8]=='1']
    dirs=collections.Counter((int(r[6])>0,int(r[7])>0) for r in rs if r[8]=='1')
    on.sort()
    q=lambda f: on[int(f*(len(on)-1))] if on else -1
    mr=st.mean(float(r[9]) for r in rs if r[8]=='1') if on else -1
    print(k[0],k[1],len(rs),round(100*len(on)/len(rs),1),q(.5),q(.1),q(.9),on[-1] if on else -1,
          [dirs[(True,False)],dirs[(True,True)],dirs[(False,False)],dirs[(False,True)]], round(mr,1))
