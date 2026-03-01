# WisdomCompiler — Human Workflow

> How to edit, publish, and deploy content from Obsidian.

---

## What Changed (March 2026)

This vault is now **both** an Obsidian vault and a Quartz static site source. Key changes:

- **Dataview queries are gone.** Book pages (e.g., `Ashtavakra Gita.md`) no longer use `dataview` code blocks. They now contain static `[[wikilinks]]` to screenshot notes. This means you won't see the dynamic tables in Obsidian anymore — but the links still work in both Obsidian and the published site.
- **A script regenerates book/teacher pages.** When you add or change screenshots, you re-run the script to update which passages appear on each book page.
- **`draft: true` controls visibility.** Any file with `draft: true` in frontmatter is hidden from the live site. Remove it or set `draft: false` to publish.
- **`Edited: true` marks screenshot quality.** Screenshots you've reviewed and cleaned up have `Edited: true`. During migration, only these were published.

---

## Day-to-Day: Editing a Screenshot Note

1. **Open the vault** in Obsidian at `D:\Vaults\WisdomCompiler\`
2. **Navigate** to `Screenshots/Notes/` and open a note
3. **Review and clean up** the `text::` field — fix OCR errors, formatting, attribution
4. **Set frontmatter** when done editing:
   ```yaml
   Edited: true
   ```
5. **Remove `draft: true`** (or set to `draft: false`) to make it publishable:
   ```yaml
   # Remove this line entirely, or change to:
   draft: false
   ```
6. **Check the `source` field** — make sure it points to the right book or teacher:
   ```yaml
   source: "[[Talks with Ramana Maharshi]]"
   ```

That's it for editing. The note will go live on next deploy.

---

## Publishing: From Edit to Live Site

After editing one or more screenshots, follow these steps:

### Step 1: Regenerate Book/Teacher Pages

This updates which passages appear on each book and teacher page:

```bash
cd D:\Vaults\WisdomCompiler
python scripts/generate-book-links.py
```

You'll see output like:
```
Book: Ashtavakra Gita -> 8 passages
Teacher: Ramana Maharshi -> 23 passages
```

**When to run this:**
- After changing any screenshot's `source` field
- After adding new screenshot notes
- After adding a new book file
- NOT needed if you only edited the `text::` content of existing notes

### Step 2: Build the Site

```bash
cd D:\Vaults\WisdomCompiler
npx quartz build
```

Takes ~50-60 seconds. This generates the `public/` folder.

### Step 3: Deploy to Cloudflare

```bash
cd D:\Vaults\WisdomCompiler
npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4
```

If you get auth errors, run this first:
```bash
unset CF_API_TOKEN && unset CLOUDFLARE_API_TOKEN
```

### One-Liner (Steps 2+3 combined)

```bash
cd D:\Vaults\WisdomCompiler && npx quartz build && npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4
```

---

## Adding New Content

### New Screenshot Note

1. Create a new `.md` file in `Screenshots/Notes/`
2. Add frontmatter:
   ```yaml
   ---
   Edited: true
   source: "[[Book Name Here]]"
   Page: "0"
   image_name: your-image.png
   Source Type: []
   tags:
   ---
   ```
3. Add the image embed: `![[your-image.png]]`
4. Add the text: `text::Your transcribed text here`
5. Place the image file in `Screenshots/Images/`
6. Run the generate script (Step 1 above) to add it to the book page

### New Book

1. Create a new `.md` file in `Books/` (e.g., `My New Book.md`)
2. Add frontmatter:
   ```yaml
   ---
   sticker: emoji//1f4d6
   Author: Author Name
   title: My New Book
   source: url
   tags:
   draft: false
   ---
   ```
3. Run `python scripts/generate-book-links.py` — it will automatically find any screenshots whose `source` matches `[[My New Book]]` and list them

### New Teacher

Same as books, but in `Teachers/`:
```yaml
---
draft: false
---
```
The script handles teachers the same way it handles books.

---

## What NOT to Do

- **Never publish `Whatsapp - Maji.md`** — this file must always have `draft: true`
- **Don't manually edit book page passage lists** — the script will overwrite them on next run
- **Don't add dataview blocks** — they render as raw code on the live site

---

## Quick Reference

| Task | Command |
|------|---------|
| Regenerate book links | `python scripts/generate-book-links.py` |
| Build site locally | `npx quartz build --serve` (then open localhost:8080) |
| Build for deploy | `npx quartz build` |
| Deploy | `npx wrangler pages deploy public --project-name=wisdom-compiler --commit-dirty=true --branch=v4` |
| Git push | `git add -A && git commit -m "Update content" && git push` |

## File Locations

| What | Where |
|------|-------|
| Screenshot notes | `content/Screenshots/Notes/` |
| Screenshot images | `content/Screenshots/Images/` |
| Book pages | `content/Books/` |
| Teacher pages | `content/Teachers/` |
| Link generator script | `scripts/generate-book-links.py` |
| Quartz config | `quartz.config.ts` |
| Build output | `public/` |
| This workflow doc | `production/WORKFLOW.md` |
| Session notes | `production/ai/SESSION-2026-03-01.md` |
