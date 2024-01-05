document.querySelectorAll(".nav .nav-link").forEach(function(link) {
    link.addEventListener("click", function(e) {
        e.preventDefault();
        document.querySelectorAll(".nav .nav-link").forEach(function(navLink) { // Corrected here
            navLink.classList.remove("active");
        });
        this.classList.add("active");

        let activeTab = this.getAttribute("href");
        document.querySelectorAll(".tab-content .tab-pane").forEach(function(tabPane) {
            tabPane.classList.remove("active");
        });
        document.querySelector(activeTab).classList.add("active");
    });
});