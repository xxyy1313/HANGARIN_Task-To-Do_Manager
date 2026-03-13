document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("themeToggle");
    const htmlElement = document.documentElement;

    const savedTheme = localStorage.getItem("hangarin-theme");
    if (savedTheme) {
        htmlElement.setAttribute("data-theme", savedTheme);
    }

    if (themeToggle) {
        themeToggle.addEventListener("click", function () {
            const currentTheme = htmlElement.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";

            htmlElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("hangarin-theme", newTheme);
        });
    }
});