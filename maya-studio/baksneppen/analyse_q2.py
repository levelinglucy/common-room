import analyse, numpy as np, os
def fc(h):
    plat=h[900:995].mean(); k=int(np.argmax(h>plat/2))
    if k==0: return float('nan')
    y0,y1=h[k-1],h[k]; return (k-0.5)/1000+(plat/2-y0)/(y1-y0)/1000
for tag in ['P1','REG']:
    for N in [500,2000,8000,32000]:
        pre=f'qruns/{tag}_N{N}'
        if not os.path.exists(pre+'_hist.txt'): continue
        r=analyse.fc_of(pre)
        d=np.loadtxt(pre+'_deg.txt')[:,1:]
        fr=d.sum(0)/d.sum()
        parts=' '.join(f'k{k}:{fc(d[:,k]):.3f}({fr[k]:.3f})' for k in range(8) if fr[k]>0.001)
        print(f'{tag} N{N:6d} fc {r[0]:.4f} width {r[3]:.3f} | by in-degree {parts}')
pre='qruns/HALF_N8000'; r=analyse.fc_of(pre); d=np.loadtxt(pre+'_deg.txt')[:,1:]; fr=d.sum(0)/d.sum()
print('HALF N8000 fc %.4f'%r[0], ' '.join(f'k{k}:{fc(d[:,k]):.3f}({fr[k]:.3f})' for k in range(8) if fr[k]>0.001))
