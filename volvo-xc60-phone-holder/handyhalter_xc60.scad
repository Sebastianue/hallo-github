// ================================================================
// Volvo XC60 (Bj. 2009–2017, Gen1) – Handyhalter mit Wireless Charger
// ================================================================
// Einbauort : Mittelkonsole, Becherhalterbereich unter dem Rollo
// Handy     : iPhone 15 Pro (146,6 × 70,6 × 8,25 mm)
// Charger   : 15W Wireless Flat-Pad A02767-134 / Modell A2E
// Drucker   : Bambulab P1S – Material: PETG (hitzebeständiger als PLA)
// Druck     : Platte = Unterseite Ablage (Zapfen zeigen nach oben)
//             → kein Support nötig, Oberfläche wird glatt
// ================================================================
//
// !! WICHTIG – VOR DEM ERSTEN DRUCK NACHMESSEN !!
// Alle mit "MESSEN!" markierten Parameter mit einem Messschieber
// am echten Fahrzeug prüfen und bei Bedarf anpassen.
//
// Schritt 1: Rollo öffnen, Becherhalter freilegen
// Schritt 2: Innendurchmesser eines Becherhalters messen (cup_id)
// Schritt 3: Achsabstand der zwei Becher messen (cup_abstand)
// Schritt 4: Tiefe der Becherhalter messen (cup_tiefe)
// Schritt 5: Charger-Pad-Durchmesser und -Dicke messen (charger_*)
// ================================================================

/* [BECHERHALTER – Volvo XC60 Gen1 geschätzte Werte] */
cup_id         = 76;    // MESSEN! Innendurchmesser Becherhalter [mm]
cup_tiefe      = 72;    // MESSEN! Tiefe der Becherhalter-Vertiefung [mm]
cup_abstand    = 100;   // MESSEN! Achsabstand Mitte-zu-Mitte der zwei Becher [mm]
zapfen_spiel   = 0.8;   // Spiel am Radius für sicheren Sitz (0.5 = fest, 1.2 = locker)
zapfen_hoehe   = 55;    // Wie tief der Zapfen in den Becher geht [mm]

/* [WIRELESS CHARGER PAD – 15W Flat Silikon Pad A2E] */
charger_od     = 85;    // MESSEN! Außendurchmesser Charger-Pad [mm]
charger_dicke  = 6;     // MESSEN! Dicke des Charger-Pads [mm]
charger_versenkung = 2; // Charger liegt xx mm vertieft in der Wanne [mm]
kabel_od       = 5;     // Außendurchmesser des Charger-Kabels [mm]

/* [ABLAGE-PLATTE] */
platte_dicke   = 5;     // Stärke der Ablageplatte [mm]
rand_hoehe     = 6;     // Höhe des umlaufenden Seitenrands [mm]
rand_breite    = 3;     // Breite des Rands (oben gemessen) [mm]
ecken_r        = 5;     // Abrundungsradius der Platte-Ecken [mm]

/* [IPHONE 15 PRO – nur für Referenz / Sichtprüfung] */
iphone_laenge  = 146.6; // iPhone 15 Pro Länge
iphone_breite  = 70.6;  // iPhone 15 Pro Breite
iphone_dicke   = 8.25;  // iPhone 15 Pro Dicke (ohne Hülle)

// ================================================================
// Berechnete Werte (nicht ändern)
// ================================================================
zapfen_ar      = cup_id / 2 - zapfen_spiel;   // Außenradius Zapfen oben
zapfen_ir      = zapfen_ar - 3.5;             // Innenradius Zapfen (Wandstärke 3,5 mm)

// Platte groß genug für Charger-Pad + Rand, aber nicht breiter als Konsole
platte_breite  = max(cup_abstand + cup_id * 0.85, charger_od + rand_breite * 2 + 4);
platte_laenge  = max(charger_od + rand_breite * 2 + 4, 155);

$fn = 72;

// ================================================================
// MODULE
// ================================================================

// Abgerundete Box (konvexes Dreieck-Hull-Verfahren für gerade Kanten)
module box_rund(breite, laenge, hoehe, r) {
    hull() {
        for (x = [-(breite/2 - r), (breite/2 - r)])
            for (y = [-(laenge/2 - r), (laenge/2 - r)])
                translate([x, y, 0])
                    cylinder(r = r, h = hoehe);
    }
}

// Einzelner Hohlzapfen (geht in den Becherhalter)
module zapfen() {
    difference() {
        // Außenkontur – leicht konisch für einfaches Einführen
        cylinder(
            h  = zapfen_hoehe,
            r1 = zapfen_ar - 1.5,   // Unterseite etwas kleiner (Einführhilfe)
            r2 = zapfen_ar
        );
        // Innenhohlraum (spart Material, Kabelkanal)
        translate([0, 0, -0.1])
            cylinder(
                h  = zapfen_hoehe + 0.2,
                r1 = zapfen_ir - 1.5,
                r2 = zapfen_ir
            );
        // Kabelkanal im linken Zapfen (seitlicher Schlitz unten)
        translate([0, -kabel_od / 2, -0.1])
            cube([zapfen_ar + 1, kabel_od, kabel_od * 1.5]);
    }
}

// Versteifungssteg zwischen den zwei Zapfen
module steg() {
    hoehe_steg = 12;
    translate([0, 0, zapfen_hoehe - hoehe_steg])
        hull() {
            translate([-cup_abstand/2, 0, 0])
                cylinder(h = hoehe_steg, r = zapfen_ar);
            translate([ cup_abstand/2, 0, 0])
                cylinder(h = hoehe_steg, r = zapfen_ar);
        }
}

// Ablageplatte mit Charger-Wanne und Rand
module ablageplatte() {
    difference() {
        union() {
            // Basis-Platte
            box_rund(platte_breite, platte_laenge, platte_dicke, ecken_r);

            // Umlaufender Rand
            difference() {
                box_rund(
                    platte_breite,
                    platte_laenge,
                    platte_dicke + rand_hoehe,
                    ecken_r
                );
                // Inneres der Rand-Box herausschneiden
                translate([0, 0, platte_dicke])
                    box_rund(
                        platte_breite  - rand_breite * 2,
                        platte_laenge  - rand_breite * 2,
                        rand_hoehe + 0.1,
                        max(1, ecken_r - rand_breite)
                    );
            }
        }

        // Charger-Pad-Vertiefung (kreisförmige Wanne)
        translate([0, 0, platte_dicke - charger_versenkung])
            cylinder(h = charger_versenkung + 0.1, r = charger_od / 2);

        // Kabelauslass-Schlitz an der hinteren Schmalseite
        translate([0, platte_laenge / 2 - rand_breite / 2, platte_dicke / 2 - kabel_od / 2])
            cube([kabel_od * 1.5, rand_breite + 1, kabel_od], center = true);

        // Kabelkanal durch Platteninneres nach unten zum linken Zapfen
        translate([-cup_abstand / 2, 0, -0.1])
            cylinder(h = platte_dicke + 0.2, r = kabel_od / 2 + 0.5);
    }
}

// ================================================================
// ZUSAMMENBAU
// ================================================================
translate([0, 0, 0]) {
    // Linker Zapfen
    translate([-cup_abstand / 2, 0, 0])
        zapfen();

    // Rechter Zapfen
    translate([ cup_abstand / 2, 0, 0])
        zapfen();

    // Verbindungssteg
    steg();

    // Ablageplatte (sitzt auf Zapfen-Oberkante)
    translate([0, 0, zapfen_hoehe])
        ablageplatte();
}

// ================================================================
// VORSCHAU: iPhone 15 Pro (transparent, nur zur Kontrolle)
// Auskommentieren für den echten Druck-Export
// ================================================================
%translate([0, 0, zapfen_hoehe + platte_dicke + charger_dicke - charger_versenkung])
    color("silver", 0.4)
        cube([iphone_breite, iphone_laenge, iphone_dicke], center = true);

// Charger-Pad Vorschau
%translate([0, 0, zapfen_hoehe + platte_dicke - charger_versenkung + charger_dicke / 2])
    color("black", 0.5)
        cylinder(h = charger_dicke, r = charger_od / 2, center = true);
