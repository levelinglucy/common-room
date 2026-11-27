"""The zero of a shape: the identity element of the abelian sandpile group.

Cells inside a mask hold grains; a cell with 4 or more topples, sending one
grain to each of its four neighbours. Grains that leave the mask are lost
(the sink). The recurrent stable piles form a group under "add, then
stabilise", and its identity is

    e = S(6 - S(6))

where 6 means six grains on every cell and S is stabilisation.
"""
import sys
import numpy as np


def stabilise(z, mask, max_iter=10_000_000):
    z = z.copy()
    m = mask.astype(np.int64)
    it = 0
    topples = 0
    while True:
        t = z >> 2  # floor(z/4); z >= 0 always
        if not t.any():
            break
        topples += int(t.sum())
        z -= 4 * t
        p = np.zeros((z.shape[0] + 2, z.shape[1] + 2), dtype=z.dtype)
        p[1:-1, 1:-1] = 0
        give = np.zeros_like(z)
        give[1:, :] += t[:-1, :]
        give[:-1, :] += t[1:, :]
        give[:, 1:] += t[:, :-1]
        give[:, :-1] += t[:, 1:]
        z += give * m
        it += 1
        if it > max_iter:
            raise RuntimeError("did not settle")
    return z, it, topples


def identity(mask):
    six = np.where(mask, 6, 0).astype(np.int64)
    s6, _, _ = stabilise(six, mask)
    e, it, top = stabilise(np.where(mask, six - s6, 0), mask)
    return e


def add(a, b, mask):
    return stabilise(np.where(mask, a + b, 0), mask)[0]


if __name__ == "__main__":
    import time
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    mask = np.ones((n, n), bool)
    t0 = time.time()
    e = identity(mask)
    dt = time.time() - t0
    # check: e + e = e, and e + random recurrent = itself
    ok = np.array_equal(add(e, e, mask), e)
    rng = np.random.default_rng(0)
    r = add(np.where(mask, 3, 0), np.where(mask, rng.integers(0, 4, mask.shape), 0), mask)
    ok2 = np.array_equal(add(r, e, mask), r)
    print(f"n={n} time={dt:.1f}s e+e=e:{ok} r+e=r:{ok2} counts={np.bincount(e[mask], minlength=4)}")
