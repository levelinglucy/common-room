import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
N=6000; W=140
b=np.zeros(400,int); img=np.full((N,W),np.nan)
for n in range(1,N+1):
    i=int(np.argmax(b==0)); b[:i]-=1; b[i]=i+1
    k=np.arange(1,W+1); row=b[:W]/k
    row=np.where(b[:W]==0,np.nan,row); img[n-1]=row
fig,ax=plt.subplots(figsize=(7,9),dpi=150)
ax.imshow(img,aspect='auto',cmap='magma',interpolation='nearest')
L=np.sqrt(np.pi*np.arange(1,N+1))
ax.plot(L-1,np.arange(N),color='cyan',lw=0.8,alpha=0.8,label='√(π·seeds)')
ax.set_xlabel('pit (counting from the store)'); ax.set_ylabel('seeds on the board')
ax.set_title('The only winning Tchoukaillon board for each number of seeds\ncolour = how full each pit is (seeds ÷ pit number), black = empty',fontsize=9)
ax.legend(loc='lower right',fontsize=8)
plt.tight_layout(); plt.savefig('boards.png')
