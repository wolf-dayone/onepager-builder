# Animationen

Wie sich dieses System bewegt — und warum es sich genau so bewegt.
Wer ein Modul baut oder ändert, liest das hier, bevor er eine `transition`
schreibt.

## Grundsatz

Bewegung ist hier kein Effekt, sondern Reihenfolge. Sie sagt, **was zuerst
gilt** und **was woraus folgt**: erst der Kapitelmarker, dann die Aussage, dann
der Beleg. Alles, was diese Reihenfolge nicht trägt, bewegt sich nicht.

Drei Regeln, aus denen alles andere folgt:

1. **Nichts läuft beim Laden.** Jede Sektion animiert erst, wenn man sie
   erreicht. Wer oben einsteigt, sieht den Hero laufen — und sonst nichts.
2. **Eine Sache bewegt sich pro Ebene.** Der Marker blendet auf, die Headline
   kommt hoch, die Linie zeichnet sich. Nicht alles gleichzeitig und nicht
   alles auf dieselbe Art.
3. **Ankommen, nicht abbremsen.** Alle Einblendungen laufen auf einer
   Ease-out-Kurve: schneller Start, langes Ausrollen.

## Warum kein motion.js

Die Frage stand im Raum, die Antwort ist bewusst „nein":

- Jede gebaute Seite ist **eine einzige HTML-Datei ohne externe Requests** —
  sie muss im Meetingraum ohne Netz laufen und als Anhang verschickbar sein.
  Eine Bibliothek müsste dafür in jede Datei einkopiert werden, in jede.
- Die Choreografien hier sind **Reihenfolgen, keine Physik**: nacheinander
  einblenden, eine Linie ziehen, einen Balken wachsen lassen. Das kann CSS
  nativ, und der Browser rechnet es auf dem Compositor statt in JS.
- Wo wirklich sequenziert werden muss (Zeitachse, Schreibmaschine, Gantt),
  steht die Logik in `bausteine/_basis.js` — dieselbe Stelle, an der auch der
  QA-Replay hängt. Eine zweite Zeitachse in einer Bibliothek müsste damit
  synchron gehalten werden.

Sollte das kippen — echte Physik, Gesten, verschachtelte Timelines — ist der
Einstiegspunkt `_basis.js`, nicht das einzelne Modul.

## Tokens

Dauern und Kurven stehen **nur** in `referenzen/tokens.css`. Kein Modul
schreibt eigene Millisekunden.

| Token | Wert | Wofür |
|---|---|---|
| `--ease-reveal` | `cubic-bezier(.22,1,.36,1)` | Einblendungen |
| `--ease-linie` | `cubic-bezier(.65,0,.35,1)` | Linien, Balken, Strecken |
| `--ease-ui` | `cubic-bezier(.33,1,.68,1)` | Hover, Fokus, Tabwechsel |
| `--dur-ui` | `0.2s` | UI-Reaktionen |
| `--dur-reveal` | `1.1s` | Standard-Einblendung |
| `--dur-linie` | `0.8s` | Linien-Reveal, Balkenwachstum |
| `--dur-lang` | `1.4s` | lange Strecken (Zeitachsen-Segment) |

## Die Reveal-Rolle

Ein Element, das beim Reinscrollen erscheinen soll, bekommt `.reveal` — mehr
nicht. `stageReveal()` in `_basis.js` staffelt alle `.reveal` einer Sektion in
DOM-Reihenfolge.

```html
<p class="eyebrow reveal">…<span class="eyebrow-linie"></span></p>
<h2 class="h2 reveal">…</h2>
<p class="lead reveal">…</p>
```

Varianten:

- `.reveal.ist-nur-opacity` — erscheint ohne Ortswechsel. Für alles, was seine
  Position selbst aussagt: Achsenlabel, Quadranten, Prozesskarten.
- `.linie-oben` — zieht zusätzlich eine 1px-Linie über die volle Breite des
  Elements ein, **synchron mit dem Element selbst**. Farbe über
  `--linie-farbe`.

### `--reveal-delay` statt `transition-delay`

Die Staffelung liegt als Custom Property auf dem Element, nicht als
Inline-`transition-delay`. Grund: ein Inline-Style erreicht keine
Pseudo-Elemente. Die Linien in `.linie-oben::before` starteten dadurch alle
gleichzeitig, während ihre Blöcke gestaffelt hochkamen — der letzte Block schob
sich mit fertig gezeichneter Linie ins Bild. Über die Property erben
`::before`/`::after` dieselbe Verzögerung.

Wer eine eigene verzögerte Transition schreibt, hängt sich dort ein:

```css
.mein-element{transition-delay:var(--reveal-delay,0ms)}
```

### Takt pro Sektion

Standard sind 130 ms Abstand, gedeckelt bei 900 ms. Eine Sektion darf enger
takten:

```html
<section data-stagger="90" …>
```

Faustregel: viele gleichartige Elemente (Logowand, Agenda) enger, wenige große
Blöcke im Standardtakt.

## Choreografien mit eigener Logik

Vier Module brauchen mehr als Staffelung. Sie liegen in `_basis.js`, jeweils
mit einer `replay…()`-Funktion für die QA-Leiste:

- **Chart-Slide** (`growChart`) — leeres Diagramm zuerst, dann wachsen die
  Säulen nacheinander von unten, der Zähler läuft mit, der Wert erscheint erst
  beim Wachsen.
- **Zeitachse** (`timelineAbspielen`) — Punkt setzt sich, Beschriftung folgt,
  Linie wächst zum nächsten Punkt, von vorn. Der aktuelle Punkt pulsiert
  danach dauerhaft weiter; die Strecke zu künftigen Meilensteinen ist
  gestrichelt und grau.
- **Gantt** (`ganttAusfahren`) — Balken fahren nacheinander von links auf.
- **Zitat** (`zitatTippen`) — der Satz wird getippt, die Quelle blendet erst
  danach auf.

## Bewegung reduzieren

`prefers-reduced-motion: reduce` ist kein Sonderfall, den man am Ende
nachreicht. Jede neue Animation braucht ihren Ausschalter in derselben Datei:

```css
@media(prefers-reduced-motion:reduce){
  .mein-element{transform:none;transition:none}
}
```

In JS fragt `reduceMotion()` denselben Zustand ab — die QA-Leiste schaltet ihn
zum Testen um, ohne dass man die Systemeinstellung anfassen muss.

## Prüfen

`modul-galerie.html` ist die Teststrecke: jedes Modul einmal, in echter
Sektionshöhe, mit Farbwechsel-Rhythmus. Die Leiste unten zeigt das aktuelle
Modul und bietet „Replay current" / „Replay all", dazu Schalter für Animationen
und Reduced Motion.

Die Galerie spielt beim Laden **nichts** vor — genau wie eine echte Seite. Was
man sehen will, scrollt man an oder spielt man per Knopf noch einmal ab.
