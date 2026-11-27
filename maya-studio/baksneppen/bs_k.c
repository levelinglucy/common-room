// Bak-Sneppen with K partners per species. usage: bs_k N K mode steps_millions seed f0 outprefix
// mode 0 fresh (K random each step), 1 one-way fixed (K random out-links), 2 two-way (random K-regular undirected graph)
// Outputs <prefix>_hist.txt and _min.txt (as bs_q.c), and prints: hit share = fraction of drags landing on a species with f < f0
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint64_t s[4];
static inline uint64_t rotl(const uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){const uint64_t r=rotl(s[1]*5,7)*9;const uint64_t t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl(s[3],45);return r;}
static inline double U(void){return (nxt()>>11)*0x1.0p-53;}
static inline int RI(int n){return (int)(U()*n);}
int N,M;double*tree;int*idx;
static void upd(int i,double v){int k=i+M;tree[k]=v;idx[k]=i;k>>=1;while(k){int a=2*k,b=a+1;if(tree[a]<=tree[b]){tree[k]=tree[a];idx[k]=idx[a];}else{tree[k]=tree[b];idx[k]=idx[b];}k>>=1;}}
int main(int argc,char**argv){
  if(argc<8){fprintf(stderr,"usage\n");return 1;}
  N=atoi(argv[1]);int K=atoi(argv[2]);int mode=atoi(argv[3]);long steps=(long)(atof(argv[4])*1e6);uint64_t seed=strtoull(argv[5],0,10);double f0=atof(argv[6]);char*pre=argv[7];
  s[0]=seed*0x9E3779B97F4A7C15ULL+1;s[1]=seed^0xD1B54A32D192ED03ULL;s[2]=0x8CB92BA72F3D8DD7ULL+seed;s[3]=0xABCDEF1234567ULL;for(int i=0;i<20;i++)nxt();
  M=1;while(M<N)M<<=1;tree=malloc(sizeof(double)*2*M);idx=malloc(sizeof(int)*2*M);for(int k=0;k<2*M;k++){tree[k]=2.0;idx[k]=0;}
  double*f=malloc(sizeof(double)*N);for(int i=0;i<N;i++){f[i]=U();upd(i,f[i]);}
  int*nb=malloc(sizeof(int)*N*K);
  if(mode==1){for(int i=0;i<N;i++)for(int k=0;k<K;k++){int j;do j=RI(N);while(j==i);nb[i*K+k]=j;}}
  if(mode==2){ // configuration model with rerolls: pair stubs, retry whole thing on failure, else fix by random edge swaps
    int S=N*K;int*st=malloc(sizeof(int)*S);int*deg=calloc(N,sizeof(int));
    for(;;){
      for(int a=0;a<S;a++)st[a]=a/K;
      for(int a=S-1;a>0;a--){int b=RI(a+1);int t=st[a];st[a]=st[b];st[b]=t;}
      // repair bad pairs by swapping with random pairs
      int bad=1,iter=0;
      while(bad&&iter<100*S){bad=0;
        for(int e=0;e<S/2;e++){int u=st[2*e],v=st[2*e+1];int isbad=(u==v);
          if(!isbad){for(int g=0;g<S/2;g++){if(g==e)continue;int x=st[2*g],y=st[2*g+1];if((x==u&&y==v)||(x==v&&y==u)){isbad=1;break;}}}
          if(isbad){bad=1;int g=RI(S/2);int t=st[2*e+1];st[2*e+1]=st[2*g+1];st[2*g+1]=t;iter++;}}
      }
      if(!bad)break;
    }
    memset(deg,0,sizeof(int)*N);
    for(int e=0;e<S/2;e++){int u=st[2*e],v=st[2*e+1];nb[u*K+deg[u]++]=v;nb[v*K+deg[v]++]=u;}
  }
  long warm=steps/5,hist[1000]={0},mh[1000]={0};long drags=0,hits=0;
  int*tg=malloc(sizeof(int)*K);
  for(long t=0;t<steps;t++){
    int i=idx[1];double m=tree[1];
    if(t>=warm){int b=(int)(m*1000);if(b>999)b=999;mh[b]++;
      if((t&1023)==0)for(int k=0;k<N;k++){int bb=(int)(f[k]*1000);if(bb>999)bb=999;hist[bb]++;}}
    for(int k=0;k<K;k++){int j;if(mode==0){do j=RI(N);while(j==i);}else j=nb[i*K+k];tg[k]=j;}
    if(t>=warm&&m<f0){for(int k=0;k<K;k++){drags++;if(f[tg[k]]<f0)hits++;}}
    f[i]=U();upd(i,f[i]);
    for(int k=0;k<K;k++){int j=tg[k];f[j]=U();upd(j,f[j]);}
  }
  char fn[512];FILE*o;
  sprintf(fn,"%s_hist.txt",pre);o=fopen(fn,"w");for(int b=0;b<1000;b++)fprintf(o,"%d %ld\n",b,hist[b]);fclose(o);
  sprintf(fn,"%s_min.txt",pre);o=fopen(fn,"w");for(int b=0;b<1000;b++)fprintf(o,"%d %ld\n",b,mh[b]);fclose(o);
  printf("%s hitshare %.5f drags %ld\n",pre,drags?(double)hits/drags:0.0,drags);
  return 0;
}
