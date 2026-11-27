"""Cause or effect: are the choir seams written in the 7-nearest web before
anyone flashes?

Same perches, many runs. Each run draws new starting phases and (optionally)
new natural rates. If the seams belong to the graph, the same links should
end up crossing a choir border run after run, and a graph-only score should
pick them out in advance.

Per count-7 link (i listens to j, both in real choirs):
  crossing in run r?  -> how often, over R runs (link 'seam frequency')
Graph-only scores per link, computed before any run:
  overlap   : shared neighbours of i and j in the symmetrised 7-nearest graph
  spectral  : |difference| of the Fiedler-like coordinates of the first few
              eigenvectors of the normalised Laplacian (distance in spectral
              embedding)

usage: python cause.py PERCH_SEED RUNS MODE   (MODE = phases | both)
"""
import sys
import numpy as np
from scipy.sparse import csr_matrix, diags, identity
from scipy.sparse.linalg import eigsh
import firefly as ff
from borders import choir_labels


def run2(pos, lists, eps, rate_seed, phase_seed, periods=200, dt=0.002, spread=0.02):
    n = len(pos)
    seen_by = ff.invert(lists, n)
    rate = 1.0 + np.random.default_rng(rate_seed).normal(0, spread, n)
    phase = np.random.default_rng(10_000 + phase_seed).random(n)
    steps = int(periods / dt)
    last = np.zeros(n)
    for s in range(steps):
        t = s * dt
        phase += rate * dt
        if phase.max() < 1.0:
            continue
        fired = np.zeros(n, bool)
        queue = list(np.nonzero(phase >= 1.0)[0])
        while queue:
            j = queue.pop()
            if fired[j]:
                continue
            fired[j] = True
            phase[j] = 0.0
            h = seen_by[j]
            if len(h):
                h = h[~fired[h]]
                phase[h] *= (1.0 + eps)
                queue.extend(h[phase[h] >= 1.0].tolist())
        last[fired] = t
    return [[x] for x in last]


def ari(a, b):
    from scipy.special import comb
    _, ai = np.unique(a, return_inverse=True); _, bi = np.unique(b, return_inverse=True)
    M = np.zeros((ai.max()+1, bi.max()+1)); np.add.at(M, (ai, bi), 1)
    s = comb(M, 2).sum(); sa = comb(M.sum(1), 2).sum(); sb = comb(M.sum(0), 2).sum()
    e = sa * sb / comb(len(a), 2)
    return (s - e) / (0.5 * (sa + sb) - e)


def graph_scores(lists, n, k_eig=8):
    rows = np.repeat(np.arange(n), [len(l) for l in lists])
    cols = np.concatenate(lists)
    A = csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    S = ((A + A.T) > 0).astype(float)
    nb = [set(S[i].indices.tolist()) for i in range(n)]
    deg = np.asarray(S.sum(1)).ravel()
    Dm = diags(1 / np.sqrt(deg))
    L = identity(n) - Dm @ S @ Dm
    vals, vecs = eigsh(L.tocsc(), k=k_eig + 1, sigma=-1e-3, which="LM")
    o = np.argsort(vals)
    emb = (Dm @ vecs[:, o[1:]])
    emb /= np.linalg.norm(emb, axis=0)
    return nb, emb


if __name__ == "__main__":
    ps = int(sys.argv[1]); R = int(sys.argv[2]); mode = sys.argv[3]
    eps = 0.03
    pos = ff.perches(400, 100 + ps)
    lists = ff.listen_lists(pos, "count", 7)
    n = len(pos)
    edges = np.array([(i, j) for i, l in enumerate(lists) for j in l])
    cross = np.zeros(len(edges)); valid = np.zeros(len(edges))
    labs = []
    for r in range(R):
        rs = ps if mode == "phases" else 500 + r
        ft = run2(pos, lists, eps, rate_seed=rs, phase_seed=r)
        lab = choir_labels(ft)
        labs.append(lab)
        ok = (lab[edges[:, 0]] >= 0) & (lab[edges[:, 1]] >= 0)
        valid += ok
        cross += ok & (lab[edges[:, 0]] != lab[edges[:, 1]])
        print(f"run {r}: choirs {lab.max()+1}  sizes {sorted(np.bincount(lab[lab>=0]).tolist(), reverse=True)[:5]}", flush=True)
    np.save(f"cause_out/labs_p{ps}_{mode}.npy", np.array(labs))
    freq = np.where(valid > 0, cross / np.maximum(valid, 1), np.nan)
    np.save(f"cause_out/freq_p{ps}_{mode}.npy", freq)
    nb, emb = graph_scores(lists, n)
    overlap = np.array([len(nb[i] & nb[j]) for i, j in edges])
    spec = np.linalg.norm(emb[edges[:, 0]] - emb[edges[:, 1]], axis=1)
    m = ~np.isnan(freq)
    base = np.nanmean(freq)
    print(f"mean crossing per run {base:.3f}")
    # reproducibility: links that crossed in at least half the runs vs never
    print("seam frequency spread: never %.2f, 1-25%% %.2f, 25-50%% %.2f, >=50%% %.2f of links" % (
        np.mean(freq[m] == 0), np.mean((freq[m] > 0) & (freq[m] < .25)), np.mean((freq[m] >= .25) & (freq[m] < .5)), np.mean(freq[m] >= .5)))
    # null: if every link crossed independently at the base rate, fraction >=50%
    from scipy.stats import binom, spearmanr
    print("null (independent links, rate %.3f over %d runs): >=50%% expected %.4f" % (base, R, binom.sf(np.ceil(R/2)-1, R, base)))
    print("spearman freq vs overlap %.2f, vs spectral distance %.2f" % (spearmanr(freq[m], overlap[m])[0], spearmanr(freq[m], spec[m])[0]))
    # prediction: top 10%% of links by spectral distance -> what share of all crossings
    for name, sc, sign in (("spectral", spec, 1), ("low overlap", overlap, -1)):
        thr = np.quantile(sign * sc[m], 0.9)
        top = sign * sc[m] >= thr
        print(f"top 10% links by {name}: carry {freq[m][top].sum()/freq[m].sum():.2f} of crossings, mean freq {freq[m][top].mean():.3f} vs rest {freq[m][~top].mean():.3f}")
    # pairwise agreement between runs: of links crossing in run a, share crossing in run b
    agree = []
    for a in range(R):
        for b in range(R):
            if a == b: continue
            la, lb = labs[a], labs[b]
            ok = (la[edges[:,0]]>=0)&(la[edges[:,1]]>=0)&(lb[edges[:,0]]>=0)&(lb[edges[:,1]]>=0)
            ca = ok & (la[edges[:,0]]!=la[edges[:,1]]); cb = ok & (lb[edges[:,0]]!=lb[edges[:,1]])
            if ca.sum(): agree.append((ca&cb).sum()/ca.sum() / max(cb.sum()/ok.sum(), 1e-9))
    print(f"lift: P(cross in b | cross in a) / P(cross in b) = {np.mean(agree):.2f} (1 = no memory of place)")
    # null for the lift: random Voronoi patches, same number of choirs each draw
    from scipy.spatial import cKDTree
    rng = np.random.default_rng(ps)
    vl = []
    for lab in labs:
        k = lab.max() + 1
        _, v = cKDTree(rng.random((k, 2))).query(pos)
        vl.append(v)
    nagree = []
    for a in range(R):
        for b in range(R):
            if a == b: continue
            ca = vl[a][edges[:,0]] != vl[a][edges[:,1]]; cb = vl[b][edges[:,0]] != vl[b][edges[:,1]]
            nagree.append((ca&cb).sum()/max(ca.sum(),1) / max(cb.mean(), 1e-9))
    print(f"lift for random patches (link length alone): {np.mean(nagree):.2f}")
    length = np.linalg.norm(pos[edges[:,0]] - pos[edges[:,1]], axis=1)
    thr = np.quantile(length[m], 0.9); top = length[m] >= thr
    print(f"top 10% links by length: carry {freq[m][top].sum()/freq[m].sum():.2f} of crossings")
    # spectral clustering prediction vs choirs (adjusted Rand), against Voronoi null
    from scipy.cluster.vq import kmeans2
    sc_ari, null_ari, run_ari = [], [], []
    for r, lab in enumerate(labs):
        k = lab.max() + 1; ok = lab >= 0
        X = emb[:, :min(k, emb.shape[1])]
        best = None
        for t in range(10):
            c, pred = kmeans2(X, k, minit="++", seed=t)
            sse = ((X - c[pred]) ** 2).sum()
            if best is None or sse < best[0]: best = (sse, pred)
        sc_ari.append(ari(lab[ok], best[1][ok])); null_ari.append(ari(lab[ok], vl[r][ok]))
    for a in range(R):
        for b in range(a+1, R):
            ok = (labs[a] >= 0) & (labs[b] >= 0)
            run_ari.append(ari(labs[a][ok], labs[b][ok]))
    print(f"ARI choirs vs spectral clusters {np.mean(sc_ari):.2f}, vs random patches {np.mean(null_ari):.2f}, run vs run {np.mean(run_ari):.2f}")
