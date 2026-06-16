#!/usr/bin/env python3
"""Meta Quest 3 Wandhalterung — Verkaufsvorschau Generator"""

import numpy as np, io, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image, ImageDraw, ImageFilter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import HexColor, white

OUT = '/home/user/hallo-github'

# ── geometry primitives ──────────────────────────────────────
def box_v(x1,y1,z1,x2,y2,z2):
    v = np.array([[x1,y1,z1],[x2,y1,z1],[x2,y2,z1],[x1,y2,z1],
                  [x1,y1,z2],[x2,y1,z2],[x2,y2,z2],[x1,y2,z2]],dtype=np.float32)
    f = [[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],
         [2,3,7],[2,7,6],[0,4,7],[0,7,3],[1,2,6],[1,6,5]]
    return np.array([[v[t[0]],v[t[1]],v[t[2]]] for t in f],dtype=np.float32)

def cyl_v(cx,cy,z1,z2,r,n=20):
    a = np.linspace(0,2*np.pi,n,endpoint=False)
    pb = np.column_stack([cx+r*np.cos(a),cy+r*np.sin(a),np.full(n,z1)])
    pt = np.column_stack([cx+r*np.cos(a),cy+r*np.sin(a),np.full(n,z2)])
    vecs=[]
    for i in range(n):
        j=(i+1)%n
        vecs+=[[pb[i],pb[j],pt[j]],[pb[i],pt[j],pt[i]]]
    cb=np.array([cx,cy,z1]); ct=np.array([cx,cy,z2])
    for i in range(n):
        j=(i+1)%n
        vecs+=[[cb,pb[j],pb[i]],[ct,pt[i],pt[j]]]
    return np.array(vecs,dtype=np.float32)

def ring_v(cx,cy,z1,z2,ro,ri,n=20):
    a=np.linspace(0,2*np.pi,n,endpoint=False)
    oo=np.column_stack([cx+ro*np.cos(a),cy+ro*np.sin(a),np.full(n,z1)])
    ot=np.column_stack([cx+ro*np.cos(a),cy+ro*np.sin(a),np.full(n,z2)])
    io_=np.column_stack([cx+ri*np.cos(a),cy+ri*np.sin(a),np.full(n,z1)])
    it=np.column_stack([cx+ri*np.cos(a),cy+ri*np.sin(a),np.full(n,z2)])
    vecs=[]
    for i in range(n):
        j=(i+1)%n
        vecs+=[[oo[i],oo[j],ot[j]],[oo[i],ot[j],ot[i]]]
        vecs+=[[io_[j],io_[i],it[i]],[io_[j],it[i],it[j]]]
        vecs+=[[ot[i],it[j],ot[j]],[ot[i],it[i],it[j]]]
        vecs+=[[oo[j],oo[i],io_[i]],[oo[j],io_[i],io_[j]]]
    return np.array(vecs,dtype=np.float32)

# ── normal-based shading ─────────────────────────────────────
LIGHT = np.array([-0.45, 0.38, 1.0]); LIGHT /= np.linalg.norm(LIGHT)

def shade(vecs, rgb, ambient=0.22, diffuse=0.78):
    cols=[]
    for tri in vecs:
        e1=tri[1]-tri[0]; e2=tri[2]-tri[0]
        n=np.cross(e1,e2); nl=np.linalg.norm(n)
        if nl>1e-9: n/=nl
        b = ambient + diffuse*max(0.0,float(np.dot(n,LIGHT)))
        cols.append((min(1,rgb[0]*b), min(1,rgb[1]*b), min(1,rgb[2]*b), 0.96))
    return cols

# ════════════════════════════════════════════
# SCENE GEOMETRY
# ════════════════════════════════════════════

# Mount constants
AT=18; IX=60; UBOT=78; UTOP=133; UZ2=55

mount=[]
mount.append(box_v(-110,-140,0,110,140,8))              # plate
mount.append(box_v(-IX-AT,UBOT,8,-IX,UTOP,UZ2))         # U left arm
mount.append(box_v(IX,UBOT,8,IX+AT,UTOP,UZ2))           # U right arm
mount.append(box_v(-IX-AT,UBOT,8,IX+AT,UBOT+AT,UZ2))    # U crossbar
mount.append(box_v(-IX-AT,50,8,-IX-AT+12,UBOT,36))      # gusset L
mount.append(box_v(IX+AT-12,50,8,IX+AT,UBOT,36))        # gusset R
# Pegs at Y=-70 (below headset body which ends at Y=-18)
for px in [-83,83]:
    mount.append(cyl_v(px,-70,8,60,13))
    mount.append(cyl_v(px,-70,60,65,16))
# Mounting hole rings
for hx,hy in [(-95,-122),(95,-122),(-95,122),(95,122)]:
    mount.append(ring_v(hx,hy,8,11.5,6.5,3.5))
mount_all = np.vstack(mount)

# Meta Quest 3 headset — hanging in U-cradle
# Halo band rests in crossbar (Y=78-96); body hangs below Y=77
hs=[]
hs.append(box_v(-90,-18,18, 90,77,57))      # main body (charcoal)
hs.append(box_v(-88,-16,55, 88,75,59))      # front panel (darker)
hs.append(box_v(-74, -5,54, 74,68,61))      # visor / lens area
hs.append(box_v(-93, 12,22,-88,63,50))      # left side wing
hs.append(box_v( 88, 12,22, 93,63,50))      # right side wing
hs.append(cyl_v(-27,30,58,64,7))            # camera bump L
hs.append(cyl_v( 27,30,58,64,7))            # camera bump R
hs.append(box_v(-92,73,24, 92,79,44))       # halo band connector (top)
hs_all = np.vstack(hs)

# Touch Plus controllers — hanging on pegs (X=±83, Y=-70)
ctrl=[]
for px in [-83,83]:
    s = 1 if px>0 else -1
    ctrl.append(box_v(px-14,-138,32,px+14,-68,50))   # handle body
    ctrl.append(box_v(px-24,-75,27,px+24,-67,53))    # ring guard (flat top)
    ctrl.append(box_v(px-19,-82,29,px+19,-67,51))    # grip top
    # thumbstick (small cylinder on face, pointing Z+)
    ctrl.append(cyl_v(px-s*8,-79,50,57,5))
ctrl_all = np.vstack(ctrl)

# Wall panel behind mount (very light)
wall = np.array([[[-140,-160,-1],[140,-160,-1],[140,160,-1]],
                  [[-140,-160,-1],[140,160,-1],[-140,160,-1]]],dtype=np.float32)

# ════════════════════════════════════════════
# 3-D RENDER WITH MATPLOTLIB
# ════════════════════════════════════════════
fig = plt.figure(figsize=(13,9), dpi=130)
ax  = fig.add_subplot(111, projection='3d')

# Wall
ax.add_collection3d(Poly3DCollection(wall, facecolors=['#f5f0ea'], edgecolor='none', alpha=1.0, zsort='average'))

# Mount — steel blue
mc = shade(mount_all, (0.28,0.50,0.83))
ax.add_collection3d(Poly3DCollection(mount_all, facecolors=mc, edgecolor='none', alpha=0.97, zsort='average'))

# Headset — dark charcoal body
hc_body  = shade(np.vstack([hs[0],hs[3],hs[4],hs[7]]), (0.13,0.13,0.14))
hc_panel = shade(np.vstack([hs[1]]),                    (0.08,0.08,0.09))
hc_visor = shade(np.vstack([hs[2]]),                    (0.10,0.12,0.16))
hc_cams  = shade(np.vstack([hs[5],hs[6]]),              (0.20,0.20,0.22))
ax.add_collection3d(Poly3DCollection(np.vstack([hs[0],hs[3],hs[4],hs[7]]), facecolors=hc_body,  edgecolor='none', alpha=0.97, zsort='average'))
ax.add_collection3d(Poly3DCollection(hs[1],  facecolors=hc_panel, edgecolor='none', alpha=0.97, zsort='average'))
ax.add_collection3d(Poly3DCollection(hs[2],  facecolors=hc_visor, edgecolor='none', alpha=0.97, zsort='average'))
ax.add_collection3d(Poly3DCollection(np.vstack([hs[5],hs[6]]), facecolors=hc_cams, edgecolor='none', alpha=0.97, zsort='average'))

# Controllers — dark anthracite
cc = shade(ctrl_all, (0.18,0.18,0.19))
ax.add_collection3d(Poly3DCollection(ctrl_all, facecolors=cc, edgecolor='none', alpha=0.97, zsort='average'))

ax.set_xlim(-140,140); ax.set_ylim(-160,160); ax.set_zlim(-5,88)
ax.set_box_aspect([1,1.18,0.48])
ax.view_init(elev=19, azim=-40)
ax.set_axis_off()
ax.set_facecolor('#f5f0ea')
fig.patch.set_facecolor('#f5f0ea')
plt.subplots_adjust(left=0,right=1,top=1,bottom=0)

buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=130, bbox_inches='tight', facecolor='#f5f0ea')
buf.seek(0)
render = Image.open(buf).copy()
buf.close(); plt.close()
print(f"Render: {render.size}")

# ════════════════════════════════════════════
# SALES POSTER  (Pillow composite)
# ════════════════════════════════════════════
PW, PH = 1800, 1000

poster = Image.new('RGB', (PW, PH), '#ffffff')
draw   = ImageDraw.Draw(poster)

# --- background gradient (wall) left side ---
for y in range(PH):
    t = y/PH
    r = int(245 - t*12); g = int(240 - t*10); b = int(234 - t*8)
    draw.line([(0,y),(1200,y)], fill=(r,g,b))

# --- right dark panel ---
for x in range(1200, PW):
    draw.line([(x,0),(x,PH)], fill=(22,22,38))

# --- paste render ---
rw, rh = render.size
scale   = min(1160/rw, 980/rh)
rw2,rh2 = int(rw*scale), int(rh*scale)
render_s = render.resize((rw2,rh2), Image.LANCZOS)
rx = (1200-rw2)//2; ry = (PH-rh2)//2
poster.paste(render_s, (rx,ry))

# soft shadow under mount area
shadow_layer = Image.new('RGBA', (PW,PH), (0,0,0,0))
sd = ImageDraw.Draw(shadow_layer)
sd.ellipse([rx+rw2//4, ry+rh2-60, rx+3*rw2//4, ry+rh2+30], fill=(0,0,0,60))
shadow_blur = shadow_layer.filter(ImageFilter.GaussianBlur(radius=18))
poster = Image.alpha_composite(poster.convert('RGBA'), shadow_blur).convert('RGB')
draw = ImageDraw.Draw(poster)

# --- accent line divider ---
for y in range(PH):
    draw.rectangle([1198,y,1201,y], fill=(74,127,212))

# --- right panel text ---
def txt(x,y,text,size=16,color='#ffffff',bold=False):
    draw.text((x,y), text, fill=color, font=None)

panel_x = 1230

# Title
draw.rectangle([panel_x-5, 60, PW-20, 65], fill='#4a7fd4')
draw.text((panel_x, 75),  "META QUEST 3",          fill='#4a7fd4')
draw.text((panel_x, 105), "WANDHALTERUNG",          fill='#ffffff')
draw.text((panel_x, 145), "+ CONTROLLER DOCK",      fill='#aabbee')
draw.text((panel_x, 195), "3D-Gedruckt | PETG",     fill='#8899cc')

# Divider
draw.line([(panel_x, 230),(PW-30,230)], fill='#3a3a5a', width=1)

# Features
features = [
    ("◆", "U-Cradle Kopfhalter"),
    ("◆", "Anti-Slip Controller-Pegs"),
    ("◆", "Kein Support nötig"),
    ("◆", "Passend für Halo-Band"),
    ("◆", "220 × 280 mm Wandplatte"),
    ("◆", "4× M5 Wandbefestigung"),
    ("◆", "PETG / PLA+ / ASA"),
    ("◆", "Bambu Lab P1S optimiert"),
]
fy = 255
for dot, feat in features:
    draw.text((panel_x, fy),      dot,  fill='#4a7fd4')
    draw.text((panel_x+22, fy),   feat, fill='#ddeeff')
    fy += 38

# Divider
draw.line([(panel_x, fy+5),(PW-30, fy+5)], fill='#3a3a5a', width=1)
fy += 25

# Dimensions box
draw.text((panel_x, fy),    "ABMESSUNGEN",  fill='#8899cc')
fy += 30
dims = [("Platte:",  "220 × 280 × 8 mm"),
        ("Tiefe:",   "65 mm"),
        ("Peg Ø:",   "26 mm / 32 mm Lippe"),
        ("Bohrbild:", "190 × 244 mm")]
for k,v in dims:
    draw.text((panel_x,    fy), k, fill='#aab8cc')
    draw.text((panel_x+140,fy), v, fill='#ffffff')
    fy += 30

# Divider
draw.line([(panel_x, fy+5),(PW-30, fy+5)], fill='#3a3a5a', width=1)
fy += 25

draw.text((panel_x, fy),    "DRUCKZEIT ca. 5–6 h  |  ~120 g",  fill='#6677aa')
fy += 35
draw.text((panel_x, fy),    "Layer: 0.2 mm  |  Infill: 25%",   fill='#6677aa')

# Price badge
bx1,by1,bx2,by2 = panel_x, PH-120, PW-30, PH-30
draw.rounded_rectangle([bx1,by1,bx2,by2], radius=12, fill='#4a7fd4')
draw.text((bx1+25, by1+15), "Empf. Verkaufspreis", fill='#c0d8ff')
draw.text((bx1+25, by1+40), "€ 24,99 – 34,99",    fill='#ffffff')

# Watermark bottom-left
draw.text((20, PH-30), "Kein Support erforderlich  |  Für Bambu Lab P1S optimiert", fill='#888888')

sales_img_path = os.path.join(OUT, 'sales_preview.png')
poster.save(sales_img_path, quality=95)
print(f"Sales image → {sales_img_path}")

# ════════════════════════════════════════════
# SALES PDF  (reportlab, A4)
# ════════════════════════════════════════════
W, H = A4
pdf_path = os.path.join(OUT, 'sales_preview.pdf')
c = rl_canvas.Canvas(pdf_path, pagesize=A4)

# ── Page 1: full sales poster ────────────────
c.setFillColor(HexColor('#f5f0ea'))
c.rect(0, 0, W, H, fill=1, stroke=0)
c.drawImage(sales_img_path, 0, 0, width=W, height=H, preserveAspectRatio=False)
c.setFillColor(HexColor('#1a1a26'))
c.setFont('Helvetica', 7)
c.setFillColor(HexColor('#888888'))
c.drawCentredString(W/2, 8*mm, 'Meta Quest 3 Wandhalterung + Controller Dock  |  3D-Druck STL  |  Für Bambu Lab P1S')
c.showPage()

# ── Page 2: render + detail views ───────────
c.setFillColor(HexColor('#f5f0ea'))
c.rect(0, 0, W, H, fill=1, stroke=0)

# header
c.setFillColor(HexColor('#1a1a2e'))
c.rect(0, H-25*mm, W, 25*mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont('Helvetica-Bold', 14)
c.drawCentredString(W/2, H-15*mm, 'META QUEST 3 WANDHALTERUNG — PRODUKTDETAILS')

# main render (large, left)
render_2 = render.resize((int(render.size[0]*0.7), int(render.size[1]*0.7)), Image.LANCZOS)
r2_path = os.path.join(OUT, '_tmp_render2.png')
render_2.save(r2_path)
c.drawImage(r2_path, 8*mm, H-25*mm-115*mm, width=120*mm, height=110*mm, preserveAspectRatio=True, anchor='nw')

# right side: feature table
rx = 138*mm; ry = H-30*mm
c.setFillColor(HexColor('#1a1a2e'))
c.rect(rx, ry-175*mm, 67*mm, 175*mm, fill=1, stroke=0)

c.setFillColor(HexColor('#4a7fd4'))
c.rect(rx, ry-8*mm, 67*mm, 8*mm, fill=1, stroke=0)
c.setFillColor(white)
c.setFont('Helvetica-Bold', 9)
c.drawCentredString(rx+33.5*mm, ry-5.5*mm, 'FEATURES')

items = [
    ('Kopfhalter', 'U-Cradle 120mm Öffnung'),
    ('Controller', '2× Anti-Slip Peg Ø26mm'),
    ('Wandplatte', '220 × 280 × 8 mm'),
    ('Befestigung', '4× M5 Dübel'),
    ('Infill', '25% Gyroid'),
    ('Support', 'Kein Support!'),
    ('Material', 'PETG / PLA+ / ASA'),
    ('Druckzeit', '~5–6 Stunden'),
    ('Gewicht', '~120 g Filament'),
    ('Schicht', '0.20 mm'),
    ('Bett', 'Textured PEI'),
    ('Kompatibel', 'Quest 3 & 3S'),
]
iy = ry-12*mm
for k,v in items:
    c.setFont('Helvetica', 7); c.setFillColor(HexColor('#8899cc'))
    c.drawString(rx+3*mm, iy, k)
    c.setFont('Helvetica-Bold', 7.5); c.setFillColor(white)
    c.drawString(rx+28*mm, iy, v)
    iy -= 10*mm

# price badge
c.setFillColor(HexColor('#4a7fd4'))
c.roundRect(rx+3*mm, iy-16*mm, 61*mm, 14*mm, 4, fill=1, stroke=0)
c.setFillColor(white); c.setFont('Helvetica-Bold', 11)
c.drawCentredString(rx+33.5*mm, iy-8*mm, '€ 24,99 – 34,99')

# Bottom section: 3 info boxes
box_y = H-25*mm-125*mm; box_h = 55*mm; box_w = 60*mm
labels = [
    ('DRUCKMATERIAL', ['✔  PETG (empfohlen)', '✔  PLA+ (Alternative)', '✔  ASA (Outdoor)',
                       '','Bett: 85°C | Nozzle: 240°C']),
    ('MONTAGE', ['① STL in Bambu Studio öffnen', '② Slice: kein Support',
                 '③ 4× M5 Dübel in Wand', '④ Platte einhängen', '⑤ Geräte einlegen']),
    ('LIEFERUMFANG', ['✔  Druckfertige STL-Datei', '✔  PDF Montageanleitung',
                      '✔  Technische Zeichnung', '','Kein Assembly nötig']),
]
for i,(title,lines) in enumerate(labels):
    bx = 8*mm + i*(box_w+3*mm)
    c.setFillColor(HexColor('#1a1a2e'))
    c.rect(bx, box_y, box_w, box_h, fill=1, stroke=0)
    c.setFillColor(HexColor('#4a7fd4'))
    c.rect(bx, box_y+box_h-8*mm, box_w, 8*mm, fill=1, stroke=0)
    c.setFillColor(white); c.setFont('Helvetica-Bold', 7.5)
    c.drawCentredString(bx+box_w/2, box_y+box_h-5*mm, title)
    c.setFont('Helvetica', 7); lly = box_y+box_h-13*mm
    for ln in lines:
        c.setFillColor(HexColor('#aabbdd'))
        c.drawString(bx+3*mm, lly, ln); lly -= 7.5*mm

# footer
c.setFont('Helvetica', 7); c.setFillColor(HexColor('#999'))
c.drawCentredString(W/2, 8*mm, 'Meta Quest 3 Wandhalterung  |  STL-Datei  |  Bambu Lab P1S  |  Kein Support benötigt')

c.save()
if os.path.exists(r2_path): os.remove(r2_path)

print(f"Sales PDF  → {pdf_path}")
print("\nFertig!")
