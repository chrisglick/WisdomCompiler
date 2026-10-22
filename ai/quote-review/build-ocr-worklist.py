"""build-ocr-worklist.py — list the quote notes that still carry a review flag.

Usage (from repo root):
    python -I ai/quote-review/build-ocr-worklist.py [out.json] [--tags needs-review,needs-manual-review]

Writes a JSON array, one object per flagged note:
  file, image, image_exists, edited, draft, source, tier, body_len, title
`draft` is recorded verbatim so verify-ocr-pass.py can prove no agent changed it.
Default tags: needs-review, needs-manual-review, needs-source. tier = the first flag found.
"""
import json, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, "..", "..", "content", "Wisdom Quotes")
args = sys.argv[1:]
tags = "needs-review,needs-manual-review,needs-source"
if "--tags" in args:
    i = args.index("--tags"); tags = args[i + 1]; del args[i:i + 2]
out = args[0] if args else None
wanted = [t.strip() for t in tags.split(",") if t.strip()]

def fm_value(fm, key):
    m = re.search(r"^%s:\s*(.*)$" % re.escape(key), fm, re.M)
    return m.group(1).strip() if m else None

rows = []
for name in sorted(os.listdir(root)):
    if not name.endswith(".md"):
        continue
    txt = open(os.path.join(root, name), "rb").read().decode("utf-8", "replace")
    m = re.match(r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n?(.*)$", txt, re.S)
    if not m:
        continue
    fm, body = m.groups()
    flags = [t for t in wanted
             if re.search(r"(^\s*-\s*[\"']?%s[\"']?\s*$)|([\[,]\s*[\"']?%s[\"']?\s*[\],])" % (t, t), fm, re.M)]
    if not flags:
        continue
    img = (fm_value(fm, "image_name") or "").strip('"\'')
    rows.append({
        "file": name,
        "image": img,
        "image_exists": bool(img) and os.path.exists(os.path.join(root, "Images", img)),
        "edited": (fm_value(fm, "Edited") or "").lower() or None,
        "draft": fm_value(fm, "draft"),
        "source": fm_value(fm, "source"),
        "tier": flags[0].replace("needs-", ""),
        "body_len": len(body.strip()),
        "title": fm_value(fm, "title"),
    })

data = json.dumps(rows, indent=1, ensure_ascii=False)
if out:
    open(out, "w", encoding="utf-8", newline="\n").write(data)
    print("wrote", out)
from collections import Counter
print(len(rows), "flagged notes;", dict(Counter(r["tier"] for r in rows)))
