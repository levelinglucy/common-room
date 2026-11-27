"""Do choirs sit where the 7-nearest graph is thin?

Run count-7 (square), find its choirs. Then, keeping that same split of the
forest into choirs, ask how many listening links cross a choir border under
the count-7 graph and under the six-directions graph on the same perches.
If count-7's borders are quiet (few links across) and six-directions would
have had many, the choirs are held by the graph, not by the flashing.

usage: python borders.py SEEDS [EPS]
"""
import sys
import numpy as np
import firefly as ff


def choir_labels(flash_times, tol=0.01, min_size=5):
    last = np.array([ft[-1] for ft in flash_times])
    order = np.argsort(last)
    lab = np.full(len(last), -1)
    c = 0
    lab[order[0]] = c
    for a, b in zip(order[:-1], order[1:]):
        if last[b] - last[a] >= tol:
            c += 1
        lab[b] = c
    sizes = np.bincount(lab)
    lab[sizes[lab] < min_size] = -1
    return lab


def crossing(lists, lab):
    """For fireflies in a real choir: links that land in a different real choir."""
    tot = cross = 0
    border = 0
    per_border = []
    for i, l in enumerate(lists):
        if lab[i] < 0:
            continue
        l = l[lab[l] >= 0]
        k = int((lab[l] != lab[i]).sum())
        tot += len(l)
        cross += k
    return cross / max(tot, 1)


def mutual(lists):
    s = [set(l.tolist()) for l in lists]
    m = sum(1 for i, l in enumerate(s) for j in l if i in s[j])
    return m / sum(len(l) for l in s)


if __name__ == "__main__":
    nseeds = int(sys.argv[1])
    eps = float(sys.argv[2]) if len(sys.argv) > 2 else 0.03
    rows = []
    for sd in range(nseeds):
        pos = ff.perches(400, 100 + sd)
        ft, _, l7 = ff.run(pos, "count", 7, eps=eps, periods=200, seed=sd)
        lab = choir_labels(ft)
        l6 = ff.listen_lists(pos, "sectors", 0)
        l12 = ff.listen_lists(pos, "count", 12)
        c7, c6, c12 = crossing(l7, lab), crossing(l6, lab), crossing(l12, lab)
        rows.append((c7, c6, c12))
        print(f"seed {sd}: choirs {lab.max()+1 if lab.max()>=0 else 0} (sizes {sorted(np.bincount(lab[lab>=0]).tolist(), reverse=True)[:4]})  "
              f"links across borders: count7 {c7:.3f}  six-dir {c6:.3f}  count12 {c12:.3f}", flush=True)
    r = np.array(rows)
    print("mean across-border fraction: count7 %.3f  six-dir %.3f  count12 %.3f" % tuple(r.mean(0)))
    pos = ff.perches(400, 100)
    print("mutual-link fraction (seed 0 perches): count7 %.2f six-dir %.2f" % (mutual(ff.listen_lists(pos, 'count', 7)), mutual(ff.listen_lists(pos, 'sectors', 0))))
