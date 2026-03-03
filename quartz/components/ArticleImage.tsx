import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const ArticleImage: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const showImage = fileData.frontmatter?.ShowImage
  const imageName = fileData.frontmatter?.image_name as string | undefined

  if (!showImage || !imageName) {
    return null
  }

  // Derive the image URL from the note's slug
  // Note at Wisdom-Quotes/The-Yukon-Song → image at /Wisdom-Quotes/Images/IMG_1202.PNG
  const slug = fileData.slug ?? ""
  const slugDir = slug.includes("/") ? slug.substring(0, slug.lastIndexOf("/")) : ""
  const imageSrc = `/${slugDir}/Images/${imageName}`

  return (
    <div class={classNames(displayClass, "article-image")}>
      <img src={imageSrc} alt={fileData.frontmatter?.title ?? "Article image"} loading="lazy" />
    </div>
  )
}

ArticleImage.css = `
.article-image {
  margin: 1rem 0;
}
.article-image img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}
`

export default (() => ArticleImage) satisfies QuartzComponentConstructor
