"""
Revert Edited: true → Edited: false on files where the body content
was NOT actually edited in the batch. Uses git diff to determine which
files had BODY changes vs only FRONTMATTER changes.

Logic:
- If git diff shows body content changes (not just frontmatter lines) → keep Edited: true
- If git diff shows ONLY frontmatter changes → revert to Edited: false
- Files already Edited: false or draft: true → skip

Additionally, any file with Edited: false that was set to draft: false
should be reverted to draft: true (unedited files should not be published).
"""

import os
import re
import subprocess
import sys

QUOTES_DIR = os.path.join("content", "Wisdom Quotes")
DRY_RUN = "--dry-run" in sys.argv

# The commit where the batch edit happened — compare against parent
# Our batch commit is e788f13, its parent is d959002
BATCH_COMMIT = "e788f13"
PARENT_COMMIT = "d959002"


def get_body_diff(filepath):
    """Check if the file had body content changes (not just frontmatter) in the batch commit."""
    try:
        result = subprocess.run(
            ["git", "diff", f"{PARENT_COMMIT}..{BATCH_COMMIT}", "--", filepath],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        diff = result.stdout
    except Exception:
        return False, "error"

    if not diff:
        return False, "no_diff"

    # Parse diff to separate frontmatter changes from body changes
    in_frontmatter = False
    body_adds = 0
    body_removes = 0
    frontmatter_only = True

    for line in diff.split('\n'):
        if line.startswith('@@'):
            continue
        if line.startswith('+++') or line.startswith('---'):
            continue

        # Track frontmatter boundaries
        stripped = line[1:].strip() if len(line) > 1 else ''
        if stripped == '---':
            in_frontmatter = not in_frontmatter
            continue

        if line.startswith('+') or line.startswith('-'):
            content = line[1:]
            # Check if this is a frontmatter-only change
            if in_frontmatter or content.strip() == '':
                continue  # frontmatter change or blank line

            # Known frontmatter fields that might appear
            fm_fields = ['Edited:', 'draft:', 'source:', 'tags:', 'ShowImage:',
                         'Page:', 'image_name:', 'Source Type:', 'sticker:',
                         'title:', 'Author:']
            if any(content.strip().startswith(f) for f in fm_fields):
                continue

            # This is a body content change
            if line.startswith('+'):
                body_adds += 1
            else:
                body_removes += 1
            frontmatter_only = False

    if frontmatter_only:
        return False, f"frontmatter_only"
    else:
        return True, f"body_edited (+{body_adds}/-{body_removes} lines)"


def parse_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    if not content.startswith('---'):
        return {}
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}
    fm = {}
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            fm[key.strip()] = val.strip().strip('"')
    return fm


def set_edited_false(filepath):
    """Set Edited: false (keep draft status as-is)."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    content = re.sub(r'Edited:\s*true', 'Edited: false', content, count=1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def set_draft_true(filepath):
    """Set draft: true."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    new = re.sub(r'draft:\s*false', 'draft: true', content, count=1)
    if new != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new)
        return True
    return False


def main():
    truly_edited = []
    falsely_edited = []
    already_correct = 0
    already_draft = 0
    new_file = 0

    for filename in sorted(os.listdir(QUOTES_DIR)):
        if not filename.endswith('.md') or filename.startswith('_') or filename == 'index.md':
            continue

        filepath = os.path.join(QUOTES_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        fm = parse_frontmatter(filepath)
        edited = fm.get('Edited', '')
        draft = fm.get('draft', '')

        # Skip files already Edited: false
        if edited != 'true':
            already_correct += 1
            continue

        # Skip files already draft: true
        if draft == 'true':
            already_draft += 1
            continue

        # Check git diff for body changes
        had_body_edit, detail = get_body_diff(filepath)

        if detail == "no_diff":
            # File was renamed (not content-changed) in the batch commit
            # But it might have been modified in working tree before commit
            # These are likely false Edited: true
            falsely_edited.append((filename, "no_body_diff_in_batch"))
        elif had_body_edit:
            truly_edited.append((filename, detail))
        else:
            falsely_edited.append((filename, detail))

    print(f"\n=== RESULTS ===")
    print(f"Truly edited (body changed in batch): {len(truly_edited)}")
    print(f"Falsely edited (frontmatter-only): {len(falsely_edited)}")
    print(f"Already Edited:false: {already_correct}")
    print(f"Already draft:true: {already_draft}")

    print(f"\n=== TRULY EDITED (keep Edited:true) ===\n")
    for fn, detail in truly_edited[:10]:
        print(f"  {fn} — {detail}")
    if len(truly_edited) > 10:
        print(f"  ... and {len(truly_edited) - 10} more")

    print(f"\n=== FALSELY EDITED (revert Edited→false, draft→true) ===\n")
    for fn, detail in falsely_edited[:10]:
        print(f"  {fn} — {detail}")
    if len(falsely_edited) > 10:
        print(f"  ... and {len(falsely_edited) - 10} more")

    if not DRY_RUN:
        print(f"\n=== APPLYING ===\n")
        revert_count = 0
        draft_count = 0
        for fn, _ in falsely_edited:
            fp = os.path.join(QUOTES_DIR, fn)
            set_edited_false(fp)
            drafted = set_draft_true(fp)
            revert_count += 1
            if drafted:
                draft_count += 1
            print(f"  REVERTED: {fn}")
        print(f"\nReverted {revert_count} files (Edited→false), drafted {draft_count}")
    else:
        print(f"\n[DRY RUN] Would revert {len(falsely_edited)} files")

    # Save report
    with open("ai/research/edited-flag-audit-20260323.md", "w", encoding="utf-8") as f:
        f.write(f"# Edited Flag Audit — 2026-03-23\n\n")
        f.write(f"## Method\n")
        f.write(f"Used git diff between {PARENT_COMMIT} and {BATCH_COMMIT} to determine\n")
        f.write(f"which files had body content changes vs frontmatter-only changes.\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Truly edited (body changed): {len(truly_edited)}\n")
        f.write(f"- Falsely edited (frontmatter-only): {len(falsely_edited)}\n\n")
        f.write(f"## Truly Edited ({len(truly_edited)})\n\n")
        for fn, detail in truly_edited:
            f.write(f"- {fn} — {detail}\n")
        f.write(f"\n## Falsely Edited ({len(falsely_edited)})\n\n")
        for fn, detail in falsely_edited:
            f.write(f"- {fn} — {detail}\n")


if __name__ == "__main__":
    main()
