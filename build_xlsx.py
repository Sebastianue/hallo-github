# -*- coding: utf-8 -*-
"""Erzeugt WM-2026-Prognose.xlsx aus wm_data.py."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import wm_data as D

wb = Workbook()

HDR_FILL = PatternFill("solid", fgColor="1F4E78")
HDR_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=14, color="1F4E78")
GRP_FILL = PatternFill("solid", fgColor="D9E1F2")
GRP_FONT = Font(bold=True, size=11, color="1F4E78")
PLAYED_FILL = PatternFill("solid", fgColor="E2EFDA")
CENTER = Alignment(horizontal="center", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HDR_FILL
        cell.font = HDR_FONT
        cell.alignment = CENTER
        cell.border = BORDER


# ---- Blatt 1: Gruppenphase ----
ws = wb.active
ws.title = "Gruppenphase"
ws["A1"] = "WM 2026 – Prognose der Gruppenspiele"
ws["A1"].font = TITLE_FONT
ws.merge_cells("A1:G1")
ws["A2"] = f"Stand {D.STAND} · Wertigkeit = subjektive Verlässlichkeit des Tipps (keine echte Wahrscheinlichkeit)"
ws["A2"].font = Font(italic=True, size=9, color="808080")
ws.merge_cells("A2:G2")

headers = ["Gruppe", "Datum", "Spieltag", "Begegnung", "Sieger-Tipp", "Ergebnis-Tipp", "Wertigkeit"]
hr = 4
for i, h in enumerate(headers, 1):
    ws.cell(row=hr, column=i, value=h)
style_header(ws, hr, 7)

r = hr + 1
for grp, datum, spieltag, home, away, win, res, wert, played in D.GROUP_MATCHES:
    ws.cell(row=r, column=1, value=grp).alignment = CENTER
    ws.cell(row=r, column=2, value=datum).alignment = CENTER
    ws.cell(row=r, column=3, value=spieltag).alignment = CENTER
    ws.cell(row=r, column=4, value=f"{home} - {away}").alignment = LEFT
    ws.cell(row=r, column=5, value=(f"{win} (gespielt)" if played else win)).alignment = LEFT
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

for col, w in zip("ABCDEFG", [8, 13, 10, 30, 20, 14, 12]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "A5"

# ---- Blatt 2: Gruppentabellen-Prognose ----
ws2 = wb.create_sheet("Gruppentabellen-Prognose")
ws2["A1"] = "Prognostizierte Endplatzierungen je Gruppe"
ws2["A1"].font = TITLE_FONT
ws2.merge_cells("A1:E1")
for i, h in enumerate(["Gruppe", "1. Platz", "2. Platz", "3. Platz", "4. Platz (aus)"], 1):
    ws2.cell(row=3, column=i, value=h)
style_header(ws2, 3, 5)
r = 4
for row in D.STANDINGS:
    for i, val in enumerate(row, 1):
        cell = ws2.cell(row=r, column=i, value=val)
        cell.border = BORDER
        cell.alignment = CENTER if i == 1 else LEFT
    ws2.cell(row=r, column=1).fill = GRP_FILL
    ws2.cell(row=r, column=1).font = GRP_FONT
    r += 1
for col, w in zip("ABCDE", [8, 16, 16, 16, 16]):
    ws2.column_dimensions[col].width = w

# ---- Blatt 3: K.-o.-Prognose ----
ws3 = wb.create_sheet("K.-o.-Prognose")
ws3["A1"] = "K.-o.-Phase – Turnierverlaufs-Prognose"
ws3["A1"].font = TITLE_FONT
ws3.merge_cells("A1:D1")
ws3["A2"] = "Exakte Paarungen hängen von Endtabellen + FIFA-Zuordnung der 8 besten Dritten ab und sind nicht seriös vorab fixierbar."
ws3["A2"].font = Font(italic=True, size=9, color="808080")
ws3.merge_cells("A2:D2")
for i, h in enumerate(["Runde", "Datum", "Prognose", "Wertigkeit"], 1):
    ws3.cell(row=4, column=i, value=h)
style_header(ws3, 4, 4)
r = 5
for runde, datum, prog, wert in D.KO:
    ws3.cell(row=r, column=1, value=runde).alignment = LEFT
    ws3.cell(row=r, column=2, value=datum).alignment = CENTER
    ws3.cell(row=r, column=3, value=prog).alignment = LEFT
    wc = ws3.cell(row=r, column=4, value=wert / 100.0)
    wc.number_format = "0 %"
    wc.alignment = CENTER
    for c in range(1, 5):
        ws3.cell(row=r, column=c).border = BORDER
    r += 1

ws3.cell(row=r + 1, column=1, value="Titel-Favoriten-Ranking").font = GRP_FONT
r += 2
for i, h in enumerate(["Rang", "Team", "Titelchance"], 1):
    ws3.cell(row=r, column=i, value=h)
style_header(ws3, r, 3)
r += 1
for rang, team, chance in D.RANKING:
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
