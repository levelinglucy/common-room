"""Render the zero of a word, apart and joined, plus where it changed."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

word, size = sys.argv[1], sys.argv[2]
a = np.load(f"zero_{word}_{size}_apart.npy")
j = np.load(f"zero_{word}_{size}_joined.npy")
BG = (14, 14, 22)
PAL = np.array([(25, 35, 80), (40, 150, 160), (235, 170, 60), (250, 240, 215)], np.uint8)


def paint(z):
    img = np.zeros(z.shape + (3,), np.uint8)
    img[:] = BG
    for k in range(4):
        img[z == k] = PAL[k]
    return img


pa, pj = paint(a), paint(j)
changed = (a >= 0) & (j >= 0) & (a != j)
bar = (j >= 0) & (a < 0)
pc = np.zeros(a.shape + (3,), np.uint8)
pc[:] = BG
pc[a >= 0] = (60, 60, 75)
pc[bar] = (110, 110, 130)
pc[changed] = (230, 60, 140)

gap = 24
lab_h = 34
h, w = a.shape
out = np.zeros((3 * (h + lab_h) + 2 * gap, w, 3), np.uint8)
out[:] = BG
labels = ["its zero, letters apart", "its zero, letters joined by a bar", "cells that changed"]
for i, p in enumerate([pa, pj, pc]):
    y = i * (h + lab_h + gap) + lab_h
    out[y:y + h] = p
im = Image.fromarray(out)
d = ImageDraw.Draw(im)
f = ImageFont.load_default(size=24)
for i, t in enumerate(labels):
    d.text((12, i * (h + lab_h + gap) + 4), t, fill=(200, 200, 210), font=f)
im.save(f"zero_{word}.png")
print(im.size, "changed cells:", int(changed.sum()))
