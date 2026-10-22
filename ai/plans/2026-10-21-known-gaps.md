# Known gaps and open decisions — as of 2026-10-21

Backlog of loose ends after the OCR verification pass. One line of *what / why / where / fix* each,
highest weight first. Strike items as they close; do not renumber.

1. **191 quote edits uncommitted.** What: the whole OCR pass sits in the working tree. Why: owner review
   required before anything ships. Where: `git diff -- "content/Wisdom Quotes"`. Fix: review, then the
   commit in `ai/sessions/SESSION-2026-10-21-ocr-verification.md` §5.
2. **`ai/` folder untracked.** What: every review doc, runbook, decision and RESUME since June is not in
   git. Why: never added. Where: `git status --short | grep '^??'`. Fix: `git add ai RESUME.md` in the
   same commit as item 1.
3. **~45 non-quote notes.** What: game subtitles, picture plates, lyric searches, a physics paper.
   Why: screenshots swept in with the quotes. Where: list A in `ai/reviews/2026-10-21-ocr-verification.md`.
   Fix: delete the `.md` and `.webp` pairs, or keep as image-only pages; owner's call.
4. **Non-canonical recurring sources.** What: *Mandala* (29), MySaiBaba.com (10), Bloom County (4),
   *Awakened Leadership* (3). Why: not in the vocabulary in `EDIT-RULES.md`. Where: list D. Fix: add to
   the canonical list and re-attribute, or delete the notes.
5. **29 recognition-only attributions.** What: `source` set because the passage was recognised, image
   shows no title. Where: list B. Fix: confirm or clear; clearing means `Edited: false` + `needs-source`.
6. **96 `needs-source` notes.** What: text verified, author unknown. Fix: research task, could be a
   web-search agent pass over the first sentence of each body. Not started.
7. **Teacher enrichment drafts (Huang Po, Nisargadatta, Ramana).** What: modified since 2026-06-12,
   uncommitted. Where: `content/Teachers/`, workflow in `production/WORKFLOW-TEACHERS.md`. Fix: review, commit.
8. **`npx quartz build` broken.** What: `npm error code EMISSINGTARGET` from `package-lock.json`
   (unchanged since 2026-01-27). Fix: `rm package-lock.json && npm install`; until then
   `node ./quartz/bootstrap-cli.mjs build`.
9. **Plain `needs-review` stragglers.** What: IMG_1234, IMG_1299, IMG_1658 keep the old tag. Why: they
   are non-quotes the agents deliberately did not touch. Fix: resolved by item 3.
10. **IMG_6893 attribution.** What: `— Bob Anderson` is the book's author, not printed on the page.
    Fix: keep or drop the signature line; one-line edit.
11. **`_screenshot_template.md` date warning** on every build. Pre-existing, cosmetic. Fix: give the
    template a valid `date:` or exclude it.
12. **No `ai/CAPTURE.md` / `ai/memory/` bundle.** What: lk-doctor reports 4 WARN (missing okf shim and
    memory bundle). Why: the project predates the lk knowledge layout and uses `ai/journal` + `ai/sessions`
    instead. Fix: run `/lk-init-ai-workspace` only if the extra structure is wanted; the current layout works.
