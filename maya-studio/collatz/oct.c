// Collatz total stopping time (standard steps) for n < 2^K, with memo for n < 2^MEMO.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#define K 31
#define MEMO 28
#define MAXS 2000
int main(){
  uint16_t *s = malloc(sizeof(uint16_t)*(1ULL<<MEMO));
  s[1]=0;
  static double sum[K+1], sum2[K+1], sum3[K+1];
  static uint64_t cnt[K+1];
  static uint64_t hist[K+1][MAXS];
  int rec=-1; int nrec=0;
  FILE *fr=fopen("records.tsv","w");
  for(uint64_t n=1;n<(1ULL<<K);n++){
    uint64_t m=n; int st=0;
    while(m>=n || m>=(1ULL<<MEMO)){
      if(m==1) break;
      if(m&1) m=3*m+1; else m>>=1;
      st++;
      if(m<n && m<(1ULL<<MEMO)) break;
    }
    if(m!=1 || n==1) st += s[m]; 
    if(n<(1ULL<<MEMO)) s[n]=st;
    int k=63-__builtin_clzll(n);
    sum[k]+=st; sum2[k]+=(double)st*st; sum3[k]+=(double)st*st*st; cnt[k]++;
    if(st<MAXS) hist[k][st]++;
    if(st>rec){rec=st;nrec++;fprintf(fr,"%llu\t%d\n",(unsigned long long)n,st);}
  }
  fclose(fr);
  FILE *f=fopen("octaves.tsv","w");
  fprintf(f,"k\tcount\tmean\tsd\tskew\tmean_over_ln\tsd_over_sqrtln\n");
  for(int k=0;k<K;k++){
    double c=cnt[k], mu=sum[k]/c, var=sum2[k]/c-mu*mu;
    double sk = var>0 ? (sum3[k]/c - 3*mu*var - mu*mu*mu)/pow(var,1.5) : 0;
    double lnm = log(pow(2,k)*1.5);
    fprintf(f,"%d\t%.0f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n",k,c,mu,sqrt(var),sk,mu/lnm,sqrt(var)/sqrt(lnm));
  }
  fclose(f);
  FILE *fh=fopen("hist.tsv","w");
  for(int k=0;k<K;k++){for(int t=0;t<MAXS;t++) if(hist[k][t]) fprintf(fh,"%d\t%d\t%llu\n",k,t,(unsigned long long)hist[k][t]);}
  fclose(fh);
  printf("records %d\n",nrec);
  return 0;
}
