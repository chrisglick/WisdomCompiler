#!/bin/bash
# Review all Wisdom Quote files against design doc
# Outputs issues found for each file

DIR="content/Wisdom Quotes"
CHANGELOG="$DIR/changelog.md"

echo "# Wisdom Quotes Review Results"
echo "Date: $(date +%Y-%m-%d)"
echo ""

total=0
needs_rename=0
needs_edit=0
no_body=0
no_source=0
no_tags=0
not_edited=0
has_ocr_issues=0

for f in "$DIR"/*.md; do
  basename=$(basename "$f")

  # Skip design doc and changelog
  [[ "$basename" == "QUOTE-DESIGN-DOC.md" ]] && continue
  [[ "$basename" == "changelog.md" ]] && continue
  [[ "$basename" == "_screenshot_template.md" ]] && continue

  total=$((total + 1))
  issues=""

  # Check filename
  if echo "$basename" | grep -qE "^[0-9a-f]{8}-[0-9a-f]{4}|^[0-9]+__|^IMG_[0-9]"; then
    needs_rename=$((needs_rename + 1))
    issues="${issues}RENAME "
  fi

  # Check .txt.md
  if echo "$basename" | grep -q "\.txt\.md$"; then
    issues="${issues}DOUBLE_EXT "
  fi

  # Read file content
  content=$(cat "$f")

  # Check frontmatter
  edited=$(echo "$content" | grep -m1 "^Edited:" | sed 's/Edited: *//')
  source_val=$(echo "$content" | grep -m1 "^source:" | sed 's/source: *//')
  has_tags=$(echo "$content" | grep -c "^  - ")

  # Check Edited field
  if [[ "$edited" == "false" ]]; then
    not_edited=$((not_edited + 1))
    issues="${issues}NOT_EDITED "
  fi

  # Check source
  if [[ -z "$source_val" ]] || [[ "$source_val" == '""' ]]; then
    no_source=$((no_source + 1))
    issues="${issues}NO_SOURCE "
  fi

  # Check tags
  if [[ "$has_tags" -eq 0 ]]; then
    no_tags=$((no_tags + 1))
    issues="${issues}NO_TAGS "
  fi

  # Check body text (after frontmatter)
  body=$(echo "$content" | sed -n '/^---$/,/^---$/d; p' | sed '/^$/d' | grep -v '^\!\[' | head -1)
  if [[ -z "$body" ]]; then
    no_body=$((no_body + 1))
    issues="${issues}NO_BODY "
  fi

  # Check for draft
  if echo "$content" | grep -q "^draft: true"; then
    issues="${issues}DRAFT "
  fi

  # Check for text:: dataview field
  if echo "$content" | grep -q "^text::"; then
    issues="${issues}DATAVIEW_FIELD "
  fi

  # Check for Obsidian-only embed
  if echo "$content" | grep -q "^\!\[\["; then
    issues="${issues}OBSIDIAN_EMBED "
  fi

  if [[ -n "$issues" ]]; then
    needs_edit=$((needs_edit + 1))
    echo "FILE: $basename"
    echo "  ISSUES: $issues"
    echo ""
  fi
done

echo "=== SUMMARY ==="
echo "Total files: $total"
echo "Need rename: $needs_rename"
echo "Need edit: $needs_edit"
echo "No body text: $no_body"
echo "No source: $no_source"
echo "No tags: $no_tags"
echo "Not edited: $not_edited"
