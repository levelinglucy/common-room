"""
Can a failed signal heal the body? (mycelium.py and body.py imported unchanged.)

The 9:40 session found that with last-thread + backtracking, every failure left is an island:
the body in two pieces. Idea: a signal that fails knows it failed (path[-1] != target).
Heal rule: when route() fails, grow one new hypha (START_WEIGHT) from the organ where the
signal gave up to its target. Local: only the signal's own tip and its own target.

But in the 9:40 demo life nothing ever signals the idle organs, so nothing could fail there.
Rare-jobs life: each tick, with chance RARE a rare job (source: any organ, target: one of the
four idle organs, distinct), else a habit as before (3:1).

Recorded (after BURN, for RUN ticks): hyphae alive, body connected, live rare-job success,
and the same probes as body.py (deep copy, io_channel -> each idle organ, no heal on probes).

usage: python3 heal.py VARIANT SEEDS [prune_below] [rare]
"""
import sys, random, copy, statistics as st
sys.path.insert(0, '/home/sprite/maya-studio/memory')
import body as B
M = B.M

RARE = 0.1
import os
HEALW = float(os.environ.get('HEALW', '1.0'))  # weight of a heal hypha (default START_WEIGHT)


class Heal:
    heals = 0
    healing = True

    def route(self, source, target, max_steps=12):
        p = super().route(source, target, max_steps)
        if self.healing and p[-1] != target:
            self.grow(p[-1], target, HEALW)
            self.heals += 1
        return p


def mk(*bases):
    return type('V', bases, {})


CLS = {
    'base': M.Mycelium,
    'base_heal': mk(Heal, M.Mycelium),
    'bt': B.BaseBT,
    'bt_heal': mk(Heal, B.BaseBT),
    'both_bt': B.BothBT,
    'both_bt_heal': mk(Heal, B.BothBT),
}


def run(variant, seed):
    net = CLS[variant](nodes=list(B.ORG), rng=random.Random(seed))
    for a, b in zip(B.ORG, B.ORG[1:] + B.ORG[:1]):
        net.grow(a, b)
    life = random.Random(seed + 555)  # job choice kept apart from the net's own rng
    nh, conn = [], 0
    jobs = [0, 0]
    reach = [0, 0]
    fail = {'no_path': 0, 'path_missed': 0}
    heals0 = None
    for t in range(B.BURN + B.RUN):
        if t == B.BURN:
            heals0 = getattr(net, 'heals', 0)
        if life.random() < RARE:
            tgt = life.choice(B.IDLE)
            src = life.choice([n for n in B.ORG if n != tgt])
            ok = net.route(src, tgt)[-1] == tgt
            if t >= B.BURN:
                jobs[0] += ok
                jobs[1] += 1
        else:
            net.route(*life.choice(B.HABITS))
        net.tick()
        if t < B.BURN:
            continue
        nh.append(len(net.hyphae))
        conn += B.connected(net)
        if t % B.PROBE == 0:
            for n in B.IDLE:
                c = copy.deepcopy(net)
                c.healing = False
                c.rng = random.Random(seed * 100003 + t * 7 + B.IDLE.index(n))
                exists = n in B.component(net, 'io_channel')
                ok = c.route('io_channel', n)[-1] == n
                reach[0] += ok
                reach[1] += 1
                if not ok:
                    fail['no_path' if not exists else 'path_missed'] += 1
    return dict(nh=st.mean(nh), conn=conn / B.RUN, jobs=jobs[0] / max(1, jobs[1]),
                reach=reach[0] / reach[1], fail=fail, probes=reach[1],
                heals=(getattr(net, 'heals', 0) - heals0) / B.RUN)


if __name__ == '__main__':
    variant, seeds = sys.argv[1], int(sys.argv[2])
    if len(sys.argv) > 3:
        M.PRUNE_BELOW = float(sys.argv[3])
    if len(sys.argv) > 4:
        RARE = float(sys.argv[4])
    rs = [run(variant, s) for s in range(seeds)]
    P = sum(r['probes'] for r in rs)
    F = {k: sum(r['fail'][k] for r in rs) for k in rs[0]['fail']}
    print(f'heal weight={HEALW}')
    print(f'variant={variant} prune_below={M.PRUNE_BELOW} rare={RARE} seeds={seeds} burn={B.BURN} run={B.RUN}')
    print(f'mean hyphae alive: {st.mean(r["nh"] for r in rs):.2f}')
    print(f'whole body connected: {100 * st.mean(r["conn"] for r in rs):.1f}% of ticks')
    print(f'live rare jobs that arrived: {100 * st.mean(r["jobs"] for r in rs):.1f}%')
    print(f'heals per 100 ticks: {100 * st.mean(r["heals"] for r in rs):.2f}')
    print(f'probe io_channel -> idle organ reached: {100 * st.mean(r["reach"] for r in rs):.1f}%')
    print(f'failed probes {F["no_path"] + F["path_missed"]}/{P}: no path {F["no_path"]}, path missed {F["path_missed"]}')
