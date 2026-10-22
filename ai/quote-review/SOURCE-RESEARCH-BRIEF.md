<!-- Copied from the 2026-10-21 session scratchpad. CANON.md referred to below = the Canonical BOOKS / TEACHERS lists in EDIT-RULES.md (or ai/quote-review/vocab.json); regenerate it from there. Results of the run: ai/reviews/2026-10-21-source-research.{md,json}. -->

# Source-research brief (2026-10-21) — RESEARCH ONLY, EDIT NOTHING

You identify the origin of short spiritual/philosophical passages whose source is unknown. You NEVER edit any file in the repository. You write exactly one JSON report file at the path given in your task.

Input: your batch JSON (array of notes: file, title, body (the passage text, transcribed from a photographed page or screen), image, page). Canonical source names (books and teachers already in the site) are in CANON.md beside your batch.

For each note:
1. Pick 1–3 distinctive phrases from the body (6–12 words, exact, in double quotes) and web-search them with the WebSearch tool. Try a second phrasing if the first finds nothing. Use mode "standard" first; use "extended" only if a note stays unresolved after two standard searches.
2. Decide the most likely origin: book title + author, or teacher, or website/video channel. Prefer the original work over aggregators (Goodreads, Pinterest, quote sites). Note the page or chapter if a result shows it.
3. Map to CANON.md: if the origin is one of the canonical names (exact spelling), put it in canonical_match as "[[Name]]"; otherwise null, and give the real name in candidate_source.
4. Confidence: high = the exact passage found verbatim at a source that names the work/author; medium = strong partial match or the work is clearly identified but wording differs; low = plausible guess from style/names only; none = no evidence. Be honest: a wrong attribution is worse than none.
5. Non-quote or garbled bodies (game subtitles, UI text, OCR noise): verdict "skip", confidence "none".

Report: JSON array, one object per note, keys exactly:
{"file","candidate_source","author","canonical_match","page","confidence","evidence_url","evidence_snippet","note"}
evidence_snippet = up to 25 words from the page that match the body. note = one line of reasoning. Write the file with the Write tool, then reply with 3 lines: how many high/medium/low/none. Do not skip notes, do not paraphrase the passages into your report beyond the snippet.
