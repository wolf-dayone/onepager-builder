#!/usr/bin/env python3
"""Prueft einen DAYONE-Onepager gegen die Regeln aus Figma.

    python3 tools/pruefen.py index.html
    python3 tools/pruefen.py *.html
    python3 tools/pruefen.py --vorlage starter.html   # Platzhalter sind erlaubt

Die Stueckzahl-Grenzen kommen aus data/regeln.json (generiert aus den
Figma-Descriptions). Welche CSS-Klasse welches Modul ist, steht in
data/modul-zuordnung.json.

Rueckgabewert: 1, sobald ein FEHLER gefunden wurde. WARNUNG und HINWEIS
lassen den Lauf gruen - sie markieren Dinge, die meistens, aber nicht immer
falsch sind.
"""
import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from seite import Seite  # noqa: E402

WURZEL = pathlib.Path(__file__).resolve().parent.parent
FEHLER, WARNUNG, HINWEIS = "FEHLER", "WARNUNG", "HINWEIS"

# Schriftgroessen, die es als Token gibt (= die Figma-Textstile).
TOKEN_GROESSEN = {14, 16, 19, 24, 36, 76}


class Befund(list):
    def melden(self, grad, regel, text, zeile=0):
        self.append({"grad": grad, "regel": regel, "text": text, "zeile": zeile})


# ---------------------------------------------------------------- Struktur
def pruefe_geruest(s, b, ist_vorlage):
    hero = [k for k in s.sektionen() if k.hat_klasse("hero")]
    cta = [k for k in s.sektionen() if k.hat_klasse("cta")]

    if len(hero) != 1:
        b.melden(FEHLER, "geruest",
                 f"Genau ein Hero erwartet, {len(hero)} gefunden.",
                 hero[0].zeile if hero else 0)
    if len(cta) != 1:
        b.melden(FEHLER, "geruest",
                 f"Genau ein CTA-Footer erwartet, {len(cta)} gefunden.",
                 cta[0].zeile if cta else 0)

    # Eine Vorlage zeigt bewusst alle Bausteine - da gilt die 6-10-Regel nicht.
    anzahl = len(s.sektionen())
    if not ist_vorlage and not 6 <= anzahl <= 10:
        grad = WARNUNG if 5 <= anzahl <= 12 else FEHLER
        b.melden(grad, "umfang",
                 f"{anzahl} Module. Empfohlen sind 6–10 — darunter wirkt die "
                 f"Seite dünn, darüber ermüdet sie.")

    sprache = s.erste("html")
    if not (sprache and sprache.attrs.get("lang")):
        b.melden(FEHLER, "sprache", "<html> ohne lang-Attribut.")

    titel = s.erste("title")
    if not titel or not titel.voller_text().strip():
        b.melden(FEHLER, "titel", "Kein <title> gesetzt.")


def pruefe_kapitel(s, b, ist_vorlage):
    kapitel = [k for k in s.alle() if "data-chapter" in k.attrs]

    for k in kapitel:
        nr = k.attrs.get("data-chapter", "")
        if not k.attrs.get("id"):
            b.melden(FEHLER, "kapitel",
                     f"Kapitel {nr!r} hat kein id — die Navigation kann nicht "
                     f"dorthin springen.", k.zeile)
        if not k.attrs.get("data-chapter-title"):
            b.melden(FEHLER, "kapitel",
                     f"Kapitel {nr!r} hat kein data-chapter-title — der "
                     f"Navigationseintrag bliebe leer.", k.zeile)
        if nr and not re.fullmatch(r"\d{2}", nr) and not ist_vorlage:
            b.melden(WARNUNG, "kapitel",
                     f"data-chapter={nr!r} ist nicht zweistellig. Figma "
                     f"nummeriert Kapitelmarker zweistellig (01, 02 …).", k.zeile)

    nummern = [k.attrs.get("data-chapter") for k in kapitel]
    doppelt = {n for n in nummern if n and nummern.count(n) > 1}
    if doppelt and not ist_vorlage:
        b.melden(FEHLER, "kapitel",
                 f"Kapitelnummer mehrfach vergeben: {', '.join(sorted(doppelt))}.")

    if kapitel and not ist_vorlage and not 4 <= len(kapitel) <= 8:
        b.melden(WARNUNG, "kapitel",
                 f"{len(kapitel)} Kapitel. Figma nennt 4–8 — darüber lohnt "
                 f"die Navigation kaum noch.")

    # Kapitelmarker muss zur Kapitelnummer passen (Figma: kapitel-nav FÜLLEN).
    for k in kapitel:
        nr = k.attrs.get("data-chapter")
        marker = next((e for e in k.alle(klasse="eyebrow")), None)
        if not (nr and marker):
            continue
        text = marker.voller_text().strip()
        if text and not text.startswith(nr):
            b.melden(WARNUNG, "kapitelmarker",
                     f"Kapitel {nr}: Kapitelmarker beginnt mit {text[:22]!r}. "
                     f"Figma verlangt, dass Marker und Navigationsnummer "
                     f"übereinstimmen.", marker.zeile)


def pruefe_doppelmarker(s, b):
    """Figma, section-divider: pro Kapitel nur die erste Sektion traegt den Marker."""
    sektionen = s.sektionen()
    for i, sek in enumerate(sektionen[:-1]):
        if not sek.hat_klasse("divider"):
            continue
        hat_marker = next(sek.alle(klasse="eyebrow"), None)
        naechste = sektionen[i + 1]
        if hat_marker and next(naechste.alle(klasse="eyebrow"), None):
            b.melden(WARNUNG, "kapitelmarker",
                     "Divider und die Sektion direkt danach tragen beide einen "
                     "Kapitelmarker. Figma: nie auf beiden gleichzeitig.",
                     sek.zeile)


def pruefe_rhythmus(s, b, zuordnung):
    """Figma-Gestaltungsprinzip: nie zwei textlastige Module hintereinander."""
    textlastig = {v["klasse"] for v in zuordnung.values() if v.get("textlastig")}
    sektionen = s.sektionen()

    folge = []
    for sek in sektionen:
        art = next((kl for kl in sek.klassen() if kl in textlastig), None)
        folge.append((sek, art))

    for i in range(len(folge) - 1):
        (a, art_a), (c, art_c) = folge[i], folge[i + 1]
        if art_a and art_c and not a.hat_klasse("dark") and not c.hat_klasse("dark"):
            b.melden(HINWEIS, "rhythmus",
                     f"Zwei textlastige Module hintereinander ({art_a} → "
                     f"{art_c}), beide hell. Ein dunkles Modul dazwischen "
                     f"setzt eine Zäsur.", c.zeile)

    # Alle 3-4 Sektionen eine dunkle als Zaesur.
    seit_dunkel = 0
    for sek in sektionen:
        seit_dunkel = 0 if sek.hat_klasse("dark") else seit_dunkel + 1
        if seit_dunkel == 5:
            b.melden(HINWEIS, "rhythmus",
                     "Fünf helle Module am Stück. Figma empfiehlt alle 3–4 "
                     "Sektionen ein dunkles Modul als Zäsur.", sek.zeile)
            seit_dunkel = 0


# ------------------------------------------------------------------ Tokens
def pruefe_tokens(s, b):
    css = s.css_ohne_tokens()

    for treffer in re.finditer(r"#[0-9a-fA-F]{3,8}\b", css):
        b.melden(FEHLER, "tokens",
                 f"Roh-Farbwert {treffer.group()} außerhalb des :root-Blocks. "
                 f"Farben kommen aus den Tokens, sonst bricht der Dark-Mode.",
                 s.zeile_von(treffer.group()))

    gesehen = {}
    for treffer in re.finditer(r"font-size\s*:\s*(\d+)px", css):
        groesse = int(treffer.group(1))
        roh = treffer.group(0)
        zeile = s.zeile_von(roh, ab=gesehen.get(roh, 0))
        gesehen[roh] = gesehen.get(roh, 0) + 1
        if groesse in TOKEN_GROESSEN:
            b.melden(WARNUNG, "tokens",
                     f"font-size:{groesse}px ist eine gültige Figma-Schriftgröße, "
                     f"steht hier aber als Rohwert statt als var(--text-…).", zeile)
        else:
            b.melden(FEHLER, "tokens",
                     f"font-size:{groesse}px entspricht keinem Figma-Textstil "
                     f"({', '.join(str(g) for g in sorted(TOKEN_GROESSEN))}).", zeile)

    if re.search(r"@font-face[^}]*Roobert", s.css, re.IGNORECASE | re.DOTALL):
        b.melden(FEHLER, "schrift",
                 "Roobert wird per @font-face eingebettet. Die Schrift ist "
                 "lizenzpflichtig und darf das Haus nicht verlassen.")


# ----------------------------------------------------------------- Inhalte
PLATZHALTER = re.compile(r"\[[^\]\n]{1,60}\]")


def pruefe_platzhalter(s, b):
    """Nur sichtbarer Text - CSS-Selektoren wie [data-chapter] sind keine Platzhalter."""
    gesehen = set()
    for knoten in s.alle():
        if knoten.tag in ("style", "script"):
            continue
        for stueck in knoten.text:
            for treffer in PLATZHALTER.finditer(stueck):
                p = treffer.group()
                if p in gesehen:
                    continue
                gesehen.add(p)
                b.melden(FEHLER, "platzhalter",
                         f"Unersetzter Platzhalter {p} im sichtbaren Text.",
                         knoten.zeile)
    for tag, attr in (("title", None), ("meta", "content"), ("img", "alt"),
                       ("img", "src")):
        for knoten in s.alle(tag):
            wert = knoten.voller_text() if attr is None else knoten.attrs.get(attr, "")
            if PLATZHALTER.search(wert or ""):
                b.melden(FEHLER, "platzhalter",
                         f"Unersetzter Platzhalter in <{tag}>: {wert[:50]}",
                         knoten.zeile)


def pruefe_bilder(s, b):
    for bild in s.alle("img"):
        if bild.attrs.get("alt") is None:
            b.melden(FEHLER, "bilder", "<img> ohne alt-Attribut.", bild.zeile)
        if bild.attrs.get("loading") != "lazy":
            b.melden(WARNUNG, "bilder",
                     "<img> ohne loading=\"lazy\". Auf einer langen Scrollseite "
                     "lädt sonst alles sofort.", bild.zeile)


def pruefe_bewegung(s, b):
    if "prefers-reduced-motion" not in s.css:
        b.melden(FEHLER, "bewegung",
                 "Kein prefers-reduced-motion-Block. Die Reveal-Animationen "
                 "laufen dann auch bei Menschen, die Bewegung abgeschaltet haben.")


def _regel_werte(css, klasse, eigenschaft):
    """Alle Werte, die ein Selektor mit .klasse fuer eigenschaft setzt."""
    muster = re.compile(
        r"(?<![\w-])\." + re.escape(klasse) + r"(?![\w-])[^{}]*\{([^}]*)\}")
    werte = []
    for block in muster.findall(css):
        for m in re.finditer(re.escape(eigenschaft) + r"\s*:\s*(\d+)px", block):
            werte.append(int(m.group(1)))
    return werte


def pruefe_touch(s, b):
    """Figma, cta-footer: Buttons min. 44px hoch, Schrift min. 16px."""
    cta = s.erste(klasse="cta")
    if not cta:
        return

    # Die Buttons im CTA-Footer finden und ueber ihre Klassen nachschlagen -
    # die Regel haengt oft an .btn, nicht an einem Selektor mit .cta darin.
    knoepfe = [k for k in cta.alle() if k.tag in ("a", "button")]
    if not knoepfe:
        b.melden(WARNUNG, "touch", "CTA-Footer ohne Button.", cta.zeile)
        return

    for knopf in knoepfe:
        hoehen, groessen = [], []
        for klasse in knopf.klassen():
            hoehen += _regel_werte(s.css, klasse, "min-height")
            groessen += _regel_werte(s.css, klasse, "font-size")
        beschriftung = (knopf.voller_text().strip() or "?")[:24]

        if not hoehen:
            b.melden(WARNUNG, "touch",
                     f"CTA-Button „{beschriftung}“ ohne min-height. Figma "
                     f"verlangt 44px, sonst ist er am Handy schwer zu treffen.",
                     knopf.zeile)
        elif min(hoehen) < 44:
            b.melden(FEHLER, "touch",
                     f"CTA-Button „{beschriftung}“: min-height {min(hoehen)}px, "
                     f"Figma verlangt 44px.", knopf.zeile)

        if groessen and min(groessen) < 16:
            b.melden(FEHLER, "touch",
                     f"CTA-Button „{beschriftung}“: font-size {min(groessen)}px. "
                     f"Figma verlangt min. 16px — darunter zoomt iOS beim "
                     f"Antippen hinein.", knopf.zeile)


SPALTEN_REGEL = re.compile(r"grid-template-columns\s*:\s*([^;}]+)")


def _spaltenzahl(wert):
    """Wie viele feste Spalten legt ein grid-template-columns-Wert an?

    0 heisst: nicht zu beanstanden. Das gilt fuer eine einzelne Spalte und
    fuer repeat(auto-fit|auto-fill, minmax(...)) - letzteres bricht von selbst
    um und braucht keine Media Query.
    """
    wert = wert.strip()
    if "auto-fit" in wert or "auto-fill" in wert:
        return 0

    m = re.search(r"repeat\(\s*(\d+)", wert)
    if m:
        return int(m.group(1))

    # Tracks auf oberster Ebene zaehlen - Klammern von minmax()/calc() ueberspringen.
    tracks, tiefe, aktuell = 0, 0, ""
    for zeichen in wert:
        if zeichen == "(":
            tiefe += 1
        elif zeichen == ")":
            tiefe -= 1
        if zeichen.isspace() and tiefe == 0:
            if aktuell:
                tracks += 1
                aktuell = ""
        else:
            aktuell += zeichen
    if aktuell:
        tracks += 1
    return tracks


def pruefe_mobil(s, b):
    """Figma: 'Mobile wird zuerst kaputt' - bei Sticky-Spalten, Tabellen, Roadmaps.

    Prueft nicht das Rendering (dafuer braucht es einen Browser), sondern ob
    ein mehrspaltiges Raster ueberhaupt eine Regel fuer schmale Viewports hat.
    Ein Raster mit fester Spaltenzahl und ohne Media Query bricht dort sicher.
    """
    css = s.css_ohne_tokens()

    # Zeichenweise durchgehen und je Position merken, ob wir gerade in einer
    # max-width-Media-Query stecken. Zeilenweise geht nicht: eine einzeilige
    # Query wie "@media(max-width:900px){.a{...}}" hat oeffnende und
    # schliessende Klammern in derselben Zeile.
    in_query = [False] * len(css)
    for m in re.finditer(r"@media[^{]*max-width[^{]*\{", css):
        tiefe, i = 1, m.end()
        while i < len(css) and tiefe > 0:
            if css[i] == "{":
                tiefe += 1
            elif css[i] == "}":
                tiefe -= 1
            in_query[i] = True
            i += 1

    # Welche Klassen bekommen irgendwo eine Regel fuer schmale Viewports?
    mit_mobilregel = set()
    for m in re.finditer(r"\.([a-z0-9-]+)", css):
        if in_query[m.start()]:
            mit_mobilregel.add(m.group(1))

    gemeldet = set()
    for m in SPALTEN_REGEL.finditer(css):
        if in_query[m.start()] or _spaltenzahl(m.group(1)) < 2:
            continue
        # Selektor dieser Regel: alles zwischen der letzten schliessenden
        # Klammer davor und der oeffnenden Klammer dieser Regel.
        block_start = css.rfind("{", 0, m.start())
        selektor_start = max(css.rfind("}", 0, block_start),
                             css.rfind("{", 0, block_start)) + 1
        selektor = css[selektor_start:block_start]
        for klasse in re.findall(r"\.([a-z0-9-]+)", selektor):
            if klasse in mit_mobilregel or klasse in gemeldet:
                continue
            gemeldet.add(klasse)
            b.melden(WARNUNG, "mobil",
                     f".{klasse} legt {_spaltenzahl(m.group(1))} feste Spalten "
                     f"fest, hat aber keine Regel für schmale Viewports. "
                     f"Figma: „Mobile wird zuerst kaputt“.",
                     s.zeile_von(m.group(0)[:40]))


def pruefe_links(s, b, ist_vorlage):
    """Kein Link darf ins Leere zeigen.

    Gefunden beim ersten Blindtest: eine fertige Seite ging mit zwei
    CTA-Buttons auf href="#" raus. Die Seite wird verschickt - ein Knopf, der
    nichts tut, faellt erst der Empfaengerin auf.
    """
    for a in s.alle("a"):
        ziel = (a.attrs.get("href") or "").strip()
        text = (a.voller_text().strip() or "?")[:32]

        if not ziel:
            b.melden(FEHLER, "links",
                     f"Link „{text}“ ohne href.", a.zeile)
        elif ziel == "#":
            b.melden(FEHLER, "links",
                     f"Link „{text}“ zeigt auf href=\"#\" — also nirgendwohin. "
                     f"Echtes Ziel eintragen oder den Link entfernen.", a.zeile)
        elif PLATZHALTER.search(ziel):
            # In einer Vorlage ist href="[URL]" genau richtig - so wie ein
            # Platzhalter im Text auch.
            if ist_vorlage:
                continue
            b.melden(FEHLER, "links",
                     f"Link „{text}“ hat noch einen Platzhalter als Ziel: {ziel}",
                     a.zeile)
        elif ziel.startswith("#") and not any(
                k.attrs.get("id") == ziel[1:] for k in s.alle()):
            b.melden(WARNUNG, "links",
                     f"Link „{text}“ springt zu {ziel}, aber es gibt kein "
                     f"Element mit dieser id.", a.zeile)


# Module, die etwas Visuelles tragen (Bild, Screenshot, Diagramm, Portrait).
# Eine Seite ganz ohne so ein Modul ist eine Textwueste.
VISUELLE_MODULE = {
    "03 Inhalt/01 headline-text-bild", "04 Daten/02 chart-slide",
    "05 Diagramme/01 konzentrische-kreise",
    "05 Diagramme/02 diagrammkarte",
    "07 Media/01 bild-feature-liste", "07 Media/02 device-mockup",
    "07 Media/03 medien-karten-grid", "07 Media/04 grossbild",
    "08 Menschen/01 team-grid", "08 Menschen/02 bild-intro",
    "09 Referenzen/01 logo-wand", "09 Referenzen/02 bild-kennzahlenliste",
    "10 Abschluss/02 qr-tool-verweis",
}

# Zaehlen beim Rhythmus nicht als eigenstaendiger Inhalt.
RAHMEN_MODULE = {
    "00 Elemente/01 kapitel-nav", "00 Elemente/02 karte",
    "01 Einstieg/01 cover-hero", "10 Abschluss/03 cta-footer",
}


def _inhaltsmodule(s):
    """data-modul aller Abschnitte, die echten Inhalt tragen."""
    namen = []
    for sek in s.sektionen():
        name = sek.attrs.get("data-modul")
        if name and name not in RAHMEN_MODULE:
            namen.append(name)
    return namen


def pruefe_vielfalt(s, b, regeln):
    """Nicht zu oft dasselbe Modul - sonst liest sich die Seite wie eine Liste."""
    namen = _inhaltsmodule(s)
    if len(namen) < 4:
        return

    haeufigkeit = {n: namen.count(n) for n in set(namen)}
    kurz = lambda n: regeln["module"].get(n, {}).get("kurzname", n)

    for name, anzahl in sorted(haeufigkeit.items(), key=lambda x: -x[1]):
        if anzahl >= 3:
            b.melden(WARNUNG, "vielfalt",
                     f"{kurz(name)} kommt {anzahl}× vor. Ab dem dritten Mal wirkt "
                     f"ein Modul wie eine Formatierung statt wie eine Aussage — "
                     f"im Katalog nach einer Alternative sehen.")

    haeufigstes, spitze = max(haeufigkeit.items(), key=lambda x: x[1])
    if spitze / len(namen) > 0.4 and spitze >= 2:
        b.melden(HINWEIS, "vielfalt",
                 f"{spitze} von {len(namen)} Inhaltsmodulen sind "
                 f"{kurz(haeufigstes)}. Mehr Abwechslung trägt besser durch "
                 f"eine ganze Seite.")


def pruefe_bildanteil(s, b, ist_vorlage):
    """Figma-Prinzip: ein visueller Ruhepunkt zwischen textlastigen Abschnitten."""
    if ist_vorlage:
        return
    namen = _inhaltsmodule(s)
    if len(namen) < 4:
        return
    visuell = [n for n in namen if n in VISUELLE_MODULE]
    if not visuell and not list(s.alle("img")):
        b.melden(WARNUNG, "bildanteil",
                 f"Keines der {len(namen)} Inhaltsmodule trägt ein Bild, einen "
                 f"Screenshot oder ein Diagramm. Beim Menschen nachfragen, ob "
                 f"Material vorliegt — eine reine Textseite ermüdet.")


def pruefe_agenda(s, b):
    """Die Agenda muss sich verdienen: nur bei echter thematischer Übersicht."""
    agenda = next((k for k in s.sektionen()
                   if k.attrs.get("data-modul") == "01 Einstieg/02 agenda"), None)
    if not agenda:
        return
    kapitel = len([k for k in s.alle() if "data-chapter" in k.attrs])
    if kapitel and kapitel < 4:
        b.melden(HINWEIS, "agenda",
                 f"Agenda bei nur {kapitel} Kapiteln. Sie lohnt sich erst, wenn "
                 f"die Seite genug Umfang hat, dass eine Übersicht Orientierung "
                 f"gibt — sonst kündigt sie an, was man ohnehin gleich sieht.")


def pruefe_ueberschriften(s, b):
    h1 = list(s.alle("h1"))
    if len(h1) > 1:
        b.melden(WARNUNG, "ueberschriften",
                 f"{len(h1)} <h1> auf der Seite. Eine reicht — der Hero-Titel.")


# --------------------------------------------------- Stueckzahlen je Modul
def grenze_fuer(regel_modul, einheit):
    """Sucht in den aus Figma extrahierten Grenzen die passende Einheit."""
    if not einheit:
        return None
    for g in regel_modul.get("grenzen", []):
        if g["einheit"].lower().startswith(einheit.lower()[:6]):
            return g
    return None


def vorkommen(s, figma_name, zu):
    """Alle Stellen, an denen dieses Modul auf der Seite steht.

    Primaer ueber data-modul="<Figma-Name>" - das ist die verlaessliche
    Kennung. Die CSS-Klasse ist nur der Rueckfall fuer aeltere Seiten.
    """
    ausgezeichnet = [k for k in s.alle() if k.attrs.get("data-modul") == figma_name]
    if ausgezeichnet:
        return ausgezeichnet
    return list(s.alle(klasse=zu["klasse"]))


def pruefe_modulkennung(s, b, zuordnung):
    """Jeder Abschnitt soll sagen, welches Figma-Modul er ist."""
    bekannt = set(zuordnung)
    ohne = []
    for sek in s.sektionen():
        name = sek.attrs.get("data-modul")
        if not name:
            ohne.append(sek)
        elif name not in bekannt:
            b.melden(FEHLER, "modulkennung",
                     f"data-modul={name!r} gibt es in Figma nicht. Gültige "
                     f"Namen stehen in referenzen/module-katalog.md.", sek.zeile)
    if ohne:
        b.melden(WARNUNG, "modulkennung",
                 f"{len(ohne)} von {len(s.sektionen())} Abschnitten ohne "
                 f"data-modul. Ohne diese Kennung lässt sich nicht prüfen, ob "
                 f"ein Abschnitt seine Figma-Regeln einhält.", ohne[0].zeile)


def pruefe_stueckzahlen(s, b, regeln, zuordnung):
    for figma_name, zu in zuordnung.items():
        if zu.get("baustein") or not zu.get("zaehlt"):
            continue
        regel = regeln["module"].get(figma_name, {})
        kurz = regel.get("kurzname", figma_name)

        for sek in vorkommen(s, figma_name, zu):
            anzahl = sum(1 for _ in sek.alle(klasse=zu["zaehlt"]))
            if anzahl == 0:
                continue

            if "genau" in zu and anzahl != zu["genau"]:
                b.melden(FEHLER, "stueckzahl",
                         f"{kurz}: {anzahl} × .{zu['zaehlt']} — das Modul ist "
                         f"auf genau {zu['genau']} ausgelegt.", sek.zeile)
                continue

            g = grenze_fuer(regel, zu.get("einheit"))
            if not g:
                continue
            if g["min"] and anzahl < g["min"]:
                b.melden(WARNUNG, "stueckzahl",
                         f"{kurz}: {anzahl} {g['einheit']}, Figma nennt "
                         f"{g['min']}–{g['max']}. „{g['quelle']}“", sek.zeile)
            elif g["max"] and anzahl > g["max"]:
                b.melden(WARNUNG, "stueckzahl",
                         f"{kurz}: {anzahl} {g['einheit']}, Figma nennt "
                         f"{g['min']}–{g['max']}. „{g['quelle']}“", sek.zeile)


# ------------------------------------------------------------------ Bericht
FARBEN = {FEHLER: "\033[31m", WARNUNG: "\033[33m", HINWEIS: "\033[36m"}
AUS = "\033[0m"


def bericht(pfad, befund, farbig):
    def f(grad):
        return f"{FARBEN[grad]}{grad}{AUS}" if farbig else grad

    zahl = {g: sum(1 for x in befund if x["grad"] == g)
            for g in (FEHLER, WARNUNG, HINWEIS)}
    print(f"\n── {pfad} " + "─" * max(0, 60 - len(str(pfad))))
    if not befund:
        print("   alles sauber.")
        return
    for grad in (FEHLER, WARNUNG, HINWEIS):
        for x in [x for x in befund if x["grad"] == grad]:
            ort = f"{pfad}:{x['zeile']}" if x["zeile"] else str(pfad)
            print(f"   {f(grad):<9} {x['regel']:<14} {ort}")
            print(f"             {x['text']}")
    print(f"   → {zahl[FEHLER]} Fehler, {zahl[WARNUNG]} Warnungen, "
          f"{zahl[HINWEIS]} Hinweise")


def pruefe_datei(pfad, regeln, zuordnung, ist_vorlage, ist_galerie=False):
    s = Seite(pfad)
    b = Befund()
    pruefe_geruest(s, b, ist_vorlage or ist_galerie)
    pruefe_kapitel(s, b, ist_vorlage or ist_galerie)
    # Eine Galerie zeigt jedes Modul einmal - Dramaturgie-Regeln (Rhythmus,
    # Kapitelmarker-Abfolge, eine Headline) gelten dort nicht.
    if not ist_galerie:
        pruefe_doppelmarker(s, b)
        pruefe_rhythmus(s, b, zuordnung)
    pruefe_tokens(s, b)
    pruefe_bilder(s, b)
    pruefe_bewegung(s, b)
    pruefe_links(s, b, ist_vorlage)
    if not ist_galerie:
        pruefe_vielfalt(s, b, regeln)
        pruefe_bildanteil(s, b, ist_vorlage)
        pruefe_agenda(s, b)
    pruefe_mobil(s, b)
    pruefe_touch(s, b)
    if not ist_galerie:
        pruefe_ueberschriften(s, b)
    pruefe_modulkennung(s, b, zuordnung)
    pruefe_stueckzahlen(s, b, regeln, zuordnung)
    if not ist_vorlage:
        pruefe_platzhalter(s, b)
    return b


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("dateien", nargs="+", type=pathlib.Path)
    p.add_argument("--vorlage", action="store_true",
                   help="Datei ist ein Template — Platzhalter sind dort erwünscht")
    p.add_argument("--galerie", action="store_true",
                   help="Datei ist die Modul-Galerie — Dramaturgie-Regeln gelten nicht")
    p.add_argument("--keine-farbe", action="store_true")
    args = p.parse_args()

    regeln = json.loads((WURZEL / "data" / "regeln.json").read_text())
    zuordnung = json.loads(
        (WURZEL / "data" / "modul-zuordnung.json").read_text())["module"]

    farbig = sys.stdout.isatty() and not args.keine_farbe
    fehler_gesamt = 0
    for pfad in args.dateien:
        if not pfad.exists():
            print(f"nicht gefunden: {pfad}", file=sys.stderr)
            fehler_gesamt += 1
            continue
        ist_galerie = args.galerie or pfad.name == "modul-galerie.html"
        ist_vorlage = args.vorlage or ist_galerie or pfad.name == "starter.html"
        befund = pruefe_datei(pfad, regeln, zuordnung, ist_vorlage, ist_galerie)
        bericht(pfad, befund, farbig)
        fehler_gesamt += sum(1 for x in befund if x["grad"] == FEHLER)

    print()
    return 1 if fehler_gesamt else 0


if __name__ == "__main__":
    sys.exit(main())
