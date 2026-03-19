"""
Publish quotes that are ready: clean text, has source, readable filename.
Sets Edited: true and draft: false.

Usage: python scripts/publish-ready-quotes.py
"""

import os
import re

NOTES_DIR = os.path.join("content", "Wisdom Quotes")

READY_QUOTES = [
    "Both experience and experiencer will disappear.md",
    "By mercy is really meant not conceiving of a Buddha to be Enlightened.md",
    "God has His own plans and all these go on according to that.md",
    "Painful indeed is the process but later on everything becomes auspicious from beginning to end.md",
    "Su Tung-p'o wrote the follow  The roaring waterfall  is the Buddha's golden mouth.md",
    "There is only one God - the language, location, and system may be different_.md",
    "when dhyana becomes deep and firm it leads to sahaja sthiti.md",
]

count = 0
for fname in READY_QUOTES:
    filepath = os.path.join(NOTES_DIR, fname)
    if not os.path.exists(filepath):
        print(f"  NOT FOUND: {fname}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Set Edited: true
    content = re.sub(r'Edited:\s*false', 'Edited: true', content)
    # Set draft: false
    content = re.sub(r'draft:\s*true', 'draft: false', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    count += 1
    print(f"  Published: {fname[:-3]}")

print(f"\nPublished {count} quotes.")
