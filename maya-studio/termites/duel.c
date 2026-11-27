// Two solid piles duel. usage: duel L T MA MB seed maxticks
// Discs of MA and MB chips centred at (L/4, L/2) and (3L/4, L/2) on a torus.
// Stops when one half of the torus holds < 3% of the chips on the ground.
// prints: seed winner(A/B/-) ticks chipsA chipsB
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static uint64_t s[2];
static inline uint64_t rnd(void){uint64_t a=s[0],b=s[1],r=a+b;b^=a;s[0]=((a<<55)|(a>>9))^b^(b<<14);s[1]=(b<<36)|(b>>28);return r;}
static const int DX[8]={1,1,0,-1,-1,-1,0,1}, DY[8]={0,1,1,1,0,-1,-1,-1};
static int L, JUMP=20; static unsigned char*g;
static void disc(int cx,int cy,int m){
  // fill the m cells nearest the centre (ties by order), exactly m chips
  int n=L*L; double *d=malloc(n*sizeof(double)); int *idx=malloc(n*sizeof(int)); int k=0;
  for(int y=0;y<L;y++)for(int x=0;x<L;x++){double dx=x-cx,dy=y-cy; if(fabs(dx)<L/4&&fabs(dy)<L/4){d[k]=dx*dx+dy*dy+1e-6*(y*L+x);idx[k]=y*L+x;k++;}}
  for(int i=0;i<m;i++){int b=i; for(int j=i+1;j<k;j++) if(d[j]<d[b]) b=j; double td=d[i];d[i]=d[b];d[b]=td; int ti=idx[i];idx[i]=idx[b];idx[b]=ti; g[idx[i]]=1;}
  free(d);free(idx);
}
int main(int argc,char**argv){
  L=atoi(argv[1]); int T=atoi(argv[2]); int MA=atoi(argv[3]), MB=atoi(argv[4]); long long seed=atoll(argv[5]); long long maxt=atoll(argv[6]);
  s[0]=seed*0x9E3779B97F4A7C15ULL+7; s[1]=0xD1B54A32D192ED03ULL^s[0]; for(int i=0;i<20;i++) rnd();
  int n=L*L; g=calloc(n,1); disc(L/4,L/2,MA); disc(3*L/4,L/2,MB);
  long long F[2][2]={{0,0},{0,0}}; long long picks[2]={0,0}; int *ps=malloc(T*4); long long fluxend=argc>7?atoll(argv[7]):0; if(argc>8) JUMP=atoi(argv[8]); int *x=malloc(T*4),*y=malloc(T*4),*h=malloc(T*4),*st=malloc(T*4),*jp=malloc(T*4);
  for(int k=0;k<T;k++){do{x[k]=rnd()%L;y[k]=rnd()%L;}while(g[y[k]*L+x[k]]); h[k]=rnd()%8;st[k]=0;jp[k]=0;}
  for(long long t=1;t<=maxt;t++){
    for(int k=0;k<T;k++){
      if(jp[k]>0){x[k]=(x[k]+DX[h[k]]+L)%L; y[k]=(y[k]+DY[h[k]]+L)%L; jp[k]--; continue;}
      h[k]=(h[k]+(int)(rnd()%3)+7)&7;
      x[k]=(x[k]+DX[h[k]]+L)%L; y[k]=(y[k]+DY[h[k]]+L)%L;
      int c=y[k]*L+x[k];
      if(st[k]==0){ if(g[c]){g[c]=0; st[k]=1; jp[k]=JUMP; ps[k]=(x[k]>=L/2); if(t<=fluxend) picks[ps[k]]++;} }
      else if(st[k]==1){ if(g[c]) st[k]=2; }
      else { if(!g[c]){g[c]=1; st[k]=0; jp[k]=JUMP; if(t<=fluxend) F[ps[k]][x[k]>=L/2]++;} }
    }
    if(fluxend && t==fluxend){ fprintf(stderr,"seed %lld flux t<=%lld: picks A %lld B %lld | A->A %lld A->B %lld B->A %lld B->B %lld\n",seed,fluxend,picks[0],picks[1],F[0][0],F[0][1],F[1][0],F[1][1]); }
    if(t%2000==0){ int a=0,b=0; for(int yy=0;yy<L;yy++)for(int xx=0;xx<L;xx++) if(g[yy*L+xx]){ if(xx<L/2) a++; else b++; }
      double tot=a+b; if(a<0.03*tot||b<0.03*tot){ printf("%lld %c %lld %d %d\n",seed,a>b?'A':'B',t,a,b); return 0; } }
  }
  int a=0,b=0; for(int yy=0;yy<L;yy++)for(int xx=0;xx<L;xx++) if(g[yy*L+xx]){ if(xx<L/2) a++; else b++; }
  printf("%lld - %lld %d %d\n",seed,maxt,a,b); return 0;
}
