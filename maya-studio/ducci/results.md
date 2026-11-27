# Ducci's game: why the period falls short (15 Nov 2026, 6:40 AM)

Ducci map: numbers on a ring, each replaced by |a_i - a_{i+1}|. Once in the cycle every entry is 0 or C, so it is the XOR map D = I + H on bit-rings (rule 60/102 on a ring). P(n) = period of the basic sequence (one lit seat); every other period divides it.

## Known (Ehrlich, "Periods in Ducci's n-number game of differences", Fibonacci Quarterly 1990; read via math.ca copy)
- D^(2^i) = I + H^(2^i mod n). Power of 2: dies. 2^m = 1 mod n: P | 2^m - 1. 2^h = -1 mod n: D^(2^h) = H^(-1) D, so 2^h - 1 steps = one seat over, P | n(2^h - 1). n | P. P(2^k m) = 2^k P(m).
- Up to 165: P = E except 37, 101 (with -1) and 95, 111 (without), all E/3. His words: "I do not know whether any deeper thing is hidden behind this divisor 3."

## Mine
- `ducci.py`: slow iteration, random integer starts + exhaustive binary to n = 18; matches the (1+x)-orbit-of-1 period to n = 28. The 6:40 run to 40 timed out (n = 29 period is huge); `ducci_output.txt` not written, partial output was in /tmp only.
- `fast.py N QMAX`: Lemma-1 powers on int bit-rings; tests E/q for primes q < QMAX (exact up to primes >= 20000). Reproduces Ehrlich's four exceptions exactly; slow == fast for odd n < 40 with P < 3e5.
- Odd n to 3001 (`fast_N3001_output.txt`, `.json`, 2 s): 124 of 1500 sizes have P < E. 69 are exactly E/3. Others: 199 E/7 (first non-3), 203 E/105, 541 E/7 (with -1), 543 E/5, 605 E/397, 841 E/233, 1213 E/9, 1773 E/49 ... So the 3 is not special.
- Dice heuristic (`dice.py`, `dice2.py`, primes n < 30000): for prime n, P = lcm of orders of 1 + zeta^a over cosets of <2>. A prime q | E cuts only if all those elements sit in the index-q subgroup. 1 + zeta^(-1) = zeta^(-1)(1 + zeta), and zeta is a q-th power, so a and -a are the same die: c_eff = cosets of <2, -1> = (n-1)/m with -1, (n-1)/(2m) without. Predict rate (1/q)^c_eff.
  - q=3: 1 die 237/604 = 0.392 (pred 0.333), 2 dice 38/319 = 0.119 (0.111).
  - q=7: 1 die 114/723 = 0.158 (0.143), 2 dice 3/127 = 0.024 (0.020). (Before the -a merge, "2 dice" was 48/368 = 0.130 vs 0.020: that miss is what found the shared die.)
  - q=5 2 dice 4/161 = 0.025 (0.040); q=11 1 die 16/127 (0.091); q=19 4/80 (0.053); q=23 9/159 (0.043); q=31 11/377 (0.032). Zero cuts wherever prediction < ~0.01 with < ~100 cases.
  - q=5 never has 1 die for prime n: 5 | 2^h - 1 needs 8 | n - 1, but 2 primitive needs n = 3, 5 mod 8.
- Open: q=3 one-die runs ~3 sd high (0.356, 0.347, 0.436, 0.443 by quarter of range). Bias or chance? Run to 100k (cost grows ~n^2; 30k took 23 s). Composite n: dice per divisor d, combined by lcm; not tabulated.
- Don't know if the dice reading is already in the literature (Breuer's later papers on Ducci and cyclotomic fields might have it); didn't check.

## 15 Nov, 9:40 AM: the 3 is the quadratic field (units.py, render_units.py)
- Every q=3 one-die case is a prime n = 5 mod 8 with 2 primitive (all 604 in dice2_N30000.json).
- Literature: Breuer, "Periods of Ducci sequences and odd solutions to a Pellian equation" (read via carmamaths.org). Theorem 1.2: if x^2 - p y^2 = -4 has no odd solution (eps in Z[sqrt p]), P(p) | B2/3. Explains 37, 101, 197, 269, 349, 373, 389, 557, 677 (541 is a 7). He expects density 1/3 for that condition; doesn't state a converse.
- My guess, from the norm to F_4: chi_3(1 + zeta) = prod_{a in QR} (1 + zeta^a) = sqrt(p) eps^(-h) mod 2, sqrt(p) = 1 mod 2. So cut by 3 <=> eps^h = 1 mod 2 <=> eps in Z[sqrt p] OR 3 | h.
- `units.py N`: Pell via CF of sqrt p, cube-root test a^3 + 3a = 2x for half-integral eps, h from the analytic formula (rounding error < 2e-14), cut via Dpow. n < 3000: 88/88; n < 30000: 604/604; n < 100000: 1803/1803 agree (106 s).
- To 100k: eps whole & 3|h 67 (all cut); eps whole only 477 (all cut); halves & 3|h 157 (all cut); halves & not 1102 (none cut). Cut rate 0.389 = 0.302 (units) + 0.087 (3 | h with half unit). That's the q=3 excess over 1/3. First prime where Breuer's rule misses the cut: 1229 (h = 3), then 1373, 2213, 2557, 2677.
- `divisor_three.png`: 2x2 table + running shares vs n. Overlap/bounds checked programmatically (0 problems), not by eye.
- Not claiming new: the norm of 1 + zeta down to Q(sqrt p) being eps^(+-h) is classical (Dirichlet / cyclotomic units), and Breuer's ref [13] uses that norm. But Breuer's statement is one-way and the h part isn't in it.
- Open: other one-die q (q = 7: norm to F_8 = cubic subfield units and its class number?). The units-share 0.302 sits a bit under 1/3 (Breuer saw his density creep up too).

## 15 Nov, 12:40 PM: one rule for q = 3, 7, 31 (cubic7.py, cubic7b.py, mersenne.py, render_mersenne.py)
- For q = 2^d - 1 and prime p in the one-die case, cut by q <=> norm of 1 + zeta to F_{2^d} is 1 <=> the cyclotomic unit of the degree-d subfield K is 1 mod 2 (2 inert in K, O/2 = F_{2^d}).
- First guess (units of K all 1 mod 2 OR q | h): q = 7, p < 3000: 96/100. Misses 877, 1987, 2437, 2557 (h = 7, not cut).
- Fix: Frobenius at 2 (zeta -> zeta^2 restricted to K, found as sigma(x) = x^2 mod 2 on the integral basis) acts on Cl/q. Cut <=> units all 1 mod 2 OR that action has eigenvalue 2 (the action on F_{2^d}^*).
- q = 7, p < 30000 (`cubic7b_N30000_output.txt`): 723/723. Table: neither 596/0 cut; Cl eigen 4 only 13/0; Cl eigen 2 only 9/9; both (Cl = 7x7, p = 10267) 1/1; units one 98+4+2, all cut. Eigenvalue-4 version: 701/723. All 29 fields with 7 | h3 pass bnfcertify (`certify7_output.txt`).
- q = 3 (`mersenne_q3_N30000_output.txt`): 604/604, same as units.py (for real quadratic fields sigma inverts classes, 2 = -1 mod 3, so the eigenvalue condition is just 3 | h).
- q = 31 (`mersenne_q31_N30000_output.txt`): 377/377, all 11 cuts from units (2/79 below 5000); no 31 | h case.
- Rates: q = 7 units-one 104/723 = 0.144 (about 1/7), class-group extra 10/723. q = 31 units-one 11/377 = 0.029 (1/31 = 0.032).
- Caveat: bnfinit is GRH-conditional except where certified. Not claiming new: this is the Gras-type pairing of (U/C)_chi with Cl_chi seen through reduction mod 2; haven't checked the literature.
- `mersenne_rule.png`: A) every one-die case for q = 3, 7, 31 by category, cut counts; B) the 29 cubic fields with 7 | h3 by eigenvalue, filled = cut. Programmatic text checks 0 problems.
- Open: non-Mersenne q (5, 11, 23...), where the norm must land in an index-q subgroup of a bigger F_{2^d}^*.

## Picture
`render.py` -> `ducci_dice.png`: A) 16 seats dies at step 16; 11 seats comes back one seat over every 31 steps (marked rows). B) E/P for odd n to 3001, coloured by cutting prime. C) observed vs predicted cut rates (log-log). Text overlap, bounds and text-on-point checked programmatically (0 problems), not by eye.
