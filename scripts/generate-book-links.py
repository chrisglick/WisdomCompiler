#!/usr/bin/env python3
"""
Generate static markdown links for Book and Teacher pages.

Replaces Obsidian dataview queries with static wikilinks by:
1. Scanning all Wisdom Quotes for their `source` frontmatter
2. Grouping notes by source (book or teacher name)
3. Rewriting each Book/Teacher page with a list of wikilinks

Re-runnable: safe to run multiple times as it always regenerates from source data.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

CONTENT_DIR = Path(__file__).parent.parent / "content"
SCREENSHOTS_DIR = CONTENT_DIR / "Wisdom Quotes"
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


def extract_link_section(filepath: Path) -> str:
    """Extract any '## Read Online' or '## Get the Book' section from existing body.

    Only captures the header and markdown link lines (starting with '- ['),
    not any trailing content like '*No passages collected yet.*'.
    """
    text = filepath.read_text(encoding="utf-8")
    for header in ["## Read Online", "## Get the Book"]:
        idx = text.find(header)
        if idx == -1:
            continue
        # Find the next ## header to bound the section
        next_header = text.find("\n## ", idx + len(header))
        if next_header == -1:
            block = text[idx:]
        else:
            block = text[idx:next_header]
        # Keep only the header and link lines
        lines = []
        for line in block.strip().split("\n"):
            stripped = line.strip()
            if stripped.startswith("## ") or stripped.startswith("- ["):
                lines.append(line)
        return "\n".join(lines) if lines else ""
    return ""


def set_frontmatter_draft(filepath: Path, draft: bool):
    """Set draft: true/false in frontmatter."""
    text = filepath.read_text(encoding="utf-8")
    if "draft:" in text:
        text = re.sub(r"draft:\s*(true|false)", f"draft: {'true' if draft else 'false'}", text)
    else:
        # Insert draft field before closing ---
        end = text.find("---", 3)
        if end != -1:
            text = text[:end] + f"draft: {'true' if draft else 'false'}\n" + text[end:]
    filepath.write_text(text, encoding="utf-8")


def rewrite_page(filepath: Path, notes: list[str], section_title: str = "Passages"):
    """Rewrite a page: preserve frontmatter and link sections, replace passages."""
    frontmatter_block = rebuild_frontmatter(filepath)
    link_section = extract_link_section(filepath)

    lines = [frontmatter_block, ""]
    if link_section:
        lines.append(link_section)
        lines.append("")
    lines.append(f"## {section_title}")
    lines.append("")
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
            set_frontmatter_draft(f, draft=False)
            print(f"  Book: {book_name} -> {len(notes)} passages")
            book_count += 1
        else:
            # Preserve link sections even for empty books
            link_section = extract_link_section(f)
            fm_block = rebuild_frontmatter(f)
            body_parts = [fm_block, ""]
            if link_section:
                body_parts.append(link_section)
                body_parts.append("")
            body_parts.append("*No passages collected yet.*")
            body_parts.append("")
            f.write_text("\n".join(body_parts), encoding="utf-8")
            set_frontmatter_draft(f, draft=True)
            print(f"  Book: {book_name} -> 0 passages (drafted)")
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
            set_frontmatter_draft(f, draft=False)
            print(f"  Teacher: {teacher_name} -> {len(notes)} passages")
            teacher_count += 1
        else:
            link_section = extract_link_section(f)
            fm_block = rebuild_frontmatter(f)
            body_parts = [fm_block, ""]
            if link_section:
                body_parts.append(link_section)
                body_parts.append("")
            body_parts.append("*No passages collected yet.*")
            body_parts.append("")
            f.write_text("\n".join(body_parts), encoding="utf-8")
            set_frontmatter_draft(f, draft=True)
            print(f"  Teacher: {teacher_name} -> 0 passages (drafted)")
            teacher_count += 1

    print(f"Processed {teacher_count} teacher files")

    # Summary
    print("\n--- Source Coverage ---")
    for source, notes in sorted(groups.items()):
        print(f"  {source}: {len(notes)} notes")


if __name__ == "__main__":
    main()
