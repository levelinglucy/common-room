"""Two-clock check (18 Nov, 6:40 PM).
usage: python3 clocks.py NMIN NMAX

Claim to test: during a one-card-one-hole plateau, the state is just three rings turning
rigidly (d_{k-1}: k seats, d_k: k+1, d_{k+1}: k+2; seat i -> i+1, last seat -> 0), and
the plateau ends at the first moment one of two clocks runs out:
  card clock: the card on d_{k+1} seat c needs d_k seats c-1 and c filled (edge seats need one);
  hole clock: the hole on d_{k-1} seat h needs d_k seats h and h+1 empty.
For every start whose trip ends in such a plateau, compare the real trip with the rigid
rotation, compute both clock times from the plateau's first state, and record which clock
ends it. Also: max card clock should be (k+2)(r-1)+2, max hole clock k(k-r).
"""
import sys
from collections import Counter
sys.path.insert(0, '/home/sprite/maya-studio/solitaire')
from tie_trace import depth_all
from vernier import tri_k, vernier_state, diag_cells


def seats(p, t):
    return frozenset(diag_cells(p, t))


def rot(S, t, s=1):
    return frozenset((i + s) % (t + 1) for i in S)


def card_ok(c, D, k):
    need = []
    if c <= k:
        need.append(c)
    if c >= 1:
        need.append(c - 1)
    return all(x in D for x in need)


def hole_ok(h, D):
    return h not in D and (h + 1) not in D


def clock_times(h, c, D, k, cap):
    """number of consecutive rigid-rotation states (from s = 0) where each condition holds."""
    tc = th = None
    for s in range(cap):
        hs = (h + s) % k
        cs = (c + s) % (k + 2)
        Ds = rot(D, k, s)
        if tc is None and not card_ok(cs, Ds, k):
            tc = s
        if th is None and not hole_ok(hs, Ds):
            th = s
        if tc is not None and th is not None:
            break
    return tc, th


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for n in range(a, b + 1):
        k, r = tri_k(n)
        if k < 3 or r == 0:
            continue
        d, nxt, oc = depth_all(n)
        cap = 4 * (k + 2) * (k + 1)
        runs = 0
        rigid_bad = 0
        ender = Counter()
        len_bad = 0
        maxc = maxh = 0
        longest = 0
        for p in d:
            if p in oc:
                continue
            x = p
            run = []
            while x not in oc:
                v = vernier_state(x, k)
                run = [] if v is None else run + [(v, seats(x, k))]
                x = nxt[x]
            if not run:
                continue
            # only count each plateau once: from its first state (p itself is the start
            # only if the plateau began at p; dedupe by first state)
            runs += 1
            (h0, c0), D0 = run[0]
            for s, ((h, c), D) in enumerate(run):
                if h != (h0 + s) % k or c != (c0 + s) % (k + 2) or D != rot(D0, k, s):
                    rigid_bad += 1
                    break
            tc, th = clock_times(h0, c0, D0, k, cap)
            L = len(run)
            maxc = max(maxc, tc)
            maxh = max(maxh, th)
            longest = max(longest, L)
            if L != min(tc, th):
                len_bad += 1
            ender['card' if tc < th else 'hole' if th < tc else 'both'] += 1
        fc, fh = (k + 2) * (r - 1) + 2, k * (k - r)
        print(f'n={n} k={r and k} r={r} runs={runs} rigid_bad={rigid_bad} len!=min(clocks)={len_bad} '
              f'ended_by={dict(ender)} max_card={maxc} (pred {fc}) max_hole={maxh} (pred {fh}) '
              f'longest={longest} (pred {min(fc, fh)})')
        sys.stdout.flush()


if __name__ == '__main__':
    main()
