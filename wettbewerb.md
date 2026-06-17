# Wettbewerbsanalyse: Spracherkennung / Dokumentation für den OP-Saal (DACH)

*Stand: Juni 2026. Quellen überwiegend 2024–2026.*

> **Kennzeichnung:** `[BELEGT]` = durch Quelle gestützt. `[EINSCHÄTZUNG]` = Schlussfolgerung aus der Recherche.

## TL;DR für Eilige

- **Es gibt eine echte Marktlücke beim OP-Use-Case.** Alle großen Anbieter (Nuance/Microsoft, Solventum, Philips, Abridge, Nabla, Suki) zielen auf **Arztbrief und Arzt-Patient-Gespräch** — **nicht** auf den Operationssaal.
- Der OP existiert bisher nur als **Forschung und Klinik-Einzellösung** (TUM, UKE/ORPHEUS), nicht als Produktkategorie.
- **Fenster ist kurz** (geschätzt 12–24 Monate): Ambient-Anbieter wandern erkennbar in chirurgische Fächer.
- **Die Sprach-Engine muss man nicht selbst bauen** — gute deutsche medizinische Speech-to-Text gibt es als API zu kaufen (z. B. Corti, ~0,0065 $/Audiominute). Der Wert liegt im **OP-/KIS-Integrations-Layer**, nicht in der reinen Texterkennung.
- **„DSGVO / Made in Germany" ist ein Verkaufsargument** im DACH-Markt.

---

## (a) Die wichtigsten Player

| Anbieter | Produkt(e) | Zielgruppe | Modell | OP-spezifisch? |
|---|---|---|---|---|
| **Microsoft / Nuance** | Dragon Medical One, DAX Copilot → **Dragon Copilot** (seit 03/2025) | Diktat + Ambient Arzt-Patient, Arztbrief; Marktführer | Lizenz/Subscription pro Nutzer | Nein |
| **Solventum** (ehem. 3M/M*Modal) | Fluency Direct/Align/Mobile | Notizerstellung in die EHR, alle Fächer | Lizenz, EHR-integriert | Nein |
| **Philips** | SpeechMagic, SpeechLive, SpeechLive Health AI Assistant (03/2026) | Speech-Engine + strukturierte Doku | SaaS / Engine-Lizenz | Nein |
| **Abridge** | Abridge Ambient | Ambient-Doku, >250 Health Systems (Mayo, Duke, Kaiser) | SaaS Enterprise | Nein |
| **Nabla** (Paris) | Nabla Ambient | Ambient-Doku, 85.000 Kliniker; EU-Player | SaaS | Nein |
| **Suki / DeepScribe / Ambience / Augmedix** | Ambient AI Scribes | Arzt-Patient-Doku, fachspezifisch | SaaS | Nein (Ambience optimiert Chirurgie-*Notizen*, nicht intraoperativ) |
| **Augnito** | Spectra, **Speech API/SDK** | Med. Diktat 99,3 %, Vorlagen | **API/SDK** + Lizenz | Nein |
| **Corti** (Dänemark) | **Symphony Speech-to-Text** | **Reine Med-STT-API**, real-time/Ambient/Batch; Deutsch top-gerankt | **API, ~0,0065 $/Min** | Nein, aber idealer Baustein |
| **MediaInterface** (Dresden) | Spracherkennung „Made in Germany" | ~77.800 Nutzer, >600 Kliniken DACH; KIS-integriert | Lizenz, DACH-Marktführer | Nein |
| **IDM gGmbH** | **ORPHEUS** | UKE: Konsile, Visiten, **OP-Berichte per Sprachnachricht** | Lizenz | **Teilweise** |
| **Doc Report AI / Arztbrief.ai** | KI-Arztbrief-Generatoren (DE) | Arztbrief in Min., GOÄ/EBM, ICD-10; Praxis/MVZ | SaaS | Nein |

## (b) Markt-Erfolg & Größe

- **Microsoft kaufte Nuance 2022 für 19,7 Mrd. USD** — zweitgrößter Microsoft-Deal. Nuance-Tech wird laut Microsoft von 55 % der US-Ärzte, 75 % der Radiologen, 77 % der US-Krankenhäuser genutzt. In DE: >80 % der Krankenhäuser. `[BELEGT]`
- **Markt medizinische Spracherkennung:** ~2,6 Mrd. USD (2026) → ~7,5 Mrd. USD (2035), CAGR ~12 %. `[BELEGT]`
- **Markt Ambient Clinical Documentation (Wachstumssegment):** 3,8 Mrd. USD (2025) → 18,6 Mrd. USD (2034). 100 % der US-Health-Systems haben Ambient-AI-Aktivitäten; 34 % der US-Ärzte nutzten Ambient-Scribing Ende 2025. `[BELEGT]`
- **Funding boomt:** Abridge >800 Mio. USD gesamt (Bewertung 5,3 Mrd.), Nabla 120 Mio. (Series C u. a. von HV Capital/DE), Ambience 243 Mio. `[BELEGT]`
- **DACH:** MediaInterface lokal etabliert, Nuance dominiert Befundung. US-Ambient-Scribes hatten lange wenig Traktion in DE (Sprache, DSGVO, KIS-Fragmentierung); ändert sich erst 2025/26 mit deutschen KI-Arztbrief-Startups. `[BELEGT/EINSCHÄTZUNG]`

## (c) Die Lücke beim OP-Use-Case — klares Ja

1. **Kein großer Anbieter hat ein breit ausgerolltes intraoperatives OP-Produkt.** `[BELEGT durch Abwesenheit + Produktbeschreibungen]`
2. OP existiert v. a. als **Forschung/Einzellösung:** RIVD-Studie (intraoperatives Diktat liefert vollständigere OP-Übersicht), TUM MITI („kontextspezifische Spracherkennung im OP"), UKE/ORPHEUS (OP-Bericht per Sprache). `[BELEGT]`
3. **Technische Hürden sind real** (Mikrofon-Abstand, Lärm, mehrere Sprecher, Sterilität) — genau das macht den OP zum unterbedienten Spezialfall (DOMHOS-Projekt, Picovoice). `[BELEGT]`
4. **Aber: Lücke wird sichtbar adressiert** — Ambient-Scribes wandern „upstream" in chirurgische Fächer. OP ist kurz vor dem Wettbewerbsfokus, aber **noch nicht besetzt**. `[BELEGT/EINSCHÄTZUNG]`

## (d) API-fähige Med-STT — Konkurrenz oder Baustein

- **Corti Symphony** — reine Med-STT-API (REST/WebSocket), real-time/Ambient/Batch, Diarisierung & Keyterm-Biasing, ~0,0065 $/Min, **Deutsch top-gerankt (2,4 % WER vs. 13 % beim Nächstbesten)**, 14 Sprachen. `[BELEGT]`
- **Augnito Speech API/SDK** — Plug-and-play, 99,3 % Genauigkeit. `[BELEGT]`
- **Nuance/Microsoft** — Engine via Dragon Medical SDK einbettbar, aber plattform-/lizenzgetrieben. `[BELEGT]`

→ `[EINSCHÄTZUNG]` Die rohe STT muss man nicht selbst bauen; Corti/Augnito als Engine nutzen und sich auf den OP-/KIS-Layer differenzieren.

## (e) Implikation für die Produktidee

1. **Whitespace ist real, aber zeitkritisch** (Fenster ~12–24 Monate).
2. **Moat = OP-/KIS-Layer, nicht die Engine:** Lärm-/Distanz-Robustheit, Multi-Sprecher, Sterilität, OP-Bericht-Strukturierung, tiefe KIS-Integration (Orbis/Dedalus, i.s.h.med/Oracle, CGM — fragmentierter DACH-Markt).
3. **DSGVO / „Made in Germany" als Verkaufsargument** (Erfolg MediaInterface; EU-Engine wie Corti passt).
4. **Risiken:** Microsoft/Nuance kann OP jederzeit auf die Roadmap nehmen; OP technisch hart; lange Klinik-Sales-Zyklen + KIS-Integrationsaufwand.

**Fazit:** Echte, belegbare Lücke (OP-spezifisch, intraoperativ) in stark wachsendem Markt. Beste Positionierung `[EINSCHÄTZUNG]`: OP-/KIS-Integrations-Layer auf zugekaufter EU-Med-STT, mit DSGVO-konformer Verarbeitung als Differenzierung.

---

### Datenlücken (noch zu vertiefen)
- Konkrete deutsche Marktanteile (Nuance vs. MediaInterface) im OP-Segment in keiner Quelle verfügbar → ggf. Analystenreports (KLAS, kma).

### Quellen (Auswahl)
Microsoft Dragon Copilot · Solventum Fluency · Philips SpeechLive Health · Abridge (Fierce Healthcare) · Nabla (PRNewswire) · Augnito API · Corti STT / VentureBeat · MediaInterface · UKE/ORPHEUS · RIVD-Studie (Langenbeck's, Springer) · TUM MITI · CIO.de · KIS-Markt 2026 (kma-online).
