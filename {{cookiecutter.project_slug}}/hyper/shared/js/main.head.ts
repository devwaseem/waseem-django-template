const savedTheme = window.localStorage.getItem("theme");
const preferredTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";

document.documentElement.dataset.theme =
  savedTheme === "light" || savedTheme === "dark" ? savedTheme : preferredTheme;
