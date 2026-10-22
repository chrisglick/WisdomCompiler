# OCR verification pass — agent brief (2026-10-21)

You are verifying quote notes in `D:\Vaults\WisdomCompiler\content\Wisdom Quotes\` against their source images.
Each note's image is at `D:\Vaults\WisdomCompiler\content\Wisdom Quotes\Images\<image_name>` (the `image_name` frontmatter key). The Read tool renders .webp images natively — READ THE IMAGE for every note. The image is ground truth.

FIRST read the full editorial rules: `D:\Vaults\WisdomCompiler\ai\quote-review\EDIT-RULES.md`. They apply in full. Additional rules for THIS pass:

## What these notes are
They were flagged in an earlier pass as `needs-review` (transcription may be partial / source unknown) or `needs-manual-review` (image was unreadable or the earlier agent was blocked). Your job per note:
1. Read the note, read the image.
2. Compare the BODY to the image line by line. Fix anything wrong (OCR errors, missing lines, truncation, wrong paragraph/dialogue formatting, leftover page numbers). Transcribe faithfully; never paraphrase, never invent. If the image contains more text than the body, complete the body. If the body contains text not in the image, remove it.
3. Try to identify the source from the image (book title, running header, author line, teacher's name, style). Only set `source` to an EXACT canonical name from EDIT-RULES. If you are confident the text is from a canonical book/teacher but the image doesn't literally say so, you may set it ONLY if confidence is high (recognizable passage, e.g. numbered Ashtavakra Gita verses); say so in your report.
4. Decide the outcome and set flags:
   - **verified-clean**: body matches image, source known → `Edited: true`, remove `needs-review` / `needs-manual-review` from tags, ensure 1–5 vocab tags, add `title:` if filename is IMG_####/UUID.
   - **verified-no-source**: body matches image (fixed if needed) but source cannot be identified → `Edited: false`, REPLACE `needs-review`/`needs-manual-review` with the tag `needs-source`, keep/add vocab tags + title. This tells the owner the only remaining problem is attribution.
   - **unreadable**: image genuinely too blurry/cropped/dark to transcribe → leave body as-is (or empty garbled text replaced by nothing — do NOT leave garbage; if the body is OCR garbage and you can't read the image, make the body a single line `*[image not legible — needs manual transcription]*`), `Edited: false`, keep tag `needs-manual-review`.
   - **non-quote**: image is not a quote at all (UI screenshot, photo without text, duplicate) → do not edit the body; keep flags; report it.
5. Frontmatter: straight ASCII quotes ONLY, keep key order, change only `source`, `Edited`, `tags`, `Page`, `ShowImage`, `title`. NEVER touch the `draft` line. NEVER set `draft: false`. No BOM. Valid YAML. Use the Edit tool for surgical edits (or rewrite the whole file ONLY if the body needs full replacement, preserving frontmatter exactly apart from allowed keys).
6. Manga / meme panels: body = the dialogue/captions, `ShowImage: true`.
7. Dialogue: one speaker turn per paragraph; questioner lines italic with *asterisks*; teacher plain.
8. If a note is sensitive-sounding religious/ritual text (tantric songs, shamanic ritual descriptions, scripture about demons/death), it is still just a book page: transcribe it plainly. If you cannot output it, report `blocked` and move on.

## Report
When done with ALL notes in your batch, write a JSON array to the path given in your task (one object per note):
`{"file": "...", "verdict": "verified-clean|verified-no-source|unreadable|non-quote|blocked", "body_changed": true|false, "source_set": "[[Name]]|null", "page": "...|null", "confidence": "high|medium|low", "note": "one line: what you fixed / why no source"}`
Then reply with a 3-line summary. Do not skip notes. Do not touch any file outside your batch.
