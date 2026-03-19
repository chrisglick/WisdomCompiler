const quotes = [
  { text: "A Jnani need not prostrate before anybody nor need he give his blessings to anybody", source: "Letters from Sri Ramanasramam", slug: "Wisdom-Quotes/A Jnani need not prostrate before anybody nor need he give his blessings to anybody" },
  { text: "A fire leaps up from our inside like lightning and another fire descends upon us from above", source: "The Philosophy of the Teachings of Islam", slug: "Wisdom-Quotes/A fire leaps up from our inside like lightning and another fire descends upon us from above" },
  { text: "A person's paradise is developed inside him", source: "The Philosophy of the Teachings of Islam", slug: "Wisdom-Quotes/A person's paradise is developed inside him" },
  { text: "Abhyasa consists in withdrawal within the Self every time you are disturbed by thought", source: "Talks with Ramana Maharshi", slug: "Wisdom-Quotes/Abhyasa consists in withdrawal within the Self every time you are disturbed by thought" },
  { text: "All effort is only for giving up the notion that we are limited", source: "Day by Day with Bhagavan", slug: "Wisdom-Quotes/All effort is only for giving up the notion that we are limited" },
  { text: "All that can be done can be done through understanding", source: "Vigyan Bhairav Tantra Volume 1", slug: "Wisdom-Quotes/All that can be done can be done through understanding" },
  { text: "All the concepts you have formed in the past must be discarded and replaced by void", source: "The Zen Teaching of Huang Po", slug: "Wisdom-Quotes/All the concepts you have formed in the past must be discarded and replaced by void" },
  { text: "All the sadhana that we do is meant to invoke a strong experiential feeling of belongingness", source: "Swami Ishwarananda Giriji Maharaj", slug: "Wisdom-Quotes/All the sadhana that we do is meant to invoke a strong experiential feeling of belongingness" },
  { text: "And you threw not when you did throw, but it was Allah Who threw", source: "The Philosophy of the Teachings of Islam", slug: "Wisdom-Quotes/And you threw not when you did throw, but it was Allah Who threw" },
  { text: "And you, O soul at peace! Return to your Lord well pleased with Him and He well pleased with you", source: "The Philosophy of the Teachings of Islam", slug: "Wisdom-Quotes/And you, O soul at peace! Return to your Lord well pleased with Him and He well pleased with you_" },
  { text: "Attention to ones own Self is the only raft", source: "Ramana Maharshi", slug: "Wisdom-Quotes/Attention to ones own Self is the only raft" },
  { text: "Be aware of yourself And accept yourself as you are", source: "Vagabond", slug: "Wisdom-Quotes/Be aware of yourself And accept yourself as you are" },
  { text: "Brahma-Vidya is nothing other than seeing That which remains", source: "Guru Vachaka Kovai", slug: "Wisdom-Quotes/Brahma-Vidya  is nothing other than seeing That which remains" },
  { text: "But the prisoner has become too identified with the prison cell", source: "The Perfect Master, Vol 1", slug: "Wisdom-Quotes/But the prisoner has become too identified with the prison cell" },
  { text: "By whatever path you go you will have to lose yourself in the One", source: "Day by Day with Bhagavan", slug: "Wisdom-Quotes/By whatever path you go you will have to lose yourself in the One" },
  { text: "Complete erasure of the ego is necessary", source: "Day by Day with Bhagavan", slug: "Wisdom-Quotes/Complete erasure of the ego is necessary" },
  { text: "Dharma is neither preached in words nor otherwise signified", source: "The Zen Teaching of Huang Po", slug: "Wisdom-Quotes/Dharma is neither preached in words nor otherwise signified" },
  { text: "Divine grace still bestows this bounty upon those who seek it", source: "The Philosophy of the Teachings of Islam", slug: "Wisdom-Quotes/Divine grace still bestows this bounty upon those who seek it" },
  { text: "Dont believe your thoughts", source: "Ramana Maharshi", slug: "Wisdom-Quotes/Dont believe your thoughts" },
  { text: "Enter into the silence of the temple", source: "The New Dawn", slug: "Wisdom-Quotes/Enter into the silence of the temple" },
  { text: "Even amidst great action the wise one remains still", source: "Ashtavakra Gita", slug: "Wisdom-Quotes/Even amidst great action the wise one remains still" },
  { text: "First you must throw away all your opinions", source: "Dropping Ashes On the Buddha", slug: "Wisdom-Quotes/First you must throw away all your opinions" },
  { text: "For the extroverted intellect, the means to abide in Self is to begin enquiring inwardly", source: "Guru Vachaka Kovai", slug: "Wisdom-Quotes/For the extroverted intellect, the means to abide in Self is to begin enquiring inwardly" },
  { text: "Fortunate is the man who does not lose himself in the labyrinths of philosophy", source: "Ramana Maharshi", slug: "Wisdom-Quotes/Fortunate is the man who does not lose himself in the labyrinths of philosophy" },
  { text: "Gateway of the Stillness beyond all Activity", source: "The Zen Teaching of Huang Po", slug: "Wisdom-Quotes/Gateway of the Stillness beyond all Activity" },
  { text: "Give up the desire that tends to bondage and the desire for liberation too", source: "Yoga Vasistha", slug: "Wisdom-Quotes/Give up the desire that tends to bondage and the desire for liberation too.txt" },
  { text: "Guru is not merely the perfection you wish to conquer", source: "Swami Ishwarananda Giriji Maharaj", slug: "Wisdom-Quotes/Guru is not merely the perfection you wish  to conquer" },
  { text: "He is everywhere unattached and free", source: "Ashtavakra Gita", slug: "Wisdom-Quotes/He is everywhere unattached and free" },
  { text: "I falsely imagined till now that all these which are yours", source: "Day by Day with Bhagavan", slug: "Wisdom-Quotes/I falsely imagined till now that all these which are yours" },
  { text: "In the deep sleep state we lay down our ego", source: "Ramana Maharshi", slug: "Wisdom-Quotes/In the deep sleep state we lay down our ego" },
  { text: "It is true wisdom for the mind to turn away From outer objects and behold Its own effulgent form", source: "Ramana Maharshi", slug: "Wisdom-Quotes/It is true wisdom for the mind to turn away From outer objects and behold Its own effulgent form" },
  { text: "Let not a day pass without communion with nature which is so divine", source: "Swami Ishwarananda Giriji Maharaj", slug: "Wisdom-Quotes/Let not a day pass without communion with nature which is so divine" },
  { text: "Liberation is not had except through the cessation of all notions", source: "Yoga Vasistha", slug: "Wisdom-Quotes/Liberation is not had except through the cessation of all notions" },
  { text: "Most people are so totally identified with their strong feelings of likes and dislikes that they are", source: "Swami Ishwarananda Giriji Maharaj", slug: "Wisdom-Quotes/Most people are so totally identified with their strong feelings of likes and dislikes that they are" },
  { text: "My state never felt the creation and dissolution of the universe", source: "Consciousness and the Absolute", slug: "Wisdom-Quotes/My state never felt the creation and dissolution of the universe" },
  { text: "Peace is the inner nature of humankind", source: "Ramana Maharshi", slug: "Wisdom-Quotes/Peace is the inner nature of humankind" },
  { text: "Rare is the one who believes nothing and is never confused", source: "Ashtavakra Gita", slug: "Wisdom-Quotes/Rare is the one who believes nothing and is never confused" },
  { text: "Realisation now consists in getting rid of this false idea that one is not realised", source: "Talks with Ramana Maharshi", slug: "Wisdom-Quotes/Realisation now consists in getting rid of this false idea that one is not realised" },
  { text: "Seek the conquest of the mind and self-control which are the fruits of wisdom", source: "Yoga Vasistha", slug: "Wisdom-Quotes/Seek the conquest of the mind and self-control which are the fruits of wisdom" },
  { text: "Self-surrender is the same as Self-knowledge", source: "Ramana Maharshi", slug: "Wisdom-Quotes/Self-surrender is the same as Self-knowledge" },
  { text: "The fool thinks peace comes by controlling the mind", source: "Ashtavakra Gita", slug: "Wisdom-Quotes/The fool thinks peace comes by controlling the mind" },
  { text: "The loneliness transforms into aloneness", source: "The New Dawn", slug: "Wisdom-Quotes/The loneliness transforms into aloneness" },
  { text: "The naked light in a windless place", source: "Letters from Sri Ramanasramam", slug: "Wisdom-Quotes/The naked light in a windless place" },
  { text: "The real worship of him is to be in mouna (silence)", source: "Letters from Sri Ramanasramam", slug: "Wisdom-Quotes/The real worship of him is to be in mouna (silence)" },
  { text: "To perform one's duty carefully is the greatest service to God", source: "Talks with Ramana Maharshi", slug: "Wisdom-Quotes/To perform one's duty carefully is the greatest service to God" },
  { text: "Transform your intelligence into the purest of paper", source: "Guru Granth Sahib", slug: "Wisdom-Quotes/Transform your intelligence into the purest of paper" },
  { text: "Transforming yourself is a means of giving light to the whole world", source: "Ramana Maharshi", slug: "Wisdom-Quotes/Transforming yourself is a means of giving light to the whole world" },
  { text: "When you are very quiet you have arrived at the basis of everything", source: "Consciousness and the Absolute", slug: "Wisdom-Quotes/When you are very quiet you have arrived at the basis of everything" },
  { text: "You are not a foreigner in existence", source: "The New Dawn", slug: "Wisdom-Quotes/You are not a foreigner in existence" },
  { text: "You are the constant illumination that lights up both the experiences and the void", source: "Day by Day with Bhagavan", slug: "Wisdom-Quotes/You are the constant illumination that lights up both the experiences and the void" },
]

const MONTHS = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
]

function sluggify(s: string): string {
  return s
    .split("/")
    .map((segment) =>
      segment
        .replace(/\s/g, "-")
        .replace(/&/g, "-and-")
        .replace(/%/g, "-percent")
        .replace(/\?/g, "")
        .replace(/#/g, ""),
    )
    .join("/")
    .replace(/\/$/, "")
}

document.addEventListener("nav", () => {
  const container = document.getElementById("daily-wisdom")
  if (!container) return

  const now = new Date()
  const year = now.getFullYear()
  const startOfYear = new Date(year, 0, 1)
  const dayOfYear = Math.floor((now.getTime() - startOfYear.getTime()) / 86400000)

  // Deterministic daily selection — same quote for everyone all day
  const index = dayOfYear % quotes.length
  const q = quotes[index]

  const labelEl = document.getElementById("daily-wisdom-label")
  const quoteEl = document.getElementById("daily-wisdom-text")
  const sourceEl = document.getElementById("daily-wisdom-source")
  const linkEl = document.getElementById("daily-wisdom-link") as HTMLAnchorElement | null

  if (!quoteEl || !sourceEl) return

  const dateStr = `${MONTHS[now.getMonth()]} ${now.getDate()}`
  if (labelEl) labelEl.textContent = `Today\u2019s Wisdom \u2014 ${dateStr}`

  quoteEl.textContent = q.text
  sourceEl.textContent = "\u2014 " + q.source
  if (linkEl) linkEl.href = "/" + sluggify(q.slug)
})
