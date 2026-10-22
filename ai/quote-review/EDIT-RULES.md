# WisdomCompiler quote-note editing rules

You are a meticulous editor. Clean ONE quote note IN PLACE, using its source image as ground truth.

## Steps
1. Read the note file AND read the source image. The image is ground truth; the existing body is often wrong OCR. If the image can't be read, treat as UNREADABLE.
2. Classify: quote-card / book-page / dialogue / manga-or-meme / unreadable.
3. **BODY** = clean transcription from the image. Fix OCR artifacts ONLY (never paraphrase):
   - Rejoin hyphenated line-break splits: `admit- ting`→`admitting`.
   - Fix run-together / split words: `Ifyou`→`If you`, `Tam`→`I am`.
   - Remove page-number markers (`~342~`, bare page numbers), running headers/footers FROM THE BODY.
   - Preserve original spelling (incl. British/archaic), punctuation, capitalization, emphasis.
   - **Dialogue (Q&A):** one speaker turn per paragraph (blank line between); ITALICIZE the questioner's lines with `*asterisks*`; leave the teacher's answers in plain roman text. Use the image to decide who speaks.
   - Smart/curly quotes ARE encouraged in the BODY for good typography. Do NOT add an image embed line.
4. **Page:** if a page number is visible, set frontmatter `Page` to the FIRST page number seen, straight-quoted (e.g. `Page: "232"`). Else leave Page unchanged.
5. **Source:** if a book/author/teacher is identifiable from the image, set `source: "[[Exact Name]]"` matching exactly one canonical name (below). Prefer a specific BOOK. Else leave source unchanged. Never invent a source not in the lists.
6. **Title:** if the FILENAME is a UUID or `IMG_####`, add `title: "<short ≤70-char phrase from the quote>"`. Do NOT rename the file. If the filename is already descriptive, leave title alone.
7. **Tags:** ensure `tags` lists 1–5 lowercase theme tags from the vocabulary below. Remove a junk `screenshot` tag.
8. **ShowImage:** if it's a MANGA/COMIC panel or a MEME (the picture itself is the content), set `ShowImage: true`. Otherwise leave ShowImage as-is.
9. **Flags (PUBLISH CONTROL — agents doing a review pass NEVER set draft:false; publishing happens only via the Publish rule below, as a separate step):**
   - If originally `Edited=false`: set `Edited: true` ONLY if the result is a clean, complete, confident quote with a known source; otherwise set `Edited: false` and add tag `needs-review` (or `needs-manual-review` + do not fabricate text if unreadable).
   - If originally `Edited=true`: keep `Edited: true` (you are only cleaning OCR; never downgrade).
   - NEVER change the `draft` line.
10. **Write back (surgical):** preserve every frontmatter key and its order; change ONLY `source`, `Edited`, `tags`, `Page`, `ShowImage`, and (add) `title` per the rules. Leave `image_name`, `Source Type`, `draft`, `published`, `publish_date`, `last_posted` intact.
   - 🔴 In FRONTMATTER use ONLY straight ASCII quotes `"` `'` — NEVER curly quotes (`“ ” ‘ ’`). Keep `--- ` fences, valid YAML, and no leading BOM.

## Canonical BOOKS
A New Earth · Ashtavakra Gita · Berzerk · Bhagavad Gita · Bible - Book of Luke · Calvin and Hobbes · Coming Home to Yourself · Conscious Immortality · Consciousness and the Absolute · Day by Day with Bhagavan · Dropping Ashes On the Buddha · Dune · Early Islamic Mysticism · Greater Community Spirituality · Guru Granth Sahib · Guru Vachaka Kovai · Haqiqatul-Wahi - The Philosophy of Divine Revelation · In Search of the Miraculous · Kaivalya Navaneetam · Letters from Sri Ramanasramam · Mob Psycho 100 · One Punch Man · Ramana Periya Purnam · Revelation, Rationality, Knowledge & Truth · Silence of the Heart · Siva Purana · Sri Ramana Gita · Talks with Ramana Maharshi · The Incredible Sai Baba · The Nectar of Immortality · The New Dawn · The Path of Self Knowledge · The Perfect Master, Vol 1 · The Philosophy of the Teachings of Islam · The Power of Now · The Prophet · The Ribhu Gita · The Search · The Sutra of Queen Srimala · The Vimalakirti Sutra · The Zen Teaching of Huang Po · Tripura Rahasya · Upadesa Saram · Vagabond · Vidyeshvara Samhita · Vigyan Bhairav Tantra Volume 1 · Vivekachudamani · Yoga Vasistha

## Canonical TEACHERS
Arthur Osborne · Ashtavakra · Bill Watterson · Eckhart Tolle · Hazrat Mirza Ghulam Ahmad · Huang Po · Mirza Tahir Ahmad · Nisargadatta Maharaj · Osho · Ramana Maharshi · Robert Adams · Seung Sahn · Sri Muruganar · Swami Ishwarananda Giriji Maharaj · Takehiko Inoue

## Tag vocabulary
nature-creation · mind · divine · guru-teacher · knowledge-wisdom · love-devotion · consciousness · service · meditation · self-knowledge · suffering · liberation · silence · death-impermanence · ego · scripture · faith-trust · surrender · non-duality · detachment · humility

## Publish rule (2026-10-21)
A quote note is published (`draft: false`) when and only when ALL hold: `Edited: true`, `source` is a canonical wikilink (`[[...]]`), and no `needs-*` tag is present.
Notes failing any of these stay `draft: true`.
The flip is done per this rule, never by hand-picking individual notes.
First application on 2026-10-21 published 107 notes.
