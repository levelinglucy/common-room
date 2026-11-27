"""How deep does the end pattern of a corridor's zero go?

For a plain strip (width w) and for the same strip standing on a foot,
measure how far up from the bottom end (or the foot's top edge) the zero
still differs from the corridor's far pattern (the row pattern in the middle
of the strip). Then compare with the reach (where strip and tee differ).
"""
import sys
import numpy as np
from sandpile_zero import identity


def shapes(w, H, foot_w, foot_h):
    W = 2 * foot_w + w + 4
    strip = np.zeros((H + 4, W), bool)
    x0 = foot_w + 2
    strip[2:H + 2, x0:x0 + w] = True
    tee = strip.copy()
    if foot_h:
        tee[H + 2 - foot_h:H + 2, 2:W - 2] = True
    return strip, tee, x0


def far_rows(e, x0, w, H):
    mid = H // 2 + 2
    return e[mid, x0:x0 + w]


def depth_from(e, x0, w, top_of_end, far):
    """rows above top_of_end (exclusive) whose corridor row != far pattern;
    return distance of the furthest such row (scanning up until mid)."""
    rows = []
    for r in range(top_of_end - 1, 1, -1):
        if not np.array_equal(e[r, x0:x0 + w], far):
            rows.append(top_of_end - r)
    return max(rows) if rows else 0


def run(w, H, foot_w, foot_h):
    strip, tee, x0 = shapes(w, H, foot_w, foot_h)
    es, et = identity(strip), identity(tee)
    far = far_rows(es, x0, w, H)
    farT = far_rows(et, x0, w, H)
    assert np.array_equal(far, farT)
    # only look at the lower half of the corridor
    base = H + 2 - foot_h
    half = H // 2
    def depth(e, bottom):
        d = 0
        for k in range(1, half - 5):
            r = bottom - k
            if not np.array_equal(e[r, x0:x0 + w], far):
                d = k
        return d
    ds = depth(es, base)  # strip: same rows, measured from the same line
    dt = depth(et, base)
    diff = (es != et) & strip
    diff[base:, :] = False
    rows = np.where(diff.any(1))[0]
    reach = base - rows.min() if rows.size else 0
    return far, ds, dt, reach, es, et


if __name__ == "__main__":
    w = int(sys.argv[1]); H = int(sys.argv[2])
    fhs = [int(x) for x in sys.argv[3].split(',')]
    for fh in fhs:
        far, ds, dt, reach, es, et = run(w, H, 3 * w, fh)
        print(f"w={w} fh={fh:<4} far={''.join(map(str, far))} strip_depth={ds:<4} tee_depth={dt:<4} reach={reach}", flush=True)
