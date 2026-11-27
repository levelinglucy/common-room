// A104737 (records of Seidov's prime queue): r <- 1; for x = k-1..1: r += ceil(r / s(x)), s(x) = p_x - x + 1.
// Leonov (Zenodo, 3 Nov 2026) Open question 3: growth of A104737 (moduli ~ x log x, outside his linear theorem).
// Prints exact T(k), and the two-phase prediction  (k - pi(k) + 1) * prod_{x < pi(k)} (1 + 1/s(x)).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

int main(int argc, char **argv) {
    long K = argc > 1 ? atol(argv[1]) : 100000000L;   // largest k
    // need p_x for x < K: p_K < K (ln K + ln ln K) for K >= 6
    double lk = log((double)K);
    long N = (long)(K * (lk + log(lk))) + 100;
    uint8_t *comp = calloc(N / 2 + 1, 1);
    for (long i = 3; i * i <= N; i += 2) if (!comp[i / 2]) for (long j = i * i; j <= N; j += 2 * i) comp[j / 2] = 1;
    int64_t *s = malloc(sizeof(int64_t) * (K + 1));
    long x = 1; s[1] = 2 - 1 + 1;  // p_1 = 2
    for (long n = 3; n <= N && x < K; n += 2) if (!comp[n / 2]) { x++; s[x] = n - x + 1; }
    if (x < K) { fprintf(stderr, "not enough primes\n"); return 1; }
    // check first terms
    for (long k = 1; k <= 12; k++) { int64_t r = 1; for (long y = k - 1; y >= 1; y--) r += (r + s[y] - 1) / s[y]; printf("%lld,", (long long)r); }
    printf("\n");
    // targets: k = 10^3 .. K at quarter decades
    // prefix log-product and pi(k) via prime counting array not stored: compute pi(k) by binary search on p_x = s[x] + x - 1
    printf("k T(k) pred T/pred T/(k ln k) prod/ln(pi k)\n");
    for (double e = 3.0; e <= log10((double)K) + 1e-9; e += 0.25) {
        long k = (long)llround(pow(10, e));
        int64_t r = 1; for (long y = k - 1; y >= 1; y--) r += (r + s[y] - 1) / s[y];
        long lo = 0, hi = K; // largest x with p_x <= k
        while (lo < hi) { long m = (lo + hi + 1) / 2; if (s[m] + m - 1 <= k) lo = m; else hi = m - 1; }
        long pk = lo;
        long double lp = 0; for (long y = 1; y < pk; y++) lp += log1pl(1.0L / s[y]);
        long double pred = (k - pk + 1) * expl(lp);
        printf("%ld %lld %.6Lf %.6Lf %.6f B~%.6Lf (r/pred-1)lnk=%.4Lf\n", k, (long long)r, pred, r / pred, r / (k * log((double)k)), expl(lp)/logl((long double)pk), (r/pred-1)*logl((long double)k));
        fflush(stdout);
    }
    return 0;
}
