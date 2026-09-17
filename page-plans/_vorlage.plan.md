<!-- Kopiervorlage fuer einen Page Plan. Fuer ein neues Projekt kopieren nach
     page-plans/<projekt-slug>.plan.md und ausfuellen - vor dem Bauen der
     eigentlichen Seite (SKILL.md, Schritt 2).

     Der Page Plan ist das Zwischenformat zwischen Inhalt und Seite: er macht
     Dramaturgie, Quellen und Modulwahl sichtbar UND gezielt aenderbar. "Bei
     Abschnitt 06 lieber Cards" bedeutet: nur diese eine Zeile aendern, den
     Rest der Tabelle unangetastet lassen und nur den betroffenen Abschnitt
     neu bauen - nicht die ganze Seite neu interpretieren.

     Der Plan ist ein Arbeitsdokument, kein weiteres Pflichtfeld: bei einem
     kurzen, klaren Auftrag reicht eine knappe Tabelle in wenigen Zeilen. Er
     ersetzt nicht referenzen/module-katalog.md (Regeln je Modul) und nicht
     data/modul-zuordnung.json (Modul zu Code) - er verweist nur darauf. -->

# Page Plan — [Projektname]

## Seite

| Feld | Wert |
|---|---|
| Titel | [Arbeitstitel der Seite] |
| Anlass | [Weekly / Kundenpitch / Case Study / Credentials / …] |
| Zielgruppe | [z. B. Client Leadership, internes Team] |
| Zweck | [Was soll die Seite bei der Zielgruppe auslösen oder klären?] |

## Abschnitte

Reihenfolge = Dramaturgie der Seite. `Modul` ist der **exakte Figma-Name** aus
`referenzen/module-katalog.md` — derselbe String, der im gebauten HTML als
`data-modul="…"` steht. Eine Zeile ändern betrifft nur diesen Abschnitt.

| # | Zweck des Abschnitts | Quelle | Modul (Figma-Name) | Medien | Status |
|---|---|---|---|---|---|
| 01 | [Was dieser Abschnitt zeigt oder beantwortet] | [Briefing / Slide 4–7 / Transkript 00:12:30 / Meeting-Notiz] | `01 Einstieg/01 cover-hero` | [client-logo.svg / keine] | offen |
| 02 | … | … | … | … | … |

**Medien:** Dateiname, wenn vorhanden — sonst `fehlt: <was gebraucht wird>`.
Ein `fehlt:`-Eintrag hier muss unter „Unresolved" auftauchen (siehe unten);
`tools/pruefen.py` blockt außerdem jedes Modul, dessen Bild-Platzhalter beim
Bauen unverändert stehen bleibt.

**Status:** `offen` (noch nicht gebaut) · `gebaut` (im HTML umgesetzt) ·
`bestätigt` (mit dem Menschen abgestimmt, gilt als fertig).

## Unresolved

Alles, was noch fehlt, bevor die Seite fertig ist. Wird beim Übergeben
(SKILL.md, Schritt 9) unverändert weitergegeben — nicht nur erwähnt, sondern
als Liste, damit nichts stillschweigend durchrutscht.

- [ ] [z. B. Bild für Abschnitt 03 — Screenshot vom Prototyp]
- [ ] [z. B. Ziel-URL für den CTA-Button]
- [ ] [z. B. Freigabe des Zitats in Abschnitt 07 durch Name]

Leer lassen (nicht löschen), wenn nichts offen ist — eine leere Liste ist das
sichtbare Signal, dass vor dem Publish nichts mehr fehlt.

## Änderungsprotokoll

Kurzer Verlauf gezielter Korrekturen am Plan, damit nachvollziehbar bleibt,
warum eine Zeile von der ursprünglichen Dramaturgie abweicht. Neueste zuerst.

- [Datum]: Abschnitt [NN] von `[altes Modul]` auf `[neues Modul]` geändert —
  Anlass: „[was der Mensch dazu gesagt hat]".
