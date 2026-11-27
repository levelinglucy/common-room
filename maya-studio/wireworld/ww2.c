// Event-driven WireWorld: only heads do work.
// usage: ww2 in.raw H W gens snap_every outprefix [y0 y1 x0 x1]
// Snapshots (every snap_every gens, and final) write only the window y0..y1, x0..x1
// (default whole grid) as outprefix_<gen>.raw.
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage\n"); return 1; }
    int H = atoi(argv[2]), W = atoi(argv[3]);
    long gens = atol(argv[4]), snap = atol(argv[5]);
    const char *pre = argv[6];
    int y0 = 0, y1 = H - 1, x0 = 0, x1 = W - 1;
    if (argc >= 11) { y0 = atoi(argv[7]); y1 = atoi(argv[8]); x0 = atoi(argv[9]); x1 = atoi(argv[10]); }
    unsigned char *g = malloc(H * W);
    FILE *f = fopen(argv[1], "rb");
    if (fread(g, 1, H * W, f) != (size_t)(H * W)) { fprintf(stderr, "short\n"); return 1; }
    fclose(f);
    int *hd = malloc(sizeof(int) * H * W), *tl = malloc(sizeof(int) * H * W);
    int *nh = malloc(sizeof(int) * H * W), *cand = malloc(sizeof(int) * H * W);
    unsigned char *cnt = calloc(H * W, 1);
    int nH = 0, nT = 0;
    for (int i = 0; i < H * W; i++) { if (g[i] == 1) hd[nH++] = i; else if (g[i] == 2) tl[nT++] = i; }
    int off[8], o = 0;
    for (int dy = -1; dy <= 1; dy++) for (int dx = -1; dx <= 1; dx++) if (dy || dx) off[o++] = dy * W + dx;
    // pattern has an empty border, so i+off stays in range for live cells
    char name[512];
    unsigned char *win = malloc((y1 - y0 + 1) * (x1 - x0 + 1));
    for (long gen = 1; gen <= gens; gen++) {
        int nc = 0;
        for (int a = 0; a < nH; a++) {
            int i = hd[a];
            for (int c = 0; c < 8; c++) {
                int j = i + off[c];
                if (g[j] == 3) { if (cnt[j]++ == 0) cand[nc++] = j; }
            }
        }
        int nn = 0;
        for (int a = 0; a < nc; a++) { int j = cand[a]; if (cnt[j] <= 2) nh[nn++] = j; cnt[j] = 0; }
        for (int a = 0; a < nT; a++) g[tl[a]] = 3;
        for (int a = 0; a < nH; a++) g[hd[a]] = 2;
        for (int a = 0; a < nn; a++) g[nh[a]] = 1;
        int *tmp = tl; tl = hd; nT = nH; hd = nh; nH = nn; nh = tmp;
        if ((snap && gen % snap == 0) || gen == gens) {
            int k = 0;
            for (int y = y0; y <= y1; y++) for (int x = x0; x <= x1; x++) win[k++] = g[y * W + x];
            snprintf(name, sizeof name, "%s_%ld.raw", pre, gen);
            FILE *out = fopen(name, "wb"); fwrite(win, 1, k, out); fclose(out);
        }
    }
    return 0;
}
