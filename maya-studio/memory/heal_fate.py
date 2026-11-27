"""Fate of heal hyphae: is a hypha grown by a failed signal ever used again before it is pruned?
Prediction (written before running): ~40% used before they die; lifespan of unused ones 23 ticks.
usage: python3 heal_fate.py VARIANT SEEDS [weight]"""
import sys, random, statistics as st
sys.path.insert(0, '/home/sprite/maya-studio/memory')
import heal as H
B, M = H.B, H.M
W = float(sys.argv[3]) if len(sys.argv) > 3 else M.START_WEIGHT

def make(base):
    class F(base):
        def route(self, source, target, max_steps=12):
            p = base.route(self, source, target, max_steps)
            if p[-1] == target:
                for a, b in zip(p, p[1:]):
                    k = M._key(a, b)
                    if k in self.track:
                        self.track[k][1] += 1
            elif p[-1] != target:
                k = M._key(p[-1], target)
                if k not in self.hyphae:
                    self.grow(p[-1], target, W)
                    self.track[k] = [self.age, 0]
            return p
        def tick(self):
            r = base.tick(self)
            for k in r['pruned']:
                if k in self.track:
                    born, uses = self.track.pop(k)
                    self.dead.append((self.age - born, uses))
            return r
    return F

base = {'base': M.Mycelium, 'bt': B.BaseBT, 'both_bt': B.BothBT}[sys.argv[1]]
C = make(base)
out = []
for s in range(int(sys.argv[2])):
    net = C(nodes=list(B.ORG), rng=random.Random(s)); net.track = {}; net.dead = []
    for a, b in zip(B.ORG, B.ORG[1:] + B.ORG[:1]):
        net.grow(a, b)
    life = random.Random(s + 555)
    for t in range(B.BURN + B.RUN):
        if life.random() < H.RARE:
            tgt = life.choice(B.IDLE); src = life.choice([n for n in B.ORG if n != tgt])
            net.route(src, tgt)
        else:
            net.route(*life.choice(B.HABITS))
        net.tick()
    out += net.dead
used = [d for d in out if d[1] > 0]
unused = [d for d in out if d[1] == 0]
print(f'variant={sys.argv[1]} weight={W} heal hyphae that died: {len(out)}')
print(f'used at least once before dying: {len(used)} ({100*len(used)/len(out):.1f}%)')
print(f'lifespan unused: median {st.median([d[0] for d in unused])}, used: median {st.median([d[0] for d in used]) if used else "-"}')
print(f'uses among used: median {st.median([d[1] for d in used]) if used else "-"}, max {max([d[1] for d in used]) if used else "-"}')
