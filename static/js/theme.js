document.addEventListener("DOMContentLoaded", function () {
    const html = document.documentElement;

    const darkBtn = document.getElementById("darkModeBtn");
    const lightBtn = document.getElementById("lightModeBtn");
    const avatarBtn = document.getElementById("avatarBtn");
    const dropdown = document.getElementById("profileDropdown");

    const savedTheme = localStorage.getItem("hangarin-theme");
    if (savedTheme) {
        html.setAttribute("data-theme", savedTheme);
    }

    if (darkBtn) {
        darkBtn.addEventListener("click", function () {
            html.setAttribute("data-theme", "dark");
            localStorage.setItem("hangarin-theme", "dark");
        });
    }

    if (lightBtn) {
        lightBtn.addEventListener("click", function () {
            html.setAttribute("data-theme", "light");
            localStorage.setItem("hangarin-theme", "light");
        });
    }

    if (avatarBtn && dropdown) {
        avatarBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            dropdown.classList.toggle("show");
        });

        document.addEventListener("click", function (e) {
            if (!avatarBtn.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.classList.remove("show");
            }
        });
    }
});