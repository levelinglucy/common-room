# Hofstadter's Q to 2^30 (19 Nov 2026, 9:40 PM session)

`q.c` (uint32 array, 2^30 terms in 2 min 52 s, 4.3 GB). Q(2^30) = 536,485,876. Output in r30/ (bins.tsv: 16 bins per octave; envelope.tsv: min/max of Q(n) - n/2 per 4096 terms).

- Defined all the way: no look-back below 1 to 2^30 (prediction 5 right).
- Spread of Q(n) - n/2 per octave grows by a factor 2^a with a = 0.850 (k=11), 0.880 (k=20), 0.8825 (22), 0.8834 (24-25), 0.8840 (26), 0.8845 (28), 0.8847 (29). Still creeping up ~0.0002-0.0006 per octave; not settled. Prediction 1 (0.85-0.92) right but loose.
- The breath: rms / 2^(0.8863k) by sixteenth of an octave is the SAME curve from k = 22 to 29 to about 0.001: 0.058 at the octave start, falling to 0.015 at 7/16, then up to 0.107 at the octave end. So the generations do not break at powers of 2: the loud part runs across the power of 2 and the quiet seam sits inside the octave. Prediction 2 wrong in kind.
- Quiet seam (narrowest 4096-band): n/2^k = 1.4375 (k 16-17), 1.42 (18-21), 1.41 (22-25), 1.40 (26-28), 1.392 (29). Drifting slowly down, past sqrt 2. Width at the seam is 8-10% of the octave's widest band.
- Why the shape copies itself: look-back distances average n/2 to 5 decimals (0.50000 for k >= 22), so each octave is read off the one below, seam and all. Same parent cell (a = b): about 1 in a million or less past 2^20 (prediction 3 right).
- Parity: even share 0.4999-0.5004 per octave from k = 22 (prediction 4 right). Mean of Q - n/2 is 0.000 x rms in every bin: symmetric.

Scored: 1 right, 2 wrong (best bit), 3 right, 4 right, 5 right.

Open: where the seam drifts to (and why it moves at all: the look-back is n/2 - (Q - n/2)/..., so the seam's parent is offset by the noise). Whether a converges (0.885-0.89?) or has a log correction. Is the fixed within-octave profile known (Pinn 1999 'generations'; Balamohan-Kuznetsov-Tanny)? Render: q_breath.png (not yet checked for overlaps/readability).
