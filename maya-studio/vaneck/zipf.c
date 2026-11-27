// Log-binned v*f(v) over window [N/2,N). Output: v_lo v_hi v_geo  v*f(v)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
int main(int argc,char**argv){
  long N=atol(argv[1]); long W=N-N/2;
  uint32_t *last=calloc(N+1,4), *cnt=calloc(N+1,4); uint32_t a=0;
  for(long n=0;n<N;n++){ uint32_t nx= last[a]?(uint32_t)(n-(last[a]-1)):0; last[a]=n+1; a=nx; if(n+1>=N/2) cnt[a]++; }
  printf("# N=%ld W=%ld zeros=%u\n",N,W,cnt[0]);
  for(int v=1;v<=20;v++) printf("%d %d %.3f %.6f\n",v,v,(double)v,(double)v*cnt[v]/W);
  double r=pow(10,0.1); double lo=21;
  while(lo<N){ long l=(long)lo, h=(long)(lo*r); if(h>N)h=N; double s=0; for(long v=l; v<h; v++) s+=cnt[v];
    double geo=sqrt((double)l*h); printf("%ld %ld %.1f %.6f\n",l,h-1,geo, s/W/(h-l)*geo); lo=lo*r; }
  return 0;
}
