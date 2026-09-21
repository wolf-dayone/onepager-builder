# Ausliefern

Zwei Wege. Welcher passt, hängt allein daran, ob der Onepager eine **eigene URL** braucht.

| | Einzelne HTML-Datei | Vercel-Deployment |
|---|---|---|
| Ergebnis | eine `.html`-Datei | öffentliche URL |
| Aufwand | keiner | einmalig einrichten |
| Teilen | Datei verschicken, im Browser öffnen | Link verschicken |
| Passt für | Weeklies, interne Updates, schnelle Reviews | Kundenpitches, alles mit eigener URL |

**Im Zweifel die HTML-Datei.** Sie funktioniert sofort, braucht keine Zugänge und lässt
sich jederzeit nachträglich deployen.

---

## Weg A — Einzelne HTML-Datei (Standard)

`assets/starter.html` kopieren, Platzhalter ersetzen, nicht gebrauchte Sektionen löschen,
fehlende ergänzen. Alles ist in einer Datei: Styles, Skripte, Struktur. Keine
Build-Schritte, keine Abhängigkeiten, kein CDN — die Seite funktioniert auch offline.

Die Datei im Output-Ordner ablegen und mit `present_files` übergeben. Ohne diesen Schritt
ist die Datei für den Menschen nicht erreichbar.

### Bilder
Ohne eigene URL gibt es zwei Möglichkeiten:
1. **Bilder daneben legen** und relativ verlinken (`<img src="bild.png">`) — dann müssen
   Datei und Bilder zusammen verschickt werden.
2. **Bilder als Data-URI einbetten** — alles bleibt in einer Datei, aber sie wird groß.
   Ab etwa 5 MB wird das unhandlich; dann besser Weg B.

Vorher immer komprimieren. Ein Screenshot braucht selten mehr als 1600 px Breite.

### Schrift
Roobert ist lizenzpflichtig und liegt nicht bei. Die Datei nutzt
`font-family: "Roobert", "Inter", system-ui` — wer Roobert lokal installiert hat, sieht
sie; alle anderen bekommen einen sauberen Fallback. Für ein Deployment mit korrekter
Schrift die Webfont-Dateien selbst hosten und per `@font-face` einbinden. Roobert
**nicht** in eine Datei einbetten, die das Haus verlässt — das wäre eine Lizenzverletzung.

---

## Weg B — Vercel

Für alles, was eine eigene URL braucht. Die bestehenden DAYONE-Onepager liegen dort
(`dayone-weekly-presentations`, `ny-pitch-three`, `cupra-pitch`).

Das einfachste Setup ist eine statische Seite — dieselbe HTML-Datei, nur deployed:

```
mein-onepager/
├── index.html      (das fertige Dokument)
└── assets/         (Bilder, ggf. Roobert-Webfonts)
```

Am schnellsten geht es über den Vercel-Connector (Tool `deploy_to_vercel`) — damit
entfällt der Git-Schritt komplett, und es reicht ein Vercel-Zugang. Wer die Seite aber
später selbst weiterpflegen will oder ohnehin ein GitHub-Konto hat, nimmt besser den
Weg über ein Git-Repo — jede Änderung landet dann mit einem `git push` automatisch live.
Beide Wege brauchen einen Vercel-Zugang; wer keinen hat, bleibt bei Weg A und lässt
jemanden mit Zugang deployen.

### Schritt für Schritt: Git-Repo → GitHub → Vercel

Diese Schritte gemeinsam mit dem Menschen durchgehen, nicht nur auflisten — vor jedem
kurz erklären, was er bewirkt, und nach jedem kurz bestätigen, dass er geklappt hat.
Ist eine Shell mit `git`/`gh` vorhanden, die Befehle selbst ausführen; der Mensch
bestätigt nur Zugänge (GitHub-Login, Vercel-Login) und Entscheidungen (Repo-Name,
privat oder öffentlich).

1. **Projektordner vorbereiten.** Die fertige `index.html` (und ein `assets/`-Ordner
   für Bilder, falls vorhanden) liegen zusammen in einem eigenen Ordner — siehe
   Struktur oben. Noch offene `[Platzhalter]` vorher ersetzen, sonst landen sie live.

2. **Lokales Git-Repo anlegen.**
   ```
   cd mein-onepager
   git init
   git add .
   git commit -m "Erster Entwurf Onepager"
   ```
   `git init` macht aus dem Ordner ein Repo, das Änderungen nachvollziehen kann;
   `git add` merkt die Dateien vor, `git commit` speichert diesen Stand als ersten
   Schnappschuss. Ohne GitHub-Konto geht es hier erstmal nicht weiter — dann Schritt 3
   überspringen und direkt mit dem Vercel-Connector (oben) arbeiten.

3. **Bei GitHub veröffentlichen.** Mit der GitHub-CLI (`gh`), falls vorhanden:
   ```
   gh repo create mein-onepager --private --source=. --remote=origin --push
   ```
   Das legt das Repo auf GitHub an (privat, sofern nicht anders gewünscht — bei
   Kundeninhalten immer privat), verknüpft es mit dem lokalen Ordner und lädt den
   ersten Stand hoch. Ohne `gh`: Repo auf github.com anlegen, dann
   ```
   git remote add origin <die-von-github-angezeigte-URL>
   git push -u origin main
   ```
   Fehlt der GitHub-Zugang komplett, hier anhalten und das dem Menschen sagen —
   nicht improvisieren.

4. **Mit Vercel verbinden.** Auf vercel.com „Add New… → Project" wählen, das gerade
   erstellte GitHub-Repo importieren und mit den Standardeinstellungen deployen (es ist
   statisches HTML, es gibt nichts zu konfigurieren). Nach ein bis zwei Minuten steht
   die live-URL fest. Alternativ per CLI: `vercel` im Projektordner ausführen und den
   Dialogen folgen (fragt beim ersten Mal nach Login und Team).

5. **Zugriffsschutz einrichten, falls Kundeninhalte betroffen sind.** In den
   Vercel-Projekteinstellungen Password Protection oder Vercel Authentication
   aktivieren (`cupra-pitch` ist so geschützt) — **vor** dem Teilen der URL, nicht
   danach.

6. **Fertige URL nennen.** Die von Vercel vergebene URL (oder eine später eingerichtete
   eigene Domain) an den Menschen weitergeben, zusammen mit einer aktiven Erinnerung
   an den Zugriffsschutz bei Kundeninhalten.

**Später etwas ändern?** Datei lokal bearbeiten, dann:
```
git add .
git commit -m "Beschreibung der Änderung"
git push
```
Vercel deployt bei jedem Push automatisch neu — die URL bleibt gleich.

Wenn ein React/Next.js-Projekt gewünscht ist, gilt zusätzlich das DAYONE UI Kit
(`ui.dayone.de`): `npx shadcn@latest init --base radix --preset nova`, dann
`npx shadcn@latest add dayone-org/ui/all`. Für einen reinen Onepager ist das aber
Overkill — statisches HTML reicht und ist schneller.

---

## Vor dem Verschicken

- [ ] Alle `[Platzhalter]` ersetzt? (Suche nach `[` in der Datei)
- [ ] Kapitelnummern in Eyebrows und Navigation stimmen überein
- [ ] Auf schmalem Fenster geprüft — Sticky-Spalten und Tabellen brechen dort zuerst
- [ ] Sensible Daten in Screenshots anonymisiert
- [ ] Zitate von den zitierten Personen freigegeben
- [ ] Bei Kundeninhalten: Zugriffsschutz aktiv

---

## Wenn du die Vorlagen selbst geändert hast

Dieser Skill ist ein **Build-Ergebnis**, keine Quelle. Er entsteht aus dem Repo
`onepager-builder` (`bausteine/`, `referenzen/`, `skill/SKILL.md`) über
`tools/skill_bauen.py`.

Das heißt: eine Änderung an einem Modul ist erst dann hier angekommen, wenn das
Paket neu gebaut **und in der Skill-Verwaltung hochgeladen** wurde. Ein Commit
allein genügt nicht — er ändert das Repo, nicht den installierten Skill. Genau
das ist schon zweimal passiert: der ausgelieferte Stand lag einmal sechs Module
und einmal zwei komplette Feedback-Runden hinter dem Repo, ohne dass es jemandem
auffiel.

Im Repo läuft der Bau automatisch bei jedem Commit (`git config core.hooksPath
tools/hooks`). Ob der **installierte** Skill noch hinterherhinkt, beantwortet:

```
python3 tools/skill_bauen.py --pruefen
```

Meldet er `UPLOAD NOETIG`, liegt der neue Stand als
`dist/dayonepager.skill` bereit und gehört in die Skill-Verwaltung. Bis
dahin bauen alle Kolleg:innen weiter mit der alten Fassung.
