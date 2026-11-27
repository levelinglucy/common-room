// Steps (standard Collatz: odd -> 3n+1, even -> n/2) until the trajectory first drops below n^a,
// a in {0.75, 0.5, 0.25, 0}; a = 0 means reaching 1 (first value < 2).
// Real map vs fair-coin model with the identical stopping rule. M samples per octave, n uniform in [2^k, 2^(k+1)).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define NA 4
static const double A[NA]={0.75,0.5,0.25,0.0};
static inline uint64_t sm(uint64_t *s){uint64_t z=(*s+=0x9E3779B97F4A7C15ULL);z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL;z=(z^(z>>27))*0x94D049BB133111EBULL;return z^(z>>31);}
typedef struct{double s1,s2,s3;long c;} Mom;
static void add(Mom*m,double x){m->s1+=x;m->s2+=x*x;m->s3+=x*x*x;m->c++;}
static void fin(Mom*m,double*mu,double*sd,double*sk){double c=m->c;*mu=m->s1/c;double v=m->s2/c-*mu**mu;*sd=sqrt(v);*sk=(m->s3/c-3**mu*v-*mu**mu**mu)/pow(v,1.5);}
int main(int argc,char**argv){
  int k=atoi(argv[1]); long M=atol(argv[2]);
  uint64_t seed=12345+k*1000003ULL;
  Mom R[NA]={0},C[NA]={0};
  for(long i=0;i<M;i++){
    uint64_t n=(1ULL<<k)|(sm(&seed)&((1ULL<<k)-1));
    double ln=log((double)n);
    double T[NA]; for(int j=0;j<NA;j++) T[j]= (A[j]==0.0)?2.0:exp(A[j]*ln);
    // real
    unsigned __int128 m=n; int st=0,j=0;
    while(j<NA){
      while(j<NA && (double)m < T[j]){ add(&R[j],st); j++; }
      if(j>=NA) break;
      if(m&1) m=3*m+1; else m>>=1; st++;
    }
    // coin (shortcut steps: (3x+1)/2 ~ x*1.5 costs 2, x/2 costs 1)
    double L=ln; st=0; j=0;
    double LT[NA]; for(int q=0;q<NA;q++) LT[q]=log(T[q]);
    uint64_t bits=0; int nb=0;
    while(j<NA){
      while(j<NA && L < LT[j]){ add(&C[j],st); j++; }
      if(j>=NA) break;
      if(nb==0){bits=sm(&seed);nb=64;}
      int odd=bits&1; bits>>=1; nb--;
      if(odd){L+=log(1.5);st+=2;} else {L-=log(2.0);st+=1;}
    }
  }
  for(int j=0;j<NA;j++){double a,b,c,d,e,f;fin(&R[j],&a,&b,&c);fin(&C[j],&d,&e,&f);
    printf("%d\t%.2f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n",k,A[j],a,d,a-d,b,e,c,f);}
  return 0;
}
