# Link Audit — Broken References After Rename (2026-03-23)

## Summary

**9 broken wiki-links found** across 7 files. All are `.txt]]` references pointing to files that were renamed from `.txt.md` to `.md`. The `.txt.md` originals no longer exist; the `.md` versions do exist.

**0 broken `[[IMG_*]]` wiki-links found.** All IMG renames were clean.

**0 broken `.txt.md` references found** in content files.

**0 broken references found** in quartz/ or scripts/ code (only benign `image_name:` frontmatter and script patterns that reference IMG_ filenames for image assets, not wiki-links).

---

## Search 1: Wiki-links referencing old IMG filenames

**Query:** `\[\[IMG_` in `content/`
**Hits:** 0

No content files contain `[[IMG_*]]` wiki-links. The rename from `IMG_*.txt.md` to descriptive names did not leave behind broken IMG wiki-links.

---

## Search 2: `.txt.md` references in content

**Query:** `\.txt\.md` in `content/`
**Hits:** 0

No content files reference `.txt.md` extensions.

---

## Search 3: `.txt]]` references in content (BROKEN LINKS)

**Query:** `\.txt\]\]` in `content/`
**Hits:** 9 matches in 7 files

Every one of these is a **confirmed broken link**. The `.txt` extension should be removed.

| # | File | Line | Broken Link | Should Be |
|---|------|------|-------------|-----------|
| 1 | `content/Teachers/Huang Po.md` | 39 | `[[If you wish to experience Enlightenment yourselves you must not indulge in such conceptions.txt]]` | `[[If you wish to experience Enlightenment yourselves you must not indulge in such conceptions]]` |
| 2 | `content/Threads/The Thread of Ego.md` | 28 | `[[If you wish to experience Enlightenment yourselves you must not indulge in such conceptions.txt]]` | `[[If you wish to experience Enlightenment yourselves you must not indulge in such conceptions]]` |
| 3 | `content/Books/Ramana Periya Purnam.md` | 21 | `[[The greatest form of ego for an individual is to present himself as a teacher and become a guru.txt]]` | `[[The greatest form of ego for an individual is to present himself as a teacher and become a guru]]` |
| 4 | `content/Books/Talks with Ramana Maharshi.md` | 19 | `[[annihilation of the mind - knowledge and one-pointedness.txt]]` | `[[annihilation of the mind - knowledge and one-pointedness]]` |
| 5 | `content/Books/The Ribhu Gita.md` | 15 | `[[By knowing which all is renounced ever abide as that itself.txt]]` | `[[By knowing which all is renounced ever abide as that itself]]` |
| 6 | `content/Books/The Zen Teaching of Huang Po.md` | 21 | `[[If you wish to experience Enlightenment yourselves you must not indulge in such conceptions.txt]]` | `[[If you wish to experience Enlightenment yourselves you must not indulge in such conceptions]]` |
| 7 | `content/Books/Yoga Vasistha.md` | 15 | `[[Give up the desire that tends to bondage and the desire for liberation too.txt]]` | `[[Give up the desire that tends to bondage and the desire for liberation too]]` |
| 8 | `content/Books/Yoga Vasistha.md` | 16 | `[[He was therefore peaceful in both pain and pleasure.txt]]` | `[[He was therefore peaceful in both pain and pleasure]]` |
| 9 | `content/Books/Yoga Vasistha.md` | 19 | `[[The distress of the mind is got rid of by enquiry into the nature of the self.txt]]` | `[[The distress of the mind is got rid of by enquiry into the nature of the self]]` |

### Verification

For every broken link above, the old `.txt.md` file is **MISSING** and the new `.md` file **EXISTS**:

- MISSING: `...conceptions.txt.md` / EXISTS: `...conceptions.md`
- MISSING: `...guru.txt.md` / EXISTS: `...guru.md`
- MISSING: `...one-pointedness.txt.md` / EXISTS: `...one-pointedness.md`
- MISSING: `...itself.txt.md` / EXISTS: `...itself.md`
- MISSING: `...too.txt.md` / EXISTS: `...too.md`
- MISSING: `...pleasure.txt.md` / EXISTS: `...pleasure.md`
- MISSING: `...self.txt.md` / EXISTS: `...self.md`

---

## Search 4: `.txt|` references (wiki-link with alias)

**Query:** `\.txt\|` in `content/`
**Hits:** 0

---

## Search 5: IMG_ references in quartz/ and scripts/

**Query:** `IMG_` in `quartz/`
**Hits:** 1 (benign)

- `quartz/components/ArticleImage.tsx:13` — comment explaining image path convention. Not a link.

**Query:** `IMG_` in `scripts/`
**Hits:** 6 (all benign)

- `scripts/audit-quotes.py` — pattern matching for audit logic
- `scripts/fix-image-paths.py` — image embed path fixer
- `scripts/fix-quotes.sh` — rename script (already executed)
- `scripts/generate-quotes.py` — quote extraction filter
- `scripts/review-quotes.sh` — review script

These are all tooling scripts that use `IMG_` patterns to identify/process files. None produce broken links.

---

## Search 6: `.txt.md` references in quartz/ and scripts/

**Query:** `\.txt\.md` in `quartz/` and `scripts/`
**Hits:** 0 in quartz/, 2 in scripts/ (benign — comments in fix-quotes.sh documenting what was done)

---

## Search 7: Trailing underscore wiki-links

**Query:** `_\]\]` in `content/Wisdom Quotes/`
**Hits:** 0

---

## Search 8: `[[IMG_` pattern (wiki-link + IMG combined)

**Query:** `\[\[.*IMG_` in `content/`
**Hits:** 0

---

## Search 9: Any `.txt` reference in content .md files

**Query:** `\.txt` in `content/**/*.md`
**Hits:** 9 — same as Search 3. No additional `.txt` references beyond the broken wiki-links already identified.

---

## Fix Required

Remove `.txt` from 9 wiki-links across 7 files. All fixes are simple string replacements: `.txt]]` -> `]]`.

### Files to edit:
1. `content/Teachers/Huang Po.md` (line 39)
2. `content/Threads/The Thread of Ego.md` (line 28)
3. `content/Books/Ramana Periya Purnam.md` (line 21)
4. `content/Books/Talks with Ramana Maharshi.md` (line 19)
5. `content/Books/The Ribhu Gita.md` (line 15)
6. `content/Books/The Zen Teaching of Huang Po.md` (line 21)
7. `content/Books/Yoga Vasistha.md` (lines 15, 16, 19)
