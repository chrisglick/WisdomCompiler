interface QuizQuestion {
  text: string
  options: { label: string; tags: Record<string, number> }[]
}

interface BookRec {
  title: string
  slug: string
  tradition: string
  category: string
  difficulty: string
  description: string
}

const questions: QuizQuestion[] = [
  {
    text: "What draws you to spiritual inquiry?",
    options: [
      {
        label: "A longing for peace and freedom from suffering",
        tags: { "Advaita Vedanta": 3, teaching: 2, approachable: 1, liberation: 2 },
      },
      {
        label: "Intellectual curiosity about the nature of reality",
        tags: { "Advaita Vedanta": 2, scripture: 2, advanced: 1, "Multiple": 1 },
      },
      {
        label: "Love, devotion, and connection to the divine",
        tags: { Hindu: 2, Sikh: 2, poetry: 2, approachable: 1 },
      },
      {
        label: "Stillness, meditation, and inner silence",
        tags: { Zen: 3, Buddhist: 2, teaching: 1, intermediate: 1 },
      },
    ],
  },
  {
    text: "Which approach resonates with you?",
    options: [
      {
        label: "Direct self-inquiry — 'Who am I?'",
        tags: { "Advaita Vedanta": 3, teaching: 1, commentary: 1 },
      },
      {
        label: "Devotion and surrender to the divine",
        tags: { Hindu: 2, Islamic: 2, Sikh: 1, scripture: 1 },
      },
      {
        label: "Meditation, mindfulness, and presence",
        tags: { Zen: 2, Contemporary: 2, Buddhist: 1, teaching: 1 },
      },
      {
        label: "Study of scripture and sacred texts",
        tags: { scripture: 3, advanced: 1, Hindu: 1, Islamic: 1 },
      },
    ],
  },
  {
    text: "Which tradition calls to you?",
    options: [
      {
        label: "Hindu / Advaita Vedanta",
        tags: { "Advaita Vedanta": 4, Hindu: 3 },
      },
      {
        label: "Buddhist / Zen",
        tags: { Zen: 3, Buddhist: 3 },
      },
      {
        label: "Islamic / Sufi",
        tags: { Islamic: 3, Sufi: 3 },
      },
      {
        label: "Contemporary / No preference",
        tags: { Contemporary: 3, "Multiple": 2, Fiction: 1 },
      },
    ],
  },
  {
    text: "What is your experience with spiritual reading?",
    options: [
      {
        label: "I'm new — I want something accessible and clear",
        tags: { approachable: 4, teaching: 2, Contemporary: 1 },
      },
      {
        label: "I've read some — ready for deeper exploration",
        tags: { intermediate: 4, commentary: 1 },
      },
      {
        label: "I'm a serious student — bring the original texts",
        tags: { advanced: 4, scripture: 2 },
      },
    ],
  },
]

// Hardcoded book recommendations with slugs
const bookDatabase: BookRec[] = [
  { title: "Bhagavad Gita", slug: "Books/Bhagavad-Gita", tradition: "Hindu", category: "scripture", difficulty: "approachable", description: "The universal scripture of dharma and self-knowledge" },
  { title: "The Power of Now", slug: "Books/The-Power-of-Now", tradition: "Contemporary", category: "teaching", difficulty: "approachable", description: "Modern classic on presence and awakening" },
  { title: "Talks with Ramana Maharshi", slug: "Books/Talks-with-Ramana-Maharshi", tradition: "Advaita Vedanta", category: "teaching", difficulty: "intermediate", description: "600+ conversations on self-inquiry and silence" },
  { title: "The Prophet", slug: "Books/The-Prophet", tradition: "Multiple", category: "poetry", difficulty: "approachable", description: "Timeless prose poetry on love, death, and spirit" },
  { title: "Dropping Ashes On the Buddha", slug: "Books/Dropping-Ashes-On-the-Buddha", tradition: "Zen", category: "teaching", difficulty: "approachable", description: "Unconventional Zen encounters" },
  { title: "The Zen Teaching of Huang Po", slug: "Books/The-Zen-Teaching-of-Huang-Po", tradition: "Zen", category: "teaching", difficulty: "intermediate", description: "Direct pointings to the One Mind" },
  { title: "Consciousness and the Absolute", slug: "Books/Consciousness-and-the-Absolute", tradition: "Advaita Vedanta", category: "teaching", difficulty: "advanced", description: "Nisargadatta's final teachings beyond 'I Am'" },
  { title: "Yoga Vasistha", slug: "Books/Yoga-Vasistha", tradition: "Advaita Vedanta", category: "scripture", difficulty: "advanced", description: "Epic dialogue on consciousness and liberation" },
  { title: "Vivekachudamani", slug: "Books/Vivekachudamani", tradition: "Advaita Vedanta", category: "scripture", difficulty: "advanced", description: "Shankaracharya's Crest-Jewel of Discrimination" },
  { title: "A New Earth", slug: "Books/A-New-Earth", tradition: "Contemporary", category: "teaching", difficulty: "approachable", description: "Awakening to life's purpose beyond ego" },
  { title: "Guru Granth Sahib", slug: "Books/Guru-Granth-Sahib", tradition: "Sikh", category: "scripture", difficulty: "intermediate", description: "The living guru of the Sikhs — devotional poetry" },
  { title: "Early Islamic Mysticism", slug: "Books/Early-Islamic-Mysticism", tradition: "Sufi", category: "mysticism", difficulty: "intermediate", description: "Anthology of Islam's contemplative heart" },
  { title: "The Philosophy of the Teachings of Islam", slug: "Books/The-Philosophy-of-the-Teachings-of-Islam", tradition: "Islamic", category: "teaching", difficulty: "intermediate", description: "Islam's teachings on the soul's journey" },
  { title: "The Sutra of Queen Srimala", slug: "Books/The-Sutra-of-Queen-Srimala", tradition: "Buddhist", category: "scripture", difficulty: "advanced", description: "Buddha-nature inherent in all beings" },
  { title: "The Vimalakirti Sutra", slug: "Books/The-Vimalakirti-Sutra", tradition: "Buddhist", category: "scripture", difficulty: "intermediate", description: "Awakening transcends monasticism" },
  { title: "Letters from Sri Ramanasramam", slug: "Books/Letters-from-Sri-Ramanasramam", tradition: "Advaita Vedanta", category: "teaching", difficulty: "approachable", description: "Daily life with Ramana Maharshi" },
  { title: "Calvin and Hobbes", slug: "Books/Calvin-and-Hobbes", tradition: "Fiction", category: "fiction", difficulty: "approachable", description: "Profound wisdom disguised as a comic strip" },
  { title: "Dune", slug: "Books/Dune", tradition: "Fiction", category: "fiction", difficulty: "intermediate", description: "Consciousness, religion, ecology, and power" },
  { title: "Vagabond", slug: "Books/Vagabond", tradition: "Fiction", category: "manga", difficulty: "approachable", description: "The way of the sword as self-knowledge" },
  { title: "The Perfect Master, Vol 1", slug: "Books/The-Perfect-Master,-Vol-1", tradition: "Sufi", category: "teaching", difficulty: "intermediate", description: "Osho on Sufi stories and spiritual alchemy" },
  { title: "Upadesa Saram", slug: "Books/Upadesa-Saram", tradition: "Advaita Vedanta", category: "scripture", difficulty: "intermediate", description: "Ramana's 30 verses on spiritual instruction" },
  { title: "Coming Home to Yourself", slug: "Books/Coming-Home-to-Yourself", tradition: "Multiple", category: "teaching", difficulty: "approachable", description: "Meditation as the path to inner bliss" },
  { title: "In Search of the Miraculous", slug: "Books/In-Search-of-the-Miraculous", tradition: "Multiple", category: "teaching", difficulty: "intermediate", description: "Gurdjieff's Fourth Way teaching" },
  { title: "Silence of the Heart", slug: "Books/Silence-of-the-Heart", tradition: "Advaita Vedanta", category: "teaching", difficulty: "intermediate", description: "Robert Adams on the silence of your true nature" },
]

document.addEventListener("nav", () => {
  const startBtn = document.getElementById("wisdom-quiz-start") as HTMLButtonElement | null
  const quizEl = document.getElementById("wisdom-quiz")
  const closeBtn = document.getElementById("wisdom-quiz-close")
  const questionEl = document.getElementById("wisdom-quiz-question")
  const optionsEl = document.getElementById("wisdom-quiz-options")
  const progressEl = document.getElementById("wisdom-quiz-progress")
  const resultsEl = document.getElementById("wisdom-quiz-results")

  if (!startBtn || !quizEl || !questionEl || !optionsEl || !progressEl || !resultsEl) return

  let currentQ = 0
  const scores: Record<string, number> = {}

  function renderQuestion() {
    if (currentQ >= questions.length) {
      showResults()
      return
    }

    const q = questions[currentQ]
    questionEl!.textContent = q.text

    // Progress bar
    const pct = ((currentQ) / questions.length) * 100
    progressEl!.innerHTML = `<div class="wisdom-quiz__progress-bar" style="width:${pct}%"></div>`

    // Options
    optionsEl!.innerHTML = ""
    resultsEl!.style.display = "none"

    q.options.forEach((opt) => {
      const btn = document.createElement("button")
      btn.className = "wisdom-quiz__option"
      btn.textContent = opt.label
      btn.addEventListener("click", () => {
        for (const [tag, weight] of Object.entries(opt.tags)) {
          scores[tag] = (scores[tag] || 0) + weight
        }
        currentQ++
        renderQuestion()
      })
      optionsEl!.appendChild(btn)
    })
  }

  function showResults() {
    questionEl!.textContent = ""
    optionsEl!.innerHTML = ""
    progressEl!.innerHTML = `<div class="wisdom-quiz__progress-bar" style="width:100%"></div>`

    // Score each book
    const scored = bookDatabase.map((book) => {
      let score = 0
      score += scores[book.tradition] || 0
      score += scores[book.category] || 0
      score += scores[book.difficulty] || 0
      return { ...book, score }
    })

    // Sort by score descending, take top 5
    scored.sort((a, b) => b.score - a.score)
    const top = scored.slice(0, 5)

    let html = `<div class="wisdom-quiz__results-title">Your Recommended Reads</div>`
    html += `<div class="wisdom-quiz__results-section">`
    html += `<div class="wisdom-quiz__results-label">Books for you</div>`

    for (const book of top) {
      html += `<a href="/${book.slug}" class="wisdom-quiz__result-card internal" data-no-popover>`
      html += `<div class="wisdom-quiz__result-name">${book.title}</div>`
      html += `<div class="wisdom-quiz__result-desc">${book.description}</div>`
      html += `</a>`
    }
    html += `</div>`
    html += `<button class="wisdom-quiz__restart" id="wisdom-quiz-restart">Try Again</button>`

    resultsEl!.innerHTML = html
    resultsEl!.style.display = "block"

    // Restart handler
    const restartBtn = document.getElementById("wisdom-quiz-restart")
    if (restartBtn) {
      restartBtn.addEventListener("click", () => {
        currentQ = 0
        for (const key in scores) delete scores[key]
        resultsEl!.style.display = "none"
        renderQuestion()
      })
    }
  }

  // Start button
  startBtn.addEventListener("click", () => {
    quizEl!.style.display = "block"
    startBtn.style.display = "none"
    currentQ = 0
    for (const key in scores) delete scores[key]
    renderQuestion()
  })

  // Close button
  closeBtn?.addEventListener("click", () => {
    quizEl!.style.display = "none"
    startBtn.style.display = "inline-block"
  })
})
