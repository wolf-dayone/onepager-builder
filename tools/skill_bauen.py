#!/usr/bin/env python3
"""Packt das Skill-Paket aus dem Repo.

    python3 tools/skill_bauen.py            # baut dist/dayone-onepager/
    python3 tools/skill_bauen.py --pruefen  # meldet nur, ob etwas auseinanderlaeuft

Bisher lief es andersherum: der Skill war die Quelle, das Repo die Spielwiese -
und beides ist auseinandergelaufen (das Skill-Template lag 351 Zeilen und sechs
Module hinter dem Repo, ohne dass es jemand gemerkt haette). Jetzt ist das Repo
die Quelle und der Skill das Build-Ergebnis.

--pruefen vergleicht zusaetzlich mit dem lokal installierten Skill und sagt,
was sich geaendert hat. Damit faellt Drift auf, statt sich anzusammeln.
"""
import argparse
import hashlib
import pathlib
import re
import shutil
import zipfile
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "dist" / "dayone-onepager"

# Woher im Repo -> wohin im Skill-Paket.
INHALT = {
    "skill/SKILL.md": "SKILL.md",
    "referenzen/module-katalog.md": "references/module-katalog.md",
    "referenzen/scroll-patterns.md": "references/scroll-patterns.md",
    "referenzen/animationen.md": "references/animationen.md",
    "referenzen/ausliefern.md": "references/ausliefern.md",
    "referenzen/tokens.css": "assets/tokens.css",
    "starter.html": "assets/starter.html",
    "modul-galerie.html": "assets/modul-galerie.html",
    "page-plans/_vorlage.plan.md": "assets/page-plan-vorlage.md",

    # Der Qualitaets-Check muss mit: SKILL.md Schritt 7 verlangt ihn, und ohne
    # diese Dateien laeuft er bei niemandem ausserhalb dieses Repos. Die Pfade
    # bleiben relativ zum Skill-Ordner, damit pruefen.py seine Regeln findet.
    "tools/pruefen.py": "tools/pruefen.py",
    "tools/seite.py": "tools/seite.py",
    "data/regeln.json": "data/regeln.json",
    "data/modul-zuordnung.json": "data/modul-zuordnung.json",
}

# Wo der Skill auf diesem Rechner installiert ist (fuer den Drift-Vergleich).
# Mehrere Orte, weil die Desktop-App im Lauf der Zeit umgezogen ist: seit dem
# Skill-Sync liegt sie unter ~/.claude/skills/synced/, davor unter Library/
# Application Support. Wird nur EIN Muster gepflegt, faellt der Vergleich
# stillschweigend aus ("nichts zu vergleichen") und Drift sammelt sich wieder
# an, genau wie vor der Umstellung auf das Repo als Quelle (2026-09-21).
SUCHMUSTER = [
    ".claude/skills/synced/*/dayone-onepager",
    ".claude/skills/*/dayone-onepager",
    "Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/"
    "*/*/skills/dayone-onepager",
]


def _installierte_skills():
    treffer = []
    for muster in SUCHMUSTER:
        treffer.extend(sorted(pathlib.Path.home().glob(muster)))
    # Nach Aenderungszeit, damit bei mehreren Fundorten der juengste gewinnt.
    return sorted(treffer, key=lambda p: p.stat().st_mtime)


INSTALLIERT = _installierte_skills()

# Die QA-Leiste in modul-galerie.html (Replay/Viewport/Reduced-Motion-Steuerung
# fuer die Modul-Galerie dieses Repos) ist kein Bestandteil ausgelieferter
# Seiten - siehe tools/bauen.py _qa_leiste_block(). Wird beim Verpacken
# herausgeschnitten, damit Skill-Nutzer:innen sie nie zu Gesicht bekommen.
QA_STRIP = re.compile(r"\n?<!-- QA-ONLY:START -->.*?<!-- QA-ONLY:END -->\n?", re.DOTALL)


def pruefsumme(pfad):
    return hashlib.sha256(pfad.read_bytes()).hexdigest()[:12]


def bauen():
    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    for quelle, ziel in INHALT.items():
        q = WURZEL / quelle
        if not q.exists():
            sys.exit(f"fehlt: {quelle} — erst tools/bauen.py und "
                     f"tools/katalog_bauen.py laufen lassen.")
        z = ZIEL / ziel
        z.parent.mkdir(parents=True, exist_ok=True)
        if quelle == "modul-galerie.html":
            inhalt, n = QA_STRIP.subn("", q.read_text(encoding="utf-8"))
            if n != 1:
                sys.exit(f"modul-galerie.html: erwartet genau einen QA-ONLY-Block, "
                          f"gefunden {n}. tools/bauen.py pruefen.")
            z.write_text(inhalt, encoding="utf-8")
        else:
            shutil.copy2(q, z)
    print(f"Skill-Paket gebaut: {ZIEL.relative_to(WURZEL)}/")
    for quelle, ziel in INHALT.items():
        groesse = (ZIEL / ziel).stat().st_size
        print(f"  {ziel:<34} {groesse:>7,} B   ← {quelle}")

    # Die Skill-Verwaltung nimmt eine .skill-Datei: ein ZIP mit dem
    # Skill-Ordner auf oberster Ebene (Format aus der bestehenden
    # dayone-onepager.skill uebernommen).
    paket = ZIEL.parent / "dayone-onepager.skill"
    if paket.exists():
        paket.unlink()
    with zipfile.ZipFile(paket, "w", zipfile.ZIP_DEFLATED) as z:
        for ziel in INHALT.values():
            z.write(ZIEL / ziel, f"dayone-onepager/{ziel}")
    print(f"\nZum Hochladen: {paket.relative_to(WURZEL)}  "
          f"({paket.stat().st_size:,} B)")


def drift_pruefen():
    """Vergleicht das gebaute Paket mit dem installierten Skill."""
    if not INSTALLIERT:
        # Nicht kommentarlos durchwinken: ein stiller "nichts zu vergleichen"
        # sieht aus wie Entwarnung, heisst aber nur, dass niemand hinsieht.
        print("Kein installierter Skill gefunden. Gesucht unter:")
        for muster in SUCHMUSTER:
            print(f"  ~/{muster}")
        print("\nWenn der Skill installiert ist, aber woanders liegt: Pfad in "
              "SUCHMUSTER (oben in dieser Datei) ergaenzen.")
        print("Sonst gilt das Paket unten als neuer Stand und muss hochgeladen "
              "werden.")
        return 0
    installiert = INSTALLIERT[-1]
    print(f"Vergleich mit: …/{installiert.parent.parent.name}/skills/dayone-onepager\n")

    abweichungen = 0
    for _, ziel in INHALT.items():
        neu = ZIEL / ziel
        alt = installiert / ziel
        if not alt.exists():
            print(f"  NEU        {ziel}")
            abweichungen += 1
        elif pruefsumme(neu) != pruefsumme(alt):
            print(f"  GEAENDERT  {ziel}  "
                  f"({alt.stat().st_size:,} B → {neu.stat().st_size:,} B)")
            abweichungen += 1
        else:
            print(f"  gleich     {ziel}")

    print()
    if abweichungen:
        print(f"UPLOAD NOETIG — {abweichungen} Datei(en) weichen ab.")
        print(f"Das Paket unter dist/dayone-onepager.skill ist der neue Stand:")
        print("in der Skill-Verwaltung hochladen, damit Kolleg:innen ihn bekommen.")
        print("Bis dahin arbeiten alle weiter mit der alten Fassung - auch dieses "
              "Repo aendert daran nichts.")
    else:
        print("Installierter Skill ist auf dem Stand des Repos.")
    return abweichungen


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pruefen", action="store_true",
                   help="zusätzlich mit dem installierten Skill vergleichen")
    args = p.parse_args()

    bauen()
    if args.pruefen:
        print()
        drift_pruefen()
    return 0


if __name__ == "__main__":
    sys.exit(main())
