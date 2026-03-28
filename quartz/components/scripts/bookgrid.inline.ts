document.addEventListener("nav", () => {
  const filters = document.getElementById("book-grid-filters")
  if (!filters) return

  const buttons = filters.querySelectorAll<HTMLButtonElement>(".book-grid__filter-btn")
  const sections = document.querySelectorAll<HTMLElement>(".book-grid__section")

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const filter = btn.getAttribute("data-filter")

      // Update active button
      buttons.forEach((b) => b.classList.remove("book-grid__filter-btn--active"))
      btn.classList.add("book-grid__filter-btn--active")

      // Show/hide sections
      if (filter === "all") {
        sections.forEach((s) => s.classList.remove("book-grid__section--hidden"))
      } else {
        sections.forEach((s) => {
          if (s.getAttribute("data-category") === filter) {
            s.classList.remove("book-grid__section--hidden")
          } else {
            s.classList.add("book-grid__section--hidden")
          }
        })
      }
    })
  })
})
