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


def betrag(v):
    """Berechnet die euklidische Norm (Länge) eines Vektors."""
    quadratsumme = 0.0
    for x in v:
        quadratsumme += x * x
    return math.sqrt(quadratsumme)


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
