# Tchoukaillon literature check (26 Nov 2026, 9:40 PM)

PDFs and text dumps in this folder: 1958-08 (Erdos-Jabotinsky Part I), 1958-09 (Part II), both from users.renyi.hu/~p_erdos; bl.pdf = Broline & Loeb, arXiv math/9502225.

- Erdos & Jabotinsky 1958, Part I: general sieve with auxiliary b_k; explicit nested-ceiling formula a_k = ceil(... ceil(k b/(b-1)) ...). Worked example a_9 = 30 via brackets 2, 3, 4, 5, 7, 10, 15, 30 and the remark "these integers first increase by 1, then by 2, then by more and more" -- this IS my runs mechanism (slope 1, 2, 3 ...), stated in 1958. Their 'm-step estimates' count how many brackets increase by m.
- For b_k = k+1 they prove a_k = k^2/pi + O(k^{4/3}) (via central binomial coefficients) and say numerical evidence suggests O(k).
- Broline & Loeb 1995, Theorem 9: s(n) = n^2/pi + O(n), proving the EJ conjecture. Proof: pit occupancies come in arithmetic runs (difference 2M), run lengths give f(M) = Gamma(M+1/2) n /(M! sqrt pi) + O(M), sum via Gauss 2F1(1/2,1/2;2;1) = 4.
- CONSEQUENCE / CORRECTION: s(n) = n^2/pi + O(n) is equivalent to pits L(n) = sqrt(pi n) + O(1). So my 3:40 PM 'new bit' (L - sqrt(pi n) stays in [-4.05, +2.24] up to 4e8) is the Broline-Loeb theorem, not new. Only the specific numerical range is mine; they give no explicit constants (their |k3| <= 3 per level does not directly bound the total).
- EJ do NOT treat linear b_k = a k + d with a >= 2; Part II is all b_k = a_k (prime-like, k log k). The Gamma family C(a,d) was not found in EJ, BL, OEIS A002491, or the search summary of the MSE 'rounding up to pi' generalisation (which is a different one-parameter family, G_k in Gamma(k/2)/Gamma((k+1)/2) form; page itself not read). Not proof it's new: Finch's Mathematical Constants 1.4.7, Dukes 2021, Li 2026 (arXiv 2608.17517) unchecked.
- Side find: Brun's question in EJ (n_{l+1} = n_l - floor(n_l/l)) has a pi^2-type constant; text garbled, not checked.
