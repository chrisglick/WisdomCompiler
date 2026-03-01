# WisdomCompiler Deployment Guide

## Architecture
- **Content**: Obsidian vault with Markdown files in `content/`
- **Generator**: Quartz v4 (converts Obsidian markdown to static HTML)
- **Hosting**: Cloudflare Pages (free, global CDN, auto-HTTPS)
- **Domain**: wisdomcompiler.com (registered on Porkbun)

## Workflow: Edit to Live

1. **Edit in Obsidian**: Open `D:\Vaults\WisdomCompiler` as an Obsidian vault
2. **Write/edit content** in `content/` folder — standard Obsidian markdown, wikilinks, tags all work
3. **Commit and push**:
   ```bash
   cd D:\Vaults\WisdomCompiler
   git add -A
   git commit -m "Update content"
   git push
   ```
4. **Auto-deploys**: Cloudflare Pages detects the push and rebuilds automatically (~2-4 min)
5. **Live at**: https://wisdomcompiler.com

## Adding New Content

### New Book
Create a file in `content/Books/Book Name.md`:
```markdown
---
title: Book Name
tags:
  - books
  - tradition-name
---

# Book Name

Description of the book and why it's valuable for seekers.

## Free Resources
- [Link to free PDF/text]
- [Link to audio version]
```

### New Teacher
Create a file in `content/Teachers/Teacher Name.md` with similar frontmatter.

### New Quote
Create a file in `content/Screenshots/Notes/Quote title.md`.

## Local Preview
```bash
cd D:\Vaults\WisdomCompiler
npx quartz build --serve
```
Opens at http://localhost:8080

## Troubleshooting
- **Build fails**: Check `npx quartz build` output for errors
- **Content not showing**: Ensure file is in `content/` and has valid frontmatter
- **Images not loading**: Place images in same directory or use relative paths
