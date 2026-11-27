"""Two forests on the same perches, same coupling, side by side:
left listens to its 7 nearest, right to the nearest in each of six directions.
Each firefly glows when it flashes and fades over ~0.1 period."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from firefly import perches, run, beats

sd = int(sys.argv[1]) if len(sys.argv) > 1 else 0
eps = 0.03
P = 200
n = 400
show_from, show_len, fstep = P - 4.0, 4.0, 0.02
pos = perches(n, 100 + sd)
panels = []
for rule, title in [("count", "7 nearest"), ("sectors", "nearest in each of 6 directions")]:
    ft, _, _ = run(pos, rule, 7 if rule == "count" else 0, eps=eps, seed=sd, periods=P)
    r, _, _ = beats(ft, periods=P)
    print(rule, f"r={r:.2f}")
    panels.append(([np.array(f) for f in ft], title))

W, PAD, TOP = 420, 20, 40
img_w = 2 * W + 3 * PAD
img_h = W + TOP + PAD
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except OSError:
    font = ImageFont.load_default()
frames = []
ts = np.arange(show_from, show_from + show_len, fstep)
for t in ts:
    im = Image.new("RGB", (img_w, img_h), (6, 10, 18))
    d = ImageDraw.Draw(im)
    for k, (ft, title) in enumerate(panels):
        x0 = PAD + k * (W + PAD)
        d.rectangle([x0, TOP, x0 + W, TOP + W], fill=(10, 18, 26))
        d.text((x0 + 6, 12), title, fill=(200, 210, 190), font=font)
        for i in range(n):
            past = ft[i][ft[i] <= t + 1e-9]
            age = t - past[-1] if len(past) else 9.0
            g = np.exp(-age / 0.06)
            cx = x0 + 10 + pos[i, 0] * (W - 20)
            cy = TOP + 10 + pos[i, 1] * (W - 20)
            col = (int(40 + 215 * g), int(50 + 205 * g), int(30 + 60 * g))
            rad = 2 + 3 * g
            if g > 0.3:
                halo = (int(30 + 90 * g), int(40 + 90 * g), int(20 + 20 * g))
                d.ellipse([cx - rad - 4, cy - rad - 4, cx + rad + 4, cy + rad + 4], fill=halo)
            d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=col)
    frames.append(im)
out = f"forest_waves_vs_unison_s{sd}.gif"
frames[0].save(out, save_all=True, append_images=frames[1:], duration=50, loop=0, optimize=True)
print("saved", out, len(frames), "frames")
