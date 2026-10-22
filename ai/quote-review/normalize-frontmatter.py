#!/usr/bin/env python
"""Backstop: convert curly/typographic quotes to straight ASCII INSIDE frontmatter only.
Body text is left untouched (smart quotes there are desirable)."""
import glob, os
WQ = os.path.join("content", "Wisdom Quotes")
TRANS = {'“':'"','”':'"','‘':"'",'’':"'"}
def fix(s):
    for k,v in TRANS.items(): s=s.replace(k,v)
    return s
changed=0; scanned=0
for f in glob.glob(os.path.join(WQ,"*.md")):
    n=os.path.basename(f)
    if n=="index.md": continue
    scanned+=1
    t=open(f,encoding="utf-8").read()
    if not t.startswith("---"): continue
    end=t.find("\n---", 3)
    if end==-1: continue
    fm=t[:end]; rest=t[end:]
    nfm=fix(fm)
    if nfm!=fm:
        open(f,"w",encoding="utf-8").write(nfm+rest)
        changed+=1
print(f"normalizer: scanned {scanned}, fixed frontmatter curly-quotes in {changed} files")
