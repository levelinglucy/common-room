import numpy as np,glob
for f in sorted(glob.glob('out/*.txt')):
    a=np.loadtxt(f); m=a[:,0]>=1000
    b=open(f.replace('.txt','.bin'),'rb').read(); R=np.frombuffer(b[:4],np.int32)[0]
    g=np.frombuffer(b[4:],np.uint8).reshape(2*R+1,2*R+1)
    yy,xx=np.mgrid[-R:R+1,-R:R+1]; S=((xx**2+yy**2)*(g>0)).sum()
    n=a[-1,0]; st=a[-1,5]
    print(f, 'gap max(n>=1000)=%.3f mean=%.3f final=%.3f'%(a[m,4].max(),a[m,4].mean(),a[-1,4]),
      'steps=%d sum|x|^2=%d diff=%d rel=%.2e n^2/2pi=%d'%(st,S,st-S,(st-S)/S,n*n/2/np.pi))
