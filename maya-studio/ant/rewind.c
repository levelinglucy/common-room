// Trace one dotted run: every K steps print t, x, y (relative to start), black cells on the grid,
// and the 104-step displacement. usage: rewind G T1 phase K Tmax
// The dot goes on the cell whose first visit in the clean run is step T1+phase.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
int main(int argc,char**argv){
  int G=atoi(argv[1]); long long T1=atoll(argv[2]); int ph=atoi(argv[3]); int K=atoi(argv[4]); long long Tmax=atoll(argv[5]); int ph2=argc>6?atoi(argv[6]):-1; int q2x=-1,q2y=-1;
  unsigned char*g=calloc((size_t)G*G,1); int c=G/2;
  // clean run to find the cell first visited at T1+ph
  unsigned char*seen=calloc((size_t)G*G,1);
  int x=c,y=c,d=0,qx=-1,qy=-1;
  long long tend=T1+(ph2>ph?ph2:ph);
  for(long long t=0;t<=tend;t++){
    size_t i=(size_t)y*G+x;
    if(!seen[i]){seen[i]=1; if(t==T1+ph){qx=x;qy=y;} if(t==T1+ph2){q2x=x;q2y=y;}}
    if(g[i]){d=(d+3)&3;g[i]=0;} else {d=(d+1)&3;g[i]=1;}
    x+=DX[d]; y+=DY[d];
  }
  if(qx<0){fprintf(stderr,"no new cell at that step\n");return 1;}
  printf("# dot at (%d,%d) relative to start\n",qx-c,qy-c);
  memset(g,0,(size_t)G*G); g[(size_t)qy*G+qx]=1; if(q2x>=0){g[(size_t)q2y*G+q2x]=1; printf("# second dot at (%d,%d)\n",q2x-c,q2y-c);}
  long long black=q2x>=0?2:1; x=c;y=c;d=0;
  static int px[104],py[104];
  long long st=-1; int sx=0,sy=0;
  long long minblack=1LL<<60, minblack_t=-1; int mind2=1<<30; long long mind2_t=-1;
  for(long long t=0;t<Tmax;t++){
    px[t%104]=x; py[t%104]=y;
    size_t i=(size_t)y*G+x;
    if(g[i]){d=(d+3)&3;g[i]=0;black--;} else {d=(d+1)&3;g[i]=1;black++;}
    x+=DX[d]; y+=DY[d];
    long long tt=t+1;
    if(tt>T1+ph){ int d2=(x-c)*(x-c)+(y-c)*(y-c); if(d2<mind2){mind2=d2;mind2_t=tt;} if(black<minblack){minblack=black;minblack_t=tt;} }
    if(tt>=104){int ex=x-px[tt%104],ey=y-py[tt%104]; int hw=(abs(ex)==2&&abs(ey)==2);
      if(st>=0 && (!hw||ex!=sx||ey!=sy)){ if(tt-st>=2080) printf("SEG %d %d from %lld to %lld (%lld steps)\n",sx,sy,st-104,tt,tt-st+104); st=-1;}
      if(hw && st<0){st=tt;sx=ex;sy=ey;} }
    if(K>0 && tt%K==0 && tt>=104){ printf("%lld %d %d %lld %d %d\n",tt,x-c,y-c,black,x-px[tt%104],y-py[tt%104]); }
    if(x<8||y<8||x>=G-8||y>=G-8){ if(st>=0) printf("SEG %d %d from %lld to edge %lld\n",sx,sy,st-104,tt); break;}
  }
  printf("# after the dot: closest approach to start %d cells^2 at step %lld; fewest black cells %lld at step %lld\n",mind2,mind2_t,minblack,minblack_t);
  return 0;
}
