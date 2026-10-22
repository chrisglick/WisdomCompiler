# OCR verification pass — 2026-10-21

Second pass over every quote note the June 2 cleanup left flagged: 160 `needs-review` + 41 `needs-manual-review` + 2 untagged garbled notes = **203 notes**. Each was re-read against its source image by an agent (sonnet for the review tier, opus for the hard tier, sonnet quote-only fallback where the content filter blocked full-page transcription). An independent haiku reader then re-checked all 83 rewritten bodies. A deterministic checker ran clean on all 203: valid YAML, no BOM, no curly quotes in frontmatter, no `draft` line touched, tags within vocabulary.

## Outcome

| Verdict | Count | Meaning |
|---|---|---|
| verified-clean | 80 | body matches image, canonical source: `Edited: true`, review tag removed |
| verified-no-source | 96 | body verified (fixed where needed) but no canonical source: `Edited: false`, tag `needs-source` |
| non-quote | 25 | picture-only plates, photos, game UI, lyric searches: left as-is |
| unreadable | 2 | cropped images (IMG_6338, "You fly about like birds"): placeholder body, `needs-manual-review` |

Vault flag counts after the pass: `needs-source` 98, `needs-manual-review` 24, plain `needs-review` 3 (the three untouched non-quotes), `Edited: true` 517 (was 522: a handful of previously-edited notes with no defensible source were downgraded per the rules). `draft: false` unchanged at 234. **Nothing published, nothing committed.** 191 files modified; review with `git diff -- "content/Wisdom Quotes"`.

Haiku QA on the 83 rewritten bodies: 79 pass, 4 fail, all fixed (a dropped "is" in IMG_6947, "his" for "this" in IMG_6948, "outselves" in the Moral nobility note, one merged dialogue paragraph in the "I exist" note). One uncertain: IMG_6893 carries `— Bob Anderson`, the book's author, which is not printed on that page.

**New tag `needs-source`** means: transcription verified, only the attribution is open. It separates "needs a human eye" from "needs a source".

## Decisions for Krishna

1. **About 45 notes are not wisdom quotes** (list A): Project Zomboid subtitle fragments, *Mandala* picture plates, two Kid Cudi lyric searches, a flywheel engineering paper, a sadhu photo, a Ramana photo. Delete, or keep as image-only pages.
2. **29 notes kept a source on recognition alone** (list B): the image shows no title. Most look right (Letters from Sri Ramanasramam, Philosophy of the Teachings of Islam). Confirm or clear.
3. **13 wrong attributions were cleared** (list C). Two stand out: a Christian sermon that had been filed under Osborne, and a Bloom County strip filed under Calvin and Hobbes.
4. **Recurring non-canonical sources** (list D): *Mandala* (Argüelles) and MySaiBaba.com video subtitles dominate. Either add them to the canonical vocabulary and re-attribute, or delete those notes.

## Method notes for the next run

- The API content filter blocks **full-page transcription of some copyrighted books** (Argüelles *Mandala* 1972, *Getting Things Done*, *Awakened Leadership*). It kills the agent with no output, on opus and sonnet alike. Fix: one note per agent so a block costs one note, then re-run in quote-only mode (body = the set-off quotation or one 2–4 sentence passage, `ShowImage: true`). Quote-only never blocked.
- Review tier: 8 notes per sonnet agent, about 70k tokens and 1.5 minutes each. Hard tier: one note per agent. The harness caps concurrent agents at 20.
- Haiku is a reliable second reader for fidelity.
- Agents that rewrite a whole file flip CRLF to LF. Git normalizes it.

## A. Delete candidates (not wisdom quotes: game-subtitle fragments, lyric searches, picture-only plates, photos)

- `IMG_1025.md` — Image is a legible iPad Google-search screenshot (query 'the lonely loner seems to free') showing a YouTube result and t
- `IMG_1026.md` — Image is legible but is an iPad screenshot of a Google search result showing song lyrics (Kid Cudi 'Day 'n' Nite', Lyric
- `IMG_1234.md` — Silent Vagabond panels (page 12 visible), no text; existing body is a scene description, left untouched, flags kept.
- `IMG_1299.md` — Only caption '(...laughter...)'; left untouched, flags kept
- `IMG_1424.md` — Video-still subtitle (MySaiBaba.com footage, not a game screenshot); subtitle matches; ShowImage true; needs-source
- `IMG_1539.md` — Image is a Project Zomboid game screenshot whose only quote text is a truncated in-game subtitle (cut off mid-sentence i
- `IMG_1540.md` — Project Zomboid game screenshot; only legible text is a subtitle fragment '...we will be slaves to the five desires whic
- `IMG_1541.md` — game screenshot (Project Zomboid, subtitle); subtitle matches; ShowImage true; needs-source
- `IMG_1542.md` — Image is a Project Zomboid gameplay screenshot (Retromation) with one legible caption line: "In all things, there is nei
- `IMG_1543.md` — Image is a Project Zomboid gameplay screenshot (Retromation watermark), not unreadable: the only text is an in-game subt
- `IMG_1544.md` — Image is a Project Zomboid game screenshot whose only content text is a single blue subtitle line, fully legible: 'One w
- `IMG_1545.md` — game screenshot (Project Zomboid, subtitle); subtitle matches; ShowImage true; needs-source
- `IMG_1546.md` — Project Zomboid game screenshot; only text is a legible subtitle fragment from an in-game 'Philosophical Quotes' disc: '
- `IMG_1547.md` — Project Zomboid gameplay screenshot (Retromation video, inventory/loot UI); only quote-like text is a partial in-game su
- `IMG_1548.md` — Project Zomboid game screenshot; legible subtitle fragment transcribed (replaced '(image not legible)'). In-game media b
- `IMG_1549.md` — Image is a Project Zomboid game screenshot (Retromation video) whose only quote text is one truncated in-game subtitle; 
- `IMG_1550.md` — Image is a video-game screenshot (Project Zomboid, RetroMation watermark) with only a subtitle fragment '...from sufferi
- `IMG_1551.md` — game screenshot (Project Zomboid, Retromation video); body set to legible subtitle 'But suffering is inseparable from pl
- `IMG_1552.md` — game screenshot (Project Zomboid, Retromation video); body replaced with the legible subtitle line 'Therefore, the more 
- `IMG_1553.md` — game screenshot (Project Zomboid, RetroMation video, PortaDisc playing a philosophy audio track): subtitle line transcri
- `IMG_1554.md` — game screenshot (Project Zomboid, PortaDisc audio subtitle); replaced '(image not legible)' with the legible subtitle ex
- `IMG_1625.md` — Not a wisdom quote and not a game screenshot: crisp excerpt from an engineering paper on flywheel energy storage (sectio
- `IMG_1651.md` — Not a game screenshot: illustrated Tibetan manuscript scroll (meditating/reclining figures, mandalas, colored circles) w
- `IMG_1658.md` — Video still of a sadhu before a sun mural, no text; left untouched, flags kept
- `IMG_1661.md` — Not a game screenshot and has no text: black-and-white photo of Ramana Maharshi (seated on a tiger skin by a boulder) wi
- `IMG_6337.md` — Not a game screenshot: Bloom County Sunday strip by Berke Breathed (April 17, 1983, book p.100), photographed sideways. 
- `IMG_6890.md` — Not a game screenshot: a legible book page, running header 'Awakened Leadership' p.184 (leadership-coaching text, not in
- `IMG_6919.md` — Photographed Mandala (Arguelles) p.13: left-cropped prose about Now/center/Mandala plus three captioned figures (Snow cr
- `IMG_6921.md` — Full-page picture (photomicrograph of a diatom, caption only: 'Photomicrograph of the Arachnoidisus Ehrenbergii', p.18, 
- `IMG_6925.md` — Mandala of the Ages plate, no real text; Mandala (Arguelles); page set 39; kept needs-manual-review, ShowImage true
- `IMG_6926.md` — Illustration only, no caption; kept needs-manual-review
- `IMG_6927.md` — Diagram with caption only; kept needs-manual-review
- `IMG_6928.md` — Diagram with caption only; kept needs-manual-review
- `IMG_6929.md` — Ouroboros diagram labels only; kept needs-manual-review
- `IMG_6930.md` — Diagrams with captions only; kept needs-manual-review
- `IMG_6933.md` — Rotated photo of a full-page illustrated diagram (zodiac signs, elements, solstices/equinoxes, +/- wedges; likely Mandal
- `IMG_6934.md` — Rotated page of Mandala (running foot 'Mandala of Bio-cyclic Rhythms', p.69): mostly an I Ching/zodiac mandala diagram p
- `IMG_6936.md` — Image is a full-page Tibetan thangka plate (wrathful Mahakala) photographed sideways; only text is a cropped plate capti
- `IMG_6937.md` — Image is a photo of a full-page Tibetan Wheel of Life (Bhavachakra) thangka painting in a book, rotated 90 degrees; only
- `IMG_6946.md` — Picture-only mandala plate with caption; kept needs-manual-review, ShowImage on
- `IMG_6955.md` — Picture-only page (Plate 13 Shath Chakra chart + Plate 14 painting, captions only; no prose or set-off quotation); body 
- `IMG_6956.md` — Page is two full-page color mandala figure plates (Plate 15 Radiant Woman, Jose Arguelles; Plate 16 Radiant Man, Miriam 

## B. Attribution kept on content recognition only (Edited:true, image shows no title). Confirm or clear.

- `A fire leaps up from our inside like lightning and another fire descends upon us from above.md` — `[[The Philosophy of the Teachings of Islam]]` — Body matches image; no header visible, source kept (Ahmad's text, recognizable); no page visible; removed need
- `As for future bondages.md` — `[[Letters from Sri Ramanasramam]]` — Added missing final line 'Whosoever is released from these three'; no header visible, source kept on content (
- `Bhagavans silence was his direct teaching he taught Self Enquiry to those who could not comprehend.md` — `[[Ramana Periya Purnam]]` — Italicized samadhi; body matches (image top has a cut-off partial line, omitted). Source not stated in image, 
- `Bondages of the past the future and the present.md` — `[[Letters from Sri Ramanasramam]]` — Body matches image (heading '(147) THE OMNIPRESENT'); no header/page visible, source kept on content/format.
- `Each gliding along in its orbit.md` — `[[The Philosophy of the Teachings of Islam]]` — Footnote text; apostrophe fixed, italics kept; source inferred from [Publisher] footnote; removed needs-review
- `Enquiry is not the only way.md` — `[[Letters from Sri Ramanasramam]]` — Body matches image exactly; kept existing source; removed needs-review.
- `Five thousand years of human minds evolution has not demystified existence.md` — `[[The New Dawn]]` — Body matches (image misprint 'Medic' kept as 'Vedic'); removed needs-review.
- `He is the ocean of love and sympathy.md` — `[[Letters from Sri Ramanasramam]]` — Body matches; source kept on content (Arunachala, Guru as Bestower, Nagamma letters style), not stated in imag
- `He is washed and cleansed and God inscribes love of virtue upon his heart and casts out from it the .md` — `[[The Philosophy of the Teachings of Islam]]` — Body matches; source kept on content (soul at rest stages), not stated in image
- `His memory was like an omnipresent prism of prescience.md` — `[[Dune]]` — Body matches; Leto/Ghanima/Stilgar is from Children of Dune, nearest canonical is Dune
- `I exist is the only permanent self-evident experience of everyone.md` — `[[Day by Day with Bhagavan]]` — Merged Swami/Bhagavan reply into one paragraph per image; source kept (not visible in image, plausible); remov
- `IMG_1286.md` — `[[The Path of Self Knowledge]]` — Fixed 'in the pure' -> 'in me pure' (cut-off top line); kept existing source, not confirmable from image
- `IMG_1362.md` — `[[Vagabond]]` — Manga panel text Here! Now! One stroke of the sword. matches; Vagabond source pre-set.
- `IMG_1419.md` — `[[Berzerk]]` — Replaced placeholder with bubble text (I see now / What I wanted more was / That light / Just like that light 
- `IMG_1623.md` — `[[Letters from Sri Ramanasramam]]` — Split into 3 paragraphs, curly quotes/italics restored, completed truncated last line; source Letters from Sri
- `IMG_1707.md` — `[[Mob Psycho 100]]` — Body matches single bubble; kept earlier-assigned Mob Psycho 100 source, which I could not independently confi
- `IMG_6032.md` — `[[Dropping Ashes On the Buddha]]` — Body matches (source typo 'nit like that' rendered as 'not'); Seung Sahn passage, source recognized by passage
- `IMG_6719.md` — `[[Ramana Maharshi]]` — Removed truncated trailing 'Learn to [text continues on next page]'; Ramana (Bhagavan) quote kept as source; h
- `Jnani conducts himself according to the wishes of others.md` — `[[Letters from Sri Ramanasramam]]` — Body matches image; source not printed in image, kept existing attribution (typeface and 'said Bhagavan' style
- `Present bondages are said to be of four types.md` — `[[Letters from Sri Ramanasramam]]` — Fixed first line (wrongly all-italic, wrong opening quote); only Panchadasi italic. Source Letters from Sri Ra
- `Sahaja Nishta.md` — `[[Letters from Sri Ramanasramam]]` — Added missing leading 'us,' and trailing 'Subsequently, the same'; source Letters from Sri Ramanasramam kept, 
- `So many things in this world cannot be expressed with words. Some things can not be explained.md` — `[[Vagabond]]` — Vagabond manga dialogue matches; panel order ambiguous, kept
- `The doctrine of Advaita Non-duality taught by the ancient Rishis.md` — `[[The Path of Self Knowledge]]` — Body matches image; existing source kept (not stated in image); cleared needs-review.
- `The first thing as I see you I see you miserable.md` — `[[The New Dawn]]` — Body matches image (cuts off at 'they always'); image has no attribution, kept existing source (Osho text); re
- `The sage is unattached to anything or anybody.md` — `[[Yoga Vasistha]]` — Body matches image; no header in image, kept existing Yoga Vasistha source (Venkatesananda-style text); remove
- `This chapter deals with all the preparatory steps which were needed before the creation of bio-units.md` — `[[Revelation, Rationality, Knowledge & Truth]]` — Body matches image, page 369 visible; source kept (Quranic/jinn/clay content, Tahir Ahmad book); removed needs
- `Three ways to describe truth - The same truth has to be expressed in different ways to suit the capa.md` — `[[Day by Day with Bhagavan]]` — Restored missing closing 'The letter continued, "In the' and italicised Sanskrit terms; page 174 visible; sour
- `To the degree that you turn away from attachments to the unreal.md` — `[[Kaivalya Navaneetam]]` — Body matches image (cropped mid-sentence, as in image); source kept from earlier pass (Master/numbered verses)
- `such a man becomes seated in the lap of God.md` — `[[The Philosophy of the Teachings of Islam]]` — Body matches; source previously set, recognizable passage; no page visible

## C. Wrong attributions cleared this pass (now empty source, tagged needs-source)

- `Becoming a reminder of human foolishness.md` — was "[[Ramana Periya Purnam]]" — Video subtitle frame of Acharya Prashant (not a canonical teacher); wrong source Ramana Periya Purna
- `Crying is an act of atonement.md` — was "[[Day by Day with Bhagavan]]" — Subtitle frame of MySaiBaba.com sadhu video, not a Day by Day book page; cleared wrong source, Edite
- `Food consecration mantra from the Bhagavad Gita.md` — was "[[Bhagavad Gita]]" — Fixed wrong opening curly quote, added line breaks in mantra list; book is a practice guide quoting 
- `He could not move as the force of Bhagavans presence held him.md` — was "[[Letters from Sri Ramanasramam]]" — Body matches (image typo 'hi his arms' kept as 'in'); passage is novel-style prose, not Letters from
- `His obsession with trade approached delirium.md` — was "[[A Very Special Patron - Saint Anthony Mary Claret]]" — Removed leading ellipsis and invented em dash to match image; source (Claret booklet) not canonical 
- `IMG_6337.md` — was "[[Calvin and Hobbes]]" — Not a game screenshot: Bloom County Sunday strip by Berke Breathed (April 17, 1983, book p.100), pho
- `IMG_6948.md` — was "[[Vidyeshvara Samhita]]" — Mandala 'Destruction' chapter; replaced placeholder with one ~60-word passage; removed unsupported V
- `Moral nobility and not social respectability.md` — was "[[The Path of Self Knowledge]]" — Rejoined 'cre- ative'; text is a Christian sermon (footnotes cite King, Strength to Love) not Path o
- `Self-negation and ultimate truth.md` — was "[[Vivekachudamani]]" — Urdu/Punjabi video subtitle frame; body matches; removed wrong Vivekachudamani source
- `Su Tung-p‘o wrote the follow  The roaring waterfall  is the Buddha’s golden mouth.md` — was "[[The Zen Teaching of Huang Po]]" — Poem matches; book not identifiable; removed unsupported Huang Po source
- `There is only one God - the language, location, and system may be different.md` — was "[[A Yogi's Insights into the Life & Miracles of Shirdi Sai Baba]]" — Video subtitle frame; body matches; cleared non-canonical source; Edited false, needs-source.
- `This course would have been better for every seeker.md` — was "[[Tripura Rahasya]]" — Body matches; crane-incident text is not Tripura Rahasya so cleared wrong source; added tag mind; Ed
- `Titov the Russian cosmonaut returned from space and declared there is no God.md` — was "[[Ramana Periya Purnam]]" — Body matches; Ramana Periya Purnam clearly wrong so cleared; no source identifiable; Edited false, n

## D. Recurring non-canonical sources (decide: add to vocab, or delete the notes)

- Mandala: 29 notes
- Project Zomboid: 16 notes
- MySaiBaba: 10 notes
- Bloom County: 4 notes
- Awakened Leadership: 3 notes
- Acharya Prashant: 2 notes
- Himalayan Institute: 2 notes
- Book of the Void: 1 notes
- Blue Exorcist: 1 notes
- Walking on Sunshine: 1 notes
- Getting Things Done: 1 notes

## E. Per-note verdicts

- `A fire leaps up from our inside like lightning and another fire descends upon us from above.md` — verified-clean / medium / body_changed=False — Body matches image; no header visible, source kept (Ahmad's text, recognizable); no page visible; removed needs-review.
- `After some time, Ashtavakra Muni happened to pass that side and, while he was about to take rest und.md` — verified-clean / high / body_changed=True — Added italics for brahmin/Durbar per image; header and page 403 visible.
- `All the concepts you have formed in the past must be discarded and replaced by void.md` — verified-clean / high / body_changed=False — Body incl. footnotes matches image; page 56 visible.
- `As for future bondages.md` — verified-clean / medium / body_changed=True — Added missing final line 'Whosoever is released from these three'; no header visible, source kept on content (Bhagavan, Vasudeva/Bharata).
- `Becoming a reminder of human foolishness.md` — verified-no-source / high / body_changed=False — Video subtitle frame of Acharya Prashant (not a canonical teacher); wrong source Ramana Periya Purnam cleared to empty, Edited false, tag ne
- `Bhagavan said his state of being was beyond subject and object.md` — verified-clean / high / body_changed=True — Added italics (Gita, upadesa, sastras, brahmin); header and page 402 visible.
- `Bhagavans silence was his direct teaching he taught Self Enquiry to those who could not comprehend.md` — verified-clean / medium / body_changed=True — Italicized samadhi; body matches (image top has a cut-off partial line, omitted). Source not stated in image, kept existing; page 284 visibl
- `Bondages of the past the future and the present.md` — verified-clean / medium / body_changed=False — Body matches image (heading '(147) THE OMNIPRESENT'); no header/page visible, source kept on content/format.
- `But when we look into the faculties of man and try to discover what is their highest reach, we find .md` — verified-clean / high / body_changed=False — Body matches image; cut-off last line retained; removed needs-review.
- `Clearing the Pain Body.md` — verified-clean / high / body_changed=True — Em dash to en dash per image; printed typos 'th'/'pan-bodies' left corrected; removed needs-review.
- `Crying is an act of atonement.md` — verified-no-source / high / body_changed=False — Subtitle frame of MySaiBaba.com sadhu video, not a Day by Day book page; cleared wrong source, Edited false, needs-source.
- `Despite so much development taking place sorrow has not decreased.md` — verified-no-source / high / body_changed=False — Video subtitle frame (MySaiBaba.com); body matches; no canonical source; needs-source.
- `Do not be so sorrow stricken the master takes care.md` — verified-no-source / medium / body_changed=True — Restored missing words (Narayana Iyer's wife, relatives pressurized, went to, take its own course); page 90 kept; existing Letters from Sri 
- `Each gliding along in its orbit.md` — verified-clean / medium / body_changed=True — Footnote text; apostrophe fixed, italics kept; source inferred from [Publisher] footnote; removed needs-review.
- `Enquiry is not the only way.md` — verified-clean / medium / body_changed=False — Body matches image exactly; kept existing source; removed needs-review.
- `Five thousand years of human minds evolution has not demystified existence.md` — verified-clean / medium / body_changed=False — Body matches (image misprint 'Medic' kept as 'Vedic'); removed needs-review.
- `Food consecration mantra from the Bhagavad Gita.md` — verified-no-source / medium / body_changed=True — Fixed wrong opening curly quote, added line breaks in mantra list; book is a practice guide quoting the Gita (not the Gita itself), unidenti
- `God has fashioned human nature such that it is like a receptacle that cannot remain empty of some fo.md` — verified-clean / high / body_changed=False — Body matches image; running header confirms source
- `He could not move as the force of Bhagavans presence held him.md` — verified-no-source / medium / body_changed=False — Body matches (image typo 'hi his arms' kept as 'in'); passage is novel-style prose, not Letters from Sri Ramanasramam; source cleared, needs
- `He is the ocean of love and sympathy.md` — verified-clean / medium / body_changed=False — Body matches; source kept on content (Arunachala, Guru as Bestower, Nagamma letters style), not stated in image
- `He is washed and cleansed and God inscribes love of virtue upon his heart and casts out from it the .md` — verified-clean / medium / body_changed=False — Body matches; source kept on content (soul at rest stages), not stated in image
- `He who is always in pursuit of happiness but finds only sorrow.md` — verified-no-source / high / body_changed=False — Subtitle from a Sai Baba video (MySaiBaba.com watermark), not a canonical book; needs-source
- `His memory was like an omnipresent prism of prescience.md` — verified-clean / medium / body_changed=False — Body matches; Leto/Ghanima/Stilgar is from Children of Dune, nearest canonical is Dune
- `His obsession with trade approached delirium.md` — verified-no-source / high / body_changed=True — Removed leading ellipsis and invented em dash to match image; source (Claret booklet) not canonical so cleared, needs-source
- `His vocational detour to the Society of Jesus had not been without purpose.md` — verified-no-source / high / body_changed=False — Body matches image; existing source is not canonical and image has no attribution; Edited->false, needs-source. Source key left unchanged.
- `I exist is the only permanent self-evident experience of everyone.md` — verified-clean / medium / body_changed=True — Merged Swami/Bhagavan reply into one paragraph per image; source kept (not visible in image, plausible); removed needs-review.
- `IMG_1025.md` — non-quote / high / body_changed=False — Image is a legible iPad Google-search screenshot (query 'the lonely loner seems to free') showing a YouTube result and the Lyrics panel for 
- `IMG_1026.md` — non-quote / high / body_changed=False — Image is legible but is an iPad screenshot of a Google search result showing song lyrics (Kid Cudi 'Day 'n' Nite', LyricFind), not a wisdom 
- `IMG_1146.md` — verified-no-source / high / body_changed=False — Body matches image exactly; no attribution visible; needs-source.
- `IMG_1203.md` — verified-clean / high / body_changed=False — Strip dialogue matches image; Edited true, needs-review removed.
- `IMG_1212.md` — verified-no-source / medium / body_changed=True — Body rewritten from handwritten notebook page (original garbled): main text plus captions; source not in canonical list; needs-source.
- `IMG_1226.md` — verified-clean / high / body_changed=True — Body matched; italicized emphasized KNEW; Edited true, needs-review removed.
- `IMG_1234.md` — non-quote / medium / body_changed=False — Silent Vagabond panels (page 12 visible), no text; existing body is a scene description, left untouched, flags kept.
- `IMG_1239.md` — verified-clean / high / body_changed=True — Added missing Heheh. bubble, normalized I'm... no one.; Edited true, needs-review removed.
- `IMG_1277.md` — verified-no-source / high / body_changed=True — Fixed Samvedansheelta spelling; video subtitle (MySaiBaba.com clip), no source
- `IMG_1278.md` — verified-no-source / high / body_changed=False — Body matches subtitle; video clip, no source
- `IMG_1286.md` — verified-clean / medium / body_changed=True — Fixed 'in the pure' -> 'in me pure' (cut-off top line); kept existing source, not confirmable from image
- `IMG_1292.md` — verified-no-source / high / body_changed=False — Body matches subtitle; video clip, no source
- `IMG_1293.md` — verified-no-source / high / body_changed=False — Body matches subtitle; video clip, no source
- `IMG_1296.md` — verified-no-source / high / body_changed=False — Body matches subtitle; video clip, no source
- `IMG_1298.md` — verified-no-source / high / body_changed=False — Body matches subtitle; video clip, no source
- `IMG_1299.md` — non-quote / high / body_changed=False — Only caption '(...laughter...)'; left untouched, flags kept
- `IMG_1303.md` — verified-no-source / high / body_changed=False — Video subtitle (MySaiBaba.com) matches; speaker unidentified, no canonical source; tag needs-source.
- `IMG_1305.md` — verified-no-source / high / body_changed=False — Video subtitle fragment matches; speaker unidentified; tag needs-source.
- `IMG_1309.md` — verified-clean / high / body_changed=True — Footer says The New Dawn/Osho p318; body matched, fixed en dash; added title; first line is a cropped fragment, last line cut mid-sentence a
- `IMG_1349.md` — verified-clean / high / body_changed=True — Rejoined pro-fundity, removed leading * * * divider; footnote omitted.
- `IMG_1362.md` — verified-clean / medium / body_changed=False — Manga panel text Here! Now! One stroke of the sword. matches; Vagabond source pre-set.
- `IMG_1417.md` — verified-clean / high / body_changed=False — Bubble text matches (readberserk.site ch.291).
- `IMG_1419.md` — verified-clean / medium / body_changed=True — Replaced placeholder with bubble text (I see now / What I wanted more was / That light / Just like that light / I); bubble reading order sli
- `IMG_1421.md` — verified-clean / high / body_changed=True — Fixed punctuation/capitalization of the list (classes and ranks, other religions, ...).
- `IMG_1423.md` — verified-no-source / high / body_changed=False — Body matches image; Borges Library of Babel text, not a canonical source; tagged needs-source
- `IMG_1424.md` — verified-no-source / high / body_changed=False — Video-still subtitle (MySaiBaba.com footage, not a game screenshot); subtitle matches; ShowImage true; needs-source
- `IMG_1427.md` — verified-no-source / high / body_changed=False — Himalayan Institute web page (Dakshinamurti story); body matches; no canonical source; needs-source
- `IMG_1428.md` — verified-no-source / high / body_changed=True — Replaced '[text cut off]' with ellipsis after 'inner self will' (image cut off there); Himalayan Institute page; needs-source
- `IMG_1539.md` — verified-no-source / medium / body_changed=True — Image is a Project Zomboid game screenshot whose only quote text is a truncated in-game subtitle (cut off mid-sentence in the image); transc
- `IMG_1540.md` — verified-no-source / high / body_changed=True — Project Zomboid game screenshot; only legible text is a subtitle fragment '...we will be slaves to the five desires which stem from the five
- `IMG_1541.md` — verified-no-source / high / body_changed=False — game screenshot (Project Zomboid, subtitle); subtitle matches; ShowImage true; needs-source
- `IMG_1542.md` — verified-no-source / medium / body_changed=True — Image is a Project Zomboid gameplay screenshot (Retromation) with one legible caption line: "In all things, there is neither male nor female
- `IMG_1543.md` — verified-no-source / medium / body_changed=True — Image is a Project Zomboid gameplay screenshot (Retromation watermark), not unreadable: the only text is an in-game subtitle from a media di
- `IMG_1544.md` — verified-no-source / high / body_changed=True — Image is a Project Zomboid game screenshot whose only content text is a single blue subtitle line, fully legible: 'One who eats meat kills t
- `IMG_1545.md` — verified-no-source / high / body_changed=False — game screenshot (Project Zomboid, subtitle); subtitle matches; ShowImage true; needs-source
- `IMG_1546.md` — verified-no-source / medium / body_changed=True — Project Zomboid game screenshot; only text is a legible subtitle fragment from an in-game 'Philosophical Quotes' disc: '...old age, sickness
- `IMG_1547.md` — non-quote / high / body_changed=False — Project Zomboid gameplay screenshot (Retromation video, inventory/loot UI); only quote-like text is a partial in-game subtitle fragment '...
- `IMG_1548.md` — verified-no-source / high / body_changed=True — Project Zomboid game screenshot; legible subtitle fragment transcribed (replaced '(image not legible)'). In-game media bar reads 'THE BUDDHA
- `IMG_1549.md` — verified-no-source / medium / body_changed=True — Image is a Project Zomboid game screenshot (Retromation video) whose only quote text is one truncated in-game subtitle; replaced '(image not
- `IMG_1550.md` — non-quote / high / body_changed=False — Image is a video-game screenshot (Project Zomboid, RetroMation watermark) with only a subtitle fragment '...from suffering and tend to cling
- `IMG_1551.md` — verified-no-source / high / body_changed=True — game screenshot (Project Zomboid, Retromation video); body set to legible subtitle 'But suffering is inseparable from pleasure.'; ShowImage:
- `IMG_1552.md` — verified-no-source / high / body_changed=True — game screenshot (Project Zomboid, Retromation video); body replaced with the legible subtitle line 'Therefore, the more we seek pleasure and
- `IMG_1553.md` — verified-no-source / high / body_changed=True — game screenshot (Project Zomboid, RetroMation video, PortaDisc playing a philosophy audio track): subtitle line transcribed exactly as shown
- `IMG_1554.md` — verified-no-source / high / body_changed=True — game screenshot (Project Zomboid, PortaDisc audio subtitle); replaced '(image not legible)' with the legible subtitle exactly as shown (trun
- `IMG_1557.md` — verified-no-source / medium / body_changed=False — Manga translator note page 18 (Rikudou); body matches; series not identified with confidence (possibly Vagabond); needs-source
- `IMG_1622.md` — verified-no-source / medium / body_changed=False — Sanskrit verse plus translation matches image; likely Ramana-related but no on-page attribution; needs-source
- `IMG_1623.md` — verified-clean / medium / body_changed=True — Split into 3 paragraphs, curly quotes/italics restored, completed truncated last line; source Letters from Sri Ramanasramam already set; ima
- `IMG_1625.md` — non-quote / high / body_changed=True — Not a wisdom quote and not a game screenshot: crisp excerpt from an engineering paper on flywheel energy storage (section 2.2.2 Electric Mac
- `IMG_1629.md` — verified-no-source / high / body_changed=False — Body matches image; text is Musashi's Book of the Void (Book of Five Rings), not a canonical book, so tagged needs-source
- `IMG_1630.md` — verified-clean / high / body_changed=False — Manga panel dialogue matches; removed needs-review
- `IMG_1632.md` — verified-clean / high / body_changed=False — Manga bubbles match in reading order; Edited true, added nature-creation tag, removed needs-review
- `IMG_1651.md` — non-quote / high / body_changed=False — Not a game screenshot: illustrated Tibetan manuscript scroll (meditating/reclining figures, mandalas, colored circles) with short handwritte
- `IMG_1658.md` — non-quote / high / body_changed=False — Video still of a sadhu before a sun mural, no text; left untouched, flags kept
- `IMG_1660.md` — verified-no-source / high / body_changed=False — Video still (documentary, not a game) with subtitle; body matches the subtitle; ShowImage true, needs-source
- `IMG_1661.md` — non-quote / high / body_changed=False — Not a game screenshot and has no text: black-and-white photo of Ramana Maharshi (seated on a tiger skin by a boulder) with a bearded standin
- `IMG_1706.md` — verified-no-source / high / body_changed=False — Blue Exorcist manga page (readblueexorcist.com), not canonical; body matches; needs-source
- `IMG_1707.md` — verified-clean / medium / body_changed=False — Body matches single bubble; kept earlier-assigned Mob Psycho 100 source, which I could not independently confirm from the image
- `IMG_1714.md` — verified-no-source / high / body_changed=False — Body already matches subtitle (the image says 'stop myself from internally suffering'; body matches). YouTube screenshot of Acharya Prashant
- `IMG_1735.md` — verified-no-source / high / body_changed=False — Body matches. Testament of St John of Rila from Byzantine Monastic Foundation Documents (Dumbarton Oaks), not canonical; needs-source.
- `IMG_1746.md` — verified-clean / high / body_changed=False — Body matches image; source already Siva Purana (verses 12-22, Mahadeva weekdays); no page number visible; Edited true.
- `IMG_1770.md` — verified-clean / high / body_changed=False — Body matches; header reads Path of Self-Knowledge by Arthur Osborne, p.195; Edited true.
- `IMG_6032.md` — verified-clean / medium / body_changed=False — Body matches (source typo 'nit like that' rendered as 'not'); Seung Sahn passage, source recognized by passage, not literally printed; no pa
- `IMG_6336.md` — verified-no-source / medium / body_changed=True — Bloom County (Berkeley Breathed) strip, not canonical; body reordered to panel order, one line per balloon; panel order of last three balloo
- `IMG_6337.md` — verified-no-source / high / body_changed=True — Not a game screenshot: Bloom County Sunday strip by Berke Breathed (April 17, 1983, book p.100), photographed sideways. Replaced '(image not
- `IMG_6338.md` — unreadable / high / body_changed=True — Bloom County panel cropped; only fragments visible ('...ran ...nd said, you saved ...h Reagan's'); body replaced with not-legible placeholde
- `IMG_6339.md` — verified-no-source / high / body_changed=True — Bloom County (Oct 9 1983), not canonical; fixed 'speed snake'->'jumbo-sized snake', 'their being survives on survival cooperation'->'their v
- `IMG_6434.md` — verified-no-source / high / body_changed=False — Web page screenshot (sribalajicafee.com blurb); kept the single quoted sentence; no canonical source.
- `IMG_6704.md` — verified-no-source / medium / body_changed=True — Table matches image; removed header row not visible in image (blank header); book unidentified.
- `IMG_6719.md` — verified-clean / medium / body_changed=True — Removed truncated trailing 'Learn to [text continues on next page]'; Ramana (Bhagavan) quote kept as source; hosting book unidentified.
- `IMG_6888.md` — verified-no-source / high / body_changed=True — Walking on Sunshine p149 (non-canonical); reduced to the 3-sentence passage, ShowImage true, needs-source.
- `IMG_6890.md` — verified-no-source / high / body_changed=True — Not a game screenshot: a legible book page, running header 'Awakened Leadership' p.184 (leadership-coaching text, not in the canonical list)
- `IMG_6891.md` — verified-no-source / high / body_changed=True — Awakened Leadership p186; body was upside-down OCR garbage; replaced with the italic set-off sentence, ShowImage true.
- `IMG_6892.md` — verified-no-source / high / body_changed=True — Everybody Into the Pool p187 (Awakened Leadership chapter); reduced to 2-sentence passage, added title, ShowImage true.
- `IMG_6893.md` — verified-no-source / high / body_changed=True — Same page as 6892; reduced to the set-off Bob Anderson passage plus attribution, ShowImage true.
- `IMG_6917.md` — verified-no-source / high / body_changed=False — Mandala (Arguelles) illustration page with lettered inscription; body matches; ShowImage true, needs-source.
- `IMG_6918.md` — verified-no-source / high / body_changed=True — Mandala (Arguelles) p.12: prose + photos + set-off Lao Tzu quotation; body is only the quotation; Lao Tzu not canonical, Mandala not canonic
- `IMG_6919.md` — non-quote / medium / body_changed=False — Photographed Mandala (Arguelles) p.13: left-cropped prose about Now/center/Mandala plus three captioned figures (Snow crystal; A flat repres
- `IMG_6920.md` — verified-no-source / low / body_changed=True — Page of Mandala (Arguelles) with plan of Mousgoum homestead, OM and yin-yang pictures, prose under 'The Center and the Polarities', and a se
- `IMG_6921.md` — non-quote / high / body_changed=False — Full-page picture (photomicrograph of a diatom, caption only: 'Photomicrograph of the Arachnoidisus Ehrenbergii', p.18, likely Mandala); no 
- `IMG_6922.md` — verified-no-source / medium / body_changed=True — Prose-only book page (appears to be Mandala, Arguelles, not a canonical source; no page number visible); body is one ~55-word excerpt, not f
- `IMG_6925.md` — non-quote / medium / body_changed=False — Mandala of the Ages plate, no real text; Mandala (Arguelles); page set 39; kept needs-manual-review, ShowImage true
- `IMG_6926.md` — non-quote / medium / body_changed=False — Illustration only, no caption; kept needs-manual-review
- `IMG_6927.md` — non-quote / medium / body_changed=False — Diagram with caption only; kept needs-manual-review
- `IMG_6928.md` — non-quote / medium / body_changed=False — Diagram with caption only; kept needs-manual-review
- `IMG_6929.md` — non-quote / medium / body_changed=False — Ouroboros diagram labels only; kept needs-manual-review
- `IMG_6930.md` — non-quote / medium / body_changed=False — Diagrams with captions only; kept needs-manual-review
- `IMG_6931.md` — verified-no-source / medium / body_changed=True — Book page (Mandala-style prose with diagrams, one set-off italic I Ching quotation 'Duration'); body = only that quotation; source not a can
- `IMG_6932.md` — verified-no-source / high / body_changed=True — Book page (Mandala, p.67) with prose, 2 diagrams, and a set-off italic quotation by Dane Rudhyar; body is only that quotation + attribution;
- `IMG_6933.md` — non-quote / high / body_changed=False — Rotated photo of a full-page illustrated diagram (zodiac signs, elements, solstices/equinoxes, +/- wedges; likely Mandala) with labels only 
- `IMG_6934.md` — non-quote / high / body_changed=False — Rotated page of Mandala (running foot 'Mandala of Bio-cyclic Rhythms', p.69): mostly an I Ching/zodiac mandala diagram plus technical prose 
- `IMG_6935.md` — verified-no-source / medium / body_changed=True — Mandala (Arguelles) rotated page; body trimmed to one 3-sentence passage; needs-source
- `IMG_6936.md` — non-quote / high / body_changed=False — Image is a full-page Tibetan thangka plate (wrathful Mahakala) photographed sideways; only text is a cropped plate caption ('Plate 8: Mahaka
- `IMG_6937.md` — non-quote / high / body_changed=False — Image is a photo of a full-page Tibetan Wheel of Life (Bhavachakra) thangka painting in a book, rotated 90 degrees; only a few tiny, illegib
- `IMG_6938.md` — verified-no-source / high / body_changed=True — Fallback mode: body is only the Kwaja Pulad of Erivan quotation; full page shown via ShowImage; book Mandala not canonical so needs-source.
- `IMG_6939.md` — verified-no-source / medium / body_changed=True — Epigraph by Tilopa (not canonical); body = quote + attribution; title added; needs-source
- `IMG_6940.md` — verified-no-source / medium / body_changed=True — Mandala (Arguelles) diagram page; body reduced to caption + petal labels, removed misattributed G. Tucci line; ShowImage on
- `IMG_6941.md` — verified-no-source / medium / body_changed=True — Fallback mode: book page (Purification / Centering sections, no set-off quotation, no visible title/page number; likely Mandala, Arguelles, 
- `IMG_6944.md` — verified-no-source / high / body_changed=True — Fallback mode: page is a 5-stanza tantric song (Eastern/Southern/Western/Northern Continent, Center), each ending 'Hum Hum Hum / Phat!', wit
- `IMG_6945.md` — verified-no-source / medium / body_changed=True — Fallback mode: photographed prose page (not a set-off quote) that looks like Mandala (Arguelles, not a canonical source). Body replaced with
- `IMG_6946.md` — non-quote / high / body_changed=False — Picture-only mandala plate with caption; kept needs-manual-review, ShowImage on
- `IMG_6947.md` — verified-no-source / medium / body_changed=True — Rotated book page, chapter 'Absorption' (Mandala): prose plus decorative pictures, no set-off quote; body = closing 2-sentence passage; no p
- `IMG_6948.md` — verified-no-source / medium / body_changed=True — Mandala 'Destruction' chapter; replaced placeholder with one ~60-word passage; removed unsupported Vidyeshvara Samhita source; page not visi
- `IMG_6949.md` — verified-no-source / medium / body_changed=True — Mandala 'Reintegration' page; trimmed to single best paragraph (quote-only treatment)
- `IMG_6950.md` — verified-no-source / medium / body_changed=True — Rotated book page (chapter 'Actualization', Mandala) of full prose, no set-off quote; body = single closing-paragraph sentence; no page numb
- `IMG_6951.md` — verified-no-source / high / body_changed=True — Mandala calligraphic plate; fixed text to 'And Through the Sun Beyond / What Even Man Or Flower Knows', page 106
- `IMG_6952.md` — verified-no-source / medium / body_changed=True — Mandala p109 dense page; trimmed to one ~55-word passage
- `IMG_6953.md` — verified-no-source / medium / body_changed=True — Page = mandala diagram (Curve of Developing Consciousness) plus prose, no set-off quote; body is one ~55-word passage on individualism; no p
- `IMG_6954.md` — verified-no-source / medium / body_changed=True — Blake set-off quote kept with attribution; removed Mandala commentary; Blake not canonical
- `IMG_6955.md` — non-quote / high / body_changed=False — Picture-only page (Plate 13 Shath Chakra chart + Plate 14 painting, captions only; no prose or set-off quotation); body left alone, ShowImag
- `IMG_6956.md` — non-quote / high / body_changed=False — Page is two full-page color mandala figure plates (Plate 15 Radiant Woman, Jose Arguelles; Plate 16 Radiant Man, Miriam Arguelles) with capt
- `IMG_7314.md` — verified-no-source / medium / body_changed=True — Not Mandala: Getting Things Done (Allen), non-canonical; quote-only 3-sentence passage, page 233
- `IMG_7315.md` — verified-no-source / medium / body_changed=True — Photo of a book page (running head 'The Power of the Key Principles | Part Three', business/productivity book on in-baskets/trust, likely Da
- `IMG_7316.md` — verified-no-source / medium / body_changed=True — Photo of a printed book page (running header 'The Power of the Key Principles | Part Three', a productivity/organization book, first-person 
- `IMG_7317.md` — verified-no-source / high / body_changed=True — Dense page of a modern copyrighted book (GTD-style, ch.11 Collection Habit), not canonical; trimmed body to 2 sentences, ShowImage true, nee
- `In olden days, when we were doing the cooking during summer, we used to have a pot into which we put.md` — verified-clean / high / body_changed=False — Body matched image; footer reads Letters from Sri Ramanasramam p.328; removed needs-review.
- `In truth there is no unalterable Dharma which the Tathagata could have taught.md` — verified-clean / high / body_changed=True — Fixed Dipamkara to Dipamkara with diacritic (Dipaṃkara); header Chun Chou Record; page not visible; removed needs-review.
- `Jnani conducts himself according to the wishes of others.md` — verified-clean / medium / body_changed=False — Body matches image; source not printed in image, kept existing attribution (typeface and 'said Bhagavan' style match Letters); Edited set tr
- `Knowing yet unable to move a single cell aware of the entire universe.md` — verified-no-source / medium / body_changed=False — Body matches the one-line crop; image shows no source, Dune attribution unverifiable so left source untouched but Edited false + needs-sourc
- `Kunju Swami meets Bhagavan for the first time.md` — verified-no-source / medium / body_changed=True — Added italics for Sanskrit terms, replaced [text continues] placeholder with the visible end of the sentence (up to mahavakyas); image cropp
- `Like the sky he provides shelter under his shade.md` — verified-clean / high / body_changed=False — Body matches; header confirms book and page 171; removed needs-review.
- `Lord Buddhas greatest grievance was that there is only suffering.md` — verified-no-source / high / body_changed=False — Video frame subtitle (MySaiBaba.com watermark), body matches; no canonical book identifiable; Edited false, needs-source.
- `Meditation is possible only if the ego is kept up.md` — verified-clean / high / body_changed=False — Body matches image (header Talks with Sri Ramana Maharshi); set Page 418, removed needs-review.
- `Moral nobility and not social respectability.md` — verified-no-source / high / body_changed=True — Rejoined 'cre- ative'; text is a Christian sermon (footnotes cite King, Strength to Love) not Path of Self Knowledge, so cleared wrong sourc
- `Non-duality means that only the Absolute is.md` — verified-clean / high / body_changed=False — Body matches; reader header confirms Path of Self-Knowledge (Osborne); removed needs-review.
- `Our original Buddha-Nature is, in highest truth, devoid of any atom of objectivity.md` — verified-clean / high / body_changed=True — Completed truncated ending ('Had there been'); Huang Po source already set, passage 8 recognizable; no page visible.
- `People understand what knowledge means but they understand it differently.md` — verified-clean / high / body_changed=True — Body text matched; restored italics emphasis; source In Search of the Miraculous kept (recognizable Gurdjieff passage), not literally stated
- `Present bondages are said to be of four types.md` — verified-clean / medium / body_changed=True — Fixed first line (wrongly all-italic, wrong opening quote); only Panchadasi italic. Source Letters from Sri Ramanasramam kept, not stated in
- `Restrain each single thought from arising then the Eighteen Sense Realms vanish.md` — verified-clean / high / body_changed=True — Fixed diacritics (Srāvakas, Kalirāja, Theravādin), 'him?!' to 'him?¹', added second footnote; Page 122 from running head Zen Teaching of Hua
- `Sahaja Nishta.md` — verified-clean / medium / body_changed=True — Added missing leading 'us,' and trailing 'Subsequently, the same'; source Letters from Sri Ramanasramam kept, not stated in image.
- `Self-negation and ultimate truth.md` — verified-no-source / high / body_changed=False — Urdu/Punjabi video subtitle frame; body matches; removed wrong Vivekachudamani source
- `Simply look at the flower and dont say anything.md` — verified-clean / high / body_changed=False — Body matches pp.105-106; Coming Home to Yourself kept
- `So many things in this world cannot be expressed with words. Some things can not be explained.md` — verified-clean / medium / body_changed=False — Vagabond manga dialogue matches; panel order ambiguous, kept
- `Sorrow is all there is there is nothing other than sorrow.md` — verified-no-source / high / body_changed=False — MySaiBaba.com video subtitle; no canonical source
- `Spiritual perfection changes even the body.md` — verified-clean / high / body_changed=False — Body matches; header Ramana Periya Puranam; no page number visible
- `Sri Guru ocean of mercy can anyone drenched with Thy kindness ever be afflicted.md` — verified-clean / high / body_changed=False — Body matches; Tripura Rahasya header p.8
- `Su Tung-p‘o wrote the follow  The roaring waterfall  is the Buddha’s golden mouth.md` — verified-no-source / medium / body_changed=False — Poem matches; book not identifiable; removed unsupported Huang Po source
- `That is because surrender means the Self itself.md` — verified-clean / high / body_changed=False — Body matches; Letters from Sri Ramanasramam p.413
- `That which rises as I is the mind it is only the mind.md` — verified-clean / high / body_changed=True — Body matched; removed running-header text from first line (kept date); cleared needs-review.
- `The Almighty has no address nor location where He can be found.md` — verified-no-source / high / body_changed=False — Video subtitle frame (MySaiBaba.com); no canonical source; Edited false, needs-source.
- `The Self remains untainted how can there be the distinctions of caste.md` — verified-clean / high / body_changed=True — Text matched; italicized disciple turns (opening fragment and Q19) per dialogue rule; cleared needs-review.
- `The Vedas contain the truth but the truth cannot be expressed in words.md` — verified-clean / high / body_changed=False — Body matches image; cleared needs-review.
- `The approach to it is called the Gateway of the Stillness beyond all Activity.md` — verified-clean / high / body_changed=False — Body matches image (Q/A format intact); no page number visible; cleared needs-review.
- `The doctrine of Advaita Non-duality taught by the ancient Rishis.md` — verified-clean / medium / body_changed=False — Body matches image; existing source kept (not stated in image); cleared needs-review.
- `The dualities of shame attraction and aversion.md` — verified-no-source / high / body_changed=False — Table matches image; source not identifiable; Edited false, needs-source.
- `The fear is created by the ego and the ego has to face this fear coal charcoal gunpowder.md` — verified-clean / high / body_changed=False — Body matches image; running header says Ramana Periya Puranam; set Page 240; draft untouched.
- `The first thing as I see you I see you miserable.md` — verified-clean / medium / body_changed=False — Body matches image (cuts off at 'they always'); image has no attribution, kept existing source (Osho text); removed needs-review.
- `The idea of one Self being aware of another Self is absurd.md` — verified-clean / high / body_changed=False — Body matches image; header reads Talks with Sri Ramana Maharshi; removed needs-review.
- `The king remained motionless like a statue.md` — verified-clean / high / body_changed=True — Added truncated final word 'is'; header and page 404 confirmed; removed needs-review.
- `The king said that he was at the very moment placing at the feet of the Guru his body, his mind, his.md` — verified-clean / high / body_changed=False — Body matches image; header and page 405 confirmed; removed needs-review.
- `The sage is unattached to anything or anybody.md` — verified-clean / medium / body_changed=False — Body matches image; no header in image, kept existing Yoga Vasistha source (Venkatesananda-style text); removed needs-review.
- `The universe is a university to educate the soul.md` — verified-no-source / high / body_changed=False — Body matches image; no attribution visible and no canonical source identifiable; tag needs-source; draft left true.
- `The universe is nothing but consciousness.md` — verified-clean / high / body_changed=True — Added missing closing bracket after 'eternal.'; page 241 confirmed; removed needs-review.
- `There has never been a single thing then where does dust alight.md` — verified-clean / high / body_changed=False — Body matches image; header 'The Chun Chou Record' confirms Huang Po; no page number shown; removed needs-review.
- `There is a remedy for sorrow.md` — verified-no-source / high / body_changed=False — MySaiBaba.com video subtitle frame; body matches; Edited false, needs-source.
- `There is no bondage no liberation no aspirant no seeker.md` — verified-clean / high / body_changed=False — Body incl. Sanskrit and Upadesa Saram verse 15 matches page header/525; removed needs-review.
- `There is only one God - the language, location, and system may be different.md` — verified-no-source / high / body_changed=False — Video subtitle frame; body matches; cleared non-canonical source; Edited false, needs-source.
- `They teach the three emancipations of emptiness, signlessness, wishlessness and nonactivation.md` — verified-clean / high / body_changed=True — Removed trailing [...] not in image; rest matches; removed needs-review.
- `This chapter deals with all the preparatory steps which were needed before the creation of bio-units.md` — verified-clean / medium / body_changed=False — Body matches image, page 369 visible; source kept (Quranic/jinn/clay content, Tahir Ahmad book); removed needs-review.
- `This course would have been better for every seeker.md` — verified-no-source / high / body_changed=False — Body matches; crane-incident text is not Tripura Rahasya so cleared wrong source; added tag mind; Edited false, needs-source.
- `Three ways to describe truth - The same truth has to be expressed in different ways to suit the capa.md` — verified-clean / medium / body_changed=True — Restored missing closing 'The letter continued, "In the' and italicised Sanskrit terms; page 174 visible; source unproven by image but alrea
- `Titov the Russian cosmonaut returned from space and declared there is no God.md` — verified-no-source / high / body_changed=False — Body matches; Ramana Periya Purnam clearly wrong so cleared; no source identifiable; Edited false, needs-source.
- `To the degree that you turn away from attachments to the unreal.md` — verified-clean / medium / body_changed=False — Body matches image (cropped mid-sentence, as in image); source kept from earlier pass (Master/numbered verses), no page visible.
- `What is it to have skillful means with ones wisdom emancipated.md` — verified-clean / high / body_changed=False — Body matches image; image is dBET Vimalakirti PDF p112.
- `What is the ego and how is it related to the Self.md` — verified-clean / high / body_changed=False — Talks 207-208 match image exactly; p181 visible.
- `When I enquired what it was Bhagavan led me to see.md` — verified-clean / high / body_changed=False — Body matches image; running header and p386 visible.
- `Where is the place of enlightenment.md` — verified-clean / high / body_changed=True — Fixed wrong-direction nested quotes (“’ to “‘) in verses 7 and 8; rest matched.
- `Why fall into nirvikalpa samadhi, without gaining the fruit of its wisdom!.md` — verified-no-source / medium / body_changed=False — Body matches verses 108-110; image has no title/header and typeface differs from the 105-106 Kaivalya Navaneetam image, so source not confid
- `Yet, his vocational detour to the Society of Jesus had not been without purpose.md` — verified-no-source / high / body_changed=False — Body matches e-reader screenshot; biography of Saint Anthony Claret, not a canonical source.
- `You fly about like birds from another world.md` — unreadable / medium / body_changed=True — Image is cropped at right edge; fixed fabricated 'to k[eep' to 'to b[…]'; set Edited false + needs-manual-review since quote is a fragment (
- `Your hunger and thirst for bliss is absolutely fulfilled.md` — verified-clean / high / body_changed=False — Body matched image; Nisargadatta dialogue, source already set; removed needs-review
- `Your true identity is beyond all concepts.md` — verified-clean / high / body_changed=True — Italicized avatars per image; running header confirms book/page
- `accept all of the pain.md` — verified-clean / high / body_changed=False — Manga panel dialogue matches; image shows onepunchmanmanga URL
- `be aware of yourself and you will see light in the deepest recesses of your core.md` — verified-clean / high / body_changed=False — Two-page spread matches body; header confirms book
- `d5ff7981-9d8c-4885-8d2f-13b44091f9a2.md` — verified-no-source / high / body_changed=False — Shiva meme text matches; no attributable source; tagged needs-source
- `great secret of the five-fold duties.md` — verified-clean / high / body_changed=False — Body matches image; no page number visible
- `such a man becomes seated in the lap of God.md` — verified-clean / medium / body_changed=False — Body matches; source previously set, recognizable passage; no page visible
- `the inner voice is not a voice it is silence.md` — verified-clean / high / body_changed=False — Body matches; footer shows The Search / 94 / Osho
