#!/usr/bin/env python3
"""
Lint and clean screenshot notes for Quartz compatibility.

Four passes per note (single read/write cycle):
  1. Remove text:: / test:: dataview inline field prefix
  2. Add ShowImage frontmatter (true for Memes, false for rest)
  3. Remove image embed line unless ShowImage: true
  4. Format long texts: double-space -> paragraph breaks (>500 chars only)

Re-runnable: safe to run multiple times (idempotent).
"""

import re
from pathlib import Path

NOTES_DIR = Path(__file__).parent.parent / "content" / "Wisdom Quotes"

# Image embed line pattern
IMAGE_EMBED_RE = re.compile(
    r'^!\[\]\(Images/[^\)]+\.(?:png|jpg|jpeg|gif|bmp|svg|webp|PNG|JPG|JPEG)\)\s*$',
    re.MULTILINE
)

# Wikilink image embed (in case any remain)
WIKILINK_IMAGE_RE = re.compile(
    r'^!\[\[[^\]]+\.(?:png|jpg|jpeg|gif|bmp|svg|webp|PNG|JPG|JPEG)\]\]\s*$',
    re.MULTILINE
)


def is_meme(text: str) -> bool:
    """Check if note has Source Type: Meme."""
    return bool(re.search(r'- Meme', text))


def add_show_image(text: str, value: bool) -> str:
    """Add or update ShowImage in frontmatter."""
    val_str = "true" if value else "false"

    # Already has ShowImage — update it
    if re.search(r'^ShowImage:\s*(true|false)\s*$', text, re.MULTILINE):
        return re.sub(
            r'^ShowImage:\s*(true|false)\s*$',
            f'ShowImage: {val_str}',
            text,
            count=1,
            flags=re.MULTILINE
        )

    # Insert ShowImage before the closing --- of frontmatter
    # Find second --- (closing frontmatter delimiter)
    lines = text.split('\n')
    delimiter_count = 0
    insert_idx = None
    for i, line in enumerate(lines):
        if line.strip() == '---':
            delimiter_count += 1
            if delimiter_count == 2:
                insert_idx = i
                break

    if insert_idx is not None:
        lines.insert(insert_idx, f'ShowImage: {val_str}')
        return '\n'.join(lines)

    return text


def remove_text_prefix(text: str) -> str:
    """Remove text:: and test:: dataview inline field prefix."""
    # Match text:: or test:: at start of line
    text = re.sub(r'^text::', '', text, flags=re.MULTILINE)
    text = re.sub(r'^test::', '', text, flags=re.MULTILINE)
    return text


def remove_image_embed(text: str) -> str:
    """Remove image embed lines."""
    text = IMAGE_EMBED_RE.sub('', text)
    text = WIKILINK_IMAGE_RE.sub('', text)
    return text


def format_paragraphs(text: str) -> str:
    """Split frontmatter from body, format body double-spaces into paragraphs.

    Only applies to bodies >500 chars. Converts OCR double-space paragraph
    markers into actual markdown paragraph breaks.
    """
    # Split frontmatter from body
    if not text.startswith('---'):
        return text

    end = text.find('---', 3)
    if end == -1:
        return text

    frontmatter = text[:end + 3]
    body = text[end + 3:]

    # Only format longer texts
    if len(body.strip()) <= 500:
        return text

    # Replace double-space (OCR paragraph gap) with paragraph break
    # But not inside frontmatter
    body = re.sub(r'  ', '\n\n', body)

    return frontmatter + body


def lint_note(filepath: Path) -> bool:
    """Lint a single note. Returns True if modified."""
    text = filepath.read_text(encoding='utf-8')
    original = text

    # Pass 1: Remove text:: prefix
    text = remove_text_prefix(text)

    # Pass 2: Add ShowImage frontmatter (before image removal)
    meme = is_meme(text)
    text = add_show_image(text, value=meme)

    # Pass 3: Remove image embed unless ShowImage: true
    if not meme and not re.search(r'^ShowImage:\s*true\s*$', text, re.MULTILINE):
        text = remove_image_embed(text)

    # Pass 4: Format long texts with paragraph breaks
    text = format_paragraphs(text)

    # Clean up triple+ blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    if text != original:
        filepath.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    fixed = 0
    total = 0
    memes = 0

    for f in sorted(NOTES_DIR.glob('*.md')):
        if f.name.startswith('_') or f.name == 'index.md':
            continue
        total += 1
        content = f.read_text(encoding='utf-8')
        if is_meme(content):
            memes += 1
        if lint_note(f):
            fixed += 1

    print(f"Scanned {total} notes, modified {fixed}")
    print(f"  Memes (ShowImage: true): {memes}")
    print(f"  Others (ShowImage: false): {total - memes}")


if __name__ == '__main__':
    main()
