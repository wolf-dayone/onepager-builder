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

Deployment über den Vercel-Connector (Tool `deploy_to_vercel`) oder per Git-Repo.
Beides braucht einen Vercel-Zugang — wer keinen hat, bleibt bei Weg A und lässt jemanden
mit Zugang deployen.

**Zugriffsschutz:** Kundeninhalte gehören nicht offen ins Netz. In den Vercel-Projekt-
einstellungen Password Protection oder Vercel Authentication aktivieren
(`cupra-pitch` ist so geschützt). Vor dem Teilen prüfen — nicht danach.

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
