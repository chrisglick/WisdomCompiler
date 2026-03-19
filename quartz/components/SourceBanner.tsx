import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative } from "../util/path"

const SourceBanner: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
  const slug = fileData.slug ?? ""

  // Determine page type
  const isQuotePage =
    slug.startsWith("Wisdom-Quotes/") &&
    slug !== "Wisdom-Quotes/index" &&
    !slug.includes("Images/")
  const isTeacherPage =
    slug.startsWith("Teachers/") &&
    slug !== "Teachers/index" &&
    !slug.includes("images/") &&
    !slug.includes("_teacher")
  const isBookPage =
    slug.startsWith("Books/") &&
    slug !== "Books/index" &&
    !slug.startsWith("Books/_")

  if (!isQuotePage && !isTeacherPage && !isBookPage) return null

  let sourceName: string | null = null
  let sourceSlug: string | null = null
  let sourceImage: string | null = null
  let isHero = false

  if (isQuotePage) {
    // Resolve source from frontmatter
    const rawSource = (fileData.frontmatter?.source as string) ?? ""
    if (!rawSource) return null
    sourceName = rawSource.replace(/\[\[/g, "").replace(/\]\]/g, "").trim()
    if (!sourceName) return null

    // Find matching page in allFiles (check Teachers and Books)
    const sourcePage = allFiles.find((f) => {
      const title = f.frontmatter?.title
      if (!title) return false
      return (
        title === sourceName &&
        (f.slug?.startsWith("Teachers/") || f.slug?.startsWith("Books/"))
      )
    })

    if (sourcePage) {
      sourceSlug = sourcePage.slug ?? null
      sourceImage = (sourcePage.frontmatter?.image as string) ?? null
    }
  } else {
    // Teacher or book page — hero mode (show own image)
    isHero = true
    sourceName = (fileData.frontmatter?.title as string) ?? null
    sourceImage = (fileData.frontmatter?.image as string) ?? null
  }

  if (!sourceName) return null

  // Resolve image path
  const imageFolder = sourceSlug?.startsWith("Books/") || isBookPage ? "Books/images" : "Teachers/images"
  const imageSrc = sourceImage ? `/${imageFolder}/${sourceImage}` : null

  // Resolve link href (only for quote banners linking to source)
  const href = sourceSlug ? resolveRelative(slug, sourceSlug) : undefined

  const variantClass = isHero ? "source-banner--hero" : "source-banner--quote"
  const imageClass = imageSrc ? "" : "source-banner--no-image"

  const inner = (
    <div class={`source-banner ${variantClass} ${imageClass}`}>
      {imageSrc && (
        <img
          class="source-banner__image"
          src={imageSrc}
          alt={sourceName}
          loading="lazy"
        />
      )}
      <span class="source-banner__name">{sourceName}</span>
    </div>
  )

  // Wrap in link for quote pages
  if (href) {
    return (
      <a href={href} class="source-banner__link internal" data-no-popover>
        {inner}
      </a>
    )
  }

  return inner
}

SourceBanner.css = `
/* ── Source Banner: shared base ── */
.source-banner {
  display: flex;
  align-items: center;
}

.source-banner__image {
  object-fit: cover;
  flex-shrink: 0;
}

.source-banner__link {
  text-decoration: none !important;
  background: none !important;
  font-weight: normal;
}

.source-banner__link:hover {
  color: inherit;
}

/* ── Quote variant (compact, clickable) ── */
.source-banner--quote {
  gap: 0.75rem;
  padding: 0.6rem 1rem;
  border-radius: 12px;
  background: color-mix(in srgb, var(--light) 90%, var(--lightgray));
  transition: background 0.2s ease, transform 0.15s ease;
  margin: 0 0 0.5rem 0;
}

.source-banner__link:hover .source-banner--quote {
  background: color-mix(in srgb, var(--light) 78%, var(--lightgray));
}

.source-banner--quote .source-banner__image {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.source-banner__link:hover .source-banner--quote .source-banner__image {
  transform: scale(1.05);
}

.source-banner--quote .source-banner__name {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--secondary);
  letter-spacing: 0.01em;
}

/* ── Hero variant (teacher/book page — badge style) ── */
.source-banner--hero {
  flex-direction: row;
  align-items: center;
  gap: 1.2rem;
  padding: 1rem 1.4rem;
  border-radius: 14px;
  background: linear-gradient(135deg,
    color-mix(in srgb, var(--secondary) 12%, var(--light)),
    color-mix(in srgb, var(--secondary) 4%, var(--light))
  );
  border: 1px solid color-mix(in srgb, var(--secondary) 18%, transparent);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  margin: 0 0 0.8rem 0;
}

.source-banner--hero .source-banner__image {
  width: 90px;
  height: 90px;
  object-fit: cover;
  object-position: top;
  border-radius: 50%;
  border: 3px solid color-mix(in srgb, var(--secondary) 30%, var(--light));
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

.source-banner--hero .source-banner__name {
  display: block;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--dark);
  letter-spacing: -0.01em;
  line-height: 1.3;
}

/* ── Fallback (no image) ── */
.source-banner--no-image {
  border-left: 4px solid var(--secondary);
  padding-left: 1rem;
}

.source-banner--no-image.source-banner--quote {
  padding: 0.5rem 1rem 0.5rem 1rem;
}

.source-banner--no-image .source-banner__name {
  font-size: 0.95rem;
}

.source-banner--no-image.source-banner--hero {
  align-items: flex-start;
  margin: 0.5rem 0;
}

.source-banner--no-image.source-banner--hero .source-banner__name {
  display: block;
  font-size: 0.85rem;
  color: var(--gray);
  font-style: italic;
}

/* ── Mobile ── */
@media (max-width: 800px) {
  .source-banner--quote .source-banner__image {
    width: 36px;
    height: 36px;
  }

  .source-banner--hero {
    gap: 1rem;
    padding: 0.8rem 1rem;
  }

  .source-banner--hero .source-banner__image {
    width: 70px;
    height: 70px;
  }

  .source-banner--hero .source-banner__name {
    font-size: 1.1rem;
  }

  .source-banner--quote {
    padding: 0.5rem 0.8rem;
    gap: 0.6rem;
  }

  .source-banner--quote .source-banner__name {
    font-size: 0.85rem;
  }
}
`

export default (() => SourceBanner) satisfies QuartzComponentConstructor
