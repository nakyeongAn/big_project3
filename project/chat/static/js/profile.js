document.querySelectorAll(".nav-tabs .nav-link").forEach(function(link) {
    link.addEventListener("click", function(e) {
        e.preventDefault();
        document
            .querySelectorAll(".nav-tabs .nav-link")
            .forEach(function(navLink) {
                navLink.classList.remove("active");
            });
        this.classList.add("active");

        let activeTab = this.getAttribute("href");
        document
            .querySelectorAll(".tab-content .tab-pane")
            .forEach(function(tabPane) {
                tabPane.classList.remove("show", "active");
            });
        document.querySelector(activeTab).classList.add("show", "active");
    });
});

document
    .getElementById("profilePictureInput")
    .addEventListener("change", function(event) {
        const fileReader = new FileReader();
        fileReader.onload = function(e) {
            document.querySelector(".profile-img img").src = e.target.result;
        };
        fileReader.readAsDataURL(event.target.files[0]);
    });

$(".nav ul li").click(function() {
    $(this).addClass("active").siblings().removeClass("active");
});

const tabBtn = document.querySelectorAll(".nav ul li");
const tab = document.querySelectorAll(".tab");

function tabs(panelIndex) {
    tab.forEach(function(node) {
        node.style.display = "none";
    });
    tab[panelIndex].style.display = "block";
}
tabs(0);

let bio = document.querySelector(".bio");
// ... rest of the code ...

const bioMore = document.querySelector("#see-more-bio");
const bioLength = bio.innerText.length;

function bioText() {
    bio.oldText = bio.innerText;

    bio.innerText = bio.innerText.substring(0, 100) + "...";
    bio.innerHTML += `<span onclick='addLength()' id='see-more-bio'>See More</span>`;
}
//        console.log(bio.innerText)

bioText();

function addLength() {
    bio.innerText = bio.oldText;
    bio.innerHTML +=
        "&nbsp;" + `<span onclick='bioText()' id='see-less-bio'>See Less</span>`;
    document.getElementById("see-less-bio").addEventListener("click", () => {
        document.getElementById("see-less-bio").style.display = "none";
    });
}
if (document.querySelector(".alert-message").innerText > 9) {
    document.querySelector(".alert-message").style.fontSize = ".7rem";
}