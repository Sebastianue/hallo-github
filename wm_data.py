# -*- coding: utf-8 -*-
"""Gemeinsame Datenbasis fuer die WM-2026-Prognose (Quelle fuer Excel und Numbers).

Bei jeder Neuberechnung nur dieses Modul anpassen, dann build_xlsx.py
und build_numbers.py erneut ausfuehren.

Kalibrierung: Wertigkeit gestuetzt auf Buchmacher-Quoten + FIFA-Rangliste
(Stand 06/2026) + bisherige Turnierergebnisse. Hohe Werte nur bei klarem
Klassenunterschied; echte 50/50-Spiele bleiben bewusst moderat.
"""

STAND = "13. Juni 2026 (kalibriert mit Buchmacher-Quoten, FIFA-Rangliste & Transfermarkt-Kaderwerten; nach den Spielen vom 11./12.06.)"

# Bereits gespielte Spiele: (datum, begegnung, ergebnis, gruppe)
PLAYED = [
    ("11.06.", "Mexiko – Südafrika", "2:0", "A"),
    ("11.06.", "Südkorea – Tschechien", "2:1", "A"),
    ("12.06.", "Kanada – Bosnien-Herz.", "1:1", "B"),
    ("12.06.", "USA – Paraguay", "4:1", "D"),
]

# Gruppenspiele: (gruppe, datum, spieltag, heim, gast, sieger, ergebnis, wertigkeit%, gespielt?)
GROUP_MATCHES = [
    ("A", "11.06.2026", 1, "Mexiko", "Südafrika", "Mexiko", "2:0", None, True),
    ("A", "11.06.2026", 1, "Südkorea", "Tschechien", "Südkorea", "2:1", None, True),
    ("A", "18.06.2026", 2, "Mexiko", "Südkorea", "Mexiko", "2:1", 52, False),
    ("A", "18.06.2026", 2, "Tschechien", "Südafrika", "Tschechien", "2:0", 66, False),
    ("A", "24.06.2026", 3, "Mexiko", "Tschechien", "Mexiko", "2:0", 64, False),
    ("A", "24.06.2026", 3, "Südkorea", "Südafrika", "Südkorea", "2:0", 72, False),

    ("B", "12.06.2026", 1, "Kanada", "Bosnien-Herz.", "Unentschieden", "1:1", None, True),
    ("B", "13.06.2026", 1, "Katar", "Schweiz", "Schweiz", "0:2", 72, False),
    ("B", "18.06.2026", 2, "Kanada", "Katar", "Kanada", "2:0", 64, False),
    ("B", "18.06.2026", 2, "Bosnien-Herz.", "Schweiz", "Schweiz", "1:2", 54, False),
    ("B", "24.06.2026", 3, "Kanada", "Schweiz", "Unentschieden", "1:1", 45, False),
    ("B", "24.06.2026", 3, "Bosnien-Herz.", "Katar", "Bosnien-Herz.", "2:0", 64, False),

    ("C", "13.06.2026", 1, "Brasilien", "Marokko", "Brasilien", "2:1", 55, False),
    ("C", "13.06.2026", 1, "Haiti", "Schottland", "Schottland", "0:2", 62, False),
    ("C", "19.06.2026", 2, "Brasilien", "Haiti", "Brasilien", "3:0", 83, False),
    ("C", "19.06.2026", 2, "Marokko", "Schottland", "Marokko", "1:0", 58, False),
    ("C", "24.06.2026", 3, "Brasilien", "Schottland", "Brasilien", "2:0", 74, False),
    ("C", "24.06.2026", 3, "Marokko", "Haiti", "Marokko", "2:0", 77, False),

    ("D", "12.06.2026", 1, "USA", "Paraguay", "USA", "4:1", None, True),
    ("D", "13.06.2026", 1, "Australien", "Türkei", "Türkei", "1:2", 55, False),
    ("D", "19.06.2026", 2, "USA", "Australien", "USA", "2:0", 70, False),
    ("D", "19.06.2026", 2, "Paraguay", "Türkei", "Türkei", "1:2", 55, False),
    ("D", "25.06.2026", 3, "USA", "Türkei", "USA", "2:1", 55, False),
    ("D", "25.06.2026", 3, "Paraguay", "Australien", "Paraguay", "1:0", 50, False),

    ("E", "14.06.2026", 1, "Deutschland", "Curaçao", "Deutschland", "3:0", 88, False),
    ("E", "14.06.2026", 1, "Elfenbeinküste", "Ecuador", "Ecuador", "0:1", 50, False),
    ("E", "20.06.2026", 2, "Deutschland", "Elfenbeinküste", "Deutschland", "2:1", 62, False),
    ("E", "20.06.2026", 2, "Curaçao", "Ecuador", "Ecuador", "0:2", 78, False),
    ("E", "25.06.2026", 3, "Deutschland", "Ecuador", "Deutschland", "2:1", 60, False),
    ("E", "25.06.2026", 3, "Curaçao", "Elfenbeinküste", "Elfenbeinküste", "0:2", 77, False),

    ("F", "14.06.2026", 1, "Niederlande", "Japan", "Niederlande", "2:1", 60, False),
    ("F", "14.06.2026", 1, "Schweden", "Tunesien", "Schweden", "1:0", 55, False),
    ("F", "20.06.2026", 2, "Niederlande", "Schweden", "Niederlande", "2:1", 62, False),
    ("F", "20.06.2026", 2, "Japan", "Tunesien", "Japan", "2:0", 66, False),
    ("F", "25.06.2026", 3, "Niederlande", "Tunesien", "Niederlande", "2:0", 74, False),
    ("F", "25.06.2026", 3, "Japan", "Schweden", "Japan", "2:1", 52, False),

    ("G", "15.06.2026", 1, "Belgien", "Ägypten", "Belgien", "2:1", 62, False),
    ("G", "15.06.2026", 1, "Iran", "Neuseeland", "Iran", "2:0", 70, False),
    ("G", "21.06.2026", 2, "Belgien", "Iran", "Belgien", "2:0", 64, False),
    ("G", "21.06.2026", 2, "Ägypten", "Neuseeland", "Ägypten", "2:0", 70, False),
    ("G", "26.06.2026", 3, "Belgien", "Neuseeland", "Belgien", "3:0", 85, False),
    ("G", "26.06.2026", 3, "Ägypten", "Iran", "Ägypten", "1:0", 48, False),

    ("H", "15.06.2026", 1, "Spanien", "Kap Verde", "Spanien", "3:0", 88, False),
    ("H", "15.06.2026", 1, "Saudi-Arabien", "Uruguay", "Uruguay", "0:2", 66, False),
    ("H", "21.06.2026", 2, "Spanien", "Saudi-Arabien", "Spanien", "3:0", 83, False),
    ("H", "21.06.2026", 2, "Kap Verde", "Uruguay", "Uruguay", "0:2", 73, False),
    ("H", "26.06.2026", 3, "Spanien", "Uruguay", "Spanien", "2:1", 62, False),
    ("H", "26.06.2026", 3, "Kap Verde", "Saudi-Arabien", "Saudi-Arabien", "0:1", 46, False),

    ("I", "16.06.2026", 1, "Frankreich", "Senegal", "Frankreich", "2:1", 58, False),
    ("I", "16.06.2026", 1, "Irak", "Norwegen", "Norwegen", "0:2", 70, False),
    ("I", "22.06.2026", 2, "Frankreich", "Irak", "Frankreich", "3:0", 82, False),
    ("I", "22.06.2026", 2, "Senegal", "Norwegen", "Norwegen", "1:2", 50, False),
    ("I", "26.06.2026", 3, "Frankreich", "Norwegen", "Frankreich", "2:1", 56, False),
    ("I", "26.06.2026", 3, "Senegal", "Irak", "Senegal", "2:0", 72, False),

    ("J", "16.06.2026", 1, "Argentinien", "Algerien", "Argentinien", "2:0", 72, False),
    ("J", "16.06.2026", 1, "Österreich", "Jordanien", "Österreich", "2:0", 68, False),
    ("J", "22.06.2026", 2, "Argentinien", "Österreich", "Argentinien", "2:1", 66, False),
    ("J", "22.06.2026", 2, "Algerien", "Jordanien", "Algerien", "2:0", 64, False),
    ("J", "27.06.2026", 3, "Argentinien", "Jordanien", "Argentinien", "3:0", 88, False),
    ("J", "27.06.2026", 3, "Algerien", "Österreich", "Österreich", "1:2", 50, False),

    ("K", "17.06.2026", 1, "Portugal", "DR Kongo", "Portugal", "2:0", 72, False),
    ("K", "17.06.2026", 1, "Usbekistan", "Kolumbien", "Kolumbien", "0:2", 66, False),
    ("K", "23.06.2026", 2, "Portugal", "Usbekistan", "Portugal", "2:0", 75, False),
    ("K", "23.06.2026", 2, "DR Kongo", "Kolumbien", "Kolumbien", "0:2", 68, False),
    ("K", "27.06.2026", 3, "Portugal", "Kolumbien", "Portugal", "2:1", 54, False),
    ("K", "27.06.2026", 3, "DR Kongo", "Usbekistan", "DR Kongo", "1:0", 52, False),

    ("L", "17.06.2026", 1, "England", "Kroatien", "England", "2:1", 56, False),
    ("L", "17.06.2026", 1, "Ghana", "Panama", "Ghana", "1:0", 56, False),
    ("L", "23.06.2026", 2, "England", "Ghana", "England", "2:0", 72, False),
    ("L", "23.06.2026", 2, "Kroatien", "Panama", "Kroatien", "2:0", 72, False),
    ("L", "27.06.2026", 3, "England", "Panama", "England", "3:0", 85, False),
    ("L", "27.06.2026", 3, "Kroatien", "Ghana", "Kroatien", "2:1", 58, False),
]

# Prognostizierte Endplatzierung: (gruppe, 1., 2., 3., 4.)
STANDINGS = [
    ("A", "Mexiko", "Südkorea", "Tschechien", "Südafrika"),
    ("B", "Schweiz", "Bosnien-Herz.", "Kanada", "Katar"),
    ("C", "Brasilien", "Marokko", "Schottland", "Haiti"),
    ("D", "USA", "Türkei", "Paraguay", "Australien"),
    ("E", "Deutschland", "Ecuador", "Elfenbeinküste", "Curaçao"),
    ("F", "Niederlande", "Japan", "Schweden", "Tunesien"),
    ("G", "Belgien", "Ägypten", "Iran", "Neuseeland"),
    ("H", "Spanien", "Uruguay", "Saudi-Arabien", "Kap Verde"),
    ("I", "Frankreich", "Norwegen", "Senegal", "Irak"),
    ("J", "Argentinien", "Österreich", "Algerien", "Jordanien"),
    ("K", "Portugal", "Kolumbien", "DR Kongo", "Usbekistan"),
    ("L", "England", "Kroatien", "Ghana", "Panama"),
]

# K.-o.-Phase: (runde, datum, prognose, wertigkeit%)
# Top kalibriert mit Buchmacher-Quoten 06/2026 + Transfermarkt-Kaderwerten:
# Frankreich (wertvollster Kader) hauchduenn vor Spanien.
KO = [
    ("Achtelfinale (Best 32)", "28.06.–03.07.2026", "Topnationen ziehen ein", 62),
    ("Achtelfinale (Best 16)", "04.07.–07.07.2026", "FRA, ESP, ENG, BRA, ARG, POR, GER, NED", 52),
    ("Viertelfinale", "09.07.–11.07.2026", "Frankreich, Spanien, England, Argentinien", 46),
    ("Halbfinale 1", "14.07.2026", "Spanien schlägt Argentinien", 40),
    ("Halbfinale 2", "15.07.2026", "Frankreich schlägt England", 39),
    ("Spiel um Platz 3", "18.07.2026", "Argentinien – England 2:1", 35),
    ("Finale", "19.07.2026", "Frankreich – Spanien", 34),
    ("Weltmeister 2026", "19.07.2026", "Frankreich (Finalsieg 2:1)", 20),
]

# Titel-Ranking (Mix aus Buchmacher-Quoten 06/2026 + Transfermarkt-Kaderwert): (rang, team, titelchance%)
RANKING = [
    (1, "Frankreich", 16), (2, "Spanien", 15), (3, "England", 12),
    (4, "Brasilien", 9), (5, "Argentinien", 9), (6, "Portugal", 6),
    (7, "Deutschland", 5), (8, "Niederlande", 4),
]

# Halbzeit-Stand der bereits gespielten Spiele: (heim, gast) -> (fuehrung, hz_ergebnis)
PLAYED_HT = {
    ("Mexiko", "Südafrika"): ("Mexiko", "1:0"),
    ("Südkorea", "Tschechien"): ("Unentschieden", "0:0"),
    ("Kanada", "Bosnien-Herz."): ("Bosnien-Herz.", "0:1"),
    ("USA", "Paraguay"): ("USA", "3:0"),
}


def _half_time(win, res, wert, played, home, away):
    """Leitet Halbzeit-Fuehrung, HZ-Ergebnis und HZ-Wertigkeit ab.
    Heuristik: enge Partien stehen zur Pause meist unentschieden;
    klare Favoriten fuehren knapp. HZ-Tipp ist eigenstaendig (oft stabiler
    als das exakte Endergebnis)."""
    if played:
        lead, hs = PLAYED_HT.get((home, away), ("?", "?"))
        return lead, hs, None
    a, b = (int(x) for x in res.split(":"))
    margin = abs(a - b)
    if wert <= 58:  # enge Partie -> zur Pause haeufig unentschieden
        return "Unentschieden", "0:0", 52
    lead = win
    if margin >= 3:
        hs = "2:0" if a > b else "0:2"
    else:
        hs = "1:0" if a > b else "0:1"
    return lead, hs, max(48, min(70, wert - 12))


# Erweiterte Spielliste inkl. Halbzeit-Feldern (12 Felder):
# (gruppe, datum, spieltag, heim, gast, sieger, ergebnis, wertigkeit%, gespielt,
#  hz_fuehrung, hz_ergebnis, hz_wertigkeit%)
GROUP_MATCHES_HT = [
    (g, d, s, h, a, win, res, wert, played, *_half_time(win, res, wert, played, h, a))
    for (g, d, s, h, a, win, res, wert, played) in GROUP_MATCHES
]
