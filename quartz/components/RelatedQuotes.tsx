import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative } from "../util/path"
import { FullSlug } from "../util/path"

// Tags that describe editorial workflow / format, not topic — ignored when
// computing thematic relatedness.
const NOISE_TAGS = new Set([
  "needs-review",
  "needs-manual-review",
  "screenshot",
  "meme",
])

// How many related passages to surface.
const MAX_RELATED = 4
// Score weights.
const SAME_SOURCE_WEIGHT = 5
const SHARED_TAG_WEIGHT = 1

const normalizeSource = (raw: unknown): string =>
  String(raw ?? "")
    .replace(/\[\[/g, "")
    .replace(/\]\]/g, "")
    .trim()
    .toLowerCase()

const topicTags = (fm: Record<string, unknown> | undefined): string[] => {
  const tags = (fm?.tags as string[] | undefined) ?? []
  return tags
    .map((t) => String(t).toLowerCase())
    .filter((t) => t && !NOISE_TAGS.has(t))
}

const isQuoteSlug = (slug: string): boolean =>
  slug.startsWith("Wisdom-Quotes/") &&
  slug !== "Wisdom-Quotes/index" &&
  !slug.includes("Images/")

const displayTitle = (fm: Record<string, unknown> | undefined, slug: string): string => {
  const t = fm?.title
  if (t && String(t).trim()) return String(t)
  // Fall back to the last path segment, de-slugified.
  const last = slug.split("/").pop() ?? slug
  return decodeURIComponent(last).replace(/-/g, " ")
}

const RelatedQuotes: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
  const slug = fileData.slug ?? ""
  if (!isQuoteSlug(slug)) return null

  const mySource = normalizeSource(fileData.frontmatter?.source)
  const myTags = new Set(topicTags(fileData.frontmatter))

  type Scored = { slug: FullSlug; title: string; source: string; score: number; sameSource: boolean }

  const scored: Scored[] = []
  for (const f of allFiles) {
    const fSlug = f.slug ?? ""
    if (fSlug === slug) continue
    if (!isQuoteSlug(fSlug)) continue
    if (f.frontmatter?.draft === true) continue

    const fSource = normalizeSource(f.frontmatter?.source)
    const sameSource = !!mySource && fSource === mySource

    let score = 0
    if (sameSource) score += SAME_SOURCE_WEIGHT
    if (myTags.size) {
      for (const t of topicTags(f.frontmatter)) {
        if (myTags.has(t)) score += SHARED_TAG_WEIGHT
      }
    }
    if (score <= 0) continue

    scored.push({
      slug: fSlug as FullSlug,
      title: displayTitle(f.frontmatter, fSlug),
      source: normalizeSource(f.frontmatter?.source)
        ? String(f.frontmatter?.source).replace(/\[\[/g, "").replace(/\]\]/g, "").trim()
        : "",
      score,
      sameSource,
    })
  }

  if (scored.length === 0) return null

  // Highest score first; same-source ties broken toward same source; then title.
  scored.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score
    if (a.sameSource !== b.sameSource) return a.sameSource ? -1 : 1
    return a.title.localeCompare(b.title)
  })

  const related = scored.slice(0, MAX_RELATED)

  return (
    <div class="related-quotes">
      <h2 class="related-quotes__heading">Kindred passages</h2>
      <ul class="related-quotes__list">
        {related.map((r) => (
          <li class="related-quotes__item">
            <a class="related-quotes__link internal" href={resolveRelative(slug, r.slug)} data-no-popover>
              <span class="related-quotes__title">{r.title}</span>
              {r.source && <span class="related-quotes__source">{r.source}</span>}
            </a>
          </li>
        ))}
      </ul>
    </div>
  )
}

RelatedQuotes.css = `
.related-quotes {
  margin: 2.5rem 0 0.5rem 0;
  padding-top: 1.4rem;
  border-top: 1px solid var(--lightgray);
}

.related-quotes__heading {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--gray);
  font-weight: 600;
  margin: 0 0 0.9rem 0;
}

.related-quotes__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.related-quotes__item {
  margin: 0;
}

.related-quotes__link {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.7rem 0.9rem;
  border-radius: 10px;
  background: color-mix(in srgb, var(--light) 92%, var(--lightgray));
  text-decoration: none !important;
  background-image: none !important;
  transition: background 0.18s ease, transform 0.15s ease;
}

.related-quotes__link:hover {
  background: color-mix(in srgb, var(--light) 80%, var(--lightgray));
  transform: translateX(2px);
  color: inherit;
}

.related-quotes__title {
  font-size: 0.98rem;
  line-height: 1.45;
  color: var(--darkgray);
}

.related-quotes__source {
  font-size: 0.74rem;
  color: var(--gray);
  letter-spacing: 0.02em;
}

@media (max-width: 800px) {
  .related-quotes {
    margin-top: 2rem;
  }
  .related-quotes__title {
    font-size: 0.92rem;
  }
}
`

export default (() => RelatedQuotes) satisfies QuartzComponentConstructor
