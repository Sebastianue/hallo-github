# -*- coding: utf-8 -*-
"""Erzeugt WM-2026-Prognose.md aus wm_data.py."""
import wm_data as D

GROUPS = "ABCDEFGHIJKL"
THIRDS_ADVANCE = "Senegal, Elfenbeinküste, Algerien, Schottland, Türkei, Schweden, Ghana, Iran"
THIRDS_OUT = "Tschechien, Kanada, Saudi-Arabien, DR Kongo"

L = []
w = L.append


def treffer(played, sok):
    if not played:
        return "offen"
    if sok is None:
        return "–"
    return "✓" if sok else "✗"


w("# WM 2026 – Prognose: Tipp vs. echtes Ergebnis\n")
w(f"**Stand:** {D.STAND} · **Turnier:** 11.06.–19.07.2026 in USA, Kanada & Mexiko · 48 Teams, 12 Gruppen (A–L)\n")
w("> ⚠️ **Fokus auf Sieger- und Halbzeit-Tipp + Wertigkeit (Tendenz).** Das exakte Endergebnis "
  "ist statistisch kaum planbar und steht nur noch als kleine Nebenangabe dabei. In jeder Zeile siehst "
  "du, **was ich getippt habe** und – sobald gespielt – **wie es wirklich ausging** (Spalten Endstand-echt und Treffer).\n")

sk, sg, hk, hg, ex, eg = D.review_summary()
w("**Bisherige Trefferquote:** "
  f"Sieger **{sk}/{sg}** (~{round(100*sk/sg)} %) · "
  f"Halbzeit-Führung **{hk}/{hg}** (~{round(100*hk/hg)} %) · "
  f"exaktes Ergebnis **{ex}/{eg}** (~{round(100*ex/eg)} %)\n")

w("---\n\n## Gruppenphase – Tipps & Ergebnisse\n")
standings = {row[0]: row[1:] for row in D.STANDINGS}
for g in GROUPS:
    teams = ", ".join(standings[g])
    w(f"### Gruppe {g} — {teams}")
    w("| Datum | ST | Begegnung | Sieger-Tipp | HZ-Tipp | Wert. | Endstand (echt) | Treffer | Erg.-Tipp |")
    w("|---|---|---|---|---|---|---|---|---|")
    for (grp, datum, st, home, away, sieger, erg, wert, hz_lead, hz_score,
         hz_wert, played, endstand, sok, hok) in D.GROUP_MATCHES_FULL:
        if grp != g:
            continue
        d = datum.replace(".2026", ".")
        hz = hz_lead if hz_lead == "—" else f"{hz_lead} ({hz_score})"
        wv = "—" if wert is None else f"{wert} %"
        es = endstand if played else "offen"
        w(f"| {d} | {st} | {home} – {away} | {sieger} | {hz} | {wv} | {es} | {treffer(played, sok)} | {erg} |")
    w("")
w("*ST = Spieltag · 'offen' = noch nicht gespielt · Erg.-Tipp = exakter Ergebnis-Tipp (unsicher)*\n")

w("---\n\n## Prognostizierte Qualifikanten für die K.-o.-Phase (32 Teams)\n")
w("**Gruppensieger (12):** " + ", ".join(standings[g][0] for g in GROUPS) + "\n")
w("**Gruppenzweite (12):** " + ", ".join(standings[g][1] for g in GROUPS) + "\n")
w(f"**Beste 8 Gruppendritte (Auswahl):** {THIRDS_ADVANCE}")
w(f"*(ausgeschieden als schwächste Dritte: {THIRDS_OUT})*\n")
w("> ⚠️ Die exakten K.-o.-Paarungen hängen von Endtabellen und FIFA-Zuordnung der acht Dritten ab "
  "und lassen sich seriös nicht vorab fixieren. Daher unten eine Turnierverlaufs-Prognose.\n")

w("---\n\n## K.-o.-Phase – Turnierverlaufs-Prognose\n")
w("| Runde | Datum | Prognose | Wertigkeit |")
w("|---|---|---|---|")
for runde, datum, prog, wert in D.KO:
    w(f"| {runde} | {datum} | {prog} | {wert} % |")
w("")
w("**Titel-Favoriten-Ranking (Buchmacher + Transfermarkt):**")
w(" · ".join(f"{rang}. {team} (~{chance} %)" for rang, team, chance in D.RANKING) + "\n")

w("---\n")
w("*Quellen u. a.: FIFA-Weltrangliste, Buchmacher-/Marktquoten (Oddspedia, ESPN, Polymarket), "
  "Transfermarkt-Kaderwerte, Wikipedia, Sky Sports, kicker, sportschau. Prognosen subjektiv und ohne Gewähr.*")

with open("WM-2026-Prognose.md", "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("WM-2026-Prognose.md erstellt")
