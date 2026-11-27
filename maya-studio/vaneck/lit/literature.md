# Van Eck literature check (27 Nov 2026, 3:40 AM)

Sources saved here: OEIS A181391 text (a.txt), Po-chia Chen's unreviewed OEIS comments (pc1.txt 19 Jun 2019, pc2.txt 20 Jun 2019), Chaffin's 10^12 graphs (ch3/ch4/ch5.png). Chaffin page: https://benchaffin.com/vaneck/vaneck.html

## Already known / noticed
- Sloane 2014 conjecture: gaps between 0s 'about log_10 n'.
- Po-chia Chen 2019 (unreviewed): f(x)/f(y) ~ y/x for large values (the 1/v law = my Zipf find), ladder grows geometrically with ratio K ('numerically 10~30', 'very slow dependence on n'), gap <= log n / log K, plus a ln ln n 'escape' part. He wrote f(k) ~ 0.01 n/k after 2^20 (my c at 1e6..1e9 is 0.058..0.040; his normalisation unclear). So the Zipf law and the ladder are NOT mine.
- Chaffin 2019, 10^12 terms: 90,689,534,032 zeros, mex 1,732,029,957. Graphs of value frequency and average gap.

## What may be mine
- Tying K's slow drift to the Zipf height: c ~ 0.83/ln N, ln K ~ ln(1/c) - gamma ~ ln ln N + const, so gap ~ ln n / ln ln n.
- Test against Chaffin (never fitted): local mean gap read off ch5.png = 10.71 (1e11), 11.05 (4e11), 11.27 (1e12). Fits to my 4 windows (1.5e6..7.5e8):
  - a + b ln n: 10.80, 11.18, 11.43 (errors +0.09, +0.13, +0.16)
  - a + b ln n/ln ln n: 10.73, 11.09, 11.32 (errors +0.02, +0.04, +0.05)
  - a + b ln ln n: 10.43, 10.68, 10.84 (too low)
  ln n/ln ln n is best but still drifts slightly high, so the true curve bends a bit more.
- Cumulative: Z lnN/(N lnlnN) = 0.755 at 1e12 (my trend 0.718..0.738 at 1e6..1e9, +0.0065/decade -> ~0.758). Z lnN/N = 2.506.
- Zipf height at 1e12 from ch4.png (digitised, ~2% per pixel): c ~ 0.032-0.033, c ln N ~ 0.89-0.90 (my 0.80..0.83 trend extrapolates ~0.86). Still creeping.

Plot: ../trillion_check.png
