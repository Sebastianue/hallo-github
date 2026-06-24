# Kandidaten-Bewertung: ORPHEUS &amp; Sally.io (Partner-Optionen)

*Stand: Juni 2026. Quellen 2024–2026. Legende: **[BELEGT]** = durch Quelle gedeckt · **[EINSCHÄTZUNG]** = eigene Bewertung.*

> **Kernaussage:** Wir bauen die Sprach-Engine nicht selbst, sondern wollen einen **Partner in unser System integrieren**. **ORPHEUS** und **Sally.io** sind die zwei Kandidaten dafür. Sie sind unterschiedlich gelagert: ORPHEUS ist **klinisch erprobt** (nah am OP-Use-Case), aber weniger flexibel; Sally.io ist **sehr anpassungsfähig**, aber bislang nur im **Konferenz-/Meeting-Bereich** tätig (kein Medizin-/OP-/KIS-Bezug). In beiden Fällen ergänzen **wir** den OP-Live-/KIS-Layer (sterile Live-Doku + strukturierte API).

---

## Steckbrief ORPHEUS

- **Anbieter:** IDM gGmbH (Innovative Digitale Medizin), gemeinnützige UKE-Ausgründung (Universitätsklinikum Hamburg-Eppendorf), gegr. 2024. **[BELEGT]**
- **Was es ist:** Medizinische KI-Spracherkennung (Sprache→Text), trainiert auf Fachterminologie; für alle Berufsgruppen. **[BELEGT]**
- **Funktionsumfang:** Diktat von Konsilen, Visiten, Befunden und **OP-Berichten** per Sprachnachricht; schreibt „an jeder Cursorposition" in jedes KIS/PVS, Word, E-Mail. **[BELEGT]**
- **OP-Eignung:** **Teilweise.** OP-**Berichte** per Diktat sind explizit dabei — aber **keine belegte sterile, hands-free, intraoperative Live-Dokumentation im OP-Saal.** **[BELEGT / EINSCHÄTZUNG]**
- **KIS-Integration:** Modell „**keine Schnittstellen, keine Konnektoren**" — universelle Texteingabe an Cursorposition. Eine **echte strukturierte API (HL7/FHIR)** ist im Material **nicht belegt** → bei IDM nachfragen. **[BELEGT / offene Frage]**
- **Datenschutz / Hosting:** Betrieb **ausschließlich in Deutschland**; on-premise (eigene GPUs), STACKIT-Cloud oder GWDG; keine internationalen Clouds; DSGVO. **[BELEGT]** → starkes Souveränitätsprofil.
- **Reifegrad / Verbreitung:** Produktiv seit Anfang 2025 am UKE; an **4 Unikliniken, 30+ weiteren Kliniken, 200+ ambulanten Einrichtungen**; ~**4,5 Mio. Audiodateien** transkribiert. **[BELEGT]** → im echten Klinikbetrieb bewährt.
- **Preis:** Kommerziell verfügbar, „fairer Preis" beworben — **keine öffentlichen Preise**. **[BELEGT]**
- **Verwandtes Produkt ARGO:** Generiert automatisch **Arztbrief-/Epikrise-Entwürfe** aus der Patientenakte. Zeigt: IDM geht über reine Spracherkennung hinaus Richtung strukturierter Dokumentation. **[BELEGT]**

## Steckbrief „Sally" (= Sally.io)

- **Anbieter:** Aliru GmbH, Mannheim (seit 2015). **[BELEGT]**
- **Was es ist:** Allgemeiner **KI-Meeting-Assistent** — Transkription, Zusammenfassungen, Task-Extraktion. **[BELEGT]**
- **Technik:** 98,8 % Genauigkeit, 103 Sprachen. **[BELEGT]**
- **Zielgruppe:** Office / Sales / Wissensarbeit; >50.000 Nutzer in >1.000 Unternehmen. **Kein Medizin-/Klinik-/OP-Bezug.** **[BELEGT]**
- **Integration:** 8.000+ Tools (HubSpot, Salesforce, Slack, Asana) — Office/CRM-Ökosystem, **kein KIS / HL7 / FHIR.** **[BELEGT]**
- **Datenschutz / Hosting:** DSGVO, AVV (Art. 28), deutsche Rechenzentren (Hetzner), EU-only, Daten-Masking vor LLM, ISO 27001/9001/14001. **[BELEGT]** → solides „Made in Germany", aber **nicht medizinisch zertifiziert**.
- **OP-/klinischer Use-Case:** **Nein.** **[BELEGT / EINSCHÄTZUNG]**

> ⚠️ **Namensverwechslung möglich:** Es gibt kein eigenständiges *medizinisches* „Sally" im DACH-Markt. Verwechslungskandidat ist **Sully.ai** (US-Healthcare-Scribe, andere Schreibweise). Falls intern ein klinisches „Sally" gemeint war → Quelle nachreichen.

---

## Vergleichstabelle

| Kriterium | **ORPHEUS (IDM / UKE)** | **Sally.io (Aliru, Mannheim)** |
|---|---|---|
| Kategorie | Medizinische KI-Spracherkennung | Allgemeiner Meeting-Assistent |
| Medizin-/Klinik-Fokus | **Ja** (Kerngeschäft) | **Nein** (Office/Sales) |
| OP-/intraoperative Doku | **Teilweise** (OP-Berichte per Diktat) | **Nein** |
| KIS-Integration | „Cursor-überall"; strukturierte API unklar | Office/CRM, **kein KIS** |
| Datenschutz/Hosting | DE-only; on-prem / STACKIT / GWDG | DE/EU (Hetzner); DSGVO; AVV |
| „Made in Germany" | **Ja** | **Ja** |
| Reifegrad (Klinik) | Hoch: UKE + 30+ Kliniken, 4,5 Mio. Audios | **0 Klinikrelevanz** |
| Öffentliche Preise | Nein | Teilweise (SaaS) |
| Rolle für uns | **Partner-Kandidat A** (klinisch erprobt) | **Partner-Kandidat B** (anpassbar, Konferenz-Herkunft) |

---

## Einordnung & Empfehlung

Beide sind **Partner-Kandidaten** für unser Vorhaben (Engine in unser System integrieren) — mit gegensätzlichen Profilen:

**ORPHEUS — der klinisch erprobte Kandidat. [EINSCHÄTZUNG]**
- **Stärke:** medizinisch trainiert, DE-souverän, breit im Klinikbetrieb, schon mit OP-Bezug (OP-Berichte). Kürzester Weg zu klinischer Glaubwürdigkeit.
- **Offen:** sterile intraoperative Live-Doku und eine echte strukturierte KIS-API sind nicht belegt → genau der Layer, den **wir** ergänzen.
- **Partnerlogik:** IDM ist gemeinnützig und stellt Anwendungen anderen Kliniken bereit → Kooperationsgespräch naheliegend.

**Sally.io — der anpassbare Kandidat. [EINSCHÄTZUNG]**
- **Stärke:** sehr flexibel/anpassbar, starke API-/Integrations-DNA, DSGVO/EU, „Made in Germany". Könnte viel für uns umsetzen.
- **Offen:** bisher **nur Konferenzen/Meetings** — kein Medizin-/OP-/KIS-Bezug. Müsste für den klinischen/OP-Einsatz **substanziell angepasst** werden (Fachterminologie, OP-Akustik, KIS, regulatorisch).
- **Partnerlogik:** als Entwicklungs-/Anpassungspartner denkbar, der mit uns in den klinischen Markt geht.

**Kurz:** ORPHEUS = Geschwindigkeit & klinische Reife; Sally.io = Flexibilität & Anpassbarkeit. In beiden Fällen liegt **unser** Mehrwert im OP-Live-/KIS-Layer.

## Offene Fragen an beide Partner (für die Gespräche)
1. **ORPHEUS/IDM:** Echte strukturierte API (HL7/FHIR) über „Cursor-überall" hinaus? Verhalten unter realer OP-Akustik / sterile Live-Doku? Lizenz-/Partnermodell & Preise?
2. **Sally.io/Aliru:** Bereitschaft & Aufwand für medizinische Anpassung (Fachterminologie, OP, KIS-Integration, regulatorisch)? Roadmap, Exklusivität, Konditionen?

### Quellen (Auswahl)
IDM/ORPHEUS: idmedizin.de · medinfoweb.de · heise.de (UKE-Ausgründung) · uke.de (Digitale Helfer 2026, ARGO-PM) · gesundheitswirtschaft.at. Sally: sally.io (Start, About, GDPR). Verwechslung: sully.ai / ycombinator.com.
*Hinweis: idmedizin.de, heise.de, sally.io lieferten teils HTTP 403; Fakten aus konsistenten Suchindex-Snippets. Für die Partnerphase direkt bei IDM verifizieren.*
