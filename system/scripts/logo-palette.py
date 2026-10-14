#!/usr/bin/env python3
"""Print the brand colours in input/assets-intake/logo.* (Phase 2, when
client.md has no palette). Run from repo root: `py -3 system/scripts/logo-palette.py`
(macOS/Linux: python3). Raster logos via Pillow; SVG via its fill/stroke hexes.
Near-white, near-black and transparent pixels are reported separately -
they are usually background, not brand.
"""
import collections, re, sys, pathlib

srcs = sorted(pathlib.Path("input/assets-intake").glob("logo.*"))
if not srcs:
    print("no input/assets-intake/logo.* - use client.md Palette or the niche default"); sys.exit(1)
src = srcs[0]

def hx(rgb): return "#{:02x}{:02x}{:02x}".format(*rgb)
def lum(rgb):
    c = [v / 255 for v in rgb]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def neutral(rgb): return lum(rgb) > 0.85 or lum(rgb) < 0.02

counts = collections.Counter()
if src.suffix.lower() == ".svg":
    for h in re.findall(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", src.read_text(encoding="utf-8", errors="ignore")):
        h = "".join(c * 2 for c in h) if len(h) == 3 else h
        counts[tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))] += 1
else:
    from PIL import Image
    with Image.open(src) as im:
        im = im.convert("RGBA"); im.thumbnail((200, 200))
        px = getattr(im, "get_flattened_data", im.getdata)()
        opaque = [p[:3] for p in px if p[3] > 200]
    q = Image.new("RGB", (len(opaque), 1)); q.putdata(opaque)
    q = q.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    for count, idx in q.getcolors():
        counts[tuple(pal[idx * 3: idx * 3 + 3])] += count

total = sum(counts.values()) or 1
print(f"=== LOGO PALETTE  {src.as_posix()} ===")
brand = [(c, n) for c, n in counts.most_common() if not neutral(c)]
for c, n in brand[:6]:
    print(f"BRAND    {hx(c)}  {n / total:5.1%}  luminance {lum(c):.2f}")
for c, n in [(c, n) for c, n in counts.most_common() if neutral(c)][:2]:
    print(f"NEUTRAL  {hx(c)}  {n / total:5.1%}")
if not brand:
    print("NOTE     logo is monochrome - take the accent from the niche default")
