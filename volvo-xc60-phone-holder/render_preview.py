"""
Rendert eine PNG-Vorschau der handyhalter_xc60.stl
Drei Ansichten: Perspektive, Oben, Seite
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import struct, os

# ── STL laden ────────────────────────────────────────────────────
def load_stl(path):
    triangles, normals = [], []
    with open(path, "rb") as f:
        f.read(80)
        n = struct.unpack("<I", f.read(4))[0]
        for _ in range(n):
            normal = struct.unpack("<fff", f.read(12))
            v = [struct.unpack("<fff", f.read(12)) for _ in range(3)]
            f.read(2)
            triangles.append(v)
            normals.append(normal)
    return np.array(triangles), np.array(normals)

stl_path = os.path.expanduser("~/Downloads/handyhalter_xc60.stl")
tris, norms = load_stl(stl_path)

# ── Bounding Box ─────────────────────────────────────────────────
all_pts = tris.reshape(-1, 3)
mn, mx = all_pts.min(axis=0), all_pts.max(axis=0)
center = (mn + mx) / 2
size   = (mx - mn).max()

# ── Farbe: Beleuchtung simulieren ────────────────────────────────
light = np.array([1, 0.6, 1.5])
light = light / np.linalg.norm(light)

face_centers = tris.mean(axis=1)
dot = np.einsum("ij,j->i", norms, light)
# Normalisieren auf [0.25, 1.0] für Helligkeit
dot_norm = (dot - dot.min()) / (dot.max() - dot.min() + 1e-9)
brightness = 0.25 + 0.75 * dot_norm

# XC60-Volvo-Blau als Basisfarbe
base = np.array([0.09, 0.30, 0.55])   # Volvo-Dunkelblau
colors = np.outer(brightness, base)    # shape: (n_tris, 3)
facecolors = [tuple(c) + (0.92,) for c in colors]

# ── Figur mit 3 Subplots ─────────────────────────────────────────
fig = plt.figure(figsize=(16, 6), facecolor="#1a1a2e")
fig.suptitle(
    "Volvo XC60 – Wireless Charger Unterlage   |   PETG · Bambulab P1S",
    color="white", fontsize=13, fontweight="bold", y=0.97
)

views = [
    ("Perspektive",   25, -50),
    ("Draufsicht",    88, -90),
    ("Seitenansicht",  0, -90),
]

axes = []
for i, (title, elev, azim) in enumerate(views):
    ax = fig.add_subplot(1, 3, i + 1, projection="3d", facecolor="#0d0d1a")
    axes.append(ax)

    poly = Poly3DCollection(tris, facecolors=facecolors, linewidths=0,
                            zsort="average", antialiased=False)
    ax.add_collection3d(poly)

    pad = size * 0.08
    ax.set_xlim(mn[0] - pad, mx[0] + pad)
    ax.set_ylim(mn[1] - pad, mx[1] + pad)
    ax.set_zlim(mn[2] - pad, mx[2] + pad)

    ax.set_box_aspect([mx[0]-mn[0], mx[1]-mn[1], mx[2]-mn[2]])
    ax.view_init(elev=elev, azim=azim)

    ax.set_title(title, color="white", fontsize=10, pad=4)
    ax.set_xlabel("X", color="#888", fontsize=7)
    ax.set_ylabel("Y", color="#888", fontsize=7)
    ax.set_zlabel("Z", color="#888", fontsize=7)
    ax.tick_params(colors="#555", labelsize=6)
    for spine in ax.spines.values():
        spine.set_color("#333")
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("#222")
    ax.yaxis.pane.set_edgecolor("#222")
    ax.zaxis.pane.set_edgecolor("#222")
    ax.grid(True, color="#222", linewidth=0.5)

# ── Maß-Annotations auf Perspektiv-Bild ──────────────────────────
ax0 = axes[0]

# Abmessungen als Textbox
dims_text = (
    f"Platte         : 95 x 182 x 21 mm\n"
    f"Zapfen (1x)    : Ø 75 mm, 49 mm tief\n"
    f"Charger-Mulde  : Ø 74 mm, 9 mm tief\n"
    f"Konsolenbreite : 97 mm  (Spiel: 1 mm)\n"
    f"Kabel-Schlitz  : 11 x 11 mm vorne\n"
    f"Rollo-Luft     : 2 mm  ✓\n"
    f"Material unterm Pad: 12 mm"
)
fig.text(
    0.01, 0.18, dims_text,
    color="#aac8e8", fontsize=8, fontfamily="monospace",
    verticalalignment="bottom",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#0d1a2e", edgecolor="#1a4080", alpha=0.85)
)

note = "!! Vor dem Druck alle Maße am Fahrzeug nachmessen !!"
fig.text(0.5, 0.01, note, ha="center", color="#ff9944", fontsize=9, style="italic")

plt.tight_layout(rect=[0, 0.04, 1, 0.95])

out = os.path.expanduser("~/Downloads/handyhalter_xc60_vorschau.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"✓ Vorschau gespeichert: {out}")
print(f"  Größe: {os.path.getsize(out)//1024} kB")
