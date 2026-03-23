# SourceBanner Design — Architecture & Design Pass

## Context
WisdomCompiler has 651 quote pages with `source:` frontmatter linking to teachers/books, 16 teacher pages with downloaded portrait images, and 18 book pages. Krishna wants clickable banners on every quote page (linking back to source) and hero banners on teacher pages, with very rounded corner images and a single CSS template governing all instances.

## Architecture Decision: Runtime allFiles Lookup

**No build script, no JSON mapping, no plugin.** The Quartz component receives `allFiles` (all pages' frontmatter) in its props. The component:
1. Reads `source: "[[Ramana Maharshi]]"` from current quote's frontmatter
2. Strips wikilink syntax → `"Ramana Maharshi"`
3. Searches `allFiles` for a page with matching title in Teachers/ or Books/
4. Reads that page's `image:` frontmatter field for the portrait filename
5. Renders the banner with link back to that source page's slug

This is identical to how Backlinks.tsx and RecentNotes.tsx already use allFiles — proven pattern.

## Component: SourceBanner.tsx (single component, two variants)

**Quote page variant (compact):** Horizontal — 48px circular portrait + source name, entire banner clickable to source page. Subtle background matching DailyWisdom style.

**Teacher/book hero variant (large):** Centered — 120px portrait with 24px border-radius (very rounded rectangle), positioned above ArticleTitle. Name hidden (ArticleTitle shows it).

**Fallback (no image):** Left accent border (4px solid secondary color) + source name text. No broken images.

## CSS Design Spec

| Property | Quote Banner | Hero Banner |
|----------|-------------|-------------|
| Image size | 48px circle | 120px wide, 3:4 aspect |
| Image border-radius | `50%` (circular) | `24px` (very rounded) |
| Container border-radius | `12px` | none |
| Background | `color-mix(in srgb, var(--light) 90%, var(--lightgray))` | transparent |
| Hover | darker background | none |
| Name font | 0.9rem, var(--secondary), 500 weight | hidden |
| Mobile image | 36px | 80px |
| Fallback | 4px left border accent | 4px left border accent |

All colors use `var(--*)` theme tokens — works in both light and dark mode automatically.

## Layout Integration

In `quartz.layout.ts` `beforeBody` array, insert after Breadcrumbs, before ArticleTitle:

```
DailyWisdom (index only)
Breadcrumbs (non-index)
SourceBanner            ← NEW
ArticleTitle
ContentMeta
ArticleImage
TagList
```

No ConditionalRender wrapper needed — component returns null for non-applicable pages.

## Image Mapping: Frontmatter `image:` Field

Each teacher page gets `image: "filename.jpg"` in frontmatter, pointing to their best portrait in `content/Teachers/images/`. This is a one-time edit to 16 teacher pages. The component reads `sourcePage.frontmatter.image` at build time.

## File Manifest

| Action | File | Change |
|--------|------|--------|
| CREATE | `quartz/components/SourceBanner.tsx` | Component (~80 lines) + CSS |
| EDIT | `quartz/components/index.ts` | Add import/export |
| EDIT | `quartz.layout.ts` | Add to beforeBody |
| EDIT | 16 teacher `.md` files | Add `image:` frontmatter |
| NONE | 651 quote `.md` files | Zero changes — reads existing `source:` |
| NONE | Quartz plugins | No modifications |

## Verification

1. `npx quartz build` succeeds
2. Quote page with source → banner shows with portrait + link
3. Teacher page → hero portrait renders
4. Quote with empty source → no banner (graceful)
5. Source without image → text-only fallback with accent border
6. Light mode + dark mode both look correct
