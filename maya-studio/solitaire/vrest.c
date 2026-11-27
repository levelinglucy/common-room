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
static int maxd2; static long long n2;
static int chain[MAXN*MAXN][MAXN+1], clen[MAXN*MAXN], cdepth;
static int ex2[MAXN+1], ex2len;
static int cmpdesc(const void *a, const void *b){ return *(int*)b - *(int*)a; }
static int fwd(const int *p, int L, int *q){ int t=0; for(int i=0;i<L;i++) if(p[i]>1) q[t++]=p[i]-1; q[t++]=L; qsort(q,t,sizeof(int),cmpdesc); return t; }
static int on_chain(const int *mu, int L, int depth){ int i = cdepth - depth; if (i < 0) return 0; if (clen[i]!=L) return 0; return memcmp(chain[i], mu, L*sizeof(int))==0; }

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
    visited++;
    if (depth > maxd) { maxd = depth; ndeep = 0; memcpy(ex, mu, L * sizeof(int)); exlen = L; }
    if (depth == maxd) ndeep++;
    if (L == N) onesdepth = depth; /* all ones */
    if (!on_chain(mu, L, depth)) { if (depth > maxd2) { memcpy(ex2, mu, L*sizeof(int)); ex2len = L; } if (depth > maxd2) { maxd2 = depth; n2 = 0; } if (depth == maxd2) n2++; }
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
    int nmin = atoi(argv[1]), nmax = atoi(argv[2]);
    static long long P[MAXN + 1];
    P[0] = 1;
    for (int part = 1; part <= MAXN; part++)
        for (int s = part; s <= MAXN; s++) P[s] += P[s - part];
    printf("n k r maxT formula match visited p(n) n_deepest ones_depth example\n");
    for (N = nmin; N <= nmax; N++) {
        K = 0; while ((K + 1) * (K + 2) / 2 <= N) K++;
        R = N - K * (K + 1) / 2;
        { int L=N; for(int i=0;i<N;i++) chain[0][i]=1; clen[0]=N; int c=0; while(!is_cycle(chain[c],clen[c])){ clen[c+1]=fwd(chain[c],clen[c],chain[c+1]); c++; } cdepth=c; }
        visited = 0; maxd2 = -1; n2 = 0; maxd = -1; ndeep = 0; onesdepth = -1;
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
        printf("%d %d %d %d %d %s %lld %lld %lld %d small:%d,%lld (", N, K, R, maxd, f,
               f == maxd ? "OK" : "MISS", visited, P[N], ndeep, onesdepth, maxd2, n2);
        for (int i = 0; i < exlen; i++) printf("%d%s", ex[i], i + 1 < exlen ? "," : "");
        printf(") rest_ex(");
        for (int i = 0; i < ex2len; i++) printf("%d%s", ex2[i], i + 1 < ex2len ? "," : "");
        printf(")\n");
        fflush(stdout);
    }
    return 0;
}
