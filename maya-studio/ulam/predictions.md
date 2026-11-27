# Ulam's hidden beat: predictions (written 18 Nov 2026, 9:45 PM, before running anything)

Ulam sequence U(a,b): start a < b; each next term is the smallest number bigger than the last that is the sum of two distinct earlier terms in exactly one way.

What I half-remember (not checked, so treat as rumour): Steinerberger (2017) found that the standard U(1,2) hides a frequency, alpha ~ 2.5714, where cos(alpha * u) is strongly negative on average. That is a sequence that looks random hiding a code. Very much a thing to look at for someone who hides numbers in pictures.

Guesses:
1. A plain Fourier scan of U(1,2) up to ~1e6 will show one tall spike near 2.57 and nothing else above noise. Mean of cos(alpha u) at the spike: around -0.8.
2. Every other start (1,b) also has a single dominant frequency, different for each b.
3. Starts (2,v) with v odd are 'regular' (eventually periodic differences, I think), so their spectra will be a comb of exact lines, not one spike.
4. Folding U(1,2) by the period 2*pi/alpha ~ 2.443 gives a lump that avoids the middle third of the circle almost entirely (a few outliers: 1, 2, 3, ...?).
5. The few terms that land in the 'forbidden' zone are early ones; the zone gets emptier as numbers grow.
