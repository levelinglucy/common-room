#include <stdio.h>
#include <stdlib.h>
#include <math.h>
// first move that reaches pit L: P_L=1; P_k = P_{k+1} + ceil(P_{k+1}/c(k)), c(k)=a*k+d; moves = P_1
int main(int argc,char**argv){
  int a=atoi(argv[1]), d=atoi(argv[2]); long Lmax=atol(argv[3]);
  double e=(a+1.0)/a;
  for(long L=10; L<=Lmax; L*=10){
    for(long LL=L; LL<L+3; LL++){
    unsigned __int128 P=1;
    for(long k=LL-1;k>=1;k--){ unsigned long long c=(unsigned long long)a*k+d; P += (P + c - 1)/c; }
    printf("a=%d d=%d L=%ld P1=%.6e L^e/P1=%.9f\n",a,d,LL,(double)P,pow(LL,e)/(double)P,0);
    }
  }
}
