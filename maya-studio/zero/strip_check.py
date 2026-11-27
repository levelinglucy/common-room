"""Check the corridor law reach = w(w+4)/8 on other widths, heights and feet."""
import numpy as np
from sandpile_zero import identity


def reach(w, H, foot_w, foot_h):
    W = 2 * foot_w + w + 4
    strip = np.zeros((H + 4, W), bool)
    x0 = foot_w + 2
    strip[2:H + 2, x0:x0 + w] = True
    tee = strip.copy()
    tee[H + 2 - foot_h:H + 2, 2:W - 2] = True
    ea, et = identity(strip), identity(tee)
    diff = (ea != et) & strip
    diff[H + 2 - foot_h:, :] = False
    rows = np.where(diff.any(1))[0]
    return (H + 2 - foot_h) - rows.min() if rows.size else 0


if __name__ == "__main__":
    print("w   H     foot_w foot_h  reach  w(w+4)/8")
    cases = [(48, 900, 48, 48), (24, 600, 24, 24), (24, 600, 10, 4), (24, 600, 60, 40),
    (10, 300, 10, 10), (20, 400, 20, 20), (30, 500, 30, 30), (33, 500, 33, 33), (7, 200, 7, 7), (9, 200, 9, 9)]
    for w, H, fw, fh in cases:
        r = reach(w, H, fw, fh)
        print(f"{w:<3} {H:<5} {fw:<6} {fh:<7} {r:<6} {w*(w+4)/8:.1f}")
