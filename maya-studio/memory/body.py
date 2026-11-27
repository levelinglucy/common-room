"""
Does Velisara's mycelium keep its whole body? (mycelium.py imported unchanged.)

The demo life: 8 organs on a birth ring, habits io_channel->memory_store (3 in 4)
and dream_engine->symbolic_renderer (1 in 4), one route + one tick per tick.
Four organs are never in a habit: identity_store, logger, scheduler, recovery_manager.

After BURN ticks, for RUN ticks, record every tick:
  - number of hyphae
  - which organs have no hypha at all (cut off)
  - whether the hyphae graph is connected
Every PROBE ticks, on a deep copy (so the real net is untouched):
  - can a signal from io_channel actually reach each idle organ with route()?
    (route is local and greedy-random; a path existing is not the same as finding it)

Variants (subclasses, mycelium.py itself untouched):
  base        unchanged
  last_thread a hypha that is some organ's only hypha is never pruned (held at the floor)
  lonely      explore() grows from the least-connected organ to a random unjoined one

usage: python3 body.py VARIANT SEEDS [prune_below]
"""
import sys, random, copy, statistics as st
sys.path.insert(0, '/home/sprite')
import mycelium as M

ORG = ['identity_store', 'memory_store', 'logger', 'scheduler', 'io_channel',
       'recovery_manager', 'dream_engine', 'symbolic_renderer']
IDLE = ['identity_store', 'logger', 'scheduler', 'recovery_manager']
HABITS = [('io_channel', 'memory_store')] * 3 + [('dream_engine', 'symbolic_renderer')]
BURN, RUN, PROBE = 300, 3000, 25


def degree(net):
    d = {n: 0 for n in net.nodes}
    for a, b in net.hyphae:
        d[a] += 1
        d[b] += 1
    return d


class LastThread(M.Mycelium):
    def tick(self):
        self.age += 1
        pruned = []
        for k in list(self.hyphae):
            self.hyphae[k] *= M.DECAY
        d = degree(self)
        for k in sorted(self.hyphae, key=lambda k: self.hyphae[k]):
            if self.hyphae[k] < M.PRUNE_BELOW:
                a, b = k
                if d[a] == 1 or d[b] == 1:
                    self.hyphae[k] = M.PRUNE_BELOW  # last thread: hold at the floor
                    continue
                del self.hyphae[k]
                d[a] -= 1
                d[b] -= 1
                pruned.append(k)
        grown = self.explore() if self.rng.random() < M.GROW_CHANCE else None
        return {'age': self.age, 'pruned': pruned, 'grown': grown}


class Lonely(M.Mycelium):
    def explore(self):
        d = degree(self)
        cands = [n for n in self.nodes
                 if any(M._key(n, m) not in self.hyphae for m in self.nodes if m != n)]
        if not cands:
            return None
        low = min(d[n] for n in cands)
        a = self.rng.choice([n for n in cands if d[n] == low])
        b = self.rng.choice([m for m in self.nodes if m != a and M._key(a, m) not in self.hyphae])
        self.grow(a, b)
        return a, b


class Both(LastThread, Lonely):
    pass


class Backtrack:
    """route() that steps back out of a dead end instead of giving up.
    Same weighted choice, same 12-move budget (a step back costs a move).
    Only the final simple path is reinforced."""
    def route(self, source, target, max_steps=12):
        path = [source]
        visited = {source}
        moves = 0
        while path[-1] != target and moves < max_steps:
            here = path[-1]
            options = {n: w for n, w in self.neighbours(here).items() if n not in visited}
            if target in options:
                nxt = target
            elif options:
                names, weights = zip(*options.items())
                nxt = self.rng.choices(names, weights=weights, k=1)[0]
            else:
                if len(path) == 1:
                    break
                path.pop()
                moves += 1
                continue
            path.append(nxt)
            visited.add(nxt)
            moves += 1
        if path[-1] == target:
            self._reinforce(path)
        return path


class BaseBT(Backtrack, M.Mycelium):
    pass


class BothBT(Backtrack, Both):
    pass


CLS = {'base': M.Mycelium, 'last_thread': LastThread, 'lonely': Lonely, 'both': Both, 'base_bt': BaseBT, 'both_bt': BothBT}


def component(net, start):
    seen = {start}
    todo = [start]
    while todo:
        x = todo.pop()
        for y in net.neighbours(x):
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def connected(net):
    seen = {net.nodes[0]}
    todo = [net.nodes[0]]
    while todo:
        x = todo.pop()
        for y in net.neighbours(x):
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return len(seen) == len(net.nodes)


def run(variant, seed):
    net = CLS[variant](nodes=list(ORG), rng=random.Random(seed))
    for a, b in zip(ORG, ORG[1:] + ORG[:1]):
        net.grow(a, b)
    nh, conn = [], 0
    cut = {n: 0 for n in ORG}
    reach = {n: [0, 0] for n in IDLE}
    fail = {'no_path': 0, 'path_missed': 0, 'missed_dead_end': 0, 'missed_steps': 0}
    first_cut = None
    for t in range(BURN + RUN):
        net.route(*net.rng.choice(HABITS))
        net.tick()
        d = degree(net)
        if first_cut is None and any(d[n] == 0 for n in ORG):
            first_cut = t + 1
        if t < BURN:
            continue
        nh.append(len(net.hyphae))
        conn += connected(net)
        for n in ORG:
            cut[n] += d[n] == 0
        if t % PROBE == 0:
            for n in IDLE:
                c = copy.deepcopy(net)
                c.rng = random.Random(seed * 100003 + t * 7 + IDLE.index(n))
                exists = n in component(net, 'io_channel')
                p = c.route('io_channel', n)
                ok = p[-1] == n
                reach[n][0] += ok
                reach[n][1] += 1
                if not ok:
                    if not exists:
                        fail['no_path'] += 1
                    else:
                        fail['path_missed'] += 1
                        fail['missed_steps' if (len(p) == 13 or variant.endswith('_bt')) else 'missed_dead_end'] += 1
    return dict(nh=st.mean(nh), conn=conn / RUN, cut={n: cut[n] / RUN for n in ORG},
                reach={n: reach[n][0] / reach[n][1] for n in IDLE}, first_cut=first_cut,
                fail=fail, probes=sum(v[1] for v in reach.values()))


if __name__ == '__main__':
    variant, seeds = sys.argv[1], int(sys.argv[2])
    if len(sys.argv) > 3:
        M.PRUNE_BELOW = float(sys.argv[3])
    rs = [run(variant, s) for s in range(seeds)]
    print(f'variant={variant} prune_below={M.PRUNE_BELOW} seeds={seeds} burn={BURN} run={RUN}')
    print(f'mean hyphae alive: {st.mean(r["nh"] for r in rs):.2f}')
    print(f'whole body connected: {100 * st.mean(r["conn"] for r in rs):.1f}% of ticks')
    fc = [r['first_cut'] for r in rs if r['first_cut'] is not None]
    print(f'first organ cut off: {len(fc)}/{seeds} runs, median tick {st.median(fc) if fc else "-"}')
    print('organ                cut off %   route from io_channel reaches it %')
    for n in ORG:
        c = 100 * st.mean(r['cut'][n] for r in rs)
        rr = f'{100 * st.mean(r["reach"][n] for r in rs):.1f}' if n in IDLE else '(habit)'
        print(f'  {n:18s} {c:7.1f}     {rr}')
    avg_reach = st.mean(st.mean(r['reach'][n] for n in IDLE) for r in rs)
    print(f'idle organs reached on one try, average: {100 * avg_reach:.1f}%')
    P = sum(r['probes'] for r in rs)
    F = {k: sum(r['fail'][k] for r in rs) for k in rs[0]['fail']}
    print(f'failed probes: {sum(F[k] for k in ("no_path", "path_missed"))}/{P}: '
          f'no path at all {F["no_path"]}, path existed but route missed it {F["path_missed"]} '
          f'(dead end {F["missed_dead_end"]}, ran out of 12 steps {F["missed_steps"]})')
