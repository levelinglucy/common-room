"""Independent check of obstacle2.c results with a plain Python ant (dict ground, no grid edges).
usage: python3 verify_obstacle.py T1 idx [idx ...]
  idx = cell index in first-visit order among cells first visited in [T1, T1+312)
Runs the clean ant and the dotted ant to T_END, then reports the final 104-step displacement and,
for a (-2,2) road, the smallest lag L such that the last 3000 positions equal the clean ones shifted
by L steps (positive L: behind the clean ant; negative: ahead).
"""
import sys

DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)


def run(T, dots=()):
    g = set(dots)
    x = y = d = 0
    xs = [0] * (T + 1)
    ys = [0] * (T + 1)
    first = {}
    for t in range(T + 1):
        xs[t] = x
        ys[t] = y
        if (x, y) not in first:
            first[(x, y)] = t
        if (x, y) in g:
            d = (d + 3) & 3
            g.discard((x, y))
        else:
            d = (d + 1) & 3
            g.add((x, y))
        x += DX[d]
        y += DY[d]
    return xs, ys, first


def main():
    T1 = int(sys.argv[1])
    idxs = [int(a) for a in sys.argv[2:]]
    T_END = T1 + 200000
    cxs, cys, first = run(T_END)
    cells = sorted((t, c) for c, t in first.items() if T1 <= t < T1 + 312)
    dots = [cells[i][1] for i in idxs]
    print('dots', dots, 'first visits', [cells[i][0] for i in idxs])
    xs, ys, _ = run(T_END, dots)
    ex, ey = xs[-1] - xs[-105], ys[-1] - ys[-105]
    print('final 104-step displacement', (ex, ey))
    if (ex, ey) == (-2, 2):
        W = 3000
        tail = list(zip(xs[-W:], ys[-W:]))
        # find L with xs[t] == cxs[t-L] for the tail
        for L in range(-2000, 2001):
            a = T_END - W + 1 - L
            if a < 0 or a + W > len(cxs):
                continue
            if tail[0] == (cxs[a], cys[a]) and tail == list(zip(cxs[a:a + W], cys[a:a + W])):
                print('matches clean road exactly, lag', L)
                break
        else:
            # same road shape but moved: look for a phase L (0..103) and a translation (tx, ty)
            a0 = T_END - W + 1
            for L in range(104):
                a = a0 - L
                tx, ty = tail[0][0] - cxs[a], tail[0][1] - cys[a]
                if all(tail[k] == (cxs[a + k] + tx, cys[a + k] + ty) for k in range(W)):
                    print('same road shape, moved by', (tx, ty), 'at phase lag', L)
                    break
            mn = min(x + y for x, y in tail[-104:])
            cmn = min(cxs[t] + cys[t] for t in range(T_END - 103, T_END + 1))
            print('same direction, not the clean road; sideways shift', mn - cmn)


if __name__ == '__main__':
    main()
