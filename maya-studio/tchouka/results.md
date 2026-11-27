# Tchoukaillon: pi in a sowing game (26 Nov 2026, 3:40 PM)

> **CORRECTION (26 Nov 2026, 9:40 PM, see `lit/literature.md`):** L(n) = sqrt(pi n) + O(1) (the board staying within a few pits of sqrt(pi x seeds)) is already proved: Broline & Loeb 1995, Theorem 9, settling Erdos & Jabotinsky's 1958 conjecture. The "runs of slope 1, 2, 3..." staircase in `variants/` was also noticed by Erdos & Jabotinsky in 1958. Possibly mine, both UNCHECKED against the wider literature: the measured range L - sqrt(pi n) in [-4.05, +2.24] up to 4e8 seeds, and the Gamma-function formula for fatter pits in `variants/`.

Rule: row of pits, store at the end. A pit k places from the store holding exactly k seeds can be sown: one seed into each pit nearer the store, last one into the store. Win = empty board.

- `t.py`, `t.c`, `err.c`: build the winning board for n seeds by reverse play (find the first empty pit i, take one seed from each pit before it, put i seeds in it).
- `verify.py`: built boards win by greedy forward play for n <= 3000; brute force confirms the board is the only winner for n = 1..10. e.g. n = 20: [0,2,2,1,3,5,7].
- Pits used L(n): L^2/n = 3.025 (1e3), 3.0976 (1e4), 3.136 (1e5), 3.1405 (1e7), 3.141047 (1e8), 3.1414 (4e8). Known: Broline & Loeb 1995, arXiv math/9502225 (n^2/pi bound, periodicity of pit occupancies).
- My bit: L(n) - sqrt(pi n) stays inside [-4.05, +2.24] pits for all n from 1000 to 4e8 (err.c, 3.4 s). Not checked against the paper's error term.
- `boards.png` (pic.py): every winning board for n = 1..6000, colour = seeds / pit number. The near pits flicker, then curved bands of pits in step, a black band of nearly-empty pits, and the far edge riding sqrt(pi n).

Open: what draws the curved bands (pit k refills on a cycle of k+1?); explain the error range; variants (two seeds per pit, two stores) and whether another constant replaces pi.
