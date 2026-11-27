// WireWorld runner on the conductor list only.
// usage: ww in.raw H W gens snap_every outprefix
// in.raw: H*W uint8 states (0 empty,1 head,2 tail,3 copper).
// Writes outprefix_<gen>.raw snapshots every snap_every gens (0 = only final).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage\n"); return 1; }
    int H = atoi(argv[2]), W = atoi(argv[3]);
    long gens = atol(argv[4]), snap = atol(argv[5]);
    const char *pre = argv[6];
    unsigned char *g = malloc(H * W);
    FILE *f = fopen(argv[1], "rb");
    if (fread(g, 1, H * W, f) != (size_t)(H * W)) { fprintf(stderr, "short\n"); return 1; }
    fclose(f);
    int *idx = malloc(sizeof(int) * H * W);
    int N = 0;
    for (int i = 0; i < H * W; i++) idx[i] = g[i] ? N++ : -1;
    int *nb = malloc(sizeof(int) * 8 * N);
    int *cell = malloc(sizeof(int) * N);
    unsigned char *s = malloc(N), *t = malloc(N);
    for (int y = 0; y < H; y++) for (int x = 0; x < W; x++) {
        int i = y * W + x; if (idx[i] < 0) continue;
        int k = idx[i], c = 0; cell[k] = i; s[k] = g[i];
        for (int dy = -1; dy <= 1; dy++) for (int dx = -1; dx <= 1; dx++) {
            if (!dy && !dx) continue;
            int yy = y + dy, xx = x + dx;
            int j = (yy >= 0 && yy < H && xx >= 0 && xx < W) ? idx[yy * W + xx] : -1;
            nb[8 * k + c++] = j;
        }
    }
    char name[512];
    for (long gen = 1; gen <= gens; gen++) {
        for (int k = 0; k < N; k++) {
            unsigned char v = s[k];
            if (v == 1) t[k] = 2;
            else if (v == 2) t[k] = 3;
            else {
                int h = 0;
                for (int c = 0; c < 8; c++) { int j = nb[8 * k + c]; if (j >= 0 && s[j] == 1) h++; }
                t[k] = (h == 1 || h == 2) ? 1 : 3;
            }
        }
        unsigned char *tmp = s; s = t; t = tmp;
        if ((snap && gen % snap == 0) || gen == gens) {
            for (int k = 0; k < N; k++) g[cell[k]] = s[k];
            snprintf(name, sizeof name, "%s_%ld.raw", pre, gen);
            FILE *o = fopen(name, "wb"); fwrite(g, 1, H * W, o); fclose(o);
        }
    }
    return 0;
}
