// One (or two) dots in the road. Langton's ant highway meets black cells placed on its future path.
// usage: obstacle2 G T1 Tmax npair_periods
//   classes = cells whose FIRST visit in the clean run falls in [T1, T1+104)
//   singles: one dot per class.  pairs: every pair of cells with first visit in [T1, T1+104*npair_periods)
// output lines:
//   S idx across phase outcome dx dy chaos shift lag
//   P i j phase_i phase_j outcome dx dy chaos shift lag
// across: (x+y) of dot minus min(x+y) over the clean highway period at T1 (0..width-1)
// outcome: A = never broke (displacement stayed (-2,2) throughout), B = broke and rebuilt, N = no highway by Tmax
// shift: for a final (-2,2) highway, min(x+y) over the last 104 steps minus the clean one (sideways move of the road)
// lag:   for a final (-2,2) highway with shift 0: how many steps behind the clean ant it runs (mod checks done by matching)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int G;
static unsigned char *g;
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};
static int *cx,*cy; static long long cleanEnd; static int cleanMin;
static long long T1;

typedef struct { char out; int dx,dy; long long chaos; int shift; long long lag; long long end; } Res;

static Res run(long long Tmax,int nd,const int*dxs,const int*dys,long long tv){
  memset(g,0,(size_t)G*G);
  for(int k=0;k<nd;k++) g[(size_t)dys[k]*G+dxs[k]]=1;
  int c=G/2; int x=c,y=c,d=0; long long t=0;
  static int px[104],py[104];
  long long streak=-1; int sdx=0,sdy=0; long long firstbreak=-1; int edge=0;
  while(t<Tmax){
    px[t%104]=x; py[t%104]=y;
    size_t i=(size_t)y*G+x;
    if(g[i]){d=(d+3)&3;g[i]=0;} else {d=(d+1)&3;g[i]=1;}
    x+=DX[d]; y+=DY[d]; t++;
    if(t>=104){
      int ex=x-px[t%104], ey=y-py[t%104];
      if(abs(ex)==2&&abs(ey)==2){ if(streak<0||ex!=sdx||ey!=sdy){streak=t;sdx=ex;sdy=ey;} }
      else streak=-1;
      if(t>tv && firstbreak<0 && !(ex==-2&&ey==2)) firstbreak=t;
    }
    if(x<8||y<8||x>=G-8||y>=G-8){edge=1;break;}
  }
  Res r; r.dx=sdx; r.dy=sdy; r.chaos=-1; r.shift=0; r.lag=-1; r.end=t;
  if(firstbreak<0) r.out='A';
  else if(edge && streak>=0 && t-streak>20000){ r.out='B'; r.chaos=(streak-104)-tv; }
  else { r.out='N'; return r; }
  if(sdx==-2&&sdy==2){
    int mn=1<<30; for(int k=0;k<104;k++){int s=px[k]+py[k]; if(s<mn)mn=s;}
    r.shift=mn-cleanMin;
    if(r.shift==0){ // lag: L such that the last 104 positions equal the clean ones L steps earlier
      for(long long L=-3000; L<=200000; L++){
        long long u=t-L; if(u>cleanEnd||u-104<0) continue;
        int ok=1; for(long long k=1;k<=104&&ok;k++){ long long tt=t-k; int ix=(int)(tt%104);
          if(px[ix]!=cx[u-k]||py[ix]!=cy[u-k]) ok=0; }
        if(ok){ r.lag=L; break; }
      }
    }
  }
  return r;
}

int main(int argc,char**argv){
  G=atoi(argv[1]); T1=atoll(argv[2]); long long Tmax=atoll(argv[3]); int npp=atoi(argv[4]);
  g=malloc((size_t)G*G);
  int c=G/2;
  int *first=malloc(sizeof(int)*(size_t)G*G);
  for(size_t i=0;i<(size_t)G*G;i++) first[i]=-1;
  memset(g,0,(size_t)G*G);
  cx=malloc(sizeof(int)*(Tmax+2)); cy=malloc(sizeof(int)*(Tmax+2));
  {int x=c,y=c,d=0; cleanEnd=Tmax;
   for(long long t=0;t<=Tmax;t++){
    cx[t]=x; cy[t]=y; size_t i=(size_t)y*G+x;
    if(first[i]<0) first[i]=(int)t;
    if(x<8||y<8||x>=G-8||y>=G-8){cleanEnd=t;break;}
    if(g[i]){d=(d+3)&3;g[i]=0;} else {d=(d+1)&3;g[i]=1;}
    x+=DX[d]; y+=DY[d];
   }}
  // clean min(x+y) over the last full 104 window before cleanEnd
  cleanMin=1<<30; for(long long t=cleanEnd-104;t<cleanEnd;t++){int s=cx[t]+cy[t]; if(s<cleanMin)cleanMin=s;}
  int refMin=1<<30; for(long long t=T1;t<T1+104;t++){int s=cx[t]+cy[t]; if(s<refMin)refMin=s;}
  int n=0, cap=104*npp+10; int *rx=malloc(sizeof(int)*cap*2),*ry=malloc(sizeof(int)*cap*2),*rt=malloc(sizeof(int)*cap*2);
  for(int y=0;y<G;y++)for(int x=0;x<G;x++){int f=first[(size_t)y*G+x]; if(f>=T1&&f<T1+104*(npp>0?npp:1)){rx[n]=x;ry[n]=y;rt[n]=f;n++;}}
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++) if(rt[j]<rt[i]){int t;t=rt[i];rt[i]=rt[j];rt[j]=t;t=rx[i];rx[i]=rx[j];rx[j]=t;t=ry[i];ry[i]=ry[j];ry[j]=t;}
  fprintf(stderr,"cells %d cleanEnd %lld\n",n,cleanEnd);
  for(int k=0;k<n;k++){ if(rt[k]>=T1+104) break;
    Res r=run(Tmax,1,&rx[k],&ry[k],rt[k]);
    printf("S %d %d %d %c %d %d %lld %d %lld\n",k,(rx[k]+ry[k])-refMin,(int)(rt[k]-T1),r.out,r.dx,r.dy,r.chaos,r.shift,r.lag); fflush(stdout);}
  if(npp>0) for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
    int xs[2]={rx[i],rx[j]}, ys[2]={ry[i],ry[j]};
    Res r=run(Tmax,2,xs,ys,rt[i]);
    printf("P %d %d %d %d %c %d %d %lld %d %lld\n",i,j,(int)(rt[i]-T1),(int)(rt[j]-T1),r.out,r.dx,r.dy,r.chaos,r.shift,r.lag); fflush(stdout);}
  return 0;
}
