# Dayonepager — Projektverlauf
### Gliederung für eine Team-Präsentation (inkl. Aufbau der Modulbibliothek in Figma)

---

## Teil 1 — Fundament: Die Modulbibliothek aufbauen

### 1. Ausgangslage und erster Schritt: Bestandsaufnahme statt Neubau

- Auftrag war ursprünglich, ein Component-System aus Figma-Design und Code aufzubauen — der erste Schritt war aber nicht bauen, sondern ehrlich prüfen, was schon da ist.
- Audit gegen drei echte Quellen gleichzeitig: den installierten Skill, das GitHub-Repository und die Figma-Datei live über den Figma-MCP.
- Zentraler Befund: Das Zielbild existierte bereits zu großen Teilen als laufendes System mit eigener CI — nicht als lose Idee. Die Aufgabe war also gezielt ergänzen, nicht neu erfinden.

---

### 2. Figma ↔ Code: die Verbindung der Modulbibliothek

- Alle 34 Module aus der Figma-Datei „DAYONE | AI-ready slides" live per Figma-MCP abgefragt und 1:1 gegen den Code abgeglichen — jede Komponente in Figma hat genau eine Datei in `bausteine/`.
- Die Figma-Component-Descriptions sind die tatsächliche Quelle für Zweck, Füllregeln und Abgrenzung jedes Moduls — nicht von Hand im Katalog gepflegt, sondern automatisch generiert.
- Eine einzige handgepflegte Datei (`modul-zuordnung.json`) verbindet Figma-Namen mit CSS-Klassen und Zählregeln — bewusst die einzige Stelle, die von Hand gepflegt wird, um keine zweite Wahrheit entstehen zu lassen.
- Eine CI-Prüfung stellt sicher, dass Code und Bausteine nie auseinanderlaufen können: Build schlägt fehl, wenn `bausteine/` und die daraus gebauten Seiten nicht übereinstimmen.

---

### 3. Modul für Modul gegen Figma geprüft

- Systematischer Durchgang durch alle 34 Module: Füllverhalten, Animation, Verhalten im Kontext (hell/dunkel, Kapitelmarker), bestehende Breakpoints — jeweils gegen Figma-Screenshot und Component-Description verifiziert, nicht nur gegen den Code gelesen.
- Bewusste Priorisierung mit Ernst abgestimmt: erst ein schneller Durchlauf über alle Module, Vertiefung nur dort, wo etwas auffiel — und Mobile-Breakpoints in Figma erst gezielt ergänzen, nachdem der Audit echte Lücken gezeigt hat, nicht pauschal vorab.
- Acht konkrete Korrekturen aus dem Durchlauf umgesetzt (zum Beispiel: Zebra-Streifen in der Tabelle, Bildreihenfolge bei „Bild-Intro" korrigiert, doppelte Case-Study-Zeile entfernt) — jede einzeln mit Ernst bestätigt, dann im geteilten Baustein statt nur lokal gefixt.
- Jede Korrektur sofort durch die volle Pipeline verifiziert: Katalog neu bauen, Seiten neu bauen, Qualitäts-Check, Selbsttest — nie „sieht gut aus" allein als Bestätigung genommen.

---

### 4. Modulnamen generalisiert — Figma und Code synchron umbenannt

- Acht Module trugen Namen, die nur für einen Anwendungsfall klangen, obwohl die Struktur generisch war — zum Beispiel `case-study-ziele`, das strukturell nur „Headline plus Liste" ist.
- Figma-Komponentennamen und Code in einem Zug umbenannt, damit die Figma-Datei als Source of Truth nie vom Repository abweicht — inklusive aller Cross-Referenzen in anderen Figma-Beschreibungen.
- Bewusst nicht angefasst: ein eingefrorener historischer Demo-Export, der nicht Teil der aktiven Pipeline ist — Aufwand nur dort investiert, wo es tatsächlich etwas verändert.
- Nach der Umbenennung die komplette Pipeline neu gebaut und das Repository per Volltextsuche auf verbliebene alte Namen durchsucht, um sicherzugehen, dass nichts übersehen wurde.

---

### 5. Animationen und Interaktionen geschärft

- Arbeitsweise bewusst klein gehalten: jeweils ein bis drei Animations-Muster bearbeiten, danach in einem gebündelten Browser-Test verifizieren, statt nach jeder Kleinigkeit neu zu testen.
- Am Beispiel des Steppers: Figma verlangte eigentlich ein automatisches „Scrollspy"-Verhalten, das im Code nie umgesetzt worden war — gemeinsam mit Ernst entschieden, die bestehenden Klick-Tabs zu behalten, aber den Panel-Wechsel visuell sauberer zu machen (sanftes Überblenden statt hartem Schnitt).
- Einen Bug gefunden, der nur im echten Browser sichtbar wurde, nicht beim Lesen des Codes: eine gestaffelte Verzögerung aus der ersten Einblend-Animation blieb am Element hängen und verzögerte versehentlich auch spätere Tab-Wechsel um einen zufälligen Betrag — durch einen gezielten Reset behoben.
- Das reduzierte-Bewegung-Verhalten (`prefers-reduced-motion`) für jede neue Animation ausdrücklich mitgeprüft, nicht nur den Normalfall.

---

## Teil 2 — Diese Session: Vom Rohsystem zum veröffentlichten Produkt

### 6. Iteratives Debugging anhand neuen Feedbacks

- Vier weitere, mit Screenshots gemeldete Fehler bearbeitet: Textgröße im Stepper, Reveal-Animationen vor dem eigentlichen Scrollen, eine falsche Zuordnung zwischen Roadmap und Gantt-Balken, Farbwechsel mitten im Kapitel statt an Kapitelgrenzen.
- Eine eigene Fehleinschätzung unterwegs korrigiert (zuerst die Tab-Beschriftung statt des Panel-Inhalts vergrößert) nach direkter Rückmeldung.
- Eine selbst verursachte Regression behoben: Die Korrektur des Scroll-Triggers hatte die Lade-Animation des Hero-Bereichs kaputt gemacht — eine Ausnahme ergänzt, damit der Hero beim ersten Laden zuverlässig animiert.

---

### 7. Aus Korrekturen dauerhafte Regeln machen

- Die zwei neuen Fehlerarten nicht nur gepatcht, sondern als zwei neue automatische Prüfungen in den Qualitäts-Check aufgenommen.
- Mit der bestehenden Selbsttest-Suite abgesichert, die eine bekannt-gute Seite gezielt sabotiert und prüft, ob der Check das erkennt.
- Ergebnis: Diese Fehlerarten können künftig nicht mehr unbemerkt zurückkommen — dasselbe Prinzip, das schon den gesamten Qualitäts-Check seit dem ursprünglichen Aufbau trägt.

---

### 8. Den Skill sauber umbenennen

- Durchgängig von `dayone-onepager` zu `dayonepager` umbenannt: Build-Tooling, `SKILL.md`, Dokumentation, Paketnamen — am Ende das gesamte Repository auf Reste durchsucht.
- Wichtige Unterscheidung in der Praxis gelernt: Den Anzeigenamen in der Skill-Verwaltung zu ändern ist etwas anderes, als den tatsächlichen Paket-Inhalt neu hochzuladen.

---

### 9. Der Skill plant seinen eigenen Launch

- Den Skill selbst benutzt, um Anleitung zur Veröffentlichung der eigenen Modul-Galerie zu bekommen — wie eine echte Nutzerin.
- Eine echte Umgebungsgrenze erkannt und berücksichtigt: Die Sandbox-Shell hat keinen GitHub-Zugang, `git push` musste aus einem echten Terminal laufen.

---

### 10. Landingpage veröffentlichen und an DAYONE-Standards ausrichten

- Das GitHub-Repository in Vercel verbunden, dabei echten bestehenden Inhalt auf der Live-Domain gefunden und vor jeder Änderung die Git-Historie geprüft, statt vorschnell zu überschreiben.
- Nach ausdrücklicher Freigabe eine eigens gebaute Landingpage veröffentlicht und anschließend mit `dayone-tone-of-voice` redigiert, mit der echten DAYONE-Wortmarke statt eines Platzhaltner-Logos versehen und eng an den Tokens und Komponenten-Konventionen des bestehenden Modulsystems ausgerichtet statt freien Stils.

---

### 11. Aktivierungsregeln des Skills verschärft

- Ursprünglich griff der Skill schon bei allgemeinen Begriffen wie „Präsentation" oder „Weekly".
- Jetzt nötig: entweder ein explizites Stichwort (Onepager, Online-Präsentation, Website-Pitch) oder die ausdrückliche Aussage, dass das Ergebnis teilbar sein soll.

---

### 12. Unternehmensweite Verteilung fehlerbehoben

- Einen „Geister-Skill" aufgeklärt: ein alter, separat veröffentlichter Eintrag im Organisations-Katalog, unabhängig vom bereits umbenannten persönlichen Skill.
- Die entscheidende Unterscheidung geklärt: Veröffentlichen macht einen Skill auffindbar, installiert ihn aber nicht automatisch bei allen — eine unternehmensweite Standardinstallation ist eine eigene, admin-seitige Stufe.

---

## Erkenntnisse

- Erst prüfen, was schon da ist, dann gezielt ergänzen — nicht neu bauen, was bereits funktioniert.
- Figma bleibt die einzige Design-Wahrheit; Code und Katalog werden automatisch daraus abgeleitet, nie von Hand parallel gepflegt.
- Jede Fehlerkorrektur wird zu einer automatischen Prüfung, damit sie nicht wiederkehren kann.
- Den eigenen Skill wie eine echte Nutzerin behandeln, deckt Lücken auf, die reines Lesen der Anleitung nie zeigen würde.
- Zuständigkeiten klar trennen: Skill-Inhalt vs. Skill-Name, Veröffentlichen vs. Installieren, persönliche Liste vs. geteilter Katalog.
