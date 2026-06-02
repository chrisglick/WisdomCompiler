# WisdomCompiler

A free, open library of spiritual wisdom — books, teachers, and 600+ curated quotes — published as a static site from an Obsidian vault.

**Live site:** [wisdomcompiler.com](https://wisdomcompiler.com)

## What This Is

WisdomCompiler is a curated collection of spiritual resources spanning Advaita Vedanta, Sufism, Christianity, Sikhism, Zen, and other traditions of inner inquiry. Each book page includes a link to read the full text online for free where available.

Built with [Quartz v4](https://quartz.jzhao.xyz/) on top of an Obsidian vault. Content is authored in Obsidian, built to static HTML by Quartz, and deployed to Cloudflare Pages.

## Content Structure

```
content/
  Books/                  # ~50 spiritual texts with curated passages and free reading links
    index.md              # Books landing page (customizes folder listing)
    Ashtavakra Gita.md    # Individual book pages with [[wikilinks]] to quote notes
    ...
  Teachers/               # Teacher pages (Ramana Maharshi, etc.) with passage links
    images/               # Teacher portraits
  Wisdom Quotes/          # ~660 transcribed quote notes (.md files) + landing page
    index.md              # Landing page for the quotes collection
    Images/               # ~650 source images (.webp photos of book pages)
    _screenshot_template.md  # Template for a new quote note (underscore = not built)
  Concepts/               # Concept notes (draft)
  Websites/               # Spiritual website directory (draft — not yet published)
  YouTube/                # Video teachings (draft — not yet published)
  Social-Media/, Threads/ # Drafting/staging folders (hidden from the site)
  index.md                # Homepage
```

**How quotes work:** Each quote is a markdown note in `Wisdom Quotes/` (still referred to as a "screenshot note" in the scripts) with a `source` field linking it to a book or teacher. Book and teacher pages contain `[[wikilinks]]` to these notes. Quartz resolves them using shortest-path matching.

**Draft control:** Any file with `draft: true` in frontmatter is excluded from the published site. Selected folders (`images`, `social-media`, `about`, `tags`, `lakshmi the cow`) are hidden from the Explorer sidebar via a custom `filterFn` in `quartz.layout.ts`, but their pages are still built for link resolution.

## Build Pipeline

### Prerequisites

- Node.js (for Quartz and Wrangler)
- Python (for the book-link generation script)
- Cloudflare account with `wrangler` authenticated

### Local Development

```bash
# Preview the site locally (builds + serves at http://localhost:8080)
npx quartz build --serve
```

### Full Build & Deploy

```bash
# 1. (Optional) Regenerate book/teacher passage links from screenshot notes
python scripts/generate-book-links.py

# 2. Build the site (~50-60 seconds, outputs to public/)
npx quartz build

# 3. Deploy to Cloudflare Pages
npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4
```

**One-liner:**
```bash
npx quartz build && npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4
```

If you get Cloudflare auth errors:
```bash
unset CF_API_TOKEN && unset CLOUDFLARE_API_TOKEN
```

### Git Workflow

Single branch: `v4`. Push to `origin/v4`:
```bash
git add <files> && git commit -m "description" && git push origin v4
```

Note: The `.github/workflows/` CI files are inherited from upstream Quartz and gated for `jackyzha0/quartz` — they do not run on this fork.

## Key Files

| File | Purpose |
|------|---------|
| `production/WORKFLOW.md` | Full human workflow: editing, publishing, adding content |
| `quartz.config.ts` | Site config: title, base URL, theme colors, plugins |
| `quartz.layout.ts` | Page layout: Explorer filter, sidebar components, RandomQuote placement |
| `quartz/styles/custom.scss` | Custom CSS: mobile responsiveness, touch targets, text wrapping |
| `quartz/styles/variables.scss` | Breakpoints ($mobile: 800px, $desktop: 1200px), grid layouts |
| `quartz/components/DailyWisdom.tsx` | Rotating quote shown on the homepage (data: `scripts/dailywisdom.inline.ts`) |
| `quartz/components/WisdomQuiz.tsx` | Homepage "guess the source" quiz (data: `scripts/wisdomquiz.inline.ts`) |
| `quartz/components/HomepageExplore.tsx` | Homepage browse/explore section |
| `quartz/components/RandomQuote.tsx` | Legacy random-quote component (registered but no longer placed in the layout; data from `scripts/randomquote.inline.ts`) |
| `scripts/generate-book-links.py` | Scans `Wisdom Quotes/` notes, regenerates passage lists on book/teacher pages |
| `scripts/generate-quotes.py` | Extracts quotes from `Wisdom Quotes/` into `randomquote.inline.ts` |
| `production/ai/SESSION-*.md` | AI-assisted development session notes |
| `production/templates/NEW-BOOK.md` | Template and guide for adding a new book page |
| `production/templates/NEW-TEACHER.md` | Template and guide for adding a new teacher page |
| `production/QUOTE-DESIGN-DOC.md` | Design spec for wisdom quote file structure |

## Customization Details

### Explorer Filtering

The sidebar Explorer hides certain folders via `filterFn` in `quartz.layout.ts`:

```typescript
filterFn: (node) => {
  const name = node.name?.toLowerCase()
  if (!name) return true
  const excluded = ["tags", "images", "social-media", "lakshmi the cow", "about"]
  return !excluded.includes(name)
}
```

The optional chaining (`node.name?.`) is required — some Quartz tree nodes have undefined names.

### Mobile Responsiveness

All mobile CSS lives in `quartz/styles/custom.scss` inside `@media all and ($mobile)`. Key rules:
- `overflow-x: hidden` on html/body/.page to prevent horizontal scroll
- `word-break: break-word` on article content and links
- 44px touch targets for sidebar and footer links
- Scaled-down headings for small screens

### Theme

Warm, parchment-inspired color scheme (see `quartz.config.ts` theme section):
- Light mode: cream background (`#faf8f0`), brown accents (`#8b5e3c`)
- Dark mode: deep brown (`#1a1510`), gold accents (`#c49a6c`)

## Hosting

- **Platform:** Cloudflare Pages
- **Project name:** `wisdom-compiler`
- **Branch:** `v4`
- **Domain:** wisdomcompiler.com

## Built On

- [Quartz v4.5.2](https://quartz.jzhao.xyz/) by Jacky Zhao
- [Obsidian](https://obsidian.md/) for content authoring
