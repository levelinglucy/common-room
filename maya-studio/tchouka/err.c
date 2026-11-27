#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(){long N=400000000;int M=100000;long*b=calloc(M,sizeof(long));long l=0;double mx=-1e9,mn=1e9;long chk=1000;
for(long n=1;n<=N;n++){int i=0;while(b[i])i++;for(int j=0;j<i;j++)b[j]--;b[i]=i+1;if(i+1>l)l=i+1;
 double e=l-sqrt(M_PI*n); if(n>1000){if(e>mx)mx=e;if(e<mn)mn=e;}
 if(n==chk||n==N){printf("%ld L=%ld e=%.3f range[%.3f,%.3f] L^2/n=%.7f\n",n,l,e,mn,mx,(double)l*l/n);chk*=4;}}}
