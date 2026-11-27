#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc,char**argv){
  int a=atoi(argv[1]), d=atoi(argv[2]); long moves=atol(argv[3]);
  int M=4000000; long *b=calloc(M,sizeof(long)); int L=0; double next=1000; long seeds=0;
  double e=(a+1.0)/a;
  for(long m=1;m<=moves;m++){
    int i=0; while(b[i]) i++;
    for(int j=0;j<i;j++) b[j]--;
    b[i]=(long)a*(i+1)+d; seeds+= b[i]-i; if(i+1>L) L=i+1;
    if(m>=next){ printf("a=%d d=%d moves=%ld L=%d seeds=%ld L^e/moves=%.6f L^e/seeds=%.6f\n",a,d,m,L,seeds,pow(L,e)/m,pow(L,e)/seeds); fflush(stdout); next*=sqrt(10);}
  }
}
