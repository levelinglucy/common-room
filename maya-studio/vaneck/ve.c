// Van Eck sequence to N terms. Prints checkpoint stats.
// last[v] = 1 + last index where v occurred before current position (0 = never).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
int main(int argc,char**argv){
  long N = atol(argv[1]);
  uint32_t *last = calloc(N+1, sizeof(uint32_t));
  uint32_t *first = calloc(N+1, sizeof(uint32_t)); // first index+1 where v appears
  FILE *fz = fopen(argc>2?argv[2]:"zeros.bin","wb");
  long zeros=0, ones=0, maxv=0, mex=1; // mex: smallest positive value not yet seen
  uint32_t a=0; first[0]=1;
  long cp=1000;
  for(long n=0;n<N;n++){
    uint32_t nxt;
    if(last[a]) nxt = (uint32_t)(n - (last[a]-1)); else nxt=0;
    last[a]=(uint32_t)(n+1);
    a=nxt;
    long idx=n+1;
    if(a==0){zeros++; fwrite(&idx,4,1,fz);} // index of zero (low 32 bits)
    if(a==1)ones++;
    if(a>maxv)maxv=a;
    if(!first[a]) first[a]=(uint32_t)(idx+1);
    while(mex<=N && first[mex]) mex++;
    if(idx==cp){
      double L=log((double)idx);
      printf("N=%ld zeros=%ld Z*lnN/N=%.5f ones=%ld ones/zeros=%.4f max=%ld max/N=%.4f mex=%ld distinct_frac=%.5f\n",
        idx,zeros,zeros*L/idx,ones,(double)ones/zeros,maxv,(double)maxv/idx,mex,(double)(zeros+1)/idx);
      fflush(stdout);
      cp*=10; if(cp>N)cp=N;
      if(idx==N)break;
    }
  }
  // first appearance of v for sample values
  FILE *ff=fopen("first.bin","wb"); fwrite(first,4,(N<20000001?N:20000001),ff); fclose(ff);
  fclose(fz);
  return 0;
}
