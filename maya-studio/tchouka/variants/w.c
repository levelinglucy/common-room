#include <stdio.h>
#include <stdlib.h>
// pit i (1-indexed) sown when holding c(i)=a*i+d seeds; one into each nearer pit, rest to store
int main(int argc,char**argv){
  int a=atoi(argv[1]), d=atoi(argv[2]); long moves=atol(argv[3]);
  int M=400000; long *b=calloc(M,sizeof(long)); int L=0; long next=1000;
  for(long m=1;m<=moves;m++){
    int i=0; while(b[i]) i++;
    for(int j=0;j<i;j++) b[j]--;
    b[i]=(long)a*(i+1)+d; if(i+1>L) L=i+1;
    if(m==next){ printf("a=%d d=%d moves=%ld L=%d L^2/moves=%.6f\n",a,d,m,L,(double)L*L/m); fflush(stdout); next*=10;}
  }
}
