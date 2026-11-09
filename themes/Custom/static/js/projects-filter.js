// Project filters: show only projects whose data-filters contain the chosen key.
(function () {
  var buttons = document.querySelectorAll(".filters [data-filter]");
  var projects = document.querySelectorAll(".project[data-filters]");

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var key = button.getAttribute("data-filter");
      buttons.forEach(function (b) {
        b.setAttribute("aria-pressed", b === button ? "true" : "false");
      });
      projects.forEach(function (project) {
        var keys = project.getAttribute("data-filters").split(" ");
        project.hidden = key !== "*" && keys.indexOf(key) === -1;
      });
    });
  });
})();
