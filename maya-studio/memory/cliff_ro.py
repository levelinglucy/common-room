"""
Does the body fix (last thread + lonely explore + backtracking + reach_out) move the forgetting cliff?
Same setup as myc_cliff.py (imported), but the net is one of the variant classes.

In mycelium.py, route() jumps straight to a target that is a neighbour, so 'remembering A->B'
means the A-B hypha still exists, whatever its weight. Last-thread can hold a hypha at the floor
instead of pruning it, so besides the prune tick this records:
  held   - first tick A-B was held at the floor (it would have died without last-thread)
  alive  - A-B still exists after the away phase (A->B would still arrive in one step)

Predictions (written before running, 16 Nov 3:40 PM):
  floor 0.15, elsewhere: median death within +-5 of 46; at most 20% of runs keep A-B to tick 400.
  floor 0.0015, elsewhere: ~102, unchanged.

usage: python3 cliff_ro.py VARIANT SEEDS [prune_below]
"""
import sys, random, math, statistics as st
sys.path.insert(0, '/home/sprite/maya-studio/memory')
import reach_out, heal as H
import myc_cliff as C
M = H.M
B = H.B
CLS = dict(H.CLS)


def run(variant, seed, cond):
    net = CLS[variant](nodes=list(C.ORG), rng=random.Random(seed))
    for a, b in zip(C.ORG, C.ORG[1:] + C.ORG[:1]):
        net.grow(a, b)
    net.grow(C.A, C.B)
    kAB = M._key(C.A, C.B)
    for _ in range(C.TRAIN):
        net.route(C.A, C.B)
        net.tick()
    if kAB not in net.hyphae:
        return dict(death=0, held=None, alive=False, ring=0, why=None)
    ring = sum(M._key(a, b) in net.hyphae for a, b in zip(C.ORG, C.ORG[1:] + C.ORG[:1]))
    x, y = C.AWAY[cond]
    death = held = None
    why = None
    for t in range(1, C.AWAY_T + 1):
        net.route(x, y)
        res = net.tick()
        if kAB in res['pruned']:
            death = t
            break
        if held is None and kAB in net.hyphae and abs(net.hyphae[kAB] - M.PRUNE_BELOW) < 1e-12:
            held = t
            d = B.degree(net)
            why = (d[C.A], d[C.B])
    return dict(death=death, held=held, alive=kAB in net.hyphae, ring=ring, why=why)


if __name__ == '__main__':
    variant, seeds = sys.argv[1], int(sys.argv[2])
    if len(sys.argv) > 3:
        M.PRUNE_BELOW = float(sys.argv[3])
    rate = -math.log(M.DECAY)
    print(f'variant={variant} PRUNE_BELOW={M.PRUNE_BELOW} seeds={seeds} away={C.AWAY_T}')
    for cond in C.AWAY:
        rs = [run(variant, s, cond) for s in range(seeds)]
        deaths = [r['death'] for r in rs if r['death']]
        helds = [r['held'] for r in rs if r['held']]
        alive = sum(r['alive'] for r in rs)
        print(f'\n[{cond}]')
        print(f'  birth-ring hyphae left after training: mean {st.mean(r["ring"] for r in rs):.2f}')
        if deaths:
            print(f'  pruned: {len(deaths)}/{seeds}; min {min(deaths)} median {st.median(deaths)} max {max(deaths)}')
        print(f'  ever held at the floor: {len(helds)}/{seeds}' + (f', first hold median tick {st.median(helds)}' if helds else ''))
        whys = [r['why'] for r in rs if r['why']]
        if whys:
            a1 = sum(w[0] == 1 for w in whys); b1 = sum(w[1] == 1 for w in whys)
            print(f'  at first hold: {C.A} had degree 1 in {a1}, {C.B} had degree 1 in {b1}')
        print(f'  A-B still there after {C.AWAY_T} ticks: {alive}/{seeds}')
