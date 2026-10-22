# Site Architecture & Known Gotchas — WisdomCompiler

_Durable orientation for any agent working on this project. Last verified: 2026-06-10._

## What it is
A **Quartz v4.5.2** static site generated from an Obsidian vault. Content source: `content/`. One branch: `v4`. Remote: `git@github.com:chrisglick/WisdomCompiler.git`. Live at **wisdomcompiler.com** on **Cloudflare Pages** (project `wisdom-compiler`).

## Content model
- **Wisdom Quotes** (`content/Wisdom Quotes/*.md`): ~650 notes, each a transcribed passage from a photographed book page. Filename ≈ the quote's first line / a human title. Key frontmatter: `source: "[[Book or Teacher]]"`, `Page`, `image_name` (the `.webp` screenshot), `tags`, `Edited`, `draft`, `ShowImage`.
- **Books** (`content/Books/`), **Teachers** (`content/Teachers/`): entity pages. A quote's `source` wikilink resolves to one of these.
- **Concepts** (`content/Concepts/`): theme pages (was a single `Concepts.md`, restructured to a folder 2026-06-10).

### Draft / publish model (IMPORTANT — was previously mis-documented)
650 notes split roughly: **234 `draft: false`** + **229 `draft: true`** + **~187 with no `draft` field** (Quartz publishes those by default). So ≈421 are public, 229 hidden. A `quartz build` reports "Filtered out 242 files" — that's the drafts + templates being excluded. **Do not assume "all notes are draft:true."** Publishing policy: keep the 229 hidden; flip `draft:false` per-note, manually, deliberately — never bulk-publish.

## Component model (custom)
Custom Quartz components in `quartz/components/`, wired in `quartz.layout.ts`, exported from `quartz/components/index.ts`:
- **`SourceBanner.tsx`** — server component. On a quote page, reads `source:` frontmatter, finds the matching Book/Teacher page in `allFiles`, renders an avatar + name + link ("attribution"). Also shows page number + "More from this source →". On Book/Teacher pages it renders a hero badge. **This is why attribution appears even though quote bodies are plain text.**
- **`RelatedQuotes.tsx`** — server component, "Kindred passages". Ranks other published quotes by same `source` (weight 5) + shared tags (weight 1); top 4. Self-gates to quote pages. In `afterBody`. See `ai/decisions/ADR-20260610-related-passages-build-time.md`.
- **`RandomQuote.tsx` / `DailyWisdom.tsx`** — homepage only. Client-side, with a HARDCODED quote list in `quartz/components/scripts/randomquote.inline.ts`. (Stylistically inconsistent with RelatedQuotes now; landing-page-only so acceptable.)
- **`HomepageExplore`, `WisdomQuiz`, `BookMeta`, `BookGrid`, `TeacherGrid`, `ArticleImage`** — other customs.

### Layout structure (`quartz.layout.ts`)
- `defaultContentPageLayout` — individual pages (quotes, books, teachers). As of 2026-06-10 the **developer chrome is stripped**: NO Explorer (file tree) on the left, NO Backlinks on the right — just PageTitle + a Search/Darkmode/ReaderMode toolbar; TOC desktop-only on the right; Breadcrumbs in `beforeBody`.
- `defaultListPageLayout` — folder/tag index pages. **Still keeps the Explorer** (browsing context).
- `afterBody` (shared) holds `RelatedQuotes` (self-gates).
- The Explorer `filterFn` excludes folders: `tags, images, social-media, lakshmi the cow, about`. MUST use optional chaining (`node.name?.toLowerCase()`) — some tree nodes have undefined names.

## Generation scripts (legacy / drift risk)
`scripts/generate-book-links.py` and friends statically write passage-link lists onto Book/Teacher pages. **Drift risk:** they go stale on content change and produce the `draft:true → 404` footgun (linking notes that don't build). Roadmap item 8 = replace these with build-time aggregation (the SourceBanner/RelatedQuotes server-component pattern). Until then: do NOT run `generate-book-links.py` against unflipped drafts.

## Build & deploy
- Build: `npx quartz build` (~2 min for ~750 files). Output → `public/`.
- Deploy: **LOCAL CLI ONLY, never CI.** `npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4`. Auth fix if needed: `unset CF_API_TOKEN && unset CLOUDFLARE_API_TOKEN`.
- CI workflows in the repo are upstream Quartz (gated to `jackyzha0/quartz`) or a never-working custom `deploy.yaml` — ignore them when asked to deploy.

## Known gotchas
1. **Shell `cd` persists** across Bash-tool calls and pollutes CWD. A stray `cd content/Wisdom Quotes` made `quartz build` fail (ENOENT on `package.json`). **Always build from project root** (`Set-Location D:\Vaults\WisdomCompiler` first, or run via PowerShell tool with explicit `Set-Location`).
2. **No graph-view component exists.** Older notes saying "graph view" are wrong; the only chrome was Explorer + Backlinks (now removed from content pages).
3. **CRLF warnings** on `git add` of content are harmless (Git normalizing line endings to LF).
4. **`live site = committed content`, not working tree.** A cleaned working tree shows nothing publicly until committed AND deployed. The "missing attribution" complaint was a content-not-yet-deployed issue, not a code bug.
5. **wisdomcompiler.com returns 403 to WebFetch** (bot filtering). Use `curl.exe -A "Mozilla/5.0 ..."` to fetch live pages for review.
6. `_screenshot_template.md` has an invalid `null` date → a harmless build warning.

## Trust order for resuming
`ai/RESUME.md` → latest `ai/journal/*.md` → `git log` → the code. Roadmap status lives in global memory `project_ux_council_roadmap.md`.
