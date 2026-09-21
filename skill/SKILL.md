---
name: dayonepager
description: Baut aus Inhalten eine fertige, teilbare Scrollytelling-Onepager-Website im DAYONE-Branding, auf Basis der 34 Module aus der Figma-Datei "DAYONE | AI-ready slides". Diesen Skill aktivieren, sobald einer dieser Begriffe explizit fällt: Onepager, Online-Präsentation, Präsentationsseite, Scrollytelling(-Seite), Pitch-Page, Website-Pitch, Landingpage oder Case-Study-Seite. Fällt stattdessen nur ein allgemeinerer Begriff wie "Präsentation", "Slides", "Deck", "Weekly" oder "Case Study" ohne eines der obigen Stichworte, den Skill nur aktivieren, wenn die Person zusätzlich ausdrücklich sagt, dass das Ergebnis teilbar sein soll (zum Beispiel "das soll man teilen können", "mit eigener URL", "als Link verschicken", "shareable"); sonst nicht von sich aus greifen. Ebenfalls verwenden, wenn ein bestehender DAYONE-Onepager erweitert, umgebaut oder mit neuen Modulen gefüllt werden soll.
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

### 2. Page Plan erstellen

Vor dem Bauen die geplante Abfolge festhalten — nicht nur als Absatz im Chat, sondern als
Datei: `page-plans/_vorlage.plan.md` kopieren nach `page-plans/<projekt-slug>.plan.md` und
ausfüllen (Seite, Abschnitte, Modul je Abschnitt, Medienstatus). Dem Menschen dabei in
Alltagssprache zeigen, worum es geht — als Abschnittstitel, nicht als Modulnamen — nicht die
rohe Tabelle vorlegen. So kann er die Reihenfolge korrigieren, bevor Arbeit hineinfließt.

Der Plan ist der Grund, warum eine spätere Korrektur wie „bei Abschnitt 6 lieber Cards"
gezielt bleibt: nur die betroffene Zeile in der Tabelle ändern und nur diesen einen Abschnitt
neu bauen — nicht die ganze Seite neu interpretieren. Jede so vorgenommene Änderung kurz im
Änderungsprotokoll des Plans festhalten.

Bei einem kurzen, eindeutigen Auftrag (z. B. 6 Module, alles im Briefing benannt) reicht eine
knappe Tabelle in wenigen Minuten — der Plan ist ein Arbeitsmittel, kein Pflichtformular.

Erprobte Abfolgen je Anlass stehen in `references/module-katalog.md`. Faustregeln:

- **6–10 Module.** Darunter dünn, darüber ermüdend.
- **Rhythmus wechseln** — nie zwei textlastige Module hintereinander. Alle 3–4 Sektionen
  ein dunkles Modul als Zäsur.
- **Ein Gedanke pro Modul.** Zwei Aussagen = zwei Module.
- **Nicht zweimal dasselbe Modul, wenn es auch anders geht.** Ab dem dritten
  Vorkommen wirkt ein Modul wie eine Formatierung statt wie eine Aussage — die
  Seite liest sich dann wie eine Liste. Der Katalog hat für fast jeden Inhalt
  zwei bis drei passende Module; die Abgrenzungen dort nennen die Alternative.
- Genau **ein** Hero am Anfang, genau **ein** CTA-Footer am Ende.

### 3. Module wählen

`references/module-katalog.md` lesen. Dort stehen alle 34 Bausteine mit Zweck,
Füllregeln und Abgrenzung — **direkt aus den Figma-Component-Descriptions generiert**,
nicht von Hand gepflegt. Was dort steht, steht so in Figma.

Die Abgrenzungen ernst nehmen — sie verhindern die häufigsten Fehlgriffe:
`big-statement` vs. `quote-block` (Namensnennung?), `kartenraster` vs.
`headline-textraster` (visuell abgesetzt?), `roadmap-timeline` vs. `roadmap-zoom-in`
(Überblick oder Planung?).

**Die Agenda muss sich verdienen.** Sie ist kein Standardbaustein. Nur einsetzen,
wenn eine thematische Übersicht wirklich Teil der Präsentation ist — also wenn:

- jemand sie ausdrücklich nennt („erst ein Überblick, dann die Details"), **oder**
- die Seite genug Umfang hat, dass eine Übersicht Orientierung gibt — Faustregel:
  ab vier Kapiteln, und der Inhalt reicht für mehr als ein paar Minuten Lesen.

Bei einer kurzen Seite mit zwei oder drei Kapiteln kündigt die Agenda nur an, was man
zwei Bildschirme später ohnehin sieht. Dann weglassen — die Kapitel-Navigation oben
leistet die Orientierung bereits. Im Zweifel nachfragen, statt sie vorsorglich zu
setzen.

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
Wie sich das System bewegt (Reveal-Rollen, Motion-Tokens, Choreografien, Reduced Motion): `references/animationen.md` — vor jeder neuen `transition` lesen.
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

**Im Zweifel mehr Bilder.** Eine reine Textseite ermüdet, egal wie gut die Texte sind —
die Module sind darauf ausgelegt, dass zwischen den textlastigen Abschnitten visuelle
Ruhepunkte liegen. Wenn nach Schritt 1 kein Bildmaterial genannt wurde, **aktiv
nachfragen**, bevor gebaut wird:

> „Hast du Screenshots, Fotos vom Team oder Grafiken dazu? Auch grobe reichen — die
> Seite trägt deutlich besser, wenn zwischen den Textabschnitten etwas zu sehen ist."

Konkret fragen, nicht allgemein: Screenshots vom Produkt, Fotos vom Workshop, das
Diagramm aus dem Konzept, Portraits fürs Team-Grid. Wer „hast du Bilder?" gefragt wird,
antwortet meistens nein; wer „hast du einen Screenshot von dem Prototyp?" gefragt wird,
sucht ihn heraus.

Der Qualitäts-Check meldet es, wenn keines der Inhaltsmodule etwas Visuelles trägt.

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
- **Screenshot fehlt, Link zeigt auf Figma:** selbst einen ziehen, wenn ein
  Figma-Zugang zur Verfügung steht (`get_screenshot` über den Figma-MCP, Node-ID aus
  der URL). Das ist ein echtes Abbild des Prototyps, keine Erfindung — und erspart dem
  Menschen einen Arbeitsschritt. Geht der Zugriff nicht (kein MCP, geschützte Datei),
  einmal nachfragen statt es schweigend zu lassen.
- **Screenshot fehlt sonst:** danach fragen — ein Prototyp-Link ohne Bild ist deutlich
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
- was noch fehlt — die `Unresolved`-Liste aus dem Page Plan unverändert übernehmen, nicht
  neu aus dem Gedächtnis zusammenstellen. **Links einzeln nennen**: welcher Button noch kein
  Ziel hat und welcher Prototyp noch kein Vorschaubild,
- was der Qualitäts-Check gemeldet hat und was davon bewusst so bleibt,
- dass sie sich per Doppelklick im Browser öffnen lässt.

Braucht die Seite eine eigene URL, `references/ausliefern.md` lesen — dort stehen der
Vercel-Weg, der Umgang mit Bildern, die Schrift-Lizenzfrage und der Zugriffsschutz für
Kundeninhalte.

### 10. Nach der Freigabe: nächste Schritte proaktiv anbieten

Sobald der Mensch den ersten Entwurf freigibt ("passt so", "sieht gut aus", o. ä.), nicht
abwarten, ob von selbst noch etwas kommt. Aktiv den nächsten Schritt anbieten und kurz
zusammenfassen, was jetzt möglich ist — zum Beispiel so:

> „Die Seite ist freigegeben. Aktuell hast du sie als Datei — die kannst du direkt per
> Doppelklick öffnen und verschicken. Wenn du sie stattdessen unter einer eigenen URL
> teilen willst (für einen Kundenpitch, zum Verlinken, oder einfach damit niemand eine
> Datei herunterladen muss), kann ich dich jetzt durch die Einrichtung von Git und Vercel
> führen — dauert in der Regel unter 15 Minuten, du brauchst dafür nur einen GitHub- und
> einen Vercel-Account. Sag Bescheid, wenn du das möchtest."

Diese Frage **immer stellen**, nicht nur wenn danach gefragt wird. Die meisten Menschen,
die diesen Skill benutzen, kennen den Unterschied zwischen Datei und eigener URL nicht
und wissen entsprechend nicht, dass Letzteres mit wenig Aufwand möglich ist — genau
deshalb ist das Anbieten Teil der Aufgabe, nicht der Person überlassen.

Will die Person eine URL: `references/ausliefern.md`, Abschnitt „Weg B — Vercel", **Schritt
für Schritt gemeinsam durchgehen** — nicht nur darauf verweisen und warten. Konkret heißt
das:

- vor jedem Schritt in einem Satz erklären, was er bewirkt und warum er nötig ist (die
  Person hat meist keinen Code-Hintergrund und soll nicht raten müssen, wofür `git init`
  gut ist),
- ist eine Shell mit Zugriff auf `git`/`gh` vorhanden, die Befehle **selbst ausführen**
  statt sie nur aufzulisten — die Person tippt nichts ab, sondern bestätigt nur Zugänge
  (GitHub-Login, Vercel-Login) und Entscheidungen (Repo-Name, privat oder öffentlich),
- nach jedem Schritt kurz bestätigen, dass er geklappt hat, bevor der nächste folgt —
  nicht alle Schritte auf einmal abarbeiten und erst am Ende berichten; falls etwas
  nicht griffbereit ist, das an dieser Stelle klar benennen (fehlender GitHub-Zugang,
  fehlender Vercel-Zugang) und dort anhalten statt zu improvisieren,
- am Ende die fertige URL nennen und, falls es sich um Kundeninhalte handelt, aktiv an
  den Zugriffsschutz erinnern (siehe Checkliste in `ausliefern.md`) — nicht erst wenn
  danach gefragt wird.

Will die Person (noch) keine URL: bei der Datei bleiben, aber kurz erwähnen, dass sich
das jederzeit nachholen lässt — die Seite dafür nicht extra vorbereiten müssen, der
Git-Schritt funktioniert auch später noch mit der fertigen Datei.

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
| `references/animationen.md` | Wenn etwas animiert wird: Tokens, Reveal-Rollen, Choreografien |
| `references/ausliefern.md` | Nach jeder Freigabe eines ersten Entwurfs proaktiv anbieten (Schritt 10) — Vercel-Weg mit Git-Schritt-für-Schritt-Anleitung, Umgang mit Bildern/Schrift/Zugriffsschutz |
| `assets/starter.html` | Immer — Grundlage jeder neuen Seite (Weekly-Abfolge) |
| `assets/modul-galerie.html` | Sobald ein Modul gebraucht wird, das nicht im Starter steht — alle 34 zum Herauskopieren |
| `assets/tokens.css` | Wenn ein Modul von Grund auf neu gebaut wird |
| `assets/page-plan-vorlage.md` | Schritt 2 — Kopiervorlage für den Page Plan |
| `tools/pruefen.py` | Schritt 8 — prüft eine fertige Seite gegen die Figma-Regeln |

Die Figma-Quelle der Module:
`https://www.figma.com/design/1CL62lpdnyiFW98MFs1GPS/DAYONE-%7C-AI-ready-slides`
(Seite *Module*). Layernamen dort und Modulnamen hier sind identisch — das prüft
`tools/katalog_bauen.py` bei jedem Sync.

**Dieser Skill ist ein Build-Ergebnis.** Quelle ist das Repo
`github.com/wolf-dayone/onepager-builder`. Änderungen an Modulen gehören nach `bausteine/`,
Änderungen an Regeln in die Figma-Component-Description — nicht in die Dateien hier.
