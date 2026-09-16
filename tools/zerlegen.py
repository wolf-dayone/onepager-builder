#!/usr/bin/env python3
"""Einmalig: zerlegt starter.html in bausteine/ (Basis + ein File je Modul).

    python3 tools/zerlegen.py

Danach ist starter.html ein Build-Ergebnis (tools/bauen.py) und keine
handgepflegte Datei mehr. Dieses Skript wird nach dem Umbau nicht mehr
gebraucht, bleibt aber als Beleg, woher die Bausteine stammen.
"""
import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
QUELLE = WURZEL / "starter.html"
ZIEL = WURZEL / "bausteine"

# CSS-Bloecke, die zur Grundausstattung gehoeren - nicht zu einem Modul.
BASIS_BLOECKE = {
    "TOKENS (identisch zu assets/tokens.css)",
    "Kapitelmarker (Eyebrow)",
    "Typo-Rollen",
    "Reveal on scroll",
}


def css_bloecke(css):
    """Zerlegt den <style>-Inhalt an den '/* ==== Name ==== *\\/'-Kommentaren."""
    muster = re.compile(r"^/\* ==== (.+?) ==== \*/$", re.MULTILINE)
    treffer = list(muster.finditer(css))
    bloecke = []
    vorspann = css[:treffer[0].start()] if treffer else css
    for i, m in enumerate(treffer):
        ende = treffer[i + 1].start() if i + 1 < len(treffer) else len(css)
        bloecke.append((m.group(1), css[m.start():ende].rstrip()))
    return vorspann.strip(), bloecke


def main():
    if not QUELLE.exists():
        sys.exit(f"nicht gefunden: {QUELLE}")
    text = QUELLE.read_text(encoding="utf-8")

    css = re.search(r"<style>\n(.*?)\n</style>", text, re.DOTALL).group(1)
    js = re.search(r"<script>\n(.*?)\n</script>", text, re.DOTALL).group(1)
    svg = re.search(r"(<svg width=\"0\".*?</svg>)", text, re.DOTALL).group(1)

    ZIEL.mkdir(exist_ok=True)
    vorspann, bloecke = css_bloecke(css)

    basis_css, modul_css = [vorspann], {}
    for name, block in bloecke:
        if name in BASIS_BLOECKE:
            basis_css.append(block)
        else:
            modul_css[name] = block

    (ZIEL / "_basis.css").write_text("\n\n".join(basis_css) + "\n")
    (ZIEL / "_basis.js").write_text(js + "\n")
    (ZIEL / "_symbole.svg").write_text(svg + "\n")
    (ZIEL / "_modul-css").mkdir(exist_ok=True)
    for name, block in modul_css.items():
        datei = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        (ZIEL / "_modul-css" / f"{datei}.css").write_text(block + "\n")

    print(f"Basis-CSS  : {len((ZIEL / '_basis.css').read_text().splitlines())} Zeilen")
    print(f"Basis-JS   : {len(js.splitlines())} Zeilen")
    print(f"Modul-CSS  : {len(modul_css)} Blöcke")
    for name in modul_css:
        print(f"             {name}")


if __name__ == "__main__":
    main()
