"""Which (letter, k) pairs allow a 'balance only' slip: every gap still
floor/ceil of 26/k, the ring just isn't maximally even, and exactly one
one-seat move fixes it, made by the drummer on the letter's seat."""
from one_beat_off import rotations, restorers, N
import json
res = {}
for k in range(5, 14):
    if N % k == 0: continue
    lo = N // k
    rots = rotations(k, N); rset = set(rots)
    for seat in range(N):
        opts = []
        for rot in rots:
            for d in (-1, 1):
                home = (seat - d) % N
                if home not in rot or seat in rot: continue
                beats = sorted((set(rot) - {home}) | {seat})
                if frozenset(beats) in rset: continue
                g = [(beats[(i+1)%k]-beats[i]) % N for i in range(k)]
                if any(x < lo or x > lo+1 for x in g): continue
                f = restorers(beats, k, N, rset)
                if len(f) == 1 and f[0][0] == seat:
                    opts.append(beats)
        if opts:
            res.setdefault(chr(65+seat), {})[k] = opts
for L in sorted(res):
    print(L, {k: len(v) for k, v in res[L].items()})
json.dump(res, open('hard_options.json', 'w'))
