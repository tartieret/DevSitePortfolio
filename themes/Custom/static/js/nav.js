// Mobile menu: close the <details> disclosure on Escape or on a tap outside it.
(function () {
  var menu = document.querySelector(".nav-mobile");
  if (!menu) return;

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && menu.open) {
      menu.open = false;
      menu.querySelector("summary").focus();
    }
  });

  document.addEventListener("click", function (event) {
    if (menu.open && !menu.contains(event.target)) menu.open = false;
  });
})();
