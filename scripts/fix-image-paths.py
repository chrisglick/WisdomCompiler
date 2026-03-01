#!/usr/bin/env python3
"""
Fix image embeds in screenshot notes for Quartz compatibility.

Converts Obsidian wikilink image embeds and broken relative paths:
  ![[IMG_1192.png]]       ->  ![](Screenshots/Images/IMG_1192.png)
  ![](../Images/IMG.png)  ->  ![](Screenshots/Images/IMG.png)

Uses full content-root paths so Quartz's CrawlLinks fallback
(pathToRoot + canonicalSlug) resolves correctly from any depth.

Re-runnable: safe to run multiple times.
"""

import re
from pathlib import Path

NOTES_DIR = Path(__file__).parent.parent / "content" / "Screenshots" / "Notes"
IMAGES_DIR = Path(__file__).parent.parent / "content" / "Screenshots" / "Images"

# Pattern matches ![[filename.ext]] where ext is an image type
WIKILINK_IMAGE_RE = re.compile(
    r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|bmp|svg|webp|PNG|JPG|JPEG))\]\]'
)

# Pattern matches ![](../Images/filename.ext) — the broken relative path from first fix attempt
RELATIVE_IMAGE_RE = re.compile(
    r'!\[\]\(\.\./Images/([^\)]+\.(?:png|jpg|jpeg|gif|bmp|svg|webp|PNG|JPG|JPEG))\)'
)


def fix_note(filepath: Path) -> bool:
    """Fix image embeds in a single note. Returns True if modified."""
    text = filepath.read_text(encoding="utf-8")
    original = text

    def replace_wikilink(match):
        filename = match.group(1)
        return f"![](Screenshots/Images/{filename})"

    def replace_relative(match):
        filename = match.group(1)
        return f"![](Screenshots/Images/{filename})"

    text = WIKILINK_IMAGE_RE.sub(replace_wikilink, text)
    text = RELATIVE_IMAGE_RE.sub(replace_relative, text)

    if text != original:
        filepath.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    fixed = 0
    total = 0

    for f in sorted(NOTES_DIR.glob("*.md")):
        if f.name.startswith("_"):
            continue
        total += 1
        if fix_note(f):
            fixed += 1

    print(f"Scanned {total} notes, fixed image paths in {fixed}")


if __name__ == "__main__":
    main()
