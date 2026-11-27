# Rotor-router discs: predictions (20 Nov 2026, 3:40 AM, before any run)

Setup: Propp's rotor-router aggregation on the square grid. Each site holds an arrow. A particle starts at the origin; at an occupied site it turns that site's arrow one quarter clockwise and steps the way it now points; it settles on the first empty site. Compare with internal DLA (same, but random steps).

Measure for n particles: r_out = farthest occupied site, r_in = nearest empty site, gap = r_out - r_in. Disc radius sqrt(n/pi).

1. All arrows start pointing north: gap stays below 2 out to n = 200,000 (Levine-Peres numerics say it is tiny).
2. Random starting arrows: still a disc, but a bigger gap, around 3 to 4, growing slowly.
3. IDLA: gap grows like log r, about 6 to 10 at r ~ 250.
4. Checkerboard starting arrows (north/east alternating) behave like all-north (gap < 2).
5. The arrow field of the all-north disc shows big spiral/curve patterns (known pictures); I guess the pattern is self-similar as n grows.
