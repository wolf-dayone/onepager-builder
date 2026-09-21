# DAYONE Onepager — Modulsystem und Qualitätssicherung

Quelle für den Skill `dayonepager`. Hier liegen die 34 Module aus der Figma-Datei
[DAYONE | AI-ready slides](https://www.figma.com/design/1CL62lpdnyiFW98MFs1GPS/DAYONE-%7C-AI-ready-slides),
die Werkzeuge, die daraus Vorlagen bauen, und der Prüfer, der fertige Seiten gegen die
Figma-Regeln hält.

**Fast alle Werkzeuge laufen auf der Python-Stdlib.** Kein `npm install`, kein Node —
macOS bringt `python3` mit. Einzige Ausnahme: `tools/qa_pruefen.py` braucht Playwright
für echte Browser-Checks (Screenshots, Overflow, Konsole) — siehe dort.

---

## Der Grundgedanke

Das System hatte vier handgepflegte Kopien derselben Wahrheit: Figma, `module-katalog.md`,
`starter.html` und die Live-Seite. Entsprechend liefen sie auseinander — Modulnamen wichen
ab, der Katalog behauptete Farbregeln, die Figma ausdrücklich verneint, und das
Skill-Template lag sechs Module hinter dem Repo, ohne dass es auffiel.

Jetzt gibt es **eine Quelle je Sache**:

| Sache | Quelle | Erzeugt daraus |
|---|---|---|
| Regeln je Modul | Figma-Component-Description | `referenzen/module-katalog.md`, `data/regeln.json` |
| Aussehen und Markup | `bausteine/<modul>.html` | `starter.html`, `modul-galerie.html` |
| Farben, Größen, Abstände | `referenzen/tokens.css` | Token-Block in jeder gebauten Datei |
| Das Skill-Paket | dieses Repo | `dist/dayonepager/` |

Was generiert wird, trägt einen Hinweis im Kopf. Wer dort von Hand ändert, verliert es
beim nächsten Build.

---

## Werkzeuge

```bash
python3 tools/katalog_bauen.py      # Figma-Descriptions → Katalog + Prüfregeln
python3 tools/bauen.py              # bausteine/ → starter.html, modul-galerie.html
python3 tools/pruefen.py seite.html # eine Seite gegen die Figma-Regeln prüfen
python3 tools/selbsttest.py         # prüft den Prüfer
python3 tools/skill_bauen.py --pruefen   # Skill-Paket bauen und Drift melden
python3 tools/qa_pruefen.py         # Browser-Checks: Screenshots, Overflow, Konsole (Playwright)
```

### `qa_pruefen.py` — was ein echter Browser sieht, den Regex nicht sieht

Lädt `modul-galerie.html` einmal je Viewport (375/768/1440 px — mobil/tablet/desktop)
und prüft jedes `[data-modul]`-Element einzeln: horizontaler Overflow, Console-/
Netzwerkfehler, kaputte Bilder (Platzhalter wie `[bild.jpg]` ausgenommen — die meldet
`pruefen.py` bereits), Links ohne Ziel. Schreibt einen Screenshot je Modul und Viewport
sowie `qa-ausgabe/qa-bericht.md` und `qa-ausgabe/befunde.json`.

Einmalig einrichten:
```bash
pip install playwright
python3 -m playwright install chromium
```
Lässt sich `chromium` wegen einer Netzwerk-Allowlist nicht herunterladen (blockiert z.B.
`cdn.playwright.dev`), läuft der Check trotzdem in der CI (Ubuntu-Runner, siehe
`.github/workflows/qualitaet.yml`) — dort non-blocking, mit Screenshots/Bericht als
Artefakt, solange die Modul-Bibliothek noch nicht durchtriagiert ist.

### `pruefen.py` — was geprüft wird

| Regel | Woher |
|---|---|
| genau ein Hero, genau ein CTA-Footer, 6–10 Module | Katalog, Dramaturgie |
| `id` + `data-chapter-title` vollständig, Nummern eindeutig, 4–8 Kapitel | Figma `kapitel-nav` |
| Kapitelmarker passt zur Kapitelnummer; nie auf Divider *und* Folgesektion | Figma `section-divider` |
| keine Roh-Hexwerte, keine Schriftgröße außerhalb 14/16/19/24/36/76 px | Figma-Variablen |
| Roobert nicht per `@font-face` eingebettet | Lizenz |
| keine übrigen `[Platzhalter]` im sichtbaren Text, in `<title>`, `<meta content>` oder `<img alt/src>` | Skill, Schritt 4 |
| Stückzahlen je Modul (3–5 Punkte, 12–24 Logos, 4–6 Meilensteine …) | Figma `FÜLLEN` |
| `alt` vorhanden, `loading="lazy"` | Zugänglichkeit, Ladezeit |
| `prefers-reduced-motion` vorhanden | Zugänglichkeit |
| CTA-Buttons ≥ 44 px hoch und ≥ 16 px Schrift | Figma `cta-footer` |
| mehrspaltiges Raster ohne Regel für schmale Viewports | Figma „Mobile wird zuerst kaputt“ |
| Rhythmus: nie zwei textlastige Module hintereinander | Gestaltungsprinzipien |

`FEHLER` lässt den Lauf rot werden. `WARNUNG` und `HINWEIS` nicht — sie markieren, was
meistens, aber nicht immer falsch ist.

Vorlagen (`starter.html`) und die Galerie sind von den Regeln ausgenommen, die für sie
nicht gelten können: Platzhalter, Modulanzahl, Dramaturgie.

### Warum es `selbsttest.py` gibt

Während der Entwicklung hat der Mobil-Check zweimal geschwiegen, obwohl die Regel
wirklich fehlte — einmal wegen einer zu engen Regex, einmal weil einzeilige Media
Queries die Zustandsverfolgung zerlegten. Ein Prüfer, der bei kaputtem Input nichts
meldet, ist schlimmer als keiner: er erzeugt Vertrauen, das er nicht deckt.

`selbsttest.py` baut deshalb eine feste Liste bekannter Fehler in die gebaute Vorlage
ein und verlangt, dass der Lint genau diese findet — siehe `FAELLE` in der Datei für
die aktuelle Anzahl und Auswahl.

---

## Ein Modul ändern

1. Datei in `bausteine/` bearbeiten. Ein Modul = eine Datei, `<style>` plus Markup.
   Braucht es CSS eines anderen Moduls, `<!-- braucht: <Figma-Name> -->` an den Anfang.
2. `python3 tools/bauen.py`
3. `modul-galerie.html` im Browser ansehen — dort steht jedes Modul einmal.
4. `python3 tools/pruefen.py starter.html modul-galerie.html index.html`
5. `python3 tools/selbsttest.py`
6. Committen. Der pre-commit-Hook wiederholt 2–5 von selbst, zieht die gebauten
   Dateien nach und baut das Skill-Paket neu (siehe unten). Die CI prüft dasselbe
   nochmal nach dem Push.
7. **Skill hochladen**, wenn die Änderung bei den Kolleg:innen ankommen soll:
   `python3 tools/skill_bauen.py --pruefen` sagt, ob es nötig ist.

## Vom Repo in den Skill

Das Repo ist die Quelle, der Skill das Build-Ergebnis. Dazwischen liegen zwei
Schritte — einer davon läuft automatisch, einer nicht:

| Schritt | Wer macht ihn |
|---|---|
| Bausteine → `starter.html`, `modul-galerie.html`, Katalog, Regeln | pre-commit-Hook |
| → `dist/dayonepager.skill` | pre-commit-Hook |
| → installierter Skill in der Claude-Skill-Verwaltung | **von Hand, ein Upload** |

Den letzten Schritt kann kein Hook übernehmen: die Skill-Verwaltung nimmt die
`.skill`-Datei über die Oberfläche entgegen, es gibt dafür keinen Repo-Zugriff.
Deshalb meldet sich der Hook nach jedem relevanten Commit, und

```bash
python3 tools/skill_bauen.py --pruefen
```

vergleicht das gebaute Paket Datei für Datei mit dem installierten Skill. Bei
`UPLOAD NOETIG` liegt der neue Stand als `dist/dayonepager.skill` bereit.

**Hook einmalig aktivieren** (pro Klon, weil `.git/hooks` nicht mitversioniert wird):

```bash
git config core.hooksPath tools/hooks
```

Der Hook springt nur an, wenn `bausteine/`, `referenzen/`, `skill/`, `tools/` oder
die Modul-Daten im Commit stecken, und bricht ab, wenn `pruefen.py` oder
`selbsttest.py` etwas finden — eine kaputte Vorlage kommt so gar nicht erst in
einen Commit.

Warum der Aufwand: der ausgelieferte Skill lag schon zweimal deutlich hinter dem
Repo (einmal sechs Module, einmal zwei Feedback-Runden), ohne dass es auffiel.
Beides wäre mit diesen zwei Zeilen aufgefallen.

---

## Eine Regel ändern

Regeln stehen **in Figma**, in der Component-Description. Dort ändern, dann:

```bash
python3 tools/katalog_bauen.py
```

Die Descriptions unter `data/descriptions/` sind Momentaufnahmen aus Figma. Sie werden
über den Figma-MCP gezogen; für einen automatischen Sync in der CI braucht es einen
`FIGMA_TOKEN` und `GET /v1/files/:key/components`.

---

## Dateien

```
bausteine/              ein Modul je Datei  ← hier wird geändert
  _basis.css            Reset, Raster, Typo-Rollen, Reveal
  _basis.js             Navigation, Reveal, Count-up, Timeline, Karussell, Stepper
  _symbole.svg          DAYONE-Logo als <symbol>
data/
  figma-komponenten.json  kanonische Namen + Node-IDs aus Figma
  descriptions/           die 34 Component-Descriptions im Original
  regeln.json             generiert — maschinenlesbare Prüfregeln
  modul-zuordnung.json    Figma-Name ↔ CSS-Klasse. Einziges handgepflegtes Stück.
referenzen/
  module-katalog.md       generiert — alle 34 Module mit Zweck und Füllregeln
  tokens.css              Farben, Schriften, Abstände — die einzige Quelle
  scroll-patterns.md
  ausliefern.md
skill/SKILL.md          Anleitung für den Skill
tools/                  die Werkzeuge
index.html              Beispielseite „Neuer Standort" (GitHub Pages)
starter.html            generiert — Weekly-Dramaturgie
modul-galerie.html      generiert — alle 34 Module zum Kopieren
dist/                   generiert — das Skill-Paket zum Hochladen
```

`tools/zerlegen.py` und `tools/seed_bestehende.py` waren einmalige Umbau-Skripte. Sie
bleiben liegen, weil sie belegen, woher die Bausteine stammen — für den laufenden
Betrieb braucht man sie nicht.
