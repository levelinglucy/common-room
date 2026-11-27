"""The zero's potential. With u1, u2 the odometers of the two stabilisations,

    e = 6 - S(6) + Lap u2,   S(6) = 6 + Lap u1   =>   e = Lap (u2 - u1).

So v = u2 - u1 is a potential whose Laplacian is the zero itself. Where the
strip's and the tee's zeros agree, dv = v_tee - v_strip is harmonic. This
script measures dv on the corridor's centre line above the foot: its value
at the junction, its slope (least squares over the middle of the changed
zone), where it reaches 0, and the reach (top of the changed cells).
"""
import sys
import numpy as np
from depth import shapes
from odometer import zero_odo


def measure(w, fh, H=None, foot_w=None):
    foot_w = foot_w or 3 * w
    H = H or max(300, int(w * w / 2) + 2 * fh + 200)
    strip, tee, x0 = shapes(w, H, foot_w, fh)
    es, u1s, u2s = zero_odo(strip)
    et, u1t, u2t = zero_odo(tee)
    vs, vt = u2s - u1s, u2t - u1t
    base = H + 2 - fh
    c = x0 + w // 2
    far_s = int(vs[H // 2, c])
    dv = (vt - vs)[:base, c][::-1][1:H // 2]  # dv[k] at height k+1
    nz = np.where(dv != 0)[0]
    zero_at = int(nz.max()) + 2 if nz.size else 0
    j = int(dv[0])
    slope = 0.0
    if zero_at > 12:
        a, b = int(zero_at * 0.2), int(zero_at * 0.8)
        k = np.arange(a, b)
        slope = float(np.polyfit(k, dv[a:b], 1)[0])
    diff = (es != et) & strip
    diff[base:, :] = False
    rows = np.where(diff.any(1))[0]
    reach = base - rows.min() if rows.size else 0
    return far_s, j, slope, zero_at, reach


if __name__ == "__main__":
    print("w    fh    v_far   dv_junction  slope   dv=0_at  reach")
    for spec in sys.argv[1:]:
        w, fh = map(int, spec.split(':'))
        far_s, j, slope, zero_at, reach = measure(w, fh)
        print(f"{w:<5}{fh:<6}{far_s:<8}{j:<13}{slope:<8.2f}{zero_at:<9}{reach}", flush=True)
