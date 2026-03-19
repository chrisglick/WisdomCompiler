---
prd: true
id: PRD-20260318-wisdomcompiler-next-level
status: COMPLETE
mode: interactive
effort_level: Comprehensive
created: 2026-03-18
updated: 2026-03-18
iteration: 0
maxIterations: 128
loopStatus: null
last_phase: VERIFY
failing_criteria: []
verification_summary: "16/16"
parent: null
children: []
---

# WisdomCompiler: Next Level — Strategic Enhancement Plan

> Transform WisdomCompiler from a static spiritual quote archive into a living, interconnected wisdom companion that serves seekers across all traditions.

## STATUS

| What | State |
|------|-------|
| Progress | 16/16 criteria passing |
| Phase | COMPLETE |
| Next action | Krishna reviews and approves plan |
| Blocked by | nothing |

## CONTEXT

### Problem Space
WisdomCompiler has 651 wisdom quotes (196 published, 453 drafts), 16 teacher pages, and 18 books — a strong foundation. But the site feels like an archive, not a living resource. Teacher pages are text-only (no images), quotes are siloed by source rather than connected by theme, 340 quotes lack attribution, and there's no mechanism to make the site feel alive day-to-day. Krishna wants to "next level" this into something worthy of the wisdom it contains.

### Current State Inventory
- **651 total quotes** in `content/Wisdom Quotes/`
  - 196 edited/published (`Edited: true`)
  - 453 unedited drafts (`Edited: false`, `draft: true`) — raw OCR from screenshots
  - 340 with empty `source: ""` — no attribution
- **16 teacher pages** in `content/Teachers/` — text bio + passage links, no images
- **18 book pages** in `content/Books/` — with free online reading links
- **RandomQuote component** — 149 curated quotes shown on homepage
- **Warm earth-tone theme** — carefully designed light/dark modes
- **Quartz v4.5.2** static site generator, deployed via **Cloudflare Pages**
- **Content authored in Obsidian**, published via `npx quartz build` → Wrangler deploy

### Key Files
- `quartz.config.ts` — site configuration, theme, plugins
- `quartz.layout.ts` — page layout, component arrangement, explorer filter
- `quartz/components/RandomQuote.tsx` — random quote component
- `scripts/generate-quotes.py` — quote extraction script
- `scripts/generate-book-links.py` — book page link generator
- `content/index.md` — homepage
- `content/Teachers/*.md` — teacher pages
- `content/Wisdom Quotes/*.md` — all quotes (651 files)

### Constraints
- Must work within Quartz v4 static site architecture
- Must deploy to Cloudflare Pages (free tier)
- Content must remain authorable in Obsidian
- No paid services required (optional upgrades clearly marked)
- No manual daily effort for "alive" features — must be automated

## PLAN

### Architecture Principle
Every enhancement follows the same pipeline: **Obsidian vault → build-time processing → static output**. No server-side logic, no databases. Intelligence lives in build scripts and Quartz plugins. The vault remains the single source of truth.

### Implementation Sequence
Priority ordering based on impact-to-effort ratio and dependency chains:

| Priority | Domain | Impact | Effort | Dependencies |
|----------|--------|--------|--------|-------------|
| **P1** | 3. OCR Quality Review | High — fixes broken content | Medium | None — foundational |
| **P2** | 1. Teacher Images | High — visual transformation | Low-Medium | None |
| **P3** | 2. Keyword Concept Pages | Very High — the "compiler" | Medium-High | P1 (clean content needed) |
| **P4** | 6. Rich Teacher Profiles | High — depth for seekers | Medium | P2 (images first) |
| **P5** | 5. Cross-Tradition Threads | Very High — unique value | Medium | P3 (taxonomy needed) |
| **P6** | 4. Daily Publishing | Medium — site vitality | Low-Medium | P1 (enough clean content) |
| **P7** | 7. Contemplative Calendar | Medium — delight factor | Medium | P6 (daily mechanism) |
| **P8** | 8. Community & Growth | Medium — long-term | Low | P6 (RSS/feed ready) |

---

## THE EIGHT DOMAINS

---

### Domain 1: Teacher Images 🖼️

**Vision:** Each teacher page opens with a portrait that gives seekers a human connection to the source of wisdom. For historical/ancient teachers, tasteful artistic representations. For modern teachers, photographic portraits.

**Image Sourcing Strategy:**

| Teacher | Era | Source Strategy |
|---------|-----|----------------|
| Ramana Maharshi (1879-1950) | Modern | Wikimedia Commons — extensive public domain photos |
| Nisargadatta Maharaj (1897-1981) | Modern | Wikimedia Commons — several available |
| Eckhart Tolle (1948-) | Living | *Cannot use without permission* — use book cover or placeholder |
| Huang Po (~770-850) | Ancient | AI-generated artistic portrait or traditional painting style |
| Ashtavakra (ancient) | Ancient | AI-generated or classical art depiction |
| Osho (1931-1990) | Modern | Wikimedia Commons — many photos available |
| Seung Sahn (1927-2004) | Modern | Kwan Um School archives (check license) |
| Robert Adams (1928-1997) | Modern | Robert Adams Foundation (check license) |
| Swami Ishwarananda | Modern | Direct permission or ashram photos |
| Others | Varies | Case-by-case: Wikimedia → AI art → text-only fallback |

**Copyright Rules:**
1. **Public domain first** — Wikimedia Commons images with clear PD or CC-BY license
2. **AI-generated art** — For ancient teachers or when no free photo exists. Use Flux/DALL-E for respectful, tradition-appropriate portraits
3. **No copyrighted photos without permission** — Especially for living teachers
4. **Fallback: decorative element** — A tradition-specific symbol (Om, Enso, Crescent, Cross) if no portrait is appropriate

**Implementation Steps:**
1. Create `content/Teachers/images/` directory in vault
2. Source images for each of 16 teachers using strategy above
3. Add `image` frontmatter field to teacher `.md` files
4. Quartz already supports `ArticleImage` component in layout — leverage this
5. Ensure images are optimized (WebP, max 400px width) for page speed
6. Add CSS for teacher image styling — circular crop, centered, with subtle shadow

**Effort:** ~2-4 hours for sourcing and implementation

---

### Domain 2: Keyword Concept Pages (Wisdom Taxonomy) 🏷️

**Vision:** A seeker thinking about "surrender" can visit `/concepts/surrender` and find every quote across all traditions that touches this theme. This is the COMPILER — it compiles scattered wisdom into thematic coherence.

**Taxonomy Design — Core Wisdom Concepts:**

**Tier 1 — Universal Themes** (appear across all traditions):
- Self / Atman / True Nature
- Ego / Mind / False Self
- Surrender / Letting Go / Submission
- Silence / Stillness / Emptiness
- Love / Devotion / Bhakti
- Knowledge / Jnana / Gnosis
- Guru / Teacher / Master
- Liberation / Moksha / Enlightenment
- Meditation / Practice / Sadhana
- God / Divine / Absolute

**Tier 2 — Specific Concepts** (tradition-specific but cross-referencing):
- Self-Enquiry (Advaita)
- Zazen / Sitting (Zen)
- Dhikr / Remembrance (Sufism)
- Prayer / Contemplation (Christianity)
- Humility / Simplicity
- Death / Impermanence
- Nature / Creation
- Scripture / Teaching
- Service / Karma Yoga
- Grace / Blessing

**Extraction Method — Build-Time Script:**
```
Pipeline: content/*.md → extract_keywords.py → concept tag injection → Quartz tag pages
```

1. **Create `scripts/extract-keywords.py`** — Scans all published quote files:
   - NLP keyword matching against the taxonomy wordlist
   - Fuzzy matching for variants (e.g., "self-enquiry", "self enquiry", "atma vichara")
   - Each quote gets `concepts:` frontmatter tags added
   - Script is idempotent — re-runnable without duplication

2. **Leverage Quartz tag system** — Quartz already has `TagPage` emitter:
   - Concept tags become tag pages automatically
   - `/tags/surrender` shows all quotes tagged with surrender
   - No custom component needed — built into Quartz

3. **Create `content/Concepts/index.md`** — A landing page listing all concept categories with descriptions:
   - Tier 1 concepts with 2-sentence explanations
   - Count of quotes per concept
   - Cross-tradition note (e.g., "Surrender appears in Advaita as *prapatti*, in Islam as *islam* itself, in Christianity as 'Thy will be done'")

4. **Manual curation layer** — After automated tagging, Krishna can refine tags in Obsidian. The script adds suggestions; the vault is the authority.

**Effort:** ~6-10 hours (script + taxonomy design + manual review pass)

---

### Domain 3: OCR Quality Review & Quote Cleanup 🔍

**Vision:** Every published quote reads cleanly — no truncated sentences, no OCR artifacts, no orphaned fragments. The 453 drafts are triaged into publishable, fixable, or discard piles.

**Current State Analysis:**
- **196 published** (`Edited: true`) — Need quality check for OCR artifacts
- **453 drafts** (`Edited: false`, `draft: true`) — Raw OCR, many with issues:
  - UUID filenames (machine-generated, no human-readable title)
  - Photo ID filenames (`56426826243__...`)
  - Truncated text (OCR cut off mid-sentence)
  - Header/footer artifacts ("xvi", page numbers)
  - Missing attribution (`source: ""` on 340 quotes)

**Triage Strategy — Three-Pass Approach:**

**Pass 1: Automated Cleanup (script-driven)**
Create `scripts/audit-quotes.py`:
- Flag quotes < 20 characters (likely fragments)
- Flag quotes ending mid-word or mid-sentence (no period, question mark, or natural ending)
- Flag quotes with page number artifacts (roman numerals, "p.", standalone numbers)
- Flag ALL CAPS segments > 3 words (OCR shouting)
- Flag quotes with empty `source:` field
- Output: `production/ai/quote-audit-report.md` with categorized issues

**Pass 2: AI-Assisted Repair (semi-automated)**
For each flagged quote:
- Use Claude/GPT to identify the likely source text and complete truncated passages
- Cross-reference with source books (many are linked to specific texts)
- Suggest attribution for unattributed quotes based on content analysis
- Output: suggested edits as a diff file for Krishna's review

**Pass 3: Human Review (Krishna's curation)**
- Krishna reviews suggested fixes in Obsidian
- Approves, modifies, or discards each suggestion
- Sets `Edited: true` and `draft: false` for approved quotes
- Renames UUID files to human-readable quote titles

**Prioritization within the 453 drafts:**
1. **Quotes with known sources** (have `source:` filled) — easiest to verify and fix (~113 quotes)
2. **Quotes with readable filenames** — already partially curated
3. **Quotes with empty sources** — need research before publishing (~340 quotes)
4. **Quotes with UUID/photo filenames** — need OCR re-read + attribution

**Effort:** ~8-16 hours total (script: 2h, AI-assist: 4h, human review: 2-10h depending on depth)

---

### Domain 4: Daily Publishing Mechanism ⏰

**Vision:** A returning visitor sees something fresh every day. The site breathes — it's not a dusty archive but a living spring of wisdom.

**Architecture Challenge:** Quartz generates static HTML. "Daily" content requires either (a) rebuilding daily, or (b) client-side date-aware logic.

**Recommended Approach: Hybrid — Client-Side "Today's Wisdom" + Scheduled Rebuilds**

**Component 1: Client-Side "Today's Wisdom"**
- Extend `RandomQuote.tsx` → create `DailyWisdom.tsx`
- Instead of `Math.random()`, use `Date`-based deterministic selection:
  ```
  const dayOfYear = Math.floor((Date.now() - new Date(Date.UTC(year,0,1)).getTime()) / 86400000)
  const todayQuote = quotes[dayOfYear % quotes.length]
  ```
- Same quote all day, changes at midnight (user's local timezone)
- Shows "Today's Wisdom — March 18" with the quote
- **No rebuild required** — purely client-side, works with static hosting

**Component 2: Scheduled Rebuild (for "Recently Added" and fresh RSS)**
- **GitHub Actions cron job** — schedule `npx quartz build` + Wrangler deploy weekly or on content push:
  ```yaml
  on:
    schedule:
      - cron: '0 6 * * 1'  # Every Monday at 6 AM UTC
    push:
      branches: [v4]
      paths: ['content/**']
  ```
- This publishes newly edited quotes automatically when Krishna pushes vault changes
- RSS feed updates automatically with new content
- **Cost: $0** — GitHub Actions free tier covers this

**Component 3: "Recently Added" Section on Homepage**
- Show last 5 published quotes by modified date
- Quartz has `RecentNotes` component — configure for Wisdom Quotes folder
- Gives visual proof the site is maintained

**No manual daily effort required.** Krishna adds/edits quotes in Obsidian whenever inspired. The GitHub Action publishes. The client-side component makes every day feel fresh.

**Effort:** ~3-5 hours (DailyWisdom component: 2h, GitHub Action: 1h, RecentNotes config: 1h)

---

### Domain 5: Cross-Tradition Wisdom Threads 🌊

**Vision:** This is the heart of what makes WisdomCompiler unique. A "Wisdom Thread" page for "Surrender" shows:
- Ramana Maharshi: *"Self-surrender is the same as Self-knowledge"*
- Huang Po: *"Let go of all thought and just be"*
- Rumi: *"When you let go of who you are, you become what you might be"*
- Jesus: *"Not my will, but yours be done"*

The seeker sees: these are not different religions — they are different languages for the same truth.

**Implementation:**

1. **Create `content/Threads/` directory** — Each thread is a curated Obsidian note:
   ```markdown
   ---
   title: "Surrender"
   thread: true
   traditions: [Advaita, Zen, Sufism, Christianity, Islam]
   ---

   # The Thread of Surrender

   > Across every tradition, the mystics speak of a moment where the seeker
   > stops seeking and simply opens. They call it by different names...

   ## In Advaita Vedanta
   [[Self-surrender is the same as Self-knowledge]]
   [[If the surrender is complete all sense of the individuality is lost]]

   ## In Zen
   ...

   ## In Sufism
   ...
   ```

2. **Build-time thread discovery** — Threads leverage Quartz's existing wikilink resolution. No custom plugin needed — just well-structured markdown.

3. **Thread Index Page** (`content/Threads/index.md`) — Lists all threads with a one-line description of how each theme manifests across traditions.

4. **Cross-linking from concept pages** — Each concept tag page links to its corresponding thread for deeper exploration.

**Seed Threads (initial set):**
- Surrender / Letting Go
- The Ego and Its Dissolution
- Silence and the Space Between Thoughts
- The Guru-Disciple Relationship
- What Happens After Death / Beyond the Body
- The Nature of Love
- Self-Inquiry: Who Am I?

**Effort:** ~6-10 hours (thread curation is thoughtful work — quality over quantity)

---

### Domain 6: Rich Teacher Profiles 👤

**Vision:** A teacher page isn't just a list of quotes — it's a gateway. A seeker encountering Huang Po for the first time should understand: who was this person, what tradition are they from, what's the core teaching, and where should I start reading?

**Enhanced Teacher Page Structure:**

```markdown
---
title: "Huang Po"
teacher: true
tradition: Ch'an (Zen) Buddhism
period: Tang Dynasty (~770-850 CE)
lineage: "Student of Baizhang Huaihai, teacher of Linji Yixuan"
core_teaching: "One Mind — all things are already Buddha-nature"
image: images/huang-po.webp
recommended_start: "[[The Zen Teaching of Huang Po]]"
---

![Huang Po](images/huang-po.webp)

## Who Was Huang Po?

Huang Po (Huángbò Xīyùn) was a Chinese Ch'an master of the Tang Dynasty,
known for his radical and uncompromising teaching style...

## Core Teaching

The One Mind — there is nothing to attain because you already ARE it...

## Tradition & Lineage

Ch'an Buddhism → Hongzhou school → Teacher of Linji (Rinzai)...

## Where to Start

If you're new to Huang Po, begin with [[The Zen Teaching of Huang Po]],
translated by John Blofeld...

## Passages

- [[quote 1]]
- [[quote 2]]
...
```

**Implementation:**
1. Design template → `content/Teachers/_teacher_template.md`
2. Enrich existing 16 teacher pages with tradition, lineage, core teaching, recommended start
3. AI-assisted research for biographical content (verify against known sources)
4. Add structured frontmatter for filtering/grouping by tradition
5. Create `content/Teachers/index.md` — group teachers by tradition, with tradition descriptions

**Effort:** ~4-8 hours (research + writing for 16 teachers)

---

### Domain 7: Contemplative Calendar 📅

**Vision:** The "Today's Wisdom" feature (Domain 4) becomes even more resonant when it's aware of spiritual seasons. During Lent, surface Christian mystic quotes about surrender. During Navaratri, surface quotes about the Divine Mother. During Ramadan, surface Islamic wisdom about fasting and devotion.

**Implementation:**

1. **Create `scripts/contemplative-calendar.json`** — A data file mapping date ranges to spiritual seasons:
   ```json
   {
     "seasons": [
       {
         "name": "Lent",
         "tradition": "Christianity",
         "type": "moveable",
         "calculate": "easter_minus_46",
         "duration_days": 46,
         "concepts": ["surrender", "prayer", "fasting", "humility"]
       },
       {
         "name": "Navaratri (Spring)",
         "tradition": "Hinduism",
         "type": "moveable",
         "calculate": "chaitra_shukla_1",
         "duration_days": 9,
         "concepts": ["devotion", "divine_mother", "shakti"]
       },
       {
         "name": "Winter Solstice / Yalda / Christmas",
         "tradition": "Universal",
         "type": "fixed",
         "start": "12-21",
         "duration_days": 4,
         "concepts": ["light", "rebirth", "hope", "divine_birth"]
       }
     ]
   }
   ```

2. **Enhance `DailyWisdom.tsx`** — Check current date against calendar. If within a spiritual season, prefer quotes tagged with matching concepts. Fallback to standard rotation.

3. **Optional "Season Banner"** — A subtle line below the daily quote: *"This is the season of Lent — a time of surrender and inner turning"*

**This is NOT about religious promotion.** It's about showing seekers how different traditions mark similar spiritual rhythms throughout the year — another dimension of the "perennial philosophy" that WisdomCompiler embodies.

**Effort:** ~4-6 hours (calendar data: 2h, component enhancement: 2h, testing: 1h)

---

### Domain 8: Community & Growth Pathway 🌱

**Vision:** WisdomCompiler grows beyond one person's curation into a community project — without requiring social features, accounts, or moderation overhead.

**Implementation — Lightweight, Static-Compatible:**

**8a. Contribution Pathway**
- Add `content/about.md` section: "Contribute a Quote"
- Simple instructions: Fork the repo, add a quote file following the template, submit a PR
- Or: email quotes to a dedicated address → Krishna adds to vault
- Template: `content/Wisdom Quotes/_screenshot_template.md` already exists — reference it

**8b. RSS + Newsletter**
- Quartz already has RSS enabled (`ContentIndex` with `enableRSS: true`)
- Add visible RSS link to footer/sidebar
- Optional: connect RSS to a free Buttondown/Substack newsletter for email delivery
- Seekers subscribe once → receive weekly/daily wisdom automatically
- **Cost: $0** for RSS; free tier newsletter services handle small audiences

**8c. "Recently Added" Feed**
- Quartz `RecentNotes` component on homepage or dedicated `/recent` page
- Shows last 10-20 published quotes with dates
- Proves the site is alive and growing

**8d. Site Statistics on About Page**
- Build-time generated stats: "651 passages from 16 teachers across 18 sacred texts"
- Updates automatically on each build
- Simple script: `scripts/generate-stats.py` → writes counts to `content/about.md` frontmatter

**8e. "Submit a Correction" Link**
- Each quote page gets a small "Report an issue" link → pre-filled GitHub issue template
- Uses Quartz's existing GitHub integration
- Zero-maintenance for Krishna — issues accumulate, review when convenient

**Effort:** ~3-5 hours (RSS visibility: 30min, RecentNotes: 1h, About stats: 1h, contribution guide: 1h, correction links: 1h)

---

## IMPLEMENTATION ROADMAP

### Phase 1: Foundation (P1-P2) — ~6-8 hours
- [x] Run OCR audit script on 651 quotes — `scripts/audit-quotes.py` ✅
- [x] Triage 453 drafts into fix/discard piles — report at `production/ai/quote-audit-report.md` ✅
- [ ] AI-assisted repair of fixable quotes (85 published with issues, 286 fixable drafts)
- [ ] Source and add teacher images for 16 pages
- [ ] Deploy and verify

### Phase 2: Intelligence (P3-P5) — ~12-20 hours
- [x] Design and implement keyword taxonomy — 16 concepts ✅
- [x] Build `extract-keywords.py` script — 517 quotes tagged ✅
- [x] Create concept index page — `content/Concepts.md` ✅
- [x] Enrich teacher profiles — 6 of 16 done (Ramana, Huang Po, Nisargadatta, Ashtavakra, Tolle, Osho) ✅
- [x] Create initial cross-tradition wisdom threads — 3 of 7 done (Surrender, Ego, Silence) ✅
- [ ] Remaining: 10 teacher pages, 4 more threads
- [ ] Deploy and verify

### Phase 3: Vitality (P6-P8) — ~8-14 hours
- [x] Build `DailyWisdom.tsx` component with date-based selection ✅
- [x] Set up GitHub Actions for scheduled builds — `.github/workflows/deploy.yaml` ✅
- [ ] Add `RecentNotes` to homepage
- [ ] Create contemplative calendar data
- [ ] Enhance DailyWisdom with seasonal awareness
- [ ] Add RSS visibility, contribution guide, correction links
- [ ] Deploy and verify

### Total Estimated Effort: 26-42 hours across 3 phases

---

## IDEAL STATE CRITERIA (Verification Criteria)

- [x] ISC-Plan-1: Plan covers all eight website improvement domains comprehensively | Verify: Read: 8 domain sections
- [x] ISC-Plan-2: Each domain includes concrete implementation steps within Quartz | Verify: Read: Quartz-specific steps per section
- [x] ISC-Plan-3: Plan preserves Obsidian vault authoring workflow compatibility | Verify: Read: vault remains source of truth
- [x] ISC-Plan-4: Teacher image strategy addresses sourcing and copyright concerns | Verify: Read: sourcing table with copyright rules
- [x] ISC-Plan-5: Keyword concept page design specifies extraction and taxonomy | Verify: Read: taxonomy tiers + extraction pipeline
- [x] ISC-Plan-6: OCR review strategy scopes the 453 draft quotes systematically | Verify: Read: three-pass triage methodology
- [x] ISC-Plan-7: Daily publishing mechanism works with static site architecture | Verify: Read: client-side + cron approach
- [x] ISC-Plan-8: Items five through eight reflect deep spiritual site understanding | Verify: Custom: evaluate seeker-centricity
- [x] ISC-Plan-9: Plan includes effort estimates and priority ordering per domain | Verify: Read: priority table + hour estimates
- [x] ISC-Plan-10: Cross-tradition synthesis connects wisdom across all represented traditions | Verify: Read: Thread concept described
- [x] ISC-Plan-11: Guided reading paths proposed for different seeker stages | Verify: Read: Thread seeds + teacher "where to start"
- [x] ISC-Plan-12: Plan addresses the 340 quotes with empty source attribution | Verify: Read: attribution gap in triage strategy
- [x] ISC-A1: Plan does not propose breaking existing site functionality | Verify: Read: all additive proposals
- [x] ISC-A2: Plan does not require paid services or infrastructure changes | Verify: Read: all free tier
- [x] ISC-A3: No proposal requires manual daily effort from Krishna | Verify: Read: all automated mechanisms
- [x] ISC-A4: Plan does not propose generic web features unrelated to wisdom | Verify: Custom: all proposals serve seekers

## DECISIONS

- 2026-03-18: Chose client-side date-based quote selection over server-side rebuild for daily freshness. Rationale: zero-cost, zero-maintenance, works with any static host. Trade-off: same quote for all visitors on same day (feature, not bug — shared daily wisdom).
- 2026-03-18: Chose Quartz tag system for concept pages rather than custom plugin. Rationale: leverages existing infrastructure, no maintenance burden, familiar Obsidian tag workflow.
- 2026-03-18: Chose "Threads" as cross-tradition feature name over "Connections" or "Parallels." Rationale: evokes weaving, continuity, the thread of truth running through all traditions.

## LOG

### Iteration 0 — 2026-03-18 (Planning)
- Phase reached: VERIFY
- Criteria progress: 16/16 (plan verified)
- Work done: Comprehensive 8-domain plan created and verified

### Iteration 1 — 2026-03-18 (Implementation)
- Phase reached: BUILD/EXECUTE
- Work done:
  - Quote audit script built and run (648 quotes scanned, triage report generated)
  - Keyword extraction: 16-concept taxonomy applied to 517 quotes, 16 tag pages generated
  - Concepts landing page created with curated descriptions
  - DailyWisdom component built (replaced RandomQuote on homepage)
  - 6 quotes published from ready pile
  - GitHub Actions deploy workflow created (push + weekly cron)
  - 6 teacher pages enriched (Ramana, Huang Po, Nisargadatta, Ashtavakra, Tolle, Osho)
  - 3 Wisdom Threads created (Surrender, Ego, Silence)
  - Final build: 721 files → 1210 emitted, clean
- Remaining:
  - Teacher images (10 more teachers to enrich)
  - 4 more Wisdom Threads
  - OCR repair of published quotes with issues
  - Contemplative calendar, community features
  - Deploy to Cloudflare Pages
- Context for next iteration: Build succeeds locally. Needs deploy + GitHub secrets setup for CI/CD.
