// Dump a(n) for n in [S, S+L) to file (uint32).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char**argv){
  long S=atol(argv[1]), L=atol(argv[2]); long N=S+L;
  uint32_t *last=calloc(N+1,4); uint32_t *buf=malloc(L*4); uint32_t a=0;
  for(long n=0;n<N-1;n++){
    uint32_t nx = last[a]? (uint32_t)(n-(last[a]-1)) : 0;
    last[a]=n+1; a=nx; long idx=n+1;
    if(idx>=S) buf[idx-S]=a;
  }
  FILE*f=fopen(argv[3],"wb"); fwrite(buf,4,L-1,f); fclose(f); return 0;
}
