"""Read and write registers R1..R52 of the WireWorld computer directly in the copper (gen 0).

Register R(k+1), k=0..51: loop with top row y=411+6k, top-run start xs=487-6k, probe
cell (y, xs+5).  Electrons on the top row move left.  At gen 0, bit i is set iff a
head reaches the probe at t = 1 + 6*((k+14+i) % 16).
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from regbank import step

HERE = os.path.dirname(os.path.abspath(__file__))
G0 = os.path.join(HERE, '..', 'primes.npy')

def geom(R):
    k = R - 1
    return k, 411 + 6 * k, 487 - 6 * k

def slot(R, i):
    k = R - 1
    return 1 + 6 * ((k + 14 + i) % 16)

def build_shiftmap(g, R=2, T=192):
    """Loop cells of register R as offsets from its probe, ordered by upstream distance s."""
    k, y, xs = geom(R)
    py, px = y, xs + 5
    y0, y1, x0, x1 = y - 2, y + 5, xs - 4, xs + 52
    hist = []
    cur = g
    for t in range(T):
        hist.append(cur[y0:y1 + 1, x0:x1 + 1] == 1)
        cur = step(cur)
    hist = np.array(hist)[:96]
    probe = hist[:, py - y0, px - x0]
    assert probe.sum() > 0
    S = {}
    for a in range(hist.shape[1]):
        for b in range(hist.shape[2]):
            ser = hist[:, a, b]
            if ser.sum() != probe.sum(): continue
            ss = [s for s in range(96) if np.array_equal(ser, np.roll(probe, -s))]
            off = (a + y0 - py, b + x0 - px)
            common = all(g[geom(Q)[1] + off[0], geom(Q)[2] + 5 + off[1]] > 0 for Q in range(1, 53))
            if len(ss) == 1 and common: S[off] = ss[0]
    # walk upstream from the probe
    def walk(order):
        s = len(order)
        cy, cx = order[-1]
        if s == 96:
            return order if max(abs(cy), abs(cx)) == 1 else None
        for c in [c for c, v in S.items() if v == s and max(abs(c[0] - cy), abs(c[1] - cx)) == 1]:
            r = walk(order + [c])
            if r: return r
        return None
    order = walk([(0, 0)])
    assert order, 'loop does not close'
    return order   # order[s] = offset of the cell s steps upstream of the probe

def read_reg(g, R, order, gen=0):
    k, y, xs = geom(R)
    py, px = y, xs + 5
    v = 0
    for i in range(16):
        dy, dx = order[(slot(R, i) - gen) % 96]
        if g[py + dy, px + dx] == 1: v |= 1 << i
    return v

def write_reg(g, R, value, order):
    k, y, xs = geom(R)
    py, px = y, xs + 5
    for s in range(96):
        dy, dx = order[s]
        g[py + dy, px + dx] = 3
    for i in range(16):
        if value >> i & 1:
            t = slot(R, i)
            dy, dx = order[t]; g[py + dy, px + dx] = 1
            dy, dx = order[t + 1]; g[py + dy, px + dx] = 2
    return g

if __name__ == '__main__':
    from wwcpu import PRIMES_HEX
    g = np.load(G0)
    order = build_shiftmap(g)
    np.save(os.path.join(HERE, 'loop_order.npy'), np.array(order))
    bad = []
    for R in range(1, 53):
        v = read_reg(g, R, order)
        want = PRIMES_HEX.get(R, 0)
        if v != want: bad.append((R, hex(v), hex(want)))
    print('registers R1..R52 read from copper; mismatches with the listing:', bad)
    # round trip
    g2 = g.copy()
    for R in range(1, 53): write_reg(g2, R, read_reg(g, R, order), order)
    print('rewrite identical:', np.array_equal(g, g2), int((g != g2).sum()))
