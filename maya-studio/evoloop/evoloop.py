"""Evoloop (Sayama 1999) on a torus, from Golly's Evoloop.rule.

States 0-8 (8 = dissolving). von Neumann, rotate4. The @TABLE is expanded
into a 9^5 lookup (index C,N,E,S,W) and cross-checked against the @TREE.
"""
import itertools
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RULE = os.path.join(HERE, "..", "loops", "Evoloop.rule")
NS = 9


def _sections(path):
    sec, out = None, {}
    for line in open(path):
        line = line.strip()
        if line.startswith("@"):
            sec = line.split()[0]
            out[sec] = []
            continue
        if sec:
            out[sec].append(line)
    return out


def lut_from_table(path=RULE):
    lines = _sections(path)["@TABLE"]
    vars_ = {}
    lut = np.full(NS ** 5, -1, dtype=np.int16)
    for line in lines:
        if not line or line.startswith("#"):
            continue
        if line.startswith("var "):
            name, vals = line[4:].split("=")
            vars_[name.strip()] = [int(v) for v in vals.strip("{} ").split(",")]
            continue
        if ":" in line or "," not in line:
            continue
        toks = [t.strip() for t in line.split(",")]
        names = sorted({t for t in toks[:5] if not t.isdigit()})
        for combo in itertools.product(*[vars_[n] for n in names]):
            bind = dict(zip(names, combo))
            v = [int(t) if t.isdigit() else bind[t] for t in toks[:5]]
            o = toks[5]
            out = int(o) if o.isdigit() else bind[o]
            c, nb = v[0], v[1:]
            for r in range(4):
                rn = nb[r:] + nb[:r]
                idx = (((c * NS + rn[0]) * NS + rn[1]) * NS + rn[2]) * NS + rn[3]
                if lut[idx] < 0:  # first match wins
                    lut[idx] = out
    unmatched = int((lut < 0).sum())
    idx = np.arange(NS ** 5)
    lut[lut < 0] = (idx // NS ** 4)[lut < 0]
    return lut.astype(np.uint8), unmatched


def lut_from_tree(path=RULE):
    lines = [l for l in _sections(path)["@TREE"] if l and l[0].isdigit()]
    nodes = [list(map(int, l.split())) for l in lines]
    root = len(nodes) - 1
    lut = np.zeros(NS ** 5, dtype=np.uint8)
    for c, n, e, s, w in itertools.product(range(NS), repeat=5):
        x = root
        for v in (n, w, e, s, c):  # Golly order for vonNeumann: N W E S C
            node = nodes[x]
            x = node[1 + v]
            if node[0] == 1:
                break
        idx = (((c * NS + n) * NS + e) * NS + s) * NS + w
        lut[idx] = x
    return lut


LUT = None


def get_lut():
    global LUT
    if LUT is None:
        LUT, _ = lut_from_table()
    return LUT


def step(g):
    L = get_lut()
    n = np.roll(g, 1, 0)
    s = np.roll(g, -1, 0)
    w = np.roll(g, 1, 1)
    e = np.roll(g, -1, 1)
    idx = (((g.astype(np.int32) * NS + n) * NS + e) * NS + s) * NS + w
    return L[idx]


def parse_rle(path, bg=0):
    txt = open(path).read()
    lines = [l for l in txt.splitlines() if not l.startswith("#")]
    header = lines[0]
    body = "".join(lines[1:])
    x = int(header.split("x =")[1].split(",")[0])
    y = int(header.split("y =")[1].split(",")[0])
    g = np.full((y, x), bg, dtype=np.uint8)
    r = c = 0
    num = ""
    for ch in body:
        if ch.isdigit():
            num += ch
            continue
        k = int(num) if num else 1
        num = ""
        if ch == "!":
            break
        if ch == "$":
            r += k
            c = 0
            continue
        if ch in ".b":
            val = 0
        elif ch == "o":
            val = 1
        else:
            val = ord(ch) - ord("A") + 1
        g[r, c:c + k] = val
        c += k
    return g


if __name__ == "__main__":
    a, unmatched = lut_from_table()
    b = lut_from_tree()
    print("table entries unmatched (kept state):", unmatched)
    print("table vs tree mismatches:", int((a != b).sum()), "of", NS ** 5)
