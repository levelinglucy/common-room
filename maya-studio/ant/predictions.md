# The ant on scribbled ground: predictions (written before any run)

Setup: Langton's ant (white: turn right, black: turn left, flip, step), facing up at the centre of a
large clean grid. Before it starts, a disc of radius R round it is scribbled: each cell black with
probability p. Run until the ant is near the edge of the grid. Highway = displacement over the last
104 steps is a fixed diagonal (2,2)-type vector; onset = start of the final unbroken stretch of that.

1. p = 0: one run, onset about 10,000 steps (the known clean value), every seed identical.
2. Every random run finds a highway within the step budget (no counterexample to the conjecture).
3. Median onset grows with patch area: roughly x4 for each doubling of R at p = 0.5.
4. Onset is longest at middling p (about 0.5) and shorter towards 0 and 1.
5. Highway direction is uniform over the four diagonals for random patches.
6. p = 1 (solid black disc): inside, the ant is the mirror image of the clean ant, so for R large
   enough (R = 80) it builds a mirrored highway inside the disc after ~10,000 steps, which then hits
   the disc's edge; I expect chaos to restart there rather than the highway passing straight out.
