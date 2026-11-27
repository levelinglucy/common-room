"""
The forgetting cliff, run in Velisara's own mycelium.py (unchanged, imported).

Setup: ring of the 8 demo organs plus one direct hypha io_channel <-> memory_store (A-B) at 1.0.
Train: habit A->B for TRAIN ticks (one route + one tick per tick).
Away:  habit X->Y for AWAY ticks. Record the first tick the A-B hypha is pruned.
  elsewhere: dream_engine -> symbolic_renderer (ring neighbours, never touches A or B)
  near:      io_channel -> logger (logger is B's ring neighbour: the old road leads there)
  far:       io_channel -> dream_engine (old road is a dead end for it)
Also: the moment the away habit gets its own direct hypha (A-C), since route() jumps straight
to a target that is a neighbour.

usage: python3 myc_cliff.py SEEDS [prune_below]
"""
import sys, random, math, statistics as st
sys.path.insert(0, '/home/sprite')
import mycelium as M

ORG = ['identity_store', 'memory_store', 'logger', 'scheduler', 'io_channel',
       'recovery_manager', 'dream_engine', 'symbolic_renderer']
A, B = 'io_channel', 'memory_store'
AWAY = {'elsewhere': ('dream_engine', 'symbolic_renderer'),
        'near': ('io_channel', 'logger'),
        'far': ('io_channel', 'dream_engine')}
TRAIN, AWAY_T = 60, 400


def run(seed, cond, train=True):
    net = M.Mycelium(nodes=list(ORG), rng=random.Random(seed))
    for a, b in zip(ORG, ORG[1:] + ORG[:1]):
        net.grow(a, b)
    net.grow(A, B)
    kAB = M._key(A, B)
    for _ in range(TRAIN):
        if train:
            net.route(A, B)
        else:
            net.route(*AWAY['elsewhere'])
        net.tick()
    if kAB not in net.hyphae:
        return dict(w0=0.0, death=0, direct=None, uses=0, last=0, ring=0, nh=0)
    w0 = net.hyphae[kAB]
    ring_left = sum(M._key(a, b) in net.hyphae for a, b in zip(ORG, ORG[1:] + ORG[:1]))
    n_after_train = len(net.hyphae)
    x, y = AWAY[cond]
    kXY = M._key(x, y)
    death = direct = None
    uses = 0
    last = 0
    for t in range(1, AWAY_T + 1):
        p = net.route(x, y)
        if p[-1] == y and any(M._key(u, v) == kAB for u, v in zip(p, p[1:])):
            uses += 1
            last = t
        if direct is None and kXY in net.hyphae:
            direct = t
        res = net.tick()
        # tick() prunes, then explore() may regrow the same pair at 1.0 in the same tick,
        # so death is read from the prune list, not from whether the key is still there.
        if kAB in res['pruned']:
            death = t
            break
    return dict(w0=w0, death=death, direct=direct, uses=uses, last=last, ring=ring_left, nh=n_after_train)


if __name__ == '__main__':
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    if len(sys.argv) > 2:
        M.PRUNE_BELOW = float(sys.argv[2])
    rate = -math.log(M.DECAY)
    print(f'PRUNE_BELOW={M.PRUNE_BELOW}  DECAY={M.DECAY}  rate={rate:.5f}/tick')
    print(f'steady trained weight (route every tick) = 0.92*0.6/0.08 = {M.DECAY*M.REINFORCE/(1-M.DECAY):.3f}')
    for cond in AWAY:
        rs = [run(s, cond) for s in range(seeds)]
        w0 = st.mean(r['w0'] for r in rs)
        pred = math.ceil(math.log(w0 / M.PRUNE_BELOW) / rate)
        deaths = [r['death'] for r in rs if r['death'] is not None]
        alive = sum(r['death'] is None for r in rs)
        uses = [r['uses'] for r in rs]
        directs = [r['direct'] for r in rs if r['direct'] is not None]
        print(f'\n[{cond}] {AWAY[cond][0]} -> {AWAY[cond][1]}  seeds={seeds}  w0={w0:.3f}  pure-decay prediction: pruned at tick {pred}')
        if deaths:
            q = st.quantiles(deaths, n=10) if len(deaths) > 1 else [deaths[0]] * 9
            print(f'  pruned at: min {min(deaths)}  median {st.median(deaths)}  p90 {q[8]:.0f}  max {max(deaths)}  (still alive after {AWAY_T}: {alive})')
            print(f'  exactly at prediction: {sum(d == pred for d in deaths)}/{seeds}')
        if cond == 'elsewhere':
            print(f'  after training: birth-ring hyphae left (of 8): mean {st.mean(r["ring"] for r in rs):.2f}, max {max(r["ring"] for r in rs)}; hyphae total mean {st.mean(r["nh"] for r in rs):.2f}')
        lag = [r['death'] - r['last'] for r in rs if r['death'] is not None and r['last'] > 0]
        if lag:
            print(f'  runs where the away habit reused A-B: {len(lag)}/{seeds}; pruned this many ticks after its last use: min {min(lag)} median {st.median(lag)} max {max(lag)}')
        print(f'  successful away routes that used A-B: mean {st.mean(uses):.1f}, max {max(uses)}')
        if directs:
            print(f'  away habit got its own direct hypha: {len(directs)}/{seeds}, median tick {st.median(directs)}')
        if cond != 'elsewhere' and deaths:
            pairs = [(r['direct'], r['death']) for r in rs if r['direct'] is not None and r['death'] is not None]
            if pairs:
                gap = [d - dr for dr, d in pairs]
                print(f'  death minus direct-hypha tick: median {st.median(gap)}, min {min(gap)}, max {max(gap)}  (pure decay from rehearsed weight would be <= {pred})')
