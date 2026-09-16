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
import shutil
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "dist" / "dayone-onepager"

# Woher im Repo -> wohin im Skill-Paket.
INHALT = {
    "skill/SKILL.md": "SKILL.md",
    "referenzen/module-katalog.md": "references/module-katalog.md",
    "referenzen/scroll-patterns.md": "references/scroll-patterns.md",
    "referenzen/ausliefern.md": "references/ausliefern.md",
    "referenzen/tokens.css": "assets/tokens.css",
    "starter.html": "assets/starter.html",
    "modul-galerie.html": "assets/modul-galerie.html",
}

# Wo der Skill auf diesem Rechner installiert ist (fuer den Drift-Vergleich).
INSTALLIERT = sorted(pathlib.Path.home().glob(
    "Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/"
    "*/*/skills/dayone-onepager"))


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
        shutil.copy2(q, z)
    print(f"Skill-Paket gebaut: {ZIEL.relative_to(WURZEL)}/")
    for quelle, ziel in INHALT.items():
        groesse = (ZIEL / ziel).stat().st_size
        print(f"  {ziel:<34} {groesse:>7,} B   ← {quelle}")


def drift_pruefen():
    """Vergleicht das gebaute Paket mit dem installierten Skill."""
    if not INSTALLIERT:
        print("Kein installierter Skill gefunden — nichts zu vergleichen.")
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
        print(f"{abweichungen} Datei(en) weichen ab. Das Paket unter "
              f"{ZIEL.relative_to(WURZEL)}/ ist der neue Stand —")
        print("in der Skill-Verwaltung hochladen, damit Kolleg:innen ihn bekommen.")
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
