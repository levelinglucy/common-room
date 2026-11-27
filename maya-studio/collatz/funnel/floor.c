// Time spent near the floor: standard steps taken while the value is below V, per trajectory (n uniform in octave k), real vs coin.
// Also: how many times the path re-enters the zone below V after leaving it.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static inline uint64_t sm(uint64_t *s){uint64_t z=(*s+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
typedef struct{double s1,s2,s3;long c;} Mom;
static void add(Mom*m,double x){m->s1+=x;m->s2+=x*x;m->s3+=x*x*x;m->c++;}
static void fin(Mom*m,double*mu,double*sd,double*sk){double c=m->c;*mu=m->s1/c;double v=m->s2/c-*mu**mu;*sd=sqrt(v);*sk=(m->s3/c-3**mu*v-*mu**mu**mu)/pow(v,1.5);}
int main(int argc,char**argv){
  int k=atoi(argv[1]); long M=atol(argv[2]); double V=atof(argv[3]);
  uint64_t seed=999+k*1000003ULL; Mom RT={0},CT={0},RE={0},CE={0}; int rmx=0,cmx=0; static long hr[4000],hc[4000];
  double lV=log(V),l2=log(2.0);
  for(long i=0;i<M;i++){
    uint64_t n=(1ULL<<k)|(sm(&seed)&((1ULL<<k)-1));
    unsigned __int128 m=n; int t=0,e=0,in=0;
    while(m!=1){ int now=(double)m<V; if(now){t++; if(!in) e++;} in=now; if(m&1) m=3*m+1; else m>>=1; }
    add(&RT,t); add(&RE,e); if(t<4000) hr[t]++; if(t>rmx) rmx=t;
    double L=log((double)n); t=0;e=0;in=0; uint64_t bits=0; int nb=0;
    while(L>=l2){ int now=L<lV; int o; if(nb==0){bits=sm(&seed);nb=64;} o=bits&1; bits>>=1; nb--;
      int c=o?2:1; if(now){t+=c; if(!in) e++;} in=now; if(o) L+=log(1.5); else L-=l2; }
    add(&CT,t); add(&CE,e); if(t<4000) hc[t]++; if(t>cmx) cmx=t;
  }
  {char fn[64];sprintf(fn,"floor_hist_%.0f.tsv",V);FILE*F=fopen(fn,"w");for(int q=0;q<4000;q++) if(hr[q]||hc[q]) fprintf(F,"%d\t%ld\t%ld\n",q,hr[q],hc[q]);fclose(F);}
  double a,b,c,d,f,g;
  fin(&RT,&a,&b,&c); fin(&CT,&d,&f,&g); printf("V %.0f  steps below V: real %.2f sd %.2f skew %.2f max %d | coin %.2f sd %.2f skew %.2f max %d\n",V,a,b,c,rmx,d,f,g,cmx);
  fin(&RE,&a,&b,&c); fin(&CE,&d,&f,&g); printf("        entries into zone: real %.3f sd %.3f | coin %.3f sd %.3f\n",a,b,d,f);
  return 0;
}
