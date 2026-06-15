"""
Volvo XC60 Gen1 (2009-2017) - Wireless Charger Unterlage
Erzeugt handyhalter_xc60.stl via CadQuery

ECHTE FAHRZEUG-MAẞE (gemessen 2026-06-15):
  - Becherhalter Innendurchmesser : 85 mm
  - Becher 1 (tief)               : 100 mm
  - Becher 2 (flach)              :  86 mm   <- 14 mm flacher!
  - Achsabstand Mitte-Mitte       : 105 mm
  - Konsole innen (Breite)        :  99 mm
  - Charger-Pad aussen            :  74 mm
  - Charger-Pad Dicke             :   9 mm
  - Kabeldurchmesser              : 3,5 mm

KONSTRUKTIONSPRINZIP:
  * Zwei UNTERSCHIEDLICH lange Zapfen gleichen die zwei Tiefen aus,
    damit die Ablageplatte exakt WAAGERECHT liegt.
  * Beide Zapfen stehen auf dem jeweiligen Becherboden auf
    -> definierte Hoehe, kein Absacken.
  * Charger-Pad liegt buendig versenkt in runder Mulde
    -> Rollo schliesst ueber Pad + Unterlage.
  * Charger ist ein Non-Slip-Silikonpad -> Handy rutscht nicht,
    daher keine separate Handymulde noetig.
  * Kabelkanal: vom Pad senkrecht nach unten, seitlicher Austritt
    tief unten (unterhalb der Rollo-Ebene).
"""

import cadquery as cq
import os

# ==================================================================
# PARAMETER (alle in mm) - HIER ANPASSEN
# ==================================================================

# --- Becherhalter (GEMESSEN) ---
cup_id          = 85.0    # Innendurchmesser Becherhalter
cup_tiefe_deep  = 100.0   # Tiefe Becher 1 (der tiefere)
cup_tiefe_shall =  86.0   # Tiefe Becher 2 (der flachere)
cup_abstand     = 105.0   # Achsabstand Mitte-Mitte (vorne-hinten)
cup_spiel       =   1.0   # Radiales Spiel der Zapfen (1.0 = leicht einzufuehren)

# --- Konsole (GEMESSEN) ---
console_breite  =  99.0   # Lichte Weite der Konsole links-rechts

# --- Wireless Charger Pad (GEMESSEN) ---
charger_od      =  74.0   # Aussendurchmesser Charger-Pad
charger_h       =   9.0   # Dicke des Charger-Pads
kabel_od        =   3.5   # Kabeldurchmesser

# --- System / Toleranzen ---
rollo_luft      =   2.0   # Luft Charger-Oberkante -> Rollo (Annahme!)
pad_spiel       =   1.0   # Spiel um das Charger-Pad in der Mulde
pad_boden       =   3.0   # Bodenstaerke unter dem Charger-Pad
wand            =   4.0   # Wandstaerke der Hohl-Zapfen
plate_breite    = console_breite - 2.0   # Plattenbreite (2 mm Fitspiel) = 97
ecken_r         =   5.0   # Eckenabrundung der Platte

# ==================================================================
# BERECHNETE GROESSEN
# ==================================================================
zapfen_r   = cup_id / 2.0 - cup_spiel          # 41.5 mm
zapfen_ri  = zapfen_r - wand                    # 37.5 mm (Hohlraum)
plate_dick = charger_h + pad_boden              # 12 mm Plattendicke
plate_l    = cup_abstand + cup_id               # 190 mm (ueberspannt beide Becher)
pad_r      = charger_od / 2.0 + pad_spiel       # 38 mm Mulden-Radius

# Z-Aufbau: z = 0 am Boden des TIEFEN Bechers, nach oben positiv
# Konsolenoberflaeche (Rollo-Ebene) liegt bei z = cup_tiefe_deep = 100
z_surface   = cup_tiefe_deep                    # 100 (Rollo-Ebene)
z_plate_top = z_surface - rollo_luft            # 98 (Plattenoberkante)
z_plate_bot = z_plate_top - plate_dick          # 86 (Plattenunterkante)
z_pocket_bot= z_plate_top - charger_h           # 89 (Mulden-Boden)

# Becherboeden relativ zu z=0
z_deep_bot  = 0.0                                # tiefer Becher: Boden bei 0
z_shall_bot = cup_tiefe_deep - cup_tiefe_shall   # flacher Becher: Boden bei 14

# Zapfenlaengen (vom Becherboden bis Plattenunterkante)
len_deep    = z_plate_bot - z_deep_bot           # 86 mm
len_shall   = z_plate_bot - z_shall_bot          # 72 mm

# Zapfenpositionen (tiefer Becher hinten, flacher vorne - frei waehlbar)
y_deep      = -cup_abstand / 2.0                 # -52.5
y_shall     = +cup_abstand / 2.0                 # +52.5

print("=== Volvo XC60 Charger-Unterlage ===")
print(f"Zapfen-Aussenradius : {zapfen_r:.1f} mm  (Becher-ID {cup_id} mm)")
print(f"Zapfen tief / flach : {len_deep:.0f} / {len_shall:.0f} mm")
print(f"Plattenmasse        : {plate_breite:.0f} x {plate_l:.0f} x {plate_dick:.0f} mm")
print(f"Charger-Mulde       : Radius {pad_r:.0f} mm, Tiefe {charger_h:.0f} mm")
print(f"Plattenoberkante    : {z_plate_top:.0f} mm  (Rollo-Ebene {z_surface:.0f} mm)")
print(f"Rollo-Luft ueber Pad: {z_surface - z_plate_top:.0f} mm")
print(f"Gesamthoehe         : {z_plate_top:.0f} mm")
print("Baue Modell ...")

# ==================================================================
# GEOMETRIE
# ==================================================================

def hohl_zapfen(y, z0, length):
    """Hohler Zapfen, Boden bei z0, Laenge length, oben 3 mm Kappe."""
    outer = (cq.Workplane("XY").circle(zapfen_r)
             .extrude(length).translate((0, y, z0)))
    inner = (cq.Workplane("XY").circle(zapfen_ri)
             .extrude(length - 3.0).translate((0, y, z0)))
    return outer.cut(inner)

# 1. Zwei Zapfen
deep_peg  = hohl_zapfen(y_deep,  z_deep_bot,  len_deep)
shall_peg = hohl_zapfen(y_shall, z_shall_bot, len_shall)

# 2. Versteifungssteg zwischen den Zapfen (verbindet beide Saeulen)
web = (cq.Workplane("XY")
       .box(16.0, cup_abstand, len_shall, centered=(True, True, False))
       .translate((0, 0, z_shall_bot)))

# 3. Ablageplatte (volle Konsolenbreite, abgerundete Ecken)
plate = (cq.Workplane("XY")
         .box(plate_breite, plate_l, plate_dick, centered=(True, True, False))
         .translate((0, 0, z_plate_bot))
         .edges("|Z").fillet(ecken_r))

body = deep_peg.union(shall_peg).union(web).union(plate)

# ==================================================================
# AUSSPARUNGEN
# ==================================================================

# 4. Charger-Pad-Mulde (rund, buendig mit Oberkante)
pocket = (cq.Workplane("XY").circle(pad_r)
          .extrude(charger_h + 1.0).translate((0, 0, z_pocket_bot)))

# 5. Kabelkanal senkrecht: Mulden-Boden -> Plattenunterseite
cable_vert = (cq.Workplane("XY").circle(kabel_od / 2.0 + 1.0)
              .extrude(charger_h + 2.0).translate((0, 0, z_plate_bot - 1.0)))

# 6. Kabelaustritt seitlich (Kanal von Mitte zur +X-Kante, tief unten)
cable_side = (cq.Workplane("XY")
              .box(plate_breite, kabel_od + 1.5, kabel_od + 1.5,
                   centered=(False, True, True))
              .translate((0, 0, z_plate_bot + (kabel_od + 1.5) / 2.0)))

result = body.cut(pocket).cut(cable_vert).cut(cable_side)

# ==================================================================
# EXPORT
# ==================================================================
out_path = os.path.expanduser("~/Downloads/handyhalter_xc60.stl")
cq.exporters.export(result, out_path, tolerance=0.05, angularTolerance=0.1)
print(f"\nOK - STL gespeichert: {out_path}")
print(f"     Groesse: {os.path.getsize(out_path) / 1024:.0f} kB")
print("\nDRUCK (Bambulab P1S):")
print("  Material   : PETG (hitzebestaendig)")
print("  Ausrichtung: PLATTE FLACH AUF DAS DRUCKBETT (Zapfen zeigen nach oben)")
print("  Supports   : EIN - nur fuer die runde Charger-Mulde noetig")
print("  Infill     : 20-25 % Gyroid, 3 Perimeter, Layer 0,2 mm")
