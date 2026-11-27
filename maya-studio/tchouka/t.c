#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int c,char**v){long N=atol(v[1]);int M=200000;long*b=calloc(M,sizeof(long));long l=0;
long chk=1000;
for(long n=1;n<=N;n++){int i=0;while(b[i])i++;for(int j=0;j<i;j++)b[j]--;b[i]=i+1;if(i+1>l)l=i+1;
 if(n==chk){printf("%ld %ld %.6f\n",n,l,(double)l*l/n);chk*=10;}
}
// profile
FILE*f=fopen("profile.txt","w");for(int k=0;k<l;k++)fprintf(f,"%d %ld\n",k+1,b[k]);fclose(f);}
