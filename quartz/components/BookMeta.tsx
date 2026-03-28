import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative } from "../util/path"

const difficultyLabels: Record<string, string> = {
  approachable: "\u{1F331} Approachable",
  intermediate: "\u{1F333} Intermediate",
  advanced: "\u{1F3D4}\u{FE0F} Advanced",
}

const BookMeta: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
  const slug = fileData.slug ?? ""

  // Only render on book pages (not index, not templates)
  if (!slug.startsWith("Books/") || slug === "Books/index" || slug.startsWith("Books/_")) {
    return null
  }

  const tradition = (fileData.frontmatter?.tradition as string) ?? ""
  const description = (fileData.frontmatter?.description as string) ?? ""
  const difficulty = (fileData.frontmatter?.difficulty as string) ?? ""
  const category = (fileData.frontmatter?.category as string) ?? ""
  const teacherRaw = (fileData.frontmatter?.teacher as string) ?? ""

  // Parse teacher wiki-link: "[[Teacher Name]]" → "Teacher Name"
  const teacherName = teacherRaw.replace(/\[\[/g, "").replace(/\]\]/g, "").trim()

  // Find teacher page
  const teacherPage = teacherName
    ? allFiles.find(
        (f) =>
          f.frontmatter?.title === teacherName && f.slug?.startsWith("Teachers/"),
      )
    : null

  // Find related books (same tradition or category, excluding current)
  const currentTitle = (fileData.frontmatter?.title as string) ?? ""
  const relatedBooks = allFiles
    .filter((f) => {
      const s = f.slug ?? ""
      if (!s.startsWith("Books/") || s === "Books/index" || s.startsWith("Books/_")) return false
      if (f.frontmatter?.draft === true) return false
      if (f.frontmatter?.title === currentTitle) return false
      const fTradition = (f.frontmatter?.tradition as string) ?? ""
      const fCategory = (f.frontmatter?.category as string) ?? ""
      return (tradition && fTradition === tradition) || (category && fCategory === category)
    })
    .slice(0, 4)

  const hasMetadata = tradition || description || difficulty || teacherName

  if (!hasMetadata && relatedBooks.length === 0) return null

  return (
    <div class="book-meta">
      {(tradition || difficulty) && (
        <div class="book-meta__badges">
          {tradition && <span class="book-meta__badge book-meta__badge--tradition">{tradition}</span>}
          {difficulty && (
            <span class="book-meta__badge book-meta__badge--difficulty">
              {difficultyLabels[difficulty] || difficulty}
            </span>
          )}
        </div>
      )}

      {description && <p class="book-meta__description">{description}</p>}

      {teacherPage && (
        <div class="book-meta__teacher">
          <a
            href={resolveRelative(slug, teacherPage.slug!)}
            class="book-meta__teacher-link internal"
          >
            About {teacherName} →
          </a>
        </div>
      )}

      {relatedBooks.length > 0 && (
        <div class="book-meta__related">
          <span class="book-meta__related-label">Explore similar</span>
          <div class="book-meta__related-list">
            {relatedBooks.map((b) => (
              <a
                href={resolveRelative(slug, b.slug!)}
                class="book-meta__related-link internal"
              >
                {b.frontmatter?.title}
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

BookMeta.css = `
.book-meta {
  padding: 1rem 1.2rem;
  border-radius: 10px;
  background: color-mix(in srgb, var(--light) 92%, var(--lightgray));
  border: 1px solid color-mix(in srgb, var(--lightgray) 50%, transparent);
  margin-bottom: 1rem;
}

.book-meta__badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.6rem;
}

.book-meta__badge {
  display: inline-block;
  font-size: 0.75rem;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-weight: 500;
}

.book-meta__badge--tradition {
  background: color-mix(in srgb, var(--secondary) 12%, var(--light));
  color: var(--secondary);
}

.book-meta__badge--difficulty {
  background: color-mix(in srgb, var(--tertiary) 12%, var(--light));
  color: var(--darkgray);
}

.book-meta__description {
  font-size: 0.92rem;
  line-height: 1.6;
  color: var(--darkgray);
  margin: 0 0 0.6rem 0;
  font-style: italic;
}

.book-meta__teacher {
  margin-bottom: 0.5rem;
}

.book-meta__teacher-link {
  font-size: 0.85rem;
  color: var(--secondary);
  font-weight: 500;
}

.book-meta__related {
  padding-top: 0.6rem;
  border-top: 1px solid color-mix(in srgb, var(--lightgray) 60%, transparent);
}

.book-meta__related-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--gray);
  font-weight: 500;
}

.book-meta__related-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.4rem;
}

.book-meta__related-link {
  font-size: 0.8rem;
  padding: 0.2rem 0.6rem;
  border-radius: 8px;
  background: color-mix(in srgb, var(--light) 85%, var(--lightgray));
  color: var(--darkgray);
  text-decoration: none !important;
  transition: all 0.15s ease;
}

.book-meta__related-link:hover {
  background: color-mix(in srgb, var(--secondary) 12%, var(--light));
  color: var(--secondary);
}

@media (max-width: 800px) {
  .book-meta {
    padding: 0.8rem 1rem;
  }

  .book-meta__description {
    font-size: 0.88rem;
  }
}
`

export default (() => BookMeta) satisfies QuartzComponentConstructor
