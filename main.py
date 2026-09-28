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
