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
