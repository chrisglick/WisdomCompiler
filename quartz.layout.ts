import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  // RelatedQuotes self-gates to quote pages (returns null elsewhere): shows
  // "Kindred passages" ranked by same source, then shared topics.
  // ThemeIndex renders the "Browse by theme" listing under content/Themes.md only.
  afterBody: [
    Component.ConditionalRender({
      component: Component.ThemeIndex(),
      condition: (page) => page.fileData.slug === "Themes",
    }),
    Component.RelatedQuotes(),
  ],
  footer: Component.Footer({
    links: {
      "GitHub": "https://github.com/chrisglick/WisdomCompiler",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.DailyWisdom(),
      condition: (page) => page.fileData.slug === "index",
    }),
    Component.ConditionalRender({
      component: Component.HomepageExplore(),
      condition: (page) => page.fileData.slug === "index",
    }),
    Component.ConditionalRender({
      component: Component.WisdomQuiz(),
      condition: (page) => page.fileData.slug === "index",
    }),
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.SourceBanner(),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.ArticleImage(),
    Component.ConditionalRender({
      component: Component.BookMeta(),
      condition: (page) => {
        const slug = page.fileData.slug ?? ""
        return slug.startsWith("Books/") && slug !== "Books/index" && !slug.startsWith("Books/_")
      },
    }),
    Component.TagList(),
  ],
  // Contemplative reading: no file-tree Explorer or Backlinks panel on content
  // pages — just a minimal search/dark-mode toolbar. Breadcrumbs (in beforeBody)
  // carry navigation. Folder index pages keep the Explorer (see list layout).
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
  ],
  right: [Component.DesktopOnly(Component.TableOfContents())],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer({
      filterFn: (node) => {
        const name = node.name?.toLowerCase()
        if (!name) return true
        const excluded = [
          "tags",
          "images",
          "social-media",
          "lakshmi the cow",
          "about",
        ]
        return !excluded.includes(name)
      },
    }),
  ],
  right: [],
}
