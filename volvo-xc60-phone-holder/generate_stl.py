"""
Volvo XC60 Gen1 (2009–2017) – Wireless Charger Unterlage
Erzeugt handyhalter_xc60.stl via CadQuery

Geometrie:
  • Zwei zylindrische Zapfen (hintereinander) greifen in die Becherhalter
  • Solide Brücke verbindet die Zapfen (volle Konsolenbreite)
  • Charger-Pad-Mulde (rund, bündig mit Oberkante) → Rollo schließt drüber
  • Handy-Mulde (rechteckig, 3 mm tief) → iPhone kann nicht verrutschen
  • Kabelkanal durch vorderen Zapfen, Austritt seitlich links
"""

import cadquery as cq
import sys, os

# ──────────────────────────────────────────────────────────────────
# PARAMETER (alle in mm)
# ──────────────────────────────────────────────────────────────────

# Becherhalter
cup_id        = 76.0   # Innendurchmesser Becherhalter
cup_tiefe     = 72.0   # Tiefe Becherhalter (Konsolenrand → Boden)
cup_abstand   = 90.0   # Achsabstand Mitte–Mitte (vorne–hinten)
cup_spiel     =  1.0   # Radiales Spiel der Zapfen (1 mm = leicht einzuführen)

# Konsole
platte_breite = 113.0  # Breite der Konsolenöffnung (links–rechts)

# Wireless Charger Pad
charger_od    = 85.0   # Außendurchmesser Charger-Pad
charger_h     =  6.0   # Dicke des Charger-Pads
kabel_od      =  5.0   # Kabeldurchmesser

# Handy (iPhone 15 Pro inkl. 2 mm Hüllenzugabe je Seite)
phone_l       = 150.0  # Länge
phone_b       =  74.0  # Breite
phone_mulde_t =  3.0   # Tiefe der Handy-Mulde

# System
rollo_luft    =  2.0   # Luft Charger-Oberkante → Rollo
ecken_r       =  5.0   # Eckenabrundung Außenkontur

# ──────────────────────────────────────────────────────────────────
# BERECHNETE GRÖẞEN
# ──────────────────────────────────────────────────────────────────
zapfen_r  = cup_id / 2 - cup_spiel    # Zapfenradius = 37 mm
platte_l  = cup_abstand + cup_id      # Gesamtlänge  = 166 mm
einsatz_h = cup_tiefe - rollo_luft    # Gesamthöhe   = 70 mm
kabel_r   = kabel_od / 2 + 1.0       # Kanalradius mit Spiel = 3.5 mm
plate_h   = 12.0                      # Dicke des Breitenüberstands oben

print(f"Zapfenradius   : {zapfen_r:.1f} mm  (Becherhalter-ID: {cup_id} mm)")
print(f"Plattenbreite  : {platte_breite:.1f} mm")
print(f"Plattenlänge   : {platte_l:.1f} mm")
print(f"Einsatz-Höhe   : {einsatz_h:.1f} mm")
print(f"Rollo-Luft     : {cup_tiefe - einsatz_h:.1f} mm  (Ziel: {rollo_luft} mm)")
print("Modell wird aufgebaut …")

# ──────────────────────────────────────────────────────────────────
# GEOMETRIE AUFBAUEN
# ──────────────────────────────────────────────────────────────────

# 1. Stadion-Körper: slot2D = Konvexe Hülle zweier Kreise (Pille/Stadion)
#    slot2D(length=cup_abstand, diameter=zapfen_r*2) → Stadion-Querschnitt
#    Orientiert entlang Y-Achse → Zapfen liegen bei Y = ±cup_abstand/2
stadium = (
    cq.Workplane("XY")
    .slot2D(cup_abstand, zapfen_r * 2, angle=90)   # Längsrichtung = Y
    .extrude(einsatz_h)
)

# 2. Breite Ablageplatte oben (volle Konsolenbreite, abgerundete Ecken)
plate = (
    cq.Workplane("XY")
    .workplane(offset=einsatz_h - plate_h)
    .rect(platte_breite, platte_l)
    .extrude(plate_h)
    .edges("|Z")            # nur vertikale Kanten abrunden
    .fillet(ecken_r)
)

# 3. Vereinigung
body = stadium.union(plate)

# ──────────────────────────────────────────────────────────────────
# AUSSPARUNGEN
# ──────────────────────────────────────────────────────────────────

# 4. Charger-Pad-Mulde (rund, von oben, bündig mit Oberkante)
charger_cut = (
    cq.Workplane("XY")
    .workplane(offset=einsatz_h - charger_h)
    .circle(charger_od / 2)
    .extrude(charger_h + 1)
)

# 5. Handy-Mulde (abgerundetes Rechteck, 3 mm tief, liegt über Charger-Mulde)
#    Handy-Mulde ist flacher → Boden liegt über Charger-Oberseite → voller Ladekontakt
phone_cut = (
    cq.Workplane("XY")
    .workplane(offset=einsatz_h - phone_mulde_t)
    .rect(phone_b, phone_l)
    .extrude(phone_mulde_t + 1)
    .edges("|Z")
    .fillet(3.0)
)

# 6. Kabelkanal vertikal (durch vorderen Zapfen, volle Höhe)
cable_vert = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .center(0, -cup_abstand / 2)
    .circle(kabel_r)
    .extrude(einsatz_h + 2)
)

# 7. Kabelaustritt horizontal (Schlitz links am vorderen Zapfen)
#    Schneidet horizontal von der Mitte nach links durch die Wand
cable_exit_len = platte_breite / 2 + 5
cable_exit = (
    cq.Workplane("YZ")
    .workplane(offset=-(platte_breite / 2 + 1))
    .center(-cup_abstand / 2, kabel_r + 2)
    .circle(kabel_r)
    .extrude(cable_exit_len)
)

# ──────────────────────────────────────────────────────────────────
# ENDFORM
# ──────────────────────────────────────────────────────────────────
result = (
    body
    .cut(charger_cut)
    .cut(phone_cut)
    .cut(cable_vert)
    .cut(cable_exit)
)

# ──────────────────────────────────────────────────────────────────
# STL EXPORT
# ──────────────────────────────────────────────────────────────────
out_path = os.path.expanduser("~/Downloads/handyhalter_xc60.stl")
cq.exporters.export(result, out_path, tolerance=0.05, angularTolerance=0.1)
print(f"\n✓ STL gespeichert: {out_path}")
print(f"  Dateigroße: {os.path.getsize(out_path) / 1024:.0f} kB")
print("\nDrucktipps:")
print("  Material  : PETG")
print("  Ausrichtung: Handy-Mulde UNTEN auf Druckbett, Zapfen zeigen OBEN")
print("  Infill    : 25 % Gyroid")
print("  Wandstärke: 3 Perimeter, Layer 0,2 mm")
