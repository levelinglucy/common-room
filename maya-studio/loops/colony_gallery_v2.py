"""Colonies of matched loops (s = L-2) side by side, same number of steps."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from build_loop import build, genome_of
from langton import step, place

import os
ARM = int(os.environ.get("ARM", "0"))
PAL = np.array([
    (12, 12, 20),     # 0 empty
    (70, 110, 220),   # 1 core
    (230, 60, 60),    # 2 sheath
    (60, 200, 90),    # 3
    (240, 220, 60),   # 4 turn
    (230, 80, 230),   # 5
    (240, 240, 240),  # 6
    (60, 220, 230),   # 7 straight
], dtype=np.uint8)


def colony(L, T, N=520):
    g = place(build(L, genome_of(L - 2, 2, L), ARM if ARM else max(L - 3, 1)), N)
    for _ in range(T):
        g = step(g)
    return g


def crop(g, size):
    ys, xs = np.nonzero(g)
    cy, cx = int(np.median(ys)), int(np.median(xs))
    h = size // 2
    return np.roll(np.roll(g, h - cy, 0), h - cx, 1)[:size, :size]


if __name__ == "__main__":
    Ls = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [8, 9, 10, 11, 12, 14]
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    size, scale = 300, 2
    tiles = []
    for L in Ls:
        g = crop(colony(L, T), size)
        im = Image.fromarray(PAL[g]).resize((size * scale, size * scale), Image.NEAREST)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 170 if L % 3 == 0 else 70, 26], fill=(0, 0, 0))
        d.text((8, 7), f"side {L}" + ("  (divisible by 3)" if L % 3 == 0 else ""), fill=(255, 255, 255))
        tiles.append(im)
    cols = 3
    rows = (len(tiles) + cols - 1) // cols
    W = size * scale
    out = Image.new("RGB", (cols * W + (cols - 1) * 6, rows * W + (rows - 1) * 6), (40, 40, 40))
    for i, im in enumerate(tiles):
        out.paste(im, ((i % cols) * (W + 6), (i // cols) * (W + 6)))
    name = sys.argv[3] if len(sys.argv) > 3 else "colony_gallery.png"
    out.save(name)
    print("saved", name, out.size)
