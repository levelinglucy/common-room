# Fatter pits (26 Nov 2026, 6:40 PM)

> **NOTE (26 Nov 2026, 9:40 PM, see `../lit/literature.md`):** the "runs of slope 1, 2, 3..." mechanism below was already noticed by Erdos & Jabotinsky (1958). The Gamma-function formula for a >= 2 is not in Erdos-Jabotinsky or Broline-Loeb, but I haven't checked Finch, Dukes 2021 or Li 2026, so it is not claimed as new.

Variant: pit k (1-indexed from the store) is sown when it holds c(k) = a*k + d seeds: one seed into each of the k-1 nearer pits, the rest into the store. Ordinary Tchoukaillon is a = 1, d = 0. Reverse play still gives one winning board per move count (first empty pit i, take one from each nearer pit, put c(i) in it).

- `v.c`, `w.c`, `x.c`: direct simulation. a = 1 with any d: pi survives, L^2/moves -> (d+1)*pi. a >= 2: pits grow faster than sqrt; L ~ moves^(a/(a+1)) (a = 2: 2/3, a = 3: 3/4).
- Exact recursion (`check_rec.py`, 340/340 against simulation for 7 (a,d) pairs): the first move to reach pit L is P_1, with P_L = 1 and P_k = P_{k+1} + ceil(P_{k+1}/c(k)). Reason: among moves that reach pit k, the pit lets c(k) through, then stops one, so pit k+1's list is pit k's list with every (c(k)+1)-th entry removed (from the first).
- `rec2.c`: constants C = L^((a+1)/a) / P_1, averaged over sampled L near 1e7.

Derivation (heuristic, not a proof):
1. Walking back from pit L, ceil(P/c) stays at j for a run, so P rises by exactly j per pit. A run ends when P reaches j*a*k. Run boundaries: k_{j+1} = k_j * (1 - a/((a+1)j)), so k_J ~ L * J^(-a/(a+1)) / Gamma(1/(a+1)), with P ~ J*a*k_J there.
2. Once j is large, ceil adds little: P_k ~ P_{k+1}(1 + 1/(ak+d)), and the product down to pit 1 is K^(1/a) * Gamma(1+(d+1)/a)/Gamma(1+d/a).
3. Multiply: J cancels (exponents (a+1)/a and a/(a+1) are reciprocal), giving
   C(a,d) = Gamma(1/(a+1))^((a+1)/a) / a * Gamma(1+(d+1)/a) / Gamma(1+d/a).
   a = 1, d = 0: Gamma(1/2)^2 = pi. a = 1, any d: (d+1)*pi.

Check (formula vs measured near 1e7 pits):
- a=1: 3.141592654 vs 3.141592267
- a=2: 1.942938567 vs 1.942938391
- a=3: 1.657912757 vs 1.657912735
- a=4: 1.522743406 vs 1.522743142
- a=5: 1.44090029 vs 1.440900244
- a=6: 1.384831743 vs 1.384831464
- (2,3): 3.298434955 vs 3.298433986; (1,3): 4pi = 12.56637061 vs 12.56636245; (3,-1): 1.371082813 vs 1.371082687; (2,-1): 1.236913108 vs 1.236913141; (4,7): 2.089067785 vs 2.089066847.
All agree to 6 or 7 significant figures.

Known? The recursion is an Erdos-Jabotinsky (1958) type sieve, and a Math StackExchange thread on "rounding up to pi" proves a related Gamma-ratio family with the same parabola/runs method. This exact family may well be in Erdos-Jabotinsky; not checked.

`fat_pits.png` (fig.py, viewed): left, the runs of slope 1, 2, 3 ... for the first move to reach pit 400 (a = 1); right, formula vs measured for a = 1..6.

Open: turn step 1-3 into a proof with error bars; why the a = 1 error range is [-4.05, +2.24] pits; d < 0 with c(k) < k (pits that can't be sown) is a different game.
