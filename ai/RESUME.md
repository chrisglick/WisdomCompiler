---
file: ai/RESUME.md
purpose: First file to read when resuming work in this project. Living snapshot — regenerated every EndSession.
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
1. **OCR verification pass (2026-10-21) is COMMITTED (`6498d94`), not yet deployed.** Read `ai/reviews/2026-10-21-ocr-verification.md`, decide on the ~45 non-quote notes (delete?) and the non-canonical sources (add *Mandala* / MySaiBaba to vocab, or delete), then `git diff -- "content/Wisdom Quotes"`, commit, build, deploy. Pick-up state, decisions and the exact commit command: `ai/sessions/SESSION-2026-10-21-ocr-verification.md`. Open items: `ai/plans/2026-10-21-known-gaps.md`. To re-run a pass: `ai/quote-review/OCR-RUNBOOK.md`.
2. **Teacher enrichment** (`production/WORKFLOW-TEACHERS.md`): Ramana / Nisargadatta / Huang Po article drafts sit in the working tree, uncommitted since 2026-06-12. Review and commit.
3. Roadmap items 5–9 (typography, unify voice, OG/RSS, build-time aggregation, concept threads): `project_ux_council_roadmap.md`.
4. After any content/code change: `node ./quartz/bootstrap-cli.mjs build` (from project root; `npx quartz build` is broken, see Key Pointers) then deploy.

## 🧭 Current State
- **Roadmap items 1–4 DONE, committed (`f0e6455`, `0eb072f`, `dd630dd`), AND DEPLOYED LIVE** to wisdomcompiler.com (2026-06-11). Production verified: Kindred passages, "More from this source", chrome removed — all confirmed live.
- Live build preview of the deployed state: https://446e0fc4.wisdom-compiler.pages.dev
- git tip: `6498d94` (OCR pass + `ai/` folder, 2026-10-21). Working tree: 3 teacher drafts + `scripts/extract-keywords.py` modified since June, untracked `scripts/audit-teachers.py`, `production/WORKFLOW-TEACHERS.md`. Live site still serves pre-pass bodies until the next deploy.
- The site now serves the cleaned, attributed content (was serving pre-cleanup content before this).
- `ai/` is tracked since `6498d94`. Transcript archives in `ai/sessions/raw/` are gitignored on purpose (public repo) and exist only on this laptop.

## 🧵 Active Threads
- **Roadmap items 5–9 remain:** typography (5), unify voice (6), OG cards + daily permalink + RSS (7), replace static Python link-scripts with build-time aggregation (8), curated concept-threads (9).
- **Publish policy:** 229 `draft:true` notes deliberately hidden. Selective publishing (flip `draft:false` per note) is future + manual — never bulk-flip.
- **OCR flags after 2026-10-21:** 80 promoted clean, 98 `needs-source` (text verified, no canonical attribution), 24 `needs-manual-review` (non-quotes / unreadable). IMG_6941 and IMG_6944 are clean now (quote-only bodies).

## ❓ Open Questions / Decisions Pending
- Criteria/timing for flipping the 229 hidden drafts to published.
- Keep homepage `RandomQuote`/`DailyWisdom` random (it's a landing-page teaser) vs make it consistent with per-quote relatedness — currently fine as-is.
- RelatedQuotes tuning: `MAX_RELATED=4`, `SAME_SOURCE_WEIGHT=5`, `SHARED_TAG_WEIGHT=1` — adjust if relatedness feels off.

## 🔑 Key Pointers
- **Deploy (LOCAL CLI only, never CI):** `node ./quartz/bootstrap-cli.mjs build && npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4`. Auth fix: `unset CF_API_TOKEN && unset CLOUDFLARE_API_TOKEN`. `v4` IS the production branch (updates wisdomcompiler.com).
- Roadmap + status: `~/.claude/projects/D--Vaults-WisdomCompiler/memory/project_ux_council_roadmap.md`
- Architecture + gotchas: `ai/context/site-architecture.md`
- OCR verification runbook + briefs + checker: `ai/quote-review/OCR-RUNBOOK.md`
- Council debate/review: `ai/reviews/2026-06-07-site-review-and-council.md`
- Why item 4 is build-time not random: `ai/decisions/ADR-20260610-related-passages-build-time.md`
- Layout: `quartz.layout.ts` · Relatedness: `quartz/components/RelatedQuotes.tsx` · Attribution: `quartz/components/SourceBanner.tsx` · Typography target: `quartz/styles/custom.scss`

## ✅ How To Verify You're Oriented
- `git -C D:/Vaults/WisdomCompiler log --oneline -3` → tip is `dd630dd feat(ux): related "Kindred passages"...`.
- Live check: `curl.exe -s -L -A "Mozilla/5.0" https://wisdomcompiler.com/Wisdom-Quotes/All-that-is-required-is-to-be-still` should contain `Kindred passages` and NOT contain `backlinks`. (WebFetch gets 403 — must use curl with a UA.)
- Build gotcha (2026-10-21): `npx quartz build` currently fails with npm `EMISSINGTARGET` (stale lock/node_modules, `node_modules/.bin/quartz` missing). Use `node ./quartz/bootstrap-cli.mjs build` instead, or `rm package-lock.json && npm install` to repair. Also: run from the project ROOT, not a subdir (a stray shell `cd` breaks it — see `ai/context/site-architecture.md`).
- Fact check: there is NO graph-view component in this project (ignore older notes that say "graph view").

---
*Generated by the EndSession skill. Do not hand-edit casually — it is overwritten each session. Put durable narrative in `ai/journal/`, durable decisions in `ai/decisions/`, durable context in `ai/context/`.*
