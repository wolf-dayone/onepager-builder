#!/usr/bin/env python3
"""Baut aus den Figma-Descriptions den Modul-Katalog und die Pruefregeln.

    python3 tools/katalog_bauen.py

Liest:   data/figma-komponenten.json  (Namen + Node-IDs, aus Figma)
         data/descriptions/*.txt      (Component-Descriptions, aus Figma)
Schreibt: referenzen/module-katalog.md (fuer Menschen)
          data/regeln.json             (fuer tools/pruefen.py)

Beides ist generiert - Aenderungen gehoeren in die Figma-Description, nicht
in diese Dateien. Das ist der ganze Punkt: Figma ist die einzige Quelle.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from figma_text import zerlegen, aufzaehlung  # noqa: E402

WURZEL = pathlib.Path(__file__).resolve().parent.parent
KOMPONENTEN = WURZEL / "data" / "figma-komponenten.json"
BESCHREIBUNGEN = WURZEL / "data" / "descriptions"
KATALOG = WURZEL / "referenzen" / "module-katalog.md"
REGELN = WURZEL / "data" / "regeln.json"

# Steht wortgleich in 33 von 34 Descriptions. Gehoert einmal in die
# Gestaltungsprinzipien, nicht 33-mal in den Katalog.
FARBE_STANDARD = "Hell (Sand/100) oder Dunkel (Gray/900), frei wählbar"


def slug(name):
    """'03 Inhalt/03 sticky-nummernliste' -> '03-inhalt-03-sticky-nummernliste'."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def kurzname(name):
    """'03 Inhalt/03 sticky-nummernliste' -> 'sticky-nummernliste'."""
    return name.split("/")[-1].split(" ", 1)[-1]


def kategorie(name):
    """'03 Inhalt/03 sticky-nummernliste' -> '03 Inhalt'."""
    return name.split("/")[0]


# --- Zahlenregeln aus dem FUELLEN-Abschnitt ziehen -------------------------
# "3–5 Punkte", "Max. 4–5 Spalten", "12–24 Logos", "min. 180 px", "Max. 2 Buttons"
SPANNE = re.compile(
    r"(?:(?P<max_prefix>max\.?|höchstens)\s+)?"
    r"(?P<von>\d+)\s*[–—-]\s*(?P<bis>\d+)\s+(?P<einheit>[A-Za-zÄÖÜäöüß/-]+)",
    re.IGNORECASE,
)
OBERGRENZE = re.compile(
    r"(?:max\.?|höchstens|nicht mehr als)\s+(?P<bis>\d+)\s+(?P<einheit>[A-Za-zÄÖÜäöüß/-]+)",
    re.IGNORECASE,
)
MINDEST = re.compile(
    r"(?:min\.?|mindestens)\s+(?P<von>[\d.]+)\s*(?P<einheit>px|%|[A-Za-zÄÖÜäöüß/-]+)",
    re.IGNORECASE,
)

# Einheiten, die keine Stueckzahl eines wiederholbaren Elements sind.
KEINE_ANZAHL = {"sätze", "satze", "zeilen", "wörter", "worter", "px", "spalten von",
                "std", "stunden", "wochen", "monate", "jahre", "zeichen"}


def zahlenregeln(fuellen_punkte):
    """Findet Stueckzahl-Grenzen ('3-5 Punkte') in den FUELLEN-Stichpunkten."""
    gefunden = []
    for punkt in fuellen_punkte:
        for m in SPANNE.finditer(punkt):
            einheit = m.group("einheit").lower().rstrip(".,")
            if einheit in KEINE_ANZAHL:
                continue
            gefunden.append({
                "min": int(m.group("von")),
                "max": int(m.group("bis")),
                "einheit": m.group("einheit").rstrip(".,"),
                "quelle": punkt,
            })
        for m in OBERGRENZE.finditer(punkt):
            einheit = m.group("einheit").lower().rstrip(".,")
            if einheit in KEINE_ANZAHL or SPANNE.search(punkt):
                continue
            gefunden.append({
                "min": None,
                "max": int(m.group("bis")),
                "einheit": m.group("einheit").rstrip(".,"),
                "quelle": punkt,
            })
        for m in MINDEST.finditer(punkt):
            einheit = m.group("einheit").lower().rstrip(".,")
            # px/% bleiben wie bisher immer erlaubt (Groessen-Angaben, keine
            # Stueckzahl eines wiederholbaren Elements). Fuer alles andere
            # (neu: generische Einheiten wie "Punkte") gilt dieselbe
            # KEINE_ANZAHL-Filterung wie bei SPANNE/OBERGRENZE.
            if einheit not in ("px", "%"):
                if einheit in KEINE_ANZAHL or SPANNE.search(punkt):
                    continue
            wert = float(m.group("von"))
            gefunden.append({
                "min": int(wert) if einheit not in ("px", "%") and wert.is_integer() else wert,
                "max": None,
                "einheit": m.group("einheit").rstrip(".,"),
                "quelle": punkt,
            })
    return gefunden


def einlesen():
    daten = json.loads(KOMPONENTEN.read_text())
    module = []
    for eintrag in daten["komponenten"]:
        name = eintrag["name"]
        pfad = BESCHREIBUNGEN / f"{slug(name)}.txt"
        if not pfad.exists():
            print(f"  ! keine Description: {name}", file=sys.stderr)
            abschnitte = {}
        else:
            abschnitte = zerlegen(pfad.read_text())

        fuellen = aufzaehlung(abschnitte.get("FÜLLEN", ""))
        farbe = abschnitte.get("FARBE", "")
        module.append({
            "name": name,
            "kurzname": kurzname(name),
            "kategorie": kategorie(name),
            "slug": slug(name),
            "nodeId": eintrag["nodeId"],
            "abschnitte": abschnitte,
            "fuellen": fuellen,
            "grenzen": zahlenregeln(fuellen),
            "farbe_frei": FARBE_STANDARD in farbe,
            "hat_regeln": bool(abschnitte.get("ZWECK")),
        })
    return daten, module


# --- Katalog (Markdown) ----------------------------------------------------
REIHENFOLGE = ["ZWECK", "WANN VERWENDEN", "ABGRENZUNG", "AUFBAU", "VERHALTEN",
               "VARIANTEN", "FÜLLEN", "SCROLL", "EINGESETZT IN",
               "KEIN DOPPELTER KAPITELMARKER", "HINWEIS", "TODO"]


def katalog_schreiben(daten, module):
    z = []
    a = z.append
    a("<!-- GENERIERT von tools/katalog_bauen.py - nicht von Hand bearbeiten. -->")
    a("<!-- Quelle: Figma-Component-Descriptions. Aenderungen dort vornehmen. -->")
    a("")
    a("# Modul-Katalog")
    a("")
    a(f"{len(module)} Bausteine aus der Figma-Datei **DAYONE | AI-ready slides**, "
      f"Seite *{daten['sectionName']}*.")
    a("Die Namen hier sind **exakt** die Figma-Layernamen — wer im Onepager ein Modul")
    a("nennt, findet es in Figma unter demselben Namen.")
    a("")
    a(f"Datei: `https://www.figma.com/design/{daten['fileKey']}/"
      f"DAYONE-%7C-AI-ready-slides` · Stand: {daten['stand']}")
    a("")
    a("## Farbe gilt für alle Module")
    a("")
    a("Jedes Modul ist **hell (Sand/100) oder dunkel (Gray/900), frei wählbar**.")
    a("Ein Farbwechsel markiert einen neuen Sinnabschnitt; gleiche Farbe hält")
    a("zusammengehörige Abschnitte optisch als Einheit. Es gibt **keine feste**")
    a("**Zuordnung** von Farbe zu Modul oder Kapiteltyp — Notizen wie „· dunkel“")
    a("an einzelnen Modulen sind falsch und wurden entfernt.")
    a("")
    a("## Mindesthöhe gilt für alle Module")
    a("")
    a("Jedes Modul ist **mindestens eine Bildschirmhöhe groß** (Code: `100svh`;")
    a("in Figma stellvertretend als 960-px-Rahmen dargestellt — der Rahmen steht")
    a("für „Viewport“, nicht für einen festen Pixelwert). **Mit mehr Inhalt darf**")
    a("**ein Modul wachsen**, verkürzt werden darf es nicht. Eine eigene, kleinere")
    a("`min-height` auf Sektionsebene ist nur zulässig, wenn hier ausdrücklich als")
    a("Ausnahme dokumentiert — aktuell gibt es **keine** Ausnahme.")
    a("")
    a("## Eyebrow ist optional")
    a("")
    a("Die Eyebrow-Zeile (`[NN] — [Kapitelname]`) markiert ein neues, **in der**")
    a("**Kapitel-Nav verlinktes Kapitel** — nicht mehr und nicht weniger. Mehrere")
    a("Module (u. a. `big-statement`, `grossbild`, `bild-kennzahlenliste`,")
    a("`headline-liste`, `device-mockup`, `diagrammkarte`,")
    a("`bild-intro`, `qr-tool-verweis`) tragen in Figma eine eigene, aber")
    a("**optionale** Eyebrow für den Fall, dass sie ein Kapitel eröffnen. Wird ein")
    a("solches Modul **innerhalb** eines Kapitels eingesetzt (als Beat, nicht als")
    a("Kapitelstart), gehört die Eyebrow-Zeile **gelöscht** — pro Kapitel trägt nur")
    a("die jeweils erste Sektion den Kapitelmarker (siehe „KEIN DOPPELTER")
    a("KAPITELMARKER“ weiter unten). Eröffnet das Modul dagegen selbst ein Kapitel,")
    a("braucht es zusätzlich `data-chapter`/`data-chapter-title`/`id` auf der")
    a("Sektion, sonst bleibt die Nummer unverlinkt und `tools/bauen.py` numeriert")
    a("sie nicht (numeriert wird nur, wenn `data-chapter=\"[NN]\"` vorkommt).")
    a("")

    ohne = [m for m in module if not m["hat_regeln"]]
    if ohne:
        a("> **Lücke in der Quelle:** "
          + ", ".join(f"`{m['name']}`" for m in ohne)
          + " hat in Figma keine Zweck-/Füllregeln. Bis das nachgetragen ist,")
        a("> gibt es für dieses Modul nichts zu prüfen.")
        a("")

    aktuelle_kategorie = None
    for m in module:
        if m["kategorie"] != aktuelle_kategorie:
            aktuelle_kategorie = m["kategorie"]
            a("---")
            a("")
            a(f"## {aktuelle_kategorie}")
            a("")
        a(f"### `{m['name']}`")
        a("")
        a(f"<sub>Figma-Node `{m['nodeId']}`</sub>")
        a("")
        for schluessel in REIHENFOLGE:
            if schluessel not in m["abschnitte"]:
                continue
            inhalt = m["abschnitte"][schluessel]
            punkte = aufzaehlung(inhalt)
            if len(punkte) > 1:
                a(f"**{schluessel}**")
                a("")
                for p in punkte:
                    a(f"- {p}")
            else:
                a(f"**{schluessel}** — {inhalt}")
            a("")
        if m["grenzen"]:
            regeln = ", ".join(
                (f"{g['min']}–{g['max']} {g['einheit']}" if g["min"] and g["max"]
                 else f"max. {g['max']} {g['einheit']}" if g["max"]
                 else f"min. {g['min']} {g['einheit']}")
                for g in m["grenzen"])
            a(f"<sub>Maschinell geprüft: {regeln}</sub>")
            a("")

    KATALOG.parent.mkdir(exist_ok=True)
    KATALOG.write_text("\n".join(z) + "\n")


def regeln_schreiben(daten, module):
    REGELN.write_text(json.dumps({
        "_hinweis": "GENERIERT von tools/katalog_bauen.py. Quelle: Figma-Descriptions.",
        "fileKey": daten["fileKey"],
        "stand": daten["stand"],
        "module": {m["name"]: {
            "kurzname": m["kurzname"],
            "kategorie": m["kategorie"],
            "slug": m["slug"],
            "nodeId": m["nodeId"],
            "zweck": m["abschnitte"].get("ZWECK", ""),
            "abgrenzung": m["abschnitte"].get("ABGRENZUNG", ""),
            "fuellen": m["fuellen"],
            "grenzen": m["grenzen"],
            "farbe_frei": m["farbe_frei"],
            "hat_regeln": m["hat_regeln"],
        } for m in module},
    }, ensure_ascii=False, indent=2) + "\n")


def main():
    daten, module = einlesen()
    katalog_schreiben(daten, module)
    regeln_schreiben(daten, module)
    mit_grenzen = sum(1 for m in module if m["grenzen"])
    print(f"{len(module)} Module -> {KATALOG.relative_to(WURZEL)}")
    print(f"{mit_grenzen} Module mit maschinell prüfbaren Stückzahl-Grenzen "
          f"-> {REGELN.relative_to(WURZEL)}")


if __name__ == "__main__":
    main()
