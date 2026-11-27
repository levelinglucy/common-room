"""One beat off: a ring puzzle.

Each ring has 26 seats (seat 1 at the top, counting clockwise).
The beats on a ring are a maximally even rhythm E(k, 26), rotated,
except that ONE drummer has slipped one seat. The seat the stray
drummer now sits on is a letter (1 = A ... 26 = Z).

This script picks, for each letter, a k, a rotation and a slip
direction such that the stray drummer is the ONLY drummer whose
one-seat move (either way) restores a maximally even ring.
"""
import json
import random

N = 26


def euclid(k, n):
    # Bresenham form: beat at seats floor(i*n/k)
    return sorted({(i * n) // k for i in range(k)})


def rotations(k, n):
    base = euclid(k, n)
    return {frozenset((b + r) % n for b in base) for r in range(n)}


def restorers(beats, k, n, rots):
    """All (seat, direction) whose one-seat move gives a maximally even ring."""
    s = set(beats)
    out = []
    for b in beats:
        for d in (-1, 1):
            t = (b + d) % n
            if t in s:
                continue
            new = frozenset((s - {b}) | {t})
            if new in rots:
                out.append((b, d))
    return out


def make_ring(letter_seat, k, rng, n=N):
    """letter_seat is 0-based seat index of the stray drummer."""
    rots = list(rotations(k, n))
    rng.shuffle(rots)
    rset = set(rots)
    for rot in rots:
        for d in (-1, 1):
            home = (letter_seat - d) % n  # stray came from home
            if home not in rot or letter_seat in rot:
                continue
            beats = sorted((set(rot) - {home}) | {letter_seat})
            if frozenset(beats) in rset:
                continue  # still even: no visible slip
            fixes = restorers(beats, k, n, rset)
            if len(fixes) == 1 and fixes[0][0] == letter_seat:
                return beats
    return None


def build(message, ks, seed=8):
    rng = random.Random(seed)
    rings = []
    for ch, k in zip(message, ks):
        seat = ord(ch) - ord('A')
        beats = make_ring(seat, k, rng)
        if beats is None:
            raise SystemExit(f'no unique ring for {ch} with k={k}')
        rings.append({'letter': ch, 'k': k, 'beats': beats})
    return rings


def solve(rings, n=N):
    """Independent solver: uses only the beats."""
    out = []
    for r in rings:
        k = len(r['beats'])
        fixes = restorers(r['beats'], k, n, rotations(k, n))
        if len(fixes) != 1:
            out.append('?')
        else:
            out.append(chr(ord('A') + fixes[0][0]))
    return ''.join(out)


if __name__ == '__main__':
    import sys
    message = 'ONEBEATOFF'
    ks = [7, 9, 11, 8, 10, 7, 12, 9, 11, 8]
    rings = build(message, ks)
    got = solve(rings)
    print('message ', message)
    print('solved  ', got)
    for r in rings:
        print(r['letter'], r['k'], [b + 1 for b in r['beats']])
    assert got == message
    json.dump(rings, open('/home/sprite/maya-studio/puzzle/one_beat_off.json', 'w'))
