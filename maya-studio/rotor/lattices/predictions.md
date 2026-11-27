# Rotors on other grids: predictions (20 Nov 2026, 6:40 AM, before any run)

Follow-up to rotor_discs (square grid, quarter-turn arrows). Same aggregation rule, all lengths in bond lengths, 200,000 walkers.
- tri: triangular grid, 6 neighbours, arrow turns 60 degrees clockwise.
- hex: honeycomb, 3 neighbours, arrow turns 120 degrees clockwise.
- sq-NSEW: square grid with the arrow cycling N, S, E, W (back and forth, not round).
- IDLA on each grid for comparison.

1. tri is a disc with a gap even smaller than the square's (~1.2), more directions = finer memory.
2. hex is still a disc but the roughest rotor edge, gap ~2.5 to 3: only three directions, and it has two kinds of site.
3. sq-NSEW is still a disc (every order cycles through all four), gap about the same as clockwise (< 2).
4. IDLA gaps scale with grid only weakly; ~5-7 on all three.
5. Steps = sum |x|^2 to 1e-4 on every rotor grid, because each full cycle of arrows sums to zero.
