"""The ramp: in the tee, the second stabilisation's odometer climbs one per row
up the corridor until it reaches a plateau. Measure, for each (w, fh):
P = strip far-field centre u2 (parabola peak), T = tee far-field centre u2,
the ramp slope (median per-row climb where it climbs), the ramp end, reach.
"""
import sys
import numpy as np
from depth import shapes
from odometer import zero_odo


def measure(w, H, fh, foot_w=None):
    foot_w = foot_w or 3 * w
    strip, tee, x0 = shapes(w, H, foot_w, fh)
    es, _, u2s = zero_odo(strip)
    et, _, u2t = zero_odo(tee)
    base = H + 2 - fh
    c = x0 + w // 2
    mid = H // 2
    P, T = int(u2s[mid, c]), int(u2t[mid, c])
    col = u2t[2:base, c][::-1]  # col[k] = u2 at height k+1 above the foot
    steps = np.diff(col)
    climbing = steps[steps > 0]
    slope = float(np.median(climbing)) if climbing.size else 0.0
    nz = np.where(col != T)[0]
    ramp_end = int(nz.max()) + 1 if nz.size else 0
    diff = (es != et) & strip
    diff[base:, :] = False
    rows = np.where(diff.any(1))[0]
    reach = base - rows.min() if rows.size else 0
    return P, T, slope, ramp_end, reach, int(col.min())


if __name__ == "__main__":
    for spec in sys.argv[1:]:
        w, fh = map(int, spec.split(':'))
        H = max(300, int(w * w / 2) + 4 * fh + 100)
        P, T, slope, ramp_end, reach, umin = measure(w, H, fh)
        print(f"w={w:<3} fh={fh:<4} P={P:<5} T={T:<5} T/P={T/P:.2f} slope={slope:.1f} ramp_end={ramp_end:<5} reach={reach:<5} min_u2={umin}", flush=True)
