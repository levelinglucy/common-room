"""What do the islands look like? For each disconnected tick, record the smaller piece(s) (organs not
in io_channel's piece) and how long each island spell lasts. usage: python3 islands.py VARIANT SEEDS"""
import sys, random, collections, statistics as st
sys.path.insert(0, '/home/sprite/maya-studio/memory')
import heal as H
try:
    import reach_out
except ImportError:
    pass
B, M = H.B, H.M
shapes = collections.Counter(); spells = []
for s in range(int(sys.argv[2])):
    net = H.CLS[sys.argv[1]](nodes=list(B.ORG), rng=random.Random(s))
    for a, b in zip(B.ORG, B.ORG[1:] + B.ORG[:1]):
        net.grow(a, b)
    life = random.Random(s + 555); cur = 0
    for t in range(B.BURN + B.RUN):
        if life.random() < H.RARE:
            tgt = life.choice(B.IDLE); src = life.choice([n for n in B.ORG if n != tgt]); net.route(src, tgt)
        else:
            net.route(*life.choice(B.HABITS))
        net.tick()
        if t < B.BURN: continue
        main = B.component(net, 'io_channel')
        rest = [n for n in B.ORG if n not in main]
        if rest:
            cur += 1
            pieces = []; left = set(rest)
            while left:
                c = B.component(net, next(iter(left))); left -= c
                k = len([h for h in net.hyphae if h[0] in c])
                pieces.append(f'{len(c)} organs/{k} hyphae')
            shapes[' + '.join(sorted(pieces))] += 1
        elif cur:
            spells.append(cur); cur = 0
print(sys.argv[1], 'disconnected ticks', sum(shapes.values()))
for k, v in shapes.most_common(8): print(f'  {v:6d}  {k}')
print('island spells:', len(spells), 'median length', st.median(spells), 'mean', round(st.mean(spells),1), 'max', max(spells))
