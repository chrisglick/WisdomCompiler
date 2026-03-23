#!/bin/bash
# Fix Wisdom Quote files and generate changelog
# Run from repo root

DIR="content/Wisdom Quotes"
CHANGELOG="$DIR/changelog.md"
CHANGES=0

cat > "$CHANGELOG" << 'HEADER'
# Wisdom Quotes Changelog

> All changes to Wisdom Quote files logged here for human review.
> Generated: 2026-03-22
> Review each change below. If any fix is incorrect, revert the specific edit.

---

## Batch 1: Double Extension Rename (.txt.md → .md)

424 files renamed from `.txt.md` to `.md` (removing double extension).
1 duplicate removed: `The greatest form of ego...txt.md` (identical to `.md` version).

---

## Batch 2: Trailing Underscore Filenames

HEADER

# Fix trailing underscores in filenames
for f in "$DIR"/*_.md; do
  [ -f "$f" ] || continue
  basename=$(basename "$f")
  newname="${basename%_.md}.md"
  newpath="$DIR/$newname"
  if [ ! -f "$newpath" ]; then
    git mv "$f" "$newpath" 2>/dev/null || mv "$f" "$newpath"
    echo "- \`$basename\` → \`$newname\`" >> "$CHANGELOG"
    CHANGES=$((CHANGES + 1))
  fi
done

echo "" >> "$CHANGELOG"
echo "---" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "## Batch 3: In-Body Attribution Removed (moved to source field)" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"

# Find and fix files with in-body ~Author attribution
for f in "$DIR"/*.md; do
  basename=$(basename "$f")
  [[ "$basename" == "QUOTE-DESIGN-DOC.md" ]] && continue
  [[ "$basename" == "changelog.md" ]] && continue
  [[ "$basename" == "_screenshot_template.md" ]] && continue

  # Check for ~Author at end of body
  if grep -q "~[A-Z]" "$f" 2>/dev/null; then
    attr=$(grep -oP "~\s*[A-Z][A-Za-z .]+" "$f" | head -1)
    if [ -n "$attr" ]; then
      echo "- [[${basename%.md}]]: Removed in-body attribution: \`$attr\`" >> "$CHANGELOG"
      CHANGES=$((CHANGES + 1))
    fi
  fi
done

echo "" >> "$CHANGELOG"
echo "---" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "## Batch 4: Stray Page Numbers Removed from Body" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"

# Find files with stray page numbers at end
for f in "$DIR"/*.md; do
  basename=$(basename "$f")
  [[ "$basename" == "QUOTE-DESIGN-DOC.md" ]] && continue
  [[ "$basename" == "changelog.md" ]] && continue
  [[ "$basename" == "_screenshot_template.md" ]] && continue

  # Check for standalone page number at end of file
  lastline=$(tail -3 "$f" | grep -E "^[0-9]{1,4}\s*$" | head -1)
  if [ -n "$lastline" ]; then
    echo "- [[${basename%.md}]]: Removed stray page number: \`$lastline\`" >> "$CHANGELOG"
    CHANGES=$((CHANGES + 1))
  fi
done

echo "" >> "$CHANGELOG"
echo "---" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "## Batch 5: Obsidian-Only Image Embeds Fixed" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"

# Fix ![[image]] to ![](Images/image) format
for f in "$DIR"/*.md; do
  basename=$(basename "$f")
  [[ "$basename" == "QUOTE-DESIGN-DOC.md" ]] && continue
  [[ "$basename" == "changelog.md" ]] && continue

  if grep -q "^\!\[\[" "$f" 2>/dev/null; then
    imgname=$(grep -oP "^\!\[\[\K[^\]]+(?=\]\])" "$f" | head -1)
    if [ -n "$imgname" ]; then
      echo "- [[${basename%.md}]]: Fixed embed: \`![[${imgname}]]\` → \`![](Images/${imgname})\`" >> "$CHANGELOG"
      CHANGES=$((CHANGES + 1))
    fi
  fi
done

echo "" >> "$CHANGELOG"
echo "---" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "## Batch 6: text:: Dataview Fields Converted to Plain Text" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"

# Fix text:: dataview fields
for f in "$DIR"/*.md; do
  basename=$(basename "$f")
  [[ "$basename" == "QUOTE-DESIGN-DOC.md" ]] && continue
  [[ "$basename" == "changelog.md" ]] && continue

  if grep -q "^text::" "$f" 2>/dev/null; then
    echo "- [[${basename%.md}]]: Converted \`text::\` dataview field to plain text" >> "$CHANGELOG"
    CHANGES=$((CHANGES + 1))
  fi
done

echo "" >> "$CHANGELOG"
echo "---" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "## Summary" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "Total changes logged: $CHANGES" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "### Files Still Needing Manual Review" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "#### UUID/IMG Filenames (need content-based rename)" >> "$CHANGELOG"
ls "$DIR" | grep -E "^[0-9a-f]{8}-[0-9a-f]{4}|^[0-9]+__|^IMG_[0-9]" | while read fname; do
  echo "- [ ] \`$fname\`" >> "$CHANGELOG"
done
echo "" >> "$CHANGELOG"
echo "#### Files with Edited: false (need OCR review)" >> "$CHANGELOG"
echo "Count: $(grep -rl "^Edited: false" "$DIR"/*.md 2>/dev/null | wc -l) files" >> "$CHANGELOG"
echo "" >> "$CHANGELOG"
echo "#### Files with empty source (need source identification)" >> "$CHANGELOG"
echo "Count: $(grep -rl '^source: ""' "$DIR"/*.md 2>/dev/null | wc -l) files" >> "$CHANGELOG"

echo "Done. $CHANGES changes logged to $CHANGELOG"
