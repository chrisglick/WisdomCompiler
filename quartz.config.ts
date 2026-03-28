import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "WisdomCompiler",
    pageTitleSuffix: " | WisdomCompiler",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "en-US",
    baseUrl: "wisdomcompiler.com",
    ignorePatterns: ["private", "templates", ".obsidian", "Book Source PDFs"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Schibsted Grotesk",
        body: "Source Sans Pro",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#faf8f0",
          lightgray: "#e8e0d4",
          gray: "#b8a89a",
          darkgray: "#4a3f35",
          dark: "#2b2520",
          secondary: "#8b5e3c",
          tertiary: "#c49a6c",
          highlight: "rgba(196, 154, 108, 0.12)",
          textHighlight: "#c49a6c44",
        },
        darkMode: {
          light: "#1a1510",
          lightgray: "#3a3228",
          gray: "#6b5d4f",
          darkgray: "#d4ccc0",
          dark: "#ede8e0",
          secondary: "#c49a6c",
          tertiary: "#8b5e3c",
          highlight: "rgba(196, 154, 108, 0.12)",
          textHighlight: "#c49a6c44",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
