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

headers = ["Gruppe", "Datum", "Spieltag", "Begegnung", "Sieger-Tipp", "Ergebnis-Tipp", "Wertigkeit"]
hr = 4
for i, h in enumerate(headers, 1):
    ws.cell(row=hr, column=i, value=h)
style_header(ws, hr, 7)

# Daten: (gruppe, datum, spieltag, heim, gast, sieger, ergebnis, wertigkeit, gespielt?)
group_matches = [
    ("A", "11.06.2026", 1, "Mexiko", "Suedafrika", "Mexiko", "2:0", None, True),
    ("A", "11.06.2026", 1, "Suedkorea", "Tschechien", "Suedkorea", "2:1", None, True),
    ("A", "18.06.2026", 2, "Mexiko", "Suedkorea", "Mexiko", "2:1", 55, False),
    ("A", "18.06.2026", 2, "Tschechien", "Suedafrika", "Tschechien", "1:0", 55, False),
    ("A", "24.06.2026", 3, "Mexiko", "Tschechien", "Mexiko", "2:0", 60, False),
    ("A", "24.06.2026", 3, "Suedkorea", "Suedafrika", "Suedkorea", "2:0", 65, False),

    ("B", "12.06.2026", 1, "Kanada", "Bosnien-Herz.", "Bosnien-Herz.", "0:5", None, True),
    ("B", "13.06.2026", 1, "Katar", "Schweiz", "Schweiz", "0:2", 70, False),
    ("B", "18.06.2026", 2, "Kanada", "Katar", "Kanada", "2:0", 60, False),
    ("B", "18.06.2026", 2, "Bosnien-Herz.", "Schweiz", "Schweiz", "1:2", 50, False),
    ("B", "24.06.2026", 3, "Kanada", "Schweiz", "Schweiz", "1:2", 50, False),
    ("B", "24.06.2026", 3, "Bosnien-Herz.", "Katar", "Bosnien-Herz.", "2:0", 62, False),

    ("C", "13.06.2026", 1, "Brasilien", "Marokko", "Brasilien", "2:1", 55, False),
    ("C", "13.06.2026", 1, "Haiti", "Schottland", "Schottland", "0:2", 62, False),
    ("C", "19.06.2026", 2, "Brasilien", "Haiti", "Brasilien", "3:0", 80, False),
    ("C", "19.06.2026", 2, "Marokko", "Schottland", "Marokko", "1:0", 55, False),
    ("C", "24.06.2026", 3, "Brasilien", "Schottland", "Brasilien", "2:0", 70, False),
    ("C", "24.06.2026", 3, "Marokko", "Haiti", "Marokko", "2:0", 75, False),

    ("D", "12.06.2026", 1, "USA", "Paraguay", "USA", "2:1", 52, False),
    ("D", "13.06.2026", 1, "Australien", "Tuerkei", "Tuerkei", "1:2", 55, False),
    ("D", "19.06.2026", 2, "USA", "Australien", "USA", "2:0", 62, False),
    ("D", "19.06.2026", 2, "Paraguay", "Tuerkei", "Tuerkei", "1:2", 53, False),
    ("D", "25.06.2026", 3, "USA", "Tuerkei", "Tuerkei", "1:2", 48, False),
    ("D", "25.06.2026", 3, "Paraguay", "Australien", "Paraguay", "1:0", 52, False),

    ("E", "14.06.2026", 1, "Deutschland", "Curacao", "Deutschland", "3:0", 85, False),
    ("E", "14.06.2026", 1, "Elfenbeinkueste", "Ecuador", "Ecuador", "0:1", 50, False),
    ("E", "20.06.2026", 2, "Deutschland", "Elfenbeinkueste", "Deutschland", "2:1", 62, False),
    ("E", "20.06.2026", 2, "Curacao", "Ecuador", "Ecuador", "0:2", 78, False),
    ("E", "25.06.2026", 3, "Deutschland", "Ecuador", "Deutschland", "2:1", 58, False),
    ("E", "25.06.2026", 3, "Curacao", "Elfenbeinkueste", "Elfenbeinkueste", "0:2", 75, False),

    ("F", "14.06.2026", 1, "Niederlande", "Japan", "Niederlande", "2:1", 58, False),
    ("F", "14.06.2026", 1, "Schweden", "Tunesien", "Schweden", "1:0", 55, False),
    ("F", "20.06.2026", 2, "Niederlande", "Schweden", "Niederlande", "2:1", 60, False),
    ("F", "20.06.2026", 2, "Japan", "Tunesien", "Japan", "2:0", 65, False),
    ("F", "25.06.2026", 3, "Niederlande", "Tunesien", "Niederlande", "2:0", 72, False),
    ("F", "25.06.2026", 3, "Japan", "Schweden", "Japan", "2:1", 52, False),

    ("G", "15.06.2026", 1, "Belgien", "Aegypten", "Belgien", "2:1", 60, False),
    ("G", "15.06.2026", 1, "Iran", "Neuseeland", "Iran", "2:0", 68, False),
    ("G", "21.06.2026", 2, "Belgien", "Iran", "Belgien", "2:0", 62, False),
    ("G", "21.06.2026", 2, "Aegypten", "Neuseeland", "Aegypten", "2:0", 70, False),
    ("G", "26.06.2026", 3, "Belgien", "Neuseeland", "Belgien", "3:0", 82, False),
    ("G", "26.06.2026", 3, "Aegypten", "Iran", "Aegypten", "1:0", 48, False),

    ("H", "15.06.2026", 1, "Spanien", "Kap Verde", "Spanien", "3:0", 85, False),
    ("H", "15.06.2026", 1, "Saudi-Arabien", "Uruguay", "Uruguay", "0:2", 65, False),
    ("H", "21.06.2026", 2, "Spanien", "Saudi-Arabien", "Spanien", "3:0", 80, False),
    ("H", "21.06.2026", 2, "Kap Verde", "Uruguay", "Uruguay", "0:2", 72, False),
    ("H", "26.06.2026", 3, "Spanien", "Uruguay", "Spanien", "2:1", 60, False),
    ("H", "26.06.2026", 3, "Kap Verde", "Saudi-Arabien", "Saudi-Arabien", "0:1", 45, False),

    ("I", "16.06.2026", 1, "Frankreich", "Senegal", "Frankreich", "2:1", 58, False),
    ("I", "16.06.2026", 1, "Irak", "Norwegen", "Norwegen", "0:2", 68, False),
    ("I", "22.06.2026", 2, "Frankreich", "Irak", "Frankreich", "3:0", 80, False),
    ("I", "22.06.2026", 2, "Senegal", "Norwegen", "Norwegen", "1:2", 50, False),
    ("I", "26.06.2026", 3, "Frankreich", "Norwegen", "Frankreich", "2:1", 55, False),
    ("I", "26.06.2026", 3, "Senegal", "Irak", "Senegal", "2:0", 70, False),

    ("J", "16.06.2026", 1, "Argentinien", "Algerien", "Argentinien", "2:0", 70, False),
    ("J", "16.06.2026", 1, "Oesterreich", "Jordanien", "Oesterreich", "2:0", 68, False),
    ("J", "22.06.2026", 2, "Argentinien", "Oesterreich", "Argentinien", "2:1", 65, False),
    ("J", "22.06.2026", 2, "Algerien", "Jordanien", "Algerien", "2:0", 65, False),
    ("J", "27.06.2026", 3, "Argentinien", "Jordanien", "Argentinien", "3:0", 85, False),
    ("J", "27.06.2026", 3, "Algerien", "Oesterreich", "Oesterreich", "1:2", 50, False),

    ("K", "17.06.2026", 1, "Portugal", "DR Kongo", "Portugal", "2:0", 70, False),
    ("K", "17.06.2026", 1, "Usbekistan", "Kolumbien", "Kolumbien", "0:2", 65, False),
    ("K", "23.06.2026", 2, "Portugal", "Usbekistan", "Portugal", "2:0", 72, False),
    ("K", "23.06.2026", 2, "DR Kongo", "Kolumbien", "Kolumbien", "0:2", 68, False),
    ("K", "27.06.2026", 3, "Portugal", "Kolumbien", "Portugal", "2:1", 52, False),
    ("K", "27.06.2026", 3, "DR Kongo", "Usbekistan", "DR Kongo", "1:0", 52, False),

    ("L", "17.06.2026", 1, "England", "Kroatien", "England", "2:1", 55, False),
    ("L", "17.06.2026", 1, "Ghana", "Panama", "Ghana", "1:0", 55, False),
    ("L", "23.06.2026", 2, "England", "Ghana", "England", "2:0", 70, False),
    ("L", "23.06.2026", 2, "Kroatien", "Panama", "Kroatien", "2:0", 70, False),
    ("L", "27.06.2026", 3, "England", "Panama", "England", "3:0", 82, False),
    ("L", "27.06.2026", 3, "Kroatien", "Ghana", "Kroatien", "2:1", 58, False),
]

r = hr + 1
for grp, datum, spieltag, home, away, win, res, wert, played in group_matches:
    ws.cell(row=r, column=1, value=grp).alignment = CENTER
    ws.cell(row=r, column=2, value=datum).alignment = CENTER
    ws.cell(row=r, column=3, value=spieltag).alignment = CENTER
    ws.cell(row=r, column=4, value=f"{home} - {away}").alignment = LEFT
    ws.cell(row=r, column=5, value=(win if not played else f"{win} (gespielt)")).alignment = LEFT
    ws.cell(row=r, column=6, value=res).alignment = CENTER
    wcell = ws.cell(row=r, column=7)
    if played:
        wcell.value = "—"
    else:
        wcell.value = wert / 100.0
        wcell.number_format = "0 %"
    wcell.alignment = CENTER
    for c in range(1, 8):
        cell = ws.cell(row=r, column=c)
        cell.border = BORDER
        if played:
            cell.fill = PLAYED_FILL
    r += 1

ws.column_dimensions["A"].width = 8
ws.column_dimensions["B"].width = 13
ws.column_dimensions["C"].width = 10
ws.column_dimensions["D"].width = 30
ws.column_dimensions["E"].width = 20
ws.column_dimensions["F"].width = 14
ws.column_dimensions["G"].width = 12
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

for i, h in enumerate(["Runde", "Datum", "Prognose", "Wertigkeit"], 1):
    ws3.cell(row=4, column=i, value=h)
style_header(ws3, 4, 4)

ko = [
    ("Achtelfinale (Best 32)", "28.06.-03.07.2026", "Topnationen ziehen ein", 60),
    ("Achtelfinale (Best 16)", "04.07.-07.07.2026", "ARG, FRA, ESP, ENG, BRA, POR, GER, NED", 50),
    ("Viertelfinale", "09.07.-11.07.2026", "ARG, FRA, ESP, ENG weiter", 45),
    ("Halbfinale 1", "14.07.2026", "Argentinien schlaegt Spanien", 40),
    ("Halbfinale 2", "15.07.2026", "Frankreich schlaegt England", 38),
    ("Spiel um Platz 3", "18.07.2026", "Spanien - England 2:1", 35),
    ("Finale", "19.07.2026", "Argentinien - Frankreich", 33),
    ("Weltmeister 2026", "19.07.2026", "Argentinien (Finalsieg 2:1)", 30),
]
r = 5
for runde, datum, prog, wert in ko:
    ws3.cell(row=r, column=1, value=runde).alignment = LEFT
    ws3.cell(row=r, column=2, value=datum).alignment = CENTER
    ws3.cell(row=r, column=3, value=prog).alignment = LEFT
    wc = ws3.cell(row=r, column=4, value=wert / 100.0)
    wc.number_format = "0 %"
    wc.alignment = CENTER
    for c in range(1, 5):
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

for col, w in zip("ABCD", [22, 18, 36, 14]):
    ws3.column_dimensions[col].width = w

wb.save("WM-2026-Prognose.xlsx")
print("WM-2026-Prognose.xlsx erstellt")
