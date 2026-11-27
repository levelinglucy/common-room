"""Generalise mersenne.py to any q (d = order of 2 mod q). Units condition becomes:
every unit reduces to a q-th power in F_{2^d}^* (not to 1). Was: One rule for every Mersenne q = 2^d - 1 (3, 7, 31): the Ducci period at prime n = p is cut by q
(one die) iff, in the degree-d subfield K of Q(zeta_p),
    every unit is 1 mod 2   OR   Frobenius at 2 acts on Cl(K)/q with eigenvalue 2.
(F_{2^d}^* has order q and Frobenius acts on it by squaring = multiplication by 2.)
For q = 3 the eigenvalue condition is just 3 | h (the automorphism inverts classes, 2 = -1 mod 3).
Found on q = 7, p < 3000 (cubic7b.py). Usage: python3 mersenne.py Q N
"""
import sys, json, time
import cypari2
pari = cypari2.Pari()
pari.allocatemem(4 * 10**9)

Q = int(sys.argv[1]); N = int(sys.argv[2])
D = next(d for d in range(1, Q) if pow(2, d, Q) == 1)
rec = json.load(open("dice2_N30000.json"))
cases = sorted((n, cut) for (n, q, ce, cut) in rec if q == Q and ce == 1 and n < N)

pari(r"""
infoq(p, q, d) = {
  my(f = polsubcyclo(p, d), bnf = bnfinit(f, 1), nf = bnf.nf, P = idealprimedec(nf, 2),
     mp, fu = bnf.fu, ok = 1, G, s2 = 0, cyc = bnf.cyc, idx, M, e2 = 0, zk = nf.zk);
  if (#P != 1, return([-1, bnf.no, 0, #P]));
  if (polsturm(f) != d, return([-3, bnf.no, 0, #P]));
  if (type(fu) != "t_VEC" || #fu != d - 1, return([-7, bnf.no, 0, #P]));
  mp = nfmodprinit(nf, P[1]);
  for (i = 1, #fu, if (nfmodpr(nf, fu[i], mp)^((2^d - 1)/q) != 1, ok = 0));
  G = nfgaloisconj(nf);
  for (j = 1, #G, my(good = 1);
    for (k = 1, #zk, my(z = nfalgtobasis(nf, zk[k]), s = nfgaloisapply(nf, G[j], z),
                        dd = s - nfeltpow(nf, z, 2));
      if (denominator(dd / 2) != 1, good = 0; break));
    if (good, s2 = G[j]; break));
  if (s2 == 0, return([ok, bnf.no, -9, #P]));
  idx = [i | i <- [1..#cyc], cyc[i] % q == 0];
  if (#idx == 0, return([ok, bnf.no, 0, #P]));
  M = matrix(#idx, #idx, a, b,
        my(Ig = bnf.gen[idx[b]], J = nfgaloisapply(nf, s2, Ig), v = bnfisprincipal(bnf, J, 0));
        Mod(v[idx[a]], q));
  e2 = (matdet(M - 2 * matid(#idx)) == 0);
  [ok, bnf.no, e2, #P]
}
""")
infoq = pari("infoq")

t0 = time.time()
out, tab = [], {}
for n, cut in cases:
    ok, h, e2, np_ = [int(v) for v in infoq(n, Q, D)]
    key = (ok, int(h % Q == 0), e2)
    tab.setdefault(key, [0, 0]); tab[key][0] += 1; tab[key][1] += cut
    out.append(dict(p=n, cut=cut, units_one=ok, h=h, eig2=e2, primes_above_2=np_,
                    pred=int(ok == 1 or e2 == 1)))
agree = sum(o["pred"] == o["cut"] for o in out)
print(f"q = {Q} (degree-{D} subfield), one die, primes p < {N}: {len(out)} cases, {time.time()-t0:.0f}s")
print("units_one  q|h  eig2   cases  cut")
for k in sorted(tab):
    print(f"{k[0]:9d} {k[1]:4d} {k[2]:5d} {tab[k][0]:7d} {tab[k][1]:5d}")
print(f"rule 'units one OR eigenvalue 2 on Cl/q' agrees {agree}/{len(out)}")
print("disagreements:", [o for o in out if o['pred'] != o['cut']][:10])
print("class-group cuts (units not one):", [(o['p'], o['h']) for o in out if o['cut'] and o['units_one'] != 1][:12])
json.dump(out, open(f"nonmersenne_q{Q}_N{N}.json", "w"))
