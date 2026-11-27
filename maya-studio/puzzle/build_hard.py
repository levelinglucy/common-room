import json, random
from one_beat_off import solve
opts = json.load(open('hard_options.json'))
msg = 'WIDEEAR'; ks = [11, 10, 11, 10, 11, 10, 11]
rng = random.Random(29)
rings = [{'letter': c, 'k': k, 'beats': rng.choice(opts[c][str(k)])} for c, k in zip(msg, ks)]
got = solve(rings)
print('solved', got); assert got == msg
for r in rings:
    b = r['beats']; k = len(b)
    print(r['letter'], k, [x+1 for x in b], [(b[(i+1)%k]-b[i]) % 26 for i in range(k)])
json.dump(rings, open('one_beat_off_hard.json', 'w'))
