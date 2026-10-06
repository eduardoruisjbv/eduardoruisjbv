#!/usr/bin/env python3
"""Render the contribution JSON as an animated GitHub-style heatmap SVG."""
from datetime import date
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
OUT = ROOT / "contrib-heatmap.svg"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL, GAP, PAD = 12, 3, 22
STEP = CELL + GAP


def level(count):
    return 0 if count == 0 else 1 if count <= 5 else 2 if count <= 15 else 3 if count <= 30 else 4


def build_grid(days):
    first = date.fromisoformat(days[0]["date"])
    grid, column = [], [None] * ((first.weekday() + 1) % 7)
    for item in days:
        weekday = (date.fromisoformat(item["date"]).weekday() + 1) % 7
        while len(column) < weekday:
            column.append(None)
        column.append((item["date"], item["count"], level(item["count"])))
        if len(column) == 7:
            grid.append(column)
            column = []
    if column:
        grid.append(column + [None] * (7 - len(column)))
    return grid


def render():
    grid = build_grid(DATA["days"])
    left, top = 52, 50
    width = left + len(grid) * STEP + PAD
    height = top + 7 * STEP + 104
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<style>@keyframes reveal{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}.cell{opacity:0;animation:reveal .42s cubic-bezier(.2,.8,.2,1) both}</style>',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1420"/><stop offset="1" stop-color="#0a0e14"/></linearGradient></defs>',
        f'<rect width="{width}" height="{height}" rx="12" fill="url(#bg)"/><rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="none" stroke="#1f6feb" stroke-opacity=".55"/>',
        f'<line x1="0" y1="30" x2="{width}" y2="30" stroke="#1f6feb" stroke-opacity=".35"/>',
        '<text x="22" y="20" fill="#ff5f56" font-size="12">●</text><text x="38" y="20" fill="#ffbd2e" font-size="12">●</text><text x="54" y="20" fill="#27c93f" font-size="12">●</text>',
        f'<text x="{width/2}" y="20" fill="#7d8590" font-size="12" text-anchor="middle">eduardoruisjbv@github:~$ ./contributions --year</text>',
    ]
    months_seen = set()
    for column_index, column in enumerate(grid):
        for cell in column:
            if cell:
                d = date.fromisoformat(cell[0])
                key = (d.year, d.month)
                if key not in months_seen and d.day <= 7:
                    months_seen.add(key)
                    parts.append(f'<text x="{left+column_index*STEP}" y="44" fill="#7d8590" font-size="10">{d.strftime("%b")}</text>')
                break
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        parts.append(f'<text x="22" y="{top+row*STEP+10}" fill="#7d8590" font-size="9">{name}</text>')
    for ci, column in enumerate(grid):
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            day, count, lvl = cell
            x, y = left + ci * STEP, top + ri * STEP
            delay = ci * .018 + ri * .045
            parts.append(f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[lvl]}" style="animation-delay:{delay:.3f}s"><title>{day}: {count} contribution{"s" if count != 1 else ""}</title></rect>')
    legend_y = top + 7 * STEP + 16
    parts.append(f'<text x="{width-196}" y="{legend_y+10}" fill="#7d8590" font-size="10">Less</text>')
    for i, color in enumerate(PALETTE):
        parts.append(f'<rect x="{width-165+i*15}" y="{legend_y}" width="12" height="12" rx="2" fill="{color}"/>')
    parts.append(f'<text x="{width-84}" y="{legend_y+10}" fill="#7d8590" font-size="10">More</text>')
    total = DATA["total_contributions"]
    parts.append(f'<text x="22" y="{height-22}" fill="#39d353" font-size="13"><tspan font-weight="700">{total:,}</tspan><tspan fill="#7d8590"> contributions in the last year</tspan></text>')
    parts.append(f'<text x="{width-22}" y="{height-22}" fill="#7d8590" font-size="11" text-anchor="end">{DATA["range"]["start"]} → {DATA["range"]["end"]}</text>')
    parts.append('</svg>')
    return ''.join(parts)


OUT.write_text(render(), encoding="utf-8")
print(f"wrote {OUT}")
