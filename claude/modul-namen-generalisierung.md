# Modul-Namen generalisiert (2026-09-17)

Anlass: Ernst fand die Modulbibliothek teilweise zu anwendungsfall-spezifisch
benannt (Beispiel: `case-study-ziele` ist strukturell nur "Headline + Liste").
Audit + Umsetzung in einem Zug: Figma-Komponentennamen UND Code gleichzeitig
umbenannt, damit Figma (Source of Truth) und Repo nicht auseinanderlaufen.

## Umbenennungen (Figma + Code synchron)

| Alt | Neu | Warum |
|---|---|---|
| `03 Inhalt/04 karten-3er` | `03 Inhalt/04 kartenraster` | Name suggerierte "genau 3", das Grid ist aber `auto-fit` (beliebig viele Karten). Zusätzlich stand in `data/modul-zuordnung.json` sogar eine harte `"genau": 3`-Regel, die den Linter entsprechend einschränkte — jetzt entfernt. |
| `04 Daten/04 datenfluss-diagramm` | `04 Daten/04 fluss-diagramm` | Struktur ist ein generisches "N Stationen, Pfeile dazwischen" — nicht spezifisch für Datenarchitektur, auch für Prozesse/Journeys nutzbar. |
| `05 Diagramme/01 way-of-working-kreis` | `05 Diagramme/01 konzentrische-kreise` | War an ein einziges DAYONE-internes Organisationsmodell gebunden. Struktur ist ein generisches Ringmodell (Reifegrad, Zwiebelmodell, Prioritätsringe etc.). |
| `05 Diagramme/02 case-study-diagrammkarte` | `05 Diagramme/02 diagrammkarte` | "Case Study" war nur Namensbestandteil, nichts an der Struktur (zentrierte Eyebrow + Diagramm-Box + Titel/Subtitel) ist case-study-spezifisch. |
| `07 Media/01 screenshot-showcase` | `07 Media/01 bild-feature-liste` | Struktur ist Bild+Text wie `headline-text-bild`, nur mit Versions-/Feature-Bullet-Layout statt Fließtext — nicht auf "Screenshot" beschränkt. |
| `08 Menschen/02 personen-intro` | `08 Menschen/02 bild-intro` | Struktur (Bild + Titel/Unterzeile, zwei Spalten) ist auch für Produkt-/Tool-Intros nutzbar, nicht nur Personen. Content-Felder (Name/Rolle) bleiben als sinnvoller Default für den häufigsten Fall. |
| `09 Referenzen/02 facts-figures` | `09 Referenzen/02 bild-kennzahlenliste` | Name legte "Unternehmenskennzahlen" fest; Struktur ist generisch Bild + Definitionsliste. |
| `09 Referenzen/03 case-study-ziele` | `09 Referenzen/03 headline-liste` | Ernsts eigenes Beispiel: strukturell nur "Headline links, Pfeil-Liste rechts", nichts Case-Study-Spezifisches. |

Kategorien/Nummerierung (`03 Inhalt`, `09 Referenzen`, …) und Positionen
unverändert gelassen, um Folgeschäden (Umsortierung aller nachfolgenden Module)
zu vermeiden — nur die Blattnamen wurden generalisiert.

## Was überall mit-aktualisiert wurde

- **Figma**: `node.name` der 8 Komponenten umbenannt (via `use_figma`,
  editierbar bestätigt über `whoami`/Live-Verbindung). Zusätzlich die
  Cross-Referenzen auf die alten Namen in den Figma-**Beschreibungen** von
  `00 Elemente/02 karte`, `03 Inhalt/02 headline-textraster`,
  `07 Media/04 grossbild`, `07 Media/02 device-mockup` (ABGRENZUNG/EINGESETZT-IN-
  Abschnitte) korrigiert.
- **Code**: Baustein-Dateien umbenannt (`bausteine/*.html`) inkl. `data-modul`-
  Attribut; `data/descriptions/*.txt` umbenannt; `data/figma-komponenten.json`
  aktualisiert; `data/modul-zuordnung.json` (Keys + interne CSS-Klassen +
  `genau`-Regel entfernt bei kartenraster); interne CSS-Klassennamen in den
  betroffenen Bausteinen an die neuen Namen angeglichen (z. B.
  `.personen-intro` → `.bild-intro`, `.wow-kreis` → `.kreis-modell`,
  `.showcase*` → `.bild-feature*`, `.facts*` → `.bild-liste*`/`.kennzahlenliste*`,
  `.cs-ziele` → `.headline-liste`, `.karten-3er-head` → `.kartenraster-kopf`);
  Beispiel-Erwähnungen in `tools/bauen.py`, `tools/katalog_bauen.py`,
  `tools/pruefen.py`, `skill/SKILL.md`, `referenzen/scroll-patterns.md`
  korrigiert.
- Danach komplett neu gebaut/geprüft: `tools/katalog_bauen.py` →
  `tools/bauen.py` → `tools/pruefen.py` (starter.html + modul-galerie.html,
  beide sauber) → `tools/selbsttest.py` (18/18) → `tools/skill_bauen.py`
  (Skill-Paket neu gepackt).

## Bewusst NICHT angefasst

- `tools/seed_bestehende.py` — einmaliges historisches Migrationsskript,
  dokumentiert den Ursprungszustand, keine aktive Codepfad-Relevanz.

## Nachtrag (überholt einen früheren Stand dieses Docs)

`index.html` (Repo-Root) wurde in diesem Durchgang zunächst bewusst NICHT
angefasst (Begründung damals: eigenständig eingefrorener Demo-Export, kein
Teil der aktiven Bausteine-Pipeline). Das war falsch: `index.html` wird von
der CI (`.github/workflows/qualitaet.yml`, Schritt 4) ebenfalls mit
`tools/pruefen.py` geprüft. Der alte `data-modul`-Wert
(`09 Referenzen/02 facts-figures`) verursachte dadurch einen echten,
blockierenden CI-Fehler (`modulkennung`: Modul existiert in Figma nicht
mehr). Fix: `data-modul`-Wert und ein Kommentar in `index.html` per
Nachtrags-Commit korrigiert, komplette CI-Pipeline lokal reproduziert und
grün verifiziert (Commit `a4812bb`, von Ernst gepusht). `index.html` bleibt
aber weiterhin eine eigene, vollständige CSS-Kopie (nicht Teil der
Bausteine-Pipeline für Inhalte) — Empfehlung weiterhin: bei Gelegenheit neu
aus der aktuellen Pipeline bauen statt einzeln nachzupatchen, sonst läuft er
mit der Zeit wieder auseinander.

## Verifiziert

`tools/pruefen.py` auf `starter.html` + `modul-galerie.html`: beide sauber.
`tools/selbsttest.py`: 18/18 bestanden. Repo-weite Grep-Suche nach allen 8
Altnamen: keine Treffer mehr außer den bewusst ausgenommenen Stellen (siehe
Nachtrag oben für den korrigierten Stand zu `index.html`).
