"""Show the plateau of a tie-family trip: per diagonal, which cells are filled.
usage: python3 plateau.py N K 'p1,p2,...'
Diagonal t has t+1 cells, cell (i, j) with i + j = t; we print each diagonal from
row 0 (the newest pile) downwards as a string of # and . .
"""
import sys
sys.path.insert(0, '/home/sprite/maya-studio/solitaire')
from bulgarian import move
from tie_trace import energy


def diagonals(p, tmax):
    rows = []
    for t in range(tmax + 1):
        s = ''
        for i in range(t + 1):
            j = t - i
            s += '#' if i < len(p) and p[i] > j else '.'
        rows.append(s)
    return rows


def main():
    n, k = int(sys.argv[1]), int(sys.argv[2])
    p = tuple(int(x) for x in sys.argv[3].split(','))
    r = n - k * (k + 1) // 2
    Emin = sum(t * (t + 1) for t in range(k)) + r * k
    seen = {}
    step = 0
    while p not in seen:
        seen[p] = step
        dg = diagonals(p, k + 2)
        print(f'{step:3d} E+{energy(p)-Emin:<3d} {str(p):28s} d{k-1}:{dg[k-1]}  d{k}:{dg[k]}  d{k+1}:{dg[k+1]}  d{k+2}:{dg[k+2]}')
        p = move(p)
        step += 1
    print('cycle re-entered at step', seen[p])


if __name__ == '__main__':
    main()
