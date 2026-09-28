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


def test_raster_behaelt_beide_labels_bei_ueberlappender_linie():
    raster = erstelle_raster([1, 2], [2, 4], breite=41, hoehe=21)
    gesamter_text = "\n".join(raster)
    assert "A" in gesamter_text
    assert "B" in gesamter_text


def test_raster_markiert_ueberlappung_bei_identischen_vektoren():
    raster = erstelle_raster([3, 4], [3, 4], breite=41, hoehe=21)
    gesamter_text = "\n".join(raster)
    assert "X" in gesamter_text
