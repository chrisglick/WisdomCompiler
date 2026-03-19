"""
Audit all wisdom quotes for quality issues.

Scans content/Wisdom Quotes/ and categorizes every quote by:
- Publication status (edited vs draft)
- Attribution status (has source vs empty)
- Text quality (clean vs OCR artifacts, fragments, truncation)
- Filename quality (human-readable vs UUID vs photo ID)

Outputs a comprehensive report to production/ai/quote-audit-report.md

Usage: python scripts/audit-quotes.py
"""

import os
import re
from collections import defaultdict

NOTES_DIR = os.path.join("content", "Wisdom Quotes")
OUTPUT_DIR = os.path.join("production", "ai")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "quote-audit-report.md")

# Filename patterns
UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    re.IGNORECASE
)
PHOTO_ID_PATTERN = re.compile(r'^\d{10,}')
IMG_PATTERN = re.compile(r'^IMG_', re.IGNORECASE)

# Text quality patterns
PAGE_NUMBER_PATTERN = re.compile(r'^\s*(xvi|xvii|xviii|xix|xx|xxi|[ivxlc]+)\s*$', re.IGNORECASE | re.MULTILINE)
ALL_CAPS_PATTERN = re.compile(r'\b[A-Z]{5,}\b')
ORPHAN_NUMBER_PATTERN = re.compile(r'^\s*\d{1,4}\s*$', re.MULTILINE)


def parse_frontmatter(filepath):
    """Extract frontmatter fields from a markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, OSError):
        return None, ""

    if not content.startswith("---"):
        return None, content

    end = content.find("---", 3)
    if end == -1:
        return None, content

    fm_text = content[3:end].strip()
    body = content[end + 3:].strip()

    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val

    return fm, body


def extract_source(fm):
    """Extract clean source name from frontmatter."""
    source = fm.get("source", "")
    source = re.sub(r'\[\[([^\]]+)\]\]', r'\1', source)
    return source.strip()


def get_body_text(body):
    """Extract readable text from body, stripping images and markdown."""
    # Remove image embeds
    text = re.sub(r'!\[.*?\]\(.*?\)', '', body)
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove markdown formatting
    text = re.sub(r'[*_#>`~]', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def classify_filename(fname):
    """Classify filename quality."""
    raw = fname[:-3]  # strip .md
    if UUID_PATTERN.match(raw):
        return "uuid"
    if PHOTO_ID_PATTERN.match(raw):
        return "photo_id"
    if IMG_PATTERN.match(raw):
        return "img_prefix"
    if raw in ("index", "Screenshots"):
        return "system"
    if raw.startswith("_"):
        return "template"
    return "readable"


def detect_issues(body_text, fname):
    """Detect quality issues in quote text."""
    issues = []

    if len(body_text) < 15:
        issues.append("very_short")
    elif len(body_text) < 30:
        issues.append("short")

    if len(body_text) > 2000:
        issues.append("very_long")

    # Truncation indicators
    if body_text and not body_text[-1] in '.!?"\u2019\u201d)':
        # Doesn't end with sentence-ending punctuation
        if len(body_text) > 20:
            issues.append("possible_truncation")

    # Page number artifacts
    if PAGE_NUMBER_PATTERN.search(body_text):
        issues.append("page_number_artifact")

    if ORPHAN_NUMBER_PATTERN.search(body_text):
        issues.append("orphan_number")

    # Excessive caps (OCR headers/artifacts)
    caps_words = ALL_CAPS_PATTERN.findall(body_text)
    if len(caps_words) > 3:
        issues.append("excessive_caps")

    # Starts with lowercase (fragment)
    if body_text and body_text[0].islower():
        issues.append("starts_lowercase")

    # Contains common OCR artifacts
    if re.search(r'[|}{\\]', body_text):
        issues.append("ocr_artifacts")

    # Hyphenated line breaks from OCR
    if re.search(r'\w-\s+\w', body_text):
        issues.append("hyphenated_breaks")

    return issues


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    stats = {
        "total": 0,
        "published": 0,
        "draft": 0,
        "has_source": 0,
        "no_source": 0,
        "filename_types": defaultdict(int),
        "issues": defaultdict(int),
    }

    # Categories for the report
    ready_to_publish = []      # Draft but clean, just needs review
    needs_text_fix = []        # Has issues that can be scripted
    needs_attribution = []     # Clean text but no source
    needs_manual_review = []   # Multiple issues, needs human
    published_with_issues = [] # Already published but has problems
    system_files = []          # Templates, index, etc.

    for fname in sorted(os.listdir(NOTES_DIR)):
        if not fname.endswith(".md"):
            continue

        filepath = os.path.join(NOTES_DIR, fname)
        fm, body = parse_frontmatter(filepath)

        if fm is None:
            continue

        filename_type = classify_filename(fname)
        stats["filename_types"][filename_type] += 1

        if filename_type in ("system", "template"):
            system_files.append(fname)
            continue

        stats["total"] += 1

        is_edited = fm.get("Edited", "").lower() == "true"
        is_draft = fm.get("draft", "").lower() == "true"
        source = extract_source(fm)
        has_source = bool(source)
        body_text = get_body_text(body)
        issues = detect_issues(body_text, fname)

        if is_edited and not is_draft:
            stats["published"] += 1
        else:
            stats["draft"] += 1

        if has_source:
            stats["has_source"] += 1
        else:
            stats["no_source"] += 1

        for issue in issues:
            stats["issues"][issue] += 1

        entry = {
            "fname": fname,
            "source": source,
            "filename_type": filename_type,
            "text_preview": body_text[:120] + "..." if len(body_text) > 120 else body_text,
            "text_length": len(body_text),
            "issues": issues,
            "is_edited": is_edited,
            "is_draft": is_draft,
        }

        if is_edited and not is_draft:
            if issues:
                published_with_issues.append(entry)
        elif not issues and has_source and filename_type == "readable":
            ready_to_publish.append(entry)
        elif not has_source and not issues:
            needs_attribution.append(entry)
        elif len(issues) <= 2:
            needs_text_fix.append(entry)
        else:
            needs_manual_review.append(entry)

    # Generate report
    lines = []
    lines.append("# WisdomCompiler Quote Audit Report")
    lines.append(f"\n*Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    lines.append("## Summary\n")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total quotes (excluding system files) | {stats['total']} |")
    lines.append(f"| Published (Edited: true, draft: false) | {stats['published']} |")
    lines.append(f"| Drafts | {stats['draft']} |")
    lines.append(f"| With source attribution | {stats['has_source']} |")
    lines.append(f"| Missing source | {stats['no_source']} |")
    lines.append("")

    lines.append("### Filename Types\n")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for ftype, count in sorted(stats["filename_types"].items(), key=lambda x: -x[1]):
        lines.append(f"| {ftype} | {count} |")
    lines.append("")

    lines.append("### Issue Frequency\n")
    lines.append("| Issue | Count |")
    lines.append("|-------|-------|")
    for issue, count in sorted(stats["issues"].items(), key=lambda x: -x[1]):
        lines.append(f"| {issue} | {count} |")
    lines.append("")

    # Triage categories
    lines.append("---\n")
    lines.append("## Triage Categories\n")

    lines.append(f"### 1. Ready to Publish ({len(ready_to_publish)} quotes)")
    lines.append("*Clean text, has attribution, readable filename — just needs Edited: true*\n")
    for entry in ready_to_publish[:30]:
        lines.append(f"- **{entry['fname'][:-3]}** — *{entry['source']}*")
    if len(ready_to_publish) > 30:
        lines.append(f"\n*... and {len(ready_to_publish) - 30} more*\n")
    lines.append("")

    lines.append(f"### 2. Needs Text Fix ({len(needs_text_fix)} quotes)")
    lines.append("*1-2 issues that can likely be automated or quickly fixed*\n")
    for entry in needs_text_fix[:30]:
        issue_str = ", ".join(entry["issues"])
        lines.append(f"- **{entry['fname'][:-3]}** [{issue_str}]")
        lines.append(f"  > {entry['text_preview']}")
    if len(needs_text_fix) > 30:
        lines.append(f"\n*... and {len(needs_text_fix) - 30} more*\n")
    lines.append("")

    lines.append(f"### 3. Needs Attribution ({len(needs_attribution)} quotes)")
    lines.append("*Clean text but source is empty — needs research*\n")
    for entry in needs_attribution[:30]:
        lines.append(f"- **{entry['fname'][:-3]}**")
        lines.append(f"  > {entry['text_preview']}")
    if len(needs_attribution) > 30:
        lines.append(f"\n*... and {len(needs_attribution) - 30} more*\n")
    lines.append("")

    lines.append(f"### 4. Needs Manual Review ({len(needs_manual_review)} quotes)")
    lines.append("*Multiple issues — requires human judgment*\n")
    for entry in needs_manual_review[:30]:
        issue_str = ", ".join(entry["issues"])
        src = f" — *{entry['source']}*" if entry["source"] else ""
        lines.append(f"- **{entry['fname'][:-3]}** [{issue_str}]{src}")
        lines.append(f"  > {entry['text_preview']}")
    if len(needs_manual_review) > 30:
        lines.append(f"\n*... and {len(needs_manual_review) - 30} more*\n")
    lines.append("")

    lines.append(f"### 5. Published with Issues ({len(published_with_issues)} quotes)")
    lines.append("*Already live but has detected quality issues*\n")
    for entry in published_with_issues:
        issue_str = ", ".join(entry["issues"])
        lines.append(f"- **{entry['fname'][:-3]}** [{issue_str}] — *{entry['source']}*")
        lines.append(f"  > {entry['text_preview']}")
    lines.append("")

    lines.append("---\n")
    lines.append("## Recommended Action Plan\n")
    lines.append(f"1. **Quick wins:** Publish the {len(ready_to_publish)} ready-to-publish quotes (set `Edited: true`, `draft: false`)")
    lines.append(f"2. **Automated fixes:** Script repairs for the {len(needs_text_fix)} quotes with minor issues")
    lines.append(f"3. **Attribution research:** Research sources for {len(needs_attribution)} unattributed but clean quotes")
    lines.append(f"4. **Manual review:** Curate the {len(needs_manual_review)} quotes needing human judgment")
    lines.append(f"5. **Published QA:** Fix the {len(published_with_issues)} already-published quotes with detected issues")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nAudit complete!")
    print(f"  Total quotes: {stats['total']}")
    print(f"  Published: {stats['published']}")
    print(f"  Drafts: {stats['draft']}")
    print(f"  With source: {stats['has_source']}")
    print(f"  Missing source: {stats['no_source']}")
    print(f"  Ready to publish: {len(ready_to_publish)}")
    print(f"  Needs text fix: {len(needs_text_fix)}")
    print(f"  Needs attribution: {len(needs_attribution)}")
    print(f"  Needs manual review: {len(needs_manual_review)}")
    print(f"  Published with issues: {len(published_with_issues)}")
    print(f"\nReport written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
