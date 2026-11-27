// Nowak-May spatial PD with four wall types, on a padded grid (ghost ring).
// usage: nm4 L steps f0 seed mode every accfile
// mode: A absent walls (same as nm3 per=0), M mirror walls, V absent walls + average payoff,
//       D ring of permanent defectors outside, P periodic (control).
// prints "t f" every `every` steps; writes the per-cell time-average of C from step 500 to accfile.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

static uint64_t s;
static inline uint64_t rnd(void){ s ^= s<<13; s ^= s>>7; s ^= s<<17; return s; }

int main(int argc, char **argv){
    int L = atoi(argv[1]); long steps = atol(argv[2]); double f0 = atof(argv[3]);
    s = 88172645463325252ULL ^ (uint64_t)atol(argv[4])*0x9E3779B97F4A7C15ULL;
    char mode = argv[5][0]; long every = atol(argv[6]); const char *accf = argv[7];
    const double b = getenv("NM_B") ? atof(getenv("NM_B")) : 1.9;
    int W = L + 2;                 // padded width
    size_t NP = (size_t)W*W;
    uint8_t *x = calloc(NP,1), *y = calloc(NP,1);
    double *p = malloc(sizeof(double)*NP);
    uint8_t *real = calloc(NP,1);  // 1 for an in-grid cell
    #define IX(r,q) ((size_t)((r)+1)*W + ((q)+1))
    for (int r=0;r<L;r++) for (int q=0;q<L;q++) real[IX(r,q)] = 1;
    rnd(); rnd();   // nm3 burns two draws before filling
    // same random fill order as nm3
    for (int r=0;r<L;r++) for (int q=0;q<L;q++)
        x[IX(r,q)] = ((rnd()>>11) * (1.0/9007199254740992.0)) < f0;
    double *acc = calloc((size_t)L*L, sizeof(double)); long nacc = 0;
    // number of real cells in each real cell's block (for V)
    int *nb = malloc(sizeof(int)*NP);
    for (int r=0;r<L;r++) for (int q=0;q<L;q++){
        int n=0; for (int dr=-1;dr<=1;dr++) for (int dq=-1;dq<=1;dq++){
            int rr=r+dr, qq=q+dq; if (rr>=0&&rr<L&&qq>=0&&qq<L) n++; }
        nb[IX(r,q)] = n;
    }
    // map ghost -> source real cell, for M (reflection about the boundary) and P (wrap)
    long *src = malloc(sizeof(long)*NP);
    for (int r=-1;r<=L;r++) for (int q=-1;q<=L;q++){
        int rr=r, qq=q;
        if (mode=='M'){ if (rr<0) rr=0; if (rr>=L) rr=L-1; if (qq<0) qq=0; if (qq>=L) qq=L-1; }
        else { rr=(rr+L)%L; qq=(qq+L)%L; }
        src[IX(r,q)] = (long)IX(rr,qq);
    }
    for (long t=0; t<=steps; t++){
        if (t % every == 0){
            long c=0; for (int r=0;r<L;r++) for (int q=0;q<L;q++) c += x[IX(r,q)];
            printf("%ld %.7f\n", t, (double)c/((double)L*L));
        }
        if (t>=500){ for (int r=0;r<L;r++) for (int q=0;q<L;q++) acc[(size_t)r*L+q] += x[IX(r,q)]; nacc++; }
        if (t==steps) break;
        // ghost states
        for (int r=-1;r<=L;r++) for (int q=-1;q<=L;q++){
            size_t i = IX(r,q); if (real[i]) continue;
            if (mode=='M' || mode=='P') x[i] = x[src[i]];
            else x[i] = 0;          // A, V: nothing there (counts no C); D: a defector
        }
        // scores of real cells
        for (int r=0;r<L;r++) for (int q=0;q<L;q++){
            size_t i = IX(r,q); int c = 0;
            for (int dr=-1;dr<=1;dr++) for (int dq=-1;dq<=1;dq++) c += x[i + (long)dr*W + dq];
            double sc = x[i] ? (double)c : b*c;
            if (mode=='V') sc /= nb[i];
            p[i] = sc;
        }
        // scores of ghosts
        for (int r=-1;r<=L;r++) for (int q=-1;q<=L;q++){
            size_t i = IX(r,q); if (real[i]) continue;
            if (mode=='M' || mode=='P') p[i] = p[src[i]];
            else if (mode=='D'){
                int c=0; for (int dr=-1;dr<=1;dr++) for (int dq=-1;dq<=1;dq++){
                    int rr=r+dr, qq=q+dq; if (rr<-1||rr>L||qq<-1||qq>L) continue;
                    c += x[IX(rr,qq)]; }
                p[i] = b*c;
            } else p[i] = -INFINITY;
        }
        // copy the best in the block (strict >, own first, same scan order as nm3)
        for (int r=0;r<L;r++) for (int q=0;q<L;q++){
            size_t i = IX(r,q); double best = p[i]; uint8_t st = x[i];
            for (int dr=-1;dr<=1;dr++) for (int dq=-1;dq<=1;dq++){
                size_t j = i + (long)dr*W + dq;
                if (p[j] > best){ best = p[j]; st = x[j]; }
            }
            y[i] = st;
        }
        for (int r=0;r<L;r++) for (int q=0;q<L;q++) x[IX(r,q)] = y[IX(r,q)];
    }
    if (accf && nacc){ for (size_t i=0;i<(size_t)L*L;i++) acc[i]/=nacc;
        FILE *a=fopen(accf,"wb"); fwrite(acc,sizeof(double),(size_t)L*L,a); fclose(a); }
    return 0;
}
