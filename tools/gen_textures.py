#!/usr/bin/env python3
"""TextUI's metal finish textures, drawn from noise (no source art):
  metal.jpg      spun aluminium disc: concentric fine rings, four soft light lobes (background)
  strip.png      brushed bar, horizontal grain, lit top / shaded bottom, dark rim (pill middle)
  cap_l/r.png    the bar's round ends, same light (pill ends: a pill is cap_l + strip + cap_r)
  bar_h/v.jpg    brushed bars for the screen frame and the art frame
Usage: gen_textures.py <theme>/v2/art   (Pillow + numpy)
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

out = sys.argv[1]
rng = np.random.default_rng(7)

def grain(h, w, axis):
    """streaks along `axis` (1: horizontal): noise stretched along the axis"""
    n = rng.normal(0, 1, (h, max(2, w // 24)) if axis == 1 else (max(2, h // 24), w))
    im = Image.fromarray(((n - n.min()) / (np.ptp(n) or 1) * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)
    fine = rng.normal(0, 1, (h, w)) * 0.15
    return (np.asarray(im, np.float32) / 255 - 0.5) + fine

# the disc
S = 720
y, x = np.mgrid[0:S, 0:S].astype(np.float32) - S / 2 + 0.5
r = np.hypot(x, y); th = np.arctan2(y, x)
rings = np.interp(r, np.arange(0, S), rng.normal(0, 1, S).cumsum() * 0.0) + rng.normal(0, 1, S)[np.clip(r.astype(int), 0, S - 1)]
rings = np.asarray(Image.fromarray(((rings - rings.min()) / np.ptp(rings) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255 - 0.5
light = 0.60 + 0.16 * np.cos(2 * (th - 0.55)) + 0.12 * np.cos(4 * (th - 0.2))
v = np.clip(light + rings * 0.10, 0, 1) * 235 + 10
disc = np.stack([v, v, v * 1.02], -1).clip(0, 255).astype(np.uint8)
Image.fromarray(disc).save(f'{out}/metal.jpg', quality=82, optimize=True)

# the bar's light, top to bottom (a rounded bar lit from above)
def shade(h):
    t = np.linspace(0, 1, h)[:, None]
    return 0.90 - 0.38 * t + 0.14 * np.exp(-((t - 0.16) / 0.09) ** 2) - 0.10 * np.exp(-((t - 0.90) / 0.08) ** 2)

H = 64
def bar(w, h, axis):
    g = grain(h, w, axis)
    s = shade(h) if axis == 1 else shade(w).T
    v = np.clip(s + g * 0.035, 0, 1) * 255
    return np.stack([v, v, v * 1.02], -1).clip(0, 255).astype(np.uint8)

def rim(a, h, w):
    """a dark 2 px rim on the bar's long edges"""
    a[:2] = (a[:2] * 0.35); a[-2:] = (a[-2:] * 0.35)
    return a

strip = rim(bar(128, H, 1).astype(np.float32), H, 128).astype(np.uint8)
Image.fromarray(strip).convert('RGBA').save(f'{out}/strip.png', optimize=True)

# the ends: the bar's light inside a half disc, its rim around (4x supersampled edge)
cw = H // 2; SS = 4
yy, xx = np.mgrid[0:H * SS, 0:cw * SS].astype(np.float32) / SS
for side in ('l', 'r'):
    cx = cw if side == 'l' else 0
    d = np.hypot(xx - cx, yy - H / 2)
    inside = (d <= H / 2).astype(np.float32)
    ring = ((d > H / 2 - 2) & (d <= H / 2)).astype(np.float32)
    a = Image.fromarray((inside * 255).astype(np.uint8)).resize((cw, H), Image.LANCZOS)
    rg = np.asarray(Image.fromarray((ring * 255).astype(np.uint8)).resize((cw, H), Image.LANCZOS), np.float32) / 255
    body = bar(cw, H, 1).astype(np.float32) * (1 - 0.65 * rg[..., None])
    im = Image.fromarray(body.clip(0, 255).astype(np.uint8)).convert('RGBA'); im.putalpha(a)
    im.save(f'{out}/cap_{side}.png', optimize=True)

Image.fromarray(bar(512, 24, 1)).save(f'{out}/bar_h.jpg', quality=85, optimize=True)
Image.fromarray(bar(24, 512, 0)).save(f'{out}/bar_v.jpg', quality=85, optimize=True)
print('ok')
