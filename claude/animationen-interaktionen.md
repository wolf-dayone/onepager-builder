# Animationen/Interaktionen schärfen — Fortschritt

Prozess (2026-09-17 mit Ernst abgestimmt): kleine Durchgänge, jeweils 1-3
Muster aus `referenzen/scroll-patterns.md`, danach in EINEM konsolidierten
Playwright-Lauf verifizieren statt nach jeder Detailänderung neu zu testen.
Figma-Motion-Daten (`get_motion_context`) nur abfragen, wenn eine Interaktion
tatsächlich als Figma-Prototyp/Smart-Animate hinterlegt ist — bei rein
textuell beschriebenem Verhalten (wie beim Stepper) bringt der Call nichts.

## Durchgang 1: Stepper (`02 Struktur/03 stepper`)

**Befund vor dem Fix:** Die Figma-Beschreibung verlangt "Sticky Scrollspy"
(Panel wechselt beim Scrollen, nicht per Klick), und genau dieses Muster ist
in `referenzen/scroll-patterns.md` Abschnitt 3 mit fertigem
`IntersectionObserver`-Code dokumentiert — im Baustein selbst aber nie
umgesetzt. Stattdessen: reine Klick-Tabs mit hartem `hidden`-Umschalten.

**Entscheidung (Ernst):** Klick-Tabs beibehalten (kein Scrollspy-Umbau, das
wäre ein größerer Struktur-Eingriff mit längerer Section), aber den
Panel-Wechsel visuell schärfen — sanftes Fade+Slide beim Erscheinen des neuen
Panels statt hartem Cut.

**Umsetzung:**
- `bausteine/02-struktur-03-stepper.html`: `.stepper-panel` bekommt eine
  Opacity/Transform-Transition (.35s), Startzustand über die Klasse
  `.ist-erscheinend` (opacity 0, translateY 8px).
- `bausteine/_basis.js` (Abschnitt 9, Stepper): beim Tab-Klick wird das neue
  Panel sichtbar gemacht, bekommt kurz `.ist-erscheinend`, das per doppeltem
  `requestAnimationFrame` wieder entfernt wird, damit der Browser den
  Startzustand erst malt, bevor die Transition losläuft. Bei
  `prefers-reduced-motion: reduce` bleibt es beim alten harten Umschalten
  (kein `classList.add`).

**Bug gefunden + gefixt (via Playwright, nicht durch Code-Lesen sichtbar):**
Jedes `.reveal`-Element bekommt beim ersten Sichtbarwerden der Section ein
gestaffeltes `transition-delay` als Inline-Style (`stageReveal`-Funktion,
Stagger-Logik). Dieser Inline-Wert bleibt am Element hängen und hat höhere
Spezifität als jede Klassen-Regel — er verzögerte dadurch auch den
Tab-Wechsel-Übergang um denselben (zufälligen, positionsabhängigen) Betrag,
bei Panel 2 z. B. zusätzliche ~440ms Verzögerung, bevor die eigentliche
0.35s-Transition überhaupt startete. Fix: `panel.style.transitionDelay =
"0ms"` wird beim Tab-Klick explizit gesetzt, bevor die neue Transition
losläuft.

**Verifiziert:** `tools/pruefen.py` (beide Testseiten sauber), `selbsttest.py`
(18/18), sowie ein konsolidierter Playwright-Lauf: normaler Modus (Panel
erreicht opacity 1 nach der Transition, alte Klasse korrekt entfernt, vorheriges
Panel korrekt wieder hidden) und `prefers-reduced-motion: reduce` (keine
Animationsklasse gesetzt, sofortiger Wechsel wie zuvor).

## Noch offen / nächste Kandidaten

Aus `referenzen/scroll-patterns.md`: Sticky-Spalte, Kapitel-Navigation,
Count-Up, horizontales Karussell, Pinned Section, sequenzielle Hervorhebung,
Zoom-Through — noch nicht in diesem Rahmen geprüft. Nächster Durchgang nach
Ernsts Priorität.

## Vereinbarter Test-Workflow (2026-09-17, neuer Chat)

Gruppierung nach Animationsverhalten statt nach Themen-Ordner, weil Changes
an einem Muster meist eine ganze Gruppe betreffen:

- **Gruppe A — Sticky-Muster:** Sticky-Spalte (`sticky-nummernliste`).
- **Gruppe B — Kapitel-Navigation:** laut Doku "im Template fertig
  implementiert" — vermutlich nur der Überlauf-Fallback (Tooltip bei zu
  vielen Kapiteln) als Kandidat zum Schärfen, kein Neubau.
- **Gruppe C — Count-Up:** nur `kennzahlen-grid`.
- **Gruppe D — Karussell:** nur das Karussell-Modul (ehem.
  `takeaways-liste`, Name ggf. seit der Generalisierung anders — im Repo
  nachschlagen).
- **Gruppe E — Pinned-Section-Familie:** Pinned Section + sequenzielle
  Hervorhebung (`logo-wand`) + Zoom-Through (`diagrammkarte`) — teilen sich
  denselben Scroll-Scrubbing-Mechanismus laut `scroll-patterns.md` Abschnitt
  7-9, daher gemeinsam behandeln (ein Grundgerüst, eine
  Playwright-Verifikation für alle drei).

Reihenfolge: C, D zuerst (klein/isoliert), dann A, B, zuletzt E (größter
Umbau, profitiert am meisten von den Lerneffekten aus den vorherigen Gruppen).

**Preview/Review-Workflow:** Baustein(e) mit Platzhalter-Content aus
`data/descriptions/*.txt` als eigenständiges, gruppiertes HTML
zusammenstellen, als Claude Artifact veröffentlichen (Achtung: Artifact-
Dateien dürfen kein eigenes doctype/html/head/body haben — der Builder-
Output aus `tools/bauen.py` muss vorher extrahiert werden). Ernst kommentiert
im Artifact, was verändert werden soll. Wichtig: neue Kommentare kommen
nicht automatisch an — Ernst muss explizit bitten nachzuschauen, daher
mehrere Kommentare sammeln statt einzeln reagieren.

**Changes-Regel:** reine Text-/Platzhalter-Änderungen nur im Repo
(`/bausteine`), Struktur-/Layout-/Verhaltensänderungen zusätzlich in Figma
synchronisieren (Figma ist Source of Truth bei Divergenz). Nach jeder
Code-Änderung: `tools/katalog_bauen.py` → `tools/bauen.py` →
`tools/pruefen.py` (starter.html + modul-galerie.html) →
`tools/selbsttest.py`, plus bei Interaktions-Changes ein konsolidierter
Playwright-Lauf statt Einzeltests.

Git-Push funktioniert aus der Sandbox/Device-Bridge nicht (keine
Credentials) — Commits lokal machen, Ernst pusht selbst.
