// One dot in the road: Langton's ant highway meets a single black cell.
// usage: obstacle G T1 Tmax [mode]
//  1) clean run to find the highway classes: cells whose FIRST visit falls in [T1, T1+104).
//  2) for each class representative, fresh run with that cell black from t = 0.
// prints one line per class:
//  idx across phase tv outcome dir_x dir_y onset chaos end_t shift_across
// across = (x+y) of dot minus (x+y) of ant at first visit (constant along the old highway)
// along  = dot position along highway relative to ant at tv (in cells, (x - y) difference / 2 sign so +ahead)
// outcome: A = absorbed (same highway kept through tv+ABS steps), B = broke and rebuilt, N = no highway
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int G;
static unsigned char *g;
static const int DX[4]={0,1,0,-1}, DY[4]={-1,0,1,0};

typedef struct { int x,y,d; long long t; } Ant;

static inline void step(Ant*a){
  size_t i=(size_t)a->y*G+a->x;
  if(g[i]){a->d=(a->d+3)&3;g[i]=0;} else {a->d=(a->d+1)&3;g[i]=1;}
  a->x+=DX[a->d]; a->y+=DY[a->d]; a->t++;
}

int main(int argc,char**argv){
  G=atoi(argv[1]); long long T1=atoll(argv[2]); long long Tmax=atoll(argv[3]);
  g=malloc((size_t)G*G);
  int c=G/2;
  // ---- clean run: first visit time of each cell, up to T1+104 ----
  int *first=malloc(sizeof(int)*(size_t)G*G); // first visit step (step index when ant stands on it)
  for(size_t i=0;i<(size_t)G*G;i++) first[i]=-1;
  memset(g,0,(size_t)G*G);
  Ant a={c,c,0,0};
  // record clean trajectory for comparison
  int *cx=malloc(sizeof(int)*(Tmax+2)), *cy=malloc(sizeof(int)*(Tmax+2));
  long long cleanEnd=Tmax;
  for(long long t=0;t<=Tmax;t++){
    cx[t]=a.x; cy[t]=a.y;
    size_t i=(size_t)a.y*G+a.x;
    if(first[i]<0) first[i]=(int)t;
    if(a.x<4||a.y<4||a.x>=G-4||a.y>=G-4){cleanEnd=t;break;}
    step(&a);
  }
  // classes
  int nc=0; int *rx=malloc(sizeof(int)*1000), *ry=malloc(sizeof(int)*1000), *rt=malloc(sizeof(int)*1000);
  for(int y=0;y<G;y++)for(int x=0;x<G;x++){int f=first[(size_t)y*G+x]; if(f>=T1&&f<T1+104){rx[nc]=x;ry[nc]=y;rt[nc]=f;nc++;}}
  fprintf(stderr,"classes %d cleanEnd %lld\n",nc,cleanEnd);
  // sort by first-visit time
  for(int i=0;i<nc;i++)for(int j=i+1;j<nc;j++) if(rt[j]<rt[i]){int t;t=rt[i];rt[i]=rt[j];rt[j]=t;t=rx[i];rx[i]=rx[j];rx[j]=t;t=ry[i];ry[i]=ry[j];ry[j]=t;}
  int px[104],py[104];
  for(int k=0;k<nc;k++){
    memset(g,0,(size_t)G*G);
    g[(size_t)ry[k]*G+rx[k]]=1;
    Ant b={c,c,0,0};
    long long tv=rt[k];
    int across=(rx[k]+ry[k])-(cx[T1]+cy[T1]);
    long long streak=-1; int sdx=0,sdy=0; long long firstbreak=-1; int edge=0;
    while(b.t<Tmax){
      px[b.t%104]=b.x; py[b.t%104]=b.y;
      step(&b);
      if(b.t>=104){
        int ex=b.x-px[b.t%104], ey=b.y-py[b.t%104];
        if(abs(ex)==2&&abs(ey)==2){ if(streak<0||ex!=sdx||ey!=sdy){streak=b.t;sdx=ex;sdy=ey;} }
        else streak=-1;
        if(b.t>tv && firstbreak<0 && !(ex==-2&&ey==2)) firstbreak=b.t;
      }
      if(b.x<8||b.y<8||b.x>=G-8||b.y>=G-8){edge=1;break;}
    }
    long long onset = streak>=0 ? streak-104 : -1;
    char out; long long chaos=-1; int shift=0;
    if(firstbreak<0){ out='A'; // never broke: compare with clean position at same t
      long long t=b.t<cleanEnd?b.t:cleanEnd; shift=(b.x+b.y)-(cx[t]+cy[t]);
    } else if(edge && streak>=0 && b.t-streak>20000){ out='B'; chaos=onset-tv;
      if(sdx==-2&&sdy==2){ // same direction: sideways shift of the line vs clean
        long long t=b.t<cleanEnd?b.t:cleanEnd; shift=(b.x+b.y)-(cx[t]+cy[t]); }
    } else out='N';
    printf("%d %d %d %lld %c %d %d %lld %lld %lld %d\n",k,across,(int)(tv-T1),tv,out,sdx,sdy,onset,chaos,b.t,shift);
    fflush(stdout);
  }
  return 0;
}
