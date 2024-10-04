let hasCarousels = false

const updateSearch = () => {
    const search = document.querySelector("input#search").value

    const searchTerms = search
        .split(" ")
        .filter(d => d.length)
        .map(d => d.toLowerCase().trim())

    if (!searchTerms.length) {
        document.querySelectorAll(".recipe-card").forEach(card => card.classList.remove("hidden"))
    } else {
        document.querySelectorAll(".recipe-card").forEach(card => {
            const match = searchTerms.every(term => card.textContent.toLowerCase().includes(term))
            if (match) {
                card.classList.remove("hidden")
            } else {
                card.classList.add("hidden")
            }
        })
    }

    // Hide carousels if there are no results
    if (hasCarousels) {
        document.querySelectorAll(".recipe-carousel").forEach(carousel => {
            const visibleCards = carousel.querySelectorAll(".recipe-card:not(.hidden)")
            if (visibleCards.length === 0) {
                carousel.classList.add("hidden")
                carousel.previousElementSibling.classList.add("hidden")
            } else {
                carousel.classList.remove("hidden")
                carousel.previousElementSibling.classList.remove("hidden")
            }
        })
    }
}

const init = () => {
    document.querySelector("input#search").addEventListener("input", updateSearch)
    hasCarousels = document.querySelectorAll(".recipe-carousel").length > 0
}

if (document.readyState !== "loading") { init() } else {
    document.addEventListener('DOMContentLoaded', prepareSearch, false)
}
