#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc,char**argv){
  int a=atoi(argv[1]), d=atoi(argv[2]); long L0=atol(argv[3]); int S=atoi(argv[4]); long step=atol(argv[5]);
  double e=(a+1.0)/a, s=0, mn=1e9, mx=-1e9;
  for(int t=0;t<S;t++){ long LL=L0+t*step;
    unsigned __int128 P=1;
    for(long k=LL-1;k>=1;k--){ unsigned __int128 c=(unsigned __int128)a*k+d; P += (P + c - 1)/c; }
    double r=pow(LL,e)/(double)P; s+=r; if(r<mn)mn=r; if(r>mx)mx=r; }
  printf("a=%d d=%d L~%ld mean C=%.9f range [%.9f, %.9f]\n",a,d,L0,s/S,mn,mx);
}
