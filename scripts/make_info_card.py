#!/usr/bin/env python3
"""Render Rui's static, terminal-style profile card as an animated SVG."""
from html import escape
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME = os.environ.get("PROFILE_THEME", "dark").lower()
if THEME not in ("dark", "light"):
    raise ValueError("PROFILE_THEME must be 'dark' or 'light'")
OUT = ROOT / ("rui-profile-card-light.svg" if THEME == "light" else "rui-profile-card.svg")
STATIC = bool(os.environ.get("STATIC"))
W, H = 800, 860
COLORS = {
    "dark": {"bg0": "#111722", "bg1": "#0d1117", "border": "#30363d", "muted": "#7d8590", "text": "#e6edf3", "cyan": "#22d3ee", "green": "#39d353"},
    "light": {"bg0": "#ffffff", "bg1": "#f6f8fa", "border": "#d0d7de", "muted": "#57606a", "text": "#24292f", "cyan": "#0969da", "green": "#1a7f37"},
}[THEME]
lines = [
    ("name", "Rui", "text"),
    ("role", "AI Systems, Product Engineering & DevOps", "cyan"),
    ("builds", "AI tools, web platforms", "text"),
    ("focus", "Developer workflows", "text"),
    ("web", "eduardorui.com.br", "green"),
    ("github", "@eduardoruisjbv", "text"),
]
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>@keyframes arrive{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}.row{animation:arrive .5s ease-out}</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{COLORS["bg0"]}"/><stop offset="1" stop-color="{COLORS["bg1"]}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{COLORS["border"]}"/>',
    f'<line x1="0" y1="30" x2="{W}" y2="30" stroke="{COLORS["border"]}"/>',
]
for i, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
    parts.append(f'<circle cx="20" cy="15" r="5" fill="{color}" transform="translate({i*16} 0)"/>')
parts.append(f'<text x="{W/2}" y="19" fill="{COLORS["muted"]}" font-size="12" text-anchor="middle">eduardoruisjbv@github:~$ whoami</text>')
parts.append(f'<text x="44" y="104" fill="{COLORS["green"]}" font-size="25">Rui</text>')
parts.append(f'<text x="44" y="138" fill="{COLORS["muted"]}" font-size="15">AI SYSTEMS  /  PRODUCT ENGINEERING  /  DEVOPS</text>')
parts.append(f'<line x1="44" y1="168" x2="756" y2="168" stroke="{COLORS["border"]}"/>')
for i, (label, value, color) in enumerate(lines):
    y = 226 + i * 76
    cls = "" if STATIC else ' class="row" style="animation-delay:%.2fs"' % (i * 0.12)
    parts.append(f'<g{cls}><text x="48" y="{y}" fill="{COLORS["muted"]}" font-size="18">{escape(label)}</text><text x="226" y="{y}" fill="{COLORS[color]}" font-size="20">{escape(value)}</text></g>')
parts.append(f'<line x1="44" y1="718" x2="756" y2="718" stroke="{COLORS["border"]}"/>')
parts.append(f'<text x="48" y="766" fill="{COLORS["muted"]}" font-size="16">$ open to ideas, collaboration, and useful software</text>')
parts.append(f'<text x="48" y="804" fill="{COLORS["cyan"]}" font-size="15">https://eduardorui.com.br/</text>')
parts.append('</svg>')
OUT.write_text("".join(parts), encoding="utf-8")
print(f"wrote {OUT}")
