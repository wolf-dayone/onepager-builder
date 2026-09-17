#!/usr/bin/env python3
"""Baut aus bausteine/ die fertigen HTML-Dateien.

    python3 tools/bauen.py

Erzeugt:
  modul-galerie.html  alle 34 Module mit Dummy-Inhalt - Pruefstueck und
                      Kopiervorlage. Wer ein Modul braucht, holt es hier.
  starter.html        die erprobte Weekly-Dramaturgie, fertig zum Fuellen.

Beide sind Build-Ergebnisse. Geaendert wird in bausteine/, nie hier.

Die Kapitelnummern werden beim Bauen vergeben: [NN] im data-chapter, in der
id und im Kapitelmarker bekommen dieselbe Nummer. Damit ist der Fehler
"Kapitel 03 traegt den Marker 05" strukturell ausgeschlossen.
"""
import json
import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
B = WURZEL / "bausteine"
KOMPONENTEN = WURZEL / "data" / "figma-komponenten.json"

# Erprobte Abfolge fuer ein Weekly (referenzen/module-katalog.md).
DRAMATURGIE_WEEKLY = [
    "01 Einstieg/01 cover-hero",
    "01 Einstieg/02 agenda",
    "02 Struktur/01 section-divider",
    "03 Inhalt/03 sticky-nummernliste",
    "03 Inhalt/04 kartenraster",
    "03 Inhalt/05 prozess-schritte",
    "04 Daten/01 kennzahlen-grid",
    "08 Menschen/03 quote-block",
    "10 Abschluss/01 karten-karussell",
    "10 Abschluss/03 cta-footer",
]


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


BRAUCHT = re.compile(r"<!--\s*braucht:\s*(.+?)\s*-->")


def baustein(name, mit_abhaengigkeiten=True):
    """Liest einen Baustein und trennt <style> vom Markup.

    Ein Baustein kann per '<!-- braucht: <Figma-Name> -->' erklaeren, dass er
    das CSS eines anderen voraussetzt - so wie kartenraster und karten-karussell
    beide auf '00 Elemente/02 karte' aufbauen. Ohne diese Aufloesung faellt ein
    Modul auseinander, sobald das andere nicht mit auf der Seite liegt.
    """
    pfad = B / f"{slug(name)}.html"
    if not pfad.exists():
        sys.exit(f"Baustein fehlt: {pfad.relative_to(WURZEL)}")
    text = pfad.read_text(encoding="utf-8")

    vorher = []
    if mit_abhaengigkeiten:
        for abhaengig in BRAUCHT.findall(text):
            hilfs_bloecke, _ = baustein(abhaengig, mit_abhaengigkeiten=False)
            vorher.extend(hilfs_bloecke)

    m = re.search(r"<style>\n?(.*?)\n?</style>", text, re.DOTALL)
    eigenes = (m.group(1).strip() if m else "")
    markup = text[m.end():].strip() if m else BRAUCHT.sub("", text).strip()
    return [c for c in vorher + [eigenes] if c], markup


def nummerieren(markup, nummer):
    """Ersetzt [NN]/[nn] durch eine konkrete, ueberall gleiche Kapitelnummer."""
    return markup.replace("[NN]", nummer).replace("[nn]", nummer)


EYEBROW = re.compile(r"[ \t]*<p class=\"eyebrow[^\"]*\">.*?</p>\n?", re.DOTALL)


def marker_entfernen(markup):
    """Nimmt den Kapitelmarker aus einem Modul heraus.

    Figma, section-divider: pro Kapitel traegt nur die erste Sektion den
    Kapitelmarker. Steht ein Divider davor, gehoert er dorthin - die Sektion
    danach verliert ihren. Die Bausteine behalten ihren Marker, weil sie auch
    allein am Kapitelanfang stehen koennen.
    """
    return EYEBROW.sub("", markup, count=1)


HUELLE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titel}</title>
<!-- {stempel} -->
<style>
{css}
</style>
</head>
<body>

{symbole}

{inhalt}

<script>
{js}
</script>
</body>
</html>
"""


def zusammenbauen(titel, teile, stempel):
    """teile: Liste von (css-Bloecke, markup).

    CSS wird blockweise dedupliziert - ein Baustein, den zwei Module brauchen
    (die Karte), steht dadurch genau einmal in der fertigen Datei.
    """
    css_bloecke, gesehen = [], set()
    for bloecke, _ in teile:
        for block in bloecke:
            if block and block not in gesehen:
                gesehen.add(block)
                css_bloecke.append(block)

    # Tokens kommen aus referenzen/tokens.css - eine Quelle, kein zweiter
    # Satz Werte im Template, der stillschweigend auseinanderlaufen kann.
    tokens = (WURZEL / "referenzen" / "tokens.css").read_text().strip()
    basis_css = (B / "_basis.css").read_text().rstrip()
    if "/*__TOKENS__*/" not in basis_css:
        sys.exit("bausteine/_basis.css: Platzhalter /*__TOKENS__*/ fehlt.")
    basis_css = basis_css.replace("/*__TOKENS__*/", tokens)
    js = (B / "_basis.js").read_text().rstrip()
    symbole = (B / "_symbole.svg").read_text().strip()

    return HUELLE.format(
        titel=titel,
        stempel=stempel,
        css="\n\n".join([basis_css] + css_bloecke),
        symbole=symbole,
        inhalt="\n\n".join(m for _, m in teile if m),
        js=js,
    )


def stempel(daten):
    return (f"dayone-onepager · {len(daten['komponenten'])} Module · "
            f"Figma-Stand {daten['stand']} · gebaut mit tools/bauen.py")


# ------------------------------------------------------------------ Galerie
GALERIE_CSS = """/* ==== Galerie-Rahmen (nur in modul-galerie.html) ==== */
/* Kein sticky Modul-Kopf mehr zwischen den Sektionen (Ernst, 2026-09-17): die
   schwarzen Balken lenkten vom eigentlichen Effekt ab, den die Galerie ja
   gerade zeigen soll. Die Modulidentitaet liefert jetzt ausschliesslich die
   QA-Leiste (bausteine/_galerie-qa.js) unten am Bildschirmrand. Bewusst KEIN
   min-height:0-Override mehr - die Galerie
   ist jetzt die QA-Testflaeche, nicht nur ein Katalog zum Kopieren - jedes
   Modul soll exakt so gross gerendert werden wie in echten Onepagern, sonst
   verdeckt die Galerie selbst genau die Layout-Probleme, die sie aufdecken
   soll (z. B. vertikale Zentrierung, Whitespace bei kurzem Inhalt). Macht
   die Galerie deutlich laenger (34 Module x mind. 1 Viewporthoehe) - das ist
   der akzeptierte Tradeoff. */
.galerie-intro{padding:var(--space-24) var(--grid-margin)}
.galerie-baustein{padding:var(--space-16) var(--grid-margin)}"""

# ---- QA-Leiste: NUR in modul-galerie.html, wird beim Skill-Bauen entfernt ----
# (siehe tools/skill_bauen.py QA_STRIP) - deshalb zwischen den Sentinel-
# Kommentaren, an denen der Strip-Schritt den kompletten Block erkennt.
# Ausschliesslich Design-Tokens (var(--...)), damit tools/pruefen.py
# pruefe_tokens() (keine rohen Hex-/px-Werte) auch diese Datei sauber
# durchlaesst wie jeden anderen Baustein.
QA_CSS = """/* ==== QA-Leiste (nur in modul-galerie.html, siehe QA-ONLY-Marker) ==== */
body.galerie{padding-bottom:64px}
.qa-leiste{position:fixed;left:0;right:0;bottom:0;z-index:100;
  display:flex;flex-wrap:wrap;gap:var(--space-6);align-items:center;justify-content:space-between;
  padding:10px var(--grid-margin);background:var(--color-main-text);color:var(--color-bg);
  font-family:var(--font);font-size:var(--text-body-s);border-top:1px solid var(--gray-500)}
.qa-leiste button{font-family:inherit;font-size:inherit;cursor:pointer;
  background:var(--gray-500);color:var(--color-bg);border:1px solid var(--gray-400);
  border-radius:var(--radius-input);padding:6px 12px}
.qa-leiste button:hover{background:var(--gray-400)}
.qa-leiste button[aria-pressed="true"]{background:var(--sand-600);border-color:var(--sand-900);color:var(--color-main-text)}
.qa-info{display:flex;gap:var(--space-6);align-items:baseline;min-width:0}
.qa-info .qa-modul{font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.qa-info .qa-viewport{opacity:.6;white-space:nowrap}
.qa-aktionen{display:flex;flex-wrap:wrap;gap:8px}
/* "Animations: off" - rein CSS-getriebene Wirkung, siehe setAnimationsEnabled()
   in bausteine/_basis.js Abschnitt 10. !important, weil sie jede Modul-eigene
   transition/animation uebersteuern muss, unabhaengig von deren Spezifitaet. */
.qa-anim-off, .qa-anim-off *{transition:none!important;animation:none!important}"""


def _qa_leiste_block():
    """Baut den QA-ONLY-Block (Style + Skript) fuer modul-galerie.html.

    Zwischen Sentinel-Kommentaren, damit tools/skill_bauen.py ihn beim
    Verpacken des Skills komplett herausschneiden kann - die QA-Leiste ist
    ein Werkzeug fuer dieses Repo, kein Bestandteil ausgelieferter Seiten.
    """
    qa_js = (B / "_galerie-qa.js").read_text(encoding="utf-8").rstrip()
    return (
        "<!-- QA-ONLY:START -->\n"
        f"<style>\n{QA_CSS}\n</style>\n"
        f"<script>\n{qa_js}\n</script>\n"
        "<!-- QA-ONLY:END -->"
    )


def galerie_bauen(daten):
    teile = [([GALERIE_CSS], "")]
    zuordnung = json.loads(
        (WURZEL / "data" / "modul-zuordnung.json").read_text())["module"]

    teile.append(([], f"""<div class="galerie-intro">
  <h1 class="h1">Modul-Galerie</h1>
  <p class="lead" style="margin-top:var(--space-6);max-width:680px">Alle
  {len(daten['komponenten'])} Bausteine aus der Figma-Datei
  <em>DAYONE&nbsp;|&nbsp;AI-ready&nbsp;slides</em>, jeweils einmal mit
  Platzhalter-Inhalt. Diese Seite ist beides: Pr&uuml;fst&uuml;ck f&uuml;r
  jede &Auml;nderung am System und Kopiervorlage f&uuml;r neue Seiten.</p>
  <p class="small" style="margin-top:var(--space-6);color:var(--color-text)">Regeln
  zu jedem Modul: <code>referenzen/module-katalog.md</code></p>
</div>"""))

    kapitel = 0
    for eintrag in daten["komponenten"]:
        name = eintrag["name"]
        css, markup = baustein(name)
        kategorie, _, kurz = name.partition("/")

        if "[NN]" in markup:
            kapitel += 1
            markup = nummerieren(markup, f"{kapitel:02d}")

        if zuordnung.get(name, {}).get("baustein"):
            markup = (f'<div class="galerie-baustein" style="max-width:440px">'
                      f'{markup}</div>')

        teile.append((css, markup))

    html = zusammenbauen("Modul-Galerie — DAYONE", teile, stempel(daten))
    html = html.replace("<body>", '<body class="galerie">')
    html = html.replace("</body>", _qa_leiste_block() + "\n</body>")
    (WURZEL / "modul-galerie.html").write_text(html)
    return kapitel


# ------------------------------------------------------------------ Starter
def starter_bauen(daten):
    teile = []
    kapitel = 0
    # Die Navigation steht immer zuerst.
    teile.append(baustein("00 Elemente/01 kapitel-nav"))

    vorheriger_war_divider = False
    for name in DRAMATURGIE_WEEKLY:
        css, markup = baustein(name)
        if vorheriger_war_divider:
            markup = marker_entfernen(markup)
        # Nur numerieren, wenn die Sektion wirklich ein neues, in der Nav
        # verlinktes Kapitel markiert (data-chapter) - nicht bei jedem "[NN]".
        # Mehrere Module (big-statement, grossbild, bild-kennzahlenliste, ...) tragen
        # eine EIGENE, optionale Eyebrow mit "[NN]" als Beat innerhalb eines
        # Kapitels, ohne selbst data-chapter zu fuehren. Wuerde man auf jedes
        # "[NN]" numerieren, bekaeme so ein Beat eine Kapitelnummer, die in
        # der selbstbauenden Nav gar nicht existiert - Nummern und Nav-Links
        # liefen auseinander. Bleibt "[NN]" danach unersetzt stehen, faengt
        # das der bestehende Platzhalter-FEHLER in tools/pruefen.py ab: wer
        # das Modul als Kapitelstart braucht, ergaenzt data-chapter selbst
        # (siehe referenzen/module-katalog.md, Abschnitt "Eyebrow") - wer es
        # nur als Beat braucht, loescht die Eyebrow-Zeile.
        if 'data-chapter="[NN]"' in markup:
            kapitel += 1
            markup = nummerieren(markup, f"{kapitel:02d}")
        elif vorheriger_war_divider:
            # Der Divider hat die Kapitelnummer schon vergeben, die Sektion
            # danach gehoert zum selben Kapitel und bekommt keine neue.
            pass
        vorheriger_war_divider = name == "02 Struktur/01 section-divider"
        teile.append((css, markup))

    html = zusammenbauen("[Titel der Präsentation] — DAYONE", teile, stempel(daten))
    (WURZEL / "starter.html").write_text(html)
    return len(DRAMATURGIE_WEEKLY), kapitel


def main():
    if not (B / "_basis.css").exists():
        sys.exit("bausteine/_basis.css fehlt — zuerst tools/zerlegen.py laufen lassen.")
    daten = json.loads(KOMPONENTEN.read_text())

    kap_galerie = galerie_bauen(daten)
    module, kap_starter = starter_bauen(daten)

    print(f"modul-galerie.html  {len(daten['komponenten'])} Module, "
          f"{kap_galerie} Kapitel")
    print(f"starter.html        {module} Module, {kap_starter} Kapitel "
          f"(Weekly-Dramaturgie)")


if __name__ == "__main__":
    main()
