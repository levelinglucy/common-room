// Langton's ant on an (almost) endless scribbled plane: first time it reaches each radius,
// and how much of the walk so far was highway-like (104-step displacement a (2,2) diagonal).
// usage: plane p seed0 nseeds [G] [Rfill]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
static uint64_t sm;
static uint64_t next64(void){uint64_t z=(sm+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
static double unif(void){return (next64()>>11)*(1.0/9007199254740992.0);}
int main(int argc,char**argv){
  double p=atof(argv[1]); long seed0=atol(argv[2]); int ns=atoi(argv[3]);
  int G=argc>4?atoi(argv[4]):4096; int RF=argc>5?atoi(argv[5]):1900;
  const int NR=7; int radii[7]={20,40,80,160,320,640,1280};
  unsigned char*g=malloc((size_t)G*G);
  const int dx[4]={0,1,0,-1}, dy[4]={-1,0,1,0};
  int px[104],py[104];
  for(int s=0;s<ns;s++){
    long seed=seed0+s; sm=(uint64_t)seed*2654435761ULL+(uint64_t)(p*1e6)+17;
    memset(g,0,(size_t)G*G); int c=G/2;
    for(int y=-RF;y<=RF;y++)for(int x=-RF;x<=RF;x++) if(x*x+y*y<=RF*RF && unif()<p) g[(size_t)(c+y)*G+(c+x)]=1;
    int x=c,y=c,d=0; long long t=0, hwsteps=0, streak=0, best=0, visited=0; int k=0; unsigned char*v=calloc((size_t)G*G,1);
    long long hit[7]; long long hwat[7]; for(int i=0;i<NR;i++){hit[i]=-1;hwat[i]=-1;}
    long long Tmax=4000000000LL;
    while(t<Tmax && k<NR){
      px[t%104]=x; py[t%104]=y;
      size_t i=(size_t)y*G+x;
      if(g[i]){d=(d+3)&3;g[i]=0;} else {d=(d+1)&3;g[i]=1;}
      x+=dx[d]; y+=dy[d]; t++;
      if(t>=104){int ex=x-px[t%104], ey=y-py[t%104]; if(abs(ex)==2&&abs(ey)==2){hwsteps++;streak++;if(streak>best)best=streak;} else streak=0;}
      {size_t j=(size_t)y*G+x; if(!v[j]){v[j]=1;visited++;}}
      long long r2=(long long)(x-c)*(x-c)+(long long)(y-c)*(y-c);
      while(k<NR && r2>=(long long)radii[k]*radii[k]){hit[k]=t;hwat[k]=hwsteps;k++;}
    }
    printf("%.3f %ld",p,seed);
    for(int i=0;i<NR;i++) printf(" %lld %lld",hit[i],hwat[i]);
    long long blk=0; for(size_t j=0;j<(size_t)G*G;j++) if(v[j]&&g[j]) blk++;
    printf(" %lld %lld %lld\n",best,visited,blk); free(v); fflush(stdout);
  }
  return 0;
}
