---
id: ADR-20260610-related-passages-build-time
date: 2026-06-10
status: accepted
template_version: 1
---

# Related "Kindred passages" via build-time server component, not client-side random

## Context
Council roadmap item 4 originally read "give me another" — a button to surface another quote, modeled on the existing homepage `RandomQuote` (which ships a hardcoded ~149-quote list in an inline client script). Krishna corrected the intent: the next quote should not be random, it should come from "similar places — same book, author, or topic."

Constraints/forces at play:
- Quote frontmatter is rich after the cleanup: 537/650 have `source:` (a `[[wikilink]]` to a Book/Teacher), 650/650 have topic `tags:`.
- Quartz server components can read `allFiles` at build time (the existing `SourceBanner` already does this to resolve a quote's source page).
- A solo-maintained static site; minimizing JS and stale hand-maintained lists is valuable.

## Decision
Item 4 is a **build-time server component** (`quartz/components/RelatedQuotes.tsx`) that, for each quote page, scans `allFiles` and ranks other published quotes by relatedness: **same `source` = strong weight (5), each shared topic tag = weak weight (1)**, with workflow/noise tags excluded (`needs-review`, `needs-manual-review`, `screenshot`, `meme`). It renders the top 4 as "Kindred passages" links (title + source). Self-gates to quote pages, excludes drafts and self. No hardcoded list — always in sync with content.

## Alternatives Considered
- **Client-side "give me another" random button** (extend `RandomQuote`): rejected — contradicts the "similar, not random" intent, needs a hardcoded/maintained quote list, produces no crawlable links.
- **Same-source-only relatedness:** rejected — quotes whose source has <4 siblings would show too few; tag overlap gives a graceful topical fallback across sources.
- **Tag-only relatedness:** rejected — "same book" is the strongest, most intuitive relation; source must dominate, which the 5-vs-1 weighting ensures.
- **A Quartz plugin / precomputed similarity index:** rejected as overkill at this corpus size (~500 published × ~750 files is trivial to score inline at build).

## Consequences
- **Easier:** real internal links between related passages (SEO + the council's "concept-threads retain seekers" retention goal); zero maintenance — relatedness recomputes from frontmatter every build.
- **Harder / owed:** relatedness quality depends on `source:` and `tags:` being accurate; the homepage `RandomQuote`/`DailyWisdom` (still random, still a hardcoded list) is now stylistically inconsistent with per-quote relatedness — fine on a landing page, but a future cleanup candidate.
- **Tuning knobs** live as constants in `RelatedQuotes.tsx`: `MAX_RELATED`, `SAME_SOURCE_WEIGHT`, `SHARED_TAG_WEIGHT`, `NOISE_TAGS`.
- Establishes the **server-component-over-static-script** pattern, which roadmap item 8 should extend to replace `scripts/generate-book-links.py`.
