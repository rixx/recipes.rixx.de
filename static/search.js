let recipeData = null
let dataLoading = false


const renderSearchResults = (recipes) => {
    // build HTML
    console.log(recipes)
    const wrapper = document.querySelector("#search-container")
    const div = document.createElement("div")
    div.id = "search-results"
    if (!recipes.length && !tags.length) {
        div.classList.add("empty")  // allows us to always replace, because we're lazy like that
    } else {
        let content = ""
        recipes.forEach(recipe => {
            content += `<a href="/${recipe.id}/" class="result recipe-result">`
            if (recipe.cover) {
                content += `<img class="cover" src="/${recipe.id}/${recipe.cover}">`
            } else {
                content += `<img class="cover" src="/static/cover.png">`
            }
            content += `<div class="search-content"><div class="recipe-title">${recipe.title}</div></div></a>`
        })
        div.innerHTML = content
    }
    wrapper.replaceChild(div, wrapper.querySelector("#search-results"))
}

const updateSearch = () => {
    const searchInput = document.querySelector("input#search")
    const search = searchInput.value

    const searchTerms = search
        .split(" ")
        .filter(d => d.length)
        .map(d => d.toLowerCase().trim())

    if (!searchTerms.length) return renderSearchResults([], [])

    const recipeHits = recipeData.recipes.filter(recipe => recipe.search.filter(d => searchTerms.some(term => d.includes(term))).length)
    renderSearchResults(recipeHits)
}

const loadRecipeData = () => {
    if (recipeData) {
        return
    }
    dataLoading = true  // todo render

    fetch("/search.json").then(response => response.json().then(data => {
        recipeData = data
        dataLoading = false  // todo undo render
        const searchInput = document.querySelector("input#search")
        searchInput.removeEventListener("focus", loadRecipeData)
        searchInput.addEventListener("input", updateSearch)
        updateSearch()
    }))
}

const init = () => {
    const searchInput = document.querySelector("input#search")
    searchInput.addEventListener("focus", loadRecipeData)
}

if (document.readyState !== "loading") { init() } else {
    document.addEventListener('DOMContentLoaded', prepareSearch, false)
}
