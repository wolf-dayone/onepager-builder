<!-- GENERIERT von tools/katalog_bauen.py - nicht von Hand bearbeiten. -->
<!-- Quelle: Figma-Component-Descriptions. Aenderungen dort vornehmen. -->

# Modul-Katalog

34 Bausteine aus der Figma-Datei **DAYONE | AI-ready slides**, Seite *Module*.
Die Namen hier sind **exakt** die Figma-Layernamen — wer im Onepager ein Modul
nennt, findet es in Figma unter demselben Namen.

Datei: `https://www.figma.com/design/1CL62lpdnyiFW98MFs1GPS/DAYONE-%7C-AI-ready-slides` · Stand: 2026-09-15

## Farbe gilt für alle Module

Jedes Modul ist **hell (Sand/100) oder dunkel (Gray/900), frei wählbar**.
Ein Farbwechsel markiert einen neuen Sinnabschnitt; gleiche Farbe hält
zusammengehörige Abschnitte optisch als Einheit. Es gibt **keine feste**
**Zuordnung** von Farbe zu Modul oder Kapiteltyp — Notizen wie „· dunkel“
an einzelnen Modulen sind falsch und wurden entfernt.

## Mindesthöhe gilt für alle Module

Jedes Modul ist **mindestens eine Bildschirmhöhe groß** (Code: `100svh`;
in Figma stellvertretend als 960-px-Rahmen dargestellt — der Rahmen steht
für „Viewport“, nicht für einen festen Pixelwert). **Mit mehr Inhalt darf**
**ein Modul wachsen**, verkürzt werden darf es nicht. Eine eigene, kleinere
`min-height` auf Sektionsebene ist nur zulässig, wenn hier ausdrücklich als
Ausnahme dokumentiert — aktuell gibt es **keine** Ausnahme.

## Eyebrow ist optional

Die Eyebrow-Zeile (`[NN] — [Kapitelname]`) markiert ein neues, **in der**
**Kapitel-Nav verlinktes Kapitel** — nicht mehr und nicht weniger. Mehrere
Module (u. a. `big-statement`, `grossbild`, `bild-kennzahlenliste`,
`headline-liste`, `device-mockup`, `diagrammkarte`,
`bild-intro`, `qr-tool-verweis`) tragen in Figma eine eigene, aber
**optionale** Eyebrow für den Fall, dass sie ein Kapitel eröffnen. Wird ein
solches Modul **innerhalb** eines Kapitels eingesetzt (als Beat, nicht als
Kapitelstart), gehört die Eyebrow-Zeile **gelöscht** — pro Kapitel trägt nur
die jeweils erste Sektion den Kapitelmarker (siehe „KEIN DOPPELTER
KAPITELMARKER“ weiter unten). Eröffnet das Modul dagegen selbst ein Kapitel,
braucht es zusätzlich `data-chapter`/`data-chapter-title`/`id` auf der
Sektion, sonst bleibt die Nummer unverlinkt und `tools/bauen.py` numeriert
sie nicht (numeriert wird nur, wenn `data-chapter="[NN]"` vorkommt).

> **Lücke in der Quelle:** `01 Einstieg/02 agenda` hat in Figma keine Zweck-/Füllregeln. Bis das nachgetragen ist,
> gibt es für dieses Modul nichts zu prüfen.

---

## 00 Elemente

### `00 Elemente/01 kapitel-nav`

<sub>Figma-Node `56:58`</sub>

**ZWECK** — Horizontale Kapitel-Navigation am oberen Bildschirmrand. Gibt beim Scrollen jederzeit Orientierung, welches Kapitel gerade läuft.

**VERHALTEN**

- Erscheint erst, wenn der Hero aus dem Viewport gescrollt ist.
- Wird eine Agenda verwendet, erscheint sie stattdessen erst nach der Agenda.
- Danach sticky am oberen Rand (position: sticky, top: 0).
- Aktives Kapitel hervorgehoben, übrige auf 55 % Deckkraft.
- Klick scrollt smooth zum jeweiligen Abschnitt.
- Logo + Präsentationstitel sind ebenfalls klickbar und scrollen zurück zum Hero.

**VARIANTEN** — Prioritäts-Kaskade, nicht drei feste Breakpoints. Ausgelöst durch verfügbaren Platz relativ zum Inhalt (Kapitelanzahl, Titellängen, Präsentationstitel-Länge), nicht durch eine Viewport-Breite. Die drei Frames (Desktop/Tablet/Mobile) sind Referenzbilder für typische Fälle — bei sehr langem Präsentationstitel kann Stufe 2 schon bei 1200px greifen, bei kurzem Titel und wenigen Kapiteln bleibt Stufe 1 auch auf einem Tablet erhalten. Reihenfolge, in der Elemente weichen, sobald der Kapitel-Track nicht mehr passt: 1. Voller Zustand — Logo + Präsentationstitel + Kapitel mit vollem Titel (Anzeige=Titel). 2. Präsentationstitel ausblenden — Kapitel-Navigation ist wichtiger für die Orientierung. 3. Kapitel auf Nummern + Tooltip reduzieren (Anzeige=Nummern). 4. Logo auf Icon ohne Schriftzug reduzieren (Anzeige=Mobile) — letzte Stufe, wenn selbst die Nummern-Reihe kaum noch Platz hat. Jede Stufe bleibt bestehen, bis wieder Platz da ist — kein Zurückspringen zwischen Stufen bei kleinen Schwankungen (Hysterese).

**FÜLLEN**

- Kapitelnummern und -titel müssen mit den Kapitelmarkern (Eyebrow) der Module übereinstimmen.
- 4–8 Kapitel. Darüber lohnt die Navigation kaum noch.
- Logo-Mark: fertiges DAYONE-Logo (Icon + Schriftzug), kein reiner Textschriftzug.
- Präsentationstitel optional neben dem Logo — nur wenn neben Logo und Kapitel-Liste noch Platz ist, sonst weglassen.

**HINWEIS** — Auf Mobile NICHT ausblenden: derselbe Nummern-Fallback (Anzeige=Nummern) greift auch dort, ausgelöst durch die schmale Breite selbst statt durch einen eigenen Mobile-Zustand. Reicht das immer noch nicht, zuerst den Präsentationstitel weglassen, bevor die Kapitel-Liste angefasst wird.

**TODO** — FARBE FOLGT DER AKTIVEN SLIDE — noch nicht umgesetzt, hier festgehalten für die nächste Iteration: Aktuell hat die Nav einen fixen hellen Hintergrund (bg-default o.ä.), unabhängig davon, ob die gerade aktive Section Hell oder Dunkel ist. Richtig wäre: Hintergrund und Textfarbe der Nav passen sich beim Scrollen dynamisch an die Farbe (presentation/background) der Section an, die gerade unter der Nav aktiv ist — bei einer dunklen Section wird die Nav dunkel (mit hellem Text/Logo), bei einer hellen Section hell (mit dunklem Text/Logo). Das ist dasselbe Prinzip wie die "aktives Kapitel"-Erkennung (IntersectionObserver auf die Section-Mitte), nur dass zusätzlich zum aktiven Link-Highlight auch Hintergrund + Text/Logo-Farbe der ganzen Nav-Leiste umschalten.

<sub>Maschinell geprüft: 4–8 Kapitel</sub>

### `00 Elemente/02 karte`

<sub>Figma-Node `64:594`</sub>

**ZWECK** — Wiederverwendbare Karte aus Nummer, Titel und Fließtext. Baustein, kein Abschnitt: wird innerhalb von Modulen eingesetzt, nicht allein auf die Seite gestellt.

**FÜLLEN**

- Nummer zweistellig (01, 02 …), groß in Text-Secondary (Sand/900, #544e47).
- Titel als Merksatz, eine Zeile.
- Text 2–3 Sätze. Alle Karten einer Reihe gleich lang halten, sonst franst die Reihe aus.

**EINGESETZT IN**

- karten-karussell — als horizontal scrollbarer Karten-Track.
- kartenraster — wenn eine Option Fläche tragen soll.

**HINWEIS** — Trägt als einzige Kartenvariante eine Fläche (Sand/200). Im Hairline-Raster der Module ist das die Auszeichnung für "hervorgehoben" — deshalb sparsam einsetzen.

---

## 01 Einstieg

### `01 Einstieg/01 cover-hero`

<sub>Figma-Node `9:2`</sub>

**ZWECK** — Erster Bildschirm. Sagt in einem Atemzug, worum es geht, für wen und wann. Vorlage folgt dem DAYONE-Weekly-Hero (dayone-weekly-presentations).

**AUFBAU**

- Oben: Logo links, Badges rechts (Live-Q&A-Link, Anlass/KW). Badges sind optional — bei Kundenpitches meist nur einer oder keiner.
- Mitte: zweizeilige Headline. Zeile 1 SemiBold weiß = das Thema, Zeile 2 Regular grau = die Einordnung. Diese Zweiteilung trägt den ganzen Hero — nicht zu einer Zeile zusammenziehen.
- Unten: Trennlinie (Gradient Gray/400 → Gray/900, kein Vollton!) und Meta-Zeile aus 3 Angaben.

**FÜLLEN**

- Zeile 1: Projekt-/Produktname, 1–3 Wörter.
- Zeile 2: worum es inhaltlich geht, max. 5 Wörter.
- Subline: 1–2 Zeilen, warum das Thema jetzt relevant ist.
- Meta: genau 3 Angaben (Datum
- Presenter
- Format). Nicht erweitern.
- Logo-Mark: fertiges DAYONE-Logo (Icon + Schriftzug als ein Lockup), kein Platzhalter.
- Badge-Text: Regular, nicht SemiBold — bewusst leichter als der Rest der dunklen Fläche.

**HINWEIS** — Elemente erscheinen sofort beim Laden gestaffelt (nicht erst beim Scrollen wie bei den übrigen Modulen), da der Hero von Anfang an im Viewport ist.
Kein Scroll-Indikator. Optional leichtes Parallax auf einem Hintergrundbild; Headline dabei nicht mitbewegen.
Bewusst invertiert (Gray/900 + Gray/50), bleibt auch im Dark Mode dunkel.

### `01 Einstieg/02 agenda`

<sub>Figma-Node `27:3`</sub>

---

## 02 Struktur

### `02 Struktur/01 section-divider`

<sub>Figma-Node `118:70`</sub>

**ZWECK** — Trennt Kapitel voneinander und gibt dem Scrollen Rhythmus. Dient auch als Case-Study-Cover (früher eigenes Modul, zusammengelegt: gleiches Design).

**WANN VERWENDEN** — Nur wenn im folgenden Kapitel viel Content kommt und es eine kurze Vorwarnung/Einordnung braucht. Reicht der direkte Einstieg in die nächste Sektion, den Divider weglassen — nicht als Standard-Übergang zwischen jedem Kapitel einsetzen.

**FÜLLEN**

- Titel: 2–5 Wörter. Kapitelname ("Die Entscheidung") oder Kundenname bei Case Studies.
- Optionale Eyebrow darüber: "01 — AUSGANGSLAGE" oder "CASE STUDY".

**KEIN DOPPELTER KAPITELMARKER** — Pro Kapitel bekommt nur die jeweils erste Sektion den Kapitelmarker (Eyebrow-Nummer). Wird der Divider vor ein Modul gesetzt, das selbst schon einen Kapitelmarker führt, das Kapitelmarker-Property hier oder dort auf 'false' setzen — nie auf beiden Modulen gleichzeitig aktiv lassen.

**HINWEIS** — Läuft seit dem Mode-Umbau über presentation/background/text-Tokens wie jedes andere Modul; kein fester Dark-Zustand mehr. Standardmäßig dunkel befüllt, weil das in der Praxis meistens die richtige Wahl ist.

### `02 Struktur/02 big-statement`

<sub>Figma-Node `9:4`</sub>

**ZWECK** — Ein Gedanke, ganze Fläche. Setzt eine Zäsur und lässt eine Aussage wirken.

**ABGRENZUNG** — Mit Namensnennung stattdessen quote-block verwenden.

**FÜLLEN**

- Ein Satz, max. 2 Zeilen. Wenn zwei Gedanken drinstecken: zwei Module.
- Kein Punkt am Ende bei Claims; Punkt bei vollständigen Aussagen.
- Textbreite ist auf 10 von 12 Spalten gesetzt — nicht verbreitern, sonst leidet die Lesbarkeit.

### `02 Struktur/03 stepper`

<sub>Figma-Node `35:20`</sub>

**ZWECK** — Führt durch mehrere Phasen (Lifecycle, Journey, Prozess) und hält die Orientierung, während man scrollt.

**FÜLLEN**

- 3–6 Phasen. Kurze Labels, ein bis zwei Wörter.
- Pro Phase: Titel, Beschreibungssatz, 2–3 Opportunities/Kernpunkte.

**SCROLL** — Kernmuster: Sticky Scrollspy. Die Phasenleiste bleibt oben fixiert, die aktive Phase hebt sich ab, der Inhalt darunter wechselt beim Scrollen. Referenz: ny-pitch-three (Employee Lifecycle).

<sub>Maschinell geprüft: 3–6 Phasen, 2–3 Opportunities/Kernpunkte</sub>

---

## 03 Inhalt

### `03 Inhalt/01 headline-text-bild`

<sub>Figma-Node `27:48`</sub>

**ZWECK** — Standard-Arbeitspferd: ein Gedanke, erklärt mit Text und gestützt durch ein Bild.

**FÜLLEN**

- Topline kategorisiert (z. B. "01 — AUSGANGSLAGE").
- Fließtext 2–4 Sätze. Längeres gehört in headline-textraster.
- Bild inhaltlich, nicht dekorativ — Screenshot, Foto, Diagramm.

**SCROLL** — Gut geeignet für Sticky-Bild mit danebenlaufendem Text.

**HINWEIS** — Bei mehrfacher Verwendung Seiten abwechseln (Bild mal links, mal rechts), sonst wirkt die Seite monoton.

### `03 Inhalt/02 headline-textraster`

<sub>Figma-Node `9:5`</sub>

**ZWECK** — Vier gleichrangige Aspekte kompakt nebeneinander, ohne Karten-Optik.

**ABGRENZUNG** — Sollen die Punkte visuell abgesetzt sein, kartenraster nehmen; bei Reihenfolge 00 Elemente/02 karte (als nummerierte Kachel-Reihe).

**FÜLLEN**

- 3–4 Spalten. Titel je 1 Zeile, Text je 2–3 Zeilen.
- Spalten etwa gleich lang halten — ungleiche Längen lassen das Raster kippen.

<sub>Maschinell geprüft: 3–4 Spalten</sub>

### `03 Inhalt/03 sticky-nummernliste`

<sub>Figma-Node `9:6`</sub>

**ZWECK** — Mehrere gleichrangige Punkte erklären, ohne dass die Leitfrage aus dem Blick gerät. Nutzt das Browserformat aus: die linke Spalte bleibt stehen, die Liste rechts scrollt daran vorbei.

**AUFBAU**

- Links (sticky): Eyebrow, Headline, Einleitung. Bleibt fixiert, solange die rechte Spalte scrollt.
- Rechts: nummerierte Punkte, durch dünne Linien getrennt.

**FÜLLEN**

- mindestens 5 Punkte. Darunter lohnt das Sticky-Layout nicht.
- Titel als Aussage formulieren, nicht als Stichwort.
- Punkte etwa gleich lang halten.
- Eyebrow zweistellig nummerieren, passend zum Section-Divider davor.

**SCROLL** — position: sticky auf der linken Spalte, top-Offset ca. 120 px. Sticky erst ab Desktop; auf Mobile untereinander stapeln.

<sub>Maschinell geprüft: min. 5 Punkte</sub>

### `03 Inhalt/04 kartenraster`

<sub>Figma-Node `28:2`</sub>

**ZWECK**

- Drei gleichrangige Dinge nebeneinander stellen. Zwei erprobte Anwendungsfälle:
- Optionen-Vergleich (A/B/C) für Entscheidungs-Slides — eine Option als gewählt markieren.
- Zielgruppen-/Persona-Karten — je Segment Rolle, Kurztitel, Alltag. (Ersetzt "persona-cards".)

**FÜLLEN**

- Label oben: Option A/B/C bzw. Segmentname.
- Titel: eine Zeile, die den Kern trifft.
- Text: 2–3 Sätze. Alle drei Karten etwa gleich lang halten, sonst kippt das Raster optisch.
- Tag unten: Status oder Fazit ("Für Kernfeatures gewählt", "Nicht evaluiert").

**HINWEIS** — Bei mehr als 3 Items auf 00 Elemente/02 karte (als eigene Kachel-Reihe) oder headline-textraster wechseln.

### `03 Inhalt/05 prozess-schritte`

<sub>Figma-Node `28:22`</sub>

**ZWECK** — Zeigt einen Ablauf und wer worin welche Rolle hat (z. B. Mensch / KI, Kunde / DAYONE).

**ABGRENZUNG** — Ohne Rollenaufteilung reicht 00 Elemente/02 karte (als Reihe); mit Datumsbezug roadmap-timeline.

**FÜLLEN**

- 3–5 Schritte, zweistellig nummeriert.
- Pro Schritt zwei Rollen-Spalten mit je 2–4 Stichpunkten.
- Spaltenüberschriften konsistent über alle Schritte halten.

<sub>Maschinell geprüft: 3–5 Schritte, 2–4 Stichpunkten</sub>

---

## 04 Daten

### `04 Daten/01 kennzahlen-grid`

<sub>Figma-Node `118:76`</sub>

**ZWECK** — Harte Zahlen als Beleg. Der Moment, in dem Behauptungen messbar werden.

**FÜLLEN**

- 3–4 Kennzahlen. Mehr verwässert die Wirkung.
- Zahl kurz halten ("34", "+27,7 %", "6 Jahre"), Label darunter erklärt sie in 2–4 Wörtern.
- Nur Zahlen zeigen, die zur Kernaussage gehören — kein Dashboard.

**SCROLL** — Zwei Varianten aus derselben Vorlage: (a) statisch einblenden; (b) Pinned Section, Zahlen zählen scroll-synchron hoch und weitere Karten stapeln sich nacheinander im selben Frame (siehe cupra-pitch).

**HINWEIS** — Bewusst invertiert. Ersetzt das frühere Modul "kennzahlen-karten-stack".

<sub>Maschinell geprüft: 3–4 Kennzahlen, 2–4 Wörtern</sub>

### `04 Daten/02 chart-slide`

<sub>Figma-Node `36:3`</sub>

**ZWECK** — Eine Datenreihe, die eine These stützt.

**FÜLLEN**

- Titel sagt die Erkenntnis, nicht die Datenart. Also "Nutzung verdoppelt sich ab März", nicht "Nutzung nach Monat".
- Ein Chart pro Modul. Zwei Charts nebeneinander liest niemand.
- Quelle und Zeitraum immer angeben.
- Nur die Farben aus den Tokens; Blue Highlight für die Serie, die zählt.

**SCROLL** — Balken/Linie können beim Eintritt ins Viewport aufbauen.

### `04 Daten/03 matrix-2x2`

<sub>Figma-Node `36:10`</sub>

**ZWECK** — Vier Felder entlang zweier Achsen. Für Positionierung, Reifegrad, Portfolio.

**FÜLLEN**

- Beide Achsen benennen — ohne Achsenlabel ist eine Matrix nur ein Kasten mit vier Texten.
- Pro Quadrant Titel + 1–2 Sätze.
- Wenn eine Einordnung gezeigt wird (Punkt/Marker), im Text begründen.

### `04 Daten/04 fluss-diagramm`

<sub>Figma-Node `36:27`</sub>

**ZWECK** — Systemlandschaft oder Datenweg: was fließt von wo nach wo.

**FÜLLEN**

- 3–5 Stationen. Mehr wird zur Tapete — dann lieber gruppieren.
- Pro Box: Name + Rolle/Systemtyp.
- Pfeilrichtung konsequent (links → rechts), Rückflüsse gesondert kennzeichnen.

<sub>Maschinell geprüft: 3–5 Stationen</sub>

### `04 Daten/05 tabelle`

<sub>Figma-Node `36:41`</sub>

**ZWECK** — Wenn Werte exakt vergleichbar sein müssen und keine Grafik das leistet.

**FÜLLEN**

- Max. 4–5 Spalten, 5–8 Zeilen. Größere Tabellen gehören in einen Anhang oder Download.
- Zahlen rechtsbündig, Text linksbündig.
- Kopfzeile immer gesetzt lassen.

**HINWEIS** — Auf Mobile bricht eine breite Tabelle. Entweder horizontal scrollbar machen oder auf Karten umstellen.

<sub>Maschinell geprüft: 4–5 Spalten</sub>

---

## 05 Diagramme

### `05 Diagramme/01 text-graphic`

<sub>Figma-Node `33:19`</sub>

**ZWECK** — Text links, freie Grafik rechts (Diagramm, Illustration, Icon-Komposition o. ä.). Generalisiert aus dem frueheren "Konzentrische Kreise"-Modul; die runde Flaeche ist nur der Platzhalter-Vorschlag, kein Zwang zu Kreisen.

**FÜLLEN**

- Grafik aus dem Keynote-Master oder einer anderen Quelle uebernehmen, nicht neu zeichnen.
- Links Topline + eine Aussage, warum die Grafik hier relevant ist.

**SCROLL** — Bei mehrteiligen Grafiken (z. B. Ebenen eines Modells) lassen sich Teile nacheinander einblenden, gut als Pinned Section.

### `05 Diagramme/02 diagrammkarte`

<sub>Figma-Node `31:20`</sub>

**ZWECK** — Abstraktes Schaubild (Flywheel, Loop, Ökosystem) als visueller Einstieg in eine Case Study.

**FÜLLEN**

- Diagramm reduziert halten — es soll Aufmerksamkeit binden, nicht erklärt werden müssen.
- Darunter Projektname + Leistungsschlagworte (z. B. "Digitalstrategie und Produktentwicklung").

**SCROLL** — Zoom-Through: Das Diagramm vergrößert sich beim Scrollen kontinuierlich in einen konkreten Screenshot. Referenz: cupra-pitch.

---

## 06 Zeitachse

### `06 Zeitachse/01 roadmap-timeline`

<sub>Figma-Node `9:9`</sub>

**ZWECK** — Grober Zeitverlauf mit Meilensteinen. Für Überblick, nicht für Planung.

**ABGRENZUNG** — Für Arbeitspakete und Phasenbalken roadmap-zoom-in nehmen.

**FÜLLEN**

- 4–6 Meilensteine mit Zeitangabe + Kurzbezeichnung.
- Aktuellen Stand markieren ("Aktuell"), sonst weiß niemand, wo man steht.
- Vergangenes und Geplantes visuell unterscheiden.

<sub>Maschinell geprüft: 4–6 Meilensteine</sub>

### `06 Zeitachse/02 roadmap-zoom-in`

<sub>Figma-Node `33:3`</sub>

**ZWECK** — Detailplanung: Phasen als Balken über eine Zeitachse, plus erläuternde Meilensteine.

**FÜLLEN**

- Zeitraster wählen (Wochen / Quartale / Jahr) — Keynote-Master enthält Varianten von 6 Wochen bis 1 Jahr.
- Sidebar: 2–4 Meilensteine mit je einem Satz, was erreicht ist.
- Nicht mehr als 6 Arbeitspakete pro Ansicht.

**HINWEIS** — Bricht auf Mobile schnell. Dort besser auf eine vertikale Liste umstellen.

<sub>Maschinell geprüft: 2–4 Meilensteine, max. 6 Arbeitspakete</sub>

---

## 07 Media

### `07 Media/01 bild-feature-liste`

<sub>Figma-Node `32:3`</sub>

**ZWECK** — Ein Produkt oder Feature zeigen und gleichzeitig benennen, was es kann.

**FÜLLEN**

- Screenshot in echter Auflösung, keine skalierten Bilder.
- Versions-/Statuslabel ("Version 1.0") schafft Einordnung.
- 3–5 Feature-Punkte, je eine Zeile, mit Pfeil-Präfix.

**HINWEIS** — Sensible Daten im Screenshot vorher anonymisieren.

<sub>Maschinell geprüft: 3–5 Feature-Punkte</sub>

### `07 Media/02 device-mockup`

<sub>Figma-Node `32:21`</sub>

**ZWECK** — Prototypen im Gerätekontext zeigen, wenn die Plattform Teil der Aussage ist.

**ABGRENZUNG** — Geht es um Funktionen statt um Look & Feel: bild-feature-liste.

**FÜLLEN**

- Enthält echte Geräte aus dem DAYONE Designsystem (iPhone, MacBook; iPad ebenfalls verfügbar).
- Screen einsetzen: Screen-Ebene im Gerät auswählen und den Screenshot als Bild-Fill einsetzen — Gerät selbst nicht verändern.
- Variante pro Gerät wählbar: Color = black / white, beim iPhone zusätzlich Browser-Header = true / false.
- Mobile-Screens paarweise, Desktop einzeln — so bleibt die Komposition ruhig.
- Max. 3 Devices pro Modul.

<sub>Maschinell geprüft: max. 3 Devices</sub>

### `07 Media/03 medien-karten-grid`

<sub>Figma-Node `32:30`</sub>

**ZWECK**

- 2–3 Kacheln aus Bild + Titel + Kurztext. Zwei Anwendungsfälle:
- CTA-Kacheln, die auf Prototypen oder Unterseiten verlinken.
- Publikationen/Whitepaper mit Cover. (Ersetzt "publikations-karten".)

**FÜLLEN**

- Bilder im gleichen Seitenverhältnis, sonst wirkt die Reihe unruhig.
- Titel: Ziel der Kachel, nicht Dateiname.
- Text: ein Satz, der sagt, was den Nutzer hinter dem Klick erwartet.
- Bei CTA-Nutzung: Kachel komplett klickbar machen, nicht nur den Titel.

### `07 Media/04 grossbild`

<sub>Figma-Node `72:31`</sub>

**ZWECK** — Ein Bild, das für sich steht: Atmosphäre, Ort, Team, Produkt im Einsatz. Setzt einen visuellen Ruhepunkt zwischen textlastigen Abschnitten.

**ABGRENZUNG** — Geht es um ein Interface mit Funktionen: bild-feature-liste. Um ein Gerät: device-mockup. Um mehrere Bilder nebeneinander: medien-karten-grid.

**AUFBAU** — Das Bild läuft randabfallend über die volle Breite und bricht bewusst aus dem 12-Spalten-Raster aus. Kopf und Bildlegende bleiben im Raster (96 px Marge). Genau dieser Kontrast macht die Wirkung — Bild nicht in die Marge einrücken.

**FÜLLEN**

- Seitenverhältnis 3:2 oder 16:9, mindestens 2880 px breit (randabfallend auf Retina).
- Headline sagt die Aussage des Bildes, nicht seinen Inhalt. Also "So arbeiten wir wirklich", nicht "Büro Berlin".
- Bildlegende: ein Satz Einordnung. Fotocredit rechts, wenn nötig.
- Motiv inhaltlich, kein Stockfoto — sonst besser weglassen.

**SCROLL** — Leichtes Parallax auf dem Bild (max. 10 % Versatz) wirkt hier gut, weil das Motiv über die volle Breite läuft. Headline nicht mitbewegen.

<sub>Maschinell geprüft: min. 2880.0 px</sub>

---

## 08 Menschen

### `08 Menschen/01 team-grid`

<sub>Figma-Node `35:41`</sub>

**ZWECK** — Wer arbeitet am Projekt. Macht das Angebot greifbar.

**FÜLLEN**

- 3–6 Personen. Bei größeren Teams nur die Projektbesetzung zeigen.
- Fotos einheitlich: gleicher Hintergrund, gleicher Bildausschnitt, gleiche Höhe.
- Name + Rolle im Projekt (nicht der interne Jobtitel).

<sub>Maschinell geprüft: 3–6 Personen</sub>

### `08 Menschen/02 bild-intro`

<sub>Figma-Node `35:74`</sub>

**ZWECK** — Eine einzelne Person vorstellen, meist die präsentierende.

**ABGRENZUNG** — Ab zwei Personen team-grid verwenden.

**FÜLLEN**

- Portraitfoto, aufgelockert (kein Bewerbungsfoto-Look).
- Name, Rolle im Projekt, optional ein Satz Bezug zum Thema.

### `08 Menschen/03 quote-block`

<sub>Figma-Node `9:8`</sub>

**ZWECK** — Eine Aussage mit Absender. Wirkt als Beleg, weil jemand dafür geradesteht.

**FÜLLEN**

- Wörtliches Zitat, 1–2 Sätze. Nicht glattbügeln — Originalton wirkt stärker.
- Deutsche Anführungszeichen „ … “.
- Immer mit Name + Rolle. Ohne Attribution stattdessen big-statement nehmen.
- Freigabe der zitierten Person einholen, bevor der Onepager rausgeht.

---

## 09 Referenzen

### `09 Referenzen/01 logo-wand`

<sub>Figma-Node `30:2`</sub>

**ZWECK** — Vertrauen durch Referenzen. Zeigt auf einen Blick, mit wem DAYONE arbeitet.

**FÜLLEN**

- Logos einfarbig/schwarz, optisch auf gleiche Höhe bringen (nicht auf gleiche Breite!).
- 12–24 Logos. Bekannteste Marken nach oben links.
- Leere Slots am Zeilenende vermeiden — lieber eine Reihe weniger.

**SCROLL** — Optional Pinned Section: einzelne Logos werden nacheinander hervorgehoben (aktiv 100 %, Rest 20 % Deckkraft), z. B. um Branchen durchzugehen. Ersetzt das frühere Modul "logo-grid-sequenziell".

<sub>Maschinell geprüft: 12–24 Logos</sub>

### `09 Referenzen/02 bild-kennzahlenliste`

<sub>Figma-Node `29:38`</sub>

**ZWECK** — Unternehmenskennzahlen für Credential-Teile: Gründung, Standort, Größe.

**FÜLLEN**

- 4–6 Key-Value-Paare, feste Reihenfolge über alle Decks hinweg.
- Werte aktuell halten — Teamgröße und Jahreszahlen veralten unbemerkt.
- Bild: Büro oder Team, kein Stockfoto.

<sub>Maschinell geprüft: 4–6 Key-Value-Paare</sub>

### `09 Referenzen/03 headline-liste`

<sub>Figma-Node `118:103`</sub>

**ZWECK** — Was in einem Kundenprojekt erreicht werden sollte. Folgt meist direkt auf den Case-Study-Divider.

**FÜLLEN**

- 3–4 Ziele, je eine Zeile mit Pfeil.
- Ziele als Ergebnis formulieren ("Digitale Infrastruktur & Datenmanagement"), nicht als Tätigkeit.
- Kundenname links wiederholen, damit der Block auch isoliert lesbar bleibt.

**HINWEIS** — Bewusst invertiert, passend zum Divider davor.

<sub>Maschinell geprüft: 3–4 Ziele</sub>

---

## 10 Abschluss

### `10 Abschluss/01 karten-karussell`

<sub>Figma-Node `29:3`</sub>

**ZWECK** — Horizontal scrollbarer Karten-Track zum Strukturieren numerierter Textinhalte. Ursprünglich als reines Abschluss-Modul ("Was wir euch mitgeben") gedacht, inzwischen allgemein einsetzbar überall dort, wo mehrere gleichrangige Aussagen nummeriert nebeneinander stehen sollen (z. B. auch mitten im Content-Teil, nicht nur vor dem CTA).

**AUFBAU** — Eyebrow + Headline, darunter ein horizontal scrollbarer Karten-Track aus "00 Elemente/02 karte"-Instanzen. Die Karten laufen bewusst über den rechten Rand hinaus: das signalisiert, dass es weitergeht. Der erste Karte bleibt dabei am linken Grid-Rand ausgerichtet (gleiche Margin wie die Headline darüber) — nicht am Viewport-Rand.

**FÜLLEN**

- 4–7 Elemente. Nummer in Text-Secondary (Sand/900, #544e47), wie die Basis-Karte — keine Sonderfarbe. Titel als Merksatz, darunter 2–3 Sätze.
- Titel so formulieren, wie man es einem Kollegen im Aufzug sagen würde.
- Bei Verwendung als Abschluss: Erkenntnisse, keine Zusammenfassung. Bei Verwendung im Content-Teil: die jeweiligen Aussagen selbst.
- Alle Karten gleich hoch lassen — Text entsprechend kürzen.

**SCROLL** — Horizontaler Track (scroll-snap), Pfeile springen je eine Karte weiter. Auf Mobile untereinander stapeln oder als Swipe.

<sub>Maschinell geprüft: 4–7 Elemente</sub>

### `10 Abschluss/02 qr-tool-verweis`

<sub>Figma-Node `33:24`</sub>

**ZWECK** — Brücke aus der Präsentation in ein Tool, Board oder Formular.

**FÜLLEN**

- QR-Code mind. 180 px, sonst scannt er im Raum nicht zuverlässig.
- Ziel-URL zusätzlich als Text nennen — QR funktioniert nicht in PDFs am Desktop.
- Screenshot zeigt, was hinter dem Code wartet.

### `10 Abschluss/03 cta-footer`

<sub>Figma-Node `118:121`</sub>

**ZWECK** — Abschluss und Handlungsaufforderung. Letztes Modul jedes Onepagers.

**FÜLLEN**

- Claim kurz ("Check it out.").
- Max. 2 Buttons: einer primär, einer sekundär. Beide immer mit Pfeil →.
- Buttons auf Mobile full-width, min. 44 px hoch, Schrift min. 16 px (verhindert iOS-Zoom).
- Logo + Copyright nicht vergessen.

**HINWEIS** — Bewusst invertiert.

<sub>Maschinell geprüft: max. 2 Buttons, min. 44.0 px, min. 16.0 px</sub>

