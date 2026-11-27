"""Fair test for borders.py: maybe count-7 crosses ANY patch border less,
simply because its links are short. Cut the same perches into random
patches (Voronoi around random centres, as many patches as the real choirs)
and compare the same ratio count7 / six-dir.
"""
import sys
import numpy as np
from scipy.spatial import cKDTree
import firefly as ff
from borders import choir_labels, crossing

nseeds = int(sys.argv[1])
rng = np.random.default_rng(5)
real, base = [], []
for sd in range(nseeds):
    pos = ff.perches(400, 100 + sd)
    ft, _, l7 = ff.run(pos, "count", 7, eps=0.03, periods=200, seed=sd)
    lab = choir_labels(ft)
    l6 = ff.listen_lists(pos, "sectors", 0)
    k = len(set(lab[lab >= 0].tolist()))
    real_c7, real_c6 = crossing(l7, lab), crossing(l6, lab)
    rb = []
    for t in range(50):
        cen = rng.random((k, 2))
        _, vl = cKDTree(cen).query(pos)
        rb.append((crossing(l7, vl), crossing(l6, vl)))
    rb = np.array(rb)
    real.append((real_c7, real_c6))
    base.append(rb.mean(0))
    print(f"seed {sd}: {k} choirs. real borders: count7 {real_c7:.3f} six-dir {real_c6:.3f} ratio {real_c7/real_c6:.2f} | "
          f"random patches: count7 {rb[:,0].mean():.3f} six-dir {rb[:,1].mean():.3f} ratio {np.mean(rb[:,0]/rb[:,1]):.2f}", flush=True)
real, base = np.array(real), np.array(base)
print("mean ratio count7/six-dir: real choirs %.2f, random patches %.2f" % ((real[:,0]/real[:,1]).mean(), (base[:,0]/base[:,1]).mean()))
print("mean count7 crossing: real %.3f vs random patches %.3f" % (real[:,0].mean(), base[:,0].mean()))
print("mean six-dir crossing: real %.3f vs random patches %.3f" % (real[:,1].mean(), base[:,1].mean()))
