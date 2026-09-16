"""Minimaler HTML-Leser fuer die Onepager-Pruefung.

Kein externes Paket: html.parser aus der Stdlib baut einen kleinen Baum, der
genug kann, um nach Klassen und Tags zu suchen und sichtbaren Text von Code
(<style>, <script>) zu trennen. Genau diese Trennung ist der Grund, warum es
hier einen Parser braucht und kein grep: die bisherige Platzhalter-Regel
("am Ende nach [ suchen") schlug auf CSS-Selektoren wie [data-chapter] an.
"""
from html.parser import HTMLParser

# Tags ohne schliessendes Gegenstueck.
LEER = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
# Deren Inhalt ist Code, kein sichtbarer Text.
CODE = {"style", "script"}


class Knoten:
    __slots__ = ("tag", "attrs", "kinder", "eltern", "text", "zeile")

    def __init__(self, tag, attrs=None, zeile=0):
        self.tag = tag
        self.attrs = attrs or {}
        self.kinder = []
        self.eltern = None
        self.text = []          # direkte Textstuecke dieses Knotens
        self.zeile = zeile

    # -- Suche ------------------------------------------------------------
    def klassen(self):
        return set((self.attrs.get("class") or "").split())

    def hat_klasse(self, name):
        return name in self.klassen()

    def alle(self, tag=None, klasse=None):
        """Alle Nachfahren (ohne sich selbst), optional gefiltert."""
        for kind in self.kinder:
            if (tag is None or kind.tag == tag) and \
               (klasse is None or kind.hat_klasse(klasse)):
                yield kind
            yield from kind.alle(tag, klasse)

    def voller_text(self):
        """Sichtbarer Text dieses Teilbaums - ohne <style>/<script>."""
        if self.tag in CODE:
            return ""
        teile = list(self.text)
        for kind in self.kinder:
            teile.append(kind.voller_text())
        return " ".join(t for t in teile if t.strip())

    def __repr__(self):
        k = "." + ".".join(sorted(self.klassen())) if self.klassen() else ""
        return f"<{self.tag}{k} Z{self.zeile}>"


class _Bauer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.wurzel = Knoten("#dokument")
        self.stapel = [self.wurzel]
        self.code = {"style": [], "script": []}

    def handle_starttag(self, tag, attrs):
        knoten = Knoten(tag, dict(attrs), self.getpos()[0])
        knoten.eltern = self.stapel[-1]
        self.stapel[-1].kinder.append(knoten)
        if tag not in LEER:
            self.stapel.append(knoten)

    def handle_startendtag(self, tag, attrs):
        knoten = Knoten(tag, dict(attrs), self.getpos()[0])
        knoten.eltern = self.stapel[-1]
        self.stapel[-1].kinder.append(knoten)

    def handle_endtag(self, tag):
        for i in range(len(self.stapel) - 1, 0, -1):
            if self.stapel[i].tag == tag:
                del self.stapel[i:]
                return
        # Unbekanntes Schluss-Tag: ignorieren statt den Baum zu zerlegen.

    def handle_data(self, daten):
        aktuell = self.stapel[-1]
        aktuell.text.append(daten)
        if aktuell.tag in self.code:
            self.code[aktuell.tag].append(daten)


def _ohne_kommentare(css):
    """Entfernt /* ... */ - ersetzt durch Leerzeilen, damit Zeilennummern passen."""
    import re as _re
    return _re.sub(r"/\*.*?\*/",
                   lambda m: "\n" * m.group().count("\n"), css, flags=_re.DOTALL)


class Seite:
    """Eine eingelesene Onepager-Datei."""

    def __init__(self, pfad):
        self.pfad = pfad
        self.quelle = pfad.read_text(encoding="utf-8")
        bauer = _Bauer()
        bauer.feed(self.quelle)
        self.wurzel = bauer.wurzel
        self.css = "\n".join(bauer.code["style"])
        self.js = "\n".join(bauer.code["script"])
        self.zeilen = self.quelle.splitlines()

    def alle(self, tag=None, klasse=None):
        return self.wurzel.alle(tag, klasse)

    def erste(self, tag=None, klasse=None):
        return next(self.alle(tag, klasse), None)

    def sektionen(self):
        """Alle Seitenabschnitte in Dokumentreihenfolge - Hero und CTA zaehlen mit."""
        treffer = []
        for k in self.wurzel.alle():
            if k.tag in ("section", "header", "footer") and k.tag != "#dokument":
                # Die Kapitel-Navigation ist kein Abschnitt.
                if k.attrs.get("id") == "chapter-nav" or k.tag == "nav":
                    continue
                treffer.append(k)
        return treffer

    def zeile_von(self, text, ab=0):
        """Zeilennummer, in der text vorkommt - fuer klickbare Meldungen.

        `ab` ueberspringt die ersten Treffer, damit mehrere gleiche Fundstellen
        (fuenfmal font-size:16px) nicht alle auf dieselbe Zeile zeigen.
        """
        uebersprungen = 0
        for i, z in enumerate(self.zeilen, 1):
            if text in z:
                if uebersprungen >= ab:
                    return i
                uebersprungen += 1
        return 0

    def css_ohne_tokens(self):
        """CSS ohne :root-Bloecke und ohne Kommentare.

        In :root duerfen Rohwerte stehen - das ist die Token-Definition selbst.
        Erkennung ueber Klammerzaehlung statt Zeilenanfang, damit Formatierung
        egal ist (":root{", ":root {", eingerueckt in einer Media Query).
        Kommentare sind Dokumentation, kein Style: ein Hexwert darin ist keine
        Regelverletzung.
        """
        css = self.css
        ohne = []
        i = 0
        while True:
            treffer = css.find(":root", i)
            if treffer == -1:
                ohne.append(css[i:])
                break
            klammer = css.find("{", treffer)
            if klammer == -1:
                ohne.append(css[i:])
                break
            ohne.append(css[i:treffer])
            # Zeilenumbrueche erhalten, damit Zeilennummern weiter stimmen.
            tiefe, j = 1, klammer + 1
            while j < len(css) and tiefe > 0:
                if css[j] == "{":
                    tiefe += 1
                elif css[j] == "}":
                    tiefe -= 1
                j += 1
            ohne.append("\n" * css.count("\n", treffer, j))
            i = j
        return _ohne_kommentare("".join(ohne))
