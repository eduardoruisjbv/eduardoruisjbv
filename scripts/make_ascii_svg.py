#!/usr/bin/env python3
"""Render the prepared profile avatar as a one-shot, self-typing ASCII SVG."""
from html import escape
import os
from pathlib import Path
import sys

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "source-prepped.png"
theme_name = os.environ.get("PROFILE_THEME", "dark").lower()
if theme_name not in ("dark", "light"):
    raise ValueError("PROFILE_THEME must be 'dark' or 'light'")
target = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / ("avatar-ascii-light.svg" if theme_name == "light" else "avatar-ascii.svg")
theme = {
    "dark": {"bg0": "#111722", "bg1": "#0d1117", "border": "#30363d", "muted": "#7d8590", "ink": "#c9d1d9"},
    "light": {"bg0": "#ffffff", "bg1": "#f6f8fa", "border": "#d0d7de", "muted": "#57606a", "ink": "#24292f"},
}[theme_name]
cols = int(os.environ.get("COLS", "100"))
rows = cols
art_width = 760
cell_width = art_width / cols
cell_height = cell_width
pad = 20
title_height = 30
status_height = 34
canvas_width = art_width + 2 * pad
canvas_height = title_height + rows * cell_height + status_height + pad
ramp = " .`:-=+*cs#%@"

image = Image.open(source).convert("L")
image = ImageEnhance.Contrast(image).enhance(1.08)
image = image.resize((cols, rows), Image.Resampling.LANCZOS)
pixels = image.load()
static = bool(os.environ.get("STATIC"))
row_duration = 5.8 / rows
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{theme["bg0"]}"/><stop offset="1" stop-color="{theme["bg1"]}"/></linearGradient></defs>',
    f'<rect width="{canvas_width}" height="{canvas_height}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{canvas_width-1}" height="{canvas_height-1}" rx="12" fill="none" stroke="{theme["border"]}"/>',
    f'<line x1="0" y1="{title_height}" x2="{canvas_width}" y2="{title_height}" stroke="{theme["border"]}"/>',
]
for i, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
    parts.append(f'<circle cx="{pad + i*16}" cy="15" r="5" fill="{color}"/>')
parts.append(f'<text x="{canvas_width/2}" y="19" fill="{theme["muted"]}" font-size="12" text-anchor="middle">eduardoruisjbv@github:~$ ./whoami</text>')

for y in range(rows):
    chars = []
    for x in range(cols):
        lum = pixels[x, y] / 255
        if lum >= 0.88:
            chars.append(" ")
        else:
            idx = round((1 - lum) * (len(ramp) - 1))
            chars.append(ramp[max(0, min(len(ramp) - 1, idx))])
    baseline = title_height + y * cell_height + cell_height * 0.76
    line = escape("".join(chars))
    text = (f'<text xml:space="preserve" x="{pad}" y="{baseline:.1f}" fill="{theme["ink"]}" '
            f'font-size="{cell_height*0.86:.1f}" textLength="{art_width}" '
            f'lengthAdjust="spacing">{line}</text>')
    if static:
        parts.append(text)
    else:
        delay = y * row_duration
        top = title_height + y * cell_height
        parts.append(f'<clipPath id="r{y}"><rect x="{pad}" y="{top:.1f}" width="0" height="{cell_height:.1f}"><animate attributeName="width" from="0" to="{art_width}" begin="{delay:.3f}s" dur="{row_duration:.2f}s" fill="freeze"/></rect></clipPath>')
        parts.append(f'<g clip-path="url(#r{y})">{text}</g>')

status_y = title_height + rows * cell_height + 22
parts.append(f'<line x1="0" y1="{status_y-19}" x2="{canvas_width}" y2="{status_y-19}" stroke="{theme["border"]}"/>')
parts.append(f'<text x="{pad}" y="{status_y}" fill="{theme["muted"]}" font-size="13">eduardoruisjbv@github:~$ whoami <tspan fill="{theme["ink"]}">Rui</tspan></text>')
parts.append('</svg>')
target.write_text("".join(parts), encoding="utf-8")
print(f"wrote {target} ({target.stat().st_size} bytes)")
