# WisdomCompiler Comprehensive Audit
**Date:** 2026-03-26
**Method:** Council (7-perspective debate) + Red Team + Browser testing + Direct pipeline analysis
**Live Site:** https://wisdomcompiler.com/

---

## Executive Summary

**Overall Grade: 6.3/10 → estimated 7.5/10 after fixes** — Major issues resolved in single session.

The site has a thoughtful content model, clean architecture, warm non-dogmatic design, and genuinely curated spiritual content. After this session's fixes: homepage claims are accurate, 15/16 teacher pages are populated, images dropped 90% (669→67MB), all quotes have titles for SEO, CustomOgImages enabled, robots.txt added, and pipeline has sanity checks. Remaining gaps: Wisdom Quotes listing needs filtering, traditions need broadening, analytics not yet enabled, 9 broken .txt links unfixed.

---

## 0. FIXES APPLIED (2026-03-26 session)

| # | Fix | Status | Evidence |
|---|-----|--------|----------|
| 1 | **Restored 167 incorrectly-reverted `Edited: true` flags** | ✅ Done | Git archaeology: compared `5bf9dbe` baseline (202 files) to working tree, restored all that were incorrectly flipped to false. 13 renamed files handled. |
| 2 | **Regenerated book/teacher passage links** | ✅ Done | `generate-book-links.py` re-run, 47 books with passages, all links restored. |
| 3 | **Fixed 14/16 empty Teacher pages** — added book→teacher traversal | ✅ Done | New `build_teacher_book_map()` in `generate-book-links.py` traverses book `teacher:` frontmatter. 15/16 teachers now have passage links. Ramana: 12→151, Huang Po: 0→29, Nisargadatta: 0→19, etc. Arthur Osborne remains 0 (no books/quotes in vault). |
| 4 | **Deployed to Cloudflare Pages** | ✅ Done | 1210 files emitted, 463 new files uploaded. |
| 5 | **Fixed homepage false claims** — "600+" → "Hundreds of", Concepts link → /tags/ | ✅ Done | index.md and HomepageExplore.tsx updated. "40+" → "48". Concepts slug fixed from 404. |
| 6 | **Added robots.txt** | ✅ Done | `quartz/static/robots.txt` with Sitemap URL. |
| 7 | **Regenerated random quote pool** | ✅ Done | `randomquote.inline.ts` regenerated from all 234 published quotes. Created reusable `scripts/regenerate-quotes.py`. |
| 8 | **Stripped OCR page numbers** from 5 published quotes | ✅ Done | Standalone numbers (94, 118, 120, 122) removed from quote bodies. |
| 9 | **Attributed 3 unattributed quotes** to Osho | ✅ Partial | 10 remain unattributed (need manual image identification). |
| 10 | **Added title field** to all 234 published quotes | ✅ Done | Generated from filename, truncated at 60 chars. Fixes SEO and browser tabs. |
| 11 | **Image optimization: 669MB → 67MB** (90% reduction) | ✅ Done | 653 images converted PNG/JPG → WebP, max 1200px, quality 80. Zero errors. All references updated. |
| 12 | **Added sanity check** to generate-book-links.py | ✅ Done | 20% drop threshold with `--force` override. Prevents accidental mass link deletion. |
| 13 | **Re-enabled CustomOgImages** plugin | ✅ Done | Social sharing cards now generated per-page. |

### Updated Metrics After All Fixes
- Published Wisdom Quotes: **234** (draft:false) / **446** (Edited:true)
- Teachers with passage links: **15/16** (up from 2/16)
- Ramana Maharshi passages: **151** (up from 12)
- Image directory size: **67MB** (down from 669MB — 90% reduction)
- Random quote pool: **234** (matches published set exactly)
- All published quotes have title fields for SEO

---

## I. SITE SNAPSHOT (Verified)

| Metric | Count |
|--------|-------|
| Books (non-draft) | 48 |
| Teachers | 16 |
| Published Wisdom Quotes (`draft: false`) | 234 |
| Draft Wisdom Quotes | 223+ |
| Quotes in Random Pool (hardcoded) | 253 |
| Wisdom Threads | 3 |
| Concept Tags | 16 |
| Traditions Represented | 11 |
| Homepage features | DailyWisdom, HomepageExplore, WisdomQuiz, Search, Dark/Reader mode |

### Tradition Distribution (by published quotes via books)
| Tradition | Books | ~Quotes |
|-----------|-------|---------|
| Advaita Vedanta | 18 | ~258 |
| Fiction/Manga | 6 | ~22 |
| Hindu (non-Advaita) | 5 | ~9 |
| Islamic | 3 | ~29 |
| Zen | 3 | ~31 |
| Contemporary | 3 | ~3 |
| Sufi | 2 | ~12 |
| Buddhist | 2 | ~8 |
| Multiple/Cross-tradition | 4 | ~17 |
| Sikh | 1 | ~3 |
| Christian | 1 | ~4 |

**Missing traditions:** Taoism, Theravada Buddhism, Jewish mysticism, Christian mysticism, Indigenous, Shinto

---

## II. COUNCIL FINDINGS (7 Perspectives)

### Ratings by Perspective
| Perspective | Rating | Top Issue |
|-------------|--------|-----------|
| First-Time Spiritual Seeker | 7/10 | Quote titles are opaque — no scannable summaries |
| UX Designer | 6/10 | Wisdom Quotes listing is an unusable wall of text |
| Content Strategist | 6/10 | 400+ quotes in draft limbo; stale "600+" copy |
| Technical Architect | 8/10 | No analytics; OG images commented out |
| Accessibility Advocate | 5/10 | Quote images lack alt text; color contrast gaps |
| Comparative Religion Scholar | 6/10 | Massive Advaita Vedanta skew; missing foundational texts |
| Return Visitor / Power User | 5/10 | No "what's new for me" mechanism; only Daily Wisdom as hook |

### Universal Agreements (all 7 perspectives)
1. **Content model is strong but underutilized** — rich frontmatter, cross-linking, Threads concept
2. **Wisdom Quotes listing is the weakest page** — flat list of 234 long-titled items, no filtering
3. **Draft backlog is the elephant in the room** — 400+ quotes in limbo
4. **Stale copy undermines trust** — "600+ passages" claim vs 234 published
5. **Cross-tradition balance needs work** — Advaita is 37% of books

### Disagreements
- **Fiction inclusion**: Strength (inclusive wisdom) vs jarring (manga next to Gita)
- **Screenshot images**: Authenticity proof vs accessibility barrier
- **Quiz**: Engagement mechanism vs one-time-only interaction

---

## III. PIPELINE INTEGRITY

### Strengths
- Build is fast and reliable: 742 files → 1210 emitted in 18s
- RemoveDrafts filter properly excludes 242+ draft files
- Cloudflare Pages deployment works cleanly (463 new files on latest deploy)
- All 6 homepage navigation links return 200
- Deep pages (book, teacher, quote) all return 200
- Custom components properly registered in index.ts

### Issues Found
1. **9 broken `.txt]]` wiki-links** across 7 files (identified in prior audit, never fixed)
   - Files: Huang Po, Thread of Ego, Ramana Periya Purnam, Talks with Ramana Maharshi, The Ribhu Gita, The Zen Teaching of Huang Po, Yoga Vasistha
   - Fix: Remove `.txt` from 9 wiki-links (simple string replacement)

2. ~~**randomquote.inline.ts hardcodes 253 quotes**~~ — **FIXED.** Regenerated with all 234 published quotes. Created `scripts/regenerate-quotes.py` for future re-runs.

3. ~~**generate-book-links.py `Edited: true` filter fragile**~~ — **MITIGATED.** Added 20% sanity check threshold that aborts on mass link drops. Use `--force` to override.

4. ~~**14 of 16 Teachers have 0 passage links**~~ — **FIXED.** Added `build_teacher_book_map()` to `generate-book-links.py` that traverses book→teacher frontmatter. 15/16 teachers now populated.

5. **Berzerk is the only book with 0 passage links** — no published quotes reference it

6. **Osho teacher page missing `recommended_start` field**

---

## IV. CONNECTIVITY MAP

```
Homepage ─→ Books (200) ─→ Individual Book (200) ─→ Passage Links ─→ Quote (200) ✓
         ─→ Teachers (200) ─→ Individual Teacher (200) ─→ Passage Links ─→ Quote
                                                          ✅ 15/16 teachers have links (FIXED)
         ─→ Wisdom Quotes (200) ─→ Individual Quote (200) ✓
         ─→ Concepts (200) ─→ Tag pages ─→ Quotes ✓ (but may be sparse)
         ─→ Threads (200) ─→ Individual Thread ─→ Cross-linked quotes ✓
         ─→ Updates (200) ✓
```

**Dead ends identified:**
- 14 Teacher pages with "Passages coming soon" — no outbound links to quotes
- Concepts tag pages may have sparse results for some tags
- Quote pages link back to source book but NOT to teacher

---

## V. PRIORITIZED ACTION ITEMS

### Critical (Do This Week)
| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 1 | ~~**Fix stale "600+" copy**~~ | ✅ DONE | "Hundreds of" in index.md + HomepageExplore. Concepts → /tags/. |
| 2 | **Fix 9 broken `.txt]]` wiki-links** across 7 files | 15 min | Broken navigation links |
| 3 | **Add Cloudflare Web Analytics** (free, privacy-respecting) | 15 min | Unlocks data-driven decisions |
| 4 | ~~**Uncomment CustomOgImages**~~ | ✅ DONE | Plugin re-enabled in quartz.config.ts |

### High Priority (This Month)
| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 5 | **Add filtering/grouping to Wisdom Quotes listing** | 4-8 hrs | Transforms largest section from unusable to navigable |
| 6 | ~~**Fix Teacher page passage links**~~ | ✅ DONE | 15/16 teachers populated via book→teacher traversal |
| 7 | ~~**Triage draft backlog**~~ | ✅ PARTIAL | Edited flag restoration recovered 167 quotes. Remaining drafts need OCR cleanup. |
| 8 | ~~**Auto-generate random quote pool**~~ | ✅ DONE | Regenerated with 234 published quotes. Script: `scripts/regenerate-quotes.py` |

### Medium Priority (This Quarter)
| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 9 | **Add 5-7 foundational texts** from missing traditions | 8-16 hrs | Legitimizes "world's wisdom" claim |
| 10 | **Add alt text to quote images** | 2-4 hrs | Accessibility compliance |
| 11 | **Create 3-5 more Wisdom Threads** | 8-16 hrs | Crown jewel feature needs volume |
| 12 | **Add "Random Quote" button** beyond Daily Wisdom | 2 hrs | Return-visit engagement |
| 13 | **Audit WCAG color contrast** for secondary text | 2 hrs | Accessibility |

### Also Completed (Red Team Top 10)
| # | Action | Status |
|---|--------|--------|
| RT-1 | ~~Homepage false claims~~ | ✅ DONE (same as #1) |
| RT-2 | ~~robots.txt~~ | ✅ DONE — `quartz/static/robots.txt` with Sitemap |
| RT-3 | ~~Random quote pool~~ | ✅ DONE (same as #8) |
| RT-4 | ~~OCR page numbers~~ | ✅ DONE — 5 standalone numbers stripped |
| RT-5 | ~~Unattributed quotes~~ | ✅ PARTIAL — 3 attributed to Osho, 10 need manual image review |
| RT-6 | ~~Teacher pages~~ | ✅ DONE (same as #6) |
| RT-7 | ~~Title fields on quotes~~ | ✅ DONE — 234 titles generated from filenames |
| RT-8 | ~~Image optimization~~ | ✅ DONE — **669MB → 67MB (90% reduction)**, 653 images to WebP |
| RT-9 | ~~Sanity check in script~~ | ✅ DONE — 20% threshold abort in generate-book-links.py |
| RT-10 | ~~CustomOgImages~~ | ✅ DONE (same as #4) |

### Nice to Have (Someday)
| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 14 | "I'm feeling..." emotional entry point | 4-8 hrs | Meets seekers where they are |
| 15 | Reading history / favorites (localStorage) | 8 hrs | Power user retention |
| 16 | Recently Added auto-generated section | 4 hrs | Return visit freshness |
| 17 | ARIA attributes on WisdomQuiz | 4 hrs | Full accessibility |

---

## VI. WHAT'S WORKING WELL

1. **Wisdom Threads** — The Thread of Surrender is genuinely excellent comparative mysticism
2. **BookMeta component** — Tradition badges, difficulty, teacher links, "Explore similar"
3. **Warm, non-dogmatic tone** — "This is not a teaching. This is a compass."
4. **Free online book links** — Every book page links to free full text where available
5. **Build pipeline** — Obsidian → Quartz → Cloudflare is simple, fast, and reliable
6. **Homepage design** — DailyWisdom + HomepageExplore + Quiz provides multiple entry points
7. **Fiction inclusion** — Signals wisdom can be found anywhere
8. **Rich frontmatter schema** — tradition, difficulty, teacher, tags ready for future features

---

## VII. THE BIG PICTURE

WisdomCompiler's core identity tension: **Is it a Ramana Maharshi library that also includes other traditions, or is it truly a cross-tradition wisdom library?**

The answer will determine priorities:
- If **Ramana-centered**: The current Advaita skew is a feature, not a bug. Focus on completing the Ramana/Advaita content (many drafts), fix the pipeline issues, and own the niche.
- If **cross-tradition**: The missing foundational texts (Tao Te Ching, Dhammapada, Rumi, Meister Eckhart) are urgent. The tradition balance needs active reweighting.

Either answer is valid. But the homepage copy ("world's timeless spiritual wisdom") promises cross-tradition. If that's the vision, the content needs to grow beyond its Advaita roots.

---

*Sources: Council debate (7 perspectives), direct pipeline analysis, link connectivity testing, prior audit reports (link-audit-20260323, edited-flag-audit-20260323)*
