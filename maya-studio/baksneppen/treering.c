// Single-seed f-avalanche on the "tree of rings": the quenched small world seen locally.
// Every species sits on an infinite line; each of its two slots is, with prob p (fixed at creation),
// a permanent far link to a fresh species on a fresh line; otherwise it is the ring neighbour.
// Everything created lazily. Background above f. Min order.
// usage: treering f p trials maxsteps seed
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static uint64_t s[4];
static inline uint64_t rotl(const uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){const uint64_t r=rotl(s[1]*5,7)*9;const uint64_t t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl(s[3],45);return r;}
static inline double U(void){return (nxt()>>11)*0x1.0p-53;}
#define MAXN 16000000
int *rl,*rr,*fl,*fr; unsigned char *ff; // ff bit0: L slot far, bit1: R slot far
double *hv; int *hn; int hs; int *pos; int nn; double P;
static void sw(int a,int b){double t=hv[a];hv[a]=hv[b];hv[b]=t;int u=hn[a];hn[a]=hn[b];hn[b]=u;pos[hn[a]]=a;pos[hn[b]]=b;}
static void up(int k){while(k>0){int p=(k-1)/2;if(hv[p]<=hv[k])break;sw(p,k);k=p;}}
static void dn(int k){for(;;){int l=2*k+1,r=l+1,m=k;if(l<hs&&hv[l]<hv[m])m=l;if(r<hs&&hv[r]<hv[m])m=r;if(m==k)break;sw(m,k);k=m;}}
static void del(int v){int k=pos[v];if(k<0)return;pos[v]=-1;hs--;if(k==hs)return;hv[k]=hv[hs];hn[k]=hn[hs];pos[hn[k]]=k;up(k);dn(pos[hn[k]]);}
static void ins(int v,double x){hv[hs]=x;hn[hs]=v;pos[v]=hs;hs++;up(hs-1);}
static int newnode(void){int v=nn++;rl[v]=rr[v]=fl[v]=fr[v]=-1;pos[v]=-1;ff[v]=(U()<P?1:0)|(U()<P?2:0);return v;}
static int ringL(int v){if(rl[v]<0){int w=newnode();rl[v]=w;rr[w]=v;}return rl[v];}
static int ringR(int v){if(rr[v]<0){int w=newnode();rr[v]=w;rl[w]=v;}return rr[v];}
int main(int argc,char**argv){
  double f=atof(argv[1]);P=atof(argv[2]);int T=atoi(argv[3]);long MS=atol(argv[4]);uint64_t seed=strtoull(argv[5],0,10);
  s[0]=seed*0x9E3779B97F4A7C15ULL+1;s[1]=seed^0xD1B54A32D192ED03ULL;s[2]=0x8CB92BA72F3D8DD7ULL+seed;s[3]=0xABCDEF1234567ULL;for(int i=0;i<20;i++)nxt();
  rl=malloc(4L*MAXN);rr=malloc(4L*MAXN);fl=malloc(4L*MAXN);fr=malloc(4L*MAXN);ff=malloc(MAXN);pos=malloc(4L*MAXN);hv=malloc(8L*MAXN);hn=malloc(4L*MAXN);
  long surv[40]={0}; double msum=0; long capped=0;
  for(int t=0;t<T;t++){
    nn=0;hs=0; int r=newnode(); ins(r,U()*f); long st=0;
    while(hs>0&&st<MS&&nn<MAXN-8){
      int v=hn[0]; del(v); st++;
      double x=U(); if(x<f) ins(v,x);
      int a,c;
      if(ff[v]&1){ if(fl[v]<0) fl[v]=newnode(); a=fl[v]; } else a=ringL(v);
      if(ff[v]&2){ if(fr[v]<0) fr[v]=newnode(); c=fr[v]; } else c=ringR(v);
      double y=U(); del(a); if(y<f) ins(a,y);
      y=U(); del(c); if(y<f) ins(c,y);
    }
    if(hs>0) capped++; msum+=st;
    for(int k=0;k<40;k++){long S=(long)pow(10,k/4.0); if(st>=S) surv[k]++;}
  }
  printf("f %.4f p %g trials %d mean_trunc %.2f capped %ld\n",f,P,T,msum/T,capped);
  for(int k=0;k<40;k++){long S=(long)pow(10,k/4.0); if(S>MS)break; printf("%ld %ld\n",S,surv[k]);}
  return 0;
}
