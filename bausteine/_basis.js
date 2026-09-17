(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- 1) Kapitel-Nav aus den Sektionen aufbauen ---- */
  var nav = document.getElementById("chapter-nav");
  var list = nav.querySelector("ol");
  var brand = nav.querySelector(".brand-group");
  var chapters = Array.prototype.slice.call(document.querySelectorAll("[data-chapter]"));

  chapters.forEach(function (sec) {
    var li = document.createElement("li");
    var a = document.createElement("a");
    a.href = "#" + sec.id;
    a.dataset.title = sec.dataset.chapterTitle || "";
    a.innerHTML = '<span class="ch-num">' + sec.dataset.chapter + '</span>' +
                  '<span class="ch-title">' + (sec.dataset.chapterTitle || "") + '</span>';
    li.appendChild(a);
    list.appendChild(li);
  });

  /* ---- 2) Nav einblenden, sobald Hero (bzw. Agenda) durchgescrollt ist ---- */
  var trigger = document.getElementById("agenda") || document.getElementById("hero");
  if (trigger && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      nav.classList.toggle("visible", !entries[0].isIntersecting);
    }, { rootMargin: "-80px 0px 0px 0px" }).observe(trigger);
  }

  /* ---- 3) Aktives Kapitel markieren ---- */
  if ("IntersectionObserver" in window) {
    var linkMap = {};
    list.querySelectorAll("a").forEach(function (a) { linkMap[a.getAttribute("href").slice(1)] = a; });
    var activeObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        for (var k in linkMap) linkMap[k].classList.remove("active");
        if (linkMap[e.target.id]) linkMap[e.target.id].classList.add("active");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    chapters.forEach(function (s) { activeObs.observe(s); });
  }

  /* ---- 4) Prioritäts-Kaskade nach verfügbarem Platz (keine festen Breakpoints) ----
     Reihenfolge, in der Elemente weichen, sobald der Kapitel-Track nicht mehr passt:
       1. Voller Zustand (Logo + Präsentationstitel + Kapitel mit vollem Titel)
       2. Präsentationstitel weg (.no-title)      — Kapitel-Navigation geht vor
       3. Kapitel → Nummern + Tooltip (.compact)  — wie Figma "Anzeige=Nummern"
       4. Logo → Icon ohne Schriftzug (.icon-only) — letzte Stufe
     Jede Stufe misst den tatsächlichen Überlauf neu, statt eine Bildschirmbreite
     anzunehmen — bei vielen/langen Kapiteltiteln oder einem langen Präsentationstitel
     kann das schon bei 1200px greifen, bei kurzen Titeln erst deutlich später. */
  function fitNav() {
    nav.classList.remove("no-title", "compact", "icon-only");
    var inner = nav.querySelector(".inner");
    // inner.clientWidth zaehlt das eigene Padding-Inline von .wrap mit (96px
    // Desktop / 24px Mobile je Seite) - ohne den Abzug hielt fits() die Nav
    // fuer 192px (bzw. 48px) breiter als sie in Wirklichkeit ist und
    // ueberspringt dadurch die Kaskade (.no-title/.compact/.icon-only). Der
    // Ueberlauf verschwand dann unbemerkt im internen overflow-x:auto der
    // Kapitelliste (Sicherheitsnetz) statt sich sichtbar ueber die Kaskade
    // abzubauen - gefunden per Playwright, nicht durch Code-Lesen sichtbar.
    var innerStyle = getComputedStyle(inner);
    var innerPadding = parseFloat(innerStyle.paddingLeft) + parseFloat(innerStyle.paddingRight);
    var fits = function () {
      return list.scrollWidth <= inner.clientWidth - innerPadding - brand.offsetWidth - 32;
    };
    if (fits()) return;
    nav.classList.add("no-title");
    if (fits()) return;
    nav.classList.add("compact");
    if (fits()) return;
    nav.classList.add("icon-only");
  }
  window.addEventListener("resize", fitNav);
  fitNav();

  /* ---- 5) Reveal: pro Sektion gestaffelt (Opacity + Y-Verschiebung), Hero sofort beim
     Laden statt beim Scrollen — alle anderen Sektionen erst wenn sie in den Viewport
     kommen. Die Verzögerung pro Element wird per data-Attribut auf jeder Sektion
     gesteuert, nicht global — dadurch bleibt eine 3-Item-Section knackig und eine
     8-Item-Section trotzdem lesbar gestaffelt statt trödelnd. ---- */
  var STAGGER_MS = 220, STAGGER_MAX_MS = 960;
  function stageReveal(container) {
    var items = container.classList && container.classList.contains("reveal")
      ? [container] : container.querySelectorAll(".reveal");
    items.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i * STAGGER_MS, STAGGER_MAX_MS) + "ms";
      el.classList.add("in");
    });
  }
  var heroEl = document.getElementById("hero");
  if (heroEl) {
    if (reduce) { heroEl.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); }); }
    else { stageReveal(heroEl); }
  }
  var revealSections = Array.prototype.slice.call(document.querySelectorAll("section, footer"))
    .filter(function (s) { return s !== heroEl && s.querySelector(".reveal"); });
  if (reduce || !("IntersectionObserver" in window)) {
    revealSections.forEach(function (s) { stageReveal(s); });
  } else {
    /* Feuert, sobald die Sektion die vertikale Mitte des Viewports erreicht — nicht
       schon, wenn ihre Unterkante am unteren Bildschirmrand auftaucht. rootMargin
       schrumpft den Beobachtungsbereich auf einen schmalen Streifen um die Mitte. */
    var revObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { stageReveal(e.target); revObs.unobserve(e.target); }
      });
    }, { rootMargin: "-48% 0px -48% 0px", threshold: 0 });
    revealSections.forEach(function (s) { revObs.observe(s); });
  }

  /* ---- 6) Kennzahlen hochzählen ---- */
  var counters = document.querySelectorAll("[data-count-to]");
  function countUp(el) {
    var target = parseFloat(el.dataset.countTo);
    if (reduce) { el.textContent = target; return; }
    var start = performance.now(), dur = 1200;
    function step(now) {
      var p = Math.min((now - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var cObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { countUp(e.target); cObs.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cObs.observe(el); });
  } else {
    counters.forEach(function (el) { el.textContent = el.dataset.countTo; });
  }

  /* ---- 7) Roadmap-Timeline: farbige Linie bis zum aktuellen Punkt ----
     Breite = Position des .is-current-Punkts im Track (Dots sitzen am linken Rand
     jedes flex:1-Items, siehe .timeline-dot). Erst beim Sichtbarwerden auf die
     Zielbreite animieren (transition auf .timeline-progress erledigt das optisch),
     damit die Linie sich sichtbar "auffüllt" statt einfach dazustehen. */
  document.querySelectorAll(".timeline").forEach(function (tl) {
    var items = tl.querySelectorAll(".timeline-item");
    var progress = tl.querySelector(".timeline-progress");
    if (!items.length || !progress) return;
    var currentIndex = Array.prototype.findIndex.call(items, function (it) {
      return it.classList.contains("is-current");
    });
    if (currentIndex < 0) return; // kein aktueller Punkt markiert -> keine Linie zeichnen
    var targetPct = (currentIndex / items.length) * 100 + "%";
    if (reduce) { progress.style.width = targetPct; return; }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { progress.style.width = targetPct; obs.unobserve(e.target); }
        });
      }, { rootMargin: "-48% 0px -48% 0px", threshold: 0 }).observe(tl);
    } else {
      progress.style.width = targetPct;
    }
  });

  /* ---- 8) Karussell ---- */
  document.querySelectorAll("[data-carousel]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var track = document.getElementById(btn.dataset.carousel);
      if (!track) return;
      var card = track.querySelector(".card");
      // Card-Breite + tatsaechlicher Grid-Gap (nicht mehr hart 32px codiert -
      // sonst laeuft der Klick-Sprung wieder auseinander, sobald sich der
      // gap-Wert im CSS aendert, wie es beim Karussell-Fix passiert ist).
      var gap = card ? parseFloat(getComputedStyle(track).columnGap) || 0 : 0;
      var step = card ? card.getBoundingClientRect().width + gap : 400;
      track.scrollBy({ left: step * parseInt(btn.dataset.dir, 10), behavior: reduce ? "auto" : "smooth" });
    });
  });

  /* ---- 9) Stepper: Phasenleiste umschalten ----
     Die Leiste selbst bleibt per position:sticky oben stehen (CSS). Hier nur
     das Umschalten der Panels. Ohne JS bleibt Phase 1 sichtbar - der Inhalt
     geht also nie verloren. */
  document.querySelectorAll(".stepper-tabs").forEach(function (leiste) {
    var tabs = Array.prototype.slice.call(leiste.querySelectorAll(".stepper-tab"));
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        tabs.forEach(function (t) {
          var aktiv = t === tab;
          t.setAttribute("aria-selected", aktiv ? "true" : "false");
          var panel = document.getElementById(t.getAttribute("aria-controls"));
          if (!panel) return;
          if (!aktiv) { panel.hidden = true; panel.classList.remove("ist-erscheinend"); return; }
          panel.hidden = false;
          if (reduce) return;
          /* Panels tragen noch ein transitionDelay als Inline-Style vom
             gestaffelten Scroll-Reveal beim ersten Sichtbarwerden der Section
             (siehe stageReveal). Ungeloescht wuerde das auch diesen Wechsel
             verzoegern - deshalb hier zuruecksetzen, damit der Panel-Wechsel
             immer sofort losläuft. */
          panel.style.transitionDelay = "0ms";
          /* Panel startet unsichtbar/leicht versetzt (CSS: .ist-erscheinend),
             dann per Klasse-Entfernen in den Endzustand ueberfuehrt - das
             doppelte rAF stellt sicher, dass der Browser den Startzustand
             erst gemalt hat, bevor die Transition losläuft (sonst überspringt
             sie manche Browser komplett). */
          panel.classList.add("ist-erscheinend");
          requestAnimationFrame(function () {
            requestAnimationFrame(function () { panel.classList.remove("ist-erscheinend"); });
          });
        });
      });
    });
  });
})();
