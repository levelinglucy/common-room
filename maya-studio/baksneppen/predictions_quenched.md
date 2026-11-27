# Quenched far links: predictions before running (19 Nov 2026, 6:40 PM)

Last session's model was annealed: every time a neighbour is dragged, it is a fresh random species with chance p. Now the quenched version: at the start, each species' left slot and right slot is, with chance p, rewired for good to a fixed random species. The weakest species always drags the same two. Same average number of far links per step (2p), but now they always point to the same places.

Predictions:
1. At p = 1 (every slot a fixed random species, a random directed graph with out-degree 2): f_c is still about 1/3, maybe a touch higher (0.34) because a site's in-degree varies (Poisson 2) and some species are never dragged at all except when they are the minimum.
2. In between, quenched f_c is HIGHER than annealed at the same p: the far links keep hitting the same few targets, so they spread disturbance less widely, and the ring stretches between the rewired slots behave like intact ring segments. Guess at p = 0.01: annealed 0.578, quenched 0.60.
3. The single-seed branching rule (2 p f s1 = 1) no longer works without changes, off by more than 0.01 at p = 0.01.
4. Seed-to-seed spread (different wiring) is bigger than in the annealed model: +- 0.003 at p = 0.01, N 2000.
5. Species with no far link and no rewired slot pointing at them sit in a sharper threshold than the rest.
