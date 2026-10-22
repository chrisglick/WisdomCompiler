---
file: ai/RESUME.md
purpose: First file to read when resuming work in this project. Living snapshot, regenerated every EndSession.
last_updated: 2026-10-21
last_session: ai/sessions/SESSION-2026-10-21-ocr-verification.md
sessions_logged: 5
status: active
template_version: 1
---

# RESUME — WisdomCompiler

> **Reading this to continue work?** This is a regenerated snapshot of the *current* state.
> For the narrative of how we got here, read the dated session logs in `ai/journal/`.
> Trust order: this file → latest `ai/journal/*.md` → `git log` → the code itself.

## ▶ Start Here (next actions)
1. **Decide the small ones** (each a one-line edit, then build + deploy): duplicate Claret note (backlog 13), retitle the Le Guin note "He could not move..." (14), the 19 already-public notes that fail the publish rule (15). Backlog: `ai/plans/2026-10-21-known-gaps.md`.
2. **Cloudflare Web Analytics** is still OFF and can only be enabled in the dashboard (Workers & Pages, wisdom-compiler, Metrics, Web Analytics). Krishna only.
3. **OCR decision lists** in `ai/reviews/2026-10-21-ocr-verification.md`: ~45 non-quote notes (delete?), *Mandala* / MySaiBaba (add to canon or delete), 29 recognition-only attributions. 81 `needs-source` notes remain; research found nothing for most (`ai/reviews/2026-10-21-source-research.md`).
4. **Teacher enrichment** (`production/WORKFLOW-TEACHERS.md`): Ramana / Nisargadatta / Huang Po drafts uncommitted since 2026-06-12. Review and commit.
5. Roadmap items 6, 7, 8 (unify voice, OG/RSS, build-time link aggregation) and the questioner-line transformer (backlog 17): `project_ux_council_roadmap.md`.
6. After any content/code change: `node ./quartz/bootstrap-cli.mjs build` from the project root, then deploy (Key Pointers).

## 🧭 Current State
- **2026-10-21, all LIVE and PUSHED** (`origin/v4` level with local at `5a31bac` plus this close-out commit): OCR pass (203 notes), publish rule applied (107 + 18 notes), `/Themes` browse-by-theme page, contemplative typography on quote pages, source research pass, canon widened to 60 books with 12 new Book pages. Last deploy https://a2d03084.wisdom-compiler.pages.dev.
- Counts: `draft: false` 356 of 650 quote notes, 549 public quote pages, `needs-source` 81, `needs-manual-review` 23, 63 Book pages.
- Working tree: 3 teacher drafts + `scripts/extract-keywords.py` modified since June, untracked `scripts/audit-teachers.py`, `production/WORKFLOW-TEACHERS.md`. Nothing from the 2026-10-21 session is uncommitted.
- `ai/` is tracked since `6498d94`. Transcript archives in `ai/sessions/raw/` are gitignored on purpose (public repo) and exist only on this laptop.
- Roadmap items 1 to 5 and 9 done and live (`f0e6455`, `0eb072f`, `dd630dd`, `3d0c9a3`).

## 🧵 Active Threads
- **Publish policy:** mechanical rule in `ai/quote-review/EDIT-RULES.md` ("Publish rule"); procedure in `OCR-RUNBOOK.md` "Publish pass". Re-apply after each verification pass. 19 pre-rule public notes fail it (backlog 15).
- **Canon:** 60 books + 15 teachers (`vocab.json`, EDIT-RULES). Widened 2026-10-21 because Krishna has wide interests; add a Book page + vocab entry whenever a real non-canon source is confirmed by the image.
- **Verification tooling:** `OCR-RUNBOOK.md` (OCR pass, publish pass, research pass), briefs beside it, `build-ocr-worklist.py`, `verify-ocr-pass.py` (reports `DRAFT CHANGED` after a publish flip; expected).
- **Roadmap items 6, 7, 8 remain:** unify voice, OG cards + daily permalink + RSS, replace static Python link-scripts with build-time aggregation.

## ❓ Open Questions / Decisions Pending
- Backlog 13, 14, 15 (above). Research list B (22 low-confidence guesses): apply only after checking the image.
- Keep homepage `RandomQuote`/`DailyWisdom` random (landing-page teaser) vs consistent with per-quote relatedness; fine as-is.
- RelatedQuotes tuning: `MAX_RELATED=4`, `SAME_SOURCE_WEIGHT=5`, `SHARED_TAG_WEIGHT=1`.

## 🔑 Key Pointers
- **Deploy (LOCAL CLI only, never CI):** `node ./quartz/bootstrap-cli.mjs build && npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4`. Auth fix: `unset CF_API_TOKEN && unset CLOUDFLARE_API_TOKEN`. `v4` IS the production branch. Thermal check first on this laptop; take the CPU slot via `~/.claude/tools/heavy-slot.ps1` if a peer session is running.
- Session note (whole day, two close-outs): `ai/sessions/SESSION-2026-10-21-ocr-verification.md` · Journal: `ai/journal/2026-10-21.md`
- Roadmap + status: `~/.claude/projects/D--Vaults-WisdomCompiler/memory/project_ux_council_roadmap.md`
- Architecture + gotchas: `ai/context/site-architecture.md`
- Verification runbook + briefs + checker: `ai/quote-review/OCR-RUNBOOK.md`
- Council debate/review: `ai/reviews/2026-06-07-site-review-and-council.md`
- Why item 4 is build-time not random: `ai/decisions/ADR-20260610-related-passages-build-time.md`
- Layout: `quartz.layout.ts` · Relatedness: `quartz/components/RelatedQuotes.tsx` · Themes: `quartz/components/ThemeIndex.tsx` · Attribution: `quartz/components/SourceBanner.tsx` · Quote typography: `quartz/styles/custom.scss`

## ✅ How To Verify You're Oriented
- `git -C D:/Vaults/WisdomCompiler log --oneline -3` → tip is the 2026-10-21 close-out commit on top of `5a31bac docs: RESUME and backlog after canon widening`.
- Live check: `curl.exe -s -L -A "Mozilla/5.0" https://wisdomcompiler.com/Themes` should contain `Browse by theme`; a quote page should contain `Kindred passages` and NOT `backlinks`. (WebFetch gets 403; use curl with a UA.)
- Build gotcha: `npx quartz build` fails with npm `EMISSINGTARGET` (stale lock). Use `node ./quartz/bootstrap-cli.mjs build`, or `rm package-lock.json && npm install` to repair. Run from the project ROOT.
- Fact check: there is NO graph-view component in this project (ignore older notes that say "graph view").

---
*Generated by the EndSession skill. Do not hand-edit casually; it is overwritten each session. Put durable narrative in `ai/journal/`, durable decisions in `ai/decisions/`, durable context in `ai/context/`.*
