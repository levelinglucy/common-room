"""Read a loop's genome tape: the states round its core ring."""


def ring(g, r, c, H):
    a, b = r - 2, r + H + 1
    l, rr = c - 2, c + H + 1
    top = [g[a, j] for j in range(l, rr + 1)]
    right = [g[i, rr] for i in range(a + 1, b + 1)]
    bot = [g[b, j] for j in range(rr - 1, l - 1, -1)]
    left = [g[i, l] for i in range(b - 1, a, -1)]
    return [int(x) for x in top + right + bot + left]


def canon(seq):
    s = "".join(map(str, seq))
    return min(s[i:] + s[:i] for i in range(len(s)))
