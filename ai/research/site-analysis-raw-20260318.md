# WisdomCompiler Site Analysis — Raw Data (2026-03-18)

## Content Inventory

### Wisdom Quotes (`content/Wisdom Quotes/`)
- **Total files:** 651
- **Published (Edited: true):** 196
- **Drafts (Edited: false, draft: true):** 453
- **Empty source attribution (source: ""):** 340
- **With known source attribution:** ~311

### Top Sources by Quote Count
| Count | Source |
|-------|--------|
| 340 | (empty — no attribution) |
| 27 | The Zen Teaching of Huang Po |
| 26 | Letters from Sri Ramanasramam |
| 25 | The Philosophy of the Teachings of Islam |
| 25 | Talks with Ramana Maharshi |
| 23 | Ramana Maharshi (direct) |
| 21 | Swami Ishwarananda Giriji Maharaj |
| 17 | Yoga Vasistha |
| 15 | Vagabond |
| 15 | Guru Vachaka Kovai |
| 14 | Ramana Periya Purnam |
| 10 | Day by Day with Bhagavan |
| 10 | Consciousness and the Absolute |
| 8 | Silence of the Heart |
| 8 | Ashtavakra Gita |
| 7 | The Vimalakirti Sutra |
| 4 | The Perfect Master, Vol 1 |
| 4 | The New Dawn |
| 4 | Early Islamic Mysticism |
| 4 | Bible - Book of Luke |

### Teachers (`content/Teachers/`)
16 teacher pages:
1. Arthur Osborne
2. Ashtavakra
3. Bill Watterson
4. Eckhart Tolle
5. Hazrat Mirza Ghulam Ahmad
6. Huang Po
7. Mirza Tahir Ahmad
8. Nisargadatta Maharaj
9. ONE (?)
10. Osho
11. Ramana Maharshi
12. Robert Adams
13. Seung Sahn
14. Sri Muruganar
15. Swami Ishwarananda Giriji Maharaj
16. Takehiko Inoue

### Books (`content/Books/`)
18 book pages including:
- Ashtavakra Gita, Day by Day with Bhagavan, Dropping Ashes On the Buddha
- Guru Vachaka Kovai, Letters from Sri Ramanasramam, Ramana Periya Purnam
- Revelation Rationality Knowledge & Truth, Silence of the Heart
- Sri Ramana Gita, Talks with Ramana Maharshi, The New Dawn
- The Power of Now, The Ribhu Gita, The Zen Teaching of Huang Po
- Vigyan Bhairav Tantra Volume 1, Yoga Vasistha
- Haqiqatul-Wahi, The Perfect Master Vol 1

### Other Content
- YouTube: 1 video page (Shirdi Sai Baba)
- Websites: 1 page (Saint Anthony Mary Claret)
- Social-Media: 1 page (Whatsapp - Maji)
- Lakshmi the Cow: 1 page (hidden from explorer)

## Architecture

- **Framework:** Quartz v4.5.2
- **Deployment:** Cloudflare Pages via Wrangler
- **Theme:** Warm earth tones (light: #faf8f0, dark: #1a1510, accent: #8b5e3c/#c49a6c)
- **Fonts:** Schibsted Grotesk (headers), Source Sans Pro (body), IBM Plex Mono (code)
- **Features enabled:** SPA, Popovers, RSS, Sitemap, Custom OG Images, Tag Pages
- **Custom components:** RandomQuote (homepage), ConditionalRender, ArticleImage
- **Build scripts:** generate-quotes.py, generate-book-links.py
- **Explorer exclusions:** tags, images, social-media, lakshmi the cow, about

## Quote File Structure (sample)

```yaml
---
Edited: true/false
source: "[[Book or Teacher Name]]"
Page: "0"
image_name: UUID.jpg
Source Type: [Meme]
tags: []
ShowImage: true/false
draft: true/false
---
![](Images/image.jpg)

Quote text here. — Attribution
```

## Key Observations

1. **Massive unpublished backlog** — 453 drafts vs 196 published (70% unpublished)
2. **Attribution gap** — 340 quotes (52% of total) have no source
3. **OCR quality issues** — Many drafts have truncated text, page artifacts, UUID filenames
4. **Teacher pages are sparse** — One paragraph bio + passage links, no images
5. **No concept/theme navigation** — Quotes organized by source only, not by theme
6. **No daily/fresh content mechanism** — Static site, same content each visit
7. **Strong foundation** — Beautiful theme, good architecture, RandomQuote works well
8. **Traditions represented:** Advaita Vedanta, Zen Buddhism, Islam/Ahmadiyya, Christianity, Sufism, Neo-Advaita, manga (Vagabond)
