# Session — OCR verification pass, orchestrated (2026-10-21)

> Resumed the quote-note verification the June 2 pass left flagged. One orchestrator dispatched
> opus / sonnet / haiku subagents to read every flagged note's source image, fix the body, set flags.
> Source: `ai/sessions/raw/1d21ff51-6169-4115-b4dd-c3fe43b3ea7f.md` (distilled transcript, gitignored,
> this machine only; the `.jsonl` beside it holds tool output).

---

## 1. What got done

### A. Verification of all 203 flagged notes — 191 files modified, committed as `6498d94`
- Worklist: 160 `needs-review`, 41 `needs-manual-review`, 2 untagged garbled notes (IMG_6941, IMG_6944).
- 20 sonnet batches of 8 for the ordinary cards; 43 single-note opus/sonnet runs for the hard tier.
- Verdicts: 80 verified-clean, 96 verified-no-source, 25 non-quote, 2 unreadable. 86 bodies rewritten.
  Confidence: 130 high, 72 medium, 1 low. Every verdict with its note: `ai/reviews/2026-10-21-ocr-results.json`.
- 13 wrong attributions cleared (list C in the review doc). About 45 notes are not quotes at all (list A).
- Haiku second reader checked all 83 changed bodies that could be re-read: 4 fidelity slips, fixed by hand
  (IMG_6947, IMG_6948, "Moral nobility…", "I exist is the only permanent…").
- Deterministic checker: 0 problems on 203. `draft: false` count 234 before and after. No BOMs, no curly
  quotes in frontmatter.

### B. Method captured for reuse
- Runbook: `ai/quote-review/OCR-RUNBOOK.md` (steps, filter fallback, build/deploy, auth pointers).
- Prompts: `ai/quote-review/OCR-AGENT-BRIEF.md`, `OCR-QA-BRIEF.md`.
- Tooling: `ai/quote-review/build-ocr-worklist.py` (new, tested: 123 flagged notes now),
  `verify-ocr-pass.py` (made path-portable from the session checker; exit 1 on problems).
- Data: `ai/reviews/2026-10-21-ocr-{worklist,batches,results}.json`.

### C. Docs
- Review doc with decision lists A–E: `ai/reviews/2026-10-21-ocr-verification.md`.
- Journal: `ai/journal/2026-10-21.md`. `ai/RESUME.md` regenerated. Memory: `project_ocr_pass_lessons`.
- `.gitignore` now excludes `ai/sessions/raw/*` (transcript archive, public repo).

### D. Verified the build still works
`node ./quartz/bootstrap-cli.mjs build` parsed 743 files, emitted in about 2 minutes. `npx quartz build`
fails on this machine with an npm lock-file error that predates the session. Nothing was deployed.

## 2. Findings in prose (survive even if the JSON is lost)
- The API output content filter, not model ability, was the blocker on the hard tier. It fires on
  full-page transcription of specific copyrighted books (Argüelles *Mandala* 1972 above all), on opus and
  sonnet alike, silently, with nothing written. A quote-only body never tripped it.
- Clusters discovered: IMG_15xx are Project Zomboid game screenshots with Buddhist subtitle fragments
  (16); IMG_69xx are *Mandala* pages and picture plates (29); IMG_1025/1026 are Kid Cudi lyric searches;
  IMG_1625 is a flywheel engineering paper. MySaiBaba.com video subtitles account for 10 notes.
- Vault flag state at close: `needs-source` 96, `needs-manual-review` 24, plain `needs-review` 3
  (IMG_1234, IMG_1299, IMG_1658, all non-quotes), `Edited: true` 517 of 650, `draft: false` 234.
- IMG_6893 keeps `— Bob Anderson`; that is the book's author, not text printed on the page. Judgment call.

## 3. PICK-UP STATE
- **Complete:** verification, QA, checker, docs, runbook, transcript archive.
- **Committed** as `6498d94` on Krishna's instruction after the close-out (content + `ai/` folder). Not pushed, not deployed.
- **Deferred to Krishna (lists in the review doc):**
  1. Delete the ~45 non-quotes or keep them as image-only pages (list A).
  2. *Mandala* (29) and MySaiBaba (10): add to the canonical vocabulary and re-attribute, or delete (list D).
  3. Confirm or clear 29 recognition-only attributions (list B).
- **Single next action:** build with `node ./quartz/bootstrap-cli.mjs build` and deploy with wrangler so the 80 cleaned public notes go live; then the three decisions.

## 4. NEXT (prioritised)
1. Commit the OCR pass plus the `ai/` knowledge folder. Why: both are untracked; a disk failure or a
   fresh clone loses the whole session. Review first, but do not let it sit for months like the teacher drafts.
2. Make the three decisions above and apply them (delete notes, or edit `EDIT-RULES.md` vocab + re-attribute).
3. Build with the bootstrap script, deploy with wrangler. Why: the live site still serves pre-pass bodies
   for the 80 cleaned notes that are `draft: false`.
4. Teacher enrichment drafts (Huang Po, Nisargadatta, Ramana) uncommitted since 2026-06-12: review and commit.
5. Repair `npm` lock file when convenient so `npx quartz build` works again.

## 5. Durability audit
| Path | State | Risk |
|---|---|---|
| `content/Wisdom Quotes/*.md` (191), `ai/`, `RESUME.md` | committed `6498d94`, not pushed | safe locally; push to reach GitHub |
| `production/WORKFLOW-TEACHERS.md`, `scripts/audit-teachers.py` | untracked | lost on clone |
| `content/Teachers/*.md` (3), `scripts/extract-keywords.py` | modified since June | lost on reset |
| `ai/sessions/raw/*` | gitignored by design (public repo) | this machine only |
| `~/.claude/projects/D--Vaults-WisdomCompiler/memory/` | in-memory store | this machine only |

Recommended commit (after review; no publishing happens because no `draft` line changed):
```
git add .gitignore ai RESUME.md "content/Wisdom Quotes"
git commit -m "content: OCR verification pass 2026-10-21 (203 notes) + ai/ knowledge folder"
```
Teacher drafts and scripts are a separate decision and a separate commit.

## 6. Decisions made this session and why
- **Nothing committed or deployed.** Krishna's standing rule: never publish without him; and the diff
  is 191 files he has not seen.
- **New tag `needs-source`** instead of leaving `needs-review`. Why: it separates "text unverified" from
  "text verified, attribution unknown", so the remaining work is visible as the research task it is.
- **Quote-only fallback** for filter-blocked pages instead of skipping them. Why: a short, accurate passage
  with the image shown is a usable note; a garbled or empty body is not.
- **Non-quotes left untouched.** Why: deleting content is Krishna's call, and the lists cost nothing to keep.
- **Previously `Edited: true` notes downgraded when the image showed no source** (5 net). Why: the rules
  say `Edited: true` requires a canonical attribution; the earlier flag was optimistic.

## 7. Not trustworthy yet
- The 72 medium-confidence and 1 low-confidence verdicts (filter by `confidence` in the results JSON).
- The 29 recognition-only attributions in list B.
- Page numbers set by agents were taken from the image where visible; where the field is null, none was visible.

---

## 8. Continuation, same day (evening and night) — deploy, publish, UX, research, canon
Source: `ai/sessions/raw/1d21ff51-6169-4115-b4dd-c3fe43b3ea7f.md` (re-archived at the final close-out; 217 turns).

### What got done
- **Publish rule written and applied** (`ai/quote-review/EDIT-RULES.md`, "Publish rule"): `draft: false` iff `Edited: true` + canonical `[[wikilink]]` source + no `needs-*` tag. First application published 107 notes (`1bc4234`). Review agents never touch `draft`; publishing is this one mechanical step.
- **Browse by theme** (`/Themes`): `quartz/components/ThemeIndex.tsx` + `styles/themeIndex.scss`, wired in `quartz.layout.ts` behind `ConditionalRender` on slug `Themes`; card on the homepage. 21 vocab tags, up to 5 samples each, each quote used at most once per page (FNV-1a spread). `3d0c9a3`.
- **Contemplative typography** on quote pages only (`quartz/styles/custom.scss`, section dated 2026-10-21): serif stack, 36rem measure, larger leading, footer aligned to the quote column. `3d0c9a3`, polish `63a484e`, `fbddeae`, `49c888b`. Browser QA (Playwright, 12 captures) passed.
- **Source research pass** over 98 `needs-source` notes, 13 sonnet agents, web search only, nothing edited: 3 high, 13 medium, 22 low, 59 none. Brief now in repo: `ai/quote-review/SOURCE-RESEARCH-BRIEF.md`; results `ai/reviews/2026-10-21-source-research.{md,json}`. `6fc693b`.
- **Canon widened** on Krishna's word ("I have wide interests"): 12 Book pages (11 new + the Claret article moved from `content/Websites/`), 18 notes attributed and published. Three researcher attributions were corrected against the images before applying (Mahaparinirvana, not Lankavatara; King's *Papers*, not *Strength to Love*; IMG_1547 is a Bequeathed Teachings line). `4afbbbf`. `vocab.json` and the EDIT-RULES canon list: 60 books.
- **Deployed** four times, last to https://a2d03084.wisdom-compiler.pages.dev (wisdomcompiler.com). **Pushed** to `origin/v4` (first push since June); branch level with origin at close.

### Findings in prose
- Counts at close: `draft: false` 356 of 650 quote notes; 549 public quote pages built; `needs-source` 81; `needs-manual-review` 23; Book pages 63.
- The remaining 81 unsourced notes are unsourced because they are not from any book in the vault, not because the canon was missed. Research found nothing for 59 of them.
- Analytics cannot be enabled from code or the wrangler token (account read + pages write only). It is one toggle in the Cloudflare dashboard: Workers & Pages, wisdom-compiler, Metrics, Web Analytics.
- 19 notes were already public before the rule existed and fail it (mostly attributions the OCR pass cleared). They are still live. Decision pending.
- `verify-ocr-pass.py` compares `draft` against the pre-pass worklist; after a publish flip it reports `DRAFT CHANGED` for every flipped note (37 now). That is the expected signal, not a defect; any other problem class is real.

### PICK-UP STATE
- **Complete, committed, pushed, live:** everything above. Content tip at close: `5a31bac`.
- **Still uncommitted (since June, not this session):** 3 teacher drafts, `scripts/extract-keywords.py`, untracked `production/WORKFLOW-TEACHERS.md`, `scripts/audit-teachers.py`.
- **Deferred, Krishna's call:** backlog items 3, 4, 5, 13 to 17 in `ai/plans/2026-10-21-known-gaps.md`.
- **Single next action:** decide items 13 and 14 (duplicate Claret note; retitle the Le Guin note), then the 19 rule-failing public notes (item 15). Each is a one-line edit plus the standard build and deploy.

### Decisions and why
- **Publish by rule, not by hand.** Why: hand-picking notes re-litigates every pass; the rule makes publishing reproducible and reviewable as a diff.
- **Themes page is build-time, not client-side.** Why: same reason as ADR-20260610 (Kindred passages): static, crawlable, no JS, deterministic samples.
- **Typography scoped to quote pages only.** Why: the rest of the site is reference material; the quote page is the reading experience.
- **Canon widened instead of leaving `needs-source`.** Why: Krishna said so; a passage with a true non-canon source is better attributed than tagged forever. Attributions were applied only where the image or verbatim text confirmed the research.
- **Research results committed before any were applied.** Why: a wrong attribution is worse than none; applying needed a separate, image-checked step.

### Not trustworthy yet
- List B of the research doc (22 low-confidence guesses): unverified; do not apply without the image.
- The 29 recognition-only attributions (list B of the OCR review doc) are unchanged.
- IMG_6954 (Blake): plate 13 by reading, page field left empty.
