#include <stdio.h>
#include <stdlib.h>
#include <math.h>
// generalised reverse play: pit i (1-indexed) is sown when it holds i+d seeds:
// one seed into each of the i-1 nearer pits, d+1 into the store.
// reverse: first empty pit i, take one from each nearer pit, put i+d in it.
int main(int argc,char**argv){
  int d=atoi(argv[1]); long moves=atol(argv[2]);
  int M=200000; long *b=calloc(M,sizeof(long));
  long n=0; int L=0; int first=0; // first empty pit index (0-based)
  long next=1000;
  for(long m=1;m<=moves;m++){
    int i=0; while(b[i]) i++;
    for(int j=0;j<i;j++) b[j]--;
    b[i]=i+1+d; n+= (long)(i+1+d) - i;
    if(i+1>L) L=i+1;
    while(L>0 && b[L-1]==0) L--;
    if(m==next){ printf("d=%d moves=%ld seeds=%ld L=%d L^2/seeds=%.6f L^2/moves=%.6f\n",d,m,n,L,(double)L*L/n,(double)L*L/m); fflush(stdout); next*=10;}
  }
}
