(function () {
  "use strict";
  // qaForceReducedMotion/qa-anim-off werden ausschliesslich von der QA-Leiste
  // in modul-galerie.html gesetzt (siehe Abschnitt 10 unten und
  // bausteine/_galerie-qa.js) - auf echten Onepagern bleiben beide immer aus,
  // reduceMotion() verhaelt sich dort exakt wie das fruehere "var reduce".
  var qaForceReducedMotion = false;
  function reduceMotion() {
    return qaForceReducedMotion ||
      document.documentElement.classList.contains("qa-anim-off") ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

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

  /* ---- 1a) Tooltip fuer den Nummern-Fallback (.compact) ----
     Ein einzelnes Element statt ::after pro Link, als direktes Kind von
     #chapter-nav (nicht der ol) - siehe Begruendung im CSS-Kommentar bei
     .nav-tooltip: die ol clippt vertikal mit, sobald sie ihr eigenes
     overflow-x:auto-Sicherheitsnetz braucht. #chapter-nav selbst (position:
     fixed) ist der naechste positionierte Vorfahr, also reicht position:
     absolute hier ohne eigenes position:relative auf #chapter-nav. */
  var tooltip = document.createElement("div");
  tooltip.className = "nav-tooltip";
  nav.appendChild(tooltip);

  function tooltipZeigen(a) {
    if (!nav.classList.contains("compact") || !a || !a.dataset.title) return;
    var navRect = nav.getBoundingClientRect();
    var aRect = a.getBoundingClientRect();
    tooltip.textContent = a.dataset.title;
    tooltip.style.left = (aRect.left - navRect.left + aRect.width / 2) + "px";
    tooltip.style.top = (aRect.bottom - navRect.top + 10) + "px";
    tooltip.classList.add("ist-sichtbar");
  }
  function tooltipVerstecken() { tooltip.classList.remove("ist-sichtbar"); }

  list.addEventListener("mouseover", function (e) {
    var a = e.target.closest ? e.target.closest("a") : null;
    if (a) tooltipZeigen(a);
  });
  list.addEventListener("mouseout", function (e) {
    if (!e.relatedTarget || !list.contains(e.relatedTarget)) tooltipVerstecken();
  });
  // Tastatur-/Screenreader-Nutzung: Tooltip auch bei Fokus zeigen, nicht nur bei Hover.
  list.addEventListener("focusin", function (e) {
    var a = e.target.closest ? e.target.closest("a") : null;
    if (a) tooltipZeigen(a);
  });
  list.addEventListener("focusout", tooltipVerstecken);

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
    tooltipVerstecken();
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
    if (reduceMotion()) { heroEl.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("in"); }); }
    else { stageReveal(heroEl); }
  }
  var revealSections = Array.prototype.slice.call(document.querySelectorAll("section, footer"))
    .filter(function (s) { return s !== heroEl && s.querySelector(".reveal"); });
  if (reduceMotion() || !("IntersectionObserver" in window)) {
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
  // WeakMap statt einfachem Flag: haelt pro Element eine "Generation" fest,
  // damit ein durch Replay neu gestarteter countUp den rAF-Loop eines noch
  // laufenden alten Aufrufs stilllegt, statt dass beide gleichzeitig ins
  // textContent schreiben und der aeltere den Zielwert des neueren ueberschreibt.
  var countUpGen = new WeakMap();
  function countUp(el) {
    var target = parseFloat(el.dataset.countTo);
    var gen = (countUpGen.get(el) || 0) + 1;
    countUpGen.set(el, gen);
    if (reduceMotion()) { el.textContent = target; return; }
    var start = performance.now(), dur = 1200;
    function step(now) {
      if (countUpGen.get(el) !== gen) return; // von neuerem Aufruf ueberholt
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
  // Ausgelagert (statt Inline in der forEach unten), weil Abschnitt 10
  // (replayTimeline) dieselbe Berechnung fuer den Replay-Control braucht -
  // eine Kopie der Formel haette bei einer spaeteren Aenderung leicht
  // auseinanderlaufen koennen.
  function timelineZielProzent(tl) {
    var items = tl.querySelectorAll(".timeline-item");
    if (!items.length) return null;
    var currentIndex = Array.prototype.findIndex.call(items, function (it) {
      return it.classList.contains("is-current");
    });
    if (currentIndex < 0) return null; // kein aktueller Punkt markiert -> keine Linie zeichnen
    return (currentIndex / items.length) * 100 + "%";
  }
  document.querySelectorAll(".timeline").forEach(function (tl) {
    var progress = tl.querySelector(".timeline-progress");
    if (!progress) return;
    var targetPct = timelineZielProzent(tl);
    if (targetPct === null) return;
    if (reduceMotion()) { progress.style.width = targetPct; return; }
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
      track.scrollBy({ left: step * parseInt(btn.dataset.dir, 10), behavior: reduceMotion() ? "auto" : "smooth" });
    });
  });

  /* ---- 9) Stepper: Phasenleiste umschalten ----
     Die Leiste selbst bleibt per position:sticky oben stehen (CSS). Hier nur
     das Umschalten der Panels. Ohne JS bleibt Phase 1 sichtbar - der Inhalt
     geht also nie verloren. */
  // stepperWechseln() ist die gemeinsame Umschalt-Logik fuer Klick UND Replay
  // (Abschnitt 10) - frueher stand das nur im Klick-Handler, Replay haette
  // sonst eine zweite, leicht abweichende Kopie gebraucht.
  function stepperWechseln(leiste, zielTab) {
    var tabs = Array.prototype.slice.call(leiste.querySelectorAll(".stepper-tab"));
    tabs.forEach(function (t) {
      var aktiv = t === zielTab;
      t.setAttribute("aria-selected", aktiv ? "true" : "false");
      var panel = document.getElementById(t.getAttribute("aria-controls"));
      if (!panel) return;
      if (!aktiv) { panel.hidden = true; panel.classList.remove("ist-erscheinend"); return; }
      panel.hidden = false;
      if (reduceMotion()) return;
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
  }
  document.querySelectorAll(".stepper-tabs").forEach(function (leiste) {
    var tabs = Array.prototype.slice.call(leiste.querySelectorAll(".stepper-tab"));
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () { stepperWechseln(leiste, tab); });
    });
  });

  /* ---- 10) QA-Testschnittstelle (nur fuer die Modul-Galerie) ----
     Ziel: Motion-Testing ohne Reload/Hochscrollen/manuelles Triggern (siehe
     modul-namen-generalisierung/Testkonzept). Bewusst NICHT der Versuch, den
     Trigger-Mechanismus (IntersectionObserver vs. sofort) zu vereinheitlichen
     - das wuerde Produktionsverhalten anfassen. Stattdessen: eigene,
     additive "Replay"-Funktionen, die den DOM-Zustand direkt zuruecksetzen
     und die Animation erneut anstossen, unabhaengig davon, wie sie beim
     echten Seitenaufruf ausgeloest wurde.

     root ist i.d.R. die [data-modul]-Sektion in modul-galerie.html. Jede
     replayX-Funktion ist ein No-Op, wenn ihr Effekt im root nicht vorkommt -
     replayModule() kann dadurch generisch auf jede Sektion angewendet
     werden, ohne dass hier pro Modulname unterschieden werden muss.

     Auf echten Onepagern (starter.html, index.html) wird window.DAYONE_QA
     nie aufgerufen - dieser Abschnitt aendert an deren Verhalten nichts,
     er haengt nur zusaetzliche Funktionen an ein globales Objekt. */

  function replayReveal(root) {
    var items = root.querySelectorAll ? root.querySelectorAll(".reveal") : [];
    var rootIstReveal = root.classList && root.classList.contains("reveal");
    if (!items.length && !rootIstReveal) return;
    items.forEach(function (el) { el.classList.remove("in"); el.style.transitionDelay = ""; });
    if (rootIstReveal) { root.classList.remove("in"); root.style.transitionDelay = ""; }
    // Reflow erzwingen, damit der Browser den zurueckgesetzten Zustand erst
    // malt, bevor stageReveal() die .in-Klasse (und damit die Transition)
    // wieder anstoesst - sonst wird der zweite Durchlauf manchmal ohne
    // sichtbaren Uebergang direkt in den Endzustand gesprungen.
    void root.offsetWidth;
    requestAnimationFrame(function () { stageReveal(root); });
  }

  function replayCounters(root) {
    var counters = root.querySelectorAll ? root.querySelectorAll("[data-count-to]") : [];
    if (!counters.length) return;
    counters.forEach(function (el) { el.textContent = "0"; countUp(el); });
  }

  function replayTimeline(root) {
    var timelines = root.classList && root.classList.contains("timeline")
      ? [root] : (root.querySelectorAll ? root.querySelectorAll(".timeline") : []);
    Array.prototype.forEach.call(timelines, function (tl) {
      var progress = tl.querySelector(".timeline-progress");
      if (!progress) return;
      var targetPct = timelineZielProzent(tl);
      if (targetPct === null) return;
      // Breite ohne Transition auf 0 zuruecksetzen, Reflow erzwingen, dann
      // Transition wieder zulassen und den Zielwert setzen - sonst faehrt
      // die Linie nur von der aktuellen Breite ab statt sichtbar neu von 0.
      progress.style.transition = "none";
      progress.style.width = "0%";
      void progress.offsetWidth;
      progress.style.transition = "";
      requestAnimationFrame(function () { progress.style.width = targetPct; });
    });
  }

  function replayCarousel(root) {
    var tracks = root.classList && root.classList.contains("carousel")
      ? [root] : (root.querySelectorAll ? root.querySelectorAll(".carousel") : []);
    Array.prototype.forEach.call(tracks, function (track) {
      track.scrollTo({ left: 0, behavior: reduceMotion() ? "auto" : "smooth" });
    });
  }

  function replayStepper(root) {
    var leisten = root.classList && root.classList.contains("stepper-tabs")
      ? [root] : (root.querySelectorAll ? root.querySelectorAll(".stepper-tabs") : []);
    Array.prototype.forEach.call(leisten, function (leiste) {
      var ersterTab = leiste.querySelector(".stepper-tab");
      if (ersterTab) stepperWechseln(leiste, ersterTab);
    });
  }

  function replayModule(root) {
    if (!root) return;
    replayReveal(root);
    replayCounters(root);
    replayTimeline(root);
    replayCarousel(root);
    replayStepper(root);
  }

  function replayAll() {
    document.querySelectorAll("[data-modul]").forEach(function (root) { replayModule(root); });
  }

  function setAnimationsEnabled(enabled) {
    // Rein CSS-getriebene Wirkung (siehe .qa-anim-off in bausteine/_basis.css /
    // tools/bauen.py QA_CSS): transition/animation:none!important auf allem.
    // reduceMotion() liest dieselbe Klasse zusaetzlich fuer JS-getimte Effekte
    // (countUp, Timeline-Bar), damit "Animations off" beide Wege abdeckt.
    document.documentElement.classList.toggle("qa-anim-off", !enabled);
  }

  function setReducedMotion(on) {
    qaForceReducedMotion = !!on;
  }

  window.DAYONE_QA = {
    replay: replayModule,
    replayAll: replayAll,
    setAnimationsEnabled: setAnimationsEnabled,
    setReducedMotion: setReducedMotion
  };
})();
