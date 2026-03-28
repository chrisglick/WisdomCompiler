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


def build_teacher_book_map() -> dict[str, list[str]]:
    """Build a mapping from teacher name -> list of book names they authored.

    Reads each book's 'teacher' frontmatter field (e.g. '[[Ramana Maharshi]]')
    and maps the teacher to the book name.
    """
    teacher_books = defaultdict(list)
    for f in sorted(BOOKS_DIR.glob("*.md")):
        if f.name.startswith("_") or f.name == "index.md":
            continue
        fm, _ = parse_frontmatter(f)
        teacher_raw = fm.get("teacher", "")
        if not teacher_raw:
            continue
        teacher_name = extract_source_name(teacher_raw)
        if teacher_name:
            teacher_books[teacher_name].append(f.stem)
    return dict(teacher_books)


SANITY_THRESHOLD = 0.20  # Abort if published count drops >20% from previous


def sanity_check(groups: dict[str, list[str]]):
    """Abort if published count drops >20% from previous run.

    Reads the current state of book files to count existing passage links,
    then compares with what the new run would produce.
    """
    current_total = 0
    for f in sorted(BOOKS_DIR.glob("*.md")):
        if f.name.startswith("_") or f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        current_total += text.count("- [[")

    new_total = sum(len(v) for v in groups.values())

    if current_total > 0 and new_total < current_total * (1 - SANITY_THRESHOLD):
        print(f"\n!!! SANITY CHECK FAILED !!!")
        print(f"  Current passage links across books: {current_total}")
        print(f"  New run would produce: {new_total}")
        print(f"  Drop: {current_total - new_total} ({(1 - new_total/current_total)*100:.1f}%)")
        print(f"  Threshold: {SANITY_THRESHOLD*100:.0f}%")
        print(f"  ABORTING to prevent data loss. Use --force to override.")
        import sys
        if "--force" not in sys.argv:
            sys.exit(1)
    else:
        print(f"  Sanity check passed: {current_total} existing -> {new_total} new links")


def main():
    print("Scanning screenshot notes...")
    groups = scan_screenshots()
    print(f"Found {sum(len(v) for v in groups.values())} notes across {len(groups)} sources")

    # Sanity check: abort if massive link drop detected
    sanity_check(groups)

    # Build teacher -> books mapping for teacher page population
    teacher_books = build_teacher_book_map()
    print(f"Found {len(teacher_books)} teachers with book attributions")

    # Process Books
    book_count = 0
    book_results = {}  # name -> passage_count (for logging)
    for f in sorted(BOOKS_DIR.glob("*.md")):
        if f.name.startswith("_") or f.name == "index.md":
            continue

        book_name = f.stem
        notes = groups.get(book_name, [])
        fm, body = parse_frontmatter(f)

        # Books with descriptions/categories stay un-drafted even without passages
        has_metadata = bool(fm.get("description") or fm.get("category"))

        if notes:
            rewrite_page(f, notes)
            set_frontmatter_draft(f, draft=False)
            print(f"  Book: {book_name} -> {len(notes)} passages")
            book_results[book_name] = len(notes)
            book_count += 1
        elif has_metadata:
            # Keep book visible — it has useful metadata for the card grid
            link_section = extract_link_section(f)
            fm_block = rebuild_frontmatter(f)
            body_parts = [fm_block, ""]
            if link_section:
                body_parts.append(link_section)
                body_parts.append("")
            body_parts.append("## Passages")
            body_parts.append("")
            body_parts.append("*Passages coming soon.*")
            body_parts.append("")
            f.write_text("\n".join(body_parts), encoding="utf-8")
            set_frontmatter_draft(f, draft=False)
            print(f"  Book: {book_name} -> 0 passages (has metadata, kept)")
            book_results[book_name] = 0
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
            book_results[book_name] = 0
            book_count += 1

    print(f"\nProcessed {book_count} book files")

    # Process Teachers
    teacher_count = 0
    teacher_results = {}  # name -> passage_count (for logging)
    for f in sorted(TEACHERS_DIR.glob("*.md")):
        if f.name.startswith("_"):
            continue

        teacher_name = f.stem

        # Merge direct quotes (source = teacher) with quotes from teacher's books
        direct_notes = groups.get(teacher_name, [])
        book_notes = []
        for book_name in teacher_books.get(teacher_name, []):
            book_notes.extend(groups.get(book_name, []))
        # Deduplicate while preserving all unique quotes
        notes = sorted(set(direct_notes + book_notes))

        fm, body = parse_frontmatter(f)

        # Teachers with metadata (tradition, core_teaching) stay un-drafted
        has_metadata = bool(fm.get("tradition") and fm.get("core_teaching"))

        if notes:
            rewrite_page(f, notes, section_title="Passages")
            set_frontmatter_draft(f, draft=False)
            print(f"  Teacher: {teacher_name} -> {len(notes)} passages")
            teacher_results[teacher_name] = len(notes)
            teacher_count += 1
        elif has_metadata:
            # Preserve existing body if it has content beyond placeholder
            if body.strip() and body.strip() != "*No passages collected yet.*":
                # Body already has real content, don't overwrite
                set_frontmatter_draft(f, draft=False)
                print(f"  Teacher: {teacher_name} -> 0 passages (has metadata, kept)")
            else:
                # Write a minimal body with passages placeholder
                fm_block = rebuild_frontmatter(f)
                body_parts = [fm_block, ""]
                body_parts.append("## Passages")
                body_parts.append("")
                body_parts.append("*Passages coming soon.*")
                body_parts.append("")
                f.write_text("\n".join(body_parts), encoding="utf-8")
                set_frontmatter_draft(f, draft=False)
                print(f"  Teacher: {teacher_name} -> 0 passages (has metadata, un-drafted)")
            teacher_results[teacher_name] = 0
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
            teacher_results[teacher_name] = 0
            teacher_count += 1

    print(f"Processed {teacher_count} teacher files")

    # Summary
    print("\n--- Source Coverage ---")
    for source, notes in sorted(groups.items()):
        print(f"  {source}: {len(notes)} notes")

    # Write audit log
    write_audit_log(book_results, teacher_results, groups)


def write_audit_log(book_results: dict, teacher_results: dict, groups: dict):
    """Write a timestamped audit log for every run."""
    from datetime import datetime

    LOG_DIR = Path(__file__).parent.parent / "ai" / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    log_path = LOG_DIR / f"link-gen-{timestamp}.md"

    total_book_passages = sum(book_results.values())
    total_teacher_passages = sum(teacher_results.values())
    books_with_passages = sum(1 for v in book_results.values() if v > 0)
    teachers_with_passages = sum(1 for v in teacher_results.values() if v > 0)
    unique_sources = len(groups)
    total_notes = sum(len(v) for v in groups.values())

    lines = [
        f"# Link Generation Log — {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total unique notes | {total_notes} |",
        f"| Unique sources | {unique_sources} |",
        f"| Books processed | {len(book_results)} |",
        f"| Books with passages | {books_with_passages} |",
        f"| Total book passages | {total_book_passages} |",
        f"| Teachers processed | {len(teacher_results)} |",
        f"| Teachers with passages | {teachers_with_passages} |",
        f"| Total teacher passages | {total_teacher_passages} |",
        "",
        "## Books",
        "",
        "| Book | Passages |",
        "|------|----------|",
    ]

    for name in sorted(book_results.keys()):
        count = book_results[name]
        lines.append(f"| {name} | {count} |")

    lines.extend([
        "",
        "## Teachers",
        "",
        "| Teacher | Passages |",
        "|---------|----------|",
    ])

    for name in sorted(teacher_results.keys()):
        count = teacher_results[name]
        lines.append(f"| {name} | {count} |")

    lines.extend([
        "",
        "## Source Coverage (all matched sources)",
        "",
        "| Source | Notes |",
        "|--------|-------|",
    ])

    for source in sorted(groups.keys()):
        lines.append(f"| {source} | {len(groups[source])} |")

    lines.append("")

    log_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nAudit log written to: {log_path}")


if __name__ == "__main__":
    main()
