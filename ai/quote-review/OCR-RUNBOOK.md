# OCR verification runbook — quote notes vs. source images

How to re-run the image-to-text verification of `content/Wisdom Quotes/` with Claude Code subagents.
Last run: 2026-10-21 (203 notes, see `ai/reviews/2026-10-21-ocr-verification.md`). Written so a
fresh clone can repeat it in six months.

## What a pass does
Each quote note's **body is the quote**; `image_name` in its frontmatter points at the ground-truth
screenshot in `content/Wisdom Quotes/Images/`. A pass has an agent read the image, fix the body,
try to identify the source, and set flags. Flag semantics:

| Verdict | Flags after |
|---|---|
| verified-clean | `Edited: true`, review tag removed, `source` is a canonical `"[[Name]]"` |
| verified-no-source | `Edited: false`, tag `needs-source` (text correct, attribution unknown) |
| unreadable | body `*[image not legible — needs manual transcription]*`, tag `needs-manual-review` |
| non-quote | untouched, tag kept, listed for a human delete/keep decision |

Hard rules: never touch the `draft:` line, never set `draft: false`, straight ASCII quotes in
frontmatter, editorial rules in `EDIT-RULES.md` apply in full.

## Prerequisites
- Repo at `D:\Vaults\WisdomCompiler` (paths in the briefs are absolute Windows paths; edit them if the clone lives elsewhere).
- Python 3 on PATH; `pyyaml` optional (the checker degrades to regex checks without it).
- Claude Code with the Agent tool and `opus` / `sonnet` / `haiku` model overrides.
- Thermal check first on this laptop (`~/.claude/hooks/ThermalCheck.ps1`); a pass is API-bound, not CPU-bound, but don't stack it with a build.

## Steps (from repo root)
1. **Worklist** — snapshot the flagged notes and their current `draft` values:
   ```
   python -I ai/quote-review/build-ocr-worklist.py <scratch>/worklist.json
   ```
   Default tags are `needs-review,needs-manual-review,needs-source`; narrow with `--tags`.
2. **Batch** — ordinary quote cards: 8 notes per agent, `sonnet`. Anything that is a book page,
   manga, game UI, or previously `needs-manual-review`: **one note per agent**, `opus` or `sonnet`.
   At most 20 agents run at once (harness cap); queue the rest.
3. **Brief** — give every agent `OCR-AGENT-BRIEF.md` plus its file list and a per-batch JSON report path.
   Agents write reports as `{"file","verdict","body_changed","source_set","page","confidence","note"}`.
4. **Content-filter casualties** — an agent that dies with "Output blocked by content filtering
   policy" writes nothing. Do not retry the same prompt. Re-run that note alone in **quote-only mode**:
   body = the set-off quotation or one 2–4 sentence passage, `ShowImage: true`, tag `needs-source`.
   Known triggers: full-page transcription of Argüelles *Mandala* (1972), *Getting Things Done*,
   *Awakened Leadership*. The orchestrator must not transcribe those pages itself (a block on the
   orchestrator's output ends the session).
5. **Second reader** — for every note whose body changed, a `haiku` agent with `OCR-QA-BRIEF.md`
   (about 8 notes per agent) reports pass / fail / uncertain. Fix fails by hand with a one-line edit.
6. **Deterministic checks**:
   ```
   python -I ai/quote-review/normalize-frontmatter.py            # curly → straight quotes in frontmatter
   python -I ai/quote-review/verify-ocr-pass.py <scratch>/worklist.json   # exit 1 on any PROBLEM
   grep -l '^draft: false' content/Wisdom\ Quotes/*.md | wc -l    # must equal the count before the pass
   ```
7. **Aggregate** the per-batch JSON into one results file and write the review doc
   (`ai/reviews/YYYY-MM-DD-ocr-verification.md`: outcome table, decision lists, per-note verdicts).
   Keep the results JSON and worklist beside it.
8. **Human review, then ship**: `git diff -- "content/Wisdom Quotes"`, commit, build, deploy.

## Build and deploy (local CLI only, never CI)
```
node ./quartz/bootstrap-cli.mjs build
npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4
```
`npx quartz build` is broken on this machine since before 2026-10-21 (`npm error code EMISSINGTARGET`
in `package-lock.json`); repair with `rm package-lock.json && npm install` when wanted.
Wrangler auth is the browser OAuth login held in wrangler's own config dir; refresh with
`npx wrangler login`. If deploy fails on auth, `unset CF_API_TOKEN && unset CLOUDFLARE_API_TOKEN`
first (stale env vars override the login). No secrets live in this repo.

## Artifact layout
- `ai/quote-review/EDIT-RULES.md` — canonical sources, tag vocabulary, formatting rules.
- `ai/quote-review/OCR-AGENT-BRIEF.md`, `OCR-QA-BRIEF.md` — the prompts used on 2026-10-21.
- `ai/quote-review/build-ocr-worklist.py`, `verify-ocr-pass.py`, `normalize-frontmatter.py` — tooling.
- `ai/reviews/2026-10-21-ocr-*.json` — worklist, batches, and all 203 verdicts from the last run.
- `ai/sessions/raw/<session-id>.md` — distilled transcript of the run (gitignored, this machine only).

## Gotchas learned
- Multi-note batches lose every note when the filter kills the agent. Isolation is the fix, not retries.
- Agents that rewrite whole files flip CRLF to LF; git normalises it, the diff is noise.
- The harness Agent tool does not stall; the June 2026 Workflow runtime did. Prefer Agent.
- Haiku is good enough as a fidelity reader; it caught 4 slips in 83 bodies that sonnet/opus missed.
- `cd` inside a Bash call persists to the next call; use absolute paths.
