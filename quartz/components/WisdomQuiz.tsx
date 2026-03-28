// @ts-ignore
import script from "./scripts/wisdomquiz.inline"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const WisdomQuiz: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <div class={`wisdom-quiz-wrapper ${displayClass ?? ""}`}>
      <button id="wisdom-quiz-start" class="wisdom-quiz__trigger">
        Discover Your Path
      </button>
      <div id="wisdom-quiz" class="wisdom-quiz" style="display:none;">
        <div class="wisdom-quiz__header">
          <span class="wisdom-quiz__title">Find Your Path</span>
          <button id="wisdom-quiz-close" class="wisdom-quiz__close">&times;</button>
        </div>
        <div class="wisdom-quiz__progress" id="wisdom-quiz-progress"></div>
        <div id="wisdom-quiz-question" class="wisdom-quiz__question"></div>
        <div id="wisdom-quiz-options" class="wisdom-quiz__options"></div>
        <div id="wisdom-quiz-results" class="wisdom-quiz__results" style="display:none;"></div>
      </div>
    </div>
  )
}

WisdomQuiz.afterDOMLoaded = script

WisdomQuiz.css = `
.wisdom-quiz-wrapper {
  margin-bottom: 1rem;
  text-align: center;
}

.wisdom-quiz__trigger {
  padding: 0.7rem 1.8rem;
  border: 2px solid var(--secondary);
  border-radius: 24px;
  background: transparent;
  color: var(--secondary);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--bodyFont);
  letter-spacing: 0.02em;
}

.wisdom-quiz__trigger:hover {
  background: var(--secondary);
  color: var(--light);
}

.wisdom-quiz {
  text-align: left;
  margin-top: 1rem;
  padding: 1.5rem;
  border-radius: 14px;
  background: color-mix(in srgb, var(--light) 95%, var(--lightgray));
  border: 1px solid color-mix(in srgb, var(--secondary) 20%, transparent);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.wisdom-quiz__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.wisdom-quiz__title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--dark);
}

.wisdom-quiz__close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--gray);
  cursor: pointer;
  padding: 0 0.3rem;
  line-height: 1;
}

.wisdom-quiz__close:hover {
  color: var(--dark);
}

.wisdom-quiz__progress {
  height: 4px;
  border-radius: 2px;
  background: var(--lightgray);
  margin-bottom: 1.2rem;
  overflow: hidden;
}

.wisdom-quiz__progress-bar {
  height: 100%;
  background: var(--secondary);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.wisdom-quiz__question {
  font-size: 1rem;
  font-weight: 600;
  color: var(--dark);
  margin-bottom: 1rem;
  line-height: 1.4;
}

.wisdom-quiz__options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.wisdom-quiz__option {
  padding: 0.8rem 1rem;
  border: 1px solid var(--lightgray);
  border-radius: 10px;
  background: var(--light);
  cursor: pointer;
  transition: all 0.15s ease;
  font-size: 0.9rem;
  color: var(--darkgray);
  text-align: left;
  font-family: var(--bodyFont);
}

.wisdom-quiz__option:hover {
  border-color: var(--secondary);
  background: color-mix(in srgb, var(--secondary) 6%, var(--light));
  color: var(--dark);
}

.wisdom-quiz__results {
  margin-top: 0.5rem;
}

.wisdom-quiz__results-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 0.8rem;
}

.wisdom-quiz__results-section {
  margin-bottom: 1rem;
}

.wisdom-quiz__results-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--gray);
  font-weight: 500;
  margin-bottom: 0.4rem;
}

.wisdom-quiz__result-card {
  display: block;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  background: color-mix(in srgb, var(--light) 88%, var(--lightgray));
  margin-bottom: 0.4rem;
  text-decoration: none !important;
  color: inherit;
  transition: all 0.15s ease;
}

.wisdom-quiz__result-card:hover {
  background: color-mix(in srgb, var(--secondary) 10%, var(--light));
}

.wisdom-quiz__result-name {
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--dark);
}

.wisdom-quiz__result-desc {
  font-size: 0.78rem;
  color: var(--gray);
  margin-top: 0.15rem;
}

.wisdom-quiz__restart {
  margin-top: 1rem;
  padding: 0.5rem 1.2rem;
  border: 1px solid var(--lightgray);
  border-radius: 20px;
  background: transparent;
  color: var(--darkgray);
  font-size: 0.82rem;
  cursor: pointer;
  font-family: var(--bodyFont);
  transition: all 0.15s ease;
}

.wisdom-quiz__restart:hover {
  border-color: var(--secondary);
  color: var(--secondary);
}

@media (max-width: 800px) {
  .wisdom-quiz {
    padding: 1.2rem;
  }

  .wisdom-quiz__option {
    padding: 0.7rem 0.9rem;
    font-size: 0.85rem;
  }
}
`

export default (() => WisdomQuiz) satisfies QuartzComponentConstructor
