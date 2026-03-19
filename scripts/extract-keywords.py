"""
Extract wisdom concept keywords from quotes and add them as tags.

Scans all published quotes in content/Wisdom Quotes/, matches text against
a curated taxonomy of spiritual concepts, and adds matching concepts as
tags in frontmatter.

Idempotent — safe to re-run. Preserves existing tags, adds new concept tags.

Usage: python scripts/extract-keywords.py [--dry-run]
"""

import os
import re
import sys

NOTES_DIR = os.path.join("content", "Wisdom Quotes")

# === WISDOM TAXONOMY ===
# Each concept has a canonical name and a list of matching patterns.
# Patterns are case-insensitive and match as whole words or phrases.

TAXONOMY = {
    # Tier 1 — Universal Themes
    "self-knowledge": [
        r"\bself[- ]?enquiry\b", r"\bself[- ]?knowledge\b", r"\bself[- ]?reali[sz]ation\b",
        r"\bwho am i\b", r"\batma[n]?\b", r"\bvichara\b", r"\bself[- ]?awareness\b",
        r"\btrue self\b", r"\btrue nature\b", r"\bknow thyself\b", r"\bknow yourself\b",
        r"\binquiry\b", r"\benquiry\b", r"\binquire\b",
    ],
    "ego": [
        r"\bego\b", r"\bahamkara\b", r"\bfalse self\b", r"\bi[- ]?thought\b",
        r"\bindividuality\b", r"\bidentification\b", r"\bidentified\b",
        r"\bself[- ]?importance\b", r"\bpersonality\b",
    ],
    "surrender": [
        r"\bsurrender\b", r"\bletting go\b", r"\blet go\b", r"\bsubmission\b",
        r"\bsubmit\b", r"\bprapatti\b", r"\brelinquish\b", r"\brelinquishment\b",
        r"\babandon\b", r"\bgive up\b", r"\byield\b",
    ],
    "silence": [
        r"\bsilence\b", r"\bstillness\b", r"\bmouna\b", r"\bquiet\b",
        r"\bpeaceful?\b", r"\bpeace\b", r"\bserenit[iy]\b", r"\bcalm\b",
        r"\btranquilit[iy]\b",
    ],
    "love-devotion": [
        r"\blove\b", r"\bdevoti\w+\b", r"\bbhakti\b", r"\bcompassion\b",
        r"\bgrace\b", r"\bmercy\b", r"\bblessing\b", r"\bworship\b",
        r"\bprayer\b", r"\badorati\w+\b",
    ],
    "knowledge-wisdom": [
        r"\bjnana\b", r"\bgnosis\b", r"\bwisdom\b", r"\bknowledge\b",
        r"\bunderstanding\b", r"\bvidya\b", r"\bintellect\b",
        r"\bdiscernment\b", r"\bviveka\b",
    ],
    "guru-teacher": [
        r"\bguru\b", r"\bmaster\b", r"\bteacher\b", r"\bsatguru\b",
        r"\bshishya\b", r"\bdisciple\b", r"\bsage\b", r"\bsaint\b",
        r"\bbhagavan\b", r"\bswami\b",
    ],
    "liberation": [
        r"\bliberation\b", r"\bmoksha\b", r"\benlightenment\b", r"\bnirvana\b",
        r"\bfreedom\b", r"\bemancipati\w+\b", r"\bsalvation\b",
        r"\bawakening\b", r"\bkaivalya\b", r"\bsahaja\b",
    ],
    "meditation": [
        r"\bmeditat\w+\b", r"\bsadhana\b", r"\bpractice\b", r"\bdhyana\b",
        r"\bsamadhi\b", r"\bcontemplat\w+\b", r"\bjapa\b",
        r"\bconcentrat\w+\b", r"\babsorpti\w+\b",
    ],
    "divine": [
        r"\bgod\b", r"\bdivine\b", r"\ballah\b", r"\bbrahman\b",
        r"\babsolute\b", r"\bsupreme\b", r"\bparamatma\b",
        r"\blord\b", r"\bcreator\b", r"\btranscenden\w+\b",
    ],

    # Tier 2 — Specific Concepts
    "mind": [
        r"\bmind\b", r"\bthoughts?\b", r"\bthinking\b", r"\bmanas\b",
        r"\bmental\b", r"\bconcepts?\b", r"\bnotions?\b",
        r"\billusi\w+\b", r"\bmaya\b",
    ],
    "humility": [
        r"\bhumilit[iy]\b", r"\bhumble\b", r"\bmodest[iy]?\b",
        r"\bsimplicit[iy]\b", r"\bsimple\b", r"\bmeek\b",
    ],
    "death-impermanence": [
        r"\bdeath\b", r"\bdie\b", r"\bdying\b", r"\bimpermanen\w+\b",
        r"\btransien\w+\b", r"\bmortali\w+\b", r"\bdissoluti\w+\b",
    ],
    "nature-creation": [
        r"\bnature\b", r"\bcreation\b", r"\buniverse\b", r"\bcosm\w+\b",
        r"\bworld\b", r"\bearth\b", r"\bexistence\b",
    ],
    "service": [
        r"\bservice\b", r"\bserv\w+\b", r"\bkarma[- ]?yoga\b",
        r"\bduty\b", r"\bdharma\b", r"\baction\b", r"\bwork\b",
    ],
    "scripture": [
        r"\bscripture\b", r"\bteaching\b", r"\bveda\b", r"\bsutra\b",
        r"\bgita\b", r"\bquran\b", r"\bbible\b", r"\bgospel\b",
    ],
}

# Compile patterns
COMPILED_TAXONOMY = {}
for concept, patterns in TAXONOMY.items():
    COMPILED_TAXONOMY[concept] = [re.compile(p, re.IGNORECASE) for p in patterns]


def parse_file(filepath):
    """Read file and split into frontmatter + body."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None, None, content

    end = content.find("---", 3)
    if end == -1:
        return None, None, content

    fm_raw = content[3:end]
    body = content[end + 3:]
    return fm_raw, body, content


def extract_tags(fm_raw):
    """Extract existing tags from frontmatter text."""
    tags = []
    in_tags = False
    for line in fm_raw.split("\n"):
        stripped = line.strip()
        if stripped.startswith("tags:"):
            rest = stripped[5:].strip()
            if rest.startswith("["):
                # Inline array: tags: [foo, bar]
                inner = rest.strip("[]")
                if inner:
                    tags = [t.strip().strip("'\"") for t in inner.split(",") if t.strip()]
                return tags
            elif rest:
                tags.append(rest)
            in_tags = True
            continue
        if in_tags:
            if stripped.startswith("- "):
                tags.append(stripped[2:].strip().strip("'\""))
            elif stripped and not stripped.startswith("-"):
                in_tags = False
    return tags


def match_concepts(text):
    """Find all matching concepts in text."""
    matched = set()
    for concept, patterns in COMPILED_TAXONOMY.items():
        for pattern in patterns:
            if pattern.search(text):
                matched.add(concept)
                break
    return sorted(matched)


def rebuild_frontmatter(fm_raw, new_tags):
    """Rebuild frontmatter with updated tags."""
    lines = fm_raw.split("\n")
    result = []
    skip_tag_items = False

    for line in lines:
        stripped = line.strip()

        # Skip existing tags section
        if stripped.startswith("tags:"):
            skip_tag_items = True
            continue
        if skip_tag_items:
            if stripped.startswith("- ") or stripped == "[]" or stripped == "":
                if stripped.startswith("- "):
                    continue
                if stripped == "[]":
                    continue
            else:
                skip_tag_items = False

        if not skip_tag_items:
            result.append(line)

    # Remove trailing empty lines
    while result and result[-1].strip() == "":
        result.pop()

    # Add new tags
    if new_tags:
        result.append("tags:")
        for tag in sorted(new_tags):
            result.append(f"  - {tag}")
    else:
        result.append("tags: []")

    return "\n".join(result)


def main():
    dry_run = "--dry-run" in sys.argv

    stats = {"scanned": 0, "tagged": 0, "concepts": {}}
    changes = []

    for fname in sorted(os.listdir(NOTES_DIR)):
        if not fname.endswith(".md") or fname.startswith("_"):
            continue
        if fname in ("index.md", "Screenshots.md"):
            continue

        filepath = os.path.join(NOTES_DIR, fname)
        fm_raw, body, full_content = parse_file(filepath)

        if fm_raw is None:
            continue

        stats["scanned"] += 1

        # Get existing tags
        existing_tags = extract_tags(fm_raw)

        # Match concepts against filename (title) + body text
        title = fname[:-3]
        searchable_text = title + " " + (body or "")
        new_concepts = match_concepts(searchable_text)

        # Merge: keep existing non-concept tags, add matched concepts
        existing_non_concept = [t for t in existing_tags if t not in TAXONOMY and t != "home"]
        merged_tags = sorted(set(existing_non_concept + new_concepts))

        # Track stats
        for c in new_concepts:
            stats["concepts"][c] = stats["concepts"].get(c, 0) + 1

        if set(merged_tags) != set(existing_tags):
            stats["tagged"] += 1
            changes.append((fname, existing_tags, merged_tags, new_concepts))

            if not dry_run:
                new_fm = rebuild_frontmatter(fm_raw, merged_tags)
                new_content = "---" + new_fm + "\n---" + body
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)

    # Report
    mode = "DRY RUN" if dry_run else "APPLIED"
    print(f"\n=== Keyword Extraction Complete ({mode}) ===")
    print(f"  Scanned: {stats['scanned']} quotes")
    print(f"  Tagged/Updated: {stats['tagged']} quotes")
    print(f"\nConcept Distribution:")
    for concept, count in sorted(stats["concepts"].items(), key=lambda x: -x[1]):
        print(f"  {concept}: {count}")

    if dry_run and changes:
        print(f"\nSample changes (first 10):")
        for fname, old, new, concepts in changes[:10]:
            print(f"  {fname[:-3][:60]}")
            print(f"    + {', '.join(concepts)}")


if __name__ == "__main__":
    main()
