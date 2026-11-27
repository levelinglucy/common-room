"""Steps for every 4-digit string 0000..9999 to reach 6174 (base 10).
Row = first two digits, column = last two. Repdigits (fall to 0000) marked separately."""
import numpy as np
from kaprekar import K

steps = np.full(10000, -1)
for n in range(10000):
    m, s = n, 0
    while m != 6174 and s < 20:
        if m == 0:
            s = -1
            break
        m = K(m, 10, 4)
        s += 1
    steps[n] = s if m == 6174 else -1
grid = steps.reshape(100, 100)
np.save('steps_6174.npy', grid)
vals, cnt = np.unique(steps, return_counts=True)
for v, c in zip(vals, cnt):
    print(v, c)
# symmetry: does the picture have the 8 permutation-invariances? count distinct multisets per step
from collections import Counter
ms = Counter()
for n in range(10000):
    ms[(tuple(sorted(f'{n:04d}')), steps[n])] += 1
by = Counter(s for (_, s) in ms)
print('distinct digit-multisets per step:', sorted(by.items()))
