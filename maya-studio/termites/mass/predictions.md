# How fast does a lone pile wander, by size? Predictions before running (19 Nov 2026, 6:40 AM)

Setup: one packed disc of M chips on an L x L torus, T termites, same rules as termites.c (jump 20).
Measure the pile centre's diffusion constant D (MSD = 4 D t), the drop rate, and the mean squared chip hop.

Independent-hop picture: D = rate x <hop^2> / (4 M^2).
- A chip is picked from the rim and dropped on the rim, so <hop^2> ~ R^2 ~ M.
- rate: termites are the bottleneck. A random walker on a torus finds a disc at a rate that depends only weakly (logarithmically) on its radius, so rate ~ T x (slowly rising in M).

Predictions:
1. D ~ M^-1, with a small correction from the log: measured exponent between -0.8 and -1.0. NOT M^-1.5 or M^-2 (what I guessed last session).
2. <hop^2> / M roughly constant (within 30%) across M.
3. Doubling T doubles D (termites act independently at this density).
4. Hops still explain ~80% of the MSD at every size (the shortfall is a fixed anticorrelation, not size-dependent).
