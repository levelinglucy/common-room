"""
chladni_words.py: words played on a Chladni plate.

Sprinkle sand on a metal plate and draw a violin bow down its edge. The plate
rings at one note, and the sand jumps off the parts that shake and piles up
along the lines that stay still. Ernst Chladni showed these figures around
1787. Change the note and the sand runs into a new figure.

Here every word picks its own note, using the old Pythagorean numerology
(A=1 ... I=9, J=1 ... R=9, S=1 ... Z=8), reduced to a single digit:

  m = the vowels' number      (numerologists call it the soul urge)
  n = the consonants' number  (the personality number)
  the whole word's number     (the expression number) picks the sign:
                              odd adds the two waves, even subtracts them

The plate's shape for that note is the textbook approximation for a square
plate with free edges:

    u(x, y) = cos(n pi x) cos(m pi y)  +/-  cos(m pi x) cos(n pi y)

and the sand obeys one rule: each grain hops a random distance that grows with
how hard the plate shakes under it. Grains on the still lines barely move, so
that's where they gather. Nothing draws the lines. The sand finds them.

The plate's pitch goes up with n^2 + m^2, so every word also has a note.

Usage:
    python3 chladni_words.py                       # gallery + the sentence animation
    python3 chladni_words.py gallery word1 word2   # your own gallery (up to 9 words)
    python3 chladni_words.py play "a whole sentence" # sand dancing word to word
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
VOWELS = set("aeiou")


def value(ch):
    return (ord(ch) - ord("a")) % 9 + 1


def root(s):
    return 0 if s == 0 else 1 + (s - 1) % 9


def word_numbers(word):
    letters = [c for c in word.lower() if c.isalpha()]
    soul = root(sum(value(c) for c in letters if c in VOWELS))
    pers = root(sum(value(c) for c in letters if c not in VOWELS))
    expr = root(sum(value(c) for c in letters))
    return soul, pers, expr


def plate_mode(word):
    """Turn a word into (n, m, sign) for the plate."""
    soul, pers, expr = word_numbers(word)
    m = max(soul, 1)          # a word with no vowels still needs a wave
    n = max(pers, 1)
    sign = 1 if expr % 2 else -1
    if n == m:
        sign = 1              # subtracting a wave from itself leaves a dead plate
    return n, m, sign


def shake(n, m, sign, x, y):
    u = np.cos(n * np.pi * x) * np.cos(m * np.pi * y) \
        + sign * np.cos(m * np.pi * x) * np.cos(n * np.pi * y)
    return np.abs(u) / 2.0    # 0 = still line, 1 = shaking hardest


def settle(px, py, mode, steps, rng, hop=None):
    n, m, s = mode
    if hop is None:
        # bigger hops on slow, wide waves, so every figure settles in about
        # the same number of steps
        hop = 0.12 / max(n, m, 2)
    for _ in range(steps):
        a = shake(n, m, s, px, py)
        step = hop * a + 0.0006
        px += rng.normal(0, 1, px.size) * step
        py += rng.normal(0, 1, py.size) * step
        # grains that bounce off the edge come back in (reflect)
        px = np.abs(px); py = np.abs(py)
        px = 1 - np.abs(1 - px); py = 1 - np.abs(1 - py)
    return px, py


def render(px, py, size, tint=(255, 214, 150)):
    h, _, _ = np.histogram2d(py, px, bins=size, range=[[0, 1], [0, 1]])
    h = h / (np.percentile(h[h > 0], 99) + 1e-9)
    h = np.clip(h, 0, 1) ** 0.6
    plate = np.array([14, 17, 26], float)
    sand = np.array(tint, float)
    img = plate[None, None, :] * (1 - h[..., None]) + sand[None, None, :] * h[..., None]
    return Image.fromarray(img.astype(np.uint8))


def relative_pitch(mode):
    """Semitones above the plate's lowest possible note, (1,2)."""
    n, m, _ = mode
    return 12 * math.log2((n * n + m * m) / 5)


def figure_key(mode):
    """Two words draw the same figure when this matches. Swapping n and m
    only flips the wave upside down, and sand can't tell up from down."""
    n, m, s = mode
    return (min(n, m), max(n, m), s)


def all_figures():
    return {figure_key((n, m, s if n != m else 1))
            for n in range(1, 10) for m in range(1, 10) for s in (1, -1)}


def twins(words):
    groups = {}
    for w in words:
        groups.setdefault(figure_key(plate_mode(w)), []).append(w)
    return groups


def gallery(words, path, grains=90000, steps=250, seed=7):
    """One tile per figure. Words that draw the same figure share a tile."""
    rng = np.random.default_rng(seed)
    groups = list(twins(words).values())
    tile, pad, label = 300, 18, 54
    cols = 3
    rows = math.ceil(len(groups) / cols)
    W = cols * tile + (cols + 1) * pad
    H = rows * (tile + label) + (rows + 1) * pad
    canvas = Image.new("RGB", (W, H), (6, 7, 11))
    draw = ImageDraw.Draw(canvas)
    big = ImageFont.load_default(size=20)
    small = ImageFont.load_default(size=14)
    report = []
    for i, group in enumerate(groups):
        w = group[0]
        mode = plate_mode(w)
        px, py = rng.random(grains), rng.random(grains)
        px, py = settle(px, py, mode, steps, rng)
        r, c = divmod(i, cols)
        x0 = pad + c * (tile + pad)
        y0 = pad + r * (tile + label + pad)
        canvas.paste(render(px, py, tile), (x0, y0))
        soul, pers, expr = word_numbers(w)
        sign = "+" if mode[2] > 0 else "-"
        draw.text((x0, y0 + tile + 6), " = ".join(group), fill=(235, 225, 205), font=big)
        lo, hi, _ = figure_key(mode)
        draw.text((x0, y0 + tile + 32), f"plate {lo}, {hi}  ({sign})",
                  fill=(140, 150, 170), font=small)
        for g in group:
            report.append((g, *word_numbers(g), mode, relative_pitch(mode)))
    canvas.save(path)
    return report


def play(sentence, path, grains=60000, size=420, steps_per_word=70, hold=12, seed=3):
    """The sand dances from each word's figure to the next."""
    rng = np.random.default_rng(seed)
    words = [w for w in sentence.split() if any(c.isalpha() for c in w)]
    px, py = rng.random(grains), rng.random(grains)
    font = ImageFont.load_default(size=26)
    small = ImageFont.load_default(size=15)
    frames = []

    def frame(word, mode):
        im = render(px, py, size)
        band = Image.new("RGB", (size, 64), (6, 7, 11))
        d = ImageDraw.Draw(band)
        d.text((14, 6), word, fill=(235, 225, 205), font=font)
        n, m, s = mode
        d.text((14, 40), f"n={n}  m={m}  {'+' if s > 0 else '-'}", fill=(140, 150, 170), font=small)
        full = Image.new("RGB", (size, size + 64))
        full.paste(im, (0, 0)); full.paste(band, (0, size))
        return full

    # start as a fresh scatter of sand
    for _ in range(6):
        frames.append(frame("", (0, 0, 1)))
    for w in words:
        mode = plate_mode(w)
        for _ in range(steps_per_word // 5):
            px, py = settle(px, py, mode, 5, rng)
            frames.append(frame(w, mode))
        for _ in range(hold):
            frames.append(frames[-1])
    frames[0].save(path, save_all=True, append_images=frames[1:],
                   duration=70, loop=0, optimize=True)
    return words, len(frames)


GALLERY = ["spiral", "emergence", "wall",
           "mycelium", "numbers",
           "pattern", "crayon",
           "recursion", "lines",
           "maya", "echo",
           "chladni", "the",
           "autonomy", "finds",
           "velisara",
           "still"]
SENTENCE = "the sand finds the still lines"


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "gallery":
        rep = gallery(args[1:10] or GALLERY, OUT / "chladni_gallery_custom.png")
    elif args and args[0] == "play":
        print(play(" ".join(args[1:]) or SENTENCE, OUT / "chladni_play_custom.gif"))
        rep = []
    else:
        rep = gallery(GALLERY, OUT / "chladni_gallery.png")
        print(play(SENTENCE, OUT / "chladni_play.gif"))
    for w, soul, pers, expr, mode, pitch in rep:
        print(f"{w:10s} soul {soul} pers {pers} expr {expr} -> n={mode[0]} m={mode[1]} "
              f"sign {mode[2]:+d}  pitch +{pitch:.1f} semitones")
