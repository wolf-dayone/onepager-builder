(function () {
  "use strict";
  // Nur in modul-galerie.html eingebunden (siehe QA-ONLY-Marker in
  // tools/bauen.py galerie_bauen() und der Strip-Schritt in
  // tools/skill_bauen.py) - auf echten Onepagern existiert dieses Skript
  // gar nicht erst. Es nutzt ausschliesslich das oeffentliche
  // window.DAYONE_QA-Interface aus bausteine/_basis.js, keine internen
  // Details der einzelnen Module.

  if (!window.DAYONE_QA) return; // Schutz, falls die Datei je isoliert geladen wird

  var module = Array.prototype.slice.call(document.querySelectorAll("[data-modul]"));
  if (!module.length) return;

  var leiste = document.createElement("div");
  leiste.className = "qa-leiste";
  leiste.innerHTML =
    '<div class="qa-info">' +
      '<span class="qa-modul">–</span>' +
      '<span class="qa-viewport"></span>' +
    '</div>' +
    '<div class="qa-aktionen">' +
      '<button type="button" data-qa="replay">Replay current</button>' +
      '<button type="button" data-qa="replay-all">Replay all</button>' +
      '<button type="button" data-qa="anim" aria-pressed="false">Animations: on</button>' +
      '<button type="button" data-qa="reduced" aria-pressed="false">Reduced motion: off</button>' +
    '</div>';
  document.body.appendChild(leiste);

  var modulLabel = leiste.querySelector(".qa-modul");
  var viewportLabel = leiste.querySelector(".qa-viewport");
  var animBtn = leiste.querySelector('[data-qa="anim"]');
  var reducedBtn = leiste.querySelector('[data-qa="reduced"]');

  /* ---- aktuelles Modul: die Sektion, deren Mitte der Viewport-Mitte am
     naechsten liegt. rAF-gedrosselt, damit das Scroll-Event nicht bei jedem
     Pixel neu rechnet. ---- */
  var aktuelles = module[0];

  function aktuellesBestimmen() {
    var mitte = window.innerHeight / 2;
    var bester = module[0], besterAbstand = Infinity;
    module.forEach(function (m) {
      var rect = m.getBoundingClientRect();
      var modMitte = rect.top + rect.height / 2;
      var abstand = Math.abs(modMitte - mitte);
      if (abstand < besterAbstand) { besterAbstand = abstand; bester = m; }
    });
    aktuelles = bester;
    modulLabel.textContent = aktuelles.getAttribute("data-modul") || "–";
  }

  var scrollGeplant = false;
  window.addEventListener("scroll", function () {
    if (scrollGeplant) return;
    scrollGeplant = true;
    requestAnimationFrame(function () { aktuellesBestimmen(); scrollGeplant = false; });
  }, { passive: true });

  function viewportAnzeigen() {
    viewportLabel.textContent = window.innerWidth + "×" + window.innerHeight;
  }
  window.addEventListener("resize", viewportAnzeigen);
  viewportAnzeigen();
  aktuellesBestimmen();

  /* ---- Klick-Wiring ---- */
  var animationenAn = true;
  var reducedMotionAn = false;

  leiste.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest("button[data-qa]") : null;
    if (!btn) return;
    switch (btn.dataset.qa) {
      case "replay":
        window.DAYONE_QA.replay(aktuelles);
        break;
      case "replay-all":
        window.DAYONE_QA.replayAll();
        break;
      case "anim":
        animationenAn = !animationenAn;
        window.DAYONE_QA.setAnimationsEnabled(animationenAn);
        animBtn.textContent = "Animations: " + (animationenAn ? "on" : "off");
        animBtn.setAttribute("aria-pressed", animationenAn ? "false" : "true");
        break;
      case "reduced":
        reducedMotionAn = !reducedMotionAn;
        window.DAYONE_QA.setReducedMotion(reducedMotionAn);
        reducedBtn.textContent = "Reduced motion: " + (reducedMotionAn ? "on" : "off");
        reducedBtn.setAttribute("aria-pressed", reducedMotionAn ? "true" : "false");
        break;
    }
  });

  /* ---- Alle Animationen einmal direkt beim Laden anstossen, damit man sie
     sieht, ohne erst scrollen zu muessen (Kernziel aus dem Testkonzept). ---- */
  requestAnimationFrame(function () { window.DAYONE_QA.replayAll(); });
})();
