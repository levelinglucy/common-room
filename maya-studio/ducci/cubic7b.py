"""Refine cubic7.py. 7 | h3 alone was not enough (cut 1 of 5 below 3000).
The 7-part of the class group carries a Galois action. Frobenius at 2 (sigma_2, the restriction of
zeta -> zeta^2) acts on Cl/7 by 2 or by 4 (the cube roots of 1 mod 7). Guess: the cut needs the
7-part in one particular eigenspace, which pairs with the eigenspace the reduction F_8^* sees
(sigma_2 acts on F_8^* by squaring, i.e. by 2).
Record, per prime: units_one, h3, and which eigenvalues (2, 4) appear on Cl/7.
"""
import sys, json, time
import cypari2
pari = cypari2.Pari()
pari.allocatemem(2 * 10**9)

N = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
rec = json.load(open("dice2_N30000.json"))
cases = sorted((n, cut) for (n, q, ce, cut) in rec if q == 7 and ce == 1 and n < N)

pari(r"""
info(p) = {
  my(f = polsubcyclo(p, 3), bnf = bnfinit(f, 1), nf = bnf.nf, P = idealprimedec(nf, 2),
     mp, fu = bnf.fu, ok = 1, G, s2 = 0, cyc = bnf.cyc, idx, M, e2 = 0, e4 = 0, zk = nf.zk);
  if (#P != 1, return([-1, bnf.no, 0, 0, #P]));
  mp = nfmodprinit(nf, P[1]);
  for (i = 1, #fu, if (nfmodpr(nf, fu[i], mp) != 1, ok = 0));
  \\ Frobenius at 2: sigma(x) = x^2 mod 2 on the integral basis
  G = nfgaloisconj(nf);
  for (j = 1, #G, my(good = 1);
    for (k = 1, #zk, my(z = nfalgtobasis(nf, zk[k]), s = nfgaloisapply(nf, G[j], z),
                        d = s - nfeltpow(nf, z, 2));
      if (denominator(d / 2) != 1, good = 0; break));
    if (good, s2 = G[j]; break));
  if (s2 == 0, return([ok, bnf.no, -9, -9, #P]));
  idx = [i | i <- [1..#cyc], cyc[i] % 7 == 0];
  if (#idx == 0, return([ok, bnf.no, 0, 0, #P]));
  M = matrix(#idx, #idx, a, b,
        my(Ig = bnf.gen[idx[b]], J = nfgaloisapply(nf, s2, Ig), v = bnfisprincipal(bnf, J, 0));
        Mod(v[idx[a]] * (cyc[idx[a]] / 7) / (cyc[idx[a]] / 7), 7));
  \\ v[idx[a]] mod 7 is the coordinate in Cl/7 (generator of a 7-divisible cyclic factor)
  e2 = (matdet(M - 2 * matid(#idx)) == 0);
  e4 = (matdet(M - 4 * matid(#idx)) == 0);
  [ok, bnf.no, e2, e4, #P]
}
""")
info = pari("info")

t0 = time.time()
out, tab = [], {}
for n, cut in cases:
    ok, h, e2, e4, np_ = [int(v) for v in info(n)]
    key = (ok, h % 7 == 0, e2, e4)
    tab.setdefault(key, [0, 0]); tab[key][0] += 1; tab[key][1] += cut
    out.append(dict(p=n, cut=cut, units_one=ok, h3=h, eig2=e2, eig4=e4, primes_above_2=np_))
print(f"q = 7, one die, primes p < {N}: {len(out)} cases, {time.time()-t0:.0f}s")
print("units_one  7|h3  eig2  eig4   cases  cut")
for k in sorted(tab):
    print(f"{k[0]:9d} {int(k[1]):5d} {k[2]:5d} {k[3]:5d} {tab[k][0]:7d} {tab[k][1]:5d}")
for lam in (2, 4):
    pred = [int(o['units_one'] == 1 or o[f'eig{lam}'] == 1) for o in out]
    print(f"guess 'units one OR eigenvalue {lam} on Cl/7': agrees {sum(p == o['cut'] for p, o in zip(pred, out))}/{len(out)}")
json.dump(out, open(f"cubic7b_N{N}.json", "w"))
