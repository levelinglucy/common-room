// ln B partial: S(X) = sum_{x<X} ln(1+1/s(x)) - ln ln X, s(x)=p_x-x+1, printed at X = 10^4..10^8
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
int main(){ long K=100000000; double lk=log(K); long N=(long)(K*(lk+log(lk)))+100;
 uint8_t*c=calloc(N/2+1,1); for(long i=3;i*i<=N;i+=2) if(!c[i/2]) for(long j=i*i;j<=N;j+=2*i) c[j/2]=1;
 long double S=0; long x=0; long next=10000;
 for(long n=2;n<=N;n++){ if(n>2&&(n%2==0||c[n/2])) continue; x++; if(x==next){ printf("%ld %.12Lf\n",x,S-logl(logl((long double)x))); next*=10; if(x>=K) break;} S+=log1pl(1.0L/(n-x+1)); }
}
