/* Bulgarian solitaire: longest trip to the cycle, by walking the tree backwards.
 * Outside the cycles every partition has exactly one successor, so the
 * partitions hanging off the cycles form trees: a DFS over predecessors
 * visits each partition once, with no visited set.
 *
 * Predecessors of mu (parts sorted desc, length L): pick a part value m of mu
 * with m >= L-1, remove one copy, add 1 to every other part, append m-(L-1) ones.
 * Cycle states for n = T_k + r: sorted parts p_i = (k+1-i) + d_i, d_i in {0,1},
 * i = 1..k+1 (Brandt).
 *
 * usage: ./vtree NMIN NMAX
 * prints: n k r maxdepth formula match visited p(n) count_deepest ones_depth example
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 200
static int N, K, R;
static long long visited, ndeep;
static int maxd;
static int ex[MAXN + 1], exlen;
static int onesdepth;
static long long hist[100000]; static int nshow=0, SHOW=12, TARGET=-1; static long long partsat[MAXN+1];

static int is_cycle(const int *p, int L) {
    if (L > K + 1) return 0;
    for (int i = 0; i < K + 1; i++) {
        int v = i < L ? p[i] : 0;
        int d = v - (K - i);
        if (d != 0 && d != 1) return 0;
    }
    return 1;
}

static void dfs(const int *mu, int L, int depth) {
    visited++; hist[depth]++;
    if (depth == TARGET) { partsat[L]++; if (nshow < SHOW && (nshow < SHOW/2 || L < 2*K)) { nshow++; printf("  deep:"); for (int i=0;i<L;i++) printf(" %d", mu[i]); printf("\n"); } }
    if (depth > maxd) { maxd = depth; ndeep = 0; memcpy(ex, mu, L * sizeof(int)); exlen = L; }
    if (depth == maxd) ndeep++;
    if (L == N) onesdepth = depth; /* all ones */
    int q[MAXN + 1];
    for (int j = 0; j < L; j++) {
        if (j > 0 && mu[j] == mu[j - 1]) continue; /* distinct values only */
        int m = mu[j];
        if (m < L - 1) break; /* sorted desc: later ones are smaller */
        int t = 0;
        for (int i = 0; i < L; i++) if (i != j) q[t++] = mu[i] + 1;
        for (int i = 0; i < m - (L - 1); i++) q[t++] = 1;
        if (depth == 0 && is_cycle(q, t)) continue; /* stay off the cycle */
        dfs(q, t, depth + 1);
    }
}

/* note: a predecessor of a non-cycle state is never a cycle state (the cycle
 * state's successor is on the cycle), so the cycle check is only needed at depth 0. */

int main(int argc, char **argv) {
    int nmin = atoi(argv[1]), nmax = nmin; TARGET = atoi(argv[2]);
    static long long P[MAXN + 1];
    P[0] = 1;
    for (int part = 1; part <= MAXN; part++)
        for (int s = part; s <= MAXN; s++) P[s] += P[s - part];
    printf("n k r maxT formula match visited p(n) n_deepest ones_depth example\n");
    for (N = nmin; N <= nmax; N++) {
        K = 0; while ((K + 1) * (K + 2) / 2 <= N) K++;
        R = N - K * (K + 1) / 2;
        visited = 0; maxd = -1; ndeep = 0; onesdepth = -1;
        int d[MAXN + 1], p[MAXN + 1];
        /* all 0/1 vectors of length K+1 with R ones */
        for (unsigned long mask = 0; mask < (1UL << (K + 1)); mask++) {
            if (__builtin_popcountl(mask) != R) continue;
            int L = 0;
            for (int i = 0; i < K + 1; i++) {
                d[i] = (mask >> i) & 1;
                int v = (K - i) + d[i];
                if (v > 0) p[L++] = v;
            }
            dfs(p, L, 0);
        }
        int down = K * (K - 1 - R);
        int up = K * (K + 1) - (K + 1 - R) * (K + 2);
        int fl = N - K;
        int f = down; if (up > f) f = up; if (fl > f) f = fl;
        printf("%d %d %d %d %d %s %lld %lld %lld %d (", N, K, R, maxd, f,
               f == maxd ? "OK" : "MISS", visited, P[N], ndeep, onesdepth);
        for (int i = 0; i < exlen; i++) printf("%d%s", ex[i], i + 1 < exlen ? "," : "");
        printf(")\n");
        for (int i=0;i<=maxd;i++) printf("H %d %lld\n", i, hist[i]);
        for (int i=0;i<=N;i++) if (partsat[i]) printf("P %d %lld\n", i, partsat[i]);
        fflush(stdout);
    }
    return 0;
}
