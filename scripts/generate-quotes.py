"""
Generate random quotes data from vault screenshot notes.

Scans content/Wisdom Quotes/ for edited notes with readable filenames,
extracts quote text (note title) and source, outputs quartz/components/scripts/randomquote.inline.ts.

Usage: python scripts/generate-quotes.py
"""

import os
import re

NOTES_DIR = os.path.join("content", "Wisdom Quotes")
OUTPUT_FILE = os.path.join("quartz", "components", "scripts", "randomquote.inline.ts")

# UUID pattern to skip machine-generated filenames
UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    re.IGNORECASE
)
# Skip filenames that start with long numeric sequences (photo IDs)
PHOTO_ID_PATTERN = re.compile(r'^\d{10,}')
# Skip filenames that start with chapter/verse numbers
CHAPTER_NUM_PATTERN = re.compile(r'^\d+[\.\s]')

MIN_TITLE_LENGTH = 25
MAX_TITLE_LENGTH = 150


def parse_frontmatter(filepath):
    """Extract frontmatter fields from a markdown file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None

    end = content.find("---", 3)
    if end == -1:
        return None

    fm_text = content[3:end].strip()
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val

    return fm


def extract_source(fm):
    """Extract clean source name from frontmatter source field."""
    source = fm.get("source", "")
    source = re.sub(r'\[\[([^\]]+)\]\]', r'\1', source)
    return source.strip()


def clean_title(title):
    """Clean a note title for use as quote text."""
    # Remove .txt suffix if present
    if title.endswith(".txt"):
        title = title[:-4]

    # Remove trailing underscores (Obsidian escaping)
    title = title.rstrip("_")

    # Clean up multiple spaces
    title = re.sub(r'\s+', ' ', title).strip()

    return title


def is_good_quote(title):
    """Filter for quality quotes suitable for a banner."""
    # Too short or too long
    if len(title) < MIN_TITLE_LENGTH or len(title) > MAX_TITLE_LENGTH:
        return False

    # Starts with chapter/verse number
    if CHAPTER_NUM_PATTERN.match(title):
        return False

    # Starts with lowercase (sentence fragment)
    if title[0].islower():
        return False

    # Starts with common non-quote patterns
    skip_starts = [
        "Image ", "IMG_", "TOPIC OF", "THE WAN LING",
        "THE CHUN CHOU", "Chapter ", "M:", "Q:", "M.",
        "Chemistry ", "May ", "Yesterday ", "Afternoon ",
    ]
    for prefix in skip_starts:
        if title.startswith(prefix):
            return False

    # Contains ALL CAPS words of 4+ chars (shouting, not quote-like)
    # Exception: single emphasis words are OK
    caps_words = re.findall(r'\b[A-Z]{4,}\b', title)
    if len(caps_words) > 2:
        return False

    return True


def title_to_slug(title):
    """Convert note title to Quartz-compatible slug path."""
    return f"Wisdom-Quotes/{title}"


def main():
    quotes = []

    for fname in sorted(os.listdir(NOTES_DIR)):
        if not fname.endswith(".md"):
            continue
        if fname.startswith("_"):
            continue

        raw_title = fname[:-3]  # strip .md

        # Skip UUID and photo ID filenames
        if UUID_PATTERN.match(raw_title):
            continue
        if PHOTO_ID_PATTERN.match(raw_title):
            continue

        filepath = os.path.join(NOTES_DIR, fname)
        fm = parse_frontmatter(filepath)

        if fm is None:
            continue
        if fm.get("Edited", "").lower() != "true":
            continue

        source = extract_source(fm)
        if not source:
            continue

        # Skip sources that aren't real books/teachers
        skip_sources = ["Whatsapp", "Gantz", "A Very Special Patron"]
        if any(s in source for s in skip_sources):
            continue

        title = clean_title(raw_title)

        if not is_good_quote(title):
            continue

        slug = title_to_slug(raw_title)

        quotes.append({
            "text": title,
            "source": source,
            "slug": slug,
        })

    # Deduplicate by text
    seen = set()
    unique_quotes = []
    for q in quotes:
        if q["text"] not in seen:
            seen.add(q["text"])
            unique_quotes.append(q)
    quotes = unique_quotes

    print(f"Found {len(quotes)} quality quotes from edited notes")

    # Sort for deterministic output
    quotes.sort(key=lambda q: q["text"])

    # Generate TypeScript file
    ts_lines = ["const quotes = ["]
    for q in quotes:
        text_escaped = q["text"].replace("\\", "\\\\").replace('"', '\\"')
        source_escaped = q["source"].replace("\\", "\\\\").replace('"', '\\"')
        slug_escaped = q["slug"].replace("\\", "\\\\").replace('"', '\\"')
        ts_lines.append(f'  {{ text: "{text_escaped}", source: "{source_escaped}", slug: "{slug_escaped}" }},')
    ts_lines.append("]")
    ts_lines.append("")
    ts_lines.append('document.addEventListener("nav", () => {')
    ts_lines.append('  const container = document.getElementById("random-quote")')
    ts_lines.append("  if (!container) return")
    ts_lines.append("")
    ts_lines.append("  const q = quotes[Math.floor(Math.random() * quotes.length)]")
    ts_lines.append('  const quoteEl = document.getElementById("random-quote-text")')
    ts_lines.append('  const sourceEl = document.getElementById("random-quote-source")')
    ts_lines.append('  const linkEl = document.getElementById("random-quote-link") as HTMLAnchorElement | null')
    ts_lines.append("  if (!quoteEl || !sourceEl) return")
    ts_lines.append("")
    ts_lines.append("  quoteEl.textContent = q.text")
    ts_lines.append('  sourceEl.textContent = "\\u2014 " + q.source')
    ts_lines.append('  if (linkEl) linkEl.href = "/" + q.slug')
    ts_lines.append("})")
    ts_lines.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(ts_lines))

    print(f"Wrote {OUTPUT_FILE} with {len(quotes)} quotes")


if __name__ == "__main__":
    main()
