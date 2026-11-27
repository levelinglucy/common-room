# Check: Kaprekar 4-digit step K(N) = max - min  equals (1089*S + 729*m)/4, where
# S = sum of the six pairwise |digit differences| and m = the smallest of the three
# pairing sums |p-q|+|r-s|.   Exhaustive over 0000..9999.
from itertools import combinations
bad = 0
for N in range(10000):
    d = [int(c) for c in f'{N:04d}']
    s = sorted(d, reverse=True)
    K = int(''.join(map(str, s))) - int(''.join(map(str, s[::-1])))
    S = sum(abs(a - b) for a, b in combinations(d, 2))
    p, q, r, t = d
    m = min(abs(p-q)+abs(r-t), abs(p-r)+abs(q-t), abs(p-t)+abs(q-r))
    if 4 * K != 1089 * S + 729 * m: bad += 1
print('mismatches', bad, 'of 10000')
# 3-digit: K = 99*(max-min) = 99*(|a-b|+|b-c|+|a-c|)/2
bad3 = 0
for N in range(1000):
    a, b, c = [int(x) for x in f'{N:03d}']
    s = sorted([a, b, c], reverse=True)
    K = int(''.join(map(str, s))) - int(''.join(map(str, s[::-1])))
    if 2 * K != 99 * (abs(a-b)+abs(b-c)+abs(a-c)): bad3 += 1
print('3-digit mismatches', bad3, 'of 1000')
