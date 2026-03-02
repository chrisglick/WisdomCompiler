// @ts-ignore
import script from "./scripts/randomquote.inline"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const RandomQuote: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <div class={`random-quote ${displayClass ?? ""}`} id="random-quote">
      <a id="random-quote-link" class="internal" href="/" data-no-popover>
        <blockquote id="random-quote-text"></blockquote>
        <cite id="random-quote-source"></cite>
      </a>
    </div>
  )
}

RandomQuote.afterDOMLoaded = script
RandomQuote.css = `
.random-quote {
  text-align: center;
  padding: 1.2rem 1.5rem;
  margin: 0 0 1.5rem 0;
  border-left: none;
  border-radius: 8px;
  background: color-mix(in srgb, var(--light) 90%, var(--lightgray));
  transition: background 0.2s ease;
}

.random-quote:hover {
  background: color-mix(in srgb, var(--light) 80%, var(--lightgray));
}

.random-quote a {
  text-decoration: none;
  font-weight: normal;
  background: none;
  padding: 0;
}

.random-quote a:hover {
  color: inherit;
}

.random-quote blockquote {
  border: none;
  padding: 0;
  margin: 0 0 0.4rem 0;
  font-size: 1.05rem;
  line-height: 1.7;
  font-style: italic;
  color: var(--darkgray);
  font-family: var(--bodyFont);
}

.random-quote cite {
  display: block;
  font-size: 0.8rem;
  color: var(--gray);
  font-style: normal;
  letter-spacing: 0.02em;
}

@media (max-width: 800px) {
  .random-quote {
    padding: 1rem;
    margin: 0 0 1rem 0;
  }
  .random-quote blockquote {
    font-size: 0.95rem;
  }
}
`

export default (() => RandomQuote) satisfies QuartzComponentConstructor
