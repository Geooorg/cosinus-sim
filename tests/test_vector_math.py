import math

import pytest

from vector_math import skalarprodukt, betrag, cosinus_aehnlichkeit, winkel_in_grad


def test_skalarprodukt_berechnet_summe_der_produkte():
    assert skalarprodukt([1, 2, 3], [4, 5, 6]) == 32


def test_skalarprodukt_wirft_fehler_bei_unterschiedlicher_laenge():
    with pytest.raises(ValueError):
        skalarprodukt([1, 2], [1, 2, 3])


def test_betrag_berechnet_euklidische_norm():
    assert betrag([3, 4]) == 5.0


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
