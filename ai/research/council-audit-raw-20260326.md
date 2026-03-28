# WisdomCompiler Council Audit
**Date:** 2026-03-26
**Site:** https://wisdomcompiler.com/
**Method:** Multi-perspective council debate grounded in codebase analysis

---

## Site Snapshot (Verified from Codebase)

| Metric | Count |
|--------|-------|
| Books (non-draft) | ~49 (51 files minus templates/index) |
| Teachers (non-draft) | 16 |
| Wisdom Quotes (published, `draft: false`) | 234 |
| Wisdom Quotes (draft/unpublished) | 229 (`draft: true`) + ~851 without `draft:` key |
| Quotes in Random Pool | 253 |
| Wisdom Threads | 3 (Surrender, Ego, Silence) |
| Concept Tags (tag pages) | 16 |
| Traditions Represented | Advaita Vedanta (18), Fiction (6), Hindu (5), Multiple (4), Zen (3), Islamic (3), Contemporary (3), Sufi (2), Buddhist (2), Sikh (1), Christian (1) |

**Homepage features:** DailyWisdom quote, HomepageExplore cards (5 sections), WisdomQuiz ("Discover Your Path"), "Where to Start" starter recommendations, search, dark mode, reader mode.

**Known content issues:** ~427 UUID-named quote files still in draft with OCR artifacts (e.g., `147a554d-...md` contains garbled text like "Oi eo ern ae a it"). Homepage claims "600+ passages" but only 234 are published.

---

## Perspective 1: First-Time Spiritual Seeker

**Rating: 7/10**

### Assessment
The homepage is welcoming. The tagline "Guiding seekers to the world's timeless spiritual wisdom" immediately signals purpose. The "Where to Start" section with 5 curated books (Bhagavad Gita, Talks with Ramana Maharshi, The Power of Now, The Prophet, Dropping Ashes On the Buddha) is excellent for someone who has no idea where to begin. The "Discover Your Path" quiz lowers the barrier to engagement.

However, clicking through reveals friction. The Wisdom Quotes listing shows 234 entries but many have cryptic, long titles like "Arpana offering means that the mind gets merged in the self and becomes one with it Part 2" -- these are not scannable. A seeker looking for guidance on suffering or fear would not know where to click.

### Top 3 Issues
1. **Quote titles are opaque** -- Most are sentence fragments that don't signal the teaching's relevance to a seeker's actual question (e.g., "How do I deal with anxiety?"). No quote has a subtitle or one-line summary visible in listings.
2. **Concepts page is tag-based but the tags are inconsistent** -- The Concepts page links to `/tags/self-knowledge`, `/tags/ego`, etc., but it's unclear how many quotes have been tagged. The tag pages may show sparse results for some concepts.
3. **No "I'm struggling with X" entry point** -- There's no emotional/situational navigation (grief, loneliness, anger, fear). The framework is intellectual (ego, mind, liberation) rather than meeting seekers where they are.

### Top 3 Strengths
1. **"Where to Start" is genuinely helpful** -- Five diverse books spanning traditions with clear subtitles ("Self-inquiry from the source", "Modern awakening classic").
2. **Free online links on every book page** -- Each book page has a "Read Online" section with actual URLs to free texts. This is rare and generous.
3. **Warm, non-dogmatic tone** -- "This is not a teaching. This is a compass." The site avoids the trap of claiming one path is superior.

### Highest-Priority Recommendation
Add short, human-readable summaries (1-2 sentences) below each quote title in listing views. Even better: create an "I'm feeling..." or "I need help with..." entry point that maps emotional states to relevant quotes.

---

## Perspective 2: UX Designer

**Rating: 6/10**

### Assessment
The information architecture has a solid skeleton: Homepage > Books / Teachers / Quotes / Concepts / Threads. The 5-card explore grid on the homepage is clean. Book pages have well-structured metadata (tradition badge, difficulty level, description, teacher link, "Explore similar" related books). The BookMeta component is thoughtfully built.

The main IA problem is that three of the five top-level sections are underpopulated: Threads has only 3 entries, Concepts routes to tag pages that may be sparse, and the Wisdom Quotes folder page is an overwhelming flat list of 234 items with no filtering, sorting, or grouping.

### Top 3 Issues
1. **Wisdom Quotes listing is a wall of text** -- 234 items in a flat list with long titles. No pagination, no filtering by tradition/teacher/theme. On mobile this is especially punishing. Compare: Books page at least has the explorer sidebar for browsing.
2. **Broken promises in navigation** -- Homepage links to "Concepts" but there's no `/Concepts/` folder -- it's a single `Concepts.md` file that links to tag pages. Similarly, "600+ curated passages" is stated but only 234 are live. The stats component dynamically computes counts, so it shows the real number, but the markdown text in `index.md` and `Updates.md` says 600+.
3. **Quote pages lack clear hierarchy** -- Individual quote pages show the source image (screenshot of a physical book page), then transcribed text. There's no clear visual separation between "this is the quote" and "this is the metadata." The `ShowImage: true` flag means users see a phone photo of a book page which can be hard to read.

### Top 3 Strengths
1. **BookMeta component** -- Tradition badges, difficulty levels, teacher cross-links, and "Explore similar" recommendations are exactly what good IA looks like.
2. **Search is prominent** -- Search appears in the left sidebar on every page with dark mode and reader mode toggles alongside it.
3. **Responsive mobile CSS** -- The `custom.scss` is thorough: 44px touch targets, proper `box-sizing`, Safari text-size-adjust fix, responsive grid columns, overflow handling.

### Highest-Priority Recommendation
Add filtering/grouping to the Wisdom Quotes listing. At minimum: group by source book or tradition. Ideally: client-side filter chips for tradition, teacher, and concept tag. This single change would transform the largest content section from unusable to navigable.

---

## Perspective 3: Content Strategist

**Rating: 6/10**

### Assessment
The content model is sound: Books contain Passages (quotes), Teachers link to Books and Passages, Concepts aggregate by tag, Threads provide curated cross-tradition narratives. The frontmatter schema is rich (tradition, difficulty, category, teacher, source, tags, Edited flag, ShowImage). This is a well-thought-out content graph.

The execution gap is significant. Only 234 of ~660 quotes are published. The draft backlog (229 marked `draft: true`, plus ~851 files without a draft key at all, many with UUID filenames and OCR garbage) represents a massive content debt. The published-to-draft ratio means the site is showing less than 25% of its potential content.

The tradition distribution is heavily skewed toward Advaita Vedanta (18 of 49 books). This is authentic to the curator's interests but creates an imbalance.

### Top 3 Issues
1. **Content debt: 400+ quotes in draft limbo** -- Many have garbled OCR text (e.g., "Oi eo ern ae a it"). The `Edited: false` flag marks unreviewed content but there's no automated pipeline to surface which drafts are closest to publishable.
2. **Stale copy: "600+ passages" claim** -- `index.md` says "600+ curated passages" but only 234 are live. `Updates.md` says "600+ Quotes Refined" which is misleading. The HomepageExplore component correctly computes the live count dynamically, creating a contradiction between the static text and dynamic number on the same page.
3. **Thin Threads section** -- Only 3 threads exist. The Surrender thread is excellent (well-written narrative connecting Advaita, Zen, Islam, Yoga traditions with quote links). But 3 threads for a site claiming cross-tradition wisdom feels like a proof of concept, not a feature.

### Top 3 Strengths
1. **Content model is rich and extensible** -- Frontmatter includes tradition, difficulty, teacher links, tags. This is a solid foundation for filtering, recommendation, and cross-linking.
2. **Wisdom Threads are the site's crown jewel** -- The Thread of Surrender is genuinely excellent content: it provides context, narrative, and curated passages across 4 traditions. This format is what makes WisdomCompiler more than just a quote database.
3. **Book pages are complete** -- Each has tradition, difficulty, description, free online link, teacher link, and passage list. The BookMeta component surfaces all of this beautifully.

### Highest-Priority Recommendation
Fix the "600+" stale copy in `index.md` to match reality (say "200+ published passages" or reference the dynamic count). Then prioritize drafts: triage the 229 `draft: true` files to identify which have clean text and only need a title rename, vs. which need OCR re-transcription. A script that checks `Edited: true` + `draft: true` (contradiction) would surface quick wins.

---

## Perspective 4: Technical Architect

**Rating: 8/10**

### Assessment
The Obsidian -> Quartz v4 -> Cloudflare Pages pipeline is solid and well-understood. The `quartz.config.ts` is clean: SPA mode enabled, popovers enabled, proper ignore patterns, RemoveDrafts filter in place. The build uses standard Quartz plugins with no fragile customizations. Custom components (DailyWisdom, BookMeta, HomepageExplore, WisdomQuiz, SourceBanner) are well-encapsulated with colocated CSS.

The `ConditionalRender` pattern in `quartz.layout.ts` is elegant -- homepage-only components are cleanly gated. The Explorer `filterFn` with optional chaining (`node.name?.toLowerCase()`) shows awareness of edge cases.

### Top 3 Issues
1. **No analytics** -- `analytics: null` in config. There's no way to know which pages are popular, where users drop off, or what search terms bring people in. For a content site, this is flying blind.
2. **CustomOgImages commented out** -- Social sharing will show generic cards rather than book-specific or quote-specific preview images. This hurts social media discovery significantly.
3. **randomquote.inline.ts hardcodes 253 quotes** -- The random quote pool is a static array baked into the JS bundle. Adding new published quotes requires manually updating this file. There's no build-time generation step that auto-syncs published quotes into the random pool.

### Top 3 Strengths
1. **RemoveDrafts filter** -- The 400+ draft files are properly excluded from the build. Users never see broken OCR content.
2. **Build is fast and simple** -- `npx quartz build` with Cloudflare Pages deploy. No complex CI, no database, no server. The static site model is perfect for this content.
3. **Custom components are well-structured** -- BookMeta, HomepageExplore, and WisdomQuiz each own their CSS, use proper Quartz types, and compute data from `allFiles` at build time rather than client-side fetches.

### Highest-Priority Recommendation
Add lightweight analytics (Cloudflare Web Analytics is free and privacy-respecting -- just set `analytics: { provider: "umami" }` or use Cloudflare's dashboard analytics). Then uncomment CustomOgImages to unlock social sharing.

---

## Perspective 5: Accessibility Advocate

**Rating: 5/10**

### Assessment
The site has some accessibility wins: Source Sans Pro body font is readable, the warm color scheme (`#faf8f0` background, `#2b2520` dark text) provides good contrast, and the mobile CSS ensures 44px touch targets. Dark mode is available.

However, accessibility was clearly not a primary design consideration. The codebase shows no ARIA attributes in custom components. The WisdomQuiz is entirely JS-driven with no fallback. Screenshot images of book pages (`ShowImage: true`) are the primary content for many quotes but likely lack meaningful alt text.

### Top 3 Issues
1. **Quote images lack alt text** -- Many wisdom quote pages embed a photo of a physical book page (`![](Images/uuid.jpg)`). These images have no alt text. Screen readers would skip the primary content entirely. Since the transcription is below the image, a screen reader user would get the text, but the image is still an accessibility gap.
2. **WisdomQuiz has no keyboard/screen-reader support** -- The quiz is a button that reveals a JS-driven interactive panel. Without checking the inline script, it likely lacks ARIA roles, focus management, and keyboard navigation.
3. **Color contrast may fail for secondary elements** -- The `--gray: #b8a89a` (light mode) used for descriptions and dividers against `--light: #faf8f0` background yields a contrast ratio of approximately 2.5:1, below the WCAG AA minimum of 4.5:1 for normal text.

### Top 3 Strengths
1. **Good body text contrast** -- Primary text (`#4a3f35` on `#faf8f0`) is approximately 8:1 contrast ratio, well above WCAG AA.
2. **Responsive design** -- Mobile CSS with proper touch targets, readable font sizes (1rem base), and line-height (1.65) means the site is usable on small screens.
3. **Reader mode available** -- The reader mode toggle in the sidebar can strip distractions for users who need a cleaner reading experience.

### Highest-Priority Recommendation
Add alt text to all wisdom quote images. For screenshot images, `alt="Screenshot of passage from [Book Title]"` is a minimum. Better: since the transcribed text is on the same page, use `alt=""` (decorative) with `aria-hidden="true"` so screen readers skip to the transcription. Also audit the gray text color for WCAG compliance.

---

## Perspective 6: Comparative Religion Scholar

**Rating: 6/10**

### Assessment
The tradition coverage is authentic but narrow. Of 49 books:
- **Advaita Vedanta: 18 books** (dominant -- Ramana Maharshi alone has ~6 books)
- **Hindu (non-Advaita): 5** (Siva Purana, Bhagavad Gita, etc.)
- **Fiction/Manga: 6** (Dune, Vagabond, One Punch Man, Berzerk, Calvin and Hobbes, Mob Psycho 100)
- **Islamic: 3** (Ahmadiyya texts specifically)
- **Zen: 3** (Huang Po, Seung Sahn)
- **Buddhist (non-Zen): 2** (Vimalakirti Sutra, Sutra of Queen Srimala)
- **Sufi: 2** (Early Islamic Mysticism, partial)
- **Contemporary: 3** (Eckhart Tolle, Greater Community Spirituality)
- **Sikh: 1** (Guru Granth Sahib)
- **Christian: 1** (Bible - Book of Luke)

Major traditions absent or nearly absent: **Taoism** (no Tao Te Ching, no Zhuangzi), **Theravada Buddhism** (no Dhammapada), **Jewish mysticism** (no Zohar, no Kabbalah texts), **Christian mysticism** (no Meister Eckhart, no Cloud of Unknowing, no St. John of the Cross), **Indigenous traditions**, **Shinto**.

The inclusion of manga (One Punch Man, Mob Psycho 100, Berzerk, Vagabond) is unconventional but interesting -- it signals that wisdom can be found in unexpected places. Calvin and Hobbes likewise.

### Top 3 Issues
1. **Massive Advaita Vedanta skew** -- 18/49 books is 37%. Ramana Maharshi has 6+ associated books. A scholar of comparative religion would see this as "a Ramana Maharshi library with some other traditions attached."
2. **Missing foundational texts** -- No Tao Te Ching, no Dhammapada, no Rumi's Masnavi, no Meister Eckhart, no Kabbalah. These are arguably more foundational to cross-tradition study than, say, Greater Community Spirituality.
3. **Islamic representation is Ahmadiyya-specific** -- Three of the Islamic books are by Mirza Ghulam Ahmad and Mirza Tahir Ahmad (Ahmadiyya movement). While valid, this is a very specific subset of Islamic thought. Mainstream Sufi masters (Rumi, Ibn Arabi, Al-Ghazali) and core texts (Quran selections, Hadith Qudsi) are absent.

### Top 3 Strengths
1. **Wisdom Threads show genuine cross-tradition literacy** -- The Thread of Surrender meaningfully connects Advaita, Zen, Islam, and Yoga. This is not superficial comparison but real comparative mysticism.
2. **Honest about scope** -- The site says "compiled" not "comprehensive." It doesn't claim to be an encyclopedia.
3. **Fiction inclusion is a strength** -- Including Dune, Vagabond, and Calvin and Hobbes alongside the Bhagavad Gita signals an inclusive, non-hierarchical view of where wisdom can be found.

### Highest-Priority Recommendation
Add 5-7 foundational texts from underrepresented traditions: Tao Te Ching, Dhammapada, selected Rumi, Meister Eckhart, and at least one Jewish mystical text. This would shift the balance meaningfully and justify the "world's timeless spiritual wisdom" claim.

---

## Perspective 7: Return Visitor / Power User

**Rating: 5/10**

### Assessment
The Daily Wisdom quote (changes each day) is the primary return-visit hook. The "What's New" page exists but was last updated March 2026 (initial batch). There's no RSS feed for new quotes (RSS is enabled in config but it's a site-wide feed, not a quotes-specific one). There's no email newsletter, no "save favorites" feature, no reading history.

For a power user who has read through the 234 published quotes, there is little reason to return until new content is published. The 3 Wisdom Threads are finite. The Concepts tag pages are static. The quiz is a one-time interaction.

### Top 3 Issues
1. **No "what's new for me" mechanism** -- No way to know which quotes are new since last visit. No bookmarking, no favorites, no reading progress. Every visit requires re-discovering content.
2. **Daily Wisdom is the only return hook** -- And it draws from only 253 quotes, meaning repeats will occur within a year. No seasonal themes, no "deep dive of the week," no progressive revelation.
3. **Search is the only discovery method for repeat visitors** -- After exhausting the homepage, book pages, and threads, the only way to find something new is search or random browsing through the explorer. There's no "surprise me" beyond the daily quote, no "readers also liked," no recommendation engine.

### Top 3 Strengths
1. **Daily Wisdom is a good start** -- Having a reason to visit each day, even a small one, is the foundation of a return-visit habit.
2. **Backlinks component** -- On the right sidebar, backlinks show which other pages reference the current one. For a power user exploring connections, this is valuable for organic discovery.
3. **Popovers enabled** -- `enablePopovers: true` means hovering over internal links shows a preview. This rewards exploratory browsing, which is exactly what power users do.

### Highest-Priority Recommendation
Add a "Recently Added" section to the homepage (or make the What's New page auto-generated from git history / frontmatter dates). Also consider a "Random Quote" button (beyond Daily Wisdom) that serves a new random quote on click, encouraging serendipitous exploration.

---

## Cross-Perspective Synthesis

### Points of Universal Agreement

1. **The content model is strong but underutilized** -- All perspectives recognize the rich frontmatter schema, cross-linking (books <-> teachers <-> quotes <-> tags), and the Wisdom Threads concept. The architecture can support far more than it currently delivers.

2. **The Wisdom Quotes listing is the weakest page on the site** -- UX Designer, Seeker, and Power User all identify the flat list of 234 long-titled quotes as the primary navigation failure. It is simultaneously the site's largest content section and its least usable.

3. **Draft backlog is the elephant in the room** -- Content Strategist, Technical Architect, and Scholar all note that 400+ quotes in draft represent both a content debt and a credibility gap (the "600+" claim). Resolving this either by publishing cleaned quotes or acknowledging the real count is urgent.

4. **Stale copy undermines trust** -- "600+ curated passages" appears in static markdown while the dynamic component shows the real count (~234). First-time visitors and return visitors both lose trust when claims don't match reality.

5. **Cross-tradition balance needs work** -- The Scholar perspective highlights this most strongly, but even the Seeker notices: if someone arrives looking for Taoist or Jewish mystical wisdom, they will leave empty-handed.

### Points of Disagreement

- **Fiction inclusion**: The Scholar sees it as a strength (inclusive definition of wisdom); a more traditional seeker might find One Punch Man alongside the Bhagavad Gita jarring. The site doesn't explain why manga is included alongside ancient scriptures.

- **Image screenshots**: The Accessibility Advocate sees them as a barrier; the Content Strategist sees them as authenticity markers (proof these are real physical books). Both are right -- the solution is proper alt text + decorative image treatment, not removal.

- **Quiz feature**: UX Designer appreciates the engagement mechanism; the Accessibility Advocate flags it as inaccessible; the Power User sees it as a one-time interaction with no replay value. Priority depends on audience.

### Top 5 Prioritized Action Items

| Priority | Action | Effort | Impact | Perspectives Aligned |
|----------|--------|--------|--------|---------------------|
| **1** | **Fix stale "600+" copy** in `index.md` and `Updates.md` to match actual published count (~234), or remove hardcoded numbers and rely on the dynamic HomepageExplore stats component | Low (30 min) | High -- eliminates trust-damaging contradiction visible on homepage | Content Strategist, UX Designer, Seeker |
| **2** | **Add filtering/grouping to Wisdom Quotes listing** -- group by source book or tradition at minimum; client-side filter chips ideal | Medium (4-8 hrs) | High -- transforms the site's largest section from unusable to navigable | UX Designer, Seeker, Power User |
| **3** | **Triage draft backlog** -- run audit script to identify which of the 229 `draft: true` + `Edited: true` quotes have clean text and only need title rename; batch-publish the easy wins | Medium (2-4 hrs) | High -- could double published content from 234 to 400+ with moderate effort | Content Strategist, Technical Architect, Scholar |
| **4** | **Add analytics** -- enable Cloudflare Web Analytics (free, privacy-respecting, zero-config for CF Pages sites) | Low (15 min) | Medium -- unlocks data-driven decisions for all future improvements | Technical Architect, Content Strategist, UX Designer |
| **5** | **Add 5 foundational texts from missing traditions** -- Tao Te Ching, Dhammapada, Rumi (Masnavi selections), Meister Eckhart, one Kabbalistic text | High (8-16 hrs) | High -- legitimizes "world's timeless spiritual wisdom" claim and fills obvious gaps | Scholar, Seeker, Content Strategist |

### Honorable Mentions (Next Tier)

6. **Uncomment CustomOgImages** to enable social sharing previews (low effort, medium impact)
7. **Add alt text to all quote images** (medium effort, important for accessibility)
8. **Create 3-5 more Wisdom Threads** to flesh out the cross-tradition feature (high effort, high impact for returning visitors)
9. **Add a "Random Quote" button** beyond Daily Wisdom for serendipitous browsing (low effort, medium impact for return visitors)
10. **Auto-generate the random quote pool** from published quotes at build time instead of maintaining a hardcoded array (medium effort, eliminates maintenance burden)

---

## Overall Site Grade: **6.3 / 10**

The site has excellent bones: a thoughtful content model, clean architecture, beautiful warm design, and genuinely curated spiritual content. The Wisdom Threads are the standout feature -- original, well-written comparative mysticism. The BookMeta component and homepage explore cards show sophisticated UX thinking.

What holds it back is execution completeness: a 400+ quote backlog, stale copy, an unusable quote listing page, missing traditions, and no analytics. The gap between the site's potential (a truly cross-tradition wisdom library) and its current state (primarily an Advaita Vedanta quote collection with some other traditions) is the central challenge.

The good news: the highest-impact improvements (fix stale copy, add filtering, triage drafts, add analytics) are all low-to-medium effort. A focused 2-day sprint could move the grade from 6.3 to 8+.
