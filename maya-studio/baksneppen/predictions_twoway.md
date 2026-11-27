# Predictions: two-way links (20 Nov 2026, 12:40 AM session), written before any run

Question: fixed far links pushed the p = 1 threshold from 1/3 (fresh) to 0.4015 (fixed, one-way, out-degree 2), because the weakest keeps re-dragging the two it wore out. What if links are two-way (undirected), so a dragged neighbour drags the minimum back when it becomes the minimum?

Model family: every species has K partners; the weakest species and all K partners get new fitnesses.
- fresh: K uniformly random species each step (exact 1/(K+1)).
- one-way: K fixed random out-links per species.
- two-way: random K-regular undirected graph (configuration model, stubs paired at random, self-loops and double edges rerolled).

K = 2 two-way is a random union of cycles: locally a ring, so it must give the ring's 0.667. That one is a sanity check, not a prediction.

1. K = 3: fresh 0.25, one-way ~0.30, two-way ~0.36 (two-way wastes more, since the back-drag hits the species that just made you weak).
2. K = 4: fresh 0.20, one-way ~0.235, two-way ~0.27.
3. The two-way minus one-way gap shrinks with K, roughly like 1/K^2.
4. Repeat-minimum share (fraction of avalanche steps that hit a species already the minimum before in this avalanche) is higher two-way than one-way at every K.
