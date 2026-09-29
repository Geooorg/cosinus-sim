import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Scanner;

/**
 * CLI für die schrittweise Berechnung und Visualisierung der Cosinus-Ähnlichkeit.
 */
public class Main {

    // ANSI-Farbcodes als Ersatz für colorama
    public static final String ANSI_RED = "\u001B[31m";
    public static final String ANSI_BLUE = "\u001B[34m";
    public static final String ANSI_MAGENTA = "\u001B[35m";
    public static final String ANSI_RESET = "\u001B[0m";

    public static final String SYMBOL_A = "*";
    public static final String SYMBOL_B = "o";
    public static final String SYMBOL_UEBERLAPP = "X";

    private static final Map<String, String> FARBEN = new HashMap<>();

    static {
        FARBEN.put(SYMBOL_A, ANSI_RED);
        FARBEN.put("A", ANSI_RED);
        FARBEN.put(SYMBOL_B, ANSI_BLUE);
        FARBEN.put("B", ANSI_BLUE);
        FARBEN.put(SYMBOL_UEBERLAPP, ANSI_MAGENTA);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("=== Cosinus-Ähnlichkeit ===");
        System.out.println(
            "Die Cosinus-Ähnlichkeit misst, wie ähnlich sich zwei Vektoren in ihrer\n" +
            "Richtung sind - unabhängig von ihrer Länge. Sie wird z.B. verwendet, um\n" +
            "die Ähnlichkeit von Texten oder Empfehlungen zu berechnen.\n"
        );

        double[][] vektoren = liesZweiVektoren(scanner);
        double[] a = vektoren[0];
        double[] b = vektoren[1];
        System.out.println();

        double skalar = zeigeSkalarproduktSchritte(a, b);
        double normA = zeigeBetragSchritte(a, "A");
        double normB = zeigeBetragSchritte(b, "B");
        double ergebnis = zeigeCosinusSchritt(a, b, normA, normB, skalar);

        System.out.printf(Locale.US, "Ergebnis: cos(θ) ≈ %.4f%n", ergebnis);
        System.out.println(interpretiere(ergebnis));
        System.out.println();

        if (a.length == 2 && b.length == 2) {
            double winkel = winkelInGrad(a, b);
            System.out.println("=== Visualisierung ===");
            List<String> raster = erstelleRaster(a, b);
            for (String zeile : faerbeRaster(raster)) {
                System.out.println(zeile);
            }
            System.out.printf(
                "%nLegende: %s* = Vektor A%s, %so = Vektor B%s, %sX = A und B (gleiche Richtung)%s%n",
                ANSI_RED, ANSI_RESET, ANSI_BLUE, ANSI_RESET, ANSI_MAGENTA, ANSI_RESET
            );
            System.out.printf(Locale.US, "Winkel zwischen den Vektoren: %.2f°%n", winkel);
        } else {
            System.out.println("Hinweis: Die Visualisierung ist nur für 2D-Vektoren verfügbar.");
        }

        scanner.close();
    }

    /**
     * Färbt die Vektor-Symbole und -Labels im ASCII-Raster ein.
     */
    public static List<String> faerbeRaster(List<String> raster) {
        List<String> gefaerbteZeilen = new ArrayList<>();
        for (String zeile : raster) {
            StringBuilder gefaerbt = new StringBuilder();
            for (char zeichenChar : zeile.toCharArray()) {
                String zeichen = String.valueOf(zeichenChar);
                if (FARBEN.containsKey(zeichen)) {
                    gefaerbt.append(FARBEN.get(zeichen)).append(zeichen).append(ANSI_RESET);
                } else {
                    gefaerbt.append(zeichen);
                }
            }
            gefaerbteZeilen.add(gefaerbt.toString());
        }
        return gefaerbteZeilen;
    }

    /**
     * Liest einen Vektor von der Konsole ein und validiert die Eingabe.
     */
    public static double[] liesVektor(Scanner scanner, String bezeichnung) {
        while (true) {
            System.out.printf("Vektor %s (Werte durch Leerzeichen getrennt): ", bezeichnung);
            String eingabe = scanner.nextLine().trim();

            if (eingabe.isEmpty()) {
                System.out.println("Bitte mindestens einen Wert eingeben.\n");
                continue;
            }

            String[] teile = eingabe.split("\\s+");
            double[] vektor = new double[teile.length];
            boolean gueltig = true;

            for (int i = 0; i < teile.length; i++) {
                try {
                    vektor[i] = Double.parseDouble(teile[i]);
                } catch (NumberFormatException e) {
                    System.out.println("Bitte nur Zahlen eingeben, getrennt durch Leerzeichen.\n");
                    gueltig = false;
                    break;
                }
            }

            if (!gueltig) {
                continue;
            }

            boolean endlicheZahlen = true;
            for (double wert : vektor) {
                if (!Double.isFinite(wert)) {
                    endlicheZahlen = false;
                    break;
                }
            }

            if (!endlicheZahlen) {
                System.out.println("Bitte nur endliche Zahlen eingeben (kein 'nan' oder 'inf').\n");
                continue;
            }

            if (betrag(vektor) == 0) {
                System.out.println("Der Nullvektor ist nicht erlaubt (Division durch 0 bei der Normalisierung).\n");
                continue;
            }

            return vektor;
        }
    }

    /**
     * Liest zwei Vektoren gleicher Dimension ein.
     */
    public static double[][] liesZweiVektoren(Scanner scanner) {
        double[] a = liesVektor(scanner, "A");
        while (true) {
            double[] b = liesVektor(scanner, "B");
            if (a.length != b.length) {
                System.out.printf("Vektor B muss wie Vektor A genau %d Werte haben.%n%n", a.length);
                continue;
            }
            return new double[][]{a, b};
        }
    }

    public static double zeigeSkalarproduktSchritte(double[] a, double[] b) {
        System.out.println("Schritt 1: Skalarprodukt (Punktprodukt)");
        List<String> termeList = new ArrayList<>();
        List<String> zwischenwerteList = new ArrayList<>();

        for (int i = 0; i < a.length; i++) {
            termeList.add(String.format("(%s·%s)", formatG(a[i]), formatG(b[i])));
            zwischenwerteList.add(formatG(a[i] * b[i]));
        }

        String terme = String.join(" + ", termeList);
        String zwischenwerte = String.join(" + ", zwischenwerteList);
        double ergebnis = skalarprodukt(a, b);

        System.out.printf("  A · B = %s%n", terme);
        System.out.printf("        = %s%n", zwischenwerte);
        System.out.printf("        = %s%n%n", formatG(ergebnis));
        return ergebnis;
    }

    public static double zeigeBetragSchritte(double[] v, String name) {
        System.out.printf("Schritt: Betrag (Norm) von %s%n", name);
        List<String> quadrateList = new ArrayList<>();
        double quadratsumme = 0.0;

        for (double x : v) {
            if (x < 0) {
                quadrateList.add(String.format("(%s)²", formatG(x)));
            } else {
                quadrateList.add(String.format("%s²", formatG(x)));
            }
            quadratsumme += x * x;
        }

        String quadrate = String.join(" + ", quadrateList);
        double ergebnis = betrag(v);

        System.out.printf("  ‖%s‖ = √(%s)%n", name, quadrate);
        System.out.printf("       = √(%s)%n", formatG(quadratsumme));
        System.out.printf(Locale.US, "       ≈ %.4f%n%n", ergebnis);
        return ergebnis;
    }

    public static double zeigeCosinusSchritt(double[] a, double[] b, double normA, double normB, double skalar) {
        System.out.println("Schritt: Cosinus-Ähnlichkeit");
        double ergebnis = cosinusAehnlichkeit(a, b);
        System.out.println("  cos(θ) = (A · B) / (‖A‖ · ‖B‖)");
        System.out.printf(Locale.US, "         = %s / (%.4f · %.4f)%n", formatG(skalar), normA, normB);
        System.out.printf(Locale.US, "         ≈ %.4f%n%n", ergebnis);
        return ergebnis;
    }

    public static String interpretiere(double ergebnis) {
        if (ergebnis > 0.9) {
            return "Die Vektoren sind sich sehr ähnlich (kleiner Winkel).";
        }
        if (ergebnis > 0.1) {
            return "Die Vektoren sind sich teilweise ähnlich.";
        }
        if (ergebnis >= -0.1) {
            return "Die Vektoren sind (nahezu) unabhängig voneinander (orthogonal).";
        }
        if (ergebnis >= -0.9) {
            return "Die Vektoren sind sich eher unähnlich (großer Winkel).";
        }
        return "Die Vektoren zeigen (nahezu) in entgegengesetzte Richtungen.";
    }

    // --- Mathematische Funktionen ---

    public static double skalarprodukt(double[] a, double[] b) {
        if (a.length != b.length) {
            throw new IllegalArgumentException("Vektoren müssen die gleiche Länge haben.");
        }
        double summe = 0.0;
        for (int i = 0; i < a.length; i++) {
            summe += a[i] * b[i];
        }
        return summe;
    }

    public static double betrag(double[] v) {
        double quadratsumme = 0.0;
        for (double x : v) {
            quadratsumme += x * x;
        }
        return Math.sqrt(quadratsumme);
    }

    public static double cosinusAehnlichkeit(double[] a, double[] b) {
        double normA = betrag(a);
        double normB = betrag(b);
        if (normA == 0 || normB == 0) {
            throw new IllegalArgumentException("Cosinus-Ähnlichkeit ist für den Nullvektor nicht definiert.");
        }
        return skalarprodukt(a, b) / (normA * normB);
    }

    public static double winkelInGrad(double[] a, double[] b) {
        double cosTheta = cosinusAehnlichkeit(a, b);
        cosTheta = Math.max(-1.0, Math.min(1.0, cosTheta));
        return Math.toDegrees(Math.acos(cosTheta));
    }

    // --- 2D-Raster Visualisierung ---

    public static List<String> erstelleRaster(double[] a, double[] b) {
        int radius = (int) Math.max(5, Math.ceil(Math.max(
            Math.max(Math.abs(a[0]), Math.abs(a[1])),
            Math.max(Math.abs(b[0]), Math.abs(b[1]))
        )));

        int size = radius * 2 + 1;
        char[][] grid = new char[size][size];

        for (int y = 0; y < size; y++) {
            for (int x = 0; x < size; x++) {
                if (y == radius && x == radius) {
                    grid[y][x] = '+';
                } else if (y == radius) {
                    grid[y][x] = '-';
                } else if (x == radius) {
                    grid[y][x] = '|';
                } else {
                    grid[y][x] = '.';
                }
            }
        }

        boolean[][] targetA = zeichneVektor(grid, radius, a[0], a[1]);
        boolean[][] targetB = zeichneVektor(grid, radius, b[0], b[1]);

        List<String> zeilen = new ArrayList<>();
        for (int y = 0; y < size; y++) {
            StringBuilder sb = new StringBuilder();
            for (int x = 0; x < size; x++) {
                if (targetA[y][x] && targetB[y][x]) {
                    sb.append(SYMBOL_UEBERLAPP);
                } else if (targetA[y][x]) {
                    sb.append(SYMBOL_A);
                } else if (targetB[y][x]) {
                    sb.append(SYMBOL_B);
                } else {
                    sb.append(grid[y][x]);
                }
            }
            zeilen.add(sb.toString());
        }
        return zeilen;
    }

    private static boolean[][] zeichneVektor(char[][] grid, int radius, double vx, double vy) {
        int size = radius * 2 + 1;
        boolean[][] marked = new boolean[size][size];
        int schritte = (int) Math.max(10, Math.ceil(Math.hypot(vx, vy) * 5));

        for (int i = 1; i <= schritte; i++) {
            double t = (double) i / schritte;
            int px = (int) Math.round(radius + t * vx);
            int py = (int) Math.round(radius - t * vy); // Y-Achse für Konsole invertieren

            if (px >= 0 && px < size && py >= 0 && py < size) {
                marked[py][px] = true;
            }
        }
        return marked;
    }

    /**
     * Hilfsmethode zur kompakten Zahlenformatierung analog zu Pythons `:g`.
     */
    private static String formatG(double val) {
        if (val == (long) val) {
            return String.format(Locale.US, "%d", (long) val);
        }
        return String.format(Locale.US, "%g", val).replaceAll("0+$", "").replaceAll("\\.$", "");
    }
}