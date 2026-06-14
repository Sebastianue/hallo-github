# -*- coding: utf-8 -*-
"""Erzeugt WM-2026-Prognose.md aus wm_data.py."""
import wm_data as D

GROUPS = "ABCDEFGHIJKL"
THIRDS_ADVANCE = "Senegal, Elfenbeinküste, Algerien, Schottland, Türkei, Schweden, Ghana, Iran"
THIRDS_OUT = "Tschechien, Kanada, Saudi-Arabien, DR Kongo"

L = []
w = L.append

w("# WM 2026 – Prognose aller noch zu spielenden Begegnungen\n")
w(f"**Stand:** {D.STAND} · **Turnier:** 11.06.–19.07.2026 in USA, Kanada & Mexiko · 48 Teams, 12 Gruppen (A–L)\n")
w("> ⚠️ **Hinweis:** Subjektive, modellgestützte Schätzungen – **keine** echten Ergebnisse. "
  "Die **Wertigkeit** (%) ist die Verlässlichkeit des Tipps (gestützt auf Buchmacher-Quoten, "
  "FIFA-Rangliste und Turnierform), nicht die mathematische Siegwahrscheinlichkeit. "
  "Hohe Werte nur bei klarem Klassenunterschied; echte 50/50-Spiele bleiben bewusst moderat.\n")

w("---\n\n## Bereits gespielt\n")
w("| Datum | Begegnung | Ergebnis | Gruppe |")
w("|---|---|---|---|")
for datum, beg, erg, grp in D.PLAYED:
    w(f"| {datum} | {beg} | {erg} | {grp} |")
w("")

w("---\n\n## Gruppenphase – noch zu spielende Begegnungen\n")
standings = {row[0]: row[1:] for row in D.STANDINGS}
for g in GROUPS:
    teams = ", ".join(standings[g])
    w(f"### Gruppe {g} — {teams}")
    w("| Datum | ST | Begegnung | Sieger-Tipp | Ergebnis | Wert. | HZ-Führung | HZ-Erg. | HZ-Wert. |")
    w("|---|---|---|---|---|---|---|---|---|")
    for (grp, datum, st, home, away, win, res, wert, played,
         ht_lead, ht_res, ht_wert) in D.GROUP_MATCHES_HT:
        if grp != g or played:
            continue
        d = datum.replace(".2026", ".")
        hzw = "—" if ht_wert is None else f"{ht_wert} %"
        w(f"| {d} | {st} | {home} – {away} | {win} | {res} | {wert} % | {ht_lead} | {ht_res} | {hzw} |")
    w("")
w("*ST = Spieltag*\n")

w("---\n\n## Prognostizierte Qualifikanten für die K.-o.-Phase (32 Teams)\n")
w("**Gruppensieger (12):** " + ", ".join(standings[g][0] for g in GROUPS) + "\n")
w("**Gruppenzweite (12):** " + ", ".join(standings[g][1] for g in GROUPS) + "\n")
w(f"**Beste 8 Gruppendritte (Auswahl):** {THIRDS_ADVANCE}")
w(f"*(ausgeschieden als schwächste Dritte: {THIRDS_OUT})*\n")
w("> ⚠️ Die exakten K.-o.-Paarungen hängen von den Endtabellen und der FIFA-Zuordnung der "
  "acht Gruppendritten ab und lassen sich seriös nicht vorab fixieren. Daher unten eine "
  "Turnierverlaufs-Prognose statt fiktiver exakter Paarungen.\n")

w("---\n\n## K.-o.-Phase – Turnierverlaufs-Prognose\n")
w("| Runde | Datum | Prognose | Wertigkeit |")
w("|---|---|---|---|")
for runde, datum, prog, wert in D.KO:
    w(f"| {runde} | {datum} | {prog} | {wert} % |")
w("")
w("**Titel-Favoriten-Ranking (Buchmacher-Quoten 06/2026):**")
w(" · ".join(f"{rang}. {team} (~{chance} %)" for rang, team, chance in D.RANKING) + "\n")

w("---\n")
w("*Quellen u. a.: FIFA-Weltrangliste, Buchmacher-/Marktquoten (Oddspedia, ESPN, Polymarket), "
  "Transfermarkt-Kaderwerte, Wikipedia, Sky Sports, kicker, sportschau. Prognosen subjektiv und ohne Gewähr.*")

with open("WM-2026-Prognose.md", "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("WM-2026-Prognose.md erstellt")
