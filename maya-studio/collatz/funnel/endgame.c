// Split each trajectory at the first value below an absolute threshold B: phase 1 (the drop) and phase 2 (the endgame, B -> 1).
// Real vs coin, identical stopping rules. Prints mean/sd/skew of each phase and total, and corr(phase1, phase2).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static inline uint64_t sm(uint64_t *s){uint64_t z=(*s+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
typedef struct{double s1,s2,s3;long c;} Mom;
static void add(Mom*m,double x){m->s1+=x;m->s2+=x*x;m->s3+=x*x*x;m->c++;}
static void fin(Mom*m,double*mu,double*sd,double*sk){double c=m->c;*mu=m->s1/c;double v=m->s2/c-*mu**mu;*sd=sqrt(v);*sk=(m->s3/c-3**mu*v-*mu**mu**mu)/pow(v,1.5);}
int main(int argc,char**argv){
  int k=atoi(argv[1]); long M=atol(argv[2]); double B=atof(argv[3]);
  uint64_t seed=777+k*1000003ULL;
  Mom R1={0},R2={0},C1={0},C2={0}; double rx=0,cx=0; int rmax=0,cmax=0;
  double lB=log(B), l2=log(2.0);
  for(long i=0;i<M;i++){
    uint64_t n=(1ULL<<k)|(sm(&seed)&((1ULL<<k)-1));
    unsigned __int128 m=n; int st=0,s1=-1;
    while(m!=1){ if(s1<0 && (double)m<B) s1=st; if(m&1) m=3*m+1; else m>>=1; st++; }
    if(s1<0) s1=st;
    add(&R1,s1); add(&R2,st-s1); rx+=(double)s1*(st-s1); if(st-s1>rmax) rmax=st-s1;
    double L=log((double)n); st=0; s1=-1; uint64_t bits=0; int nb=0;
    while(L>=l2){ if(s1<0 && L<lB) s1=st; if(nb==0){bits=sm(&seed);nb=64;} int o=bits&1; bits>>=1; nb--;
      if(o){L+=log(1.5);st+=2;} else {L-=l2;st+=1;} }
    if(s1<0) s1=st;
    add(&C1,s1); add(&C2,st-s1); cx+=(double)s1*(st-s1); if(st-s1>cmax) cmax=st-s1;
  }
  double a,b,c,d,e,f,g,h,q,r,s,t;
  fin(&R1,&a,&b,&c); fin(&R2,&d,&e,&f); fin(&C1,&g,&h,&q); fin(&C2,&r,&s,&t);
  double rc=(rx/M-a*d)/(b*e), cc=(cx/M-g*r)/(h*s);
  printf("k %d B %.0f\n real drop  %.3f sd %.3f skew %.3f | endgame %.3f sd %.3f skew %.3f max %d | corr %.4f\n",k,B,a,b,c,d,e,f,rmax,rc);
  printf(" coin drop  %.3f sd %.3f skew %.3f | endgame %.3f sd %.3f skew %.3f max %d | corr %.4f\n",g,h,q,r,s,t,cmax,cc);
  return 0;
}
