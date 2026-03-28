import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative } from "../util/path"

interface BookData {
  title: string
  author: string
  category: string
  tradition: string
  description: string
  difficulty: string
  slug: string
}

const categoryOrder = [
  "scripture",
  "teaching",
  "commentary",
  "mysticism",
  "poetry",
  "fiction",
  "manga",
]

const categoryLabels: Record<string, string> = {
  scripture: "Sacred Scriptures",
  teaching: "Teachings & Discourses",
  commentary: "Commentaries",
  mysticism: "Mystical Texts",
  poetry: "Spiritual Poetry",
  fiction: "Fiction & Philosophy",
  manga: "Manga & Visual Stories",
}

const difficultyEmoji: Record<string, string> = {
  approachable: "\u{1F331}",
  intermediate: "\u{1F333}",
  advanced: "\u{1F3D4}\u{FE0F}",
}

const BookGrid: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
  const books: BookData[] = allFiles
    .filter((f) => {
      const slug = f.slug ?? ""
      return (
        slug.startsWith("Books/") &&
        slug !== "Books/index" &&
        !slug.startsWith("Books/_") &&
        f.frontmatter?.draft !== true
      )
    })
    .map((f) => ({
      title: (f.frontmatter?.title as string) ?? "",
      author: (f.frontmatter?.Author as string) ?? "",
      category: (f.frontmatter?.category as string) ?? "teaching",
      tradition: (f.frontmatter?.tradition as string) ?? "",
      description: (f.frontmatter?.description as string) ?? "",
      difficulty: (f.frontmatter?.difficulty as string) ?? "intermediate",
      slug: f.slug ?? "",
    }))

  // Group by category
  const grouped: Record<string, BookData[]> = {}
  for (const book of books) {
    const cat = book.category || "teaching"
    if (!grouped[cat]) grouped[cat] = []
    grouped[cat].push(book)
  }

  // Sort within each group alphabetically
  for (const cat in grouped) {
    grouped[cat].sort((a, b) => a.title.localeCompare(b.title))
  }

  const currentSlug = fileData.slug ?? ""

  return (
    <div class="book-grid">
      <div class="book-grid__filters" id="book-grid-filters">
        <button class="book-grid__filter-btn book-grid__filter-btn--active" data-filter="all">
          All
        </button>
        {categoryOrder
          .filter((cat) => grouped[cat]?.length)
          .map((cat) => (
            <button class="book-grid__filter-btn" data-filter={cat}>
              {categoryLabels[cat] || cat}
            </button>
          ))}
      </div>

      {categoryOrder
        .filter((cat) => grouped[cat]?.length)
        .map((cat) => (
          <div class="book-grid__section" data-category={cat}>
            <h2 class="book-grid__section-title">{categoryLabels[cat] || cat}</h2>
            <div class="book-grid__cards">
              {grouped[cat].map((book) => (
                <a
                  href={resolveRelative(currentSlug, book.slug)}
                  class="book-grid__card internal"
                  data-category={book.category}
                  data-tradition={book.tradition}
                  data-no-popover
                >
                  <div class="book-grid__card-header">
                    <span class="book-grid__card-title">{book.title}</span>
                    <span class="book-grid__card-difficulty" title={book.difficulty}>
                      {difficultyEmoji[book.difficulty] || ""}
                    </span>
                  </div>
                  <div class="book-grid__card-author">{book.author}</div>
                  {book.tradition && (
                    <span class="book-grid__card-tradition">{book.tradition}</span>
                  )}
                  {book.description && (
                    <p class="book-grid__card-desc">{book.description}</p>
                  )}
                </a>
              ))}
            </div>
          </div>
        ))}
    </div>
  )
}

// @ts-ignore
import filterScript from "./scripts/bookgrid.inline"
BookGrid.afterDOMLoaded = filterScript

BookGrid.css = `
.book-grid__filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--lightgray);
}

.book-grid__filter-btn {
  padding: 0.4rem 0.9rem;
  border: 1px solid var(--lightgray);
  border-radius: 20px;
  background: transparent;
  color: var(--darkgray);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--bodyFont);
}

.book-grid__filter-btn:hover {
  border-color: var(--secondary);
  color: var(--secondary);
}

.book-grid__filter-btn--active {
  background: var(--secondary);
  color: var(--light);
  border-color: var(--secondary);
}

.book-grid__section {
  margin-bottom: 2rem;
}

.book-grid__section-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--secondary);
  margin: 0 0 1rem 0;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid color-mix(in srgb, var(--secondary) 20%, transparent);
}

.book-grid__cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.book-grid__card {
  display: block;
  padding: 1rem 1.2rem;
  border-radius: 10px;
  background: color-mix(in srgb, var(--light) 90%, var(--lightgray));
  border: 1px solid color-mix(in srgb, var(--lightgray) 60%, transparent);
  transition: all 0.2s ease;
  text-decoration: none !important;
  color: inherit;
}

.book-grid__card:hover {
  background: color-mix(in srgb, var(--light) 78%, var(--lightgray));
  border-color: color-mix(in srgb, var(--secondary) 30%, transparent);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.book-grid__card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
}

.book-grid__card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--dark);
  line-height: 1.3;
}

.book-grid__card-difficulty {
  font-size: 0.9rem;
  flex-shrink: 0;
}

.book-grid__card-author {
  font-size: 0.85rem;
  color: var(--gray);
  margin-top: 0.25rem;
}

.book-grid__card-tradition {
  display: inline-block;
  font-size: 0.72rem;
  padding: 0.15rem 0.55rem;
  border-radius: 10px;
  background: color-mix(in srgb, var(--secondary) 12%, var(--light));
  color: var(--secondary);
  margin-top: 0.4rem;
  font-weight: 500;
}

.book-grid__card-desc {
  font-size: 0.82rem;
  color: var(--darkgray);
  line-height: 1.5;
  margin: 0.5rem 0 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-grid__section--hidden {
  display: none;
}

@media (max-width: 800px) {
  .book-grid__cards {
    grid-template-columns: 1fr;
  }

  .book-grid__filters {
    gap: 0.4rem;
  }

  .book-grid__filter-btn {
    font-size: 0.75rem;
    padding: 0.35rem 0.7rem;
  }

  .book-grid__card {
    padding: 0.9rem 1rem;
  }
}
`

export default (() => BookGrid) satisfies QuartzComponentConstructor
