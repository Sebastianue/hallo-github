#!/usr/bin/env python3
"""
Meta Quest 3 Wall Mount + Controller Dock
STL & PDF Generator — Bambu Lab P1S
"""

import numpy as np
from stl import mesh as stl_mesh
import os, math

OUT = '/home/user/hallo-github'

# ─────────────────────────────────────────────
# GEOMETRY HELPERS
# ─────────────────────────────────────────────

def box_vecs(x1, y1, z1, x2, y2, z2):
    v = np.array([
        [x1,y1,z1],[x2,y1,z1],[x2,y2,z1],[x1,y2,z1],
        [x1,y1,z2],[x2,y1,z2],[x2,y2,z2],[x1,y2,z2]
    ], dtype=np.float32)
    f = [
        [0,2,1],[0,3,2],
        [4,5,6],[4,6,7],
        [0,1,5],[0,5,4],
        [2,3,7],[2,7,6],
        [0,4,7],[0,7,3],
        [1,2,6],[1,6,5],
    ]
    return np.array([[v[t[0]],v[t[1]],v[t[2]]] for t in f], dtype=np.float32)

def cyl_vecs(cx, cy, z1, z2, r, n=24):
    a  = np.linspace(0, 2*np.pi, n, endpoint=False)
    pb = np.column_stack([cx+r*np.cos(a), cy+r*np.sin(a), np.full(n,z1)])
    pt = np.column_stack([cx+r*np.cos(a), cy+r*np.sin(a), np.full(n,z2)])
    vecs = []
    for i in range(n):
        j = (i+1)%n
        vecs += [[pb[i],pb[j],pt[j]], [pb[i],pt[j],pt[i]]]
    cb = np.array([cx,cy,z1]); ct = np.array([cx,cy,z2])
    for i in range(n):
        j = (i+1)%n
        vecs += [[cb,pb[j],pb[i]], [ct,pt[i],pt[j]]]
    return np.array(vecs, dtype=np.float32)

def ring_vecs(cx, cy, z1, z2, ro, ri, n=24):
    a  = np.linspace(0, 2*np.pi, n, endpoint=False)
    oo = np.column_stack([cx+ro*np.cos(a), cy+ro*np.sin(a), np.full(n,z1)])
    ot = np.column_stack([cx+ro*np.cos(a), cy+ro*np.sin(a), np.full(n,z2)])
    io = np.column_stack([cx+ri*np.cos(a), cy+ri*np.sin(a), np.full(n,z1)])
    it = np.column_stack([cx+ri*np.cos(a), cy+ri*np.sin(a), np.full(n,z2)])
    vecs = []
    for i in range(n):
        j = (i+1)%n
        vecs += [[oo[i],oo[j],ot[j]],[oo[i],ot[j],ot[i]]]
        vecs += [[io[j],io[i],it[i]],[io[j],it[i],it[j]]]
        vecs += [[ot[i],it[j],ot[j]],[ot[i],it[i],it[j]]]
        vecs += [[oo[j],oo[i],io[i]],[oo[j],io[i],io[j]]]
    return np.array(vecs, dtype=np.float32)

# ─────────────────────────────────────────────
# BUILD 3-D MODEL
# ─────────────────────────────────────────────
AT   = 18    # U-cradle arm thickness
IX   = 60    # inner half-width  (120 mm opening)
UBOT = 78    # Y-base of U
UTOP = 133   # Y-top of arms
UZ2  = 55    # Z-depth of cradle

all_vecs = []

# Back plate 220 × 280 × 8 mm
all_vecs.append(box_vecs(-110, -140, 0, 110, 140, 8))

# Headset U-cradle
all_vecs.append(box_vecs(-IX-AT, UBOT, 8, -IX,    UTOP, UZ2))   # left arm
all_vecs.append(box_vecs( IX,    UBOT, 8,  IX+AT,  UTOP, UZ2))  # right arm
all_vecs.append(box_vecs(-IX-AT, UBOT, 8,  IX+AT,  UBOT+AT, UZ2))  # crossbar

# Gusset ribs
all_vecs.append(box_vecs(-IX-AT,     50, 8, -IX-AT+12, UBOT, 36))
all_vecs.append(box_vecs( IX+AT-12,  50, 8,  IX+AT,    UBOT, 36))

# Controller pegs
for px in [-83, 83]:
    all_vecs.append(cyl_vecs(px, 5,  8, 60, 13))   # shaft Ø26
    all_vecs.append(cyl_vecs(px, 5, 60, 65, 16))   # anti-slip lip Ø32

# Mounting hole indicator rings
for hx, hy in [(-95,-122),(95,-122),(-95,122),(95,122)]:
    all_vecs.append(ring_vecs(hx, hy, 8, 11.5, 6.5, 3.5))

combined = np.vstack(all_vecs)
m = stl_mesh.Mesh(np.zeros(combined.shape[0], dtype=stl_mesh.Mesh.dtype))
m.vectors = combined
m.update_normals()
stl_path = os.path.join(OUT, 'meta_quest3_wall_mount.stl')
m.save(stl_path)
print(f"STL saved  →  {stl_path}  ({combined.shape[0]} triangles)")


# ─────────────────────────────────────────────
# 3-D PREVIEW WITH MATPLOTLIB
# ─────────────────────────────────────────────
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as mpatches

fig = plt.figure(figsize=(10, 8), dpi=150)
ax  = fig.add_subplot(111, projection='3d')

z_vals = combined[:,:,2].mean(axis=1)
z_min, z_max = z_vals.min(), z_vals.max()

# colour: cool blue palette shaded by Z depth
cmap = plt.cm.Blues
norm_z = (z_vals - z_min) / (z_max - z_min + 1e-6)
face_colors = cmap(0.35 + 0.55 * norm_z)

col = Poly3DCollection(combined, zsort='average', alpha=0.93,
                       facecolor=face_colors, edgecolor='none')
ax.add_collection3d(col)

ax.set_xlim(-130, 130)
ax.set_ylim(-160, 160)
ax.set_zlim(   0,  90)
ax.set_box_aspect([1, 1.27, 0.5])
ax.view_init(elev=30, azim=-50)
ax.set_axis_off()

bg = '#f0f4fa'
ax.set_facecolor(bg)
fig.patch.set_facecolor(bg)

# Annotations
ax.text(0, 152, 62, 'U-Cradle\n(Kopfhalter)', fontsize=8, ha='center',
        color='#1a3a6e', fontweight='bold')
ax.text(-83, 5, 72, 'Ctrl-Peg L', fontsize=7, ha='center', color='#2c5fa5')
ax.text( 83, 5, 72, 'Ctrl-Peg R', fontsize=7, ha='center', color='#2c5fa5')
ax.text(0, -148, 2, 'Wandplatte 220 × 280 × 8 mm', fontsize=7.5,
        ha='center', color='#444', style='italic')

plt.suptitle('Meta Quest 3 — Wandhalterung + Controller Dock',
             fontsize=13, fontweight='bold', y=0.97, color='#1a1a2e')
plt.title('3D-Vorschau (Bambu Lab P1S – kein Support benötigt)',
          fontsize=9, color='#555', pad=4)

img_path = os.path.join(OUT, 'mount_preview.png')
plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig(img_path, dpi=150, bbox_inches='tight', facecolor=bg)
plt.close()
print(f"Preview    →  {img_path}")


# ─────────────────────────────────────────────
# PDF WITH REPORTLAB
# ─────────────────────────────────────────────
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import HexColor, white, black

W, H = A4   # 595.3 x 841.9 pt

def mm2pt(v):
    return v * mm

def new_canvas(path):
    c = rl_canvas.Canvas(path, pagesize=A4)
    return c

def header_bar(c, title, sub='', y_top=H):
    c.setFillColor(HexColor('#1a1a2e'))
    bar_h = 30*mm if sub else 22*mm
    c.rect(0, y_top - bar_h, W, bar_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(W/2, y_top - 18*mm, title)
    if sub:
        c.setFont('Helvetica', 9)
        c.setFillColor(HexColor('#aabbcc'))
        c.drawCentredString(W/2, y_top - 26*mm, sub)

# ─── PAGE 1: technical drawing + specs ───────
c = new_canvas(os.path.join(OUT, 'meta_quest3_wall_mount.pdf'))

header_bar(c, 'META QUEST 3 — WANDHALTERUNG + CONTROLLER DOCK',
           'Für Bambu Lab P1S  |  PETG / PLA+  |  Kein Support erforderlich')

# ─── 2-D technical diagram ───────────────────
# Plate: 220 × 280 mm   centre = (CX_pt, CY_pt) in ReportLab pts
CX = 95*mm     # diagram centre X
CY = 160*mm    # diagram centre Y (from page bottom)
S  = 0.64*mm   # scale: 1 design-mm → S pts

def dx(x): return CX + x*S
def dy(y): return CY + y*S   # ReportLab Y goes UP

# Plate outline
c.setFillColor(HexColor('#dce8f8'))
c.setStrokeColor(HexColor('#3c5080'))
c.setLineWidth(0.5)
c.rect(dx(-110), dy(-140), 220*S, 280*S, fill=1, stroke=1)

# U-cradle fill
c.setFillColor(HexColor('#a0bce6'))
# left arm
c.rect(dx(-IX-AT), dy(UBOT), AT*S, (UTOP-UBOT)*S, fill=1, stroke=1)
# right arm
c.rect(dx(IX), dy(UBOT), AT*S, (UTOP-UBOT)*S, fill=1, stroke=1)
# crossbar
c.rect(dx(-IX-AT), dy(UBOT), (2*IX+2*AT)*S, AT*S, fill=1, stroke=1)

# gussets
c.setFillColor(HexColor('#8cabe0'))
c.rect(dx(-IX-AT),    dy(50), 12*S, (UBOT-50)*S, fill=1, stroke=0)
c.rect(dx(IX+AT-12),  dy(50), 12*S, (UBOT-50)*S, fill=1, stroke=0)

# Controller peg circles
c.setFillColor(HexColor('#6488cc'))
c.setStrokeColor(HexColor('#3c5080'))
c.setLineWidth(0.5)
for px_ in [-83, 83]:
    c.circle(dx(px_), dy(5), 13*S, fill=1, stroke=1)
    # lip ring
    c.setFillColor(HexColor('#4a6db5'))
    c.circle(dx(px_), dy(5), 16*S, fill=0, stroke=1)
    c.setFillColor(HexColor('#6488cc'))

# Mounting hole rings
for hx_, hy_ in [(-95,-122),(95,-122),(-95,122),(95,122)]:
    c.setFillColor(white)
    c.setStrokeColor(HexColor('#505050'))
    c.setLineWidth(0.4)
    c.circle(dx(hx_), dy(hy_), 6.5*S, fill=1, stroke=1)
    c.setFillColor(HexColor('#dce8f8'))
    c.circle(dx(hx_), dy(hy_), 3.5*S, fill=1, stroke=1)

# ─── Dimension lines ─────────────────────────
c.setStrokeColor(HexColor('#333366'))
c.setLineWidth(0.3)
c.setFillColor(HexColor('#333366'))
c.setFont('Helvetica', 6.5)

def dim_h(x1d, x2d, yd, label):
    y = dy(yd)
    x1, x2 = dx(x1d), dx(x2d)
    c.line(x1, y-3, x1, y+3)
    c.line(x2, y-3, x2, y+3)
    c.line(x1, y, x2, y)
    c.drawCentredString((x1+x2)/2, y+2, label)

def dim_v(y1d, y2d, xd, label):
    x = dx(xd)
    y1, y2 = dy(y1d), dy(y2d)
    c.line(x-3, y1, x+3, y1)
    c.line(x-3, y2, x+3, y2)
    c.line(x, y1, x, y2)
    c.drawCentredString(x+18, (y1+y2)/2, label)

dim_h(-110, 110,  148, '220 mm')
dim_v(-140, 140,  118, '280 mm')
dim_h(-IX-AT, IX+AT, 140, '156 mm')
dim_h(-IX, IX, 81, '120 mm')

# Label annotations
c.setFont('Helvetica-Bold', 7)
c.setFillColor(HexColor('#1a3a6e'))
c.drawString(dx(-IX-AT)-28*mm, dy(109), 'U-Cradle')
c.drawString(dx(-IX-AT)-28*mm, dy(103), '(Kopfhalter)')
c.setFillColor(HexColor('#2c5fa5'))
c.drawString(dx(83)+5*mm, dy(12), 'Peg R')
c.drawString(dx(-83)-14*mm, dy(12), 'Peg L')
c.setFillColor(HexColor('#666'))
c.setFont('Helvetica', 6.5)
c.drawString(dx(-110)+1*mm, dy(-127), 'M5')
c.drawString(dx(91), dy(-127), 'M5')
c.drawString(dx(-110)+1*mm, dy(120), 'M5')
c.drawString(dx(91), dy(120), 'M5')

# ─── Right specs panel ───────────────────────
rx = 148*mm
panel_y_top = H - 30*mm
panel_h = 250*mm
c.setFillColor(HexColor('#eef2fc'))
c.setStrokeColor(HexColor('#8090c0'))
c.setLineWidth(0.4)
c.rect(rx, panel_y_top - panel_h, 57*mm, panel_h, fill=1, stroke=1)

def panel_section(title, items, y_start):
    y = y_start
    c.setFillColor(HexColor('#1a3a6e'))
    c.rect(rx+2*mm, y-6*mm, 53*mm, 6*mm, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 8.5)
    c.drawCentredString(rx+28.5*mm, y-4.5*mm, title)
    y -= 8*mm
    c.setStrokeColor(HexColor('#8090c0'))
    c.setLineWidth(0.3)
    c.line(rx+3*mm, y, rx+54*mm, y)
    y -= 1*mm
    for k, v in items:
        c.setFont('Helvetica', 7)
        c.setFillColor(HexColor('#444'))
        c.drawString(rx+3*mm, y, k)
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(HexColor('#1a3a6e'))
        c.drawRightString(rx+55*mm, y, v)
        y -= 5.5*mm
    return y

dim_items = [
    ('Rückplatte',    '220×280×8 mm'),
    ('U-Cradle Breite','156 mm'),
    ('Innen-Öffnung', '120 mm'),
    ('Arm-Stärke',    '18 mm'),
    ('Peg Schaft Ø',  '26 mm'),
    ('Peg Länge',     '57 mm'),
    ('Peg Lippe Ø',   '32 mm'),
    ('Gesamt-Tiefe',  '65 mm'),
    ('Bohrloch-Abst.','190 × 244 mm'),
]
print_items = [
    ('Drucker',       'Bambu P1S'),
    ('Material',      'PETG / PLA+'),
    ('Layer-Höhe',    '0.20 mm'),
    ('Wandstärke',    '3 Perimeter'),
    ('Infill',        '25 % Gyroid'),
    ('Supports',      'Kein!'),
    ('Druckzeit',     '~5–6 h'),
    ('Filament',      '~120 g'),
    ('Bett-Temp.',    '85 °C (PETG)'),
    ('Nozzle',        '240 °C'),
    ('Plate',         'Textured PEI'),
]

y_cur = panel_y_top - 2*mm
y_cur = panel_section('ABMESSUNGEN', dim_items, y_cur) - 3*mm
y_cur = panel_section('DRUCKINFO',   print_items, y_cur)

c.showPage()


# ─── PAGE 2: preview image + description ─────
header_bar(c, 'MONTAGEANLEITUNG & HINWEISE')

# 3-D preview image
if os.path.exists(img_path):
    c.drawImage(img_path, 10*mm, H - 30*mm - 95*mm,
                width=120*mm, height=90*mm,
                preserveAspectRatio=True, anchor='nw')
img_bottom = H - 30*mm - 97*mm

# Assembly steps box (right of image)
bx = 135*mm; by = H - 30*mm - 95*mm; bw = 65*mm; bh = 93*mm
c.setFillColor(HexColor('#eef2fc'))
c.setStrokeColor(HexColor('#8090c0'))
c.setLineWidth(0.4)
c.rect(bx, by, bw, bh, fill=1, stroke=1)
c.setFillColor(HexColor('#1a3a6e'))
c.rect(bx, by+bh-7*mm, bw, 7*mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont('Helvetica-Bold', 8.5)
c.drawCentredString(bx+bw/2, by+bh-5*mm, 'MONTAGE-SCHRITTE')

steps = [
    ('1', 'STL in Bambu Studio laden'),
    ('2', 'Flache Seite auf Bett'),
    ('3', 'Slice: Gyroid 25 %, kein Support'),
    ('4', 'Drucken (PETG empfohlen)'),
    ('5', '4× M5-Dübel bohren & setzen'),
    ('  ', 'Abstand: 190 × 244 mm'),
    ('6', 'Platte einhängen & schrauben'),
    ('7', 'Quest 3 Halo-Band in U legen'),
    ('8', 'Controller auf Pegs hängen'),
    ('  ', 'Fertig — viel Spaß! ✔'),
]
sy = by + bh - 9.5*mm
for num, txt in steps:
    c.setFont('Helvetica-Bold' if num.strip().isdigit() else 'Helvetica', 7.5)
    c.setFillColor(HexColor('#1a3a6e') if num.strip().isdigit() else HexColor('#444'))
    c.drawString(bx+3*mm, sy, f'{num}  {txt}')
    sy -= 5.8*mm

# ─── Feature blocks ──────────────────────────
fy = img_bottom - 8*mm
c.setFillColor(HexColor('#1a1a2e'))
c.rect(10*mm, fy, W-20*mm, 7*mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont('Helvetica-Bold', 9)
c.drawCentredString(W/2, fy+2*mm, 'FEATURES & DESIGN-ENTSCHEIDUNGEN')
fy -= 5*mm

features = [
    ('U-Cradle Kopfhalter',
     '120 mm breite Öffnung für den Halo-Band des Quest 3. Armstärke 18 mm und '
     'Gusset-Rippen verhindern Durchbiegen. Tiefe 47 mm hält den Kopfhörer sicher '
     'ohne zu verrutschen.'),
    ('Anti-Slip Controller-Pegs',
     'Zwei Ø 26 mm Zylinder-Pegs mit Ø 32 mm Lippe. Der Wrist-Loop des Touch Plus '
     'Controllers hängt sicher darüber. Abstand 166 mm entspricht der Griffbreite. '
     'Schaft-Länge 52 mm gibt genug Platz für den Controller-Ring.'),
    ('Wandplatte & Dübel-Markierungen',
     '220 × 280 × 8 mm Platte. 4 eingefrästete Ringmarkierungen (Ø 13 mm) zeigen '
     'die Bohrstellen für M5-Schrauben. Lochbild: 190 mm horizontal, 244 mm '
     'vertikal. Maximale Traglast mit PETG: ~2 kg.'),
    ('Support-freies Drucken',
     'Vollständig support-frei auf dem Bambu P1S druckbar. Alle Überhänge < 45°. '
     'Flache Rückseite auf das Druckbett legen. Textured PEI empfohlen für '
     'optimale Haftung bei PETG.'),
]

for title, desc in features:
    c.setFont('Helvetica-Bold', 8.5)
    c.setFillColor(HexColor('#1a3a6e'))
    c.drawString(14*mm, fy, f'▸  {title}')
    fy -= 4.5*mm
    c.setFont('Helvetica', 7.5)
    c.setFillColor(HexColor('#333'))
    lines = []
    words = desc.split()
    line = ''
    for w in words:
        test = (line + ' ' + w).strip()
        if c.stringWidth(test, 'Helvetica', 7.5) < 175*mm:
            line = test
        else:
            lines.append(line)
            line = w
    lines.append(line)
    for l in lines:
        c.drawString(20*mm, fy, l)
        fy -= 4*mm
    fy -= 3*mm

# ─── Material table ──────────────────────────
fy -= 2*mm
c.setFillColor(HexColor('#1a1a2e'))
c.rect(10*mm, fy, W-20*mm, 7*mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont('Helvetica-Bold', 9)
c.drawCentredString(W/2, fy+2*mm, 'MATERIAL-EMPFEHLUNG')
fy -= 1*mm

headers = ['Material', 'Nozzle', 'Bett', 'Stabilität', 'Hinweis']
col_w   = [30*mm, 16*mm, 14*mm, 22*mm, 0]
col_w[4] = W - 20*mm - sum(col_w[:4])

mat_rows = [
    ['PETG  ★ (empfohlen)', '240 °C', '85 °C', 'Hoch',     'UV-beständig, leicht flexibel, beste Wahl'],
    ['PLA+',                '220 °C', '60 °C', 'Mittel',   'Einfacher Druck, nicht für heiße Räume'],
    ['ASA',                 '250 °C', '100 °C','Sehr hoch','Für helle/warme Umgebungen'],
]
row_h = 6.5*mm
# header row
c.setFillColor(HexColor('#3c5080'))
c.rect(10*mm, fy - row_h, W-20*mm, row_h, fill=1, stroke=0)
c.setFillColor(white)
c.setFont('Helvetica-Bold', 7.5)
cx_ = 10*mm
for h, w in zip(headers, col_w):
    c.drawCentredString(cx_ + w/2, fy - row_h + 2*mm, h)
    cx_ += w
fy -= row_h

for ri, row in enumerate(mat_rows):
    bg = HexColor('#e8edf8') if ri % 2 == 0 else HexColor('#f0f4fc')
    c.setFillColor(bg)
    c.rect(10*mm, fy - row_h, W-20*mm, row_h, fill=1, stroke=0)
    cx_ = 10*mm
    for ci, (val, w) in enumerate(zip(row, col_w)):
        c.setFont('Helvetica-Bold' if ci == 0 else 'Helvetica', 7.5)
        c.setFillColor(HexColor('#1a3a6e') if ci == 0 else HexColor('#222'))
        c.drawString(cx_ + 2*mm, fy - row_h + 2*mm, val)
        cx_ += w
    fy -= row_h

# final note
fy -= 5*mm
c.setFont('Helvetica-Oblique', 7)
c.setFillColor(HexColor('#666'))
note = ('Tipp: Nach dem Druck die Ringmarkierungen mit einem Ø 5 mm Bohrer '
        'durchbohren. Für Wandabstände: 4× M5-Dübel im 190 × 244 mm Raster setzen. '
        'Maximale Traglast mit PETG + Betonwand: ca. 2 kg.')
c.drawString(10*mm, fy, note[:100])
fy -= 4*mm
c.drawString(10*mm, fy, note[100:])

c.save()
pdf_path = os.path.join(OUT, 'meta_quest3_wall_mount.pdf')
print(f"PDF saved  →  {pdf_path}")
print("\nAlle Dateien erfolgreich erstellt!")
print(f"  {stl_path}")
print(f"  {img_path}")
print(f"  {pdf_path}")
