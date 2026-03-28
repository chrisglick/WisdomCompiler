"""
Scan all published (draft: false) wisdom quotes for OCR garbage.
Outputs a list of files that should be set to draft: true.

Signals of bad content:
1. Raw URLs in body text (http:// or https://)
2. Standalone page numbers (line is just a number)
3. Garbled OCR (high density of uppercase consonant clusters, random special chars)
4. Very short body text (< 50 chars after stripping whitespace — likely incomplete)
5. Non-descriptive filenames (IMG_*, UUID patterns) that are published
6. Sanskrit/devanagari transliteration mixed with OCR errors
7. OCR pipe artifacts (| not in tables)
"""

import os
import re
import sys

QUOTES_DIR = os.path.join("content", "Wisdom Quotes")

# Patterns that indicate OCR garbage
URL_PATTERN = re.compile(r'https?://')
STANDALONE_NUMBER = re.compile(r'^\s*\d{1,4}\s*$')
GARBLED_TEXT = re.compile(r'[A-Z]{4,}[a-z]*[A-Z]{3,}')  # e.g., PEEUNSEE, qitraanicaiecal
PIPE_ARTIFACT = re.compile(r'\|.*\|.*\|')  # OCR pipe formatting
DEVANAGARI_MIXED = re.compile(r'[\u0900-\u097F]')  # Devanagari Unicode block
RANDOM_CHARS = re.compile(r'[^a-zA-Z0-9\s.,;:!?\'"()\-\u2014\u2013\u2018\u2019\u201C\u201D\u2026]{3,}')  # 3+ non-standard chars in a row
UUID_FILENAME = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}', re.IGNORECASE)
IMG_FILENAME = re.compile(r'^IMG_\d+\.md$')
PHOTO_ID_FILENAME = re.compile(r'^\d{10,}')

def parse_file(filepath):
    """Parse frontmatter and body from a markdown file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    frontmatter = parts[1]
    body = parts[2]
    return frontmatter, body

def is_draft(frontmatter):
    """Check if draft: true in frontmatter."""
    if not frontmatter:
        return True
    return bool(re.search(r'draft:\s*true', frontmatter))

def analyze_body(body, filename):
    """Analyze body text for OCR garbage. Returns list of reasons."""
    reasons = []
    lines = body.strip().split('\n')
    body_text = body.strip()

    # Skip image-only lines
    non_image_lines = [l for l in lines if not l.strip().startswith('![') and l.strip()]
    text_only = '\n'.join(non_image_lines).strip()

    # 1. Raw URLs in body
    url_count = len(URL_PATTERN.findall(text_only))
    if url_count > 0:
        reasons.append(f"raw_url ({url_count} URLs in body)")

    # 2. Standalone page numbers
    num_lines = sum(1 for l in non_image_lines if STANDALONE_NUMBER.match(l))
    if num_lines > 0:
        reasons.append(f"page_numbers ({num_lines} standalone numbers)")

    # 3. Garbled OCR text
    garbled = GARBLED_TEXT.findall(text_only)
    if garbled:
        reasons.append(f"garbled_ocr ({len(garbled)} patterns: {garbled[:3]})")

    # 4. Very short body (< 50 chars of actual text)
    if len(text_only) < 50 and len(text_only) > 0:
        reasons.append(f"too_short ({len(text_only)} chars)")

    # 5. Empty body
    if len(text_only) == 0:
        reasons.append("empty_body")

    # 6. Devanagari mixed with Latin (OCR artifact)
    if DEVANAGARI_MIXED.search(text_only):
        reasons.append("devanagari_mixed")

    # 7. Random special characters
    random = RANDOM_CHARS.findall(text_only)
    if random:
        reasons.append(f"random_chars ({len(random)} clusters)")

    # 8. Non-descriptive filename that's published
    basename = os.path.basename(filename)
    if IMG_FILENAME.match(basename):
        reasons.append("img_filename")
    elif UUID_FILENAME.match(basename):
        reasons.append("uuid_filename")
    elif PHOTO_ID_FILENAME.match(basename):
        reasons.append("photo_id_filename")

    # 9. OCR pipe formatting artifacts
    pipe_lines = sum(1 for l in non_image_lines if PIPE_ARTIFACT.search(l))
    if pipe_lines > 0:
        reasons.append(f"pipe_artifacts ({pipe_lines} lines)")

    return reasons

def main():
    results = []
    clean_count = 0
    draft_count = 0

    for filename in sorted(os.listdir(QUOTES_DIR)):
        if not filename.endswith('.md'):
            continue
        if filename.startswith('_') or filename == 'index.md':
            continue

        filepath = os.path.join(QUOTES_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        frontmatter, body = parse_file(filepath)

        if is_draft(frontmatter):
            draft_count += 1
            continue

        reasons = analyze_body(body, filepath)

        if reasons:
            results.append((filename, reasons))
        else:
            clean_count += 1

    # Output
    print(f"\n=== SCAN RESULTS ===")
    print(f"Already draft: {draft_count}")
    print(f"Published & clean: {clean_count}")
    print(f"Published & BAD: {len(results)}")
    print(f"\n=== FILES TO DRAFT ===\n")

    for filename, reasons in results:
        print(f"  {filename}")
        for r in reasons:
            print(f"    - {r}")

    print(f"\nTotal to draft: {len(results)}")

    # Write list for processing
    with open("scripts/bad-quotes-list.txt", "w") as f:
        for filename, reasons in results:
            f.write(f"{filename}\t{'; '.join(reasons)}\n")

if __name__ == "__main__":
    main()
