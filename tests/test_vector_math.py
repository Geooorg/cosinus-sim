import math

import pytest

from vector_math import skalarprodukt, betrag


def test_skalarprodukt_berechnet_summe_der_produkte():
    assert skalarprodukt([1, 2, 3], [4, 5, 6]) == 32


def test_skalarprodukt_wirft_fehler_bei_unterschiedlicher_laenge():
    with pytest.raises(ValueError):
        skalarprodukt([1, 2], [1, 2, 3])


def test_betrag_berechnet_euklidische_norm():
    assert betrag([3, 4]) == 5.0
