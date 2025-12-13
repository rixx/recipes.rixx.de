let recipes = []
let searchInput = null
let resultsContainer = null

const loadRecipes = async () => {
    const response = await fetch("/search.json")
    recipes = await response.json()
}

const updateSearch = () => {
    const search = searchInput.value
    const searchTerms = search
        .split(" ")
        .filter(d => d.length)
        .map(d => d.toLowerCase().trim())

    if (!searchTerms.length) {
        resultsContainer.classList.add("hidden")
        resultsContainer.innerHTML = ""
        return
    }

    const matches = recipes.filter(recipe => {
        const searchText = `${recipe.title} ${recipe.tags.join(" ")} ${recipe.category}`.toLowerCase()
        return searchTerms.every(term => searchText.includes(term))
    }).slice(0, 8)

    if (matches.length === 0) {
        resultsContainer.innerHTML = '<div class="search-no-results">Keine Rezepte gefunden</div>'
        resultsContainer.classList.remove("hidden")
        return
    }

    resultsContainer.innerHTML = matches.map(recipe => {
        const thumbnail = recipe.thumbnail
            ? `<img src="${recipe.thumbnail}" alt="">`
            : '<div class="search-placeholder"></div>'
        const tags = recipe.tags.length > 0 ? `<span class="search-tags">${recipe.tags.join(", ")}</span>` : ""
        return `<a href="/${recipe.id}/" class="search-result">
            ${thumbnail}
            <div class="search-result-text">
                <span class="search-title">${recipe.title}</span>
                ${tags}
            </div>
        </a>`
    }).join("")

    resultsContainer.classList.remove("hidden")
}

const handleClickOutside = (e) => {
    if (!resultsContainer.contains(e.target) && e.target !== searchInput) {
        resultsContainer.classList.add("hidden")
    }
}

const handleFocus = () => {
    if (searchInput.value.trim().length > 0) {
        updateSearch()
    }
}

const init = () => {
    searchInput = document.querySelector("input#search")
    resultsContainer = document.querySelector("#search-results")

    if (!searchInput || !resultsContainer) return

    loadRecipes()
    searchInput.addEventListener("input", updateSearch)
    searchInput.addEventListener("focus", handleFocus)
    document.addEventListener("click", handleClickOutside)
}

if (document.readyState !== "loading") {
    init()
} else {
    document.addEventListener("DOMContentLoaded", init, false)
}
