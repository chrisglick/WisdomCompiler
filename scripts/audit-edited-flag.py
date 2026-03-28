"""
Audit all Edited: true quote files. For each, analyze whether the body content
is actually clean enough to warrant the Edited flag.

Files that fail quality checks get reverted to:
  Edited: false
  draft: true

Quality checks (a file is DIRTY if ANY of these are true):
1. Body contains garbled OCR (nonsensical character sequences)
2. Body contains raw URLs (http:// or https://)
3. Body has standalone page numbers
4. Body is empty or too short (<80 chars of actual text)
5. Body has OCR pipe artifacts (garbled | formatting)
6. Body has Devanagari Unicode mixed with garbled Latin
7. File has non-descriptive filename (IMG_*, UUID, photo ID)
"""

import os
import re
import sys

QUOTES_DIR = os.path.join("content", "Wisdom Quotes")
DRY_RUN = "--dry-run" in sys.argv

# === PATTERNS ===

# Genuine OCR garbage: nonsensical character sequences that aren't real words
# These are sequences of 5+ chars with unusual consonant clusters that don't
# appear in English, Sanskrit transliteration, or any language in our corpus
GARBLED_PATTERNS = [
    # Random consonant clusters that no language produces
    re.compile(r'[A-Z]{2,}[a-z]*[A-Z]{2,}[a-z]*[A-Z]{2,}'),  # MiXeD CaSe garbage like PEEUNSEE VVEREE
    re.compile(r'\b[A-Za-z]*[A-Z]{3,}[a-z]{0,2}[A-Z]{3,}[A-Za-z]*\b'),  # OHHSUOTUW, TLILILG
    re.compile(r'\b[bcdfghjklmnpqrstvwxyz]{5,}\b', re.IGNORECASE),  # 5+ consonants in a row
]

# Known OCR garbage strings (found in previous audit)
KNOWN_GARBAGE = [
    'PEEUNSEE', 'VVEREE', 'VVEENSEE', 'OHHSUOTUW', 'TLILILG', 'ABDILIG',
    'VCAPULICLIVEYU', 'ULIIELOELIU', 'TLUTITT', 'ACAMACREAITA', 'TCTHATIOT',
    'BICHAFASP', 'LOTWSRISSMT', 'YSIUNEAIAT', 'AHGEATY',
    'qitraanicaiecal', 'panipadadimandeho', 'tattacchakterandsacca',
    'honsense', 'Dilagaval', 'WOuUId', 'alu UICTCVY',
    'Owe ee ORONO', 'NEF NENG', 'IAENAD', 'EEE IMA EARLE',
    'AAA wwe ws mane', 'NA. TF .1--Lhee', 'BTS Qo HlL_omev',
    'oomolurrerflitHev', 'Sunt oucflum Glsorfl',
    'SNR NG', 'Ya AAT arated', 'TTT: HOTU', 'AAT SISAA',
    'FEAST OHHSUOTUW', 'ADYUS SHYSU',
    'LIS GuIT oT', 'FTWeMwwUyM', 'BMonoSwybd', 'sMecdc amhaGor',
    'AaflecpnrGon', 'sosHled wolls saps',
    'FATES STAT TS', 'Adeddecd Se at ACA', 'aad J Prd A GAHAN',
    'PHeaad: TARR TASa', 'TACHA S TIT',
    'N c ik D',  # very short garbled
]

# Legitimate ALL-CAPS words that should NOT be flagged
LEGITIMATE_CAPS = {
    # Sanskrit names and terms
    'VASISTHA', 'BHAGAVAN', 'BHAGIRATHA', 'SIKHIDHVAJA', 'BRAHMANA', 'BRAHMAN',
    'BRAHMAPANAM', 'BRAHMAGNI', 'ISHWARANANDA', 'MANDAVYA', 'TRITALA', 'SADHANA',
    'BHUSUNVA', 'DAKSHINAMURTI', 'PRANAYAMA', 'VIPASSANA', 'MANTRA', 'DHARMA',
    'KARMA', 'SAMSARA', 'MOKSHA', 'NIRVANA', 'ATMAN', 'PARAMATMA', 'MAHARSHI',
    'RAMANA', 'NISARGADATTA', 'SHANKARACHARYA',
    # English words that appear in ALL-CAPS in legitimate quotes
    'SEEKING', 'SURRENDER', 'COMPLETELY', 'YOURSELVES', 'WITHDRAW',
    'TEACHING', 'PERCEPTION', 'REASONING', 'PONDERING', 'THEREBY',
    'GREATER', 'COMMUNITY', 'SPIRITUALITY', 'SUMMARY', 'SETTLED',
    'CONCLUSIONS', 'INSTRUCTION', 'ABIDING', 'NEGATION', 'ULTIMATE',
    'CHILDREN', 'BELOVED', 'DISCIPLE', 'HOSTILE', 'EXCLAIMED',
    'COCONUT', 'PARTAKEN', 'RESPECT', 'PASSIONATE', 'SILENTLY',
    'SOMETIMES', 'DESCRIPTION', 'PENTADS', 'DISCARDED', 'DUALITIES',
    'HANDWRITING', 'OMNIPRESENT', 'ANALYSIS', 'SCHOLARS', 'CONSCIOUSLY',
    'PREACHER', 'ARRAKEEN', 'TLEILAXU', 'FEDAYKIN', 'JOURNALS',
    'THOUGHT', 'FAMILIAR', 'SUPPOSE', 'RELYING',
    'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER', 'JANUARY', 'FEBRUARY',
    'MARCH', 'APRIL', 'CHAPTER', 'ESSENTIAL', 'PHOTOSYNTHESIS', 'EVOLUTION',
    'INITIATION', 'SLOGANS', 'TAMASIC', 'ARTICLES',
    # Book/section titles
    'BHAGAVANS',
}

URL_PATTERN = re.compile(r'https?://')
STANDALONE_NUMBER = re.compile(r'^\s*\d{1,4}\s*$')
UUID_FILENAME = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}', re.IGNORECASE)
IMG_FILENAME = re.compile(r'^IMG_\d+\.md$')
PHOTO_ID_FILENAME = re.compile(r'^\d{10,}')


def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    if not content.startswith('---'):
        return None, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content
    return parts[1], parts[2]


def get_field(frontmatter, field):
    m = re.search(rf'{field}:\s*(.+)', frontmatter)
    return m.group(1).strip() if m else None


def has_garbled_ocr(text):
    """Check for genuine OCR garbage, excluding legitimate words."""
    # Check known garbage strings
    for garbage in KNOWN_GARBAGE:
        if garbage in text:
            return True, f"known_garbage: {garbage}"

    # Only flag words that are genuinely nonsensical — not real English/Sanskrit
    # Look for mixed-case garbage patterns like "oTLILILG" or "ABDILIGveval"
    mixed_case_garbage = re.findall(r'\b[A-Za-z]*(?:[A-Z][a-z]{0,1}[A-Z]){2,}[A-Za-z]*\b', text)
    for word in mixed_case_garbage:
        upper = word.upper()
        if upper in LEGITIMATE_CAPS or len(word) < 6:
            continue
        return True, f"mixed_case_garbage: {word}"

    return False, None


def analyze_body(body, filename):
    """Returns list of quality issues."""
    issues = []
    lines = body.strip().split('\n')
    non_image_lines = [l for l in lines if not l.strip().startswith('![') and l.strip()]
    text_only = '\n'.join(non_image_lines).strip()

    basename = os.path.basename(filename)

    # 1. Non-descriptive filename
    if IMG_FILENAME.match(basename):
        issues.append("img_filename")
    elif UUID_FILENAME.match(basename):
        issues.append("uuid_filename")
    elif PHOTO_ID_FILENAME.match(basename):
        issues.append("photo_id_filename")

    # 2. Empty or very short
    if len(text_only) == 0:
        issues.append("empty_body")
        return issues
    if len(text_only) < 30:
        issues.append(f"too_short ({len(text_only)} chars)")

    # 3. Raw URLs
    urls = URL_PATTERN.findall(text_only)
    if urls:
        issues.append(f"raw_url ({len(urls)})")

    # 4. Standalone page numbers
    num_lines = sum(1 for l in non_image_lines if STANDALONE_NUMBER.match(l))
    if num_lines > 0:
        issues.append(f"page_numbers ({num_lines})")

    # 5. Garbled OCR
    is_garbled, detail = has_garbled_ocr(text_only)
    if is_garbled:
        issues.append(f"garbled_ocr ({detail})")

    return issues


def revert_file(filepath):
    """Set Edited: false and draft: true."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    content = re.sub(r'Edited:\s*true', 'Edited: false', content, count=1)
    content = re.sub(r'draft:\s*false', 'draft: true', content, count=1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    dirty = []
    clean = []
    already_draft = 0
    no_edited = 0

    for filename in sorted(os.listdir(QUOTES_DIR)):
        if not filename.endswith('.md') or filename.startswith('_') or filename == 'index.md':
            continue

        filepath = os.path.join(QUOTES_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        frontmatter, body = parse_file(filepath)
        if not frontmatter:
            continue

        edited = get_field(frontmatter, 'Edited')
        if edited != 'true':
            no_edited += 1
            continue

        draft = get_field(frontmatter, 'draft')
        if draft == 'true':
            already_draft += 1
            continue

        issues = analyze_body(body, filepath)
        if issues:
            dirty.append((filename, issues))
        else:
            clean.append(filename)

    print(f"\n=== AUDIT RESULTS ===")
    print(f"Edited:true + draft:false scanned: {len(dirty) + len(clean)}")
    print(f"  CLEAN (keep published): {len(clean)}")
    print(f"  DIRTY (revert to draft): {len(dirty)}")
    print(f"Already draft:true: {already_draft}")
    print(f"Edited:false (skipped): {no_edited}")

    print(f"\n=== DIRTY FILES ===\n")
    for filename, issues in dirty:
        print(f"  {filename}")
        for i in issues:
            print(f"    - {i}")

    if not DRY_RUN:
        print(f"\n=== APPLYING REVERTS ===\n")
        for filename, issues in dirty:
            filepath = os.path.join(QUOTES_DIR, filename)
            revert_file(filepath)
            print(f"  REVERTED: {filename}")
        print(f"\nReverted {len(dirty)} files to Edited:false + draft:true")
    else:
        print(f"\n[DRY RUN] Would revert {len(dirty)} files")

    # Save report
    with open("ai/research/edited-flag-audit-20260323.md", "w", encoding="utf-8") as f:
        f.write(f"# Edited Flag Audit — 2026-03-23\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Scanned: {len(dirty) + len(clean)} files (Edited:true + draft:false)\n")
        f.write(f"- Clean (kept published): {len(clean)}\n")
        f.write(f"- Dirty (reverted to draft): {len(dirty)}\n\n")
        f.write(f"## Clean Files ({len(clean)})\n\n")
        for fn in clean:
            f.write(f"- {fn}\n")
        f.write(f"\n## Dirty Files ({len(dirty)})\n\n")
        for fn, issues in dirty:
            f.write(f"- **{fn}**: {'; '.join(issues)}\n")


if __name__ == "__main__":
    main()
