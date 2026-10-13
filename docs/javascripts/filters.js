// Level and provider filters for the training catalog.
//
// The filter bar is rendered hidden, so readers without JavaScript see every
// card and no dead buttons. Section headings hide when all their cards do.
(function () {
  function setup() {
    var bar = document.querySelector(".dt-filter");
    if (!bar || bar.dataset.ready) return;
    bar.dataset.ready = "1";
    bar.hidden = false;

    var active = { level: "", provider: "" };
    var empty = bar.querySelector(".dt-filter__empty");

    function apply() {
      var shown = 0;
      document.querySelectorAll(".dt-grid").forEach(function (grid) {
        var visible = 0;
        grid.querySelectorAll(".dt-card").forEach(function (card) {
          var match =
            (!active.level || card.dataset.level === active.level) &&
            (!active.provider || card.dataset.provider === active.provider);
          card.hidden = !match;
          if (match) visible += 1;
        });
        shown += visible;
        // Hide the section heading and intro that precede an empty grid
        var intro = grid.previousElementSibling;
        var heading = intro && intro.previousElementSibling;
        [grid, intro, heading].forEach(function (el) {
          if (el) el.hidden = visible === 0;
        });
      });
      empty.hidden = shown !== 0;
    }

    bar.addEventListener("click", function (event) {
      var chip = event.target.closest(".dt-chip");
      if (!chip) return;
      var name = chip.dataset.filter;
      active[name] = chip.dataset.value;
      bar.querySelectorAll('.dt-chip[data-filter="' + name + '"]').forEach(function (other) {
        other.setAttribute("aria-pressed", String(other === chip));
      });
      apply();
    });
  }

  // Material-style themes expose document$ for instant navigation
  if (typeof document$ !== "undefined") {
    document$.subscribe(setup);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setup);
  } else {
    setup();
  }
})();
