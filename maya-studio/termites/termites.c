// Resnick termites on an L x L torus, 8 headings.
// usage: termites L p T maxticks seed outevery(0=log) [snapprefix]
// prints: tick piles largest chips_in_hand ups downs
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static uint64_t s[2];
static inline uint64_t rnd(void){uint64_t a=s[0],b=s[1],r=a+b;b^=a;s[0]=((a<<55)|(a>>9))^b^(b<<14);s[1]=(b<<36)|(b>>28);return r;}
static int L; static unsigned char *g; static int *lab,*stk;
static const int DX[8]={1,1,0,-1,-1,-1,0,1}, DY[8]={0,1,1,1,0,-1,-1,-1};

static int ge[5]; static const int TH[5]={2,5,20,100,500};
static int count(int *largest){
  int n=L*L, piles=0, big=0; for(int q=0;q<5;q++) ge[q]=0;
  for(int i=0;i<n;i++) lab[i]=0;
  for(int i=0;i<n;i++) if(g[i]&&!lab[i]){
    piles++; int sp=0, sz=0; stk[sp++]=i; lab[i]=piles;
    while(sp){int c=stk[--sp]; sz++; int x=c%L,y=c/L;
      for(int d=0;d<8;d++){int xx=(x+DX[d]+L)%L, yy=(y+DY[d]+L)%L, j=yy*L+xx;
        if(g[j]&&!lab[j]){lab[j]=piles; stk[sp++]=j;}}}
    if(sz>big) big=sz; for(int q=0;q<5;q++) if(sz>=TH[q]) ge[q]++;
  }
  *largest=big; return piles;
}

int main(int argc,char**argv){
  L=atoi(argv[1]); double p=atof(argv[2]); int T=atoi(argv[3]);
  long long maxt=atoll(argv[4]); s[0]=atoll(argv[5])*0x9E3779B97F4A7C15ULL+1; s[1]=0xD1B54A32D192ED03ULL^s[0];
  long long every=atoll(argv[6]); const char*snap=(argc>7&&strcmp(argv[7],"-"))?argv[7]:NULL; long long tstart=argc>8?atoll(argv[8]):-1; double sd2=0,sdx=0,sdy=0; long long nd=0;
  for(int i=0;i<20;i++) rnd();
  int n=L*L; g=calloc(n,1); lab=malloc(n*sizeof(int)); stk=malloc(n*sizeof(int));
  for(int i=0;i<n;i++) g[i]=(rnd()>>11)*(1.0/9007199254740992.0)<p;
  int *px=malloc(T*4),*py=malloc(T*4); int *x=malloc(T*4),*y=malloc(T*4),*h=malloc(T*4),*st=malloc(T*4),*jp=malloc(T*4);
  for(int k=0;k<T;k++){x[k]=rnd()%L;y[k]=rnd()%L;h[k]=rnd()%8;st[k]=0;jp[k]=0;}
  long long next=1; int prevN=-1; long long ups=0,downs=0;
  for(long long t=0;t<=maxt;t++){
    int doit = every? (t%every==0) : (t>=next);
    if(doit){int big,N=count(&big); int hand=0; for(int k=0;k<T;k++) hand+=(st[k]!=0);
      if(prevN>=0){ if(N>prevN) ups+=N-prevN; else downs+=prevN-N; }
      prevN=N;
      printf("%lld %d %d %d %lld %lld %d %d %d %d %d\n",t,N,big,hand,ups,downs,ge[0],ge[1],ge[2],ge[3],ge[4]);
      if(snap){char fn[256]; sprintf(fn,"%s_%lld.bin",snap,t); FILE*f=fopen(fn,"wb"); fwrite(g,1,n,f); fclose(f);}
      if(!every){ next = (long long)(next*1.25)+1; }
      if(N==1 && hand==0 && !snap){ }
    }
    for(int k=0;k<T;k++){
      if(jp[k]>0){x[k]=(x[k]+DX[h[k]]+L)%L; y[k]=(y[k]+DY[h[k]]+L)%L; jp[k]--; continue;}
      h[k]=(h[k]+(int)(rnd()%3)+7)&7;
      x[k]=(x[k]+DX[h[k]]+L)%L; y[k]=(y[k]+DY[h[k]]+L)%L;
      int c=y[k]*L+x[k];
      if(st[k]==0){ if(g[c]){g[c]=0; st[k]=1; jp[k]=20; px[k]=x[k]; py[k]=y[k];} }
      else if(st[k]==1){ if(g[c]) st[k]=2; }
      else { if(!g[c]){g[c]=1; st[k]=0; jp[k]=20; if(tstart>=0&&t>=tstart){int ddx=((x[k]-px[k])%L+L+L/2)%L-L/2, ddy=((y[k]-py[k])%L+L+L/2)%L-L/2; sd2+=ddx*ddx+ddy*ddy; sdx+=ddx; sdy+=ddy; nd++;}} }
    }
  }
  if(tstart>=0) fprintf(stderr,"drops %lld over %lld ticks: rate %.5f/tick, mean d2 %.2f, mean dx %.3f dy %.3f\n",nd,maxt-tstart+1,nd/(double)(maxt-tstart+1),sd2/nd,sdx/nd,sdy/nd);
  return 0;
}
