"""
Volvo XC60 Gen1 - Wireless Charger Unterlage
Echte Masse (gemessen):
  Becher-Innendurchmesser : 77 mm
  Becher vorne Tiefe      : 72 mm (wird verwendet)
  Becher hinten Tiefe     : 64 mm (wird weggelassen)
  Achsabstand Mitte-Mitte : 105 mm
  Konsole innen Breite    : 97 mm
  Charger-Pad Durchmesser : 74 mm
  Charger-Pad Dicke       : 9 mm
  Kabeldurchmesser        : 9 mm
  Platten-Dicke           : 21 mm
  Charger-Aussparung      : 74 mm Durchmesser, 9 mm tief, mittig oben

Konstruktion:
  - EIN Zapfen geht in den vorderen Becherhalter (haelt die Platte)
  - Breite Platte liegt auf dem Konsolenrand auf (seitlich gestuetzt)
  - Charger-Pad-Aussparung (rund, 74 mm, 9 mm tief) mittig auf der Platte
  - Kabel tritt an der Vorderkante unten aus (Schlitz 11 x 11 mm)
  - Rollo schliesst mit 2 mm Luft ueber der Platte

Hoehen-Schema (z=0 am vorderen Becherboden):
  z = 72  Konsolenrand (Rollo-Ebene)
  z = 70  Plattenoberseite = Charger-Pad-Oberseite
  z = 61  Boden der Charger-Aussparung
  z = 49  Plattenunterseite (Zapfen-Oberkante)
  z =  0  Boden vorderer Becherhalter

Druck (Bambulab P1S):
  Material   : PETG
  Ausrichtung: Plattenoberflaeche (mit Aussparung) NACH UNTEN aufs Druckbett
               -> Zapfen zeigt nach OBEN, kein Support noetig ausser Charger-Mulde
  Infill     : 25 % Gyroid
  Wandstaerke: 3 Perimeter, Layer 0.2 mm
"""

import cadquery as cq
import os

# ==================================================================
# PARAMETER
# ==================================================================
cup_id          = 77.0   # Innendurchmesser Becherhalter vorne
cup_tiefe       = 72.0   # Tiefe Becherhalter vorne (ab Konsolenrand)
cup_abstand     = 105.0  # Achsabstand Mitte-Mitte
console_breite  = 97.0   # Konsole innen (links-rechts)
charger_h       = 9.0    # Charger-Pad Dicke = Aussparungstiefe
pad_w           = 78.0   # Breite Pad-Aussparung (gemessen)
pad_l           = 164.0  # Laenge Pad-Aussparung (gemessen)
charger_od      = pad_w  # fuer Abwaertskompatibilitaet
kabel_od        = 9.0    # Kabeldurchmesser
plate_thick     = 21.0   # Plattendicke
rollo_luft      = 2.0    # Luft Plattenoberseite -> Rollo
cup_spiel       = 1.0    # Radiales Spiel Zapfen in Becher
zapfen_wand     = 4.0    # Wandstaerke Hohlzapfen

# ==================================================================
# BERECHNETE WERTE
# ==================================================================
zapfen_r   = cup_id / 2.0 - cup_spiel        # 37.5 mm Zapfen-Aussenradius
zapfen_ri  = zapfen_r - zapfen_wand           # 33.5 mm Zapfen-Innenradius (hohl)
plate_w    = console_breite - 2.0             # 95 mm  (1 mm Spiel je Seite)
plate_l    = cup_abstand + cup_id             # 182 mm (von Becherfront bis Hinterkante)
charger_r  = charger_od / 2.0 + 1.0          # 38 mm  (1 mm Spiel)
kabel_r    = kabel_od / 2.0 + 1.0            # 5.5 mm Kanalradius

# Z-Koordinaten (z=0 = Boden vorderer Becherhalter, z=72 = Konsolenrand)
z_rim      = cup_tiefe                        # 72
z_top      = z_rim - rollo_luft              # 70  <- Plattenoberseite
z_bot      = z_top - plate_thick             # 49  <- Plattenunterseite
zapfen_h   = z_bot                            # 49  <- Zapfenhoehe
z_pocket   = z_top - charger_h               # 61  <- Aussparungsboden

# Y-Positionen (vorderer Becher bei y_front, Platte zentriert bei y=0)
y_front    = -(cup_abstand / 2.0)            # -52.5 mm

print("=== Volvo XC60 Charger-Unterlage (1 Zapfen) ===")
print(f"Zapfen-Aussenradius  : {zapfen_r:.1f} mm")
print(f"Zapfenhoehe          : {zapfen_h:.0f} mm  (in {cup_tiefe:.0f} mm tiefen Becher)")
print(f"Plattengroesse       : {plate_w:.0f} x {plate_l:.0f} x {plate_thick:.0f} mm")
print(f"Charger-Aussparung   : {pad_w:.0f} x {pad_l:.0f} mm, {charger_h:.0f} mm tief, mittig")
print(f"Plattenoberseite z   : {z_top:.0f} mm  (Konsolenrand {z_rim:.0f} mm)")
print(f"Rollo-Luft           : {z_rim - z_top:.0f} mm")
print(f"Material unter Pad   : {plate_thick - charger_h:.0f} mm  (Plattendicke - Padtiefe)")
print("Aufbau laeuft ...")

# ==================================================================
# GEOMETRIE AUFBAUEN
# ==================================================================

# --- 1. Hohlzapfen (vorderer Becherhalter) -----------------------
# Leicht konisch (unten 1.5 mm schmaler) -> leichter einzufuehren
zapfen_solid = (
    cq.Workplane("XY")
    .add(cq.Solid.makeCylinder(
        radius=zapfen_r, height=zapfen_h,
        angleDegrees=360
    ))
    .translate((0, y_front, 0))
)

# Alternativer Weg ohne Konus (stabiler fuer Boolean-Ops):
zapfen_solid = (
    cq.Workplane("XY")
    .circle(zapfen_r).extrude(zapfen_h)
    .translate((0, y_front, 0))
)

zapfen_hole = (
    cq.Workplane("XY")
    .circle(zapfen_ri).extrude(zapfen_h - 3)
    .translate((0, y_front, 0))
)

zapfen = zapfen_solid.cut(zapfen_hole)

# --- 2. Platte (zentriert in X und Y, auf Zapfen aufgesetzt) -----
# Erstelle Rechteck, extrude, dann Ecken abrunden
plate = (
    cq.Workplane("XY")
    .rect(plate_w, plate_l)
    .extrude(plate_thick)
    .translate((0, 0, z_bot))
    .edges("|Z")
    .fillet(5.0)
)

# Koerper zusammenfuegen
body = zapfen.union(plate)

# ==================================================================
# AUSSPARUNGEN
# ==================================================================

# --- 3. Charger-Pad-Aussparung (78x164mm rechteckig, 9mm tief, mittig oben) ---
pad_corner = 3.0           # Eckenradius
charger_pocket = (
    cq.Workplane("XY")
    .workplane(offset=z_pocket - 0.1)
    .rect(pad_w, pad_l)
    .extrude(charger_h + 0.2)
    .edges("|Z")
    .fillet(pad_corner)
)

# --- 4. Kabelschlitz an der Vorderkante unten -------------------
# Kabel (9mm) tritt an der Vorderkante der Platte aus und laeuft
# nach unten neben dem Zapfen zur USB-Quelle
# Schlitz: 11 mm breit (kabel+2), 11 mm hoch, geht von Plattenvorderkante
#          bis zur Charger-Aussparung durch
kabel_schlitz_w = kabel_od + 2.0          # 11 mm
kabel_schlitz_h = kabel_od + 2.0          # 11 mm
schlitz_tiefe   = (plate_w - pad_w) / 2.0 + 2.0  # von Plattenkante bis Pad-Rand

kabel_schlitz = (
    cq.Workplane("XY")
    .box(kabel_schlitz_w, schlitz_tiefe + 1.0, kabel_schlitz_h,
         centered=(True, False, False))
    .translate((0, -(plate_l / 2.0), z_bot))
)

# --- 5. Kabel-Fuehrungskanal durch den Zapfen (vertikal) ---------
# Der Schlitz verbindet sich mit dem Zapfenhohlraum;
# ein Kanal im Boden des Schlitzes fuehrt nach unten
kabel_kanal = (
    cq.Workplane("XY")
    .workplane(offset=-0.5)
    .center(0, y_front)
    .circle(kabel_r)
    .extrude(z_bot + 0.5)   # von Becherboden bis Plattenunterseite
)

# ==================================================================
# ENDFORM
# ==================================================================
result = (
    body
    .cut(charger_pocket)
    .cut(kabel_schlitz)
    .cut(kabel_kanal)
)

# ==================================================================
# EXPORT
# ==================================================================
out_path = os.path.expanduser("~/Downloads/handyhalter_xc60.stl")
cq.exporters.export(result, out_path, tolerance=0.05, angularTolerance=0.1)

size_kb = os.path.getsize(out_path) // 1024
print(f"\n  STL gespeichert: {out_path}  ({size_kb} kB)")
print("\n  Druckhinweise:")
print("  - Plattenoberflaeche (Charger-Aussparung) auf das Druckbett legen")
print("  - Zapfen zeigt nach oben beim Drucken")
print("  - Support nur fuer runde Charger-Aussparung (ist oben, also kein Support!)")
print("  - Tatsaechlich: kein Support noetig wenn Platte unten liegt")
print("  - PETG, 0.2 mm Layer, 25% Gyroid, 3 Perimeter")
