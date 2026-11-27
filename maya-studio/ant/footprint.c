// Dump the ant's footprint when it first reaches radius Rstop on a scribbled plane.
// usage: footprint p seed Rstop W out.raw   (W x W window round the start)
// codes: 0 untouched white, 1 untouched scribble, 2 visited now white, 3 visited now black
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint64_t sm;
static uint64_t next64(void){uint64_t z=(sm+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
static double unif(void){return (next64()>>11)*(1.0/9007199254740992.0);}
int main(int argc,char**argv){
  double p=atof(argv[1]); long seed=atol(argv[2]); int Rs=atoi(argv[3]); int W=atoi(argv[4]);
  int G=2048, RF=1000; int c=G/2;
  unsigned char*g=calloc((size_t)G*G,1),*v=calloc((size_t)G*G,1);
  sm=(uint64_t)seed*2654435761ULL+(uint64_t)(p*1e6)+17;
  for(int y=-RF;y<=RF;y++)for(int x=-RF;x<=RF;x++) if(x*x+y*y<=RF*RF && unif()<p) g[(size_t)(c+y)*G+(c+x)]=1;
  const int dx[4]={0,1,0,-1}, dy[4]={-1,0,1,0};
  int x=c,y=c,d=0; long long t=0;
  while(1){
    size_t i=(size_t)y*G+x; v[i]=1;
    if(g[i]){d=(d+3)&3;g[i]=0;} else {d=(d+1)&3;g[i]=1;}
    x+=dx[d]; y+=dy[d]; t++;
    long long r2=(long long)(x-c)*(x-c)+(long long)(y-c)*(y-c);
    if(r2>=(long long)Rs*Rs) break;
  }
  FILE*f=fopen(argv[5],"wb");
  for(int yy=c-W/2;yy<c-W/2+W;yy++)for(int xx=c-W/2;xx<c-W/2+W;xx++){size_t j=(size_t)yy*G+xx; unsigned char code=v[j]?(2+g[j]):g[j]; fputc(code,f);}
  fclose(f);
  long long vis=0; for(size_t j=0;j<(size_t)G*G;j++) vis+=v[j];
  printf("%.3f %ld %lld %lld\n",p,seed,t,vis);
  return 0;
}
