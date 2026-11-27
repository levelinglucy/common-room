"""'How far they can hear': nine drummers on a 16-pulse ring, one bar per move.

Same scattered start four times. Each time the drummers hear one more neighbour
each side (j = 1, 2, 3, 4). The two short gaps (the two places where beats sit
side by side) walk apart and stop with j-1 ordinary gaps between them; at j = 4
that is as far apart as they can go, which is the Euclidean rhythm E(9, 16).
Each drummer has its own note (D dorian, rising round the ring). The drummer
who just moved rings brighter. A soft tick marks all 16 pulses.
Writes ladder_piece.wav and ladder_piece_score.json.
"""
import random, json, wave, sys
import numpy as np
from trajectory import run_log, is_euclid
sys.path.insert(0, '..')
from drummers import gaps_of

K, N = 9, 16
SR = 44100
PULSE = 0.13
REPEAT_END = 3
midi = [62, 64, 65, 67, 69, 71, 72, 74, 76]
freqs = [440.0 * 2 ** ((m - 69) / 12) for m in midi]


def sep(pos):
    g = gaps_of(sorted(pos), N)
    idx = [i for i, x in enumerate(g) if x == 1]
    if len(idx) != 2 or any(x not in (1, 2) for x in g):
        return None
    d = (idx[1] - idx[0]) % K
    return min(d, K - d) - 1


def find_seed(limit=5000):
    for seed in range(limit):
        start = sorted(random.Random(seed).sample(range(N), K))
        if sep(start) is not None and sep(start) <= 0:
            pass
        runs = [run_log(start, N, j, random.Random(seed * 10 + j)) for j in (1, 2, 3, 4)]
        seps = [sep(r[0][-1]) for r in runs]
        lens = [len(r[0]) - 1 for r in runs]
        if seps == [0, 1, 2, 3] and is_euclid(runs[3][0][-1], N) and all(L >= 1 for L in lens) \
                and 12 <= sum(lens) <= 24:
            return seed, start, runs
    raise SystemExit('no seed')


def tone(f, dur=0.5, amp=0.3, bright=False):
    t = np.arange(int(dur * SR)) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 9.0)
    x += 0.35 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 25)
    if bright:
        x += 0.5 * np.sin(2 * np.pi * 4.0 * f * t) * np.exp(-t * 18)
    x += np.random.default_rng(int(f)).standard_normal(len(t)) * np.exp(-t * 400) * 0.12
    return amp * x


def tick(accent):
    t = np.arange(int(0.035 * SR)) / SR
    return (0.05 if accent else 0.02) * np.random.default_rng(2).standard_normal(len(t)) * np.exp(-t * 170)


seed, start, runs = find_seed()
bars = []
for j, (log, movers) in zip((1, 2, 3, 4), runs):
    for p, m in zip(log, movers):
        bars.append((j, 'moving', p, m))
    bars += [(j, 'settled', log[-1], None)] * REPEAT_END
    bars.append((j, 'rest', None, None))

bar_len = int(PULSE * N * SR)
out = np.zeros(bar_len * (len(bars) + 2))
for b, (j, label, pos, mover) in enumerate(bars):
    if pos is None:
        continue
    base = b * bar_len
    for s in range(N):
        tk = tick(s % 4 == 0)
        i0 = base + int(s * PULSE * SR)
        out[i0:i0 + len(tk)] += tk
    for d, s in enumerate(pos):
        x = tone(freqs[d], bright=(d == mover))
        i0 = base + int(s * PULSE * SR)
        out[i0:i0 + len(x)] += x
out *= 0.85 / np.abs(out).max()
with wave.open('ladder_piece.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())

score = [{'j': j, 'label': l, 'pos': list(p) if p else None, 'mover': m,
          'gaps': list(gaps_of(sorted(p), N)) if p else None,
          'sep': sep(p) if p else None, 'start_s': round(i * PULSE * N, 2)}
         for i, (j, l, p, m) in enumerate(bars)]
json.dump({'K': K, 'N': N, 'seed': seed, 'start': start, 'pulse_s': PULSE, 'bars': score},
          open('ladder_piece_score.json', 'w'), indent=1)
print('seed', seed, 'start', start, f'{len(bars)} bars, {len(out) / SR:.1f} s')
for x in score:
    if x['pos']:
        print(x['start_s'], 'j', x['j'], x['label'], 'gaps', ''.join(map(str, x['gaps'])), 'sep', x['sep'], 'mover', x['mover'])
