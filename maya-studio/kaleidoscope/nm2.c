// Nowak-May spatial prisoner's dilemma, synchronous, Moore neighbourhood + self.
// usage: nm L steps f0 seed periodic(0/1) single(0/1) every [dumpfile dumpstep...]
// f0 = starting cooperator share (random mode); single=1: all C except centre D.
// prints "t f" every `every` steps; dumps grid (bytes: 0 C stay,1 D stay,2 D->C,3 C->D) at listed steps.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t s;
static inline uint64_t rnd(void){ s ^= s<<13; s ^= s>>7; s ^= s<<17; return s; }

int main(int argc, char **argv){
    int L = atoi(argv[1]); long steps = atol(argv[2]); double f0 = atof(argv[3]);
    s = 88172645463325252ULL ^ (uint64_t)atol(argv[4])*0x9E3779B97F4A7C15ULL;
    int per = atoi(argv[5]); int single = atoi(argv[6]); long every = atol(argv[7]);
    const char *dumpf = argc > 8 ? argv[8] : NULL;
    int ndump = argc > 9 ? argc - 9 : 0;
    long *dumps = malloc(sizeof(long)*(ndump+1));
    for (int i=0;i<ndump;i++) dumps[i] = atol(argv[9+i]);
    FILE *df = dumpf ? fopen(dumpf, "wb") : NULL;
    const double b = getenv("NM_B") ? atof(getenv("NM_B")) : 1.9; int selfp = getenv("NM_NOSELF") ? 0 : 1;
    size_t N = (size_t)L*L;
    uint8_t *x = malloc(N), *y = malloc(N), *prev = malloc(N);
    int *k = malloc(sizeof(int)*N);   // number of C in 3x3 block
    double *p = malloc(sizeof(double)*N);
    for (rnd(),rnd(); 0;);
    for (size_t i=0;i<N;i++){
        if (single) x[i] = 1; // 1 = C
        else x[i] = ((rnd()>>11) * (1.0/9007199254740992.0)) < f0;
    }
    if (single) x[(size_t)(L/2)*L + L/2] = 0;
    memcpy(prev, x, N);
    for (long t=0; t<=steps; t++){
        // report
        if (t % every == 0){
            long c=0; for (size_t i=0;i<N;i++) c += x[i];
            printf("%ld %.7f\n", t, (double)c/N);
        }
        for (int d=0; d<ndump; d++) if (dumps[d]==t && df){
            uint8_t *o = malloc(N);
            for (size_t i=0;i<N;i++){
                int a=prev[i], c=x[i];
                o[i] = (a&&c)?0 : (!a&&!c)?1 : (!a&&c)?2 : 3;
            }
            fwrite(&t, sizeof(long), 1, df); fwrite(o,1,N,df); free(o);
        }
        if (t==steps) break;
        // count cooperators in each 3x3 block
        for (int r=0;r<L;r++) for (int q=0;q<L;q++){
            int c=0;
            for (int dr=-1;dr<=1;dr++) for (int dq=-1;dq<=1;dq++){
                int rr=r+dr, qq=q+dq;
                if (per){ rr=(rr+L)%L; qq=(qq+L)%L; }
                else if (rr<0||rr>=L||qq<0||qq>=L) continue;
                c += x[(size_t)rr*L+qq];
            }
            k[(size_t)r*L+q]=c;
            p[(size_t)r*L+q] = x[(size_t)r*L+q] ? (double)(c - (selfp?0:1)) : b*c;
        }
        for (int r=0;r<L;r++) for (int q=0;q<L;q++){
            size_t i=(size_t)r*L+q; double best=p[i]; uint8_t st=x[i];
            for (int dr=-1;dr<=1;dr++) for (int dq=-1;dq<=1;dq++){
                int rr=r+dr, qq=q+dq;
                if (per){ rr=(rr+L)%L; qq=(qq+L)%L; }
                else if (rr<0||rr>=L||qq<0||qq>=L) continue;
                size_t j=(size_t)rr*L+qq;
                if (p[j] > best){ best=p[j]; st=x[j]; }
            }
            y[i]=st;
        }
        memcpy(prev, x, N);
        uint8_t *tmp=x; x=y; y=tmp;
    }
    if (df) fclose(df);
    return 0;
}
