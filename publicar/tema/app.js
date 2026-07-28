// Alternância de tema (claro/escuro) — dependency-free, persistida na sessão.
(function () {
  var b = document.getElementById("alt-tema");
  if (!b) return;
  b.addEventListener("click", function () {
    var r = document.documentElement;
    var dark = r.getAttribute("data-theme") === "dark" ||
      (!r.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    r.setAttribute("data-theme", dark ? "light" : "dark");
  });
})();
