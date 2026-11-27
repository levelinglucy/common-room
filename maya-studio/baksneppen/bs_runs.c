// Bak-Sneppen on a ring with a far-neighbour swap probability p.
// usage: bs N p steps_millions seed f0 outprefix
// Each step: find min species i. Replace i, and neighbours i-1, i+1;
// each neighbour independently, with prob p, is swapped for a uniform random species.
// Outputs: <prefix>_hist.txt (fitness histogram, 1000 bins, after warmup),
//          <prefix>_min.txt  (histogram of the selected minimum),
//          <prefix>_aval.txt (avalanche sizes below f0, log-binned counts),
//          <prefix>_jump.txt (ring distance between successive minima, counts by distance)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>

static uint64_t s[4];
static inline uint64_t rotl(const uint64_t x, int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){const uint64_t r=rotl(s[1]*5,7)*9;const uint64_t t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl(s[3],45);return r;}
static inline double U(void){return (nxt()>>11)*0x1.0p-53;}

int N, M; double *tree; int *idx;
// tree over leaves M..2M-1; store min value and index
static void upd(int i,double v){int k=i+M;tree[k]=v;idx[k]=i;k>>=1;while(k){int a=2*k,b=2*k+1;if(tree[a]<=tree[b]){tree[k]=tree[a];idx[k]=idx[a];}else{tree[k]=tree[b];idx[k]=idx[b];}k>>=1;}}

int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage\n");return 1;}
  N=atoi(argv[1]); double p=atof(argv[2]); long steps=(long)(atof(argv[3])*1e6); uint64_t seed=strtoull(argv[4],0,10); double f0=atof(argv[5]); char*pre=argv[6];
  s[0]=seed*0x9E3779B97F4A7C15ULL+1;s[1]=seed^0xD1B54A32D192ED03ULL;s[2]=0x8CB92BA72F3D8DD7ULL+seed;s[3]=0xABCDEF1234567ULL;for(int i=0;i<20;i++)nxt();
  M=1;while(M<N)M<<=1; tree=malloc(sizeof(double)*2*M); idx=malloc(sizeof(int)*2*M);
  for(int k=0;k<2*M;k++){tree[k]=2.0;idx[k]=0;}
  double*f=malloc(sizeof(double)*N);
  for(int i=0;i<N;i++){f[i]=U();upd(i,f[i]);}
  long warm=steps/5;
  long hist[1000]={0}, mh[1000]={0};
  long jump[100001]; memset(jump,0,sizeof(jump)); long far=0; // jumps beyond 100000 never at our N
  long aval[64]={0}; long cur=0;
  double lv[80]; long rcur[80], rsum[80], rcnt[80]; for(int q=0;q<80;q++){lv[q]=0.30+0.005*q; rcur[q]=0;rsum[q]=0;rcnt[q]=0;} int prev=-1; long nhist=0;
  for(long t=0;t<steps;t++){
    int i=idx[1]; double m=tree[1];
    if(t>=warm){
      int b=(int)(m*1000); if(b>999)b=999; mh[b]++;
      if(prev>=0){int d=abs(i-prev); if(d>N-d)d=N-d; jump[d]++;}
      for(int q=0;q<80;q++){ if(m<lv[q]) rcur[q]++; else if(rcur[q]>0){rsum[q]+=rcur[q];rcnt[q]++;rcur[q]=0;} }
      if(m<f0) cur++; else { if(cur>0){int lb=(int)floor(log2((double)cur)); aval[lb]++;} cur=0; }
      if((t&1023)==0){ for(int k=0;k<N;k++){int bb=(int)(f[k]*1000); if(bb>999)bb=999; hist[bb]++;} nhist++; }
    }
    prev=i;
    int a=(i+N-1)%N, c=(i+1)%N;
    if(p>0){ if(U()<p) a=(int)(U()*N); if(U()<p) c=(int)(U()*N); }
    f[i]=U();upd(i,f[i]); f[a]=U();upd(a,f[a]); f[c]=U();upd(c,f[c]);
  }
  char fn[512]; FILE*o;
  sprintf(fn,"%s_hist.txt",pre);o=fopen(fn,"w");for(int b=0;b<1000;b++)fprintf(o,"%d %ld\n",b,hist[b]);fclose(o);
  sprintf(fn,"%s_min.txt",pre);o=fopen(fn,"w");for(int b=0;b<1000;b++)fprintf(o,"%d %ld\n",b,mh[b]);fclose(o);
  sprintf(fn,"%s_aval.txt",pre);o=fopen(fn,"w");for(int b=0;b<64;b++)fprintf(o,"%d %ld\n",b,aval[b]);fclose(o);
  sprintf(fn,"%s_jump.txt",pre);o=fopen(fn,"w");for(int d=0;d<=N/2;d++)if(jump[d])fprintf(o,"%d %ld\n",d,jump[d]);fclose(o);
  sprintf(fn,"%s_runs.txt",pre);o=fopen(fn,"w");for(int q=0;q<80;q++)fprintf(o,"%.3f %ld %ld\n",lv[q],rsum[q],rcnt[q]);fclose(o);
  return 0;
}
