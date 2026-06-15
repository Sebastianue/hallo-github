# -*- coding: utf-8 -*-
"""Erzeugt WM-2026-Prognose.numbers (Apple Numbers) aus wm_data.py."""
from numbers_parser import Document, RGB
import wm_data as D


def main():
    doc = Document()
    hdr = doc.add_style(bold=True, bg_color=RGB(31, 78, 121), font_color=RGB(255, 255, 255))
    grp = doc.add_style(bold=True, bg_color=RGB(217, 225, 242))
    played_st = doc.add_style(bg_color=RGB(226, 239, 218))

    # ---- Blatt 1: Gruppenphase ----
    sheet = doc.sheets[0]
    sheet.name = "Gruppenphase"
    t = sheet.tables[0]
    t.name = "Gruppenphase"
    headers = ["Gruppe", "Datum", "ST", "Begegnung", "Sieger-Tipp", "HZ-Tipp",
               "Wertigkeit %", "Endstand (echt)", "Treffer", "Erg.-Tipp (unsicher)"]
    for c, h in enumerate(headers):
        t.write(0, c, h)
        t.set_cell_style(0, c, hdr)
    for ri, (g, datum, st, home, away, sieger, erg, wert, hz_lead, hz_score,
             hz_wert, played, endstand, sok, hok) in enumerate(D.GROUP_MATCHES_FULL, start=1):
        treffer = "offen" if not played else ("-" if sok is None else ("OK" if sok else "X"))
        row = [g, datum, st, f"{home} - {away}", sieger,
               hz_lead if hz_lead == "—" else f"{hz_lead} ({hz_score})",
               "—" if wert is None else wert,
               endstand if played else "offen", treffer, erg]
        for c, val in enumerate(row):
            t.write(ri, c, val)
            if played:
                t.set_cell_style(ri, c, played_st)
    t.num_header_rows = 1
    t.num_header_cols = 0

    # ---- Blatt 2: Gruppentabellen ----
    doc.add_sheet("Gruppentabellen", "Gruppentabellen")
    t2 = doc.sheets[-1].tables[0]
    for c, h in enumerate(["Gruppe", "1. Platz", "2. Platz", "3. Platz", "4. Platz (aus)"]):
        t2.write(0, c, h)
        t2.set_cell_style(0, c, hdr)
    for ri, row in enumerate(D.STANDINGS, start=1):
        for c, val in enumerate(row):
            t2.write(ri, c, val)
        t2.set_cell_style(ri, 0, grp)
    t2.num_header_rows = 1
    t2.num_header_cols = 0

    # ---- Blatt 3: K.-o.-Prognose ----
    doc.add_sheet("K.-o.-Prognose", "K.-o.-Prognose")
    t3 = doc.sheets[-1].tables[0]
    for c, h in enumerate(["Runde", "Datum", "Prognose", "Wertigkeit %"]):
        t3.write(0, c, h)
        t3.set_cell_style(0, c, hdr)
    ri = 1
    for runde, datum, prog, wert in D.KO:
        for c, val in enumerate([runde, datum, prog, wert]):
            t3.write(ri, c, val)
        ri += 1
    ri += 1
    t3.write(ri, 0, "Titel-Favoriten-Ranking")
    t3.set_cell_style(ri, 0, grp)
    ri += 1
    for c, h in enumerate(["Rang", "Team", "Titelchance %"]):
        t3.write(ri, c, h)
        t3.set_cell_style(ri, c, hdr)
    ri += 1
    for rang, team, chance in D.RANKING:
        for c, val in enumerate([rang, team, chance]):
            t3.write(ri, c, val)
        ri += 1
    t3.num_header_rows = 1
    t3.num_header_cols = 0

    # ---- Blatt 4: Bilanz ----
    doc.add_sheet("Bilanz", "Bilanz")
    t4 = doc.sheets[-1].tables[0]
    sk, sg, hk, hg, ex, eg = D.review_summary()
    t4.write(0, 0, f"Trefferquote: Sieger {sk}/{sg} (~{round(100*sk/sg)} %) · "
                   f"HZ-Führung {hk}/{hg} (~{round(100*hk/hg)} %) · "
                   f"Exakt {ex}/{eg} (~{round(100*ex/eg)} %)")
    t4.set_cell_style(0, 0, grp)
    for c, h in enumerate(["Datum", "Begegnung", "Sieger-Tipp", "Endstand (echt)", "Sieger", "HZ"]):
        t4.write(2, c, h)
        t4.set_cell_style(2, c, hdr)
    ri = 3
    for (g, datum, st, home, away, sieger, erg, wert, hz_lead, hz_score,
         hz_wert, played, endstand, sok, hok) in D.GROUP_MATCHES_FULL:
        if not played:
            continue
        tipp = sieger if sieger == "—" else f"{sieger} {erg}"
        row = [datum[:6], f"{home} - {away}", tipp, endstand,
               "-" if sok is None else ("OK" if sok else "X"),
               "-" if hok is None else ("OK" if hok else "X")]
        for c, val in enumerate(row):
            t4.write(ri, c, val)
        ri += 1
    t4.num_header_rows = 1
    t4.num_header_cols = 0

    doc.save("WM-2026-Prognose.numbers")
    print("WM-2026-Prognose.numbers erstellt")


if __name__ == "__main__":
    main()
