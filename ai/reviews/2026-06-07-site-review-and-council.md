# WisdomCompiler — Site Review & Council Debate
_Date: 2026-06-07 · Reviewer: Gyges (PAI) · Method: live-site audit + 5-agent Council debate_

---

## 1. Status snapshot

| | |
|---|---|
| **Live site** | [wisdomcompiler.com](https://wisdomcompiler.com) — 500 published pages |
| **Published breakdown** | 427 Wisdom-Quotes · 49 Books · 16 Teachers · 4 Threads · about · Concepts · Updates |
| **Framework** | Quartz v4.5.2 (static site from Obsidian vault), branch `v4` |
| **Deploy** | Local CLI only (`quartz build` + `wrangler pages deploy`) — by owner decision |
| **Last work** | 2026-06-02 multi-agent cleanup of **all 647** quote notes (OCR-fixed, attributed, titled, tagged) |
| **⚠️ Critical gap** | The cleaned 647 are **UNCOMMITTED** and `draft:true`. The live site still serves the **older, uncleaned** content. |

**What the live site shows today (the un-cleaned state):**
- Quote pages: raw transcribed passages, titled by their first line, **no visible attribution**.
- Book pages (e.g. Ashtavakra Gita): "Read Online" link + flat list of passage links, titles **truncated mid-word** ("…that comes from duty be hap").
- Teacher pages (e.g. Ramana Maharshi): walls of dozens of truncated link titles, **visible duplicates** ("Arpana offering means…" appears twice).
- Homepage and About page tell **contradictory stories** (personal "shrine" vs. "community directory"; About references a "Media" section that doesn't exist in nav).
- Default Quartz "digital-garden" chrome (Explorer sidebar, graph view, backlinks panel).

> Most of these are **already fixed** in the uncommitted local content. Publishing it is the single highest-leverage action.

---

## 2. Council debate

Five agents reviewed the live site as evidence and debated across 3 rounds (positions → challenges → synthesis).

**Members:** 🏛️ Architect (Serena) · 🎨 Designer (Aditi) · ⚙️ Engineer (Marcus) · 🔍 Researcher (Ava) · 🌱 Intern/first-visitor (Dev)

### Round 1 — Initial positions
- **🏛️ Serena (Architect):** "A near-flat namespace masquerading as an information architecture. Filesystem folders are not a taxonomy." Treat metadata as the primary access layer; model Teacher / Source / Concept as real entities with quotes as edges; deduplicate and assign stable IDs **before** the publish wave bakes in structural debt.
- **🎨 Aditi (Designer):** "This site wears a developer's clothes to a meditation." Kill the documentation-tool chrome; contemplative reading wants one centered column, generous line-height, a serif with soul. Truncated titles and duplicates are unforgivable. Pick one voice for homepage/About. The words are the design — get out of their way.
- **⚙️ Marcus (Engineer):** The static Python link-scripts are out-of-band coupling that **guarantees drift** — stale pages, duplicates, the `draft:true`/`Edited:true` → 404 footgun. Cheap wins: commit the cleaned 647, flip drafts, kill the footgun. Correct long-term: replace scripts with Quartz build-time aggregation.
- **🔍 Ava (Researcher):** Attribution is the **SEO moat** — quote searches are long-tail; Goodreads dominates because every quote has a stable URL + author/source + tags. Retention comes from ritual (a true daily-quote permalink, à la The Marginalian / dailyzen), not just a homepage randomizer. OG quote-cards for shareability.
- **🌱 Dev (first-time visitor):** "Beautiful words, but who *said* this? No author, no breadcrumb, no next-quote — I'd bounce in four seconds." The sidebar/graph machinery "looks like someone's private Obsidian notebook I wasn't supposed to see." Wants: attribution + a "give me another" button on **every** page, hidden chrome, fixed link-walls, a clean shareable card.

### Round 2 — Challenges
- Serena: dedup + stable IDs must precede publish — **indexed URLs are immutable**; "attribution is the schema; the directory is the substrate, the shrine is the rendering."
- Aditi: the entity model must **not** surface as faceted-search UI — just one quiet attribution line + "more from this teacher." Gwern-style backlink panels *are* the chrome to kill. "Year-three purity that delays attribution is malpractice."
- Marcus: killing the chrome is "an afternoon in `quartz.layout.ts` — the highest-ROI move on the board." The full entity model = custom plugins; buy the cheap 80% (stable IDs + clean frontmatter) now. (Local-CLI deploy respected as owner's call.)
- Ava: "Depth is the moat, not cards." Kill auto-machinery but keep **editorial** inline concept-links. "Card converts strangers; concept-threads retain seekers — a shrine you can navigate."
- Dev: "Build the moat, ship the doorknob first." Email is dead — the URL itself is the ritual. Clean first, *then* publish.

### Round 3 — Synthesis
All five converged on: **clean before publish** (stable IDs before indexing), **attribution ships now** (not "year three"), **kill the developer chrome** (cheapest high-ROI win), and **card-then-depth** as the funnel. Remaining tension: how much of Serena's formal entity model to build now (Marcus/Dev: defer; Serena/Ava: model it correctly even if rendered quietly).

---

## 3. Prioritized roadmap

> Ordering reflects council consensus: doorknob first, moat second.

| # | Action | Effort | Why |
|---|--------|--------|-----|
| **1** | **Commit the cleaned 647 notes; finish the 2 garbled ones; run the publish wave** | M | Unblocks everything. Live site currently serves stale content. Stable URLs must land before indexing. |
| **2** | **Strip developer chrome** (graph view, raw backlinks panel) in `quartz.layout.ts` | S | "An afternoon." Highest immediate ROI — stops the site reading as a private notebook. |
| **3** | **Attribution line on every quote page** (teacher · book · page) + "more from this teacher" | S–M | Kills the #1 bounce cause; it's the SEO moat. Data already exists in the new frontmatter. |
| **4** | **"Give me another" button on every quote page** (extend RandomQuote beyond index) | S | Turns one landing into a session; the engagement loop Dev demanded. |
| **5** | **Contemplative typography pass** (centered ~65ch measure, serif quote text, AA contrast) | S | First impression. Sloppy type reads "amateur" before any feature earns trust. |
| **6** | **Unify homepage/About voice** around "one seeker's shrine"; remove the phantom Media section | S | Resolves the identity conflict that confuses both seekers and crawlers. |
| **7** | **OG quote-card images + a daily-quote permalink (+ optional RSS)** | M | Shareability + the return-visit ritual. |
| **8** | **Replace static Python link-scripts with Quartz build-time aggregation** | L | Kills the drift/404 footgun permanently; single source of truth. |
| **9** | **Hand-curated cross-tradition concept-threads** | L | The retention moat — depth that a million quote sites can't match. |

**Headline insight:** _"Card converts strangers; concept-threads retain seekers."_ Kill the *auto-generated* machinery, but keep *editorial* related-passage links.

---

## 4. Recommended next move
Item 1 is ~95% done sitting in the working tree (645 modified notes, uncommitted). Start with the diff review → commit on `v4` → finish the 2 garbled notes (`IMG_6941.md`, `IMG_6944.md`) → selectively flip `draft:false`. Then items 2–4 are a single short session.

_See also: `RESUME.md`, `ai/sessions/SESSION-2026-06-02-quote-review.md`, `production/WORKFLOW.md`._
