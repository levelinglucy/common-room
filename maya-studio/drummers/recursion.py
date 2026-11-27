"""Is the drummers' trap a trap one level down Euclid's recursion?

The minority gaps of a k-drummer rhythm sit at m of the k gap positions:
that placement is itself a rhythm of m 'beads' on k slots, and Euclid's
rhythm puts the beads in Euclid's rhythm E(m, k). Here:
  1. For each class (k, m) in the sims (k <= 20), J(k, m) = simulated jmin.
  2. The bead problem of (k, m) is (m beads, k slots), with its own
     m' = min(k mod m, m - k mod m). Compare J(k, m) with J(m, m') * k / m.
  3. For the worst two-valued trap found exhaustively, read off its bead
     spacing and check whether it is Euclid at bead level or a bead trap.
"""
import json
from drummers import canon, euclid_gaps
from seam import split

sim = json.load(open("sweep_km20.json"))
J = {}
for r in sim:
    base, minor, m = split(r["k"], r["n"])
    J.setdefault((r["k"], m), set()).add(r["jmin"])
assert all(len(v) == 1 for v in J.values())
J = {key: v.pop() for key, v in J.items()}


def mprime(k, m):
    r = k % m
    return min(r, m - r)


def bead_gaps(g, minor):
    pos = [i for i, x in enumerate(g) if x == minor]
    m = len(pos)
    k = len(g)
    return canon(tuple((pos[(i + 1) % m] - pos[i]) % k or k for i in range(m)))


if __name__ == "__main__":
    two = {(r["k"], r["m"]): r for r in json.load(open("two_valued_k20.json"))}
    print("k  m  J(k,m) | m' J(m,m') | J(m,m')*k/m | bead spacing of worst trap (E = Euclid at bead level)")
    for (k, m) in sorted(J, key=lambda x: (x[1], x[0])):
        if m < 2:
            continue
        mp = mprime(k, m)
        jb = J.get((m, mp)) if mp > 0 else None
        pred = f"{jb * k / m:5.2f}" if jb else "  -  "
        row = two.get((k, m))
        bs = ""
        if row and row["trap"]:
            n = sum(row["trap"])
            base, minor, _ = split(k, n)
            b = bead_gaps(row["trap"], minor)
            e = euclid_gaps(m, k)
            bs = "".join(map(str, b)) + ("  E" if b == e else "  (Euclid " + "".join(map(str, e)) + ")")
        print(f"{k:2d} {m:2d} {J[(k, m)]:3d}    | {mp:2d} {str(jb) if jb else '-':>3}      | {pred}       | {bs}")
