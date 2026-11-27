// Langton's ant on scribbled ground.
// usage: ant R p seed0 nseeds [G] [Tmax]
// prints one line per seed: R p seed onset end_t escaped hx hy onset_r maxr_before_onset
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

static uint64_t sm;
static uint64_t next64(void){uint64_t z=(sm+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
static double unif(void){return (next64()>>11)*(1.0/9007199254740992.0);}

int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 1;}
  int R=atoi(argv[1]); double p=atof(argv[2]); long seed0=atol(argv[3]); int ns=atoi(argv[4]);
  int G=argc>5?atoi(argv[5]):4096; long long Tmax=argc>6?atoll(argv[6]):400000000LL;
  unsigned char*g=malloc((size_t)G*G);
  const int dx[4]={0,1,0,-1}, dy[4]={-1,0,1,0};
  int px[104],py[104];
  for(int s=0;s<ns;s++){
    long seed=seed0+s; sm=(uint64_t)seed*1000003ULL+(uint64_t)(R*7919)+(uint64_t)(p*1e6);
    memset(g,0,(size_t)G*G);
    int c=G/2;
    for(int y=-R;y<=R;y++)for(int x=-R;x<=R;x++) if(x*x+y*y<=R*R){ if(unif()<p) g[(size_t)(c+y)*G+(c+x)]=1; }
    int x=c,y=c,d=0; long long t=0; long long streak=-1; int sdx=0,sdy=0; int escaped=0;
    double maxr=0, maxr_at_streak=0;
    int margin=8;
    while(t<Tmax){
      px[t%104]=x; py[t%104]=y;
      size_t i=(size_t)y*G+x;
      if(g[i]){d=(d+3)&3;g[i]=0;} else {d=(d+1)&3;g[i]=1;}
      x+=dx[d]; y+=dy[d]; t++;
      if(t>=104){
        int ex=x-px[t%104], ey=y-py[t%104];
        if(abs(ex)==2&&abs(ey)==2){ if(streak<0||ex!=sdx||ey!=sdy){streak=t;sdx=ex;sdy=ey;maxr_at_streak=maxr;} }
        else streak=-1;
      }
      double r2=(double)(x-c)*(x-c)+(double)(y-c)*(y-c);
      if(r2>maxr*maxr) maxr=sqrt(r2);
      if(x<margin||y<margin||x>=G-margin||y>=G-margin){escaped=1;break;}
    }
    long long onset = streak>=0 ? streak-104 : -1;
    double onr=-1;
    if(streak>=0){ /* radius at onset approx: position 104 steps before streak start unknown now; use maxr_at_streak */ onr=maxr_at_streak; }
    // highway must have run at least 20000 steps to count
    int hw = escaped && streak>=0 && (t-streak)>20000;
    printf("%d %.3f %ld %lld %lld %d %d %d %d %.1f\n",R,p,seed,hw?onset:-1,t,escaped,hw?sdx:0,hw?sdy:0,hw,onr);
    fflush(stdout);
  }
  return 0;
}
