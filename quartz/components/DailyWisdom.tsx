// @ts-ignore
import script from "./scripts/dailywisdom.inline"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const DailyWisdom: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <div class={`daily-wisdom ${displayClass ?? ""}`} id="daily-wisdom">
      <div class="daily-wisdom-label" id="daily-wisdom-label"></div>
      <a id="daily-wisdom-link" class="internal" href="/" data-no-popover>
        <blockquote id="daily-wisdom-text"></blockquote>
        <cite id="daily-wisdom-source"></cite>
      </a>
    </div>
  )
}

DailyWisdom.afterDOMLoaded = script
DailyWisdom.css = `
.daily-wisdom {
  text-align: center;
  padding: 1.4rem 1.8rem;
  margin: 0 0 1.5rem 0;
  border-left: none;
  border-radius: 8px;
  background: color-mix(in srgb, var(--light) 90%, var(--lightgray));
  transition: background 0.2s ease;
}

.daily-wisdom:hover {
  background: color-mix(in srgb, var(--light) 80%, var(--lightgray));
}

.daily-wisdom-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--gray);
  margin-bottom: 0.6rem;
  font-weight: 500;
}

.daily-wisdom a {
  text-decoration: none;
  font-weight: normal;
  background: none;
  padding: 0;
}

.daily-wisdom a:hover {
  color: inherit;
}

.daily-wisdom blockquote {
  border: none;
  padding: 0;
  margin: 0 0 0.5rem 0;
  font-size: 1.05rem;
  line-height: 1.7;
  font-style: italic;
  color: var(--darkgray);
  font-family: var(--bodyFont);
}

.daily-wisdom cite {
  display: block;
  font-size: 0.8rem;
  color: var(--gray);
  font-style: normal;
  letter-spacing: 0.02em;
}

@media (max-width: 800px) {
  .daily-wisdom {
    padding: 1rem;
    margin: 0 0 1rem 0;
  }
  .daily-wisdom blockquote {
    font-size: 0.95rem;
  }
}
`

export default (() => DailyWisdom) satisfies QuartzComponentConstructor
