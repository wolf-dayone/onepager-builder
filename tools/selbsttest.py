#!/usr/bin/env python3
"""Prueft den Pruefer.

    python3 tools/selbsttest.py

Nimmt die gebaute starter.html, baut je einen bekannten Fehler ein und
verlangt, dass der Lint genau diesen findet. Ausserdem: die unveraenderte
Datei muss sauber durchlaufen.

Der Grund fuer diese Datei: waehrend der Entwicklung hat der Mobil-Check
zweimal nichts gemeldet, obwohl die Regel wirklich fehlte - einmal wegen
einer zu engen Regex, einmal weil einzeilige Media Queries die Zustands-
verfolgung zerlegt haben. Ein Check, der bei kaputtem Input schweigt, ist
schlimmer als kein Check: er erzeugt Vertrauen, das er nicht deckt.
"""
import json
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pruefen import pruefe_datei, FEHLER  # noqa: E402

WURZEL = pathlib.Path(__file__).resolve().parent.parent
VORLAGE = WURZEL / "starter.html"

# (Name, Sabotage-Funktion, erwartete Regel)
FAELLE = [
    ("Platzhalter im Text",
     lambda s: s.replace("[Check it out.]", "[Check it out.]").replace(
         "<title>[Titel der Präsentation] — DAYONE</title>",
         "<title>Fertige Seite</title>"),
     "platzhalter"),

    ("Roh-Hexwert im CSS",
     lambda s: s.replace(".divider{display:flex",
                         ".divider{color:#abc;display:flex"),
     "tokens"),

    ("Schriftgröße ohne Figma-Entsprechung",
     lambda s: s.replace(".lead{font-size:var(--text-body-l)",
                         ".lead{font-size:23px"),
     "tokens"),

    ("Kapitel ohne data-chapter-title",
     lambda s: s.replace('data-chapter="01" data-chapter-title="[Kapitelname]"',
                         'data-chapter="01"', 1),
     "kapitel"),

    ("Kapitelmarker passt nicht zur Kapitelnummer",
     lambda s: s.replace('<p class="eyebrow is-centered">01 —',
                         '<p class="eyebrow is-centered">07 —', 1),
     "kapitelmarker"),

    ("Zweiter Hero",
     lambda s: s.replace("</body>", '<header class="hero"></header></body>'),
     "geruest"),

    ("prefers-reduced-motion entfernt",
     lambda s: s.replace("prefers-reduced-motion", "prefers-nichts"),
     "bewegung"),

    ("Mehrspaltiges Raster ohne Mobilregel",
     lambda s: s.replace(
         "@media(max-width:900px){.sticky-list{grid-template-columns:1fr;"
         "gap:var(--space-12)}.sticky-list .left{position:static}}", ""),
     "mobil"),

    ("CTA-Button zu flach für den Daumen",
     lambda s: s.replace("min-height:44px", "min-height:32px"),
     "touch"),

    ("Roobert eingebettet",
     lambda s: s.replace("<style>",
                         "<style>@font-face{font-family:Roobert;src:url(r.woff2)}", 1),
     "schrift"),

    # Die Weekly-Vorlage enthaelt kein <img>; fuer diesen Fall eins einsetzen.
    ("Bild ohne alt-Attribut",
     lambda s: s.replace("<blockquote>",
                         '<img src="a.jpg" loading="lazy"><blockquote>', 1),
     "bilder"),

    # Medien-Blocker: ein Bild, dessen src-Attribut noch den Figma-Platzhalter
    # traegt (z.B. aus bausteine/07-media-04-grossbild.html unverandert
    # uebernommen), darf eine fertige Seite nicht mehr passieren.
    ("Bild-Platzhalter im src nicht ersetzt",
     lambda s: s.replace("<blockquote>",
                         '<img src="[bild.jpg]" alt="Team beim Workshop" '
                         'loading="lazy"><blockquote>', 1),
     "platzhalter"),

    # Aus dem ersten Blindtest: eine fertige Seite ging mit zwei toten
    # CTA-Buttons raus, ohne dass Lint oder Handpruefung es meldeten.
    ("CTA-Button ohne Ziel",
     lambda s: s.replace('href="[URL]"', 'href="#"', 1),
     "links"),

    ("Anker zeigt auf eine id, die es nicht gibt",
     lambda s: s.replace('href="#hero"', 'href="#gibt-es-nicht"', 1),
     "links"),

    # Dreimal dasselbe Modul liest sich wie eine Formatierung, nicht wie
    # eine Aussage (Wunsch aus dem Praxistest).
    ("Dreimal dasselbe Modul",
     lambda s: s.replace(
         'data-modul="04 Daten/01 kennzahlen-grid"',
         'data-modul="03 Inhalt/03 sticky-nummernliste"').replace(
         'data-modul="08 Menschen/03 quote-block"',
         'data-modul="03 Inhalt/03 sticky-nummernliste"'),
     "vielfalt"),

    ("Agenda bei zu wenigen Kapiteln",
     lambda s: s.replace('data-chapter="04"', 'data-chapter-weg="04"').replace(
         'data-chapter="05"', 'data-chapter-weg="05"'),
     "agenda"),

    ("Modul mit erfundenem data-modul",
     lambda s: s.replace('data-modul="08 Menschen/03 quote-block"',
                         'data-modul="08 Menschen/09 gibt-es-nicht"'),
     "modulkennung"),
]


def lauf(inhalt, regeln, zuordnung, ist_vorlage=True):
    with tempfile.TemporaryDirectory() as ordner:
        pfad = pathlib.Path(ordner) / "probe.html"
        pfad.write_text(inhalt, encoding="utf-8")
        return pruefe_datei(pfad, regeln, zuordnung, ist_vorlage)


def main():
    if not VORLAGE.exists():
        sys.exit("starter.html fehlt — zuerst tools/bauen.py laufen lassen.")
    regeln = json.loads((WURZEL / "data" / "regeln.json").read_text())
    zuordnung = json.loads(
        (WURZEL / "data" / "modul-zuordnung.json").read_text())["module"]
    original = VORLAGE.read_text(encoding="utf-8")

    fehlgeschlagen = []

    # 1) Die unveraenderte Vorlage muss sauber sein.
    befund = lauf(original, regeln, zuordnung)
    harte = [x for x in befund if x["grad"] == FEHLER]
    if harte:
        fehlgeschlagen.append(
            f"starter.html ist nicht sauber: {harte[0]['regel']} — {harte[0]['text']}")
        print("  FEHLT   starter.html läuft nicht sauber durch")
    else:
        print("  ok      starter.html läuft sauber durch")

    # 2) Jede Sabotage muss genau ihre Regel ausloesen.
    for name, sabotage, erwartete_regel in FAELLE:
        kaputt = sabotage(original)
        if kaputt == original:
            fehlgeschlagen.append(f"{name}: Sabotage hat nichts verändert")
            print(f"  FEHLT   {name} — Sabotage griff nicht")
            continue
        # Platzhalter werden in Vorlagen nicht geprueft: dieser Fall braucht
        # den Modus einer fertigen Seite.
        ist_vorlage = erwartete_regel != "platzhalter"
        befund = lauf(kaputt, regeln, zuordnung, ist_vorlage)
        getroffen = [x for x in befund if x["regel"] == erwartete_regel]
        if getroffen:
            print(f"  ok      {name} → {erwartete_regel}")
        else:
            gefunden = sorted({x['regel'] for x in befund}) or ["nichts"]
            fehlgeschlagen.append(
                f"{name}: erwartet '{erwartete_regel}', gemeldet: {', '.join(gefunden)}")
            print(f"  FEHLT   {name} — erwartet '{erwartete_regel}', "
                  f"gemeldet: {', '.join(gefunden)}")

    print()
    if fehlgeschlagen:
        print(f"{len(fehlgeschlagen)} von {len(FAELLE) + 1} Prüfungen fehlgeschlagen:")
        for z in fehlgeschlagen:
            print(f"  · {z}")
        return 1
    print(f"Alle {len(FAELLE) + 1} Prüfungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
