"""Zeros of words: sandpile identity on letter-shaped domains.

usage: python3 word_zero.py WORD [size] [thicken]
Writes zero_<word>_apart.npy / _joined.npy and prints how much each letter's
zero changes when the letters are joined by a bar underneath.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from sandpile_zero import identity


def word_mask(word, size=160, thicken=4, pad=12):
    font = ImageFont.load_default(size=size)
    l, t, r, b = font.getbbox(word)
    W, H = r - l + 2 * pad, b - t + 2 * pad
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).text((pad - l, pad - t), word, fill=255, font=font)
    m = np.array(im) > 127
    if thicken:
        m = ndimage.binary_dilation(m, iterations=thicken)
    return m


def with_bar(mask, height=None):
    rows = np.where(mask.any(1))[0]
    cols = np.where(mask.any(0))[0]
    h = height or max(6, (rows[-1] - rows[0]) // 10)
    m = mask.copy()
    # bar overlapping the bottom of the letters (baseline region)
    base = rows[-1]
    # find the baseline: lowest row reached by most columns' ink
    bottoms = [np.where(mask[:, c])[0][-1] for c in cols if mask[:, c].any()]
    base = int(np.median(bottoms))
    m[base - h // 2: base + h - h // 2, cols[0]:cols[-1] + 1] = True
    return m


if __name__ == "__main__":
    word = sys.argv[1]
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 160
    thick = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    m = word_mask(word, size, thick)
    mj = with_bar(m)
    lab, n = ndimage.label(m)
    _, nj = ndimage.label(mj)
    ea = identity(m)
    ej = identity(mj)
    np.save(f"zero_{word}_apart.npy", np.where(m, ea, -1))
    np.save(f"zero_{word}_joined.npy", np.where(mj, ej, -1))
    print(f"{word}: {m.sum()} cells, {n} pieces apart, {nj} joined; bar adds {mj.sum()-m.sum()} cells")
    # how much of each original piece changed (on its own cells)
    order = np.argsort([np.where(lab == k)[1].mean() for k in range(1, n + 1)])
    for k in order + 1:
        cell = lab == k
        # only compare cells away from the bar
        far = cell & ~ndimage.binary_dilation(mj & ~m, iterations=3)
        ch = (ea[far] != ej[far]).mean() if far.any() else float('nan')
        print(f"  piece {k}: {cell.sum()} cells, changed {100*ch:.1f}% (cells off the bar)")
    print("  grains apart:", np.bincount(ea[m], minlength=4), "joined:", np.bincount(ej[mj], minlength=4))
