# -*- coding: utf-8 -*-
"""Gemeinsame Datenbasis fuer die WM-2026-Prognose (Quelle fuer Excel, Numbers, Markdown).

Aufbau:
- GROUP_MATCHES: enthaelt IMMER nur den TIPP (Sieger, exaktes Ergebnis, Wertigkeit).
- ACTUAL: echtes Resultat eines Spiels, sobald gespielt -> (Endstand, Sieger, HZ-Fuehrung, HZ-Stand).
- GROUP_MATCHES_FULL: kombiniert Tipp + echtes Ergebnis + Treffer-Check (von den Buildern genutzt).

Bei jeder Neuberechnung: Tipps in GROUP_MATCHES und Ergebnisse in ACTUAL pflegen.
Kalibrierung: Buchmacher-Quoten + FIFA-Rangliste + Transfermarkt-Kaderwerte + Turnierform.
Fokus liegt auf Sieger- und Halbzeit-Tipp; das exakte Endergebnis ist statistisch kaum planbar.
"""

STAND = "19. Juni 2026 (kalibriert mit Buchmacher-Quoten, FIFA-Rangliste & Transfermarkt-Kaderwerten; nach allen Spielen bis 19.06.)"

# TIPPS je Spiel: (gruppe, datum, spieltag, heim, gast, sieger_tipp, ergebnis_tipp, wertigkeit%)
# sieger_tipp == "Unentschieden" fuer Remis-Tipp, "—" = kein Tipp abgegeben.
GROUP_MATCHES = [
    ("A", "11.06.2026", 1, "Mexiko", "Südafrika", "Mexiko", "2:0", 60),
    ("A", "11.06.2026", 1, "Südkorea", "Tschechien", "Südkorea", "2:1", 60),
    ("A", "18.06.2026", 2, "Mexiko", "Südkorea", "Mexiko", "2:1", 52),
    ("A", "18.06.2026", 2, "Tschechien", "Südafrika", "Tschechien", "2:0", 66),
    ("A", "24.06.2026", 3, "Mexiko", "Tschechien", "Mexiko", "2:0", 64),
    ("A", "24.06.2026", 3, "Südkorea", "Südafrika", "Südkorea", "2:0", 72),

    ("B", "12.06.2026", 1, "Kanada", "Bosnien-Herz.", "—", "—", None),
    ("B", "13.06.2026", 1, "Katar", "Schweiz", "Schweiz", "0:2", 72),
    ("B", "18.06.2026", 2, "Kanada", "Katar", "Kanada", "2:0", 64),
    ("B", "18.06.2026", 2, "Bosnien-Herz.", "Schweiz", "Schweiz", "1:2", 54),
    ("B", "24.06.2026", 3, "Kanada", "Schweiz", "Unentschieden", "1:1", 45),
    ("B", "24.06.2026", 3, "Bosnien-Herz.", "Katar", "Bosnien-Herz.", "2:0", 64),

    ("C", "13.06.2026", 1, "Brasilien", "Marokko", "Brasilien", "2:1", 55),
    ("C", "13.06.2026", 1, "Haiti", "Schottland", "Schottland", "0:2", 62),
    ("C", "19.06.2026", 2, "Brasilien", "Haiti", "Brasilien", "3:0", 83),
    ("C", "19.06.2026", 2, "Marokko", "Schottland", "Marokko", "1:0", 58),
    ("C", "24.06.2026", 3, "Brasilien", "Schottland", "Brasilien", "2:0", 74),
    ("C", "24.06.2026", 3, "Marokko", "Haiti", "Marokko", "2:0", 77),

    ("D", "12.06.2026", 1, "USA", "Paraguay", "USA", "2:1", 52),
    ("D", "13.06.2026", 1, "Australien", "Türkei", "Türkei", "1:2", 55),
    ("D", "19.06.2026", 2, "USA", "Australien", "USA", "2:1", 58),
    ("D", "19.06.2026", 2, "Paraguay", "Türkei", "Türkei", "1:2", 50),
    ("D", "25.06.2026", 3, "USA", "Türkei", "USA", "2:1", 58),
    ("D", "25.06.2026", 3, "Paraguay", "Australien", "Australien", "1:2", 48),

    ("E", "14.06.2026", 1, "Deutschland", "Curaçao", "Deutschland", "3:0", 88),
    ("E", "14.06.2026", 1, "Elfenbeinküste", "Ecuador", "Ecuador", "0:1", 50),
    ("E", "20.06.2026", 2, "Deutschland", "Elfenbeinküste", "Deutschland", "2:1", 56),
    ("E", "20.06.2026", 2, "Curaçao", "Ecuador", "Ecuador", "0:2", 78),
    ("E", "25.06.2026", 3, "Deutschland", "Ecuador", "Deutschland", "2:1", 60),
    ("E", "25.06.2026", 3, "Curaçao", "Elfenbeinküste", "Elfenbeinküste", "0:2", 77),

    ("F", "14.06.2026", 1, "Niederlande", "Japan", "Niederlande", "2:1", 60),
    ("F", "14.06.2026", 1, "Schweden", "Tunesien", "Schweden", "1:0", 55),
    ("F", "20.06.2026", 2, "Niederlande", "Schweden", "Niederlande", "2:1", 56),
    ("F", "20.06.2026", 2, "Japan", "Tunesien", "Japan", "2:0", 66),
    ("F", "25.06.2026", 3, "Niederlande", "Tunesien", "Niederlande", "2:0", 74),
    ("F", "25.06.2026", 3, "Japan", "Schweden", "Japan", "2:1", 52),

    ("G", "15.06.2026", 1, "Belgien", "Ägypten", "Belgien", "2:1", 62),
    ("G", "15.06.2026", 1, "Iran", "Neuseeland", "Iran", "2:0", 70),
    ("G", "21.06.2026", 2, "Belgien", "Iran", "Belgien", "2:0", 64),
    ("G", "21.06.2026", 2, "Ägypten", "Neuseeland", "Ägypten", "2:0", 70),
    ("G", "26.06.2026", 3, "Belgien", "Neuseeland", "Belgien", "3:0", 85),
    ("G", "26.06.2026", 3, "Ägypten", "Iran", "Ägypten", "1:0", 48),

    ("H", "15.06.2026", 1, "Spanien", "Kap Verde", "Spanien", "3:0", 88),
    ("H", "15.06.2026", 1, "Saudi-Arabien", "Uruguay", "Uruguay", "0:2", 66),
    ("H", "21.06.2026", 2, "Spanien", "Saudi-Arabien", "Spanien", "3:0", 83),
    ("H", "21.06.2026", 2, "Kap Verde", "Uruguay", "Uruguay", "0:2", 73),
    ("H", "26.06.2026", 3, "Spanien", "Uruguay", "Spanien", "2:1", 62),
    ("H", "26.06.2026", 3, "Kap Verde", "Saudi-Arabien", "Saudi-Arabien", "0:1", 46),

    ("I", "16.06.2026", 1, "Frankreich", "Senegal", "Frankreich", "2:1", 58),
    ("I", "16.06.2026", 1, "Irak", "Norwegen", "Norwegen", "0:2", 70),
    ("I", "22.06.2026", 2, "Frankreich", "Irak", "Frankreich", "3:0", 82),
    ("I", "22.06.2026", 2, "Senegal", "Norwegen", "Norwegen", "1:2", 50),
    ("I", "26.06.2026", 3, "Frankreich", "Norwegen", "Frankreich", "2:1", 56),
    ("I", "26.06.2026", 3, "Senegal", "Irak", "Senegal", "2:0", 72),

    ("J", "16.06.2026", 1, "Argentinien", "Algerien", "Argentinien", "2:0", 72),
    ("J", "16.06.2026", 1, "Österreich", "Jordanien", "Österreich", "2:0", 68),
    ("J", "22.06.2026", 2, "Argentinien", "Österreich", "Argentinien", "2:1", 66),
    ("J", "22.06.2026", 2, "Algerien", "Jordanien", "Algerien", "2:0", 64),
    ("J", "27.06.2026", 3, "Argentinien", "Jordanien", "Argentinien", "3:0", 88),
    ("J", "27.06.2026", 3, "Algerien", "Österreich", "Österreich", "1:2", 50),

    ("K", "17.06.2026", 1, "Portugal", "DR Kongo", "Portugal", "2:0", 72),
    ("K", "17.06.2026", 1, "Usbekistan", "Kolumbien", "Kolumbien", "0:2", 66),
    ("K", "23.06.2026", 2, "Portugal", "Usbekistan", "Portugal", "2:0", 75),
    ("K", "23.06.2026", 2, "DR Kongo", "Kolumbien", "Kolumbien", "0:2", 68),
    ("K", "27.06.2026", 3, "Portugal", "Kolumbien", "Portugal", "2:1", 54),
    ("K", "27.06.2026", 3, "DR Kongo", "Usbekistan", "DR Kongo", "1:0", 52),

    ("L", "17.06.2026", 1, "England", "Kroatien", "England", "2:1", 56),
    ("L", "17.06.2026", 1, "Ghana", "Panama", "Ghana", "1:0", 56),
    ("L", "23.06.2026", 2, "England", "Ghana", "England", "2:0", 72),
    ("L", "23.06.2026", 2, "Kroatien", "Panama", "Kroatien", "2:0", 72),
    ("L", "27.06.2026", 3, "England", "Panama", "England", "3:0", 85),
    ("L", "27.06.2026", 3, "Kroatien", "Ghana", "Kroatien", "2:1", 58),
]

# ECHTE Resultate gespielter Spiele: (heim, gast) -> (endstand, sieger, hz_fuehrung, hz_stand)
ACTUAL = {
    ("Mexiko", "Südafrika"): ("2:0", "Mexiko", "Mexiko", "1:0"),
    ("Südkorea", "Tschechien"): ("2:1", "Südkorea", "Unentschieden", "0:0"),
    ("Kanada", "Bosnien-Herz."): ("1:1", "Unentschieden", "Bosnien-Herz.", "0:1"),
    ("USA", "Paraguay"): ("4:1", "USA", "USA", "3:0"),
    ("Katar", "Schweiz"): ("1:1", "Unentschieden", "Schweiz", "0:1"),
    ("Brasilien", "Marokko"): ("1:1", "Unentschieden", "Unentschieden", "1:1"),
    ("Haiti", "Schottland"): ("0:1", "Schottland", "Schottland", "0:1"),
    ("Australien", "Türkei"): ("2:0", "Australien", "Australien", "1:0"),
    ("Deutschland", "Curaçao"): ("7:1", "Deutschland", "Deutschland", "3:1"),
    ("Elfenbeinküste", "Ecuador"): ("1:0", "Elfenbeinküste", "Unentschieden", "0:0"),
    ("Niederlande", "Japan"): ("2:2", "Unentschieden", "Unentschieden", "0:0"),
    ("Schweden", "Tunesien"): ("5:1", "Schweden", "Schweden", "2:1"),
    ("Belgien", "Ägypten"): ("1:1", "Unentschieden", None, None),
    ("Iran", "Neuseeland"): ("2:2", "Unentschieden", None, None),
    ("Spanien", "Kap Verde"): ("0:0", "Unentschieden", "Unentschieden", "0:0"),
    ("Saudi-Arabien", "Uruguay"): ("1:1", "Unentschieden", "Saudi-Arabien", "1:0"),
    ("Frankreich", "Senegal"): ("3:1", "Frankreich", None, None),
    ("Irak", "Norwegen"): ("1:4", "Norwegen", None, None),
    ("Argentinien", "Algerien"): ("3:0", "Argentinien", None, None),
    ("Österreich", "Jordanien"): ("3:1", "Österreich", None, None),
    ("Portugal", "DR Kongo"): ("1:1", "Unentschieden", None, None),
    ("Usbekistan", "Kolumbien"): ("1:3", "Kolumbien", None, None),
    ("England", "Kroatien"): ("4:2", "England", None, None),
    ("Ghana", "Panama"): ("1:0", "Ghana", None, None),
    ("Tschechien", "Südafrika"): ("1:1", "Unentschieden", None, None),
    ("Mexiko", "Südkorea"): ("1:0", "Mexiko", None, None),
    ("Bosnien-Herz.", "Schweiz"): ("1:4", "Schweiz", None, None),
    ("Kanada", "Katar"): ("6:0", "Kanada", None, None),
    ("Marokko", "Schottland"): ("1:0", "Marokko", None, None),
    ("Brasilien", "Haiti"): ("3:0", "Brasilien", None, None),
    ("USA", "Australien"): ("2:0", "USA", None, None),
    ("Paraguay", "Türkei"): ("1:0", "Paraguay", None, None),
}


def _half_time_tip(sieger, erg, wert):
    """HZ-Tipp (Fuehrung, Stand, Wertigkeit) aus dem FT-Tipp ableiten.
    Enge Partien -> zur Pause meist unentschieden; klare Favoriten fuehren knapp."""
    if sieger == "—":
        return "—", "—", None
    if sieger == "Unentschieden":
        return "Unentschieden", "0:0", 52
    a, b = (int(x) for x in erg.split(":"))
    margin = abs(a - b)
    if wert is not None and wert <= 58:
        return "Unentschieden", "0:0", 52
    if margin >= 3:
        hs = "2:0" if a > b else "0:2"
    else:
        hs = "1:0" if a > b else "0:1"
    hw = max(48, min(70, wert - 12)) if wert else None
    return sieger, hs, hw


def _build_full():
    rows = []
    for g, datum, st, home, away, sieger, erg, wert in GROUP_MATCHES:
        hz_lead, hz_score, hz_wert = _half_time_tip(sieger, erg, wert)
        played = (home, away) in ACTUAL
        endstand = sieger_ok = hz_ok = None
        if played:
            endstand, real_winner, real_hz_lead, _ = ACTUAL[(home, away)]
            if sieger != "—":
                sieger_ok = (sieger == real_winner)
                if real_hz_lead is not None:
                    hz_ok = (hz_lead == real_hz_lead)
        rows.append((g, datum, st, home, away, sieger, erg, wert,
                     hz_lead, hz_score, hz_wert, played, endstand, sieger_ok, hz_ok))
    return rows


GROUP_MATCHES_FULL = _build_full()


def review_summary():
    """(sieger_korrekt, sieger_gesamt, hz_korrekt, hz_gesamt, exakt_korrekt, exakt_gesamt)."""
    sk = sg = hk = hg = ex = eg = 0
    for r in GROUP_MATCHES_FULL:
        sieger, erg, played, endstand, sok, hok = r[5], r[6], r[11], r[12], r[13], r[14]
        if played and sok is not None:
            sg += 1
            sk += 1 if sok else 0
            eg += 1
            ex += 1 if erg == endstand else 0
        if played and hok is not None:
            hg += 1
            hk += 1 if hok else 0
    return sk, sg, hk, hg, ex, eg


# Prognostizierte Endplatzierung: (gruppe, 1., 2., 3., 4.)
STANDINGS = [
    ("A", "Mexiko", "Südkorea", "Tschechien", "Südafrika"),
    ("B", "Kanada", "Schweiz", "Bosnien-Herz.", "Katar"),
    ("C", "Brasilien", "Marokko", "Schottland", "Haiti"),
    ("D", "USA", "Australien", "Paraguay", "Türkei"),
    ("E", "Deutschland", "Elfenbeinküste", "Ecuador", "Curaçao"),
    ("F", "Niederlande", "Schweden", "Japan", "Tunesien"),
    ("G", "Belgien", "Ägypten", "Iran", "Neuseeland"),
    ("H", "Spanien", "Uruguay", "Saudi-Arabien", "Kap Verde"),
    ("I", "Frankreich", "Norwegen", "Senegal", "Irak"),
    ("J", "Argentinien", "Österreich", "Algerien", "Jordanien"),
    ("K", "Portugal", "Kolumbien", "DR Kongo", "Usbekistan"),
    ("L", "England", "Kroatien", "Ghana", "Panama"),
]

# K.-o.-Phase: (runde, datum, prognose, wertigkeit%)
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

# Titel-Ranking (Buchmacher-Quoten + Transfermarkt-Kaderwert): (rang, team, titelchance%)
RANKING = [
    (1, "Frankreich", 16), (2, "Spanien", 15), (3, "England", 12),
    (4, "Brasilien", 9), (5, "Argentinien", 9), (6, "Portugal", 6),
    (7, "Deutschland", 5), (8, "Niederlande", 4),
]
