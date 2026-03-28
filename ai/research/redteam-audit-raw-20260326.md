# Red Team Adversarial Audit: WisdomCompiler
**Date:** 2026-03-26
**Target:** https://wisdomcompiler.com/
**Method:** Source code analysis, content audit, architecture review
**Auditor:** Claude Opus 4.6 RedTeam

---

## Executive Summary

WisdomCompiler has **3 critical findings, 4 high-severity issues, and 5 medium issues**. The most dangerous problems are: (1) a 668 MB image payload that will cripple mobile users and blow Cloudflare bandwidth, (2) false content claims on the homepage that erode trust, and (3) 14 out of 16 teacher pages that are published but empty. The site's content pipeline has several fragility points that could cause data loss or quality degradation if not addressed.

---

## Finding 1: CRITICAL - 668 MB Unoptimized Image Payload

**Severity:** Critical | **Likelihood:** Certain (already happening) | **Impact:** Severe

The `content/Wisdom Quotes/Images/` directory contains **662 images totaling 668 MB**. Of these, **352 images exceed 500 KB**, with the largest at **6 MB** (IMG_1212.PNG). These are raw iPhone screenshots in PNG format.

**Evidence:**
- IMG_1212.PNG: 6,009 KB
- IMG_1660.PNG: 4,521 KB
- IMG_1659.PNG: 4,475 KB
- 10 images exceed 4 MB each

**Impact:** Quartz copies these to the build output. Even if most are behind draft pages, the build artifact is enormous. Any page that embeds a `ShowImage: true` screenshot forces a multi-MB download. On mobile with poor connectivity, this is a page-abandonment event.

**Mitigation:**
1. Convert all PNGs to WebP at 80% quality (typical 10x reduction)
2. Add a `max-width` resize step (1200px) to the build pipeline
3. Add a pre-commit hook that rejects images > 500 KB
4. Consider Cloudflare Image Resizing or Polish for on-the-fly optimization

---

## Finding 2: CRITICAL - Homepage Claims Are False

**Severity:** Critical | **Likelihood:** Certain (live now) | **Impact:** Credibility destruction

The homepage and HomepageExplore component make **three verifiably false claims:**

| Claim | Reality | Delta |
|-------|---------|-------|
| "600+ curated passages" (index.md, HomepageExplore.tsx) | 446 published quotes | **-154 (35% inflation)** |
| Concepts section linked from homepage | `content/Concepts/` directory **does not exist** | **Broken link / 404** |
| HomepageExplore stats show `{bookCount}+` with `+` suffix | 48 books renders as "48+ Books" | Misleading (no more are pending) |

**Evidence:**
- `content/index.md` line 27: "600+ curated passages from spiritual classics"
- `HomepageExplore.tsx` line 27: same "600+" claim hardcoded in card description
- `HomepageExplore.tsx` line 34: Concepts card links to `"Concepts"` slug -- no such directory exists
- HomepageExplore.tsx line 84: `{bookCount}+ Books` renders as "48+ Books"

**Impact:** A visitor who counts the quotes or clicks Concepts immediately sees the site is unreliable. For a spiritual wisdom site, trust is the product.

**Mitigation:**
1. Fix quote count to actual number (use live `quoteCount` variable already computed in HomepageExplore)
2. Create `content/Concepts/` with tag-based pages, or remove the Concepts card
3. Remove `+` suffix from stats or only use it when count exceeds a threshold

---

## Finding 3: CRITICAL - 14/16 Teacher Pages Are Empty Shells

**Severity:** Critical | **Likelihood:** Certain | **Impact:** High (user disappointment, credibility)

Of 16 published teacher pages, **14 show only "Passages coming soon"** with zero actual content:

Arthur Osborne, Ashtavakra, Bill Watterson, Eckhart Tolle, Hazrat Mirza Ghulam Ahmad, Huang Po, Mirza Tahir Ahmad, Nisargadatta Maharaj, ONE, Osho, Robert Adams, Seung Sahn, Sri Muruganar, Takehiko Inoue

**Root cause:** `generate-book-links.py` groups quotes by source, but most quotes cite **books**, not teachers. The teacher pages are populated separately and most have metadata (`tradition`, `core_teaching`) which keeps them un-drafted, but they have no passage links.

**Impact:** A user navigates to "Teachers > Nisargadatta Maharaj" expecting content and finds nothing. This is a dead end that damages the site's apparent completeness.

**Mitigation:**
1. Add teacher-to-book cross-references (e.g., Nisargadatta page links to "Consciousness and the Absolute", "The Nectar of Immortality")
2. Or: generate teacher passage lists by matching book author to teacher name
3. Consider drafting teacher pages with no real content until they have substance

---

## Finding 4: HIGH - All 446 Published Quotes Have No Title

**Severity:** High | **Likelihood:** Certain | **Impact:** Medium-High (SEO, accessibility, browser tabs)

**Every single published quote** (446/446) has no `title` field in frontmatter. Quartz falls back to the filename for page titles, meaning browser tabs and search results show filenames like:

- "Abhyasa consists in withdrawal within the Self every time you are disturbed by thought"
- "absolute consciousness that there is no way to know that there is nothing to know that there is nobo"

The second example is **truncated mid-word** due to filename length limits.

**Impact:**
- SEO: `<title>` and `og:title` will be ugly truncated filenames
- Browser tabs: unreadable
- Social sharing: looks unprofessional when shared on Twitter/Facebook
- Accessibility: screen readers will announce these long filenames

**Mitigation:**
1. Add a script to generate `title` from the filename (clean up, truncate elegantly at 60 chars with ellipsis)
2. Or add a `title` field during the editing pass

---

## Finding 5: HIGH - 7 Published Quotes Contain OCR Artifacts

**Severity:** High | **Likelihood:** Certain | **Impact:** Medium

Seven published quotes contain **standalone page numbers** visible in the content body:

| Quote | Artifact |
|-------|----------|
| Before its birth it does not exist... | `172` |
| Detachment from worldly desires... | `94` |
| Learn how to be entirely unreceptive... | `118` |
| Restrain each single thought... | `122` |
| The Gateway of Non-Duality... | `120` |
| This chapter deals with all the preparatory steps... | `369` |
| You will recognize all minds as One... | `122` |

Additionally, 3 quotes have raw URLs in the body (not formatted as links).

**Impact:** Visible to readers. Looks like unfinished OCR processing. Undermines trust.

**Mitigation:**
1. Strip standalone numeric lines from published quote bodies (regex: `^\d{1,4}$`)
2. Convert raw URLs to markdown links
3. Add a quality gate to the Edited flag workflow

---

## Finding 6: HIGH - 20 Published Quotes Have No Source Attribution

**Severity:** High | **Likelihood:** Certain | **Impact:** Medium-High

20 quotes marked `Edited: true` have empty or missing `source` fields. These include IMG_1292, IMG_1293 (which also have `draft: true` so they're safe), but also:

- "I have already finished saving all people"
- "If you examine to whom those thoughts belong, bondage will cease"
- "seeking out the Self by constant enquiry and search"
- "Dont act out of your knowledge but act out of your consciousness"
- And 16 others

**Impact:** These quotes appear on the site with no attribution. For a spiritual wisdom library, unattributed quotes are a credibility and copyright concern. They also won't appear on any book page, making them orphaned.

**Mitigation:**
1. Audit and fix source attribution for all 20
2. Add a validation step: `Edited: true` requires non-empty `source`

---

## Finding 7: HIGH - Random Quote Pool Is 43% Incomplete

**Severity:** High | **Likelihood:** Certain | **Impact:** Medium

`randomquote.inline.ts` contains **252 quotes**, but **446 are published**. This means 194 published quotes (43%) are never shown in the Daily Wisdom rotation on the homepage.

**Impact:** Repeat visitors see the same subset. Newer content is invisible in the flagship feature.

**Mitigation:**
1. Regenerate `randomquote.inline.ts` from all published quotes
2. Add this regeneration to the build pipeline or a pre-deploy script

---

## Finding 8: MEDIUM - Pipeline Single Point of Failure (Edited Flag)

**Severity:** Medium | **Likelihood:** Medium | **Impact:** High if triggered

The entire content pipeline depends on `Edited: true/false` in frontmatter. The `generate-book-links.py` script (line 79) gates ALL quote inclusion on this single boolean. A script that accidentally sets `Edited: false` (the bug that already happened once per `edited-flag-audit-20260323.md`) would:

1. Remove all passages from all book pages
2. Set books to `draft: true`
3. Effectively blank the entire site

**Evidence:** The `revert-false-edited.py` script in `scripts/` exists as a recovery tool, proving this failure mode has already occurred.

**Mitigation:**
1. Add a sanity check to `generate-book-links.py`: if published count drops > 20% from previous run, abort with warning
2. Add git pre-commit validation that rejects mass Edited flag changes
3. Consider a separate `published` field distinct from `Edited` to separate content quality status from publish status

---

## Finding 9: MEDIUM - Tradition Representation Skew

**Severity:** Medium | **Likelihood:** N/A (design issue) | **Impact:** Medium

The tradition distribution is heavily skewed:

| Tradition | Books |
|-----------|-------|
| Advaita Vedanta | 18 |
| Fiction | 6 |
| Hindu | 5 |
| Multiple | 4 |
| Contemporary | 3 |
| Zen | 3 |
| Islamic | 3 |
| Sufi | 2 |
| Buddhist | 2 |
| **Christian** | **1** |
| **Sikh** | **1** |

Advaita Vedanta dominates at 37.5% of all books. Christianity and Sikhism each have only 1 book. Buddhism (the world's 4th largest religion) has only 2 books.

**Impact:** The site claims to serve "Advaita Vedanta, Sufism, Christianity, Sikhism, Zen, or any tradition of inner inquiry" but the representation is lopsided. A Christian or Sikh visitor might feel this is an Advaita Vedanta site with token representation of other traditions.

**Mitigation:**
1. Add disclaimer about current coverage being a work in progress
2. Prioritize adding books from underrepresented traditions
3. Consider a "Traditions" page that explains the roadmap

---

## Finding 10: MEDIUM - OG Images Disabled (SEO/Social Sharing Penalty)

**Severity:** Medium | **Likelihood:** Certain | **Impact:** Medium

In `quartz.config.ts` line 89: `// Plugin.CustomOgImages()` is commented out. This means every page shares the same generic `og-image.png` (39 KB) instead of having unique social cards.

**Impact:** When anyone shares a specific quote or book page on Twitter/Facebook/Discord, the preview will show the same generic image. This kills click-through rates on social sharing -- the primary viral growth mechanism for a content site.

**Mitigation:**
1. Re-enable `CustomOgImages` (it was disabled for build speed)
2. Or use Cloudflare Workers to generate OG images on-demand

---

## Finding 11: MEDIUM - Dead-End Navigation (425 Quote Pages)

**Severity:** Medium | **Likelihood:** High | **Impact:** Low-Medium

**425 out of 446 published quotes have zero outbound links in their body**. While Quartz provides backlinks and breadcrumbs in the sidebar, the quote body itself is a dead end. A reader finishes the quote and has no "read next" or "explore similar" prompt.

**Impact:** Lower engagement, higher bounce rates. The user reads one quote and leaves.

**Mitigation:**
1. Add "More from this book" links at the bottom of each quote
2. Add "Related quotes" based on shared tags
3. Add a "Random Next Quote" button

---

## Finding 12: MEDIUM - No robots.txt

**Severity:** Medium | **Likelihood:** Certain | **Impact:** Low-Medium

There is no `robots.txt` in `quartz/static/`. The sitemap IS enabled (via `ContentIndex` with `enableSiteMap: true`), which is good. But without a `robots.txt` pointing to the sitemap, crawlers may not discover it efficiently.

**Evidence:** `quartz/static/` contains only `giscus/`, `icon.png`, and `og-image.png`.

**Mitigation:**
1. Add `quartz/static/robots.txt` with: `Sitemap: https://wisdomcompiler.com/sitemap.xml`

---

## Risk Matrix

| # | Finding | Severity | Likelihood | Risk Score |
|---|---------|----------|------------|------------|
| 1 | 668 MB unoptimized images | CRITICAL | Certain | **10** |
| 2 | False homepage claims (600+ quotes, Concepts 404) | CRITICAL | Certain | **10** |
| 3 | 14/16 teacher pages empty | CRITICAL | Certain | **9** |
| 4 | No title on any quote (SEO/UX) | HIGH | Certain | **8** |
| 5 | OCR artifacts in published quotes | HIGH | Certain | **7** |
| 6 | 20 quotes with no source attribution | HIGH | Certain | **7** |
| 7 | Random quote pool 43% incomplete | HIGH | Certain | **6** |
| 8 | Edited flag single point of failure | MEDIUM | Medium | **6** |
| 9 | Tradition representation skew | MEDIUM | Permanent | **5** |
| 10 | OG images disabled | MEDIUM | Certain | **5** |
| 11 | Dead-end quote navigation | MEDIUM | High | **4** |
| 12 | No robots.txt | MEDIUM | Certain | **3** |

---

## Top 10 Prioritized Actions

1. **Fix homepage claims NOW** -- change "600+" to live `quoteCount`, remove or create Concepts section. (30 min, eliminates credibility risk)
2. **Add robots.txt** -- 2 minutes, easy SEO win
3. **Regenerate randomquote.inline.ts** -- run script to include all 446 quotes. (5 min)
4. **Strip OCR page numbers from 7 quotes** -- quick regex cleanup. (10 min)
5. **Fix 20 unattributed quotes** -- audit source fields. (30 min)
6. **Add teacher-to-book cross-references** -- so 14 empty teacher pages link to their books. (1 hour)
7. **Add title field to all quotes** -- script to generate from filename. (30 min)
8. **Image optimization pipeline** -- convert PNGs to WebP, resize to 1200px max. (2 hours for script + run)
9. **Add sanity check to generate-book-links.py** -- abort if published count drops >20%. (15 min)
10. **Re-enable CustomOgImages or add Cloudflare Image Workers** -- for social sharing cards. (1 hour)

---

## Positive Observations

- **Draft filtering works correctly.** The `RemoveDrafts()` plugin is active and all unedited quotes have `draft: true`. No draft content leaks.
- **SEO meta tags are solid.** `Head.tsx` generates proper `og:title`, `og:description`, `twitter:card`, `meta description` for every page.
- **Mobile CSS is present.** All custom components have `@media (max-width: 800px)` breakpoints.
- **Sitemap and RSS are enabled.** The `ContentIndex` plugin generates both.
- **Backlinks work.** Quartz's built-in backlink component provides some inter-page navigation.
- **The `ignorePatterns`** correctly excludes `.obsidian`, `private`, `templates`, and `Book Source PDFs` from the build.

---

*Generated by Red Team audit, 2026-03-26. All findings verified against source code and content files.*
