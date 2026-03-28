import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
import { concatenateResources } from "../../util/resources"
import BookGrid from "../BookGrid"
import TeacherGrid from "../TeacherGrid"

// Import original FolderContent for fallback
import OriginalFolderContent from "./FolderContent"

const OriginalFC = OriginalFolderContent()

export default (() => {
  const SmartFolderContent: QuartzComponent = (props: QuartzComponentProps) => {
    const slug = props.fileData.slug ?? ""

    if (slug === "Books/index" || slug === "Books") {
      return (
        <div class="popover-hint">
          <article>{/* index.md content is rendered by the tree */}</article>
          <BookGridComponent {...props} />
        </div>
      )
    }

    if (slug === "Teachers/index" || slug === "Teachers") {
      return (
        <div class="popover-hint">
          <article></article>
          <TeacherGridComponent {...props} />
        </div>
      )
    }

    // Default: use original FolderContent
    return OriginalFC(props)
  }

  const BookGridComponent = BookGrid()
  const TeacherGridComponent = TeacherGrid()

  SmartFolderContent.css = concatenateResources(
    OriginalFC.css,
    BookGridComponent.css,
    TeacherGridComponent.css,
  )
  SmartFolderContent.afterDOMLoaded = concatenateResources(
    OriginalFC.afterDOMLoaded,
    BookGridComponent.afterDOMLoaded,
    TeacherGridComponent.afterDOMLoaded,
  )

  return SmartFolderContent
}) satisfies QuartzComponentConstructor
