#!/usr/bin/env python3
"""Erzeugt WM-2026-Prognose.xlsx aus den Prognosedaten."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()

# ---- Stile ----
HDR_FILL = PatternFill("solid", fgColor="1F4E78")
HDR_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=14, color="1F4E78")
GRP_FILL = PatternFill("solid", fgColor="D9E1F2")
GRP_FONT = Font(bold=True, size=11, color="1F4E78")
PLAYED_FILL = PatternFill("solid", fgColor="E2EFDA")
CENTER = Alignment(horizontal="center", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center")
WRAP = Alignment(horizontal="left", vertical="center", wrap_text=True)
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HDR_FILL
        cell.font = HDR_FONT
        cell.alignment = CENTER
        cell.border = BORDER

# =====================================================================
# Blatt 1: Gruppenphase
# =====================================================================
ws = wb.active
ws.title = "Gruppenphase"

ws["A1"] = "WM 2026 – Prognose: noch zu spielende Gruppenspiele"
ws["A1"].font = TITLE_FONT
ws.merge_cells("A1:E1")
ws["A2"] = "Stand 12.06.2026 · Wertigkeit = subjektive Verlaesslichkeit des Tipps (keine echte Wahrscheinlichkeit)"
ws["A2"].font = Font(italic=True, size=9, color="808080")
ws.merge_cells("A2:E2")

headers = ["Gruppe", "Begegnung", "Sieger-Tipp", "Ergebnis-Tipp", "Wertigkeit"]
hr = 4
for i, h in enumerate(headers, 1):
    ws.cell(row=hr, column=i, value=h)
style_header(ws, hr, 5)

# Daten: (gruppe, heim, gast, sieger, ergebnis, wertigkeit, gespielt?)
group_matches = [
    ("A", "Mexiko", "Suedafrika", "Mexiko", "2:0", None, True),
    ("A", "Suedkorea", "Tschechien", "Suedkorea", "2:1", None, True),
    ("A", "Mexiko", "Suedkorea", "Mexiko", "2:1", 55, False),
    ("A", "Mexiko", "Tschechien", "Mexiko", "2:0", 60, False),
    ("A", "Suedkorea", "Suedafrika", "Suedkorea", "2:0", 65, False),
    ("A", "Tschechien", "Suedafrika", "Tschechien", "1:0", 55, False),

    ("B", "Kanada", "Bosnien-Herz.", "Bosnien-Herz.", "0:5", None, True),
    ("B", "Katar", "Schweiz", "Schweiz", "0:2", 70, False),
    ("B", "Kanada", "Katar", "Kanada", "2:0", 60, False),
    ("B", "Kanada", "Schweiz", "Schweiz", "1:2", 50, False),
    ("B", "Bosnien-Herz.", "Katar", "Bosnien-Herz.", "2:0", 62, False),
    ("B", "Bosnien-Herz.", "Schweiz", "Schweiz", "1:2", 50, False),

    ("C", "Brasilien", "Marokko", "Brasilien", "2:1", 55, False),
    ("C", "Haiti", "Schottland", "Schottland", "0:2", 62, False),
    ("C", "Brasilien", "Haiti", "Brasilien", "3:0", 80, False),
    ("C", "Brasilien", "Schottland", "Brasilien", "2:0", 70, False),
    ("C", "Marokko", "Haiti", "Marokko", "2:0", 75, False),
    ("C", "Marokko", "Schottland", "Marokko", "1:0", 55, False),

    ("D", "USA", "Paraguay", "USA", "2:1", 52, False),
    ("D", "Australien", "Tuerkei", "Tuerkei", "1:2", 55, False),
    ("D", "USA", "Australien", "USA", "2:0", 62, False),
    ("D", "USA", "Tuerkei", "Tuerkei", "1:2", 48, False),
    ("D", "Paraguay", "Australien", "Paraguay", "1:0", 52, False),
    ("D", "Paraguay", "Tuerkei", "Tuerkei", "1:2", 53, False),

    ("E", "Deutschland", "Curacao", "Deutschland", "3:0", 85, False),
    ("E", "Elfenbeinkueste", "Ecuador", "Ecuador", "0:1", 50, False),
    ("E", "Deutschland", "Elfenbeinkueste", "Deutschland", "2:1", 62, False),
    ("E", "Deutschland", "Ecuador", "Deutschland", "2:1", 58, False),
    ("E", "Curacao", "Elfenbeinkueste", "Elfenbeinkueste", "0:2", 75, False),
    ("E", "Curacao", "Ecuador", "Ecuador", "0:2", 78, False),

    ("F", "Niederlande", "Japan", "Niederlande", "2:1", 58, False),
    ("F", "Schweden", "Tunesien", "Schweden", "1:0", 55, False),
    ("F", "Niederlande", "Schweden", "Niederlande", "2:1", 60, False),
    ("F", "Niederlande", "Tunesien", "Niederlande", "2:0", 72, False),
    ("F", "Japan", "Schweden", "Japan", "2:1", 52, False),
    ("F", "Japan", "Tunesien", "Japan", "2:0", 65, False),

    ("G", "Belgien", "Aegypten", "Belgien", "2:1", 60, False),
    ("G", "Iran", "Neuseeland", "Iran", "2:0", 68, False),
    ("G", "Belgien", "Iran", "Belgien", "2:0", 62, False),
    ("G", "Belgien", "Neuseeland", "Belgien", "3:0", 82, False),
    ("G", "Aegypten", "Iran", "Aegypten", "1:0", 48, False),
    ("G", "Aegypten", "Neuseeland", "Aegypten", "2:0", 70, False),

    ("H", "Spanien", "Kap Verde", "Spanien", "3:0", 85, False),
    ("H", "Saudi-Arabien", "Uruguay", "Uruguay", "0:2", 65, False),
    ("H", "Spanien", "Saudi-Arabien", "Spanien", "3:0", 80, False),
    ("H", "Spanien", "Uruguay", "Spanien", "2:1", 60, False),
    ("H", "Kap Verde", "Saudi-Arabien", "Saudi-Arabien", "0:1", 45, False),
    ("H", "Kap Verde", "Uruguay", "Uruguay", "0:2", 72, False),

    ("I", "Frankreich", "Senegal", "Frankreich", "2:1", 58, False),
    ("I", "Irak", "Norwegen", "Norwegen", "0:2", 68, False),
    ("I", "Frankreich", "Irak", "Frankreich", "3:0", 80, False),
    ("I", "Frankreich", "Norwegen", "Frankreich", "2:1", 55, False),
    ("I", "Senegal", "Irak", "Senegal", "2:0", 70, False),
    ("I", "Senegal", "Norwegen", "Norwegen", "1:2", 50, False),

    ("J", "Argentinien", "Algerien", "Argentinien", "2:0", 70, False),
    ("J", "Oesterreich", "Jordanien", "Oesterreich", "2:0", 68, False),
    ("J", "Argentinien", "Oesterreich", "Argentinien", "2:1", 65, False),
    ("J", "Argentinien", "Jordanien", "Argentinien", "3:0", 85, False),
    ("J", "Algerien", "Oesterreich", "Oesterreich", "1:2", 50, False),
    ("J", "Algerien", "Jordanien", "Algerien", "2:0", 65, False),

    ("K", "Portugal", "DR Kongo", "Portugal", "2:0", 70, False),
    ("K", "Usbekistan", "Kolumbien", "Kolumbien", "0:2", 65, False),
    ("K", "Portugal", "Usbekistan", "Portugal", "2:0", 72, False),
    ("K", "Portugal", "Kolumbien", "Portugal", "2:1", 52, False),
    ("K", "DR Kongo", "Usbekistan", "DR Kongo", "1:0", 52, False),
    ("K", "DR Kongo", "Kolumbien", "Kolumbien", "0:2", 68, False),

    ("L", "England", "Kroatien", "England", "2:1", 55, False),
    ("L", "Ghana", "Panama", "Ghana", "1:0", 55, False),
    ("L", "England", "Ghana", "England", "2:0", 70, False),
    ("L", "England", "Panama", "England", "3:0", 82, False),
    ("L", "Kroatien", "Ghana", "Kroatien", "2:1", 58, False),
    ("L", "Kroatien", "Panama", "Kroatien", "2:0", 70, False),
]

r = hr + 1
for grp, home, away, win, res, wert, played in group_matches:
    ws.cell(row=r, column=1, value=grp).alignment = CENTER
    ws.cell(row=r, column=2, value=f"{home} - {away}").alignment = LEFT
    ws.cell(row=r, column=3, value=(win if not played else f"{win} (gespielt)")).alignment = LEFT
    ws.cell(row=r, column=4, value=res).alignment = CENTER
    wcell = ws.cell(row=r, column=5)
    if played:
        wcell.value = "—"
    else:
        wcell.value = wert / 100.0
        wcell.number_format = "0 %"
    wcell.alignment = CENTER
    for c in range(1, 6):
        cell = ws.cell(row=r, column=c)
        cell.border = BORDER
        if played:
            cell.fill = PLAYED_FILL
    r += 1

ws.column_dimensions["A"].width = 8
ws.column_dimensions["B"].width = 30
ws.column_dimensions["C"].width = 20
ws.column_dimensions["D"].width = 14
ws.column_dimensions["E"].width = 12
ws.freeze_panes = "A5"

# =====================================================================
# Blatt 2: Gruppentabellen-Prognose
# =====================================================================
ws2 = wb.create_sheet("Gruppentabellen-Prognose")
ws2["A1"] = "Prognostizierte Endplatzierungen je Gruppe"
ws2["A1"].font = TITLE_FONT
ws2.merge_cells("A1:E1")
h2 = ["Gruppe", "1. Platz", "2. Platz", "3. Platz", "4. Platz (aus)"]
for i, h in enumerate(h2, 1):
    ws2.cell(row=3, column=i, value=h)
style_header(ws2, 3, 5)

standings = [
    ("A", "Mexiko", "Suedkorea", "Tschechien", "Suedafrika"),
    ("B", "Schweiz", "Bosnien-Herz.", "Kanada", "Katar"),
    ("C", "Brasilien", "Marokko", "Schottland", "Haiti"),
    ("D", "Tuerkei", "USA", "Paraguay", "Australien"),
    ("E", "Deutschland", "Ecuador", "Elfenbeinkueste", "Curacao"),
    ("F", "Niederlande", "Japan", "Schweden", "Tunesien"),
    ("G", "Belgien", "Aegypten", "Iran", "Neuseeland"),
    ("H", "Spanien", "Uruguay", "Saudi-Arabien", "Kap Verde"),
    ("I", "Frankreich", "Norwegen", "Senegal", "Irak"),
    ("J", "Argentinien", "Oesterreich", "Algerien", "Jordanien"),
    ("K", "Portugal", "Kolumbien", "DR Kongo", "Usbekistan"),
    ("L", "England", "Kroatien", "Ghana", "Panama"),
]
r = 4
for row in standings:
    for i, val in enumerate(row, 1):
        cell = ws2.cell(row=r, column=i, value=val)
        cell.border = BORDER
        cell.alignment = CENTER if i == 1 else LEFT
    ws2.cell(row=r, column=1).fill = GRP_FILL
    ws2.cell(row=r, column=1).font = GRP_FONT
    r += 1
for col, w in zip("ABCDE", [8, 16, 16, 16, 16]):
    ws2.column_dimensions[col].width = w

# =====================================================================
# Blatt 3: K.-o.-Phase / Titel
# =====================================================================
ws3 = wb.create_sheet("K.-o.-Prognose")
ws3["A1"] = "K.-o.-Phase – Turnierverlaufs-Prognose"
ws3["A1"].font = TITLE_FONT
ws3.merge_cells("A1:C1")
ws3["A2"] = "Exakte Paarungen haengen von Endtabellen + FIFA-Zuordnung der 8 besten Dritten ab und sind nicht serioes vorab fixierbar."
ws3["A2"].font = Font(italic=True, size=9, color="808080")
ws3.merge_cells("A2:C2")

for i, h in enumerate(["Runde", "Prognose", "Wertigkeit"], 1):
    ws3.cell(row=4, column=i, value=h)
style_header(ws3, 4, 3)

ko = [
    ("Halbfinale 1", "Argentinien schlaegt Spanien", 40),
    ("Halbfinale 2", "Frankreich schlaegt England", 38),
    ("Spiel um Platz 3", "Spanien - England 2:1", 35),
    ("Finale", "Argentinien - Frankreich", 33),
    ("Weltmeister 2026", "Argentinien (Finalsieg 2:1)", 30),
]
r = 5
for runde, prog, wert in ko:
    ws3.cell(row=r, column=1, value=runde).alignment = LEFT
    ws3.cell(row=r, column=2, value=prog).alignment = LEFT
    wc = ws3.cell(row=r, column=3, value=wert / 100.0)
    wc.number_format = "0 %"
    wc.alignment = CENTER
    for c in range(1, 4):
        ws3.cell(row=r, column=c).border = BORDER
    r += 1

# Titel-Ranking
ws3.cell(row=r + 1, column=1, value="Titel-Favoriten-Ranking").font = GRP_FONT
r += 2
for i, h in enumerate(["Rang", "Team", "Titelchance"], 1):
    ws3.cell(row=r, column=i, value=h)
style_header(ws3, r, 3)
r += 1
ranking = [
    (1, "Argentinien", 22), (2, "Frankreich", 18), (3, "Spanien", 15),
    (4, "England", 12), (5, "Brasilien", 10), (6, "Portugal", 7),
    (7, "Deutschland", 6), (8, "Niederlande", 4),
]
for rang, team, chance in ranking:
    ws3.cell(row=r, column=1, value=rang).alignment = CENTER
    ws3.cell(row=r, column=2, value=team).alignment = LEFT
    cc = ws3.cell(row=r, column=3, value=chance / 100.0)
    cc.number_format = "0 %"
    cc.alignment = CENTER
    for c in range(1, 4):
        ws3.cell(row=r, column=c).border = BORDER
    r += 1

for col, w in zip("ABC", [20, 34, 14]):
    ws3.column_dimensions[col].width = w

wb.save("WM-2026-Prognose.xlsx")
print("WM-2026-Prognose.xlsx erstellt")
