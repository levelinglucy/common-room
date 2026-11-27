// Single-seed f-avalanche on an infinite out-tree: every species drags the SAME two children every time
// it is the minimum (quenched), children created lazily. Background: everything above f.
// usage: tree f trials maxsteps seed order(0=min,1=random,2=annealed: fresh children every time)
// prints: survival counts at steps 10^k/2 grid and mean truncated size
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static uint64_t s[4];
static inline uint64_t rotl(const uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){const uint64_t r=rotl(s[1]*5,7)*9;const uint64_t t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl(s[3],45);return r;}
static inline double U(void){return (nxt()>>11)*0x1.0p-53;}
#define MAXN 60000000
int *ch; // ch[2v], ch[2v+1]
double *val; int nn;
// heap of (value,node) with lazy deletion: store version
double *hv; int *hn; int hs; int *pos; // pos[v] = heap index or -1
static void sw(int a,int b){double t=hv[a];hv[a]=hv[b];hv[b]=t;int u=hn[a];hn[a]=hn[b];hn[b]=u;pos[hn[a]]=a;pos[hn[b]]=b;}
static void up(int k){while(k>0){int p=(k-1)/2;if(hv[p]<=hv[k])break;sw(p,k);k=p;}}
static void dn(int k){for(;;){int l=2*k+1,r=l+1,m=k;if(l<hs&&hv[l]<hv[m])m=l;if(r<hs&&hv[r]<hv[m])m=r;if(m==k)break;sw(m,k);k=m;}}
static void del(int v){int k=pos[v];if(k<0)return;pos[v]=-1;hs--;if(k==hs)return;hv[k]=hv[hs];hn[k]=hn[hs];pos[hn[k]]=k;up(k);dn(pos[hn[k]]);}
static void ins(int v,double x){hv[hs]=x;hn[hs]=v;pos[v]=hs;hs++;up(hs-1);}
static int newnode(void){int v=nn++;ch[2*v]=-1;ch[2*v+1]=-1;pos[v]=-1;return v;}
int main(int argc,char**argv){
  double f=atof(argv[1]);int T=atoi(argv[2]);long MS=atol(argv[3]);uint64_t seed=strtoull(argv[4],0,10);int order=atoi(argv[5]);
  s[0]=seed*0x9E3779B97F4A7C15ULL+1;s[1]=seed^0xD1B54A32D192ED03ULL;s[2]=0x8CB92BA72F3D8DD7ULL+seed;s[3]=0xABCDEF1234567ULL;for(int i=0;i<20;i++)nxt();
  ch=malloc(sizeof(int)*2*MAXN);pos=malloc(sizeof(int)*MAXN);hv=malloc(sizeof(double)*MAXN);hn=malloc(sizeof(int)*MAXN);
  long surv[40]={0}; long hits=0, hitact=0, revis=0, revhit=0; char*seen=calloc(MAXN,1); double msum=0; long capped=0;
  for(int t=0;t<T;t++){
    for(int q=0;q<nn;q++)seen[q]=0; nn=0;hs=0; int r=newnode(); ins(r,U()*f);
    long st=0;
    while(hs>0 && st<MS && nn<MAXN-3){
      int v;
      if(order==1){ v=hn[(int)(U()*hs)]; } else v=hn[0];
      del(v); st++; int rv=seen[v]; seen[v]=1; if(rv)revis++;
      double x=U(); if(x<f) ins(v,x);
      for(int j=0;j<2;j++){
        int c;
        if(order==2){ c=newnode(); }
        else { c=ch[2*v+j]; if(c<0){c=newnode();ch[2*v+j]=c;} }
        double y=U(); hits++; if(pos[c]>=0){hitact++; if(rv)revhit++;} del(c); if(y<f) ins(c,y);
      }
    }
    if(hs>0) capped++;
    msum+=st;
    for(int k=0;k<40;k++){ long S=(long)pow(10,k/4.0); if(st>=S) surv[k]++; }
  }
  printf("child hits on active: %.4f (pred at criticality (3f-1)/2 = %.4f); steps by a repeat minimum: %.4f; share of active hits that come from repeat minima: %.4f\n",(double)hitact/hits,(3*f-1)/2,(double)revis/msum,(double)revhit/hitact);
  printf("f %.4f order %d trials %d mean_trunc %.2f capped %ld\n",f,order,T,msum/T,capped);
  for(int k=0;k<40;k++){long S=(long)pow(10,k/4.0); if(S>MS)break; printf("%ld %ld\n",S,surv[k]);}
  return 0;
}
