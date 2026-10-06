#!/usr/bin/env python3
"""Render Rui's static, terminal-style profile card as an animated SVG."""
from html import escape
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "rui-profile-card.svg"
STATIC = bool(os.environ.get("STATIC"))
W, H = 800, 860
lines = [
    ("name", "Rui", "#e6edf3"),
    ("role", "AI Systems & Product Engineer", "#22d3ee"),
    ("builds", "AI tools, web platforms", "#e6edf3"),
    ("focus", "Developer workflows", "#e6edf3"),
    ("web", "eduardorui.com.br", "#39d353"),
    ("github", "@eduardoruisjbv", "#e6edf3"),
]
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>@keyframes arrive{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}.row{animation:arrive .5s ease-out}</style>',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="#30363d"/>',
    f'<line x1="0" y1="30" x2="{W}" y2="30" stroke="#30363d"/>',
]
for i, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
    parts.append(f'<circle cx="20" cy="15" r="5" fill="{color}" transform="translate({i*16} 0)"/>')
parts.append(f'<text x="{W/2}" y="19" fill="#7d8590" font-size="12" text-anchor="middle">eduardoruisjbv@github:~$ whoami</text>')
parts.append('<text x="44" y="104" fill="#39d353" font-size="25">Rui</text>')
parts.append('<text x="44" y="138" fill="#7d8590" font-size="15">AI SYSTEMS  /  PRODUCT ENGINEERING</text>')
parts.append('<line x1="44" y1="168" x2="756" y2="168" stroke="#30363d"/>')
for i, (label, value, color) in enumerate(lines):
    y = 226 + i * 76
    cls = "" if STATIC else ' class="row" style="animation-delay:%.2fs"' % (i * 0.12)
    parts.append(f'<g{cls}><text x="48" y="{y}" fill="#7d8590" font-size="18">{escape(label)}</text><text x="226" y="{y}" fill="{color}" font-size="20">{escape(value)}</text></g>')
parts.append('<line x1="44" y1="718" x2="756" y2="718" stroke="#30363d"/>')
parts.append('<text x="48" y="766" fill="#7d8590" font-size="16">$ open to ideas, collaboration, and useful software</text>')
parts.append('<text x="48" y="804" fill="#22d3ee" font-size="15">https://eduardorui.com.br/</text>')
parts.append('</svg>')
OUT.write_text("".join(parts), encoding="utf-8")
print(f"wrote {OUT}")
