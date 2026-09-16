---
name: dayone-onepager
description: Baut aus Inhalten eine fertige, teilbare Scrollytelling-Onepager-Website im DAYONE-Branding — auf Basis der 34 Module aus der Figma-Datei "DAYONE | AI-ready slides". Diesen Skill immer verwenden, wenn jemand einen Onepager, eine Präsentationsseite, eine Weekly-Präsentation, eine Pitch-Page, eine Case-Study-Seite oder eine Scrollytelling-Seite erstellen will — auch dann, wenn nur von "Präsentation", "Slides", "Deck", "Landingpage für das Projekt", "Seite für das Weekly" oder "das als Website bauen" die Rede ist und die Begriffe Onepager oder Scrollytelling gar nicht fallen. Ebenfalls verwenden, wenn ein bestehender DAYONE-Onepager erweitert, umgebaut oder mit neuen Modulen gefüllt werden soll.
---

# DAYONE Onepager

Dieser Skill macht aus Inhalten eine funktionierende, teilbare Website — kein Slide-Deck
als PDF, sondern eine Seite, die man scrollt und deren URL oder Datei man weitergibt.

Die Bausteine existieren als Figma-Komponenten und sind hier **vollständig** als HTML
abgebildet. Die Aufgabe ist **nicht**, Design zu erfinden, sondern die richtigen Module
in die richtige Reihenfolge zu bringen und mit echten Inhalten zu füllen.

## Wer das benutzt

Meistens Menschen ohne Code-Hintergrund — Strategie, Marketing, PM. Sie kennen ihren
Inhalt, aber nicht die Modulnamen. Also: **nicht nach Modulen fragen, sondern nach dem
Inhalt.** Die Modulauswahl ist Aufgabe dieses Skills, nicht des Menschen.

Entsprechend auch so kommunizieren: "Ich bau dir daraus eine Seite mit sieben Abschnitten"
statt "Ich instanziiere `sticky-nummernliste` mit drei Items".

---

## Ablauf

### 1. Inhalt verstehen, nicht Module abfragen

Wenn der Anlass und der Inhalt schon im Gespräch stehen: direkt loslegen. Sonst **maximal
drei Fragen**, und zwar diese:

1. **Was ist der Anlass?** (Weekly, Kundenpitch, Case Study, Credentials — bestimmt die Dramaturgie)
2. **Was sind die 3–6 Kernbotschaften?** (bestimmt, welche Module gebraucht werden)
3. **Gibt es Zahlen, Zitate, Screenshots, Logos — und Links?** (bestimmt, welche
   Belege eingebaut werden können). **Links ausdrücklich mitfragen**: Prototyp,
   Notion-Seite, Slack-Channel, Wiki, Tool. Sie bestimmen nicht nur den Inhalt,
   sondern die Modulauswahl — siehe Schritt 7.

Mehr nicht. Alles Weitere ergibt sich oder wird sinnvoll angenommen und beim Übergeben
benannt. Wer einen langen, fertigen Input liefert, bekommt gar keine Rückfragen — dann
direkt bauen.

**Rohmaterial ist besser als vorsortiertes.** Die häufigste Bremse ist, dass Menschen
ihren Inhalt erst selbst in Form bringen wollen, bevor sie ihn abgeben — und dann gar
nicht anfangen. Wenn jemand zögert oder sich entschuldigt ("das ist noch ungeordnet",
"ich müsste das erst sortieren"), aktiv ermutigen, das Material so wie es ist
anzuhängen: Meeting-Notizen, Transkript, altes Deck, Stichpunktliste. Daraus die
Kernbotschaften selbst ziehen und zur Bestätigung vorlegen, statt danach zu fragen.
Sortieren ist Teil dieser Aufgabe, nicht Voraussetzung für sie.

### 2. Dramaturgie vorschlagen

Vor dem Bauen die geplante Abfolge in einem kurzen Absatz zeigen — als Abschnittstitel in
Alltagssprache, nicht als Modulnamen. So kann der Mensch die Reihenfolge korrigieren,
bevor Arbeit hineinfließt.

Erprobte Abfolgen je Anlass stehen in `references/module-katalog.md`. Faustregeln:

- **6–10 Module.** Darunter dünn, darüber ermüdend.
- **Rhythmus wechseln** — nie zwei textlastige Module hintereinander. Alle 3–4 Sektionen
  ein dunkles Modul als Zäsur.
- **Ein Gedanke pro Modul.** Zwei Aussagen = zwei Module.
- Genau **ein** Hero am Anfang, genau **ein** CTA-Footer am Ende.

### 3. Module wählen

`references/module-katalog.md` lesen. Dort stehen alle 34 Bausteine mit Zweck,
Füllregeln und Abgrenzung — **direkt aus den Figma-Component-Descriptions generiert**,
nicht von Hand gepflegt. Was dort steht, steht so in Figma.

Die Abgrenzungen ernst nehmen — sie verhindern die häufigsten Fehlgriffe:
`big-statement` vs. `quote-block` (Namensnennung?), `karten-3er` vs.
`headline-textraster` (visuell abgesetzt?), `roadmap-timeline` vs. `roadmap-zoom-in`
(Überblick oder Planung?).

**Farbe ist bei jedem Modul frei wählbar** (hell Sand/100 oder dunkel Gray/900). Es gibt
keine feste Zuordnung von Farbe zu Modul. Der Wechsel markiert einen neuen Sinnabschnitt,
gleiche Farbe hält Zusammengehöriges als Einheit.

### 4. Seite bauen

`assets/starter.html` kopieren — das ist die erprobte Weekly-Abfolge, fertig nummeriert.

Für alles, was dort nicht drin ist: **`assets/modul-galerie.html` öffnen.** Sie enthält
alle 34 Module einmal mit Platzhalter-Inhalt, jeweils mit Figma-Name beschriftet. Das
gewünschte Modul samt seines `<style>`-Blocks herauskopieren. **Module nicht selbst
nachbauen** — sie existieren alle.

Dann:
- Nicht gebrauchte Sektionen **löschen**, nicht auskommentieren.
- Jede Kapitel-Sektion behält `id`, `data-chapter` und `data-chapter-title` — die
  Navigation baut sich daraus selbst auf.
- Jede Sektion behält ihr `data-modul="<Figma-Name>"`. Daran erkennt der Qualitäts-Check
  in Schritt 8, welche Regeln für sie gelten. Nicht entfernen.
- Kapitelnummern durchgehend halten: `data-chapter`, `id` und der Kapitelmarker
  (`.eyebrow`) tragen dieselbe Nummer.
- Pro Kapitel trägt nur die **erste** Sektion den Kapitelmarker. Steht ein Divider davor,
  gehört der Marker dorthin — nie auf beiden.
- **Alle `[Platzhalter]` ersetzen.**

Für Scroll-Effekte über das Enthaltene hinaus: `references/scroll-patterns.md`.
Dort steht auch, warum zwei bis drei Effekte pro Seite genug sind.

Farben, Schriftgrößen und Abstände kommen aus den Tokens (`assets/tokens.css`, im Template
bereits inline). **Keine eigenen Hex-Werte, keine eigenen Schriftgrößen** — die Tokens
entsprechen 1:1 den Figma-Variablen, und nur dadurch bleibt die Seite on-brand. Gültige
Schriftgrößen sind 14, 16, 19, 24, 36 und 76 px, jeweils als `var(--text-…)`.

### 5. Inhalte schärfen

Beim Füllen nicht nur übernehmen, sondern auf das Format hin redigieren. Das ist der
Teil, der eine Seite gut macht:

- **Headlines sagen die Erkenntnis**, nicht das Thema. "Nutzung verdoppelt sich ab März"
  statt "Nutzung nach Monat".
- **Kernbotschaften als vollständige Aussage**, nicht als Stichwort. "Klarheit ist die
  neue Arbeit" statt "Klarheit".
- **Agendapunkte als Frage** — die der Abschnitt beantwortet. Wirksamer als ein Substantiv.
- **Kurz halten**: Karten 2–3 Sätze, Listenpunkte 2–4 Sätze, Kennzahl-Labels 2–4 Wörter.
- **Parallel bauen**: Karten nebeneinander etwa gleich lang, sonst kippt das Raster optisch.

Wo Inhalt fehlt, nicht erfinden: sinnvollen Platzhalter setzen und beim Übergeben nennen.

### 6. Bilder einsetzen

Das Template enthält Bild-Platzhalter. Damit umgehen:

- **Bilder liegen vor:** neben die HTML-Datei legen und relativ verlinken
  (`<img src="bild.jpg" alt="…" loading="lazy">`). Datei und Bilder dann zusammen
  verschicken. Vorher komprimieren — ein Screenshot braucht selten mehr als 1600 px
  Breite, ein randabfallendes Bild mindestens 2880 px.
- **Bilder fehlen noch:** Platzhalter stehen lassen und beim Übergeben ausdrücklich
  nennen. Nicht durch Stockfotos ersetzen — ein leerer Platzhalter ist ehrlicher und
  wird eher nachgeliefert als ein beliebiges Bild, das niemand mehr hinterfragt.
- **Charts, Gantt-Diagramme und QR-Codes** gehören nicht als Bild eingesetzt: Sie
  entstehen aus echten Daten bzw. müssen auf eine reale URL zeigen. `chart-slide` und
  `roadmap-zoom-in` bringen dafür echte HTML-Bausteine mit.

Sensible Inhalte in Screenshots vor dem Teilen anonymisieren.

### 7. Links einsetzen

Links sind kein Nachtrag, sondern bestimmen mit, welche Module gebraucht werden.
Deshalb gehören sie in die Rückfrage aus Schritt 1 und nicht erst ans Ende.

**Wohin welcher Link gehört:**

| Was verlinkt wird | Wohin damit |
|---|---|
| **Prototyp, klickbare Demo** | `07 Media/02 device-mockup`, wenn die Plattform Teil der Aussage ist (Mobile-App, Desktop-Tool). Mehrere Prototypen oder Unterseiten: `07 Media/03 medien-karten-grid` — dort ist die ganze Kachel klickbar. |
| **Notion, Confluence, Wiki, Slack-Channel** | CTA-Footer. Das sind Anlaufstellen zum Weiterlesen, keine eigenen Abschnitte — sie würden die Dramaturgie unterbrechen. |
| **Tool, das im Raum ausprobiert werden soll** | `10 Abschluss/02 qr-tool-verweis`. Der QR-Code funktioniert nur, wenn er auf eine echte URL zeigt. |
| **Quelle oder Beleg zu einer Zahl** | direkt im Text des jeweiligen Moduls, nicht in den Footer. |

**Vorschaubilder für verlinkte Prototypen:**

- **Screenshot liegt vor:** einsetzen. Alle Kacheln einer Reihe im gleichen
  Seitenverhältnis, sonst wirkt die Reihe unruhig.
- **Screenshot fehlt:** danach fragen — ein Prototyp-Link ohne Bild ist deutlich
  schwächer. Kommt keiner, eine **beschriftete Kachel** setzen: Zielname und Domain
  als Text auf der Platzhalterfläche. Das sagt ehrlich, was dahinter wartet.
- **Keine erfundenen Screenshots.** Ein selbst gebautes Bild, das aussieht wie das
  Produkt, aber keines ist, führt Leser:innen in die Irre — schlimmer als ein leeres
  Feld, weil niemand es mehr hinterfragt. Dasselbe gilt für Stockfotos.

**Harte Regel: kein Button ohne Ziel.**

Fehlt eine URL, `href="#"` **nicht** als Platzhalter setzen. Ein Knopf, der nichts tut,
fällt erst der Empfängerin auf — und bis dahin sieht die Seite fertig aus. Stattdessen:

- nach der URL fragen, oder
- den Button weglassen und beim Übergeben nennen, was noch fehlt, oder
- `href="[URL: Umzugsplan im Wiki]"` setzen — ein sichtbarer Platzhalter, den der
  Qualitäts-Check meldet.

Der Check in Schritt 8 prüft das: leeres `href`, `href="#"` und Anker, die auf eine
nicht existierende `id` zeigen, sind Fehler.

### 8. Qualitäts-Check laufen lassen

**Vor dem Übergeben.** Der Check ist Teil der Arbeit, nicht optional. Er liegt diesem
Skill bei und braucht nichts weiter als `python3` — das bringt macOS mit:

```
python3 tools/pruefen.py /pfad/zu/meine-seite.html
```

Aus dem Skill-Verzeichnis heraus aufrufen (dort liegen `tools/` und `data/`), die zu
prüfende Datei mit vollem Pfad übergeben.

Geprüft wird gegen dieselben Figma-Regeln, die im Katalog stehen: übrige Platzhalter,
Schriftgrößen und Farben außerhalb der Tokens, vollständige Kapitel-Attribute,
Stückzahlen je Modul (3–5 Punkte in der Sticky-Liste, 12–24 Logos in der Logo-Wand …),
`alt`-Texte, `prefers-reduced-motion`, Touch-Größen und mehrspaltige Raster ohne
Mobil-Regel.

`FEHLER` müssen weg. `WARNUNG` und `HINWEIS` prüfen und entweder beheben oder beim
Übergeben begründen, warum sie hier in Ordnung sind.

**Lässt sich `python3` in dieser Umgebung nicht ausführen**, den Check nicht
stillschweigend überspringen, sondern von Hand durchgehen und beim Übergeben sagen,
dass er nicht lief:

- kein `[` mehr im sichtbaren Text (Achtung: in CSS und JavaScript stehen eckige
  Klammern legitim — nur den Textinhalt prüfen)
- keine rohen `px`-Schriftgrößen; erlaubt sind 14, 16, 19, 24, 36, 76 als `var(--text-…)`
- keine Hex-Farben außerhalb des `:root`-Blocks
- jede Kapitel-Sektion mit `id`, `data-chapter`, `data-chapter-title` und `data-modul`
- Kapitelnummer und Kapitelmarker tragen dieselbe Zahl
- jedes Bild mit `alt` und `loading="lazy"`
- genau ein Hero, genau ein CTA-Footer, 6–10 Module

### 9. Übergeben

Datei in den Output-Ordner legen und mit `present_files` übergeben — ohne diesen Schritt
ist sie für den Menschen nicht erreichbar.

Dazu kurz sagen:
- welche Abschnitte die Seite hat,
- was noch fehlt (Bilder, Zahlen, Freigaben) — **Links einzeln nennen**: welcher
  Button noch kein Ziel hat und welcher Prototyp noch kein Vorschaubild,
- was der Qualitäts-Check gemeldet hat und was davon bewusst so bleibt,
- dass sie sich per Doppelklick im Browser öffnen lässt.

Braucht die Seite eine eigene URL, `references/ausliefern.md` lesen — dort stehen der
Vercel-Weg, der Umgang mit Bildern, die Schrift-Lizenzfrage und der Zugriffsschutz für
Kundeninhalte.

---

## Worauf zu achten ist

**Roobert liegt nicht bei.** Die Schrift ist lizenzpflichtig. Das Template nutzt
`"Roobert", "Inter", system-ui` — lokal installiert sieht man sie, sonst greift der
Fallback. Roobert nicht in Dateien einbetten, die das Haus verlassen.

**Kundeninhalte gehören nicht offen ins Netz.** Bei einem Deployment vorher
Passwortschutz aktivieren, nicht hinterher.

**Zitate brauchen Freigabe** der zitierten Person, bevor die Seite geteilt wird.

**Screenshots vorher anonymisieren.** Echte Kundennamen, Umsätze und Personendaten
rutschen sonst mit in ein geteiltes Dokument.

**Vercel-Zugang ist nicht selbstverständlich.** Der Deploy-Schritt setzt ihn voraus.
Wer keinen hat, bleibt bei der HTML-Datei — die ist vollwertig, nur ohne eigene URL.
Nicht so tun, als sei das ein Mangel: für Weeklies und interne Runden ist die Datei
der schnellere Weg.

**Mobile wird zuerst kaputt** — bei Sticky-Spalten, Tabellen und Roadmaps. Die Module
fangen das ab; bei eigenen Ergänzungen daran denken und eine Regel für schmale
Viewports mitschreiben. Der Qualitäts-Check meldet mehrspaltige Raster ohne solche Regel.

---

## Dateien

| Datei | Wann lesen |
|---|---|
| `references/module-katalog.md` | Immer vor der Modulauswahl — alle 34 Bausteine mit Zweck, Füllregeln, Abgrenzung und erprobten Abfolgen. Generiert aus Figma. |
| `references/scroll-patterns.md` | Wenn Scroll-Effekte über das Template hinaus gebraucht werden |
| `references/ausliefern.md` | Wenn die Seite eine eigene URL braucht oder Bilder/Schrift/Zugriffsschutz zu klären sind |
| `assets/starter.html` | Immer — Grundlage jeder neuen Seite (Weekly-Abfolge) |
| `assets/modul-galerie.html` | Sobald ein Modul gebraucht wird, das nicht im Starter steht — alle 34 zum Herauskopieren |
| `assets/tokens.css` | Wenn ein Modul von Grund auf neu gebaut wird |
| `tools/pruefen.py` | Schritt 8 — prüft eine fertige Seite gegen die Figma-Regeln |

Die Figma-Quelle der Module:
`https://www.figma.com/design/1CL62lpdnyiFW98MFs1GPS/DAYONE-%7C-AI-ready-slides`
(Seite *Module*). Layernamen dort und Modulnamen hier sind identisch — das prüft
`tools/katalog_bauen.py` bei jedem Sync.

**Dieser Skill ist ein Build-Ergebnis.** Quelle ist das Repo
`github.com/wolf-dayone/slides-test`. Änderungen an Modulen gehören nach `bausteine/`,
Änderungen an Regeln in die Figma-Component-Description — nicht in die Dateien hier.
