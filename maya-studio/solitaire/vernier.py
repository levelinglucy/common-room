"""The 'vernier' check: every trip whose last phase is one card too high (diagonal k+1)
and one hole too low (diagonal k-1), with diagonal k otherwise in place.
usage: python3 vernier.py NMIN NMAX
For each n: how many starts end that way; longest such plateau; whether every drop
happens exactly when the hole is at the bottom seat (index k-1) and the card at the
top seat (index 0); the card's seat at each lap of the hole (gap closes by 2?).
"""
import sys
sys.path.insert(0, '/home/sprite/maya-studio/solitaire')
from tie_trace import depth_all, energy


def tri_k(n):
    k = 0
    while (k + 1) * (k + 2) // 2 <= n:
        k += 1
    return k, n - k * (k + 1) // 2


def diag_cells(p, t):
    return [i for i in range(t + 1) if i < len(p) and p[i] > t - i]


def vernier_state(p, k):
    """(hole index on d_{k-1}, card index on d_{k+1}) if p is one-card-one-hole, else None."""
    if len(p) > k + 2 or (p and p[0] > k + 2):
        return None
    lo = diag_cells(p, k - 1)
    hi = diag_cells(p, k + 1)
    if len(lo) != k - 1 or len(hi) != 1:
        return None
    for t in range(k - 1):
        if len(diag_cells(p, t)) != t + 1:
            return None
    if len(diag_cells(p, k + 2)) != 0:
        return None
    hole = [i for i in range(k) if i not in lo][0]
    return hole, hi[0]


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for n in range(a, b + 1):
        k, r = tri_k(n)
        if k < 3:
            continue
        d, nxt, oc = depth_all(n)
        M = max(d.values())
        count = 0
        longest = 0
        longest_start = None
        bad_meet = 0
        bad_gap = 0
        deep_vern = 0
        for p in d:
            if p in oc:
                continue
            # walk to the cycle, keep the last run of vernier states before it
            x = p
            run = []
            while x not in oc:
                v = vernier_state(x, k)
                if v is None:
                    run = []
                else:
                    run.append(v)
                x = nxt[x]
            if not run or nxt_is_not_last(run):
                pass
            if run:
                # run must end right before the cycle
                count += 1
                if run[-1] != (k - 1, 0):
                    bad_meet += 1
                # card seat each time the hole is at the bottom seat
                laps = [c for (h, c) in run if h == k - 1]
                for u, w in zip(laps, laps[1:]):
                    if (u - w) % (k + 2) != 2:
                        bad_gap += 1
                if len(run) > longest:
                    longest = len(run)
                    longest_start = p
                if d[p] == M:
                    deep_vern += 1
        print(f'n={n} k={k} r={r} maxT={M} vernier-ending starts={count} longest plateau={longest} '
              f'(start {longest_start if longest_start and len(longest_start) < 18 else "..."}) '
              f'deepest that end this way={deep_vern} bad_meet={bad_meet} bad_gap={bad_gap}')
        sys.stdout.flush()


def nxt_is_not_last(run):
    return False


if __name__ == '__main__':
    main()
