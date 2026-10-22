import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { FullSlug, resolveRelative } from "../util/path"
import { displayTitle, isQuoteSlug } from "./RelatedQuotes"
import style from "./styles/themeIndex.scss"

// The editorial topic vocabulary (ai/quote-review/EDIT-RULES.md, "Tag vocabulary").
// Workflow flags (needs-*) and stray tags are deliberately not themes.
// A label is given only where title-casing the tag would read wrong.
const THEMES: Record<string, string | null> = {
  "nature-creation": "Nature & Creation",
  mind: null,
  divine: null,
  "guru-teacher": "Guru & Teacher",
  "knowledge-wisdom": "Knowledge & Wisdom",
  "love-devotion": "Love & Devotion",
  consciousness: null,
  service: null,
  meditation: null,
  "self-knowledge": "Self-Knowledge",
  suffering: null,
  liberation: null,
  silence: null,
  "death-impermanence": "Death & Impermanence",
  ego: null,
  scripture: null,
  "faith-trust": "Faith & Trust",
  surrender: null,
  "non-duality": "Non-Duality",
  detachment: null,
  humility: null,
}

const MAX_SAMPLES = 5
// A theme repeats an already-shown quote only to reach this many samples.
const MIN_SAMPLES = 3

// FNV-1a (32-bit): a stable "shuffle key" so samples mix sources instead of
// clustering at the start of the alphabet, yet stay identical build to build.
const fnv1a = (s: string): number => {
  let h = 0x811c9dc5
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i)
    h = Math.imul(h, 0x01000193)
  }
  return h >>> 0
}
const THREAD_STOPWORDS = new Set(["the", "thread", "of"])

const themeLabel = (tag: string): string =>
  THEMES[tag] ??
  tag
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ")

// Mirrors the RemoveDrafts filter.
const isDraft = (fm: Record<string, unknown> | undefined): boolean =>
  fm?.draft === true || fm?.draft === "true"

const cleanSource = (raw: unknown): string =>
  String(raw ?? "")
    .replace(/\[\[/g, "")
    .replace(/\]\]/g, "")
    .trim()

// A slug-derived title like "IMG 1286" or a UUID reads as noise in a sample list.
const looksMachineNamed = (title: string): boolean =>
  /^img[\s_]\d+$/i.test(title) || /^[0-9a-f]{8}[\s-][0-9a-f]{4}/i.test(title)

const slugWords = (slug: string): string[] =>
  decodeURIComponent(slug.split("/").pop() ?? slug)
    .toLowerCase()
    .split(/[-\s_]+/)
    .filter((w) => w && !THREAD_STOPWORDS.has(w))

type Sample = { slug: FullSlug; title: string; source: string; humanTitle: boolean }
type Thread = { slug: FullSlug; title: string; words: Set<string> }

const ThemeIndex: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
  const here = (fileData.slug ?? "Themes") as FullSlug

  const byTag = new Map<string, Sample[]>()
  for (const f of allFiles) {
    const fSlug = f.slug ?? ""
    if (!isQuoteSlug(fSlug) || isDraft(f.frontmatter)) continue
    const tags = new Set(
      ((f.frontmatter?.tags as string[] | undefined) ?? []).map((t) => String(t).toLowerCase()),
    )
    const title = displayTitle(f.frontmatter, fSlug)
    const sample: Sample = {
      slug: fSlug as FullSlug,
      title,
      source: cleanSource(f.frontmatter?.source),
      humanTitle: !looksMachineNamed(title),
    }
    for (const tag of tags) {
      if (!(tag in THEMES)) continue
      const list = byTag.get(tag) ?? []
      list.push(sample)
      byTag.set(tag, list)
    }
  }

  const threads: Thread[] = allFiles
    .filter((f) => {
      const s = f.slug ?? ""
      return s.startsWith("Threads/") && s !== "Threads/index" && !isDraft(f.frontmatter)
    })
    .map((f) => ({
      slug: f.slug as FullSlug,
      title: displayTitle(f.frontmatter, f.slug ?? ""),
      words: new Set(slugWords(f.slug ?? "")),
    }))
    .sort((a, b) => a.slug.localeCompare(b.slug))

  const threadFor = (tag: string): Thread | undefined =>
    threads.find((t) => tag.split("-").some((w) => t.words.has(w)))

  const themes = [...byTag.entries()]
    .map(([tag, quotes]) => ({ tag, quotes }))
    .sort((a, b) => b.quotes.length - a.quotes.length || a.tag.localeCompare(b.tag))

  if (themes.length === 0) return null

  // Assign samples in theme order (largest first) so each quote headlines at
  // most one theme; fall back to repeats only to reach MIN_SAMPLES.
  const used = new Set<string>()
  const samplesByTag = new Map<string, Sample[]>()
  for (const { tag, quotes } of themes) {
    // Sourced passages first, then real titles over machine names, then hash spread.
    const ranked = [...quotes].sort(
      (a, b) =>
        Number(!!b.source) - Number(!!a.source) ||
        Number(b.humanTitle) - Number(a.humanTitle) ||
        fnv1a(a.slug) - fnv1a(b.slug) ||
        a.slug.localeCompare(b.slug),
    )
    const picked = ranked.filter((q) => !used.has(q.slug)).slice(0, MAX_SAMPLES)
    for (const q of ranked) {
      if (picked.length >= MIN_SAMPLES) break
      if (!picked.includes(q)) picked.push(q)
    }
    picked.forEach((q) => used.add(q.slug))
    samplesByTag.set(tag, picked)
  }

  return (
    <div class="theme-index">
      {themes.map(({ tag, quotes }) => {
        const samples = samplesByTag.get(tag) ?? []
        const n = quotes.length
        const thread = threadFor(tag)
        return (
          <section class="theme-index__theme" id={`theme-${tag}`}>
            <h2 class="theme-index__heading">
              <span class="theme-index__label">{themeLabel(tag)}</span>
              <span class="theme-index__count">{n === 1 ? "1 passage" : `${n} passages`}</span>
            </h2>
            <ul class="theme-index__list">
              {samples.map((q) => (
                <li class="theme-index__item">
                  <a
                    class="theme-index__link internal"
                    href={resolveRelative(here, q.slug)}
                    data-no-popover
                  >
                    <span class="theme-index__title">{q.title}</span>
                    {q.source && <span class="theme-index__source">{q.source}</span>}
                  </a>
                </li>
              ))}
            </ul>
            <p class="theme-index__more">
              <a class="internal" href={resolveRelative(here, `tags/${tag}` as FullSlug)}>
                {n === 1 ? "The 1 passage" : `All ${n} passages`} &rarr;
              </a>
              {thread && (
                <a class="internal theme-index__thread" href={resolveRelative(here, thread.slug)}>
                  Read {thread.title} &rarr;
                </a>
              )}
            </p>
          </section>
        )
      })}
    </div>
  )
}

ThemeIndex.css = style

export default (() => ThemeIndex) satisfies QuartzComponentConstructor
