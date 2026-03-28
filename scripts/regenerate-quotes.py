#!/usr/bin/env python3
"""Regenerate randomquote.inline.ts from all published Wisdom Quotes."""

import os
import re

QUOTES_DIR = "content/Wisdom Quotes"
OUTPUT = "quartz/components/scripts/randomquote.inline.ts"

quotes = []

for fn in sorted(os.listdir(QUOTES_DIR)):
    if not fn.endswith(".md") or fn.startswith("_") or fn == "index.md":
        continue
    fp = os.path.join(QUOTES_DIR, fn)
    if not os.path.isfile(fp):
        continue

    with open(fp, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if "draft: false" not in content:
        continue
    if not content.startswith("---"):
        continue

    parts = content.split("---", 2)
    if len(parts) < 3:
        continue

    fm = parts[1]

    # Get source
    m = re.search(r'^source:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
    source_raw = m.group(1) if m else ""
    wl = re.search(r"\[\[(.+?)\]\]", source_raw)
    source = wl.group(1) if wl else source_raw.strip()

    stem = fn[:-3]
    slug = "Wisdom-Quotes/" + stem

    # Use the title for display text
    tm = re.search(r'^title:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
    text = tm.group(1).rstrip('"') if tm else stem

    quotes.append({"text": text, "source": source, "slug": slug})

print(f"Generated {len(quotes)} quotes from published content")

# Read the old file to preserve the JS logic after the array
with open(OUTPUT, "r", encoding="utf-8") as f:
    old = f.read()

# Find end of the array (the ] on its own line)
match = re.search(r"^]\s*$", old, re.MULTILINE)
if match:
    rest = old[match.end():]
else:
    rest = ""

# Build new array
lines = ["const quotes = ["]
for q in quotes:
    t = q["text"].replace("\\", "\\\\").replace('"', '\\"')
    s = q["source"].replace("\\", "\\\\").replace('"', '\\"')
    sl = q["slug"]
    lines.append(f'  {{ text: "{t}", source: "{s}", slug: "{sl}" }},')
lines.append("]")

output = "\n".join(lines) + rest

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Written {len(quotes)} quotes to {OUTPUT}")
