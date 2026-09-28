# Design: Cosinus-Ähnlichkeit (Lernprojekt)

## Zielgruppe & Zweck

Kleines Python-Lernprojekt für Schüler der gymnasialen Oberstufe. Es soll
anschaulich vermitteln, wie die Cosinus-Ähnlichkeit zweier Vektoren berechnet
wird (Skalarprodukt, Normalisierung/Betrag, Einsetzen in die Formel) und wie
sich das Ergebnis geometrisch als Winkel zwischen zwei Vektoren interpretieren
lässt.

Das Projekt läuft komplett im Terminal (CLI), es werden keine externen
Bibliotheken verwendet (nur die Python-Standardbibliothek, insbesondere
`math`). Insbesondere das Skalarprodukt wird "von Hand" berechnet (keine
Nutzung von z.B. `numpy.dot`).

Alle Ausgaben, Erklärtexte und Code-Kommentare sind auf Deutsch.

## Phase 1: Berechnung der Cosinus-Ähnlichkeit

### Projektstruktur

```
cosinus-sim/
├── main.py                    # CLI-Einstiegspunkt: Eingabe, Ablauf, Ausgabe
├── vector_math.py             # reine Rechenfunktionen
├── visualisierung.py          # ASCII-Gitter-Zeichnung für den 2D-Fall (Phase 2)
├── tests/
│   └── test_vector_math.py    # Pytest-Tests für die reinen Rechenfunktionen
└── README.md                  # Kurzanleitung für Lehrkräfte/Schüler
```

### Eingabe

- Vektoren beliebiger Dimension (n ≥ 1), Dimension von A und B muss übereinstimmen.
- Eingabeformat: eine Zeile pro Vektor, Werte durch Leerzeichen getrennt
  (z.B. `3 4 1`). Werte werden als `float` interpretiert.
- Validierung mit Wiederholungs-Schleife: Bei ungültiger Eingabe (nicht-numerische
  Werte, unterschiedliche Länge von A und B, Nullvektor) wird eine verständliche
  Fehlermeldung ausgegeben und die Eingabe erneut abgefragt — das Programm
  bricht nicht ab.
- Ein Nullvektor wird abgelehnt, da die Normalisierung sonst durch 0 teilen
  würde (Cosinus-Ähnlichkeit ist für den Nullvektor nicht definiert).

### Ablauf

1. Kurze Begrüßung und Erklärung, was Cosinus-Ähnlichkeit ist und wofür man
   sie in der Praxis nutzt (z.B. Textähnlichkeit, Empfehlungssysteme).
2. Abfrage von Vektor A, dann Vektor B (inkl. Validierungsschleife, siehe oben).
3. Schritt-für-Schritt-Ausgabe der Berechnung (jeder Rechenschritt wird
   einzeln ausgegeben, nicht nur das Endergebnis):
   - **Skalarprodukt**: Ausgabe der einzelnen Produkte und der Summe, z.B.
     `(3·4) + (1·2) = 12 + 2 = 14`
   - **Betrag/Norm** von A und von B einzeln, inkl. sichtbarer
     Wurzelrechnung, z.B. `‖A‖ = √(3² + 1²) = √10 ≈ 3.1623`
   - **Cosinus-Ähnlichkeit**: Einsetzen der zuvor berechneten Werte in die
     Formel `cos(θ) = (A·B) / (‖A‖ · ‖B‖)`, danach das Ergebnis
   - Kurze qualitative Einordnung des Ergebnisses: nahe 1 = sehr ähnlich
     (kleiner Winkel), nahe 0 = unabhängig/orthogonal, negativ = gegensätzlich
     (Winkel > 90°)

### `vector_math.py` — Funktionen

- `skalarprodukt(a, b) -> float`: berechnet das Skalarprodukt ohne externe
  Bibliothek (Schleife/`zip` + Summation von Hand).
- `betrag(v) -> float`: berechnet die euklidische Norm über `math.sqrt`
  (Standardbibliothek, keine Einschränkung, da nur `numpy`/`scipy`-artige
  Vektor-Bibliotheken ausgeschlossen sind).
- `cosinus_aehnlichkeit(a, b) -> float`: nutzt `skalarprodukt` und `betrag`,
  wirft eine aussagekräftige Exception bei Nullvektor.
- Diese drei Funktionen sind reine Funktionen (keine Ein-/Ausgabe), damit sie
  isoliert testbar sind. Die Schritt-für-Schritt-Textausgabe für die Konsole
  erfolgt in `main.py`, das dieselben Zwischenwerte (Einzelprodukte,
  Teilsummen, Quadratsummen) noch einmal nachvollzieht bzw. anzeigt.

### Fehlerbehandlung

- Nicht-numerische Eingabe → Fehlermeldung, erneute Eingabe.
- Unterschiedliche Vektorlängen → Fehlermeldung, erneute Eingabe.
- Nullvektor → Fehlermeldung mit Erklärung (Division durch 0 bei der Norm),
  erneute Eingabe.

## Phase 2: Visualisierung im Terminal (nur für 2D-Vektoren)

Wenn beide eingegebenen Vektoren genau 2 Komponenten haben, wird zusätzlich
automatisch eine ASCII-Visualisierung angezeigt. Bei höherer Dimension wird
stattdessen ein Hinweis ausgegeben, dass die Visualisierung nur für
2D-Vektoren verfügbar ist.

### `visualisierung.py`

- Erzeugt ein Zeichen-Raster fester Größe (z.B. 41 Spalten × 21 Zeilen) mit
  Ursprung in der Mitte und x-/y-Achse als `-`/`|`, Ursprung als `+`.
- Automatische Skalierung: Der größte vorkommende Betrag einer Komponente
  beider Vektoren bestimmt den Skalierungsfaktor, sodass beide Vektoren
  vollständig ins Raster passen.
- Für jeden Vektor wird eine Linie vom Ursprung zur Vektorspitze gezeichnet,
  mit einem selbst implementierten, einfachen Linienalgorithmus (Bresenham),
  ebenfalls ohne externe Bibliothek. Jeder Vektor bekommt ein eigenes Symbol
  (z.B. `*` für A, `o` für B), die Spitze wird mit `A`/`B` markiert.
- Unter dem Raster wird eine Legende sowie der Winkel zwischen den Vektoren
  in Grad ausgegeben (`math.degrees(math.acos(cosinus_aehnlichkeit(a, b)))`).
- Die Rasterzeugung ist als reine Funktion umgesetzt (Eingabe: zwei Vektoren
  + Rastergröße, Ausgabe: Liste von Strings), damit sie ohne Terminal testbar
  ist.

## Tests

`tests/test_vector_math.py` (pytest) deckt ab:

- `skalarprodukt`/`betrag`/`cosinus_aehnlichkeit` für orthogonale Vektoren
  (Ergebnis 0), identische Richtung (Ergebnis 1), genau entgegengesetzte
  Vektoren (Ergebnis -1).
- Nullvektor löst die erwartete Exception aus.
- Grundlegende Tests für die Rastererzeugung in `visualisierung.py` (richtige
  Anzahl Zeilen/Spalten, Achsen und Ursprung vorhanden).

## README.md

Kurze Anleitung für Lehrkräfte/Schüler: Zweck des Projekts, Start mit
`python main.py`, Hinweis auf fehlende Abhängigkeiten (nur Python-
Standardbibliothek), kurze Motivation (wofür Cosinus-Ähnlichkeit in der
Praxis verwendet wird).

## Out of Scope

- Keine grafische Oberfläche, kein Web-Frontend.
- Keine Unterstützung für komplexe Zahlen oder andere Distanzmaße
  (euklidische Distanz, Manhattan-Distanz etc.).
- Keine Persistenz (keine Speicherung von Eingaben/Ergebnissen).
