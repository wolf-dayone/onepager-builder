# Scroll-Patterns

Neun Muster, destilliert aus den DAYONE-Referenz-Onepagern
(`dayone-weekly-presentations`, `ny-pitch-three`, `cupra-pitch`).

**Grundregel:** Ein Onepager verträgt **zwei bis drei** dieser Muster, nicht neun.
Jeder Effekt muss etwas erklären. Bewegung ohne Aussage macht die Seite unruhig und
kostet Ladezeit.

**Barrierefreiheit:** Jeder Effekt braucht einen `prefers-reduced-motion`-Zweig. Im
Template ist das global gelöst — bei eigenen Effekten mitziehen.

---

## 1. Reveal beim Eintritt ins Viewport
Der Standard. Elemente faden leicht nach oben ein.
Im Template: Klasse `reveal` auf jedes Element, das einfliegen soll. Fertig.

```html
<div class="reveal">…</div>
```

Sparsam einsetzen: nicht jedes einzelne Listenelement, sondern Blöcke.

---

## 2. Sticky-Spalte (das wichtigste Muster)
Linke Spalte bleibt stehen, rechte scrollt vorbei. Nutzt aus, dass ein Browser kein
Slide-Format ist — die Leitfrage bleibt sichtbar, während man die Belege durchgeht.
Modul: `sticky-nummernliste`.

```css
.sticky-list{display:grid;grid-template-columns:5fr 7fr;gap:96px;align-items:start}
.sticky-list .left{position:sticky;top:140px}
@media(max-width:900px){
  .sticky-list{grid-template-columns:1fr}
  .sticky-list .left{position:static}   /* auf Mobile nie sticky */
}
```

`top` muss größer sein als die Höhe der Kapitel-Nav (72 px), sonst verschwindet der
Block darunter. 140 px ist ein guter Wert.

---

## 3. Sticky Scrollspy (Phasen-Navigation)
Wie 2, aber die sticky Leiste zeigt Phasen und markiert die aktive.
Modul: `lifecycle-stepper`. Referenz: ny-pitch-three.

```js
var obs = new IntersectionObserver(function(entries){
  entries.forEach(function(e){
    if(!e.isIntersecting) return;
    document.querySelectorAll('.phase').forEach(function(p){p.classList.remove('active')});
    document.querySelector('[data-phase="'+e.target.dataset.phase+'"]').classList.add('active');
  });
}, {rootMargin:'-45% 0px -50% 0px'});
document.querySelectorAll('[data-phase-section]').forEach(function(s){obs.observe(s)});
```

Das `rootMargin` mit -45 %/-50 % bedeutet: aktiv wird, was in der Bildschirmmitte steht.
Das fühlt sich richtiger an als "sobald es oben reinkommt".

---

## 4. Kapitel-Navigation
Erscheint, sobald der Hero (oder die Agenda) durch ist. Im Template fertig implementiert:
Sektionen mit `data-chapter` und `data-chapter-title` markieren, die Nav baut sich selbst.

```html
<section id="kapitel-01" data-chapter="01" data-chapter-title="Ausgangslage">
```

Der Überlauf-Fallback (nur Nummern + Tooltip) schaltet sich per Breitenmessung selbst ein.

---

## 5. Count-Up bei Kennzahlen
Zahlen zählen hoch, sobald sie sichtbar werden. Modul: `kennzahlen-grid`.
Im Template: `data-count-to` setzen.

```html
<div class="value" data-count-to="34">0</div>
```

Nur für ganze Zahlen gedacht. Bei "+27,7 %" oder "60–80 %" den Wert statisch lassen —
ein hochzählender Dezimalwert wirkt unruhig statt beeindruckend.

---

## 6. Horizontales Karussell
Karten laufen über den rechten Rand hinaus, Pfeile springen je eine Karte weiter.
Modul: `takeaways-liste`. Scroll-Snap macht es auf Touch von selbst richtig.

```css
.carousel{overflow-x:auto;scroll-snap-type:x mandatory;display:flex;gap:32px}
.carousel>.card{flex:0 0 420px;scroll-snap-align:start}
```

Wichtig: Die Sektion bekommt `padding-inline:0`, damit der Track wirklich bis an den
Rand läuft. Ohne das wirkt es wie ein Fehler statt wie eine Einladung.

---

## 7. Pinned Section (Scroll-Scrubbing)
Die aufwendigste Technik: Eine Sektion bleibt fixiert, während der Inhalt abhängig von
der Scroll-Position wechselt. Basis für Zahlen-Morph, Logo-Highlight und Zoom-Through —
alle drei sind **Konfigurationen desselben Musters**, nicht drei Effekte.

```css
.pinned{height:300vh}                 /* Scroll-Distanz */
.pinned .stage{position:sticky;top:0;height:100vh;display:grid;place-items:center}
```

```js
var pin = document.querySelector('.pinned');
window.addEventListener('scroll', function(){
  var r = pin.getBoundingClientRect();
  var p = Math.min(Math.max(-r.top / (pin.offsetHeight - innerHeight), 0), 1); // 0…1
  // p auf den gewünschten Zustand mappen
}, {passive:true});
```

**Vor dem Einbau abwägen:** Pinned Sections schlucken viel Scroll-Weg für wenig Inhalt
und sind auf Mobile oft mehr Last als Gewinn. Nur einsetzen, wenn der Effekt die Aussage
trägt — etwa bei einem Zoom-Through vom Schema zum echten Screenshot.
Ab `max-width: 900px` auf eine statische Darstellung zurückfallen.

---

## 8. Sequenzielle Hervorhebung im Raster
Einzelne Elemente eines Grids werden nacheinander hervorgehoben (aktiv 100 %, Rest 20 %).
Modul: `logo-wand`. Basiert auf 7.

---

## 9. Zoom-Through
Ein abstraktes Schaubild vergrößert sich beim Scrollen in einen konkreten Screenshot.
Modul: `case-study-diagrammkarte`. Basiert auf 7, gesteuert über `transform: scale()`.
Referenz: cupra-pitch.

---

## Performance

- Scroll-Listener immer mit `{passive:true}`.
- Für alles, was nur "sichtbar ja/nein" braucht: `IntersectionObserver`, nicht `scroll`.
- Bei Scroll-Scrubbing nur `transform` und `opacity` animieren — alles andere
  (width, top, margin) löst Layout-Neuberechnung aus und ruckelt.
- Bilder: `loading="lazy"` außer beim Hero-Bild.
