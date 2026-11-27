"""Does the q = 7 one-die cut follow the cubic field, the way q = 3 followed the quadratic one?

For prime p, x in F_{2^m}^* is a 7th power iff its norm down to F_8 is 1. The norm of 1 + zeta
is the product over the index-3 subgroup of <2>, which (with the a ~ -a die merge) is the
cyclotomic unit eta of the cubic subfield K3 of Q(zeta_p), reduced mod 2. If 2 is inert in K3,
O/2 = F_8, and the image of the full unit group U in F_8^* is Galois-stable, so it is trivial or
everything. Cyclotomic units sit in U with index h_3 (prime conductor). Guess:
    cut by 7  <=>  every unit of K3 is 1 mod 2   OR   7 | h_3.
Test against the direct Ducci cut (Dpow) recorded in dice2_N30000.json.
"""
import sys, json, time
import cypari2
pari = cypari2.Pari()
pari.allocatemem(2 * 10**9)

N = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
rec = json.load(open("dice2_N30000.json"))
cases = sorted((n, cut) for (n, q, ce, cut) in rec if q == 7 and ce == 1 and n < N)

pari("""unitsone(p) = my(f = polsubcyclo(p, 3), bnf = bnfinit(f, 1), nf = bnf.nf,
   P = idealprimedec(nf, 2), mp, fu = bnf.fu, ok = 1);
   if (#P != 1, return([-1, bnf.no, #P]));
   mp = nfmodprinit(nf, P[1]);
   for (i = 1, #fu, if (nfmodpr(nf, fu[i], mp) != 1, ok = 0));
   [ok, bnf.no, #P]""")
unitsone = pari("unitsone")

t0 = time.time()
out = []
tab = {}
for n, cut in cases:
    ok, h, np_ = [int(v) for v in unitsone(n)]
    pred = int(ok == 1 or h % 7 == 0)
    key = (ok, int(h % 7 == 0))
    tab.setdefault(key, [0, 0]); tab[key][0] += 1; tab[key][1] += cut
    out.append(dict(p=n, cut=cut, units_one=ok, h3=h, primes_above_2=np_, pred=pred))

agree = sum(o["pred"] == o["cut"] for o in out)
print(f"q = 7, one die, primes p < {N}: {len(out)} cases, {time.time()-t0:.0f}s")
print(f"guess agrees with the Ducci cut in {agree}/{len(out)}")
print("units_one 7|h3  cases  cut")
for k in sorted(tab):
    print(f"{k[0]:9d} {k[1]:5d} {tab[k][0]:6d} {tab[k][1]:5d}")
bad = [o for o in out if o["pred"] != o["cut"]]
print("disagreements (first 20):", bad[:20])
print("rate: cut", sum(o['cut'] for o in out) / len(out),
      " units-one", sum(o['units_one'] == 1 for o in out) / len(out),
      " 7|h3 with units not one", sum(o['units_one'] != 1 and o['h3'] % 7 == 0 for o in out) / len(out))
miss = [o['p'] for o in out if o['cut'] and o['units_one'] != 1][:10]
print("first cuts not explained by units alone:", miss)
json.dump(out, open(f"cubic7_N{N}.json", "w"))
