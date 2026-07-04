const navToggle = document.querySelector("[data-nav-toggle]");
const siteNav = document.querySelector("[data-site-nav]");

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

document.querySelectorAll("[data-lab-src]").forEach((frame) => {
  frame.setAttribute("src", frame.getAttribute("data-lab-src"));
});

document.querySelectorAll("[data-lab-href]").forEach((link) => {
  link.setAttribute("href", link.getAttribute("data-lab-href"));
});
