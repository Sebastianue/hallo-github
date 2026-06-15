// ================================================================
// Volvo XC60 Gen1 (2009–2017) – Wireless-Charger-Unterlage
// Mittelkonsole, Becherhalterbereich unter dem Rollo
// ================================================================
//
// FUNKTION:
//   • Zwei Zapfen greifen in die hintereinander liegenden Becherhalter
//   • Solide Brücke zwischen den Zapfen füllt die volle Konsolenbreite
//   • Charger-Pad liegt bündig versenkt → Rollo schließt über dem Pad
//   • iPhone 15 Pro liegt in einer Handymulde → kein Verrutschen
//   • Kabelkanal durch vorderen Zapfen, Austritt seitlich
//
// HÖHEN-SCHEMA (Seitenansicht):
//
//   Konsolen-Oberkante (=Rollo-Ebene):  72 mm ─────────────────
//   Rollo-Luft:                          2 mm
//   Einsatz-Oberkante / Pad-Oberkante:  70 mm ═══════════════
//   Handy-Mulde (3 mm tief):                    ┌───────────┐
//   Charger-Pad (6 mm tief im Körper):  64 mm   │ Charger  │ 61–67 mm
//                                               └───────────┘
//   Einsatz-Unterkante (Boden Becher):   0 mm ─────────────────
//
// DRUCKANLEITUNG (Bambulab P1S):
//   Material    : PETG (hitzebeständig ≤ 80 °C, ideal Autoinnenraum)
//   Ausrichtung : Handy-Mulde liegt UNTEN auf dem Druckbett → Zapfen
//                 zeigen nach OBEN. Kein Support nötig. Glatte Sichtfläche.
//   Layer       : 0,2 mm
//   Infill      : 25 % Gyroid
//   Wandstärke  : 3–4 Perimeter
//
// !! VOR DEM DRUCK: ALLE MIT "MESSEN!" MARKIERTEN WERTE AM AUTO PRÜFEN !!
// Schritt 1: Rollo öffnen
// Schritt 2: Innendurchmesser eines Becherhalters → cup_id
// Schritt 3: Achsabstand der Becherhalter-Mittelpunkte → cup_abstand
//            (Becher liegen HINTEREINANDER, also vorne–hinten messen!)
// Schritt 4: Tiefe der Becherhalter (Rand bis Boden) → cup_tiefe
// Schritt 5: Breite der Konsolen-Öffnung (links–rechts) → platte_breite
// Schritt 6: Charger-Pad: Außendurchmesser und Dicke
// ================================================================

// ───────────────────────────────────────────────────────────────
//  PARAMETER – HIER ANPASSEN
// ───────────────────────────────────────────────────────────────

/* [BECHERHALTER – MESSEN!] */
cup_id       = 76;   // MESSEN! Innendurchmesser Becherhalter [mm]
cup_tiefe    = 72;   // MESSEN! Tiefe Becherhalter (Konsolenrand → Boden) [mm]
cup_abstand  = 90;   // MESSEN! Achsabstand Mitte–Mitte (vorne–hinten) [mm]
cup_spiel    = 1.0;  // Spiel am Radius: 0.5 = eng, 1.0 = leicht einzusetzen

/* [KONSOLENBREITE – MESSEN!] */
platte_breite = 113; // MESSEN! Lichte Weite der Konsole links–rechts [mm]
                     // (etwas kürzer als Rollo-Breite ≈ 117 mm)

/* [WIRELESS CHARGER PAD – MESSEN!] */
charger_od   = 85;   // MESSEN! Außendurchmesser Charger-Pad [mm]
charger_h    =  6;   // MESSEN! Dicke des Charger-Pads [mm]
kabel_od     =  5;   // MESSEN! Kabeldurchmesser [mm]

/* [HANDY-MULDE – bei Hülle anpassen] */
phone_l      = 150;  // Länge Handy inkl. Hülle [mm]  (iPhone 15 Pro nackt: 146,6)
phone_b      =  74;  // Breite Handy inkl. Hülle [mm]  (iPhone 15 Pro nackt:  70,6)
phone_mulde_t =  3;  // Tiefe der Handy-Mulde [mm]

/* [SYSTEM] */
rollo_luft   = 2.0;  // Luft zwischen Charger-Pad-Oberkante und Rollo [mm]
ecken_r      = 5;    // Eckenabrundung der Grundplatte [mm]

// ───────────────────────────────────────────────────────────────
//  BERECHNETE WERTE
// ───────────────────────────────────────────────────────────────
zapfen_r  = cup_id / 2 - cup_spiel;  // Zapfenradius (passt in Becher)
platte_l  = cup_abstand + cup_id;    // Plattenlänge (überspannt beide Becher)

// Gesamthöhe des Einsatzes:
// Oberkante = Konsolenrand minus Luft fürs Rollo → Charger liegt bündig darunter
einsatz_h = cup_tiefe - rollo_luft;  // = 70 mm bei Standardwerten

// Tiefe der Charger-Vertiefung (von oben gemessen):
// Charger sitzt komplett versenkt; Oberkante bündig mit Einsatz-Oberkante
charger_tiefe = charger_h;  // = 6 mm → Pad-Oberkante = Einsatz-Oberkante ✓

// Tiefe der Handy-Mulde (beginnt ab Einsatz-Oberkante, ÜBER dem Charger):
// Handy-Mulde überlagert die Charger-Vertiefung:
// Mulde geht 3 mm tief → Boden liegt 3 mm unterhalb der Oberkante
// Charger geht 6 mm tief → Boden liegt 6 mm unterhalb der Oberkante
// Handy liegt im Mulde-Boden (3 mm Tiefe) direkt über Charger ✓

echo(str("=== Volvo XC60 Charger-Einsatz ==="));
echo(str("Zapfenradius: ", zapfen_r, " mm | Platte: ", platte_breite, " x ", platte_l, " mm"));
echo(str("Einsatz-Gesamthöhe: ", einsatz_h, " mm | Ziel-Tiefe Becher: ", cup_tiefe, " mm"));
echo(str("Rollo-Luft über Charger-Pad: ", cup_tiefe - einsatz_h, " mm"));

// ───────────────────────────────────────────────────────────────
//  HILFSFUNKTION: Abgerundete Box
// ───────────────────────────────────────────────────────────────
$fn = 80;

module box_r(b, l, h, r) {
    hull()
        for (x = [r - b/2, b/2 - r], y = [r - l/2, l/2 - r])
            translate([x, y, 0])
                cylinder(r = r, h = h);
}

// ───────────────────────────────────────────────────────────────
//  HAUPTMODELL
// ───────────────────────────────────────────────────────────────
module einsatz() {
    difference() {

        // ═══════════════════════════════════════════════════════
        // POSITIVFORM: Solider Körper
        // ═══════════════════════════════════════════════════════
        union() {
            // Zapfen vorne (sitzt im vorderen Becherhalter)
            translate([0, -cup_abstand / 2, 0])
                cylinder(
                    h  = einsatz_h,
                    r  = zapfen_r,
                    r1 = zapfen_r - 1.5   // leicht konisch → leichter einzuführen
                );

            // Zapfen hinten (sitzt im hinteren Becherhalter)
            translate([0, cup_abstand / 2, 0])
                cylinder(
                    h  = einsatz_h,
                    r  = zapfen_r,
                    r1 = zapfen_r - 1.5
                );

            // Volle Brücke zwischen den Zapfen (solid, Konsolenbreite)
            hull() {
                translate([0, -cup_abstand / 2, 0])
                    cylinder(h = einsatz_h, r = zapfen_r);
                translate([0,  cup_abstand / 2, 0])
                    cylinder(h = einsatz_h, r = zapfen_r);
            }

            // Obere Ablageplatte (füllt volle Konsolenbreite)
            hull() {
                translate([0, -cup_abstand / 2, 0])
                    cylinder(h = einsatz_h, r = platte_breite / 2 - ecken_r);
                translate([0,  cup_abstand / 2, 0])
                    cylinder(h = einsatz_h, r = platte_breite / 2 - ecken_r);
                // Eckabrundungen der Platte
                for (y = [-platte_l/2 + ecken_r, platte_l/2 - ecken_r],
                     x = [-platte_breite/2 + ecken_r, platte_breite/2 - ecken_r])
                    translate([x, y, 0])
                        cylinder(h = einsatz_h, r = ecken_r);
            }
        }

        // ═══════════════════════════════════════════════════════
        // AUSSPARUNGEN (von oben in den Körper gefräst)
        // ═══════════════════════════════════════════════════════

        // --- Charger-Pad-Vertiefung (rund, von oben) ─────────────────────
        // Pad liegt vollständig versenkt; Oberkante bündig mit Einsatz-Oberkante
        translate([0, 0, einsatz_h - charger_tiefe])
            cylinder(h = charger_tiefe + 0.1, r = charger_od / 2);

        // --- Handy-Mulde (rechteckig, 3 mm tief, liegt über Charger) ─────
        // Handy liegt in dieser Mulde – Seitenwände verhindern Verrutschen
        // Mulde ist flacher als Charger → Handy berührt Charger-Oberfläche
        translate([0, 0, einsatz_h - phone_mulde_t])
            box_r(phone_b, phone_l, phone_mulde_t + 0.1, 3);

        // --- Kabelkanal: vertikal durch vorderen Zapfen ──────────────────
        // Charger-Kabel läuft senkrecht vom Pad nach unten durch den Zapfen
        translate([0, -cup_abstand / 2, -0.1])
            cylinder(h = einsatz_h + 0.2, r = kabel_od / 2 + 1.0);

        // --- Kabelaustritt: horizontaler Schlitz seitlich am Einsatz ─────
        // Kabel biegt im Zapfen um und tritt links seitlich aus
        translate([
            -(platte_breite / 2 + 0.1),
            -cup_abstand / 2,
            kabel_od / 2 + 2          // Kabel-Mitte: 2 mm über Becherboden
        ])
            rotate([0, 90, 0])
                cylinder(
                    h = platte_breite / 2 - zapfen_r + 5,
                    r = kabel_od / 2 + 1.0
                );
    }
}

// ───────────────────────────────────────────────────────────────
//  RENDER
// ───────────────────────────────────────────────────────────────
einsatz();

// ═══════════════════════════════════════════════════════════════
//  VORSCHAU-OBJEKTE  (% = transparent, NICHT im STL-Export)
//  In OpenSCAD sichtbar zur Kontrolle; für STL-Export stehen lassen.
// ═══════════════════════════════════════════════════════════════

// Charger-Pad (dunkelgrau)
%color("dimgray", 0.65)
    translate([0, 0, einsatz_h - charger_h / 2])
        cylinder(h = charger_h, r = charger_od / 2, center = true);

// iPhone 15 Pro (silber)
%color("silver", 0.4)
    translate([0, 0, einsatz_h - phone_mulde_t + 8.25 / 2])
        cube([phone_b, phone_l, 8.25], center = true);

// Rollo-Unterseite (rot = Unterseite des geschlossenen Rollos; Luft sichtbar)
%color("red", 0.12)
    translate([0, 0, cup_tiefe + 0.5])
        cube([platte_breite + 30, platte_l + 30, 1], center = true);
