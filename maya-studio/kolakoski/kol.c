/* Kolakoski (a,b) sequence by lazy self-reading levels (Nilsson-style), O(log N) memory.
   Level k's run lengths are read from level k+1's output (a fresh copy of the same sequence).
   A prefix P (first PR runs, built directly) bootstraps every level.
   Prints the sequence (mode 'p') or statistics (mode 's'): count of a, and the walk
   D(n) = #a - #b sampled max |D| in each [2^j, 2^(j+1)).
   usage: ./kol a b N mode
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAXL 256
#define PMAX 4096
static int A, B, P[PMAX], plen, PR;
typedef struct { long long idx; long long run; int rem, sym, started; } Lv;
static Lv lv[MAXL];

static int nxt(int k) {
    Lv *l = &lv[k];
    if (k >= MAXL - 1) { fprintf(stderr, "too deep\n"); exit(1); }
    if (l->idx < plen) return P[l->idx++];
    if (l->rem == 0) {
        if (!l->started) { l->started = 1; for (int j = 0; j < PR; j++) nxt(k + 1); }
        l->rem = nxt(k + 1);
        l->sym = (l->run % 2 == 0) ? A : B;
        l->run++;
    }
    l->rem--; l->idx++;
    return l->sym;
}

int main(int argc, char **argv) {
    A = atoi(argv[1]); B = atoi(argv[2]);
    long long N = atoll(argv[3]);
    char mode = argv[4][0];
    /* direct prefix: runs until plen >= 1000 */
    int s[PMAX]; int n = 0, i = 0;
    while (n < 1000) {
        int sym = (i % 2 == 0) ? A : B;
        int L = (i < n) ? s[i] : sym;
        for (int j = 0; j < L; j++) s[n++] = sym;
        i++;
    }
    memcpy(P, s, n * sizeof(int)); plen = n; PR = i;
    for (int k = 0; k < MAXL; k++) { lv[k].idx = 0; lv[k].run = PR; lv[k].rem = 0; lv[k].started = 0; }
    if (mode == 'p') {
        for (long long t = 0; t < N; t++) putchar('0' + nxt(0));
        putchar('\n');
        return 0;
    }
    long long ca = 0, D = 0, mx = 0; int j = 0; long long next2 = 2;
    int depth = 0; double rho = argc > 5 ? atof(argv[5]) : 0, emax = 0;
    for (long long t = 1; t <= N; t++) {
        int x = nxt(0);
        if (x == A) { ca++; D++; } else D--;
        if (rho > 0) { double e = ca - rho * t; if (fabs(e) > emax) emax = fabs(e); }
        long long ad = D < 0 ? -D : D;
        if (ad > mx) mx = ad;
        if (t + 1 == next2) {
            for (depth = 0; depth < MAXL && lv[depth].idx > 0; depth++);
            printf("n=2^%d  #a/n=%.9f  D=%lld  max|D| in [2^%d,2^%d)=%lld  levels=%d\n", j + 1, (double)ca / t, D, j, j + 1, mx, depth);
            fflush(stdout);
            if (rho > 0) printf("   max|#a - rho n| so far = %.4f\n", emax);
            mx = 0; j++; next2 *= 2;
        }
    }
    return 0;
}
