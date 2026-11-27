# Does a slime mould remember a road it stopped using?

Tero's Physarum rule (memory.py): jittered triangular mesh 36 x 23 with a round hole (r 4.2) between A and B,
so there are two equally good A-B roads (over / under). C is far left of A. I0 = 1.0 (with I0 = 2 the
saturating f lets both roads survive, 54/46, in some seeds), mu = 1.8, Euler dt = 0.2.
Phases: A->B for 60 (train), A->C for T (idle), A->B for 60 (recall). Optional floor D >= floor.

## Prediction, written before the sweep (16 Nov, ~3:55 AM)

The trained road has D = f(1) = 0.5. While idle it decays by 0.8 per step (Euler), i.e. e^(-1.1157 t).
Everything off the road hit the floor during training. So the old road is the only thing thicker than
the floor until T* = ln(0.5 / floor) / 1.1157:
- floor 1e-3: T* = 5.6
- floor 1e-6: T* = 11.8
- floor 1e-9: T* = 17.9
- no floor: never (old road 2e-20 at T = 40 and still recalled 3/3 in the smoke test).
Below T*: recall on the trained side every time. Above T*: a coin flip (~50%), because every tube is
at the floor and the mesh is symmetric up to jitter.

## Sweep 1, free training (sweep.py -> sweep_24.tsv, summarise.py)

Cliff where predicted (1e-3 between T = 4 and 8, 1e-6 between 10 and 12, 1e-9 between 16 and 18),
but after it 'same side' stayed 21/24, not ~12/24. The coin-flip half of the prediction was wrong:
each mesh has a preferred side (jitter makes one road a little cheaper) and free training mostly
picks it too, so a forgotten mould lands on the same side for a different reason.

## Sweep 2, forced training (forced.py -> forced_24.tsv, forced_24_summary.txt)

A lid holds the other side's crossing edges at 1e-12 during training only; even seeds taught over,
odd seeds under. Training landed where wanted 1920/1920. Naive control per seed: same mesh and floor,
A->C for T then A->B with no training. 24 seeds x 20 values of T x 4 floors.
Counting only the seeds where the taught road is the mesh's worse side (11 to 16 of 24):
- floor 1e-3 (predicted 5.6): kept all at T = 5, 2/13 at 6, 0/13 from 7 on.
- floor 1e-6 (predicted 11.8): kept all at 11, 1/15 at 12, 0/15 from 13 on.
- floor 1e-9 (predicted 17.9): kept all at 17, 2/15 at 18, 0/15 from 19 on.
- no floor: kept all, every T up to 40 (old road 2e-20 by then).
Past the cliff the recall matches the naive mould 24/24 at every T, and so do its share and settling
time to the printed digits: the history leaves no trace at all.
Time to settle (pressure within 10% of final) at floor 1e-6: 2.2 while remembered, creeping to 2.8
right before the cliff, then 5.5 = naive. Floor 1e-3: 2.4, 2.8, 3.4 at T = 2, 4, 5, then 6.4 = naive.
So no gradual forgetting in either the choice or the speed: savings hold flat and drop at once.

Why (by hand): the flow split depends only on ratios of conductances, and the old road and the
background decay at the same rate, so with no floor the ratio never changes and nothing is forgotten.
A floor stops the background but not the road, so the ratio shrinks until the road reaches the floor,
at T* = ln(D_road / floor) / rate. Memory length is logarithmic in the floor: each 10x lower floor
buys ln 10 / 1.116 = 2.06 more time units.

Velisara's mycelium.py (DECAY 0.92 per tick, PRUNE_BELOW 0.15, MAX_WEIGHT 10) is the same shape with
pruning as the floor: an unused hypha at full weight is deleted after about 50 ticks (one at 1.0
after about 23), and each 10x lower prune threshold adds 27.6 ticks. Arithmetic only; I didn't run
mycelium.py for this.

(Corrected 16 Nov: one signal per tick caps the trained weight at 6.9, so it is ~46 ticks, not ~50; see below.)

Picture: render.py -> memory_cliff.png (seed 1, floor 1e-6: taught under; away 11 -> under; away
13 -> over, same as naive; plus the sweep and the settling times). Text checked programmatically
(0 overlaps / out of bounds, 55 texts); the three maps checked by counting thick edges beside the
hole (under 6 / under 6 / over 7). Not looked at by eye.

## 16 Nov, 6:40 AM: the cliff in mycelium.py itself (myc_cliff.py, render_myc.py -> myc_cliff.png)

mycelium.py imported unchanged. Birth ring of the 8 demo organs + direct io_channel <-> memory_store
(A-B) at 1.0; train A->B 60 ticks; then 400 ticks of an away habit; death = first tick A-B appears
in tick()'s pruned list. 300 seeds per condition.

Trained weight: 6.86 (limit 0.92 x 0.6 / 0.08 = 6.9; MAX_WEIGHT 10 is never reached with one signal
per tick). Pure decay prediction ceil(ln(6.86/floor)/0.08338): 46 / 74 / 102 for floors 0.15 / 0.015 /
0.0015. Seen: min exactly the prediction in every condition; 'elsewhere' exactly at it 185/300,
180/300, 300/300 (the rest outlived it because wandering signals crossed A-B).

Away habits at floor 0.15 (myc_cliff_0.15_output.txt):
- elsewhere (dream_engine -> symbolic_renderer): median death 46, p90 80, max 137; 115/300 runs
  reused A-B by wandering.
- near (io_channel -> logger): median 65, p90 158, max 385; 196/300 reused A-B (mean 28.4 uses).
  The away habit got its own direct hypha in 279/300, median tick 28; death minus that tick: median
  43, max 45.
- far (io_channel -> dream_engine): median 65.5, p90 162, max 342; 194/300 reused; direct in 280/300,
  median 28; death minus direct tick median 43, max 45.
- Pruned 19 to 46 ticks after the last away route that used A-B, in every condition.
So: the old road lives as long as a new job still has to walk it, then at most one decay lifetime.

Floor flips the reuse: after 60 ticks of one habit at 0.15, only 1.58 of the 8 birth-ring hyphae are
left on average (a 1.0 hypha lives 23 ticks), ~6.5 hyphae in all, so A-B is the only road out of
io_channel and new jobs rehearse it. At 0.015 reuse is 115-120/300, at 0.0015 61-62/300 (ring
hyphae live 78 ticks, outlast training, new jobs go round the ring).

Quirk: tick() prunes, then explore() may regrow the just-pruned pair at 1.0 in the same tick. Reading
death as 'key missing after tick' misses those (first harness reported deaths up to 91 ticks after
the shortcut; seed 48 far: pruned and regrown at t = 73).

Picture: A = weight traces (one seed, unused, three floors; one 'near' seed 1, shortcut at 35, dies
at 80). B = death tick vs shortcut tick, near + far, with lines 46 and shortcut + 46. Text check
50 texts, 0 problems. Not looked at by eye.

## 16 Nov, 9:40 AM: does the body stay whole? (body.py) -- predictions written BEFORE running

Demo life (3:1 io->memory / dream->symbolic), steady state after 300 ticks, floor 0.15.
Reasoning: an unused 1.0 hypha lives ln(0.15)/ln(0.92) = 22.75 ticks; explore grows 0.25/tick,
so ~5.7 random hyphae alive + 2 habit shortcuts = ~7.5 hyphae. A random pair touches a given organ
with chance 7/28 = 1/4, so an idle organ is cut off about (3/4)^5.7 = ~19% of ticks.
Predict: mean hyphae 7-8; each idle organ cut off 15-25%; whole body connected well under half
the time (guess 10-25%); route() from io_channel reaches an idle organ on one try < 40%.
last_thread: cut-off 0% by construction; cost guess +2 to +3 hyphae. lonely: cut-off a few %.

### Results (40 seeds x 3000 ticks after 300 burn-in; probes every 25 ticks on a deep copy, 19,200 per run)

| variant (floor 0.15) | hyphae | body connected | each idle organ cut off | idle organ reached, one try | fails: no path / path missed |
| base                 | 7.79 | 41.0% | ~17% | 59.8% | 5023 / 2701 |
| lonely explore       | 7.81 | 61.2% | ~6%  | 62.9% | 4312 / 2806 |
| last thread          | 8.53 | 78.4% | 0    | 69.3% | 2292 / 3605 |
| both                 | 8.25 | 74.7% | 0    | 69.3% | 2709 / 3179 |
| base + backtrack     | 7.80 | 41.0% | ~17% | 73.5% | 5096 / 0 |
| both + backtrack     | 8.28 | 74.9% | 0    | 85.9% | 2713 / 0 |
floor 0.015: base 14.83 hyphae, 95.3% connected, 95.8% reached (265 / 546); both+backtrack 99.8% (38 / 0).

Against predictions: hyphae 7.79 (said 7-8, right); idle organ cut off 17% (said 15-25%, right);
connected 41% (said 10-25%, WRONG: a plain random graph with 8 random pairs of 8 nodes is connected
46% of the time, 7 pairs 22%; my intuition undershot, the mycelium is about as connected as random pairs);
reached 60% (said < 40%, wrong, too pessimistic); last_thread cost +0.74 hyphae (said +2-3, wrong: much cheaper).

What I take from it:
- In the demo life every run loses an organ (40/40, median first at tick 68): each idle organ spends about a sixth of its
  life with no hypha at all.
- Over a third of the failed signals (2701/7724) at 0.15, and two thirds at 0.015 (546/811), are not a broken body:
  the path was there and route() walked into a dead end. route() never steps back (it refuses visited nodes and stops).
- The fixes need each other. Keeping last threads ends the cut-offs but turns each lonely organ into a leaf, and leaves are
  exactly where route() gets stuck: dead-end misses go UP (2701 -> 3605). With a route that backs out of dead ends
  (same 12-move budget, a step back costs a move, only the final path reinforced) every existing path was found
  (0 misses in all four backtrack runs), and both+backtrack reaches an idle organ 85.9% vs 59.8%, for +0.5 hyphae.
- What is left at 0.15 is islands: no organ alone, but the body in two pieces (e.g. a pair hanging off each other).
  None of these three fixes touches that; a lower floor does (0.015: 99.8%), at the price of ~7 more hyphae and the
  longer memory measured this morning.
Not looked at by eye; all numbers from body_*_output.txt.

## 16 Nov, 12:40 PM: can a failed signal heal the body? (heal.py) -- predictions written BEFORE running

Rare-jobs life: 1 tick in 10 a rare job (any organ -> one of the 4 idle organs), else the 3:1 habits. Floor 0.15.
Heal rule: a signal that fails grows one 1.0 hypha from where it gave up to its target.
Predictions:
- base in this life: probes reach ~65% (rare jobs keep some idle paths thick), connected ~50%.
- base_heal: +0.5 to +1 hyphae; probes ~72%; live rare jobs ~80%.
- both_bt: probes ~88%. both_bt_heal: probes ~93%, connected ~85%, cost +0.3 hyphae.
- Main question: does heal alone (base_heal) reach what both_bt does without healing? Guess: no, ~72 vs ~88.

### Results (40 seeds x 3000 ticks, floor 0.15, rare 0.1; heal_*_0.15_output.txt)

| variant | hyphae | connected | live rare jobs arrive | probes reach | heals /100 ticks | fails no path / missed |
| base          | 9.10 | 60.5% | 70.6% | 71.1% | -    | 3146 / 2407 |
| base_heal     | 9.74 | 73.0% | 77.8% | 78.5% | 2.21 | 1893 / 2238 |
| bt            | 9.47 | 65.7% | 83.7% | 86.8% | -    | 2539 / 0 |
| bt_heal       | 9.80 | 73.8% | 88.3% | 90.3% | 1.16 | 1861 / 0 |
| both_bt       | 9.89 | 90.3% | 94.9% | 94.7% | -    | 1023 / 0 |
| both_bt_heal  | 9.97 | 92.5% | 96.4% | 95.8% | 0.36 | 811 / 0 |

Against predictions: base 71% (said ~65%, a bit pessimistic again); base_heal 78.5% and +0.64 hyphae (said ~72%, +0.5-1: cost right);
both_bt 94.7% (said ~88%); both_bt_heal 95.8% (said ~93%) for only +0.08 hyphae (said +0.3). Main question right in direction:
heal alone (78.5%) is far short of backtracking alone (86.8%), never mind both_bt.
Surprise: just having rare jobs at all lifts the body a lot (connected 41 -> 60% base, 75 -> 90% both_bt): being asked for keeps
an organ joined. Healing is a small top-up once the body already has last-thread + backtracking.

### Heal hyphae are short bridges (heal_fate.py; heal_*_w*_output.txt)
Predicted ~40% of heal hyphae used before they die. Seen: base 37.5%, bt 44.9%, both_bt 50.7%; unused ones live
the plain 23 ticks, used ones a median 37-40 ticks and a median ONE use. Stronger heals (weight 3, 6) barely move
anything (both_bt_heal 95.8 -> 95.9 -> 96.4%). A heal patches the moment; the island re-forms.

### What the islands are (islands.py, both_bt, 40 seeds)
11,678 disconnected ticks; the commonest island by far is a lone pair joined by one hypha (3,548 ticks, 30%), then
chains of 3 and 4. Spells are short (median 5 ticks, max 56). A lone pair is something the last-thread rule PROTECTS:
each end's only hypha is to the other, so neither is ever pruned. Each end can see it locally (its own degree is 1
and so is its neighbour's).
Prediction for 'reach_out' (if a hypha's two ends both have degree 1, grow one 1.0 hypha from one end to a random
organ outside the pair, once per tick): lone-pair islands gone; disconnected ticks down ~30%; probes 94.7 -> ~96%; +0.1 hyphae.

### Results: reach_out (reach_out.py, run_ro.py; heal_*_ro*_output.txt, ro_sweep/)
Rare-jobs life, floor 0.15: both_bt_ro 10.09 hyphae, connected 96.2% (both_bt 90.3%), probes 97.8% (94.7%), live rare jobs 97.8%.
+ heal: 98.6%. base_ro (no last thread / backtrack): 75.8%, so reach_out needs the other two like they need each other.
Lone-pair islands gone entirely (islands_both_bt_ro.txt); disconnected ticks 11,678 -> 4,569 (-61%, I said -30%: the lone pair
was also the start of bigger islands). Cost +0.2 hyphae (said +0.1).
Demo life (no rare jobs, the 9:40 setting; note heal.py's own job rng, so both_bt reads 84.8% here vs 85.9% in body.py):
both_bt 84.8% -> both_bt_ro 93.3% for +0.4 hyphae. Heal adds nothing there (no live signal ever targets the idle organs).
Floor sweep (demo life, 40 seeds per point; reach_out_curve.png, checked only by its printed numbers, not by eye):
| floor | both_bt hyphae / reach | both_bt_ro hyphae / reach |
| 0.15  | 8.20 / 84.8% | 8.60 / 93.3% |
| 0.1   | 9.22 / 91.7% | 9.53 / 96.3% |
| 0.07  | 10.12 / 95.4% | 10.32 / 97.9% |
| 0.05  | 11.02 / 97.4% | 11.12 / 98.8% |
| 0.03  | 12.75 / 99.3% | 12.75 / 99.6% |
| 0.015 | 14.75 / 99.7% | 14.77 / 99.9% |
Per hypha, reach_out at 0.15 beats lowering the floor to 0.1 (8.60/93.3 vs 9.22/91.7). The real point: a lower floor also
lengthens memory (+28 ticks per 10x, this morning); reach_out leaves the floor alone. NOT yet checked: that reach_out leaves
the forgetting cliff where it was (it only adds hyphae, so it should, but last-thread could interact).

## 16 Nov, 3:40 PM: does the body fix move the forgetting cliff? (cliff_ro.py)

cliff_ro.py VARIANT SEEDS [floor]: myc_cliff.py setup (train A->B 60, away 400) with the body variants. Outputs cliff_ro_{base,both_bt,both_bt_ro}_{0.15,0.0015}.txt, 200 seeds each.
Predictions written first: 0.15 elsewhere median death within +-5 of 46, <= 20% keep A-B to 400; 0.0015 ~102 unchanged. Both right.
- 0.0015: all three variants prune at exactly 102 in elsewhere (200/200); both_bt and both_bt_ro outputs identical (ring intact, reach_out never fires).
- 0.15 elsewhere: base median 46, both_bt 49, both_bt_ro 51; min 46 in every variant (never earlier). Last-thread holds A-B at the floor in ~20% of runs (41-43/200), but only until lonely explore gives the lone end a second hypha; then it is pruned.
- 0.15 near/far: medians stretch (near 69 -> 84/84.5, far 60 -> 77/88). Cause not tested (guess: backtracking reuses the old road more).
- Caveat: 'A-B still there after 400' counts regrowth by explore() after a prune (base shows 11/200 at 0.0015 though all were pruned), so it is not memory.
Verdict: the three body changes keep the memory length where it was; worth one line in velisara_body_note.md.
