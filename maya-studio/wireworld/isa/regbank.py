"""Find and decode the register loops of the Moore/Owen WireWorld computer in primes.npy."""
import numpy as np
from scipy.ndimage import convolve

K = np.ones((3, 3), np.uint8); K[1, 1] = 0

def step(g):
    h = (g == 1).astype(np.uint8)
    n = convolve(h, K, mode='constant')
    out = g.copy()
    out[g == 1] = 2
    out[g == 2] = 3
    c = (g == 3)
    out[c & ((n == 1) | (n == 2))] = 1
    return out

def loops(g):
    """Register loops: top rows with a long second run, bottom row 3 below."""
    regs = []
    for y in range(380, 820):
        r = g[y] > 0; runs = []; x = 0
        while x < len(r):
            if r[x]:
                s = x
                while x < len(r) and r[x]: x += 1
                if x - s >= 20: runs.append((s, x - 1))
            x += 1
        if len(runs) == 2 and runs[1][1] - runs[1][0] >= 40:
            regs.append((y, runs[1]))
    return regs

if __name__ == '__main__':
    g = np.load('../primes.npy')
    regs = loops(g)
    print(len(regs), regs[:3], regs[-3:])
    T = 192
    hist = []
    cur = g
    for t in range(T):
        hist.append(cur == 1)
        cur = step(cur)
    hist = np.array(hist)
    np.save('/tmp/reghist.npy', hist[:, 380:820, :])
    for k, (y, (xs, xe)) in enumerate(regs):
        px = xs + 5
        ts = hist[:96, y, px]
        ph = [t for t in range(96) if ts[t]]
        print(k, y, xs, ''.join('1' if ts[t] else '.' for t in range(96)))
