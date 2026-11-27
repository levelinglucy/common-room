"""Check ladder_piece.wav against its score: every drummer note should start
where the score says (energy jump in the tonal band at that pulse), and nowhere else."""
import json, wave
import numpy as np

sc = json.load(open('ladder_piece_score.json'))
w = wave.open('ladder_piece.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32767
print('duration', round(len(x) / sr, 2), 's, peak', round(np.abs(x).max(), 3),
      'clipped samples', int((np.abs(x) > 0.999).sum()))
P = sc['pulse_s']; N = sc['N']
win = int(0.03 * sr)
hits = misses = false = 0
for b, bar in enumerate(sc['bars']):
    expected = set(bar['pos']) if bar['pos'] else set()
    for s in range(N):
        i0 = int((b * N + s) * P * sr)
        before = x[max(0, i0 - win):i0]
        after = x[i0:i0 + win]
        if len(after) < win:
            continue
        rise = np.sqrt((after ** 2).mean()) - np.sqrt((before ** 2).mean() if len(before) else 0)
        onset = rise > 0.03
        if s in expected:
            hits += onset; misses += (not onset)
        else:
            false += onset
print(f'note onsets found {hits}, expected but missing {misses}, unexpected {false}')
