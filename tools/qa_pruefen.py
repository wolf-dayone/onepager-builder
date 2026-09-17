#!/usr/bin/env python3
"""Browserbasierte QA-Checks fuer modul-galerie.html (Playwright).

    python3 tools/qa_pruefen.py

Ergaenzt tools/pruefen.py (reiner Text-/Regex-Lint auf der Python-Stdlib,
sieht nie einen echten Layout-Zustand) um das, was nur ein echter Browser
sehen kann: Screenshots je Modul und Viewport, Console-/Netzwerkfehler,
horizontaler Overflow, kaputte Bilder, Dummy-Links.

Einmal PRO VIEWPORT wird modul-galerie.html geladen - nicht einmal pro Modul,
das waere bei der single-DOM-Architektur (bausteine/_basis.js Abschnitt 10)
unnoetig teuer. Danach wird jedes [data-modul]-Element einzeln geprueft und
fotografiert.

Einzige externe Abhaengigkeit im Repo (siehe README.md):
    pip install playwright && python3 -m playwright install chromium
Laeuft ausserdem automatisch in .github/workflows/qualitaet.yml (Ubuntu-
Runner) - falls Playwright/Chromium lokal fehlen oder nicht installierbar
sind (z.B. Netzwerk-Allowlist ohne cdn.playwright.dev), bricht dieses Skript
mit einer klaren Meldung ab, statt den Rest der Pipeline zu blockieren.
"""
import argparse
import json
import pathlib
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
GALERIE = WURZEL / "modul-galerie.html"
AUSGABE = WURZEL / "qa-ausgabe"

# (Name, Breite, Hoehe) - deckt die drei Kern-Breakpoints aus dem Testkonzept ab.
VIEWPORTS = [("mobil", 375, 900), ("tablet", 768, 1024), ("desktop", 1440, 900)]

# Befund-Arten, die den Exit-Code auf "Fehler" setzen (vs. nur gemeldet werden).
HART = {"console", "overflow", "bild"}


def _playwright_laden():
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        sys.exit(
            "Playwright ist nicht installiert - einzige externe Abhaengigkeit\n"
            "dieses Repos, nur fuer tools/qa_pruefen.py. Einmalig:\n\n"
            "    pip install playwright\n"
            "    python3 -m playwright install chromium\n\n"
            "Laeuft die Installation von cdn.playwright.dev nicht durch (z.B. "
            "wegen einer Netzwerk-Allowlist), laeuft dieser Check trotzdem in "
            "der CI (.github/workflows/qualitaet.yml, Ubuntu-Runner ohne diese "
            "Einschraenkung) - tools/pruefen.py deckt in der Zwischenzeit den "
            "Rest ab."
        )


def _modul_pruefen(el, name, breite):
    """Prueft ein einzelnes [data-modul]-Element im aktuellen Viewport."""
    befunde = []
    modul_name = el.get_attribute("data-modul") or "?"

    # Horizontaler Overflow: Modul breiter als sein eigener Viewport. Faengt
    # das ab, was pruefen.py (reiner Quelltext) nicht sehen kann - ein
    # Mehrspalten-Raster kann im Markup vollkommen regelkonform aussehen und
    # trotzdem erst beim echten Rendern ueberlaufen.
    breite_el = el.evaluate("el => el.scrollWidth")
    if breite_el > breite + 1:
        befunde.append({"modul": modul_name, "art": "overflow",
                         "meldung": f"scrollWidth {breite_el}px > Viewport {breite}px"})

    # getAttribute('src') statt .src: Platzhalter-Bilder wie "[bild.jpg]"
    # (siehe referenzen/module-katalog.md) sind in der Galerie erwuenscht und
    # werden schon von tools/pruefen.py als Platzhalter gemeldet - hier
    # zaehlen nur echte, nicht-eckige Pfade, die trotzdem nicht laden.
    kaputte_bilder = el.evaluate(
        "el => Array.from(el.querySelectorAll('img'))"
        ".filter(i => !i.getAttribute('src') || !i.getAttribute('src').includes('['))"
        ".filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src)")
    for src in kaputte_bilder:
        befunde.append({"modul": modul_name, "art": "bild", "meldung": f"Bild laedt nicht: {src}"})

    dummy_links = el.evaluate(
        "el => Array.from(el.querySelectorAll('a[href]'))"
        ".filter(a => a.getAttribute('href') === '#' || a.getAttribute('href') === '')"
        ".map(a => a.textContent.trim())")
    for text in dummy_links:
        befunde.append({"modul": modul_name, "art": "link", "meldung": f"Link ohne Ziel: '{text}'"})

    slug = modul_name.replace("/", "-").replace(" ", "_")
    try:
        el.screenshot(path=str(AUSGABE / name / f"{slug}.png"))
    except Exception as e:
        befunde.append({"modul": modul_name, "art": "screenshot",
                         "meldung": f"Screenshot fehlgeschlagen: {e}"})

    return befunde


def pruefen():
    sync_playwright = _playwright_laden()
    if not GALERIE.exists():
        sys.exit("modul-galerie.html fehlt - erst tools/bauen.py laufen lassen.")

    AUSGABE.mkdir(exist_ok=True)
    befunde = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, breite, hoehe in VIEWPORTS:
            (AUSGABE / name).mkdir(exist_ok=True)
            page = browser.new_page(viewport={"width": breite, "height": hoehe})

            konsolenfehler, netzwerkfehler = [], []
            page.on("pageerror", lambda e: konsolenfehler.append(str(e)))
            page.on("console", lambda m: konsolenfehler.append(m.text) if m.type == "error" else None)
            page.on("response", lambda r: netzwerkfehler.append(f"{r.status} {r.url}") if r.status >= 400 else None)

            page.goto(f"file://{GALERIE}")
            # QA-Leiste loest replayAll() automatisch beim Laden aus (siehe
            # bausteine/_galerie-qa.js) - kurz abwarten, damit Kennzahlen/
            # Timeline-Balken/Reveal-Klassen ihren Endzustand erreicht haben,
            # bevor Screenshots gemacht werden.
            page.wait_for_timeout(1200)

            for fehler in konsolenfehler:
                befunde.append({"modul": "(gesamte Seite)", "viewport": name, "art": "console", "meldung": fehler})
            for eintrag in netzwerkfehler:
                befunde.append({"modul": "(gesamte Seite)", "viewport": name, "art": "asset", "meldung": eintrag})

            for el in page.query_selector_all("[data-modul]"):
                for b in _modul_pruefen(el, name, breite):
                    befunde.append({**b, "viewport": name})

            page.close()
        browser.close()

    (AUSGABE / "befunde.json").write_text(json.dumps(befunde, indent=2, ensure_ascii=False))
    _bericht_schreiben(befunde)
    return befunde


def _bericht_schreiben(befunde):
    zeilen = ["# QA-Bericht — tools/qa_pruefen.py", ""]
    if not befunde:
        zeilen.append("Keine Befunde. Alles sauber über alle Viewports.")
    else:
        nach_art = {}
        for b in befunde:
            nach_art.setdefault(b["art"], []).append(b)
        for art, eintraege in sorted(nach_art.items()):
            zeilen.append(f"## {art} ({len(eintraege)})\n")
            for b in eintraege:
                zeilen.append(f"- **{b['modul']}** ({b['viewport']}): {b['meldung']}")
            zeilen.append("")
    (AUSGABE / "qa-bericht.md").write_text("\n".join(zeilen), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.parse_args()

    befunde = pruefen()
    hart = [b for b in befunde if b["art"] in HART]
    print(f"{len(befunde)} Befund(e) ({len(hart)} davon hart) "
          f"-> {AUSGABE / 'qa-bericht.md'}  (Screenshots in {AUSGABE}/<viewport>/)")
    return 1 if hart else 0


if __name__ == "__main__":
    sys.exit(main())
