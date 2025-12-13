const lightbox = {
    overlay: null,
    img: null,
    prevBtn: null,
    nextBtn: null,
    closeBtn: null,
    images: [],
    currentIndex: 0,

    init() {
        const gallery = document.querySelector("#recipe-gallery")
        if (!gallery) return

        this.images = Array.from(gallery.querySelectorAll("a")).map(a => a.href)
        if (this.images.length === 0) return

        this.createElements()
        this.bindEvents(gallery)
    },

    createElements() {
        this.overlay = document.createElement("div")
        this.overlay.id = "lightbox-overlay"
        this.overlay.className = "hidden"
        this.overlay.innerHTML = `
            <button class="lightbox-close" aria-label="Schließen">&times;</button>
            <button class="lightbox-prev" aria-label="Vorheriges Bild">&#8249;</button>
            <img class="lightbox-img" src="" alt="">
            <button class="lightbox-next" aria-label="Nächstes Bild">&#8250;</button>
        `
        document.body.appendChild(this.overlay)

        this.img = this.overlay.querySelector(".lightbox-img")
        this.prevBtn = this.overlay.querySelector(".lightbox-prev")
        this.nextBtn = this.overlay.querySelector(".lightbox-next")
        this.closeBtn = this.overlay.querySelector(".lightbox-close")
    },

    bindEvents(gallery) {
        gallery.addEventListener("click", (e) => {
            const link = e.target.closest("a")
            if (!link) return
            e.preventDefault()
            this.currentIndex = this.images.indexOf(link.href)
            this.open()
        })

        this.overlay.addEventListener("click", (e) => {
            if (e.target === this.overlay) this.close()
        })

        this.closeBtn.addEventListener("click", () => this.close())
        this.prevBtn.addEventListener("click", () => this.prev())
        this.nextBtn.addEventListener("click", () => this.next())

        document.addEventListener("keydown", (e) => {
            if (this.overlay.classList.contains("hidden")) return
            if (e.key === "Escape") this.close()
            if (e.key === "ArrowLeft") this.prev()
            if (e.key === "ArrowRight") this.next()
        })
    },

    open() {
        this.img.src = this.images[this.currentIndex]
        this.overlay.classList.remove("hidden")
        this.updateNav()
        document.body.style.overflow = "hidden"
    },

    close() {
        this.overlay.classList.add("hidden")
        document.body.style.overflow = ""
    },

    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--
            this.img.src = this.images[this.currentIndex]
            this.updateNav()
        }
    },

    next() {
        if (this.currentIndex < this.images.length - 1) {
            this.currentIndex++
            this.img.src = this.images[this.currentIndex]
            this.updateNav()
        }
    },

    updateNav() {
        this.prevBtn.style.visibility = this.currentIndex > 0 ? "visible" : "hidden"
        this.nextBtn.style.visibility = this.currentIndex < this.images.length - 1 ? "visible" : "hidden"
    }
}

if (document.readyState !== "loading") {
    lightbox.init()
} else {
    document.addEventListener("DOMContentLoaded", () => lightbox.init(), false)
}
