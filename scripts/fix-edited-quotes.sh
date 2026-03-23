#!/bin/bash
# Fix edited Wisdom Quote files against design doc
# Applies actual content fixes and logs to changelog

DIR="content/Wisdom Quotes"
CHANGELOG="$DIR/changelog.md"
FIXES=0
REVIEWED=0

# Append new batch to changelog
cat >> "$CHANGELOG" << 'HEADER'

---

## Batch 7: Edited File Content Fixes (automated)

Fixes applied to files with `Edited: true` during sequential design doc review.

HEADER

while IFS= read -r filepath; do
  basename=$(basename "$filepath")

  # Skip meta files
  [[ "$basename" == "QUOTE-DESIGN-DOC.md" ]] && continue
  [[ "$basename" == "changelog.md" ]] && continue
  [[ "$basename" == "_screenshot_template.md" ]] && continue

  REVIEWED=$((REVIEWED + 1))
  file_fixes=""

  content=$(cat "$filepath")

  # === FIX 1: Obsidian-only image embeds ===
  if grep -q '^\!\[\[' "$filepath" 2>/dev/null; then
    # Replace ![[image]] with ![](Images/image)
    sed -i 's/^\!\[\[\([^]]*\)\]\]/\!\[\](Images\/\1)/' "$filepath"
    file_fixes="${file_fixes}  - Fixed Obsidian embed → web-compatible format\n"
  fi

  # === FIX 2: text:: dataview field ===
  if grep -q '^text::' "$filepath" 2>/dev/null; then
    sed -i 's/^text:://' "$filepath"
    file_fixes="${file_fixes}  - Removed \`text::\` dataview prefix\n"
  fi

  # === FIX 3: Trailing whitespace cleanup ===
  # Remove trailing spaces from non-empty lines in body

  # === FIX 4: Empty ShowImage field ===
  if grep -q '^ShowImage:$' "$filepath" 2>/dev/null; then
    sed -i 's/^ShowImage:$/ShowImage: false/' "$filepath"
    file_fixes="${file_fixes}  - Set empty \`ShowImage:\` to \`false\`\n"
  fi

  # === FIX 5: Empty Source Type field normalization ===
  if grep -q '^Source Type: $' "$filepath" 2>/dev/null; then
    sed -i 's/^Source Type: $/Source Type:/' "$filepath"
    file_fixes="${file_fixes}  - Normalized empty \`Source Type\` field\n"
  fi

  # === FIX 6: Inconsistent tag formatting ===
  # Check for tags: [] (empty array) vs tags: with list items

  # === FIX 7: Body text OCR common fixes ===
  body=$(sed -n '/^---$/,/^---$/!p' "$filepath")

  # Fix common OCR issues in body text
  if echo "$body" | grep -q "itselfis"; then
    sed -i 's/itselfis/itself is/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`itselfis\` → \`itself is\`\n"
  fi

  if echo "$body" | grep -q "Ifany"; then
    sed -i 's/Ifany/If any/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`Ifany\` → \`If any\`\n"
  fi

  if echo "$body" | grep -q "cannotbe"; then
    sed -i 's/cannotbe/cannot be/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`cannotbe\` → \`cannot be\`\n"
  fi

  if echo "$body" | grep -q "doesnot"; then
    sed -i 's/doesnot/does not/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`doesnot\` → \`does not\`\n"
  fi

  if echo "$body" | grep -q "willnot"; then
    sed -i 's/willnot/will not/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`willnot\` → \`will not\`\n"
  fi

  if echo "$body" | grep -q "ofthe"; then
    sed -i 's/ofthe/of the/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`ofthe\` → \`of the\`\n"
  fi

  if echo "$body" | grep -q "inthe"; then
    sed -i 's/inthe/in the/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`inthe\` → \`in the\`\n"
  fi

  if echo "$body" | grep -q "isthe"; then
    sed -i 's/isthe/is the/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`isthe\` → \`is the\`\n"
  fi

  if echo "$body" | grep -q "tothe"; then
    sed -i 's/tothe/to the/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`tothe\` → \`to the\`\n"
  fi

  if echo "$body" | grep -q "andthe"; then
    sed -i 's/andthe/and the/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed OCR: \`andthe\` → \`and the\`\n"
  fi

  if echo "$body" | grep -q " ,"; then
    sed -i 's/ ,/,/g' "$filepath"
    file_fixes="${file_fixes}  - Fixed spacing: removed space before comma\n"
  fi

  # Log if any fixes were made
  if [ -n "$file_fixes" ]; then
    FIXES=$((FIXES + 1))
    echo "- [[${basename%.md}]]:" >> "$CHANGELOG"
    echo -e "$file_fixes" >> "$CHANGELOG"
  fi

done < /tmp/edited-files.txt

echo "" >> "$CHANGELOG"
echo "**Reviewed:** $REVIEWED files | **Fixed:** $FIXES files" >> "$CHANGELOG"

echo "Reviewed: $REVIEWED files"
echo "Fixed: $FIXES files"
