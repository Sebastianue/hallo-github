// ================================================================
// Volvo XC60 Gen1 (2009-2017) - Wireless-Charger-Unterlage
// ================================================================
// Diese .scad ist die GUI-editierbare Variante. Die ausgelieferte
// STL wird mit generate_stl.py (CadQuery) erzeugt - beide nutzen
// dieselben Masse und dieselbe Konstruktion.
//
// ECHTE FAHRZEUG-MAẞE (gemessen 2026-06-15):
//   Becher-Innendurchmesser : 85 mm
//   Becher 1 (tief)         : 100 mm
//   Becher 2 (flach)        :  86 mm   <- 14 mm flacher!
//   Achsabstand Mitte-Mitte : 105 mm
//   Konsole innen (Breite)  :  99 mm
//   Charger-Pad aussen      :  74 mm
//   Charger-Pad Dicke       :   9 mm
//   Kabeldurchmesser        : 3,5 mm
//
// PRINZIP:
//   * Zwei UNTERSCHIEDLICH lange Zapfen gleichen die Tiefen aus
//     -> Ablageplatte liegt exakt waagerecht.
//   * Beide Zapfen stehen auf dem Becherboden auf (kein Absacken).
//   * Charger liegt buendig versenkt -> Rollo schliesst darueber.
//   * Charger ist Non-Slip-Silikon -> Handy rutscht nicht.
//
// DRUCK (Bambulab P1S):
//   Material    : PETG
//   Ausrichtung : Platte flach aufs Druckbett, Zapfen nach OBEN
//   Supports    : nur in der runden Charger-Mulde
//   Infill      : 20-25 % Gyroid, 3 Perimeter, 0,2 mm Layer
// ================================================================

/* [Becherhalter - GEMESSEN] */
cup_id          = 85;    // Innendurchmesser Becherhalter
cup_tiefe_deep  = 100;   // Tiefe Becher 1 (tiefer)
cup_tiefe_shall = 86;    // Tiefe Becher 2 (flacher)
cup_abstand     = 105;   // Achsabstand Mitte-Mitte
cup_spiel       = 1.0;   // Radiales Spiel der Zapfen

/* [Konsole - GEMESSEN] */
console_breite  = 99;    // Lichte Weite links-rechts

/* [Charger-Pad - GEMESSEN] */
charger_od      = 74;    // Aussendurchmesser
charger_h       = 9;     // Dicke
kabel_od        = 3.5;   // Kabeldurchmesser

/* [System] */
rollo_luft      = 2.0;   // Luft Pad-Oberkante -> Rollo (Annahme!)
pad_spiel       = 1.0;   // Spiel um das Pad in der Mulde
pad_boden       = 3.0;   // Bodenstaerke unter dem Pad
wand            = 4.0;   // Wandstaerke Hohl-Zapfen
ecken_r         = 5.0;   // Eckenabrundung Platte

// ---------------- Berechnet ----------------
zapfen_r    = cup_id / 2 - cup_spiel;        // 41.5
zapfen_ri   = zapfen_r - wand;               // 37.5
plate_breite= console_breite - 2;            // 97
plate_dick  = charger_h + pad_boden;         // 12
plate_l     = cup_abstand + cup_id;          // 190
pad_r       = charger_od / 2 + pad_spiel;    // 38

z_surface   = cup_tiefe_deep;                // 100 (Rollo-Ebene)
z_plate_top = z_surface - rollo_luft;        // 98
z_plate_bot = z_plate_top - plate_dick;      // 86
z_pocket_bot= z_plate_top - charger_h;       // 89

z_deep_bot  = 0;                             // tiefer Becher
z_shall_bot = cup_tiefe_deep - cup_tiefe_shall; // 14
len_deep    = z_plate_bot - z_deep_bot;      // 86
len_shall   = z_plate_bot - z_shall_bot;     // 72
y_deep      = -cup_abstand / 2;              // -52.5
y_shall     =  cup_abstand / 2;              // +52.5

$fn = 96;

// ---------------- Module ----------------
module hohl_zapfen(y, z0, length) {
    translate([0, y, z0])
        difference() {
            cylinder(h = length, r = zapfen_r);
            translate([0, 0, -0.01])
                cylinder(h = length - 3, r = zapfen_ri);
        }
}

module platte() {
    translate([0, 0, z_plate_bot])
        linear_extrude(plate_dick)
            offset(r = ecken_r) offset(r = -ecken_r)
                square([plate_breite, plate_l], center = true);
}

// ---------------- Zusammenbau ----------------
difference() {
    union() {
        hohl_zapfen(y_deep,  z_deep_bot,  len_deep);
        hohl_zapfen(y_shall, z_shall_bot, len_shall);
        // Versteifungssteg zwischen den Zapfen (X/Y mittig)
        translate([-8, -cup_abstand / 2, z_shall_bot])
            cube([16, cup_abstand, len_shall]);
        platte();
    }

    // Charger-Mulde
    translate([0, 0, z_pocket_bot])
        cylinder(h = charger_h + 1, r = pad_r);

    // Kabelkanal senkrecht
    translate([0, 0, z_plate_bot - 1])
        cylinder(h = charger_h + 2, r = kabel_od / 2 + 1);

    // Kabelaustritt seitlich (+X)
    translate([0, -(kabel_od + 1.5) / 2, z_plate_bot])
        cube([plate_breite, kabel_od + 1.5, kabel_od + 1.5]);
}

// ================================================================
// VORSCHAU (transparent, nicht im Export)
// ================================================================
%color("dimgray", 0.6)
    translate([0, 0, z_plate_top - charger_h / 2])
        cylinder(h = charger_h, r = charger_od / 2, center = true);

%color("silver", 0.35)
    translate([0, 0, z_plate_top + 8.25 / 2])
        cube([74, 150, 8.25], center = true);

%color("red", 0.10)
    translate([0, 0, z_surface + 0.5])
        cube([plate_breite + 30, plate_l + 30, 1], center = true);
