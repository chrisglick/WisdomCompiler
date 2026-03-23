# Wisdom Quote Design Document

> This document defines the ideal structure and quality standards for every file in `content/Wisdom Quotes/`. All quotes should conform to this specification.

## Filename Rules

1. **Descriptive name** — The filename should be a meaningful excerpt from the quote (first ~80 characters of the key sentence), not a UUID, IMG number, or hash
2. **No double extensions** — Use `.md` only, never `.txt.md`
3. **No trailing special characters** — No trailing underscores `_`, periods, or extra spaces
4. **Sentence case** — First word capitalized, rest follows natural casing
5. **No "pt 2" / "Part 2" suffixes** — Each file should be self-contained; if a quote spans multiple screenshots, consolidate into one file

### Bad filenames
- `101da6a6-ab03-40f5-ac03-86835cdd65b0.txt.md` (UUID + double extension)
- `56426826243__F9812273-53D1-445A-8BD4-BEFA4CC430D0.txt.md` (camera identifier)
- `IMG_1328.txt.md` (image number only)
- `The same truth has to be expressed in different ways to suit the capa.md` (truncated mid-word)

### Good filenames
- `A person's paradise is developed inside him.md`
- `By whatever path you go you will have to lose yourself in the One.md`
- `Don't believe your thoughts.md`

---

## Frontmatter Schema

```yaml
---
Edited: true                          # REQUIRED: true = OCR text has been human-reviewed
source: "[[Book Title]]"              # REQUIRED: Wikilink to book, not author
Page: "123"                           # REQUIRED: Page number (string), "0" if unknown
image_name: original-image.jpg        # REQUIRED: Original screenshot filename
Source Type:                           # OPTIONAL: screenshot, Meme, or empty
ShowImage: false                       # REQUIRED: true only if image IS the content (manga, meme)
tags:                                  # REQUIRED: At least one topic tag
  - topic-tag
---
```

### Field Rules

| Field | Required | Type | Rules |
|---|---|---|---|
| `Edited` | Yes | boolean | `true` if OCR text reviewed and corrected; `false` if raw/unreviewed |
| `source` | Yes | string | Must be `"[[Book Title]]"` wikilink format. Must be a **book title**, not an author name. If source is unknown, use `""` |
| `Page` | Yes | string | Page number as string. `"0"` if unknown |
| `image_name` | Yes | string | The original image filename (not a path) |
| `Source Type` | No | string/list | `screenshot`, `Meme`, or empty. Not critical |
| `ShowImage` | Yes | boolean | `true` ONLY for visual content (manga panels, calligraphy, memes). `false` for text screenshots |
| `tags` | Yes | list | At least one tag from the standard tag set (see below) |
| `draft` | No | boolean | `true` means file is not ready for publishing. Remove field when file is ready |

### Source Field — Author vs Book

The `source` field must reference a **book or text**, not an author:

| Wrong | Right |
|---|---|
| `"[[Ramana Maharshi]]"` | `"[[Talks with Ramana Maharshi]]"` or `"[[Day by Day with Bhagavan]]"` |
| `"[[Swami Ishwarananda Giriji Maharaj]]"` | Keep as-is if no specific book identified (this is a teacher, not a book) |

When the source is genuinely an author (meme images, social media posts), it's acceptable. But if the body text references a specific book, update the source field.

### Standard Tags

```
divine, ego, guru-teacher, knowledge-wisdom, liberation, love-devotion,
meditation, mind, nature-creation, scripture, self-knowledge, service,
silence, death-impermanence
```

---

## Body Content Rules

### Structure

```markdown
[Optional: image embed - only if ShowImage: true]
![](Images/image-name.jpg)

[Quote text - REQUIRED]
Clean, complete quote text here. Properly punctuated and formatted.
```

### Text Quality Requirements

1. **Complete sentences** — No partial sentences cut off at beginning or end
2. **No OCR artifacts** — No garbled text like "ae Te sage Sere", "itselfis", "Ifany"
3. **Proper punctuation** — Apostrophes in contractions (`don't`, not `dont`), possessives (`one's`, not `ones`)
4. **No `text::` dataview fields** — Use plain text, not `text::Quote here`
5. **No ALL CAPS** unless it's a proper noun or title (like DHARMA, SELF)
6. **Consistent quote marks** — Use standard double quotes `"`, not smart quotes
7. **No page numbers in body** — Remove stray page numbers like `241` or `173` at end of text
8. **No image captions repeated** — If the quote is from an image, transcribe it cleanly
9. **Attribution in body** — Remove in-body attribution like `~ Ramana Maharshi` (this belongs in frontmatter `source` field)

### Image Embeds

- Use `![](Images/filename.jpg)` format (web-compatible)
- NOT `![[filename.jpg]]` (Obsidian-only, breaks on web)
- Only include image embed if `ShowImage: true`

---

## Draft vs Published

- Files with `draft: true` or `Edited: false` are NOT ready for the website
- A file is ready when:
  - `Edited: true`
  - Body text is clean and complete
  - Source is properly attributed
  - Filename is descriptive
  - At least one tag assigned

---

## Common Issues to Fix

| Issue | Example | Fix |
|---|---|---|
| UUID filename | `101da6a6-...txt.md` | Rename to quote excerpt |
| Double extension | `file.txt.md` | Rename to `file.md` |
| OCR garble | "ae Te sage Sere" | Remove garbled text, keep clean transcription |
| Missing source | `source: ""` | Fill from body text attribution or image |
| Author as source | `"[[Ramana Maharshi]]"` | Change to specific book if identifiable |
| Truncated text | Text ends mid-word | Complete the sentence from image/context |
| Stray page numbers | `241` at end of body | Remove |
| Dataview field | `text::Quote here` | Change to plain `Quote here` |
| Obsidian-only embed | `![[image.jpg]]` | Change to `![](Images/image.jpg)` |
