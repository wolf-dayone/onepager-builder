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
  var STAGGER_MS = 130, STAGGER_MAX_MS = 900;
  function stageReveal(container) {
    var items = container.classList && container.classList.contains("reveal")
      ? [container] : container.querySelectorAll(".reveal");
    // Einzelne Sektionen duerfen ueber data-stagger="<ms>" einen engeren Takt
    // erzwingen (z. B. Agenda: gleiche Dauer je Punkt, aber schneller
    // hintereinander - Video-Feedback 2026-09-17). Fehlt das Attribut, gilt
    // der Standardtakt STAGGER_MS.
    var takt = STAGGER_MS;
    if (container.dataset && container.dataset.stagger) {
      var eigen = parseInt(container.dataset.stagger, 10);
      if (!isNaN(eigen)) takt = eigen;
    }
    items.forEach(function (el, i) {
      // --reveal-delay statt inline transition-delay: Pseudo-Elemente (die
      // Linien in .linie-oben/.raster-col/.stat) erben die Property und laufen
      // dadurch synchron mit ihrem Element ein. Siehe _basis.css, Reveal-Block.
      el.style.setProperty("--reveal-delay", Math.min(i * takt, STAGGER_MAX_MS) + "ms");
      el.classList.add("in");
    });
  }
  /* Auch der Hero laeuft ueber denselben Beobachter statt sofort beim Laden:
     auf einem echten Onepager steht er ohnehin im Viewport und startet damit
     praktisch gleichzeitig - in der Galerie (und bei jedem Direktsprung per
     Anker) sieht man ihn dagegen genau dann, wenn man ihn erreicht. Vorher
     spielte er blind beim Laden, unabhaengig davon, wo man gerade steht
     (Feedback 2026-09-17: "nur beim Reinscrollen, nicht initial fuer alle"). */
  var heroEl = document.getElementById("hero");
  var revealSections = Array.prototype.slice.call(
      document.querySelectorAll("section, header.hero, footer"))
    .filter(function (s) { return s.querySelector(".reveal") || s.classList.contains("reveal"); });
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
  // Der Zaehler startet um genau die Staffel-Verzoegerung seiner eigenen
  // .reveal-Huelle versetzt: er laeuft dadurch WAEHREND die Kennzahl hochkommt
  // und die Linie einlaeuft, nicht schon vorher im noch unsichtbaren Element
  // (Feedback 2026-09-17).
  function revealVerzoegerung(el) {
    var huelle = el.closest ? el.closest(".reveal") : null;
    if (!huelle) return 0;
    var wert = parseFloat(huelle.style.getPropertyValue("--reveal-delay"));
    return isNaN(wert) ? 0 : wert;
  }
  if ("IntersectionObserver" in window) {
    var cObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        cObs.unobserve(e.target);
        var warten = revealVerzoegerung(e.target);
        if (warten > 0) setTimeout(function () { countUp(e.target); }, warten);
        else countUp(e.target);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cObs.observe(el); });
  } else {
    counters.forEach(function (el) { el.textContent = el.dataset.countTo; });
  }

  /* ---- 6b) Chart-Slide: Balken wachsen nacheinander von unten, Zaehler laeuft
     synchron mit (Ernst, 2026-09-xx) - erst NACHDEM das leere Diagramm (Achsen,
     Gitterlinien, siehe .chart-body.reveal) fertig eingeblendet ist, nicht
     gleichzeitig damit. Reagiert deshalb auf transitionend von .chart-body
     statt auf denselben IntersectionObserver wie stageReveal(). */
  function growChart(chart) {
    var balken = Array.prototype.slice.call(chart.querySelectorAll(".chart-balken"));
    if (!balken.length) return;
    if (reduceMotion()) {
      balken.forEach(function (b) {
        b.style.setProperty("--wert", b.dataset.wert);
        b.classList.add("ist-gewachsen");
        var wert = b.querySelector(".chart-wert");
        if (wert) wert.textContent = wert.dataset.countTo;
      });
      demoBetonen(chart, 0);
      return;
    }
    var STAGGER = 180;
    balken.forEach(function (b, i) {
      setTimeout(function () {
        b.style.setProperty("--wert", b.dataset.wert);
        // Blendet den Wert ein (CSS .ist-gewachsen .chart-wert) - der Zaehler
        // laeuft dann sichtbar mit der Saeule nach oben statt davor.
        b.classList.add("ist-gewachsen");
        var wert = b.querySelector(".chart-wert");
        if (wert) countUp(wert);
      }, i * STAGGER);
    });
    demoBetonen(chart, balken.length * STAGGER + 900);
  }

  // Einmalige, kurze Simulation von Hover/Tap auf der dafuer markierten Saeule
  // (data-demo-hover) - zeigt vor, was echtes Hover/Tap ohnehin ausloest (siehe
  // .chart-balken:hover in bausteine/04-daten-02-chart-slide.html), fuer alle,
  // die nie selbst hovern/tippen. KEIN Dauerzustand, deshalb nach kurzer Zeit
  // wieder entfernt.
  function demoBetonen(chart, verzoegerung) {
    var ziel = chart.querySelector('[data-demo-hover="true"]');
    if (!ziel || reduceMotion()) return;
    setTimeout(function () {
      ziel.classList.add("ist-betont");
      setTimeout(function () { ziel.classList.remove("ist-betont"); }, 1400);
    }, verzoegerung);
  }

  // Wartet auf das Ende von .chart-body's EIGENER reveal-Transition (Opacity/
  // Transform, siehe .reveal in _basis.css), bevor der uebergebene Callback
  // laeuft - wiederverwendet sowohl beim ersten Laden als auch bei replayChart(),
  // damit die Balken in beiden Faellen erst NACH dem leeren Diagramm anwachsen.
  function chartWennSichtbar(chart, dann) {
    if (reduceMotion() || !("IntersectionObserver" in window)) { dann(); return; }
    chart.addEventListener("transitionend", function auf_fertig(e) {
      if (e.target !== chart) return; // nur .chart-body selbst, nicht durchgereichte Kind-Transitions
      chart.removeEventListener("transitionend", auf_fertig);
      dann();
    });
  }

  document.querySelectorAll(".chart-body").forEach(function (chart) {
    chartWennSichtbar(chart, function () { growChart(chart); });
  });

  // Tippen simuliert Hover auf Touch-Geraeten, wo :hover unzuverlaessig ist -
  // eigener, kurzer "betont"-Zustand statt auf CSS-:hover-Emulation zu hoffen.
  document.querySelectorAll(".chart-balken").forEach(function (b) {
    b.addEventListener("touchstart", function () {
      b.classList.add("ist-betont");
      setTimeout(function () { b.classList.remove("ist-betont"); }, 1200);
    }, { passive: true });
  });

  /* ---- 7) Roadmap-Timeline: chronologisch aufgebaute Zeitachse ----
     Reihenfolge (Figma node 9-9, Feedback 2026-09-17):
       Punkt skaliert ein -> sein Datum/Meilenstein blendet auf ->
       die Linie waechst aus dem Punkt heraus zum naechsten -> von vorn.
     Der aktuelle Punkt pulsiert danach dauerhaft weiter, die Strecke zu
     kuenftigen Meilensteinen wird gestrichelt und grau gezogen.

     Die Segmentgeometrie kommt aus den echten Dot-Positionen statt aus einer
     Prozentformel: sie stimmt damit bei jeder Anzahl Meilensteine, bei
     unterschiedlich breiten Beschriftungen und nach jedem Resize. */
  var TL_DOT = 300,     // Punkt setzt sich
      TL_TEXT = 150,    // danach Beschriftung
      TL_LINIE = 430;   // danach Linie zum naechsten Punkt

  function timelineWaagerecht(tl) {
    // Mobile stapelt die Punkte untereinander (siehe Media-Query im Modul) -
    // dann traegt die waagerechte Linienebene nichts und bleibt leer.
    var items = tl.querySelectorAll(".timeline-item");
    if (items.length < 2) return false;
    return items[0].offsetTop === items[1].offsetTop;
  }

  // Legt pro Luecke zwischen zwei Punkten ein Segment an und setzt es exakt
  // von Dot-Mitte zu Dot-Mitte. Laeuft auch bei Resize erneut.
  function timelineSegmenteBauen(tl) {
    var ebene = tl.querySelector(".timeline-linien");
    if (!ebene) return [];
    var items = Array.prototype.slice.call(tl.querySelectorAll(".timeline-item"));
    if (items.length < 2 || !timelineWaagerecht(tl)) { ebene.innerHTML = ""; return []; }
    var basis = ebene.getBoundingClientRect();
    var mitten = items.map(function (it) {
      var dot = it.querySelector(".timeline-dot");
      var r = (dot || it).getBoundingClientRect();
      return r.left + r.width / 2 - basis.left;
    });
    var vorhandene = ebene.querySelectorAll(".timeline-seg");
    if (vorhandene.length !== items.length - 1) {
      ebene.innerHTML = "";
      for (var k = 0; k < items.length - 1; k++) {
        ebene.appendChild(document.createElement("span")).className = "timeline-seg";
      }
    }
    var segmente = Array.prototype.slice.call(ebene.querySelectorAll(".timeline-seg"));
    segmente.forEach(function (seg, i) {
      seg.style.left = mitten[i] + "px";
      // Ein Segment gilt als Ausblick, sobald der Punkt an seinem RECHTEN Ende
      // noch bevorsteht - dann gestrichelt/grau statt durchgezogen rot.
      seg.classList.toggle("ist-ausblick", items[i + 1].classList.contains("ist-ausblick"));
      seg.dataset.ziel = Math.max(0, mitten[i + 1] - mitten[i]);
      // Bereits ausgefahrene Segmente muessen beim Resize mitwandern.
      if (seg.dataset.offen === "1") seg.style.width = seg.dataset.ziel + "px";
    });
    return segmente;
  }

  function timelineZuruecksetzen(tl) {
    tl.querySelectorAll(".timeline-item").forEach(function (it) {
      it.classList.remove("ist-beschriftet");
      var dot = it.querySelector(".timeline-dot");
      if (dot) dot.classList.remove("ist-da", "ist-aktuell");
    });
    tl.querySelectorAll(".timeline-seg").forEach(function (seg) {
      seg.style.transition = "none";
      seg.style.width = "0px";
      seg.dataset.offen = "0";
      void seg.offsetWidth;
      seg.style.transition = "";
    });
  }

  function timelineAbspielen(tl) {
    var items = Array.prototype.slice.call(tl.querySelectorAll(".timeline-item"));
    if (!items.length) return;
    var segmente = timelineSegmenteBauen(tl);

    function punktZeigen(i) {
      var it = items[i];
      var dot = it.querySelector(".timeline-dot");
      if (dot) {
        dot.classList.add("ist-da");
        // Der Dauerpuls haengt am Dot, nicht am Item: er darf erst starten,
        // wenn der Punkt wirklich gesetzt ist.
        if (it.classList.contains("ist-aktuell")) dot.classList.add("ist-aktuell");
      }
      it.classList.add("ist-beschriftet");
    }

    if (reduceMotion()) {
      items.forEach(function (_, i) { punktZeigen(i); });
      segmente.forEach(function (seg) { seg.style.width = seg.dataset.ziel + "px"; seg.dataset.offen = "1"; });
      return;
    }

    var t = 0;
    items.forEach(function (_, i) {
      setTimeout(function () { punktZeigen(i); }, t);
      t += TL_DOT + TL_TEXT;
      var seg = segmente[i];
      if (seg) {
        setTimeout(function () {
          seg.style.width = seg.dataset.ziel + "px";
          seg.dataset.offen = "1";
        }, t);
        t += TL_LINIE;
      }
    });
  }

  document.querySelectorAll(".timeline").forEach(function (tl) {
    timelineSegmenteBauen(tl);
    var gelaufen = false;
    function los() { if (gelaufen) return; gelaufen = true; timelineAbspielen(tl); }
    if (reduceMotion() || !("IntersectionObserver" in window)) { los(); }
    else {
      new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { los(); obs.unobserve(e.target); }
        });
      }, { rootMargin: "-40% 0px -40% 0px", threshold: 0 }).observe(tl);
    }
    window.addEventListener("resize", function () { timelineSegmenteBauen(tl); });
  });

  /* ---- 7b) Roadmap Zoom-In: Balken<->Meilenstein-Kopplung ----
     Hover/Fokus auf einem .gantt-balken hebt den Meilenstein mit demselben
     data-verweis rechts hervor - nicht mehr initial fest zugeordnet
     (.ist-aktuell), sondern ein reiner Hover-Zustand (Video-Feedback
     2026-09-17). Touch simuliert denselben Zustand kurzzeitig, wie beim
     Chart-Slide (Abschnitt 6b). */
  // Balken fahren nacheinander von links auf, sobald das Gantt sichtbar ist -
  // dieselbe Leserichtung wie beim Fluss-Diagramm und der Zeitachse.
  function ganttAusfahren(gantt) {
    var balken = Array.prototype.slice.call(gantt.querySelectorAll(".gantt-balken"));
    if (reduceMotion()) { balken.forEach(function (b) { b.classList.add("ist-da"); }); return; }
    balken.forEach(function (b, i) {
      setTimeout(function () { b.classList.add("ist-da"); }, i * 180);
    });
  }
  document.querySelectorAll(".gantt").forEach(function (gantt) {
    if (reduceMotion() || !("IntersectionObserver" in window)) { ganttAusfahren(gantt); return; }
    new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { ganttAusfahren(gantt); obs.unobserve(e.target); }
      });
    }, { rootMargin: "-35% 0px -35% 0px", threshold: 0 }).observe(gantt);
  });

  document.querySelectorAll(".roadmap-zoom").forEach(function (zoom) {
    var balken = zoom.querySelectorAll(".gantt-balken");
    function setzen(ref, an) {
      var ziel = zoom.querySelector('.zoom-meilenstein[data-verweis="' + ref + '"]');
      if (ziel) ziel.classList.toggle("ist-hervorgehoben", an);
    }
    balken.forEach(function (b) {
      var ref = b.dataset.verweis;
      b.addEventListener("mouseenter", function () { setzen(ref, true); });
      b.addEventListener("mouseleave", function () { setzen(ref, false); });
      b.addEventListener("focus", function () { setzen(ref, true); });
      b.addEventListener("blur", function () { setzen(ref, false); });
      b.addEventListener("touchstart", function () {
        b.classList.add("ist-betont"); setzen(ref, true);
        setTimeout(function () { b.classList.remove("ist-betont"); setzen(ref, false); }, 1200);
      }, { passive: true });
    });
  });

  /* ---- 7c) Zitat: Schreibmaschinen-Effekt ----
     Der Satz wird Zeichen fuer Zeichen gesetzt, die Quelle blendet erst auf,
     wenn er fertig ist (Feedback 2026-09-17). Der volle Satz steht als
     unsichtbarer Platzhalter im DOM und haelt die Hoehe - dadurch springt
     weder das Layout noch die Sektionsmitte, und Screenreader lesen den
     vollstaendigen Text (die getippte Schicht ist aria-hidden). */
  var TIPP_MS = 26; // Zeichenabstand; ~40 Anschlaege/Sekunde, ruhig lesbar
  function zitatTippen(block) {
    var platzhalter = block.querySelector(".platzhalter");
    var ziel = block.querySelector(".getippt");
    var quelle = block.parentNode ? block.parentNode.querySelector("cite") : null;
    if (!platzhalter || !ziel) return;
    var text = platzhalter.textContent;
    if (reduceMotion()) {
      ziel.textContent = text;
      if (quelle) quelle.classList.add("ist-da");
      return;
    }
    ziel.textContent = "";
    block.classList.add("ist-am-tippen");
    var i = 0, letzte = 0;
    // Ueber rAF statt setInterval: der Text laeuft dadurch im Takt der
    // Bildwiederholrate und stockt nicht, wenn der Tab kurz ausgelastet ist.
    function schritt(jetzt) {
      if (!letzte) letzte = jetzt;
      if (jetzt - letzte >= TIPP_MS) {
        letzte = jetzt;
        i += 1;
        ziel.textContent = text.slice(0, i);
      }
      if (i < text.length) { requestAnimationFrame(schritt); }
      else {
        block.classList.remove("ist-am-tippen");
        if (quelle) quelle.classList.add("ist-da");
      }
    }
    requestAnimationFrame(schritt);
  }
  document.querySelectorAll(".quote-typo").forEach(function (block) {
    // Getippt wird erst, wenn das Zitat selbst eingeblendet ist.
    if (reduceMotion() || !("IntersectionObserver" in window)) { zitatTippen(block); return; }
    var gestartet = false;
    new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (!e.isIntersecting || gestartet) return;
        gestartet = true;
        obs.unobserve(e.target);
        setTimeout(function () { zitatTippen(block); }, 450);
      });
    }, { rootMargin: "-40% 0px -40% 0px", threshold: 0 }).observe(block);
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
    var alle = rootIstReveal ? [root].concat(Array.prototype.slice.call(items)) : Array.prototype.slice.call(items);
    if (!alle.length) return;
    // .reveal traegt seine transition IMMER (auch ohne .in), nicht nur beim
    // Reinschalten - ein blosses classList.remove("in") haette also selbst
    // schon sichtbar rueckwaerts animiert (Ausblenden+Absinken), statt den
    // Ausgangszustand sauber und unsichtbar wiederherzustellen. Deshalb hier
    // dasselbe Muster wie bei replayTimeline: Transition kurz hart abschalten,
    // Reflow erzwingen, erst dann wieder freigeben.
    alle.forEach(function (el) {
      el.style.transition = "none";
      el.classList.remove("in");
      el.style.transitionDelay = "";
      el.style.removeProperty("--reveal-delay");
    });
    void root.offsetWidth;
    alle.forEach(function (el) { el.style.transition = ""; });
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
      timelineZuruecksetzen(tl);
      requestAnimationFrame(function () { timelineAbspielen(tl); });
    });
  }

  function replayGantt(root) {
    var gantts = root.classList && root.classList.contains("gantt")
      ? [root] : (root.querySelectorAll ? root.querySelectorAll(".gantt") : []);
    Array.prototype.forEach.call(gantts, function (gantt) {
      gantt.querySelectorAll(".gantt-balken").forEach(function (b) {
        b.style.transition = "none";
        b.classList.remove("ist-da", "ist-betont");
        void b.offsetWidth;
        b.style.transition = "";
      });
      requestAnimationFrame(function () { ganttAusfahren(gantt); });
    });
  }

  function replayZitat(root) {
    var bloecke = root.classList && root.classList.contains("quote-typo")
      ? [root] : (root.querySelectorAll ? root.querySelectorAll(".quote-typo") : []);
    Array.prototype.forEach.call(bloecke, function (block) {
      var quelle = block.parentNode ? block.parentNode.querySelector("cite") : null;
      if (quelle) quelle.classList.remove("ist-da");
      zitatTippen(block);
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

  function replayChart(root) {
    var charts = root.classList && root.classList.contains("chart-body")
      ? [root] : (root.querySelectorAll ? root.querySelectorAll(".chart-body") : []);
    Array.prototype.forEach.call(charts, function (chart) {
      chart.querySelectorAll(".chart-balken").forEach(function (b) {
        b.classList.remove("ist-betont", "ist-gewachsen");
        b.style.setProperty("--wert", 0);
        var wert = b.querySelector(".chart-wert");
        if (wert) { wert.textContent = "0"; }
      });
      // replayReveal() (weiter oben in replayModule()) stoesst .chart-body's
      // eigene reveal-Transition gerade erst neu an - erst wenn die
      // durchgelaufen ist, sollen die Balken wachsen, exakt wie beim ersten
      // Laden der Seite.
      chartWennSichtbar(chart, function () { growChart(chart); });
    });
  }

  function replayModule(root) {
    if (!root) return;
    replayReveal(root);
    replayCounters(root);
    replayTimeline(root);
    replayCarousel(root);
    replayStepper(root);
    replayChart(root);
    replayGantt(root);
    replayZitat(root);
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
