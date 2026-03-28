import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative } from "../util/path"

interface TeacherData {
  title: string
  tradition: string
  period: string
  coreTeaching: string
  image: string | null
  slug: string
}

const TeacherGrid: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
  const teachers: TeacherData[] = allFiles
    .filter((f) => {
      const slug = f.slug ?? ""
      return (
        slug.startsWith("Teachers/") &&
        slug !== "Teachers/index" &&
        !slug.includes("images/") &&
        !slug.includes("_teacher") &&
        f.frontmatter?.draft !== true
      )
    })
    .map((f) => ({
      title: (f.frontmatter?.title as string) ?? "",
      tradition: (f.frontmatter?.tradition as string) ?? "",
      period: (f.frontmatter?.period as string) ?? "",
      coreTeaching: (f.frontmatter?.core_teaching as string) ?? "",
      image: (f.frontmatter?.image as string) ?? null,
      slug: f.slug ?? "",
    }))
    .sort((a, b) => a.title.localeCompare(b.title))

  const currentSlug = fileData.slug ?? ""

  return (
    <div class="teacher-grid">
      <div class="teacher-grid__cards">
        {teachers.map((teacher) => {
          const imageSrc = teacher.image ? `/Teachers/images/${teacher.image}` : null

          return (
            <a
              href={resolveRelative(currentSlug, teacher.slug)}
              class={`teacher-grid__card internal ${imageSrc ? "" : "teacher-grid__card--no-image"}`}
              data-no-popover
            >
              {imageSrc ? (
                <div class="teacher-grid__card-hero">
                  <img
                    class="teacher-grid__card-image"
                    src={imageSrc}
                    alt={teacher.title}
                    loading="lazy"
                  />
                </div>
              ) : (
                <div class="teacher-grid__card-hero teacher-grid__card-hero--placeholder">
                  <span class="teacher-grid__card-initial">{teacher.title.charAt(0)}</span>
                </div>
              )}
              <div class="teacher-grid__card-info">
                <span class="teacher-grid__card-name">{teacher.title}</span>
                {teacher.tradition && (
                  <span class="teacher-grid__card-tradition">{teacher.tradition}</span>
                )}
                {teacher.period && (
                  <span class="teacher-grid__card-period">{teacher.period}</span>
                )}
                {teacher.coreTeaching && (
                  <p class="teacher-grid__card-teaching">{teacher.coreTeaching}</p>
                )}
              </div>
            </a>
          )
        })}
      </div>
    </div>
  )
}

TeacherGrid.css = `
.teacher-grid__cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.2rem;
}

.teacher-grid__card {
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  background: color-mix(in srgb, var(--light) 90%, var(--lightgray));
  border: 1px solid color-mix(in srgb, var(--lightgray) 60%, transparent);
  transition: all 0.2s ease;
  text-decoration: none !important;
  color: inherit;
  overflow: hidden;
}

.teacher-grid__card:hover {
  border-color: color-mix(in srgb, var(--secondary) 30%, transparent);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.teacher-grid__card-hero {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: color-mix(in srgb, var(--lightgray) 40%, var(--light));
}

.teacher-grid__card-hero--placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg,
    color-mix(in srgb, var(--secondary) 10%, var(--light)),
    color-mix(in srgb, var(--tertiary) 10%, var(--light))
  );
}

.teacher-grid__card-initial {
  font-size: 3rem;
  font-weight: 700;
  color: color-mix(in srgb, var(--secondary) 40%, var(--light));
}

.teacher-grid__card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
  image-rendering: auto;
}

.teacher-grid__card-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.2rem;
  padding: 0.9rem 1rem;
}

.teacher-grid__card-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--dark);
}

.teacher-grid__card-tradition {
  display: inline-block;
  font-size: 0.72rem;
  padding: 0.15rem 0.55rem;
  border-radius: 10px;
  background: color-mix(in srgb, var(--secondary) 12%, var(--light));
  color: var(--secondary);
  font-weight: 500;
}

.teacher-grid__card-period {
  font-size: 0.78rem;
  color: var(--gray);
}

.teacher-grid__card-teaching {
  font-size: 0.8rem;
  color: var(--darkgray);
  line-height: 1.45;
  margin: 0.3rem 0 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (max-width: 800px) {
  .teacher-grid__cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.8rem;
  }

  .teacher-grid__card-hero {
    height: 120px;
  }

  .teacher-grid__card-initial {
    font-size: 2.2rem;
  }

  .teacher-grid__card-info {
    padding: 0.6rem 0.8rem;
  }

  .teacher-grid__card-name {
    font-size: 0.9rem;
  }

  .teacher-grid__card-teaching {
    display: none;
  }
}

@media (max-width: 420px) {
  .teacher-grid__cards {
    grid-template-columns: 1fr;
  }

  .teacher-grid__card-hero {
    height: 200px;
  }

  .teacher-grid__card-teaching {
    display: -webkit-box;
  }
}
`

export default (() => TeacherGrid) satisfies QuartzComponentConstructor
