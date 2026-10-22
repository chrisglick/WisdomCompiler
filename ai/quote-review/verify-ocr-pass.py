"""verify-ocr-pass.py — deterministic backstop after an agent OCR pass.

Usage (from repo root):
    python -I ai/quote-review/verify-ocr-pass.py <worklist.json> [note.md ...]

worklist.json is the list written BEFORE the pass (see ai/reviews/2026-10-21-ocr-worklist.json);
its `draft` field is what each note's `draft:` line must still equal. With no note names it
checks every file in the worklist. Exit code 1 when any PROBLEM is printed.
Checks: BOM, frontmatter present, curly quotes in frontmatter, draft line unchanged, YAML parses,
tags in vocab, Edited:true implies wikilink source and no needs-* flag, non-empty body, OCR garbage.
"""
import os,re,json,sys,glob
here=os.path.dirname(os.path.abspath(__file__))
root=os.path.join(here,"..","..","content","Wisdom Quotes")
if len(sys.argv)<2: sys.exit(__doc__)
wl={i["file"]:i for i in json.load(open(sys.argv[1],encoding="utf-8"))}
sys.argv=[sys.argv[0]]+sys.argv[2:]
vocab=set("nature-creation mind divine guru-teacher knowledge-wisdom love-devotion consciousness service meditation self-knowledge suffering liberation silence death-impermanence ego scripture faith-trust surrender non-duality detachment humility needs-review needs-manual-review needs-source".split())
try:
    import yaml
except ImportError:
    yaml=None
files=sys.argv[1:] or list(wl)
probs=[];summary={}
for f in files:
    p=os.path.join(root,f); raw=open(p,"rb").read()
    if raw.startswith(b"\xef\xbb\xbf"): probs.append((f,"BOM"))
    txt=raw.decode("utf-8","replace")
    m=re.match(r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n?(.*)$",txt,re.S)
    if not m: probs.append((f,"NO FRONTMATTER")); continue
    fm,body=m.groups()
    if re.search(r"[\u201c\u201d\u2018\u2019]",fm): probs.append((f,"curly quotes in frontmatter"))
    d=re.search(r"^draft:\s*(.*)$",fm,re.M); d=d.group(1).strip() if d else None
    if d!=wl[f]["draft"]: probs.append((f,f"DRAFT CHANGED {wl[f]['draft']!r}->{d!r}"))
    if yaml:
        try: data=yaml.safe_load(fm) or {}
        except Exception as e: probs.append((f,f"YAML error {str(e)[:60]}")); data={}
        tags=data.get("tags") or []
        if isinstance(tags,str): tags=[tags]
        bad=[t for t in tags if t not in vocab]
        if bad: probs.append((f,f"non-vocab tags {bad}"))
        ed=str(data.get("Edited")).lower(); src=str(data.get("source") or "")
        if ed=="true" and ("needs-review" in tags or "needs-manual-review" in tags): probs.append((f,"Edited:true but still flagged"))
        if ed=="true" and not re.match(r"^\[\[.+\]\]$",src): probs.append((f,f"Edited:true without wikilink source ({src!r})"))
        for k in ("source","title","Page"):
            v=data.get(k)
        flag=next((t for t in tags if t.startswith("needs-")),"clean" if ed=="true" else "edited-false-unflagged")
        summary[flag]=summary.get(flag,0)+1
    if len(body.strip())<10: probs.append((f,"empty body"))
    if re.search(r"\b(aq[13t]|ayi|Suy)\b",body): probs.append((f,"looks like OCR garbage still"))
print("checked",len(files)); print("flags:",summary)
for f,msg in probs: print("PROBLEM",f,"|",msg)
print("problems:",len(probs)); sys.exit(1 if probs else 0)
