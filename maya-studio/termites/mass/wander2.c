// One packed disc of M chips wanders. usage: wander1 L T M seed maxticks every [jump] > out
// Same rules as ../duel.c. Tracks the exact centre of mass of all M chips, unwrapped,
// by adding each chip's hop (drop - pick, minimum image) / M. A carried chip counts at its pick spot.
// Prints a header line, then 't cmx cmy drops sumhop2' every `every` ticks (cumulative drops, sum hop^2).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static uint64_t s[2];
static inline uint64_t rnd(void){uint64_t a=s[0],b=s[1],r=a+b;b^=a;s[0]=((a<<55)|(a>>9))^b^(b<<14);s[1]=(b<<36)|(b>>28);return r;}
static const int DX[8]={1,1,0,-1,-1,-1,0,1}, DY[8]={0,1,1,1,0,-1,-1,-1};
static int L, JUMP=20; static unsigned char*g;
static void disc(int cx,int cy,int m){
  int n=L*L; double *d=malloc(n*sizeof(double)); int *idx=malloc(n*sizeof(int)); int k=0;
  for(int y=0;y<L;y++)for(int x=0;x<L;x++){double dx=x-cx,dy=y-cy; d[k]=dx*dx+dy*dy+1e-6*(y*L+x);idx[k]=y*L+x;k++;}
  // partial selection of m smallest
  for(int i=0;i<m;i++){int b=i; for(int j=i+1;j<k;j++) if(d[j]<d[b]) b=j; double td=d[i];d[i]=d[b];d[b]=td; int ti=idx[i];idx[i]=idx[b];idx[b]=ti; g[idx[i]]=1;}
  free(d);free(idx);
}
static inline int mi(int d){ if(d>L/2) d-=L; else if(d<-L/2) d+=L; return d; }
int main(int argc,char**argv){
  L=atoi(argv[1]); int T=atoi(argv[2]); int M=atoi(argv[3]); long long seed=atoll(argv[4]); long long maxt=atoll(argv[5]); long long every=atoll(argv[6]); if(argc>7) JUMP=atoi(argv[7]);
  s[0]=seed*0x9E3779B97F4A7C15ULL+11; s[1]=0xD1B54A32D192ED03ULL^s[0]; for(int i=0;i<20;i++) rnd();
  int n=L*L; g=calloc(n,1); disc(L/2,L/2,M);
  int *x=malloc(T*4),*y=malloc(T*4),*h=malloc(T*4),*st=malloc(T*4),*jp=malloc(T*4),*px=malloc(T*4),*py=malloc(T*4);
  for(int k=0;k<T;k++){do{x[k]=rnd()%L;y[k]=rnd()%L;}while(g[y[k]*L+x[k]]); h[k]=rnd()%8;st[k]=0;jp[k]=0;}
  double sx=0, sy=0; long long drops=0; double sh2=0;
  printf("# L %d T %d M %d seed %lld jump %d\n",L,T,M,seed,JUMP);
  for(long long t=1;t<=maxt;t++){
    for(int k=0;k<T;k++){
      if(jp[k]>0){x[k]+=DX[h[k]]; if(x[k]<0)x[k]+=L; else if(x[k]>=L)x[k]-=L; y[k]+=DY[h[k]]; if(y[k]<0)y[k]+=L; else if(y[k]>=L)y[k]-=L; jp[k]--; continue;}
      h[k]=(h[k]+(int)(rnd()%3)+7)&7;
      x[k]+=DX[h[k]]; if(x[k]<0)x[k]+=L; else if(x[k]>=L)x[k]-=L; y[k]+=DY[h[k]]; if(y[k]<0)y[k]+=L; else if(y[k]>=L)y[k]-=L;
      int c=y[k]*L+x[k];
      if(st[k]==0){ if(g[c]){g[c]=0; st[k]=1; jp[k]=JUMP; px[k]=x[k]; py[k]=y[k];} }
      else if(st[k]==1){ if(g[c]) st[k]=2; }
      else { if(!g[c]){g[c]=1; st[k]=0; jp[k]=JUMP; int dx=mi(x[k]-px[k]), dy=mi(y[k]-py[k]); sx+=dx; sy+=dy; sh2+=dx*dx+dy*dy; drops++;} }
    }
    if(t%every==0){int c=0; for(int k=0;k<T;k++) c+=(st[k]>0); printf("%lld %.6f %.6f %lld %.0f %d\n",t,sx/M,sy/M,drops,sh2,c);}
  }
  return 0;
}
