"""Why 4-digit Kaprekar is unique only at B = 5*2^m with m = 0 or odd.

Exact gap map on (x, y) = (e1, e2), digits of K derived in closed form:
  y >= 1: K digits {x, B-x, y-1, B-1-y}
  y == 0: K digits {x-1, B-1, B-1, B-x}
Away from 'collisions' this is the tent map t(z) = |2z - B| on each gap, then sorted.
The fixed point is the tent 2-cycle B/5 <-> 3B/5.

Prediction: the escape orbit started from the edge state (B/5, 0) or (2B/5, 0)
carries a deviation that doubles every step; it closes into a rival cycle exactly
when the deviation reaches 2^m = B/5 on a B/5-step, i.e. when m is even.
"""
import sys


def K(x, y, B):
    if y >= 1:
        d = [x, B - x, y - 1, B - 1 - y]
    else:
        d = [x - 1, B - 1, B - 1, B - x]
    d.sort()
    return d[3] - d[0], d[2] - d[1]


def kaprekar_direct(x, y, B):
    # check against the literal routine on a number with those gaps: digits x,y,0,0 sorted -> a=x, b=y, c=0, d=0
    digs = sorted([x, y, 0, 0], reverse=True)
    hi = sum(dg * B ** (3 - i) for i, dg in enumerate(digs))
    lo = sum(dg * B ** i for i, dg in enumerate(digs))
    n = hi - lo
    dd = sorted([(n // B ** k) % B for k in range(4)])
    return dd[3] - dd[0], dd[2] - dd[1]


def orbit(s, B, maxlen=10000):
    seen = {}
    path = []
    while s not in seen:
        seen[s] = len(path)
        path.append(s)
        s = K(*s, B)
        if len(path) > maxlen:
            return path, None
    i = seen[s]
    return path[:i], path[i:]


if __name__ == '__main__':
    # sanity: closed form vs literal routine
    import random
    for B in [5, 10, 20, 37, 80, 1280]:
        for _ in range(2000):
            x = random.randint(1, B - 1)
            y = random.randint(0, x)
            assert K(x, y, B) == kaprekar_direct(x, y, B), (B, x, y)
    print('closed form matches literal routine')
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    for m in range(0, M + 1):
        B = 5 * 2 ** m
        fp = (3 * B // 5, B // 5)
        res = []
        for start in [(B // 5, 0), (2 * B // 5, 0)]:
            tail, cyc = orbit(start, B)
            if cyc == [fp]:
                res.append(f'-> fixed point after {len(tail)}')
            else:
                res.append(f'RIVAL cycle len {len(cyc)} (tail {len(tail)})')
        print(f'm={m:2d} B={B:>9d}  from (B/5,0): {res[0]:32s} from (2B/5,0): {res[1]}')
