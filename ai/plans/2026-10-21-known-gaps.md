# Known gaps and open decisions — as of 2026-10-21

Backlog of loose ends after the OCR verification pass. One line of *what / why / where / fix* each,
highest weight first. Strike items as they close; do not renumber.

1. ~~191 quote edits uncommitted.~~ Committed `6498d94` on 2026-10-21. Still to do: push, build, deploy.
2. ~~`ai/` folder untracked.~~ Tracked since `6498d94`.
3. **~45 non-quote notes.** What: game subtitles, picture plates, lyric searches, a physics paper.
   Why: screenshots swept in with the quotes. Where: list A in `ai/reviews/2026-10-21-ocr-verification.md`.
   Fix: delete the `.md` and `.webp` pairs, or keep as image-only pages; owner's call.
4. **Non-canonical recurring sources.** What: *Mandala* (29), MySaiBaba.com (10), Bloom County (4),
   *Awakened Leadership* (3). Why: not in the vocabulary in `EDIT-RULES.md`. Where: list D. Fix: add to
   the canonical list and re-attribute, or delete the notes.
5. **29 recognition-only attributions.** What: `source` set because the passage was recognised, image
   shows no title. Where: list B. Fix: confirm or clear; clearing means `Edited: false` + `needs-source`.
6. **98 `needs-source` notes.** Web-research pass done 2026-10-21 (`ai/reviews/2026-10-21-source-research.md`): 3 high, 13 medium, 22 low, 59 none; only 4 map to canonical names. The rest are non-canon works (sutras, Bloom County, Le Guin, Musashi, I Ching, GTD, Mandala). Remaining decision: add those works to the canon or leave the tag.
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
13. **Duplicate Claret note.** `His vocational detour...` and `Yet, his vocational detour...` are the same passage from IMG_0009, both public. Fix: delete one (owner's call).
14. **Mis-titled note.** `He could not move as the force of Bhagavans presence held him.md` is Le Guin's *Rocannon's World*; the filename/title still says Bhagavan. Fix: add a `title:` from the passage.
