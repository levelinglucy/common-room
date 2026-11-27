// Self-consistency test. Run to N; count values in window [N/2, N).
// Actual: count of g in window. Predicted: sum_v c(v) p (1-p)^(g-1), p = c(v)/W (Poisson occurrences of v).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
int main(int argc,char**argv){
  long N=atol(argv[1]); long W=N-N/2;
  uint32_t *last=calloc(N+1,4), *cnt=calloc(N+1,4);
  uint32_t a=0;
  for(long n=0;n<N;n++){
    uint32_t nx = last[a]? (uint32_t)(n-(last[a]-1)) : 0;
    last[a]=n+1; a=nx;
    if(n+1>=N/2) cnt[a]++;
  }
  long G[]={1,2,3,4,5,6,8,10,15,20,30,50,70,100,150,200,300,500,700,1000,2000,5000,10000,30000,100000,300000,1000000,3000000,10000000,30000000};
  int ng=sizeof(G)/sizeof(G[0]);
  double pred[64]={0};
  for(long v=1; v<=N; v++){ if(!cnt[v]) continue; double c=cnt[v], p=c/W, lq=log1p(-p);
    for(int i=0;i<ng;i++){ if(G[i]>=N) continue; pred[i]+= c*p*exp((G[i]-1)*lq); } }
  // v=0 too: zeros occur too
  { double c=cnt[0],p=c/W,lq=log1p(-p); for(int i=0;i<ng;i++) pred[i]+=c*p*exp((G[i]-1)*lq); }
  printf("N=%ld window=%ld zeros_in_window=%u\n",N,W,cnt[0]);
  printf("%10s %12s %12s %8s\n","g","actual","poisson","ratio");
  for(int i=0;i<ng;i++){ if(G[i]>=N) continue; printf("%10ld %12u %12.1f %8.4f\n",G[i],cnt[G[i]],pred[i],cnt[G[i]]/pred[i]); }
  // top values
  printf("counts of small values: "); for(int v=0;v<=12;v++) printf("%d:%u ",v,cnt[v]); printf("\n");
  return 0;
}
