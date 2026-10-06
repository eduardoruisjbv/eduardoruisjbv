#!/usr/bin/env python3
"""Prepare the profile avatar as a high-contrast grayscale source image."""
from pathlib import Path
import sys

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "source-photo.jpg"
target = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "source-prepped.png"

image = Image.open(source).convert("RGB")
image = ImageOps.fit(image, (512, 512), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
gray = ImageOps.grayscale(image)
# The avatar already has a light backdrop. Push near-white pixels to white so
# they disappear into the empty end of the ASCII density ramp.
gray = ImageEnhance.Contrast(gray).enhance(1.55)
gray = gray.point(lambda value: 255 if value >= 226 else value)
gray.save(target)
print(f"wrote {target}")
