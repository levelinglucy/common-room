// ulam.c: generate the Ulam sequence U(a,b) up to value VMAX.
// usage: ./ulam a b VMAX > terms.txt
// counts[s] = number of ways s is a sum of two distinct terms so far (capped at 2).
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: ulam a b VMAX\n"); return 1; }
    long a = atol(argv[1]), b = atol(argv[2]), V = atol(argv[3]);
    unsigned char *cnt = calloc(2 * V + 2, 1);
    long cap = 1 << 20, n = 0;
    long *u = malloc(cap * sizeof(long));
    u[n++] = a; u[n++] = b;
    cnt[a + b] = 1;
    long last = b;
    for (long x = b + 1; x <= V; x++) {
        if (cnt[x] != 1) continue;
        // x is the next term
        if (n == cap) { cap *= 2; u = realloc(u, cap * sizeof(long)); }
        for (long i = 0; i < n; i++) {
            long s = u[i] + x;
            if (s > V) break; // terms are increasing
            if (cnt[s] < 2) cnt[s]++;
        }
        u[n++] = x;
        last = x;
    }
    for (long i = 0; i < n; i++) printf("%ld\n", u[i]);
    fprintf(stderr, "U(%ld,%ld): %ld terms up to %ld, last %ld\n", a, b, n, V, last);
    return 0;
}
