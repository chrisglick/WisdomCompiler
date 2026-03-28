import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative } from "../util/path"

interface ExploreCard {
  emoji: string
  title: string
  description: string
  slug: string
}

const cards: ExploreCard[] = [
  {
    emoji: "\u{1F4D6}",
    title: "Books & Scriptures",
    description: "The texts I kept returning to, with the passages that stopped me",
    slug: "Books",
  },
  {
    emoji: "\u{1F9D8}",
    title: "Teachers",
    description: "The teachers who guided this search, from ancient sages to living masters",
    slug: "Teachers",
  },
  {
    emoji: "\u{2728}",
    title: "Wisdom Quotes",
    description: "Hundreds of passages photographed from books over seven years of seeking",
    slug: "Wisdom-Quotes",
  },
  {
    emoji: "\u{1F4A1}",
    title: "Concepts",
    description: "Explore by theme: surrender, ego, silence, liberation, love",
    slug: "tags",
  },
  {
    emoji: "\u{1F9F5}",
    title: "Wisdom Threads",
    description: "Cross-tradition explorations of the same eternal truths",
    slug: "Threads",
  },
]

interface StarterRec {
  title: string
  subtitle: string
  slug: string
}

const starters: StarterRec[] = [
  { title: "Bhagavad Gita", subtitle: "The universal scripture", slug: "Books/Bhagavad-Gita" },
  { title: "Talks with Ramana Maharshi", subtitle: "Self-inquiry from the source", slug: "Books/Talks-with-Ramana-Maharshi" },
  { title: "The Power of Now", subtitle: "Modern awakening classic", slug: "Books/The-Power-of-Now" },
  { title: "The Prophet", subtitle: "Timeless spiritual poetry", slug: "Books/The-Prophet" },
  { title: "Dropping Ashes On the Buddha", subtitle: "Zen for beginners", slug: "Books/Dropping-Ashes-On-the-Buddha" },
]

const HomepageExplore: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
  const currentSlug = fileData.slug ?? ""

  // Compute live stats
  const bookCount = allFiles.filter(
    (f) => f.slug?.startsWith("Books/") && f.slug !== "Books/index" && !f.slug.startsWith("Books/_") && f.frontmatter?.draft !== true,
  ).length

  const teacherCount = allFiles.filter(
    (f) => f.slug?.startsWith("Teachers/") && !f.slug.includes("images/") && !f.slug.includes("_teacher") && f.frontmatter?.draft !== true,
  ).length

  const quoteCount = allFiles.filter(
    (f) => f.slug?.startsWith("Wisdom-Quotes/") && f.slug !== "Wisdom-Quotes/index" && !f.slug.startsWith("Wisdom-Quotes/_") && f.frontmatter?.draft !== true,
  ).length

  const traditions = new Set(
    allFiles
      .filter((f) => f.slug?.startsWith("Books/") && f.frontmatter?.tradition)
      .map((f) => f.frontmatter?.tradition as string)
      .filter((t) => t && t !== "Fiction"),
  )

  return (
    <div class="homepage-explore">
      <div class="homepage-explore__stats">
        <span class="homepage-explore__stat">{bookCount}+ Books</span>
        <span class="homepage-explore__stat-divider">&middot;</span>
        <span class="homepage-explore__stat">{teacherCount}+ Teachers</span>
        <span class="homepage-explore__stat-divider">&middot;</span>
        <span class="homepage-explore__stat">{quoteCount}+ Passages</span>
        <span class="homepage-explore__stat-divider">&middot;</span>
        <span class="homepage-explore__stat">{traditions.size}+ Traditions</span>
      </div>

      <div class="homepage-explore__cards">
        {cards.map((card) => (
          <a
            href={resolveRelative(currentSlug, card.slug)}
            class="homepage-explore__card internal"
            data-no-popover
          >
            <span class="homepage-explore__card-emoji">{card.emoji}</span>
            <span class="homepage-explore__card-title">{card.title}</span>
            <span class="homepage-explore__card-desc">{card.description}</span>
          </a>
        ))}
      </div>

      <div class="homepage-explore__starters">
        <h3 class="homepage-explore__starters-title">Where to Start</h3>
        <div class="homepage-explore__starters-list">
          {starters.map((rec) => (
            <a
              href={resolveRelative(currentSlug, rec.slug)}
              class="homepage-explore__starter internal"
              data-no-popover
            >
              <span class="homepage-explore__starter-title">{rec.title}</span>
              <span class="homepage-explore__starter-sub">{rec.subtitle}</span>
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}

HomepageExplore.css = `
.homepage-explore {
  margin-bottom: 1.5rem;
}

.homepage-explore__stats {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.88rem;
  color: var(--gray);
}

.homepage-explore__stat {
  font-weight: 500;
  color: var(--darkgray);
}

.homepage-explore__stat-divider {
  color: var(--lightgray);
}

.homepage-explore__cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.8rem;
  margin-bottom: 1.8rem;
}

.homepage-explore__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.2rem 0.8rem;
  border-radius: 12px;
  background: color-mix(in srgb, var(--light) 90%, var(--lightgray));
  border: 1px solid color-mix(in srgb, var(--lightgray) 50%, transparent);
  transition: all 0.2s ease;
  text-decoration: none !important;
  color: inherit;
}

.homepage-explore__card:hover {
  background: color-mix(in srgb, var(--light) 78%, var(--lightgray));
  border-color: color-mix(in srgb, var(--secondary) 25%, transparent);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.homepage-explore__card-emoji {
  font-size: 1.8rem;
  margin-bottom: 0.4rem;
}

.homepage-explore__card-title {
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--dark);
  margin-bottom: 0.2rem;
}

.homepage-explore__card-desc {
  font-size: 0.76rem;
  color: var(--gray);
  line-height: 1.4;
}

.homepage-explore__starters {
  padding: 1.2rem;
  border-radius: 12px;
  background: linear-gradient(135deg,
    color-mix(in srgb, var(--secondary) 8%, var(--light)),
    color-mix(in srgb, var(--secondary) 3%, var(--light))
  );
  border: 1px solid color-mix(in srgb, var(--secondary) 12%, transparent);
}

.homepage-explore__starters-title {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--secondary);
  margin: 0 0 0.8rem 0;
  font-weight: 600;
}

.homepage-explore__starters-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.homepage-explore__starter {
  display: flex;
  flex-direction: column;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  background: color-mix(in srgb, var(--light) 80%, transparent);
  text-decoration: none !important;
  color: inherit;
  transition: all 0.15s ease;
  flex: 1;
  min-width: 140px;
}

.homepage-explore__starter:hover {
  background: var(--light);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.homepage-explore__starter-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--dark);
}

.homepage-explore__starter-sub {
  font-size: 0.74rem;
  color: var(--gray);
}

@media (max-width: 800px) {
  .homepage-explore__cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.6rem;
  }

  .homepage-explore__card {
    padding: 0.9rem 0.6rem;
  }

  .homepage-explore__card-emoji {
    font-size: 1.4rem;
  }

  .homepage-explore__card-desc {
    display: none;
  }

  .homepage-explore__starters-list {
    flex-direction: column;
  }

  .homepage-explore__starter {
    min-width: auto;
  }

  .homepage-explore__stats {
    font-size: 0.8rem;
    gap: 0.3rem;
  }
}
`

export default (() => HomepageExplore) satisfies QuartzComponentConstructor
