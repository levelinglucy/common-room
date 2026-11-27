// Hofstadter Q to N, with per-bin stats. Usage: ./q LOG2N
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
int main(int argc,char**argv){
  int L=atoi(argv[1]); uint64_t N=1ULL<<L;
  uint32_t *Q=malloc((N+1)*sizeof(uint32_t)); if(!Q){printf("oom\n");return 1;}
  Q[1]=1;Q[2]=1;
  // bins: 16 per octave, from n=2^6
  int NB=16*L+16; double *s1=calloc(NB,8),*s2=calloc(NB,8),*sa=calloc(NB,8),*sb=calloc(NB,8),*ev=calloc(NB,8),*same=calloc(NB,8),*cnt=calloc(NB,8);
  FILE*f=fopen("envelope.tsv","w");
  uint64_t B=4096; double mx=-1e18,mn=1e18;
  for(uint64_t n=3;n<=N;n++){
    uint64_t a=n-Q[n-1], b=n-Q[n-2];
    if(Q[n-1]>=n||Q[n-2]>=n){printf("undefined at %llu\n",(unsigned long long)n);return 0;}
    Q[n]=Q[a]+Q[b];
    double d=(double)Q[n]-n/2.0;
    if(d>mx)mx=d; if(d<mn)mn=d;
    if(n%B==0){fprintf(f,"%llu\t%.1f\t%.1f\n",(unsigned long long)n,mn,mx);mx=-1e18;mn=1e18;}
    if(n>=64){int k=(int)floor(16*log2((double)n)); 
      s1[k]+=d; s2[k]+=d*d; sa[k]+=(double)a/n; sb[k]+=(double)b/n; ev[k]+=(Q[n]&1)==0; same[k]+=(a==b); cnt[k]++;}
  }
  fclose(f);
  FILE*g=fopen("bins.tsv","w");
  fprintf(g,"log2n\tcount\tmean_d\trms_d\tlook_a\tlook_b\teven\tsame\n");
  for(int k=0;k<NB;k++) if(cnt[k]>0){double c=cnt[k];
    fprintf(g,"%.4f\t%.0f\t%.3f\t%.3f\t%.5f\t%.5f\t%.5f\t%.6f\n",k/16.0,c,s1[k]/c,sqrt(s2[k]/c),sa[k]/c,sb[k]/c,ev[k]/c,same[k]/c);}
  fclose(g);
  printf("done N=2^%d Q(N)=%u\n",L,Q[N]);
  FILE*h=fopen("q_first_1M.bin","wb"); fwrite(Q,4,(1<<20)+1,h); fclose(h);
  return 0;}
