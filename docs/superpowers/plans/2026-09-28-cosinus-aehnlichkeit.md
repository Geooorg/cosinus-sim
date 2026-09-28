# Cosinus-Ähnlichkeit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ein Python-CLI-Lernprojekt bauen, das die Cosinus-Ähnlichkeit zweier
Vektoren Schritt für Schritt berechnet, erklärt und (für 2D-Vektoren) als
ASCII-Grafik im Terminal visualisiert.

**Architecture:** Drei kleine Module mit klarer Verantwortung:
`vector_math.py` (reine, getestete Rechenfunktionen), `visualisierung.py`
(reine Rasterzeugung für den 2D-Fall) und `main.py` (CLI-Orchestrierung:
Eingabe, Schritt-für-Schritt-Ausgabe, Aufruf der Visualisierung). Die reinen
Funktionen werden per TDD entwickelt; `main.py` wird danach implementiert und
manuell verifiziert, da es auf interaktivem `input()` basiert.

**Tech Stack:** Python 3 (nur Standardbibliothek: `math`), pytest für Tests.

## Global Constraints

- Nur Python-Standardbibliothek für die gesamte Vektor-Mathematik (kein
  numpy/scipy o.ä.); `math.sqrt`/`math.acos`/`math.degrees` sind erlaubt.
- Das Skalarprodukt wird manuell berechnet (keine Nutzung von z.B.
  `numpy.dot` oder Ähnlichem).
- Alle Ausgaben, Docstrings und Kommentare im Code sind auf Deutsch.
- Tests werden mit pytest geschrieben und über `python -m pytest tests/ -v`
  ausgeführt (dadurch wird das Projektverzeichnis automatisch zu `sys.path`
  hinzugefügt, ohne zusätzliche Konfiguration).
- Die Visualisierung wird nur für exakt 2-dimensionale Vektoren aufgerufen;
  ansonsten zeigt `main.py` einen Hinweistext.

---

## Task 1: Vektor-Rechenfunktionen (`vector_math.py`)

**Files:**
- Create: `vector_math.py`
- Test: `tests/test_vector_math.py`

**Interfaces:**
- Produces:
  - `skalarprodukt(a: list[float], b: list[float]) -> float` — wirft
    `ValueError`, wenn `len(a) != len(b)`.
  - `betrag(v: list[float]) -> float`
  - `cosinus_aehnlichkeit(a: list[float], b: list[float]) -> float` — wirft
    `ValueError`, wenn `a` oder `b` der Nullvektor ist.
  - `winkel_in_grad(a: list[float], b: list[float]) -> float`

- [ ] **Step 1: Schreibe fehlschlagende Tests für `skalarprodukt`**

Erstelle `tests/test_vector_math.py`:

```python
import math

import pytest

from vector_math import skalarprodukt, betrag, cosinus_aehnlichkeit, winkel_in_grad


def test_skalarprodukt_berechnet_summe_der_produkte():
    assert skalarprodukt([1, 2, 3], [4, 5, 6]) == 32


def test_skalarprodukt_wirft_fehler_bei_unterschiedlicher_laenge():
    with pytest.raises(ValueError):
        skalarprodukt([1, 2], [1, 2, 3])
```

- [ ] **Step 2: Test ausführen und Fehlschlag bestätigen**

Run: `python -m pytest tests/test_vector_math.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'vector_math'`

- [ ] **Step 3: `vector_math.py` mit `skalarprodukt` anlegen**

Erstelle `vector_math.py`:

```python
"""Reine Rechenfunktionen für Vektoren (nur Python-Standardbibliothek)."""

import math


def skalarprodukt(a, b):
    """Berechnet das Skalarprodukt zweier Vektoren ohne externe Bibliothek."""
    if len(a) != len(b):
        raise ValueError("Vektoren müssen die gleiche Länge haben.")
    summe = 0.0
    for x, y in zip(a, b):
        summe += x * y
    return summe
```

- [ ] **Step 4: Test ausführen und Erfolg bestätigen**

Run: `python -m pytest tests/test_vector_math.py -v`
Expected: die beiden `skalarprodukt`-Tests PASSEN (die anderen Importe
schlagen noch fehl, da `betrag` usw. noch nicht existieren — das ist in
diesem Zwischenschritt erwartet, siehe Step 5).

- [ ] **Step 5: Commit**

```bash
git add vector_math.py tests/test_vector_math.py
git commit -m "feat: add skalarprodukt function"
```

- [ ] **Step 6: Fehlschlagenden Test für `betrag` ergänzen**

Füge in `tests/test_vector_math.py` hinzu:

```python
def test_betrag_berechnet_euklidische_norm():
    assert betrag([3, 4]) == 5.0
```

- [ ] **Step 7: Test ausführen und Fehlschlag bestätigen**

Run: `python -m pytest tests/test_vector_math.py::test_betrag_berechnet_euklidische_norm -v`
Expected: FAIL mit `ImportError: cannot import name 'betrag'`

- [ ] **Step 8: `betrag` implementieren**

Füge in `vector_math.py` hinzu:

```python
def betrag(v):
    """Berechnet die euklidische Norm (Länge) eines Vektors."""
    quadratsumme = 0.0
    for x in v:
        quadratsumme += x * x
    return math.sqrt(quadratsumme)
```

- [ ] **Step 9: Test ausführen und Erfolg bestätigen**

Run: `python -m pytest tests/test_vector_math.py::test_betrag_berechnet_euklidische_norm -v`
Expected: PASS

- [ ] **Step 10: Commit**

```bash
git add vector_math.py tests/test_vector_math.py
git commit -m "feat: add betrag function"
```

- [ ] **Step 11: Fehlschlagende Tests für `cosinus_aehnlichkeit` und `winkel_in_grad` ergänzen**

Füge in `tests/test_vector_math.py` hinzu:

```python
def test_cosinus_aehnlichkeit_orthogonaler_vektoren_ist_null():
    assert math.isclose(cosinus_aehnlichkeit([1, 0], [0, 1]), 0.0, abs_tol=1e-9)


def test_cosinus_aehnlichkeit_gleicher_richtung_ist_eins():
    assert math.isclose(cosinus_aehnlichkeit([1, 2], [2, 4]), 1.0, abs_tol=1e-9)


def test_cosinus_aehnlichkeit_entgegengesetzter_vektoren_ist_minus_eins():
    assert math.isclose(cosinus_aehnlichkeit([1, 0], [-1, 0]), -1.0, abs_tol=1e-9)


def test_cosinus_aehnlichkeit_wirft_fehler_bei_nullvektor():
    with pytest.raises(ValueError):
        cosinus_aehnlichkeit([0, 0], [1, 2])


def test_winkel_in_grad_bei_orthogonalen_vektoren_ist_90():
    assert math.isclose(winkel_in_grad([1, 0], [0, 1]), 90.0, abs_tol=1e-6)
```

- [ ] **Step 12: Test ausführen und Fehlschlag bestätigen**

Run: `python -m pytest tests/test_vector_math.py -v`
Expected: FAIL — die neuen Tests schlagen mit `ImportError: cannot import
name 'cosinus_aehnlichkeit'` fehl.

- [ ] **Step 13: `cosinus_aehnlichkeit` und `winkel_in_grad` implementieren**

Füge in `vector_math.py` hinzu:

```python
def cosinus_aehnlichkeit(a, b):
    """Berechnet die Cosinus-Ähnlichkeit zweier Vektoren."""
    norm_a = betrag(a)
    norm_b = betrag(b)
    if norm_a == 0 or norm_b == 0:
        raise ValueError(
            "Cosinus-Ähnlichkeit ist für den Nullvektor nicht definiert."
        )
    return skalarprodukt(a, b) / (norm_a * norm_b)


def winkel_in_grad(a, b):
    """Berechnet den Winkel zwischen zwei Vektoren in Grad."""
    cos_theta = cosinus_aehnlichkeit(a, b)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.degrees(math.acos(cos_theta))
```

- [ ] **Step 14: Alle Tests ausführen und Erfolg bestätigen**

Run: `python -m pytest tests/test_vector_math.py -v`
Expected: alle 9 Tests PASSEN

- [ ] **Step 15: Commit**

```bash
git add vector_math.py tests/test_vector_math.py
git commit -m "feat: add cosinus_aehnlichkeit and winkel_in_grad functions"
```

---

## Task 2: ASCII-Visualisierung (`visualisierung.py`)

**Files:**
- Create: `visualisierung.py`
- Test: `tests/test_visualisierung.py`

**Interfaces:**
- Consumes: nichts aus Task 1 (reine Geometrie, unabhängig von `vector_math.py`).
- Produces:
  - `erstelle_raster(a: list[float], b: list[float], breite: int = 41, hoehe: int = 21) -> list[str]`
    — wirft `ValueError`, wenn `len(a) != 2` oder `len(b) != 2`.

- [ ] **Step 1: Schreibe fehlschlagende Tests für `erstelle_raster`**

Erstelle `tests/test_visualisierung.py`:

```python
import pytest

from visualisierung import erstelle_raster


def test_raster_hat_richtige_abmessungen():
    raster = erstelle_raster([3, 4], [1, -2], breite=41, hoehe=21)
    assert len(raster) == 21
    assert all(len(zeile) == 41 for zeile in raster)


def test_raster_enthaelt_ursprung_und_achsen():
    raster = erstelle_raster([3, 4], [1, -2], breite=41, hoehe=21)
    mitte_x, mitte_y = 41 // 2, 21 // 2
    assert raster[mitte_y][mitte_x] == "+"
    assert raster[0][mitte_x] == "|"
    assert raster[mitte_y][0] == "-"


def test_raster_enthaelt_beide_vektor_label():
    raster = erstelle_raster([3, 4], [1, -2], breite=41, hoehe=21)
    gesamter_text = "\n".join(raster)
    assert "A" in gesamter_text
    assert "B" in gesamter_text


def test_erstelle_raster_wirft_fehler_bei_nicht_2d_vektoren():
    with pytest.raises(ValueError):
        erstelle_raster([1, 2, 3], [1, 2])
```

- [ ] **Step 2: Test ausführen und Fehlschlag bestätigen**

Run: `python -m pytest tests/test_visualisierung.py -v`
Expected: FAIL mit `ModuleNotFoundError: No module named 'visualisierung'`

- [ ] **Step 3: `visualisierung.py` implementieren**

Erstelle `visualisierung.py`:

```python
"""ASCII-Visualisierung von 2D-Vektoren im Terminal."""

SYMBOL_A = "*"
SYMBOL_B = "o"


def _linie_punkte(x0, y0, x1, y1):
    """Berechnet die Rasterpunkte einer Linie mit dem Bresenham-Algorithmus."""
    punkte = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    fehler = dx + dy
    x, y = x0, y0
    while True:
        punkte.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * fehler
        if e2 >= dy:
            fehler += dy
            x += sx
        if e2 <= dx:
            fehler += dx
            y += sy
    return punkte


def _vektor_zu_rasterpunkt(wert, mitte, skala, invertieren=False):
    verschiebung = wert * skala
    if invertieren:
        verschiebung = -verschiebung
    return round(mitte + verschiebung)


def erstelle_raster(a, b, breite=41, hoehe=21):
    """Erstellt ein ASCII-Koordinatenraster mit den Vektoren a und b.

    a und b müssen genau 2 Komponenten haben. Gibt eine Liste von
    Zeichenketten zurück, eine pro Zeile des Rasters.
    """
    if len(a) != 2 or len(b) != 2:
        raise ValueError("Die Visualisierung funktioniert nur für 2D-Vektoren.")

    mitte_x = breite // 2
    mitte_y = hoehe // 2
    max_radius = min(mitte_x, mitte_y) - 1

    max_betrag = max(
        (a[0] ** 2 + a[1] ** 2) ** 0.5,
        (b[0] ** 2 + b[1] ** 2) ** 0.5,
    )
    skala = max_radius / max_betrag if max_betrag > 0 else 1.0

    raster = [[" " for _ in range(breite)] for _ in range(hoehe)]

    for spalte in range(breite):
        raster[mitte_y][spalte] = "-"
    for zeile in range(hoehe):
        raster[zeile][mitte_x] = "|"
    raster[mitte_y][mitte_x] = "+"

    for vektor, symbol, label in ((a, SYMBOL_A, "A"), (b, SYMBOL_B, "B")):
        ziel_x = _vektor_zu_rasterpunkt(vektor[0], mitte_x, skala)
        ziel_y = _vektor_zu_rasterpunkt(vektor[1], mitte_y, skala, invertieren=True)
        punkte = _linie_punkte(mitte_x, mitte_y, ziel_x, ziel_y)
        for x, y in punkte[1:-1]:
            if 0 <= x < breite and 0 <= y < hoehe:
                raster[y][x] = symbol
        if 0 <= ziel_x < breite and 0 <= ziel_y < hoehe:
            raster[ziel_y][ziel_x] = label

    return ["".join(zeile) for zeile in raster]
```

- [ ] **Step 4: Test ausführen und Erfolg bestätigen**

Run: `python -m pytest tests/test_visualisierung.py -v`
Expected: alle 4 Tests PASSEN

- [ ] **Step 5: Commit**

```bash
git add visualisierung.py tests/test_visualisierung.py
git commit -m "feat: add ascii grid visualization for 2d vectors"
```

---

## Task 3: CLI-Ablauf (`main.py`)

**Files:**
- Create: `main.py`

**Interfaces:**
- Consumes:
  - Aus `vector_math.py`: `skalarprodukt(a, b)`, `betrag(v)`,
    `cosinus_aehnlichkeit(a, b)`, `winkel_in_grad(a, b)`
  - Aus `visualisierung.py`: `erstelle_raster(a, b, breite=41, hoehe=21) -> list[str]`
- Produces: `main()` als Einstiegspunkt (`if __name__ == "__main__": main()`);
  keine weiteren öffentlichen Interfaces, die von anderen Tasks gebraucht
  werden.

Da `main.py` auf interaktivem `input()` basiert, wird dieser Task nicht mit
automatisierten Tests, sondern mit manuellen Verifikationsschritten
abgeschlossen (siehe Steps 3-5).

- [ ] **Step 1: `main.py` implementieren**

Erstelle `main.py`:

```python
"""CLI für die schrittweise Berechnung und Visualisierung der Cosinus-Ähnlichkeit."""

from vector_math import skalarprodukt, betrag, cosinus_aehnlichkeit, winkel_in_grad
from visualisierung import erstelle_raster


def lese_vektor(bezeichnung):
    while True:
        eingabe = input(f"Vektor {bezeichnung} (Werte durch Leerzeichen getrennt): ")
        try:
            vektor = [float(wert) for wert in eingabe.split()]
        except ValueError:
            print("Bitte nur Zahlen eingeben, getrennt durch Leerzeichen.\n")
            continue
        if len(vektor) == 0:
            print("Bitte mindestens einen Wert eingeben.\n")
            continue
        if betrag(vektor) == 0:
            print("Der Nullvektor ist nicht erlaubt (Division durch 0 bei der Normalisierung).\n")
            continue
        return vektor


def lese_zwei_vektoren():
    a = lese_vektor("A")
    while True:
        b = lese_vektor("B")
        if len(a) != len(b):
            print(f"Vektor B muss wie Vektor A genau {len(a)} Werte haben.\n")
            continue
        return a, b


def zeige_skalarprodukt_schritte(a, b):
    print("Schritt 1: Skalarprodukt (Punktprodukt)")
    produkte = [x * y for x, y in zip(a, b)]
    terme = " + ".join(f"({x:g}·{y:g})" for x, y in zip(a, b))
    zwischenwerte = " + ".join(f"{p:g}" for p in produkte)
    ergebnis = skalarprodukt(a, b)
    print(f"  A · B = {terme}")
    print(f"        = {zwischenwerte}")
    print(f"        = {ergebnis:g}")
    print()
    return ergebnis


def zeige_betrag_schritte(v, name):
    print(f"Schritt: Betrag (Norm) von {name}")
    quadrate = " + ".join(f"{x:g}²" for x in v)
    quadratsumme = sum(x * x for x in v)
    ergebnis = betrag(v)
    print(f"  ‖{name}‖ = √({quadrate})")
    print(f"       = √({quadratsumme:g})")
    print(f"       ≈ {ergebnis:.4f}")
    print()
    return ergebnis


def zeige_cosinus_schritt(a, b, norm_a, norm_b, skalar):
    print("Schritt: Cosinus-Ähnlichkeit")
    ergebnis = cosinus_aehnlichkeit(a, b)
    print("  cos(θ) = (A · B) / (‖A‖ · ‖B‖)")
    print(f"         = {skalar:g} / ({norm_a:.4f} · {norm_b:.4f})")
    print(f"         ≈ {ergebnis:.4f}")
    print()
    return ergebnis


def interpretiere(ergebnis):
    if ergebnis > 0.9:
        return "Die Vektoren sind sich sehr ähnlich (kleiner Winkel)."
    if ergebnis > 0.1:
        return "Die Vektoren sind sich teilweise ähnlich."
    if ergebnis >= -0.1:
        return "Die Vektoren sind (nahezu) unabhängig voneinander (orthogonal)."
    if ergebnis >= -0.9:
        return "Die Vektoren sind sich eher unähnlich (großer Winkel)."
    return "Die Vektoren zeigen (nahezu) in entgegengesetzte Richtungen."


def main():
    print("=== Cosinus-Ähnlichkeit ===")
    print(
        "Die Cosinus-Ähnlichkeit misst, wie ähnlich sich zwei Vektoren in ihrer\n"
        "Richtung sind - unabhängig von ihrer Länge. Sie wird z.B. verwendet, um\n"
        "die Ähnlichkeit von Texten oder Empfehlungen zu berechnen.\n"
    )

    a, b = lese_zwei_vektoren()
    print()

    skalar = zeige_skalarprodukt_schritte(a, b)
    norm_a = zeige_betrag_schritte(a, "A")
    norm_b = zeige_betrag_schritte(b, "B")
    ergebnis = zeige_cosinus_schritt(a, b, norm_a, norm_b, skalar)

    print(f"Ergebnis: cos(θ) ≈ {ergebnis:.4f}")
    print(interpretiere(ergebnis))
    print()

    if len(a) == 2 and len(b) == 2:
        winkel = winkel_in_grad(a, b)
        print("=== Visualisierung ===")
        for zeile in erstelle_raster(a, b):
            print(zeile)
        print("\nLegende: * = Vektor A, o = Vektor B")
        print(f"Winkel zwischen den Vektoren: {winkel:.2f}°")
    else:
        print("Hinweis: Die Visualisierung ist nur für 2D-Vektoren verfügbar.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Bestehende Tests erneut ausführen**

Run: `python -m pytest tests/ -v`
Expected: alle bisherigen Tests (aus Task 1 und 2) PASSEN weiterhin
unverändert.

- [ ] **Step 3: Manueller Test — 2D-Vektoren, Happy Path**

Run: `python main.py`
Eingabe: `3 4` (Vektor A), dann `4 3` (Vektor B)
Expected: Alle Rechenschritte werden nacheinander ausgegeben
(Skalarprodukt = 24, ‖A‖ ≈ 5.0000, ‖B‖ ≈ 5.0000, cos(θ) ≈ 0.9600), danach
erscheint das ASCII-Raster mit sichtbaren Linien zu den Punkten `A` und `B`
sowie der Winkel in Grad.

- [ ] **Step 4: Manueller Test — Vektoren mit mehr als 2 Dimensionen**

Run: `python main.py`
Eingabe: `1 2 3` (Vektor A), dann `4 5 6` (Vektor B)
Expected: Die Rechenschritte werden korrekt ausgegeben, am Ende erscheint
statt der Visualisierung der Hinweistext "Hinweis: Die Visualisierung ist
nur für 2D-Vektoren verfügbar." Kein Absturz.

- [ ] **Step 5: Manueller Test — ungültige Eingaben**

Run: `python main.py`
Eingaben nacheinander testen (jeweils neuer Programmlauf oder direkt nach
Fehlermeldung weiter eintippen):
- Für Vektor A: `abc` → Erwartet: Fehlermeldung "Bitte nur Zahlen eingeben,
  getrennt durch Leerzeichen." und erneute Abfrage von Vektor A.
- Für Vektor A: `0 0` → Erwartet: Fehlermeldung zum Nullvektor, erneute
  Abfrage von Vektor A.
- Vektor A: `1 2`, Vektor B: `1 2 3` → Erwartet: Fehlermeldung "Vektor B
  muss wie Vektor A genau 2 Werte haben.", erneute Abfrage von Vektor B.

In allen drei Fällen darf das Programm nicht abstürzen, sondern muss die
Eingabe erneut anfordern.

- [ ] **Step 6: Commit**

```bash
git add main.py
git commit -m "feat: add cli entry point for cosine similarity walkthrough"
```

---

## Task 4: Dokumentation (`README.md`)

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: Dateinamen und Befehle aus Task 1-3 (`main.py`, `tests/`).
- Produces: nichts, das von Code konsumiert wird — reine Dokumentation.

- [ ] **Step 1: `README.md` schreiben**

Erstelle `README.md`:

```markdown
# Cosinus-Ähnlichkeit – Lernprojekt

Ein kleines Python-Kommandozeilen-Projekt für Schüler der Oberstufe, um die
Berechnung der **Cosinus-Ähnlichkeit** zweier Vektoren Schritt für Schritt
nachzuvollziehen.

## Worum geht es?

Die Cosinus-Ähnlichkeit misst, wie ähnlich sich zwei Vektoren in ihrer
Richtung sind – unabhängig von ihrer Länge. Sie wird z.B. verwendet, um die
Ähnlichkeit von Texten (als Wortvektoren) oder in Empfehlungssystemen zu
berechnen.

Das Programm fragt zwei Vektoren ab, zeigt dann jeden Rechenschritt einzeln
an (Skalarprodukt, Betrag/Normalisierung, Einsetzen in die Formel) und gibt
am Ende das Ergebnis mit einer kurzen Einordnung aus. Sind beide Vektoren
2-dimensional, wird zusätzlich eine einfache ASCII-Visualisierung im
Terminal angezeigt.

## Voraussetzungen

- Python 3.9 oder neuer
- Keine externen Pakete nötig, um das Programm auszuführen (nur die
  Python-Standardbibliothek)
- Für die Tests: `pip install pytest`

## Ausführen

```bash
python main.py
```

Beispiel-Eingabe:

```
Vektor A (Werte durch Leerzeichen getrennt): 3 4
Vektor B (Werte durch Leerzeichen getrennt): 4 3
```

## Tests ausführen

```bash
python -m pytest tests/ -v
```

## Projektstruktur

- `main.py` – Kommandozeilen-Ablauf (Eingabe, Ausgabe der Rechenschritte)
- `vector_math.py` – reine Rechenfunktionen (Skalarprodukt, Betrag,
  Cosinus-Ähnlichkeit, Winkel)
- `visualisierung.py` – ASCII-Koordinatenraster für 2D-Vektoren
- `tests/` – Pytest-Tests für `vector_math.py` und `visualisierung.py`
```

- [ ] **Step 2: Gesamte Test-Suite ein letztes Mal ausführen**

Run: `python -m pytest tests/ -v`
Expected: alle Tests aus Task 1 und Task 2 PASSEN (13 Tests insgesamt)

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add README with usage instructions"
```
