"""Aufbereitung der Figma-Component-Descriptions.

Die Descriptions kommen aus Figma HTML-escaped (teils mehrfach verschachtelt) und
als ein einziger Fliesstext. Hier werden sie entschaerft und in ihre Abschnitte
(ZWECK, AUFBAU, FUELLEN, HINWEIS, FARBE, ...) zerlegt.
"""
import html
import re

# Reihenfolge egal - wird als Alternative in eine Regex gehaengt.
ABSCHNITTE = [
    "ZWECK", "WANN VERWENDEN", "WANN NICHT", "ABGRENZUNG", "AUFBAU",
    "FÜLLEN", "FUELLEN", "VARIANTEN", "INTERAKTION", "HINWEIS", "FARBE",
    "KEIN DOPPELTER KAPITELMARKER", "MOBILE", "BARRIEREFREIHEIT", "DATEN",
    "SCROLL", "ANIMATION", "BILD", "DATENQUELLE", "ACHTUNG",
    "VERHALTEN", "TODO", "EINGESETZT IN",
]


def entschaerfen(text):
    """Dreht mehrfaches HTML-Escaping zurueck (&amp;amp;quot; -> ")."""
    vorher = None
    while vorher != text:
        vorher = text
        text = html.unescape(text)
    return text.strip()


def zerlegen(text):
    """Zerlegt eine Description in {Abschnitt: Inhalt}.

    Abschnitte sind im Figma-Text als 'SCHLUESSEL — Inhalt' notiert. Kommt ein
    Schluessel mehrfach vor (typisch: mehrere HINWEIS-Bloecke), werden die
    Inhalte mit Zeilenumbruch aneinandergehaengt.
    """
    text = entschaerfen(text)
    alternativen = "|".join(re.escape(a) for a in ABSCHNITTE)
    # Trenner ist entweder ' — ' (Fliesstext-Abschnitt) oder direkt ein
    # Aufzaehlungspunkt '·' (dann bleibt der Punkt Teil des Inhalts).
    muster = re.compile(
        r"(?:^|\s)(" + alternativen + r")(?:\s+[—–-]\s+|\s+(?=·))"
    )
    treffer = list(muster.finditer(text))
    if not treffer:
        return {"_roh": text}

    out = {}
    for i, m in enumerate(treffer):
        start = m.end()
        ende = treffer[i + 1].start() if i + 1 < len(treffer) else len(text)
        schluessel = m.group(1).replace("FUELLEN", "FÜLLEN")
        inhalt = text[start:ende].strip()
        out[schluessel] = (out[schluessel] + "\n" + inhalt) if schluessel in out else inhalt
    return out


def aufzaehlung(inhalt):
    """Zerlegt einen Abschnitt in seine '·'-Punkte. Ohne Punkte: ein Eintrag."""
    if "·" not in inhalt:
        return [inhalt.strip()] if inhalt.strip() else []
    kopf, _, rest = inhalt.partition("·")
    punkte = [p.strip() for p in rest.split("·")]
    ergebnis = [p for p in punkte if p]
    if kopf.strip():
        ergebnis.insert(0, kopf.strip())
    return ergebnis
