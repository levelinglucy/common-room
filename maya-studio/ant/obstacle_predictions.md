# One dot in the road: predictions (18 Nov 2026, 6:40 AM, written before any run)

Setup: clean Langton's ant, let it build its highway (onset 9,976, direction (-2,2) per 104 steps).
The highway is periodic: every 104 steps it repeats, shifted by (-2,2). So the cells it will step on
ahead of it fall into a finite number of classes (cells modulo that shift). For each class, put ONE
black dot on such a cell well ahead of the ant, and run until it either passes the dot and keeps the
same highway, or builds a new highway. Record: broken or not, new direction (relative to the old),
how many steps of chaos, and how far sideways the new road sits.

1. Most classes break the highway, but not all: I guess 10-30% of dots are absorbed (the ant
   passes, maybe with its road shifted sideways, and carries on in the same direction).
2. Every broken highway rebuilds within the step budget (no endless chaos from one dot).
3. Chaos after a break is shorter than the clean 9,976 on average (a small mess, plus clean ground
   nearby): median 2,000-6,000 steps.
4. New directions among broken ones: mostly a 90-degree turn (left or right), sometimes the same
   direction after chaos, almost never straight back (the old trail is not clean ground).
5. The ant is a mirror machine in some sense, so left turns and right turns are not equally common;
   no guess which wins.
