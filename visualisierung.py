"""ASCII-Visualisierung von 2D-Vektoren im Terminal."""

SYMBOL_A = "*"
SYMBOL_B = "o"
SYMBOL_UEBERLAPP = "X"


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

    ziel_a = (
        _vektor_zu_rasterpunkt(a[0], mitte_x, skala),
        _vektor_zu_rasterpunkt(a[1], mitte_y, skala, invertieren=True),
    )
    ziel_b = (
        _vektor_zu_rasterpunkt(b[0], mitte_x, skala),
        _vektor_zu_rasterpunkt(b[1], mitte_y, skala, invertieren=True),
    )

    # Erst beide Linien zeichnen, danach beide Labels setzen - so bleiben
    # beide Labels sichtbar, auch wenn die Linie eines Vektors über die
    # Spitze des anderen verläuft (z.B. bei gleicher Richtung).
    for ziel, symbol in ((ziel_a, SYMBOL_A), (ziel_b, SYMBOL_B)):
        punkte = _linie_punkte(mitte_x, mitte_y, ziel[0], ziel[1])
        for x, y in punkte[1:-1]:
            if 0 <= x < breite and 0 <= y < hoehe:
                raster[y][x] = symbol

    if ziel_a == ziel_b:
        x, y = ziel_a
        if 0 <= x < breite and 0 <= y < hoehe:
            raster[y][x] = SYMBOL_UEBERLAPP
    else:
        for ziel, label in ((ziel_a, "A"), (ziel_b, "B")):
            x, y = ziel
            if 0 <= x < breite and 0 <= y < hoehe:
                raster[y][x] = label

    return ["".join(zeile) for zeile in raster]
