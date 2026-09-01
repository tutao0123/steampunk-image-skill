#!/usr/bin/env python3
"""Palette QC for steampunk outputs — checks an image against the five-ink rule.

Flags saturated blue / cyan / purple / magenta (never allowed) and hot photo
green (only desaturated verdigris is allowed). Needs Pillow; that is the one
dependency here, everything else in this repo stays stdlib-only.

Usage:
  python scripts/style_check.py image.jpg [more.jpg ...]   # JSON verdict per image
"""

import json
import sys

BAD_PCT_LIMIT = 1.0    # blue+cyan+purple % of pixels above which the image fails
GREEN_PCT_LIMIT = 4.0  # hot green % above which the image fails


def analyze(path):
    """Return {"blue":%,"purple":%,"green":%,"bad":%,"pass":bool} or None if Pillow is missing."""
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(path).convert("RGB")
    im.thumbnail((256, 256))
    hsv = im.convert("HSV")
    blue = purple = green = total = 0
    for h, s, v in hsv.getdata():
        total += 1
        if s < 70 or v < 50:
            continue
        if 120 <= h <= 185:          # blue / cyan
            blue += 1
        elif 185 < h <= 235:         # purple / magenta
            purple += 1
        elif 55 <= h <= 105 and s > 120 and v > 110:  # hot photo green
            green += 1
    pct = lambda n: round(100.0 * n / total, 2)
    bad = pct(blue + purple)
    grn = pct(green)
    return {"blue": pct(blue), "purple": pct(purple), "green": grn,
            "bad": bad, "pass": bad < BAD_PCT_LIMIT and grn < GREEN_PCT_LIMIT}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        r = analyze(path)
        print(path, json.dumps(r) if r else '{"error": "Pillow not installed"}')
