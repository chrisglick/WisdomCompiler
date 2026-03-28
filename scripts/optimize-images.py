#!/usr/bin/env python3
"""Convert quote images to WebP format and resize to max 1200px width.

Requires ImageMagick (magick command).
Creates .webp versions alongside originals, then updates references.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

IMAGES_DIR = Path("content/Wisdom Quotes/Images")
QUOTES_DIR = Path("content/Wisdom Quotes")
MAX_WIDTH = 1200
QUALITY = 80
DRY_RUN = "--dry-run" in sys.argv


def get_image_files():
    """Get all image files that aren't already WebP."""
    exts = {".png", ".jpg", ".jpeg"}
    files = []
    for f in sorted(IMAGES_DIR.iterdir()):
        if f.suffix.lower() in exts:
            files.append(f)
    return files


def convert_image(src: Path) -> Path:
    """Convert image to WebP, resize if wider than MAX_WIDTH."""
    dst = src.with_suffix(".webp")
    cmd = [
        "magick", str(src),
        "-resize", f"{MAX_WIDTH}x>",  # Only shrink, never enlarge
        "-quality", str(QUALITY),
        str(dst)
    ]
    if DRY_RUN:
        print(f"  [DRY RUN] {' '.join(cmd)}")
        return dst

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {src.name}: {result.stderr.strip()}")
        return None
    return dst


def update_references(old_name: str, new_name: str):
    """Update image references in quote markdown files."""
    for f in QUOTES_DIR.glob("*.md"):
        text = f.read_text(encoding="utf-8", errors="replace")
        if old_name in text:
            text = text.replace(old_name, new_name)
            if not DRY_RUN:
                f.write_text(text, encoding="utf-8")


def main():
    images = get_image_files()
    print(f"Found {len(images)} images to convert")

    converted = 0
    saved_bytes = 0
    errors = 0

    for i, src in enumerate(images):
        old_size = src.stat().st_size
        dst = convert_image(src)
        if dst is None:
            errors += 1
            continue

        if not DRY_RUN and dst.exists():
            new_size = dst.stat().st_size
            savings = old_size - new_size
            saved_bytes += savings

            # Update references
            update_references(src.name, dst.name)

            # Remove original
            src.unlink()
            converted += 1

            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(images)} ({saved_bytes/1024/1024:.1f} MB saved)")
        elif DRY_RUN:
            converted += 1

    print(f"\nDone: {converted} converted, {errors} errors")
    print(f"Space saved: {saved_bytes/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
