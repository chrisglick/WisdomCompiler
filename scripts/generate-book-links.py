#!/usr/bin/env python3
"""
Generate static markdown links for Book and Teacher pages.

Replaces Obsidian dataview queries with static wikilinks by:
1. Scanning all Screenshots/Notes for their `source` frontmatter
2. Grouping notes by source (book or teacher name)
3. Rewriting each Book/Teacher page with a list of wikilinks

Re-runnable: safe to run multiple times as it always regenerates from source data.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

CONTENT_DIR = Path(__file__).parent.parent / "content"
SCREENSHOTS_DIR = CONTENT_DIR / "Screenshots" / "Notes"
BOOKS_DIR = CONTENT_DIR / "Books"
TEACHERS_DIR = CONTENT_DIR / "Teachers"

# Files to never reference
BLACKLIST = {"Whatsapp - Maji.md"}


def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and body from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    fm_text = text[3:end].strip()
    body = text[end + 3:].strip()

    # Simple key-value parsing (handles quoted values)
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")

    return fm, body


def extract_source_name(source_val: str) -> str:
    """Extract the name from a source like '[[Book Name]]' or 'Book Name'."""
    match = re.search(r"\[\[(.+?)\]\]", source_val)
    if match:
        return match.group(1)
    return source_val.strip()


def get_note_title(filepath: Path) -> str:
    """Get display name for a screenshot note (filename without .md)."""
    return filepath.stem


def scan_screenshots() -> dict[str, list[str]]:
    """Scan all screenshot notes and group by source.

    Uses case-insensitive matching via a canonical name lookup
    so 'sri ramana gita' matches 'Sri Ramana Gita'.
    """
    # First pass: collect raw groups
    raw_groups = defaultdict(list)

    for f in sorted(SCREENSHOTS_DIR.glob("*.md")):
        if f.name in BLACKLIST or f.name.startswith("_"):
            continue

        fm, _ = parse_frontmatter(f)

        # Only include edited notes
        if fm.get("Edited", "").lower() != "true":
            continue

        source = fm.get("source", "")
        if not source:
            continue

        source_name = extract_source_name(source)
        if not source_name:
            continue

        note_title = get_note_title(f)
        raw_groups[source_name].append(note_title)

    # Build canonical name map from book/teacher filenames
    canonical = {}
    for d in [BOOKS_DIR, TEACHERS_DIR]:
        if d.exists():
            for f in d.glob("*.md"):
                if not f.name.startswith("_"):
                    canonical[f.stem.lower()] = f.stem

    # Merge groups using canonical names (case-insensitive)
    merged = defaultdict(list)
    for source_name, notes in raw_groups.items():
        canon = canonical.get(source_name.lower(), source_name)
        merged[canon].extend(notes)

    return dict(merged)


def rebuild_frontmatter(filepath: Path) -> str:
    """Read a file and return ONLY its frontmatter block (including --- markers)."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return "---\n---"

    end = text.find("---", 3)
    if end == -1:
        return "---\n---"

    return text[:end + 3]


def rewrite_page(filepath: Path, notes: list[str], section_title: str = "Passages"):
    """Rewrite a page: preserve frontmatter, replace body with wikilinks."""
    frontmatter_block = rebuild_frontmatter(filepath)

    lines = [frontmatter_block, "", f"## {section_title}", ""]
    for note in sorted(notes):
        lines.append(f"- [[{note}]]")
    lines.append("")  # trailing newline

    filepath.write_text("\n".join(lines), encoding="utf-8")


def main():
    print("Scanning screenshot notes...")
    groups = scan_screenshots()
    print(f"Found {sum(len(v) for v in groups.values())} notes across {len(groups)} sources")

    # Process Books
    book_count = 0
    for f in sorted(BOOKS_DIR.glob("*.md")):
        if f.name.startswith("_"):
            continue

        book_name = f.stem
        notes = groups.get(book_name, [])

        if notes:
            rewrite_page(f, notes)
            print(f"  Book: {book_name} -> {len(notes)} passages")
            book_count += 1
        else:
            # Still remove dataview blocks even if no notes found
            fm_block = rebuild_frontmatter(f)
            f.write_text(fm_block + "\n\n*No passages collected yet.*\n", encoding="utf-8")
            print(f"  Book: {book_name} -> 0 passages (cleared dataview)")
            book_count += 1

    print(f"\nProcessed {book_count} book files")

    # Process Teachers
    teacher_count = 0
    for f in sorted(TEACHERS_DIR.glob("*.md")):
        if f.name.startswith("_"):
            continue

        teacher_name = f.stem
        notes = groups.get(teacher_name, [])

        if notes:
            rewrite_page(f, notes, section_title="Passages")
            print(f"  Teacher: {teacher_name} -> {len(notes)} passages")
            teacher_count += 1
        else:
            fm_block = rebuild_frontmatter(f)
            f.write_text(fm_block + "\n\n*No passages collected yet.*\n", encoding="utf-8")
            print(f"  Teacher: {teacher_name} -> 0 passages")
            teacher_count += 1

    print(f"Processed {teacher_count} teacher files")

    # Summary
    print("\n--- Source Coverage ---")
    for source, notes in sorted(groups.items()):
        print(f"  {source}: {len(notes)} notes")


if __name__ == "__main__":
    main()
