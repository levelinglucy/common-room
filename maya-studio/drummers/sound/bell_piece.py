"""'Finding the bell': drummers on a 12-pulse ring, played one bar per move.

Seven drummers, each with its own note (a D dorian scale, rising round the ring),
start scattered. Part by part:
  near-deaf band (hears 1 neighbour each side)  -> gets stuck, stuck bar x4
  same start, wide ear (hears 3 each side = all) -> walks into the bell, bell x4
for several starts. A soft tick marks all 12 pulses, accent on pulse 0.
Writes bell_piece.wav, bell_piece_score.json (every bar, for the picture).
"""
import random, json, wave, sys
import numpy as np
from trajectory import run_log, is_euclid
sys.path.insert(0, '..')
from drummers import gaps_of

K, N = 7, 12
SR = 44100
PULSE = 0.16            # seconds per pulse -> 1.92 s per bar
SEEDS = [int(s) for s in sys.argv[1:]] or [4, 0, 6]
REPEAT_END = 4

# D dorian from D4: D E F G A B C
midi = [62, 64, 65, 67, 69, 71, 72]
freqs = [440.0 * 2 ** ((m - 69) / 12) for m in midi]


def tone(f, dur=0.5, amp=0.32, bright=False):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 9.0)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 25)
    if bright:
        x += 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 30)
    click = np.random.default_rng(int(f)).standard_normal(len(t)) * np.exp(-t * 400) * 0.15
    return amp * (x * env + click)


def tick(accent):
    t = np.arange(int(0.04 * SR)) / SR
    n = np.random.default_rng(1).standard_normal(len(t))
    return (0.06 if accent else 0.025) * n * np.exp(-t * 160)


bars = []    # (label, positions tuple, mover or None)
for seed in SEEDS:
    rng = random.Random(seed)
    start = sorted(rng.sample(range(N), K))
    lo, mlo = run_log(start, N, 1, random.Random(1000 + seed))
    hi, mhi = run_log(start, N, 3, random.Random(2000 + seed))
    assert not is_euclid(lo[-1], N) and is_euclid(hi[-1], N), seed
    for p, m in zip(lo, mlo):
        bars.append(('near-deaf', p, m))
    bars += [('near-deaf stuck', lo[-1], None)] * (REPEAT_END - 1)
    for p, m in zip(hi, mhi):
        bars.append(('wide ear', p, m))
    bars += [('wide ear: the bell', hi[-1], None)] * (REPEAT_END - 1)
    bars.append(('rest', None, None))

bar_len = int(PULSE * N * SR)
out = np.zeros(bar_len * (len(bars) + 2), dtype=float)
for b, (label, pos, mover) in enumerate(bars):
    base = b * bar_len
    if pos is None:
        continue
    for s in range(N):
        tk = tick(s == 0)
        i0 = base + int(s * PULSE * SR)
        out[i0:i0 + len(tk)] += tk
    for d, s in enumerate(pos):
        x = tone(freqs[d], bright=(d == mover))
        i0 = base + int(s * PULSE * SR)
        out[i0:i0 + len(x)] += x
out /= max(1e-9, np.abs(out).max()) / 0.85
pcm = (out * 32767).astype(np.int16)
with wave.open('bell_piece.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())

score = [{'label': l, 'pos': list(p) if p else None, 'mover': m,
          'gaps': list(gaps_of(sorted(p), N)) if p else None} for l, p, m in bars]
json.dump({'K': K, 'N': N, 'seeds': SEEDS, 'pulse_s': PULSE, 'bars': score},
          open('bell_piece_score.json', 'w'), indent=1)
print(f'{len(bars)} bars, {len(pcm) / SR:.1f} s')
for x in score:
    print(x['label'], x['pos'], 'mover', x['mover'], 'gaps', x['gaps'])
