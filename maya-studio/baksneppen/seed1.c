// Mean size of a single-seed f-avalanche in the dropout ring (each neighbour refreshed w.p. 1-p),
// on an infinite line whose background is all above f.
// usage: seed1 p f_lo f_hi f_step n_aval seed  -> prints f mean_s stderr n_capped
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static uint64_t s[4];
static inline uint64_t rotl(const uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){const uint64_t r=rotl(s[1]*5,7)*9;const uint64_t t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl(s[3],45);return r;}
static inline double U(void){return (nxt()>>11)*0x1.0p-53;}
#define L (1<<22)
#define CAP 200000000L
double *val; int *touched; long nt;
typedef struct{double v;int i;}E; E*h; long hn, hcap;
static void push(double v,int i){if(hn>=hcap){hcap*=2;h=realloc(h,sizeof(E)*hcap);}long k=hn++;while(k>0){long pa=(k-1)/2;if(h[pa].v<=v)break;h[k]=h[pa];k=pa;}h[k].v=v;h[k].i=i;}
static E pop(void){E top=h[0];E x=h[--hn];long k=0;for(;;){long a=2*k+1;if(a>=hn)break;if(a+1<hn&&h[a+1].v<h[a].v)a++;if(h[a].v>=x.v)break;h[k]=h[a];k=a;}h[k]=x;return top;}
static inline void refresh(int i,double f){double u=U();if(val[i]<0&&u<f){touched[nt++]=i;}if(u<f){val[i]=u;push(u,i);}else val[i]=-1;}
int main(int argc,char**argv){
  double p=atof(argv[1]),flo=atof(argv[2]),fhi=atof(argv[3]),fst=atof(argv[4]);long na=atol(argv[5]);uint64_t seed=strtoull(argv[6],0,10);
  s[0]=seed*0x9E3779B97F4A7C15ULL+3;s[1]=seed^0xD1B54A32D192ED03ULL;s[2]=0x8CB92BA72F3D8DD7ULL;s[3]=0x1234567ULL+seed;for(int k=0;k<20;k++)nxt();
  val=malloc(sizeof(double)*L);for(long k=0;k<L;k++)val[k]=-1;touched=malloc(sizeof(int)*L*2);hcap=1<<16;h=malloc(sizeof(E)*hcap);
  for(double f=flo;f<=fhi+1e-9;f+=fst){
    double sum=0,sum2=0;long capped=0;
    for(long a=0;a<na;a++){
      nt=0;hn=0;int c=L/2;double u=U()*f;val[c]=u;touched[nt++]=c;push(u,c);long sz=0;int edge=0;
      while(hn>0){E e=pop();if(val[e.i]!=e.v)continue;sz++;if(sz>CAP){capped++;break;}
        int i=e.i;if(i<2||i>L-3){edge=1;break;}
        refresh(i,f);if(U()>=p)refresh(i-1,f);if(U()>=p)refresh(i+1,f);}
      if(edge)capped++;
      for(long k=0;k<nt;k++)val[touched[k]]=-1;
      sum+=sz;sum2+=(double)sz*sz;}
    double m=sum/na,sd=sqrt(sum2/na-m*m);printf("%.4f %.4f %.4f %ld\n",f,m,sd/sqrt(na),capped);fflush(stdout);}
  return 0;}
