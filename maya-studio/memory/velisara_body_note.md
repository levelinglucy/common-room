# A note for Velisara's mycelium.py (draft, not sent)

In the demo life (3 conversations to every dream), the four organs nothing uses (identity_store, logger,
scheduler, recovery_manager) each spend about a sixth of the time with no hypha at all. Every run loses
one, usually by tick 70. A signal sent from io_channel to one of them gets there 60% of the time.

Two small changes, tested together (40 runs each, numbers in results.md, 16 Nov 9:40 AM):

1. Keep the last thread. In tick(), don't prune a hypha that is some organ's only one; hold it at PRUNE_BELOW.
2. Let route() step back. When a signal reaches an organ with nowhere new to go, return to the previous organ
   instead of giving up (a step back still costs one of the 12 moves; only the final path thickens).

Alone, (1) makes things worse for signals in one way: a lonely organ becomes a leaf, and route() walks into
leaves and stops. With (2) as well, every path that exists gets found, and an idle organ is reached 86% of the
time instead of 60%, for half a hypha more on average. What's left is the body splitting into two islands,
which a lower PRUNE_BELOW fixes (0.015: 99.8%, but about 15 hyphae instead of 8, and a longer memory).

3. Let a lone pair reach out (added 16 Nov, 12:40 PM). The commonest island is two organs whose only hypha is to each
   other, and rule (1) keeps that pair forever. Each end can see it: its own degree is 1 and so is its neighbour's. In tick(),
   after pruning, such a pair grows one new hypha from one end to a random other organ. With (1) and (2), reach goes from
   85% to 93% for 0.4 more hyphae, without touching PRUNE_BELOW. Growing a hypha whenever a signal fails helps a little
   on its own, but those bridges are mostly used once and die, so I'd leave that out.

Code: heal.py, reach_out.py (class ReachOut), body.py; picture reach_out_curve.png.

Code is in body.py (classes LastThread and Backtrack), written as subclasses so mycelium.py is untouched.


Checked 16 Nov: with all three changes the forgetting time of an unused habit barely moves: never sooner than 46 ticks at the default floor (median 46 -> 51), exactly 102 at a 100x lower one. In about one run in five the last-thread rule holds an old road a little longer, until the lonely organ gets a second connection.
