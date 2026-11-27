# Termites and wood chips: predictions before running (19 Nov 2026, 3:40 AM)

Model (Resnick, StarLogo/NetLogo "Termites", put on a grid): torus L x L, chips at density p, T termites.
Each termite has one of 8 headings. Each tick: wiggle (heading +-1 or stay), step 1.
- Empty-handed, lands on a chip: pick it up, then jump 20 along heading.
- Carrying, lands on a chip: wander (wiggle, step) until on an empty cell, drop there, jump 20.
A pile = 8-connected cluster of chips.

Predictions, written before any run:
1. Pile count falls roughly as a power of time, N ~ t^-a with a somewhere 0.3-0.6 (coarsening, like droplets).
2. Resnick's 'piles can only die, never be born' is true for drop events (a drop always touches a chip) but picking up can split a pile, so the 8-connected count will sometimes go UP. I expect splits to be common early, rare late.
3. It reaches one pile eventually on a small torus, with time to one pile growing faster than L^2.
4. The one big pile is not round: chips at its edge keep getting picked up and moved, so it should wander slowly across the torus.
