# Bak-Sneppen: predictions before running anything (19 Nov 2026, 3:40 PM)

Model: N species on a ring, each with a fitness in [0,1]. Every step, the least fit species and its two ring neighbours get fresh uniform random fitnesses. Known from memory (to be checked, not trusted): the ring self-organises so nearly every fitness sits above a threshold f_c ~ 0.667; avalanches below a level f have a power-law size distribution.

My own question ("who listens to whom" again, as with the starlings and fireflies): when the weakest species is replaced, it drags along its 2 ring neighbours. What if, with probability p, one of those two is swapped for a random species anywhere on the ring? p = 0 is the ring; p = 1 is fully random neighbours (mean field, where I expect f_c = 1/3 for 3 replaced per step).

Predictions:
1. Ring (p = 0): f_c lands at 0.667 +- 0.002 for N = 2000.
2. Random neighbours (p = 1): f_c = 1/3 exactly (in the large N limit), and the threshold is softer (the fitness histogram has a less sharp step).
3. In between, f_c(p) falls smoothly from 0.667 to 0.333. Guess: it falls fast. Half the drop (f_c = 0.5) is reached already by p = 0.1, the way one random glance holds a whole flock.
4. The avalanche exponent on the ring: P(s) ~ s^(-1.07). With any p > 0, at large sizes the avalanches cross over to the mean-field exponent 3/2.
5. The "active spot" (the location of the minimum) on the ring makes local jumps: the distance between successive minima has a power-law tail, exponent about 3.2. With p > 0, a fraction of jumps go far, roughly 2p/3 of them.
