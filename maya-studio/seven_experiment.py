"""Hawk experiment for seven_neighbours.py: one rule per process.
usage: python3 seven_experiment.py MODE R SEEDS
"""
import sys
import numpy as np
import seven_neighbours as s

mode, R, seeds = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
rows = []
for seed in range(seeds):
    r = s.run(mode, R, 1000 + seed, hawk_on=True)
    rows.append(r)
    print(f"{mode} R={R} seed {seed}: calm nb {r['calm_cnt']:.1f} calm largest {r['calm_largest']:.2f}"
          f" -> after hawk largest {r['largest']:.2f}, pieces>=5 {r['pieces']}, strays {r['strays']},"
          f" alone peak {r['alone_peak']:.3f}", flush=True)
f = lambda k: np.array([r[k] for r in rows], float)
whole_before = f('calm_largest') >= 0.95
whole_after = f('largest') >= 0.95
print(f"SUMMARY {mode} R={R}: calm nb {f('calm_cnt').mean():.1f} | whole before hawk {whole_before.sum()}/{seeds}"
      f" | whole after {whole_after.sum()}/{seeds} | broken by hawk {(whole_before & ~whole_after).sum()}"
      f" | mean largest before {f('calm_largest').mean():.2f} after {f('largest').mean():.2f}"
      f" | mean pieces {f('pieces').mean():.1f} | mean strays {f('strays').mean():.1f}"
      f" | mean alone peak {f('alone_peak').mean():.3f} | mean scared bird-steps {f('scared').mean():.0f}", flush=True)
