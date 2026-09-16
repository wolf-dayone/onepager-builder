#!/usr/bin/env python3
"""Einmalig: legt die 17 bereits gebauten Module als Bausteine ab.

CSS kommt aus bausteine/_modul-css/ (von tools/zerlegen.py), das Markup aus
der bisherigen starter.html - hier nur um data-modul ergaenzt und von zwei
Fehlern befreit (verwaistes </section> nach Facts & Figures, Kapitelmarker
"05" in Kapitel 03).
"""
import pathlib

WURZEL = pathlib.Path(__file__).resolve().parent.parent
B = WURZEL / "bausteine"
CSS = B / "_modul-css"

# slug -> (css-Dateiname ohne .css, Markup)
MODULE = {}


def modul(slug, css_datei, markup):
    MODULE[slug] = (css_datei, markup.strip())


modul("00-elemente-01-kapitel-nav", "kapitel-navigation", """
<nav id="chapter-nav" aria-label="Kapitel" data-modul="00 Elemente/01 kapitel-nav">
  <div class="wrap inner">
    <a class="brand-group" href="#hero" aria-label="Zum Seitenanfang">
      <svg class="logo-mark logo-mark-full" width="92" height="16" aria-label="DAYONE"><use href="#dayone-logo"></use></svg>
      <svg class="logo-mark logo-mark-icon" width="16" height="16" aria-label="DAYONE"><use href="#dayone-mark"></use></svg>
      <span class="nav-title">[Präsentations-Titel]</span>
    </a>
    <ol><!-- wird aus den <section data-chapter> automatisch erzeugt --></ol>
  </div>
</nav>
""")

modul("01-einstieg-01-cover-hero", "hero", """
<!-- .dark auf dem äußeren <header> (volle Breite), Inhalt in .wrap darunter. -->
<header class="hero dark" id="hero" data-modul="01 Einstieg/01 cover-hero">
  <div class="wrap">
    <div class="top reveal">
      <svg class="logo-mark" width="150" height="27" aria-label="DAYONE"><use href="#dayone-logo"></use></svg>
      <div class="badges">
        <a class="badge accent" href="[LIVE-LINK]">LIVE Q&amp;A</a>
        <span class="badge">[ANLASS – KW 00]</span>
      </div>
    </div>
    <div class="reveal">
      <h1 class="h1">[PROJEKTNAME]<span class="line2">[UNTERTITEL DER SESSION]</span></h1>
      <p class="lead sub">[Ein bis zwei Zeilen, die erklären, worum es geht und warum es jetzt relevant ist.]</p>
    </div>
    <div class="reveal">
      <div class="rule"></div>
      <dl class="meta">
        <div><dt>Datum</dt><dd>[Montag, 1. Januar 2026]</dd></div>
        <div><dt>Presenter</dt><dd>[Vorname &amp; Vorname]</dd></div>
        <div><dt>Format</dt><dd>[DAYONE Weekly]</dd></div>
      </dl>
    </div>
  </div>
</header>
""")

modul("01-einstieg-02-agenda", "agenda", """
<!-- Kein data-chapter: steht meist direkt nach dem Hero und ist selbst kein Kapitel.
     Die Kapitel-Nav erscheint dann erst nach der Agenda (siehe #agenda im Script). -->
<section class="agenda" id="agenda" data-modul="01 Einstieg/02 agenda">
  <div class="wrap">
    <h2 class="h2 reveal" style="margin-bottom:var(--space-12)">Agenda</h2>
    <div class="agenda-list">
      <div class="agenda-item reveal"><span class="num">01</span>
        <div><h3>[Agendapunkt 1]</h3><p>[Welche Frage klärt dieser Abschnitt?]</p></div></div>
      <div class="agenda-item reveal"><span class="num">02</span>
        <div><h3>[Agendapunkt 2]</h3><p>[Welche Frage klärt dieser Abschnitt?]</p></div></div>
      <div class="agenda-item reveal"><span class="num">03</span>
        <div><h3>[Agendapunkt 3]</h3><p>[Welche Frage klärt dieser Abschnitt?]</p></div></div>
      <div class="agenda-item reveal"><span class="num">04</span>
        <div><h3>[Agendapunkt 4]</h3><p>[Welche Frage klärt dieser Abschnitt?]</p></div></div>
    </div>
  </div>
</section>
""")

modul("02-struktur-01-section-divider", "divider", """
<!-- NUR verwenden, wenn im folgenden Kapitel viel Content kommt und es eine kurze
     Vorwarnung braucht. Reicht der direkte Einstieg, weglassen und Eyebrow +
     data-chapter stattdessen auf die nächste Sektion setzen. -->
<section class="divider dark" data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" data-modul="02 Struktur/01 section-divider">
  <div class="wrap reveal">
    <p class="eyebrow is-centered">[NN] — [Kapitelname]</p>
    <h2 class="h2">[Kapitelname]</h2>
  </div>
</section>
""")

modul("03-inhalt-03-sticky-nummernliste", "sticky-nummernliste", """
<section data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" data-modul="03 Inhalt/03 sticky-nummernliste">
  <div class="wrap sticky-list">
    <div class="left reveal">
      <p class="eyebrow">[NN] — [Kapitelname]</p>
      <h2 class="h1">[Die Leitfrage dieses Kapitels]</h2>
      <p class="lead" style="margin-top:var(--space-6)">[Zwei bis vier Sätze Kontext.]</p>
    </div>
    <div class="right">
      <div class="item reveal"><span class="num">01</span>
        <div><h3 class="h3">[Erster Punkt als Aussage]</h3>
        <p class="body" style="margin-top:12px">[Zwei bis vier Sätze.]</p></div></div>
      <div class="item reveal"><span class="num">02</span>
        <div><h3 class="h3">[Zweiter Punkt als Aussage]</h3>
        <p class="body" style="margin-top:12px">[Zwei bis vier Sätze.]</p></div></div>
      <div class="item reveal"><span class="num">03</span>
        <div><h3 class="h3">[Dritter Punkt als Aussage]</h3>
        <p class="body" style="margin-top:12px">[Zwei bis vier Sätze.]</p></div></div>
    </div>
  </div>
</section>
""")

modul("03-inhalt-04-karten-3er", "kartenraster", """
<section data-modul="03 Inhalt/04 karten-3er">
  <div class="wrap">
    <div class="section-head reveal">
      <div><h2 class="h1">[Wie gehen wir vor?]</h2></div>
      <p class="intro">[Ein Satz Einordnung — steht rechts neben der Headline.]</p>
    </div>
    <div class="cards">
      <div class="card reveal"><span class="label">[Option A]</span><h3 class="h3">[Titel]</h3>
        <p class="body">[2–3 Sätze.]</p><span class="tag">[Status]</span></div>
      <!-- is-selected = die gewählte Option, trägt als einzige Fläche -->
      <div class="card is-selected reveal"><span class="label">[Option B]</span><h3 class="h3">[Titel]</h3>
        <p class="body">[2–3 Sätze.]</p><span class="tag">[Gewählt]</span></div>
      <div class="card reveal"><span class="label">[Option C]</span><h3 class="h3">[Titel]</h3>
        <p class="body">[2–3 Sätze.]</p><span class="tag">[Nicht evaluiert]</span></div>
    </div>
  </div>
</section>
""")

modul("03-inhalt-05-prozess-schritte", "prozess-schritte-mit-rollen-spalten", """
<section data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" data-modul="03 Inhalt/05 prozess-schritte">
  <div class="wrap">
    <p class="eyebrow">[NN] — [Vorgehen]</p>
    <h2 class="h1 reveal" style="margin-bottom:var(--space-12)">[Wie läuft es ab?]</h2>
    <div class="process-steps">
      <div class="process-step reveal"><span class="num">01</span>
        <div class="process-step-body"><h3>[Erster Schritt]</h3>
          <div class="process-roles">
            <div class="process-role"><p class="role-name">[Rolle A]</p><p>[Was diese Rolle hier beiträgt.]</p></div>
            <div class="process-role"><p class="role-name">[Rolle B]</p><p>[Was diese Rolle hier beiträgt.]</p></div>
          </div></div></div>
      <div class="process-step reveal"><span class="num">02</span>
        <div class="process-step-body"><h3>[Zweiter Schritt]</h3>
          <div class="process-roles">
            <div class="process-role"><p class="role-name">[Rolle A]</p><p>[Was diese Rolle hier beiträgt.]</p></div>
            <div class="process-role"><p class="role-name">[Rolle B]</p><p>[Was diese Rolle hier beiträgt.]</p></div>
          </div></div></div>
      <div class="process-step reveal"><span class="num">03</span>
        <div class="process-step-body"><h3>[Dritter Schritt]</h3>
          <div class="process-roles">
            <div class="process-role"><p class="role-name">[Rolle A]</p><p>[Was diese Rolle hier beiträgt.]</p></div>
            <div class="process-role"><p class="role-name">[Rolle B]</p><p>[Was diese Rolle hier beiträgt.]</p></div>
          </div></div></div>
    </div>
  </div>
</section>
""")

modul("04-daten-01-kennzahlen-grid", "kennzahlen-dunkel", """
<section class="dark" data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" data-modul="04 Daten/01 kennzahlen-grid">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">[NN] — [Bilanz]</p>
        <h2 class="h1">[Das Projekt in Zahlen]</h2>
      </div>
    </div>
    <div class="stats">
      <div class="stat reveal"><div class="value" data-count-to="34">0</div>
        <div class="label">[Projekttage]</div><div class="note">[Kurze Einordnung.]</div></div>
      <div class="stat reveal"><div class="value" data-count-to="21">0</div>
        <div class="label">[Tage/Jahr gespart]</div><div class="note">[Kurze Einordnung.]</div></div>
      <div class="stat reveal"><div class="value" data-count-to="9">0</div>
        <div class="label">[Aktive Nutzer:innen]</div><div class="note">[Kurze Einordnung.]</div></div>
    </div>
  </div>
</section>
""")

modul("04-daten-03-matrix-2x2", "matrix-2x2", """
<section data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" data-modul="04 Daten/03 matrix-2x2">
  <div class="wrap">
    <p class="eyebrow">[NN] — [Einordnung]</p>
    <h2 class="h1 reveal" style="margin-bottom:var(--space-12)">[Vier Felder, zwei Achsen]</h2>
    <div class="matrix-wrap">
      <div class="matrix-axis-y">[ACHSE Y]</div>
      <div class="matrix-main">
        <div class="matrix-grid">
          <div class="matrix-quadrant reveal"><h3>[Quadrant A]</h3><p class="body">[1–2 Sätze zur Einordnung.]</p></div>
          <div class="matrix-quadrant reveal"><h3>[Quadrant B]</h3><p class="body">[1–2 Sätze zur Einordnung.]</p></div>
          <div class="matrix-quadrant reveal"><h3>[Quadrant C]</h3><p class="body">[1–2 Sätze zur Einordnung.]</p></div>
          <div class="matrix-quadrant reveal"><h3>[Quadrant D]</h3><p class="body">[1–2 Sätze zur Einordnung.]</p></div>
        </div>
        <div class="matrix-axis-x">[ACHSE X]</div>
      </div>
    </div>
  </div>
</section>
""")

modul("04-daten-05-tabelle", "hairline-tabelle", """
<section data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" data-modul="04 Daten/05 tabelle">
  <div class="wrap table-scroll">
    <p class="eyebrow">[NN] — [Übersicht]</p>
    <h2 class="h1 reveal" style="margin-bottom:var(--space-16)">[Tabellentitel]</h2>
    <table class="table reveal">
      <thead><tr><th>[Spalte A]</th><th>[Spalte B]</th><th>[Spalte C]</th><th>[Spalte D]</th></tr></thead>
      <tbody>
        <tr><td>[Zeile 1]</td><td>[Wert]</td><td>[Wert]</td><td>[Wert]</td></tr>
        <tr><td>[Zeile 2]</td><td>[Wert]</td><td>[Wert]</td><td>[Wert]</td></tr>
        <tr><td>[Zeile 3]</td><td>[Wert]</td><td>[Wert]</td><td>[Wert]</td></tr>
      </tbody>
    </table>
  </div>
</section>
""")

modul("06-zeitachse-01-roadmap-timeline", "roadmap-timeline", """
<section data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" data-modul="06 Zeitachse/01 roadmap-timeline">
  <div class="wrap">
    <p class="eyebrow">[NN] — [Timeline]</p>
    <h2 class="h1 reveal" style="margin-bottom:var(--space-20)">[Von wo bis wo?]</h2>
    <div class="timeline">
      <div class="timeline-progress"></div>
      <div class="timeline-track">
        <div class="timeline-item reveal"><span class="timeline-dot"></span>
          <span class="timeline-date">[Zeitpunkt 1]</span><span class="timeline-title">[Meilenstein 1]</span></div>
        <div class="timeline-item reveal"><span class="timeline-dot"></span>
          <span class="timeline-date">[Zeitpunkt 2]</span><span class="timeline-title">[Meilenstein 2]</span></div>
        <div class="timeline-item is-current reveal"><span class="timeline-dot"></span>
          <span class="timeline-date">[Zeitpunkt 3]</span><span class="timeline-title">[Meilenstein 3]</span>
          <span class="timeline-tag">Aktuell</span></div>
        <div class="timeline-item reveal"><span class="timeline-dot"></span>
          <span class="timeline-date">[Zeitpunkt 4]</span><span class="timeline-title">[Meilenstein 4]</span></div>
      </div>
    </div>
  </div>
</section>
""")

modul("07-media-04-grossbild", "gro-bild-randabfallend", """
<section data-modul="07 Media/04 grossbild">
  <div class="wrap">
    <p class="eyebrow">[NN] — [Eindruck]</p>
    <h2 class="h1 reveal" style="margin-bottom:var(--space-12)">[Was das Bild sagt — nicht was es zeigt]</h2>
  </div>
  <!-- Randabfallend: bricht bewusst aus dem Raster aus. Mind. 2880px breit. -->
  <img class="fullbleed reveal" src="[bild.jpg]" alt="[Was auf dem Bild zu sehen ist]" loading="lazy">
  <div class="wrap">
    <div class="caption">
      <p class="lead">[Ein Satz Einordnung, was hier zu sehen ist und warum es hier steht.]</p>
      <p class="small">[Foto: Name]</p>
    </div>
  </div>
</section>
""")

modul("08-menschen-01-team-grid", "team-grid", """
<section data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" data-modul="08 Menschen/01 team-grid">
  <div class="wrap">
    <p class="eyebrow">[NN] — [Team]</p>
    <h2 class="h1 reveal" style="margin-bottom:var(--space-20)">[Wer arbeitet daran?]</h2>
    <div class="team-grid">
      <div class="team-member reveal"><div class="team-avatar">[NN]</div><p class="name">[Name Nachname]</p><p class="role">[Rolle im Projekt]</p></div>
      <div class="team-member reveal"><div class="team-avatar">[NN]</div><p class="name">[Name Nachname]</p><p class="role">[Rolle im Projekt]</p></div>
      <div class="team-member reveal"><div class="team-avatar">[NN]</div><p class="name">[Name Nachname]</p><p class="role">[Rolle im Projekt]</p></div>
      <div class="team-member reveal"><div class="team-avatar">[NN]</div><p class="name">[Name Nachname]</p><p class="role">[Rolle im Projekt]</p></div>
    </div>
  </div>
</section>
""")

modul("08-menschen-03-quote-block", "zitat", """
<section class="quote" data-modul="08 Menschen/03 quote-block">
  <div class="wrap reveal">
    <blockquote>„[Ein prägnantes Zitat, ein bis zwei Sätze.]“</blockquote>
    <cite>[Name Nachname, Rolle]</cite>
  </div>
</section>
""")

modul("09-referenzen-02-facts-figures", "facts-figures", """
<section data-modul="09 Referenzen/02 facts-figures">
  <div class="wrap">
    <p class="eyebrow">[NN] — [Über uns]</p>
    <div class="facts">
      <div class="facts-image reveal">[Bild: Büro oder Team — kein Stockfoto]</div>
      <dl class="facts-list">
        <div class="facts-item reveal"><dt>[Kennzahl A]</dt><dd>[Wert]</dd></div>
        <div class="facts-item reveal"><dt>[Kennzahl B]</dt><dd>[Wert]</dd></div>
        <div class="facts-item reveal"><dt>[Kennzahl C]</dt><dd>[Wert]</dd></div>
        <div class="facts-item reveal"><dt>[Kennzahl D]</dt><dd>[Wert]</dd></div>
      </dl>
    </div>
  </div>
</section>
""")

modul("10-abschluss-01-karten-karussell", "takeaways-karussell", """
<!-- Generisches Modul für nummerierte Textinhalte, nicht nur für Abschluss-Takeaways.
     .carousel-shell begrenzt den Track auf --grid-max, damit die erste Karte am
     linken Grid-Rand startet statt am nackten Viewport-Rand. -->
<section data-chapter="[NN]" data-chapter-title="[Kapitelname]" id="kapitel-[nn]" style="padding-inline:0" data-modul="10 Abschluss/01 karten-karussell">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">[NN] — [Kapitelname]</p><h2 class="h1">[Was wir euch mitgeben]</h2></div>
    </div>
  </div>
  <div class="carousel-shell">
    <div class="carousel" id="karten-karussell">
      <div class="card"><span class="num">01</span>
        <div class="card-copy"><h3 class="h3">[Merksatz]</h3><p class="body">[2–3 Sätze.]</p></div></div>
      <div class="card"><span class="num">02</span>
        <div class="card-copy"><h3 class="h3">[Merksatz]</h3><p class="body">[2–3 Sätze.]</p></div></div>
      <div class="card"><span class="num">03</span>
        <div class="card-copy"><h3 class="h3">[Merksatz]</h3><p class="body">[2–3 Sätze.]</p></div></div>
      <div class="card"><span class="num">04</span>
        <div class="card-copy"><h3 class="h3">[Merksatz]</h3><p class="body">[2–3 Sätze.]</p></div></div>
    </div>
  </div>
  <div class="wrap carousel-controls">
    <button type="button" data-carousel="karten-karussell" data-dir="-1" aria-label="Zurück">‹</button>
    <button type="button" data-carousel="karten-karussell" data-dir="1" aria-label="Weiter">›</button>
  </div>
</section>
""")

modul("10-abschluss-03-cta-footer", "cta-footer", """
<footer class="cta dark" data-modul="10 Abschluss/03 cta-footer">
  <div class="wrap">
    <h2 class="h2 reveal">[Check it out.]</h2>
    <p class="lead reveal" style="margin-top:var(--space-4)">[Ein Satz Aufforderung.]</p>
    <div class="actions reveal">
      <a class="btn btn-primary" href="[URL]">[Zum Tool] <span aria-hidden="true">→</span></a>
      <a class="btn btn-secondary" href="[URL]">[Feedback] <span aria-hidden="true">→</span></a>
    </div>
    <div class="footer-row">
      <svg class="logo-mark" width="92" height="16" aria-label="DAYONE"><use href="#dayone-logo"></use></svg>
      <span>© 2026 DAYONE</span>
    </div>
  </div>
</footer>
""")


def main():
    fehlend = []
    for slug, (css_datei, markup) in MODULE.items():
        pfad_css = CSS / f"{css_datei}.css"
        if not pfad_css.exists():
            fehlend.append(css_datei)
            css = f"/* ==== {slug} ==== */\n"
        else:
            css = pfad_css.read_text().rstrip()
        (B / f"{slug}.html").write_text(
            f"<style>\n{css}\n</style>\n\n{markup}\n")
    print(f"{len(MODULE)} Bausteine geschrieben nach {B.relative_to(WURZEL)}/")
    if fehlend:
        print("CSS nicht gefunden für:", ", ".join(fehlend))


if __name__ == "__main__":
    main()
