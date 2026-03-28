# Bad Quote Triage — 2026-03-23

Scanned 83 flagged files from `bad-quotes-list.txt`. Each file was read in full and classified.

---

## TRUE_BAD (21 files) — Should be drafted

| # | Filename | Reason |
|---|----------|--------|
| 1 | `All is One.md` | Body is only "All is one." (12 chars). Too short to be useful as standalone page. |
| 2 | `Becoming a reminder of human foolishness.md` | Body is truncated OCR fragment: "ecoming a reminder to us of human foolishness." (46 chars, missing first letter). |
| 3 | `Before its birth it does not exist nor does it continue after death.md` | Contains raw URL (`http://www.advaitin.net/...`), standalone page number `172`, and heavy OCR garbage: `qitraanicaiecal Aca agsty Saar`, `panipadadimandeho`, garbled Devanagari-Latin mix. |
| 4 | `Bhagavans silence was his direct teaching...comprehend.md` | Body starts with massive OCR garbage: `PEEUNSEE VVEREE bon 1eBevattl VVEENSEE FINS VVC SUITE EEE GE INe beatieatined`. Legitimate text follows but the garbled prefix is severe. |
| 5 | `Crying is an act of atonement.md` | Body is OCR fragment: `~~ a  waded  Crying is an act of atonement.` (43 chars with artifacts). |
| 6 | `For those who are attached to the unreal...continues.md` | Contains OCR garbage: `PHeaad: TARR TASa FUT AACA ANAT:`, `TACHA S TIT: FAASAT AHGEATY`, garbled Devanagari-Latin mix throughout second half. |
| 7 | `How did the Self that ever is Awareness bliss...forgotten.md` | Massive OCR garbage: `FEAST OHHSUOTUW Siro HHSILD wn hsSaTGuTev oTLILILG`, `ABDILIGveval`, `ADYUS SHYSU SHYSU`, pages of garbled text. Legitimate 3-line poem at the end but body is 90% garbage. |
| 8 | `I am so small.md` | Body is only "I'm nothing. I am so small." (27 chars). Too short. |
| 9 | `I feel so alone.md` | Body is only "I feel so alone" (15 chars). Too short. |
| 10 | `IMG_1292.md` | Non-descriptive IMG_ filename. Body is fragment: "begins to believe that perhaps he is not destined to be happy. )" — truncated with stray parenthesis. |
| 11 | `IMG_1293.md` | Non-descriptive IMG_ filename. Body is fragment: "He gets accustomed to this state, and says to God, )" — truncated with stray parenthesis. |
| 12 | `If the mind is turned inwards God manifests as inner consciousness.md` | Starts with severe OCR garbage: `LY... SALLY UIW SHU AUIDS TalWLIdl ALU ULIIELOELIU TLUTITT UL OUI.` Legitimate Ramana dialogue follows but opening line is garbled. |
| 13 | `Image Avalokateshvara Gantz.md` | Empty body — frontmatter only, no content at all. |
| 14 | `Just as you would not identify yourself with your shadow.md` | Contains OCR garbage in second half: `N c ik D`, `FATES STAT TS`, `Adeddecd Se at ACA`, `aad J Prd A GAHAN Ul 164 ti`, garbled Devanagari-Latin mix. |
| 15 | `Sai Baba teachings on devotion and surrender.md` | Contains heavy OCR garbage interleaved with legitimate text: `LIS GuIT oT :- Soren FTWeMwwUyM BMonoSwybd`, `Guire Ts co:-`, `AaflecpnrGon! LU sosHled wolls saps`, `sMecdc amhaGor Gurmeat`. Garbled text is ~50% of body. |
| 16 | `Self-negation and ultimate truth.md` | Body is OCR fragment with artifacts: `Ub blue Fel Pet  SELF-NEGATION AND ULTIMATE TRUTH ARE THE SLOGANS OF LOVE` (garbled prefix). |
| 17 | `The body is a product of food...material sheath.md` | Clean English paragraph followed by heavy OCR garbage: `SNR NG`, `Ya AAT arated`, `TTT: HOTU S AAET ATE:`, `AAT SISAA YSIUNEAIATa:`, garbled Devanagari-Latin throughout. |
| 18 | `The jnani sees no one as an ajnani.md` | Contains OCR garbage: `Venba. BTS Qo HlL_omev ujL_o Aas waGlocorGer Catt. — Boos LOTUIT MMeHWI BTL LOTWSRISSMT oomolurrerflitHev Sunt oucflum Glsorfl.` |
| 19 | `There is no bondage no liberation...no seeker.md` | Contains OCR garbage: `ACAMACREAITA: BAA Fe TAA Fea:` inline with otherwise legitimate text. |
| 20 | `They are reading the four Vedas and you are doing Vedanta.md` | Contains OCR garbage: `i a iow ies ~ AAO AHATOT TCTHATIOT TAT Pn a an BICHAFASP TA eld areca` inline with Bhagavan's teaching. |
| 21 | `We capitulate to sleep but the Self is still there.md` | Opens with OCR garbage: `VCAPULICLIVEYU It oIeep ULL.` Legitimate Ramana teaching follows but garbled opener. |

---

## FALSE_POSITIVE (62 files) — Keep published

| # | Filename | Why it's fine |
|---|----------|---------------|
| 1 | `All that can be done can be done through understanding.md` | SADHANA is legitimate Sanskrit term used in context ("the only SADHANA — spiritual practice"). |
| 2 | `All the pentads to be contemplated.md` | DESCRIPTION, PENTADS, DISCARDED are legitimate chapter headers from The Ribhu Gita. |
| 3 | `All these things are within the Self.md` | BRAHMANA, SIKHIDHVAJA, VASISTHA are character names from Tripura Rahasya. |
| 4 | `BHAGAVANS HANDWRITING...transcendental s.md` | BHAGAVAN and HANDWRITING are the subject of the quote. Legitimate meme image. |
| 5 | `Bhagavan discoursed on the nature of the heart.md` | SEPTEMBER and VASISTHA are date header and character name from Day by Day. |
| 6 | `Bhagavan spoke about the nature of jnana.md` | DECEMBER and VASISTHA are date header and character name from Day by Day. |
| 7 | `Bondages of the past the future and the present.md` | OMNIPRESENT is legitimate English word in context. |
| 8 | `Church and State scientific reason and faith.md` | PREACHER and ARRAKEEN are Dune character/place names: "THE PREACHER AT ARRAKEEN". |
| 9 | `Detachment from worldly desires leads to liberation.md` | Standalone "94" is a verse number in Ashtavakra Gita context. Borderline but content is clean. |
| 10 | `Dharma is neither preached in words nor otherwise signified.md` | YOURSELVES is legitimate emphasis in Huang Po text. |
| 11 | `Do not exploit this gift...personal advantage.md` | GREATER, COMMUNITY, SPIRITUALITY are the book title "GREATER COMMUNITY SPIRITUALITY". |
| 12 | `Do not permit the events of your daily lives to bind you.md` | WITHDRAW, YOURSELVES are legitimate emphasis in Huang Po's original text. |
| 13 | `Endowed with discrimination and dispassion.md` | TRITALA, BHAGIRATHA are character names from Yoga Vasistha. |
| 14 | `Food consecration mantra from the Bhagavad Gita.md` | BISHMUR, JANARDANAHI, GYANTWA etc. are transliterated Sanskrit mantra words. Legitimate. |
| 15 | `Gratitude is meditation being silently here now...opens up.md` | COCONUT, PARTAKEN, RESPECT are legitimate English words in Osho teaching. |
| 16 | `Having many sorts of knowledge...SEEKING for anything.md` | SEEKING is original emphasis from Huang Po text. |
| 17 | `He was therefore peaceful in both pain and pleasure.md` | VASISTHA is a character name from Yoga Vasistha. |
| 18 | `I GUESS I THOUGHT THAT ONLY...ANYONE.md` | All-caps is the original style of the Mob Psycho 100 meme. Legitimate. |
| 19 | `I am Brahman...abide in Silence at ease.md` | SUMMARY, SETTLED, CONCLUSIONS are chapter header words from The Ribhu Gita. |
| 20 | `I am cool you throw fire at me and it becomes cool.md` | DISCIPLE, HOSTILE, EXCLAIMED are legitimate English words in Osho/Buddha story. |
| 21 | `It is only living a thing totally that one transcends it.md` | SOMETIMES, PASSIONATE, SILENTLY are legitimate emphasis in Osho teaching. |
| 22 | `Learn how to be entirely unreceptive...external forms.md` | TEACHING, PERCEPTION, ENTIRELY etc. are section headers/emphasis in Huang Po. Page numbers are footnote markers. |
| 23 | `Live in this world because this world gives a ripening.md` | CHAPTER and CONFUSIVA are legitimate (chapter header "VIA CONFUSIVA" from The Perfect Master). |
| 24 | `Making use of things does not defile you...separate self.md` | TEACHING is a section header in Huang Po. |
| 25 | `Most people are so totally identified...they are.md` | ANALYSIS and ISHWARANANDA are legitimate words (SELF-ANALYSIS, SWAMI SHRI ISHWARANANDA GIRI). |
| 26 | `Negation of name and form reveals the Self.md` | NEGATION is a chapter header from The Ribhu Gita. |
| 27 | `No matter how exotic human civilization...outgrows the universe.md` | TLEILAXU is a legitimate Dune faction name ("FROM THE TLEILAXU GODBUK"). |
| 28 | `On account of infinite consciousness...exist.md` | VASISTHA is a character name. |
| 29 | `Only gratitude transforms...opposite to desires.md` | DESIRES, CAPACITY, WITHOUT etc. are legitimate emphasis in Osho teaching. |
| 30 | `Pouring God into God if you know what I mean.md` | BRAHMAPANAM, BRAHMAGNI, BRAHMAN are transliterated Sanskrit mantra. |
| 31 | `RELYING ON WORDS YOURE FAMILIAR WITH WILL LEAD YOU ASTRAY.md` | All-caps is original Vagabond manga style. |
| 32 | `Restrain each single thought...Eighteen Sense Realms vanish.md` | TEACHING, SEEKING are section headers in Huang Po. Page number 122 is a page reference. |
| 33 | `Self alone is the reality all else is appearance.md` | VASISTHA is a character name. |
| 34 | `Sikhidhvaja renounces his kingdom for truth.md` | SIKHIDHVAJA, BRAHMANA are character names from Tripura Rahasya. |
| 35 | `That in which there is the fullness of Consciousness...That itself.md` | INSTRUCTION, ABIDING are chapter header words from The Ribhu Gita. |
| 36 | `The Gateway of Non-Duality is your original Mind.md` | TEACHING, PONDERING, THEREBY are emphasis in Huang Po. Page numbers are footnote refs. |
| 37 | `The Self alone remains after all illusion is destroyed.md` | DECEMBER, VASISTHA are date header and character name. |
| 38 | `The distress of the mind...enquiry into the nature of the self.md` | MANDAVYA is a character name from Yoga Vasistha. |
| 39 | `The divine Name chanting it one is transported across.md` | Pipe artifacts are actually Devanagari/Gurmukhi script from Guru Granth Sahib. Legitimate mixed-script content. |
| 40 | `The dualities of shame attraction and aversion.md` | DUALITIES is the header of a table/chart. Legitimate reference content. |
| 41 | `The first thing as I see you I see you miserable.md` | Content is clean Osho teaching. No actual pipe artifacts found in meaningful way. |
| 42 | `The mind is a bundle of thoughts arising from the I-thought.md` | Contains ASCII art diagrams (dashes, pipes) representing Ramana's teaching illustrations. Legitimate formatting. |
| 43 | `The mind is only a bundle of thoughts.md` | SEPTEMBER and VASISTHA are date header and character name from Day by Day. |
| 44 | `The sage does not teach by words but by his living presence.md` | Content is clean Ramana Periya Purnam text about Robert Adams. Minor OCR at very end (`f j J saat`) but content is excellent. |
| 45 | `The trance-state of prophecy is like no other vision.md` | JOURNALS is from "THE STOLEN JOURNALS" — a Dune source attribution. |
| 46 | `The universal human pain-body.md` | CHILDREN is a section header "THE PAIN-BODY IN CHILDREN". |
| 47 | `The universe is just there that is the only way.md` | FEDAYKIN is a Dune term ("MUAD'DIB TO HIS FEDAYKIN"). |
| 48 | `The whole world is but a long dream.md` | BHUSUNVA is a character name from Yoga Vasistha ("BHUSUNVA continued:"). |
| 49 | `There has never been a single thing then where does dust alight.md` | REASONING is legitimate emphasis in Huang Po text. |
| 50 | `There is no liberation for a person of mere book knowledge.md` | ATLASES is garbled Devanagari, but the English content is clean and the garbled portion is just the Sanskrit transliteration section which is typical of Vivekachudamani OCR. Borderline — keeping as the English content is valuable. |
| 51 | `There is unbroken flow of peace...bliss of the absolute,.md` | VASISTHA is a character name. |
| 52 | `This chapter deals with all the preparatory steps...bio-units.md` | ESSENTIAL, PHOTOSYNTHESIS, EVOLUTION are legitimate English words. Page number 369 is original page reference. |
| 53 | `This world-appearance is a confusion...optical illusion.md` | VASISTHA and VAMPIRE are character names from Yoga Vasistha (the vampire parable). |
| 54 | `Thus spake Vasistha on the nature of liberation.md` | VASISTHA is a character name. |
| 55 | `To enjoy the fruits of the worship...Lord Siva.md` | INITIATION is a chapter header from The Ribhu Gita. |
| 56 | `We are the truth...like the musk deer.md` | Content is clean Ramana Periya Purnam text. No actual pipe artifacts in meaningful context. |
| 57 | `What exists is the one Self only.md` | DECEMBER, VASISTHA are date header and character name. |
| 58 | `You will recognize all minds as One and behold all things as One.md` | TEACHING, SEEKING are emphasis in Huang Po. Page numbers are footnote refs. Duplicate of file #36 content — same Huang Po passage. |
| 59 | `absolute consciousness...there is nobo.md` | CONSCIOUSLY, SCHOLAR, SCHOLARS are legitimate English words in Osho/Jesus teaching. |
| 60 | `if you COMPLETELY SURRENDER ALL your responsibilities to ME.md` | COMPLETELY and SURRENDER are original emphasis in Ramana meme. |
| 61 | `the inner voice is not a voice it is silence.md` | BELOVED is from "BELOVED OSHO" — an address to the teacher. |
| 62 | `touch the divine Master seated within you.md` | ISHWARANANDA is the teacher's name (Swami Shri Ishwarananda Giri). |

---

## Summary

- **Total flagged:** 83
- **TRUE BAD (draft these):** 21
- **FALSE POSITIVE (keep):** 62

### Categories of TRUE BAD:
- **OCR garbage text (garbled character sequences):** 14 files
- **Too short / truncated fragments:** 5 files
- **Empty body:** 1 file
- **Non-descriptive IMG_ filename with fragment body:** 2 files
- **Raw URLs in body:** 1 file (overlaps with OCR garbage)
