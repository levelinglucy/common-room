// Rotor-router aggregation / IDLA on Z^2.
// usage: rotor mode n seed dumpfile
// mode 0: all north, 1: random arrows, 2: checkerboard N/E, 3: IDLA (random steps)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define W 1601
#define C (W/2)
static unsigned char occ[W*W], rot[W*W];
static uint64_t s;
static inline uint64_t rng(){ s^=s<<13; s^=s>>7; s^=s<<17; return s; }
int dx[4]={0,1,0,-1}, dy[4]={1,0,-1,0}; // N E S W (clockwise)
int main(int argc,char**argv){
  int mode=atoi(argv[1]); long n=atol(argv[2]); s=atol(argv[3])*2654435761ULL+88172645463325252ULL;
  for(int y=0;y<W;y++)for(int x=0;x<W;x++){
    int i=y*W+x;
    if(mode==1) rot[i]=rng()&3; else if(mode==2) rot[i]=((x+y)&1)?1:0; else rot[i]=0;
  }
  long rout2=0; long steps=0;
  long next=100;
  for(long k=1;k<=n;k++){
    int x=C,y=C;
    while(occ[y*W+x]){
      int i=y*W+x; int d;
      if(mode==3) d=rng()&3; else { rot[i]=(rot[i]+1)&3; d=rot[i]; }
      x+=dx[d]; y+=dy[d]; steps++;
      if(x<1||x>=W-1||y<1||y>=W-1){fprintf(stderr,"escaped\n");return 1;}
    }
    occ[y*W+x]=1;
    long r2=(long)(x-C)*(x-C)+(long)(y-C)*(y-C); if(r2>rout2) rout2=r2;
    if(k==next||k==n){
      long rin2=1L<<60;
      int R=(int)sqrt((double)rout2)+2;
      for(int yy=C-R;yy<=C+R;yy++)for(int xx=C-R;xx<=C+R;xx++) if(!occ[yy*W+xx]){
        long d2=(long)(xx-C)*(xx-C)+(long)(yy-C)*(yy-C); if(d2<rin2) rin2=d2; }
      double rd=sqrt(k/M_PI);
      printf("%ld %.4f %.4f %.4f %.4f %ld\n",k,rd,sqrt((double)rout2)-rd,rd-sqrt((double)rin2),sqrt((double)rout2)-sqrt((double)rin2),steps);
      fflush(stdout);
      next=(long)(next*1.25)+1;
    }
  }
  if(argc>4){ FILE*f=fopen(argv[4],"wb"); int R=(int)sqrt((double)rout2)+2; fwrite(&R,4,1,f);
    for(int yy=C-R;yy<=C+R;yy++)for(int xx=C-R;xx<=C+R;xx++){unsigned char v=occ[yy*W+xx]?(1+rot[yy*W+xx]):0; fwrite(&v,1,1,f);} fclose(f);}
  return 0;
}
