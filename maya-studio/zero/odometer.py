"""Odometers (how many times each cell topples) behind a corridor's zero.

e = S(6 - S(6)). u1 = odometer of S(6), u2 = odometer of the second
stabilisation. Look at the middle column of the corridor: how u1, u2 and
their tee-minus-strip differences fall off with height above the foot.
"""
import sys
import numpy as np
from depth import shapes


def stab_odo(z, mask):
    z = z.copy(); m = mask.astype(np.int64); u = np.zeros_like(z)
    while True:
        t = z >> 2
        if not t.any():
            return z, u
        u += t
        z -= 4 * t
        g = np.zeros_like(z)
        g[1:, :] += t[:-1, :]; g[:-1, :] += t[1:, :]
        g[:, 1:] += t[:, :-1]; g[:, :-1] += t[:, 1:]
        z += g * m


def zero_odo(mask):
    six = np.where(mask, 6, 0).astype(np.int64)
    s6, u1 = stab_odo(six, mask)
    e, u2 = stab_odo(np.where(mask, six - s6, 0), mask)
    return e, u1, u2


if __name__ == "__main__":
    w = int(sys.argv[1]); H = int(sys.argv[2]); fh = int(sys.argv[3])
    strip, tee, x0 = shapes(w, H, 3 * w, fh)
    es, u1s, u2s = zero_odo(strip)
    et, u1t, u2t = zero_odo(tee)
    base = H + 2 - fh
    c = x0 + w // 2
    mid = H // 2
    print(f"w={w} fh={fh}: far-field centre odometers u1={u1s[mid, c]} u2={u2s[mid, c]}")
    print(f"  max over corridor cross-section far: u1={u1s[mid].max()} u2={u2s[mid].max()}")
    print("  d   u1_strip u1_tee  u2_strip u2_tee  d_u1  d_u2  rowdiff")
    for d in list(range(1, 12)) + list(range(12, 200, 8)):
        r = base - d
        if r < 3: break
        rowdiff = int(((es[r] != et[r]) & strip[r]).sum())
        print(f"  {d:<4}{u1s[r, c]:<9}{u1t[r, c]:<8}{u2s[r, c]:<9}{u2t[r, c]:<8}{u1t[r, c]-u1s[r, c]:<6}{u2t[r, c]-u2s[r, c]:<6}{rowdiff}")
