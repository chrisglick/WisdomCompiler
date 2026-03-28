"""
Set draft: true on the 21 identified bad quote files.
Only changes the draft flag in frontmatter — no body content modified.
"""

import os
import re

QUOTES_DIR = os.path.join("content", "Wisdom Quotes")

BAD_FILES = [
    "All is One.md",
    "Becoming a reminder of human foolishness.md",
    "Before its birth it does not exist nor does it continue after death.md",
    "Bhagavans silence was his direct teaching he taught Self Enquiry to those who could not comprehend.md",
    "Crying is an act of atonement.md",
    "For those who are attached to the unreal identification with the body continues.md",
    "How did the Self that ever is Awareness bliss behave as if It had forgotten.md",
    "I am so small.md",
    "I feel so alone.md",
    "IMG_1292.md",
    "IMG_1293.md",
    "If the mind is turned inwards God manifests as inner consciousness.md",
    "Image Avalokateshvara Gantz.md",
    "Just as you would not identify yourself with your shadow.md",
    "Sai Baba teachings on devotion and surrender.md",
    "Self-negation and ultimate truth.md",
    "The body is a product of food it constitutes the material sheath.md",
    "The jnani sees no one as an ajnani.md",
    "There is no bondage no liberation no aspirant no seeker.md",
    "They are reading the four Vedas and you are doing Vedanta.md",
    "We capitulate to sleep but the Self is still there.md",
]

def set_draft_true(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Replace draft: false with draft: true
    new_content = re.sub(r'draft:\s*false', 'draft: true', content, count=1)

    if new_content == content:
        # If no draft: false found, check if draft: true already
        if 'draft: true' in content:
            return "already_draft"
        return "no_draft_field"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return "drafted"

count = 0
for filename in BAD_FILES:
    filepath = os.path.join(QUOTES_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  MISSING: {filename}")
        continue
    result = set_draft_true(filepath)
    print(f"  {result}: {filename}")
    if result == "drafted":
        count += 1

print(f"\nDrafted {count} files out of {len(BAD_FILES)}")
